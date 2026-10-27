"""Read-only official artifact qualification; writes evidence and private caches.

Does not invoke model scripts, docker/podman, provision services or execute binaries.
All failed/incomplete attempts are retained. Public registry bearer tokens and signed
download redirect URLs are never persisted in evidence.
"""
from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone, timedelta
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import re
import shutil
import subprocess
import posixpath
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'internal/evidence/w0/artifacts'
CACHE = Path(r'D:\Cephalon\.tools')
ACCEPT = ', '.join(['application/vnd.oci.image.index.v1+json', 'application/vnd.docker.distribution.manifest.list.v2+json', 'application/vnd.oci.image.manifest.v1+json', 'application/vnd.docker.distribution.manifest.v2+json'])
USER_AGENT = 'Cehpalon-W0-artifact-qualification/1.0'
MODELS = [
    {'name': 'Qwen3-4B-Q4_K_M.gguf', 'repo': 'Qwen/Qwen3-4B-GGUF', 'revision': 'bc640142c66e1fdd12af0bd68f40445458f3869b', 'size': 2497280256, 'sha256': '7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5'},
    {'name': 'Qwen3-Embedding-0.6B-Q8_0.gguf', 'repo': 'Qwen/Qwen3-Embedding-0.6B-GGUF', 'revision': '370f27d7550e0def9b39c1f16d3fbaa13aa67728', 'size': 639150592, 'sha256': '06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439'},
]
IMAGES = [
    ('postgresql', 'registry-1.docker.io', 'library/postgres', '18.6'),
    ('rabbitmq', 'registry-1.docker.io', 'library/rabbitmq', '4.4.0'),
    ('keycloak', 'quay.io', 'keycloak/keycloak', '26.8.1'),
    ('qdrant', 'registry-1.docker.io', 'qdrant/qdrant', 'v1.20.0'),
    ('valkey-optional', 'registry-1.docker.io', 'valkey/valkey', '9.1.3'),
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def timestamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')


def safe_error(error):
    return re.sub(r'(https?://[^\s?]+)\?[^\s]+', r'\1?[query-redacted]', f'{type(error).__name__}: {error}')[:1500]


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists() and path.read_bytes() != data:
        previous = path.read_bytes()
        history = EVIDENCE / 'retained-observations' / (path.name + '.' + hashlib.sha256(previous).hexdigest() + '.previous')
        history.parent.mkdir(parents=True, exist_ok=True)
        if not history.exists():
            history.write_bytes(previous)
    path.write_bytes(data)


def preserve_source(path, data):
    content = EVIDENCE / 'source-bytes' / (hashlib.sha256(data).hexdigest() + '.raw')
    content.parent.mkdir(parents=True, exist_ok=True)
    if not content.exists():
        content.write_bytes(data)
    if path.exists() and path.read_bytes() != data:
        previous = path.read_bytes()
        prior = EVIDENCE / 'source-bytes' / (hashlib.sha256(previous).hexdigest() + '.raw')
        if not prior.exists():
            prior.write_bytes(previous)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def fetch(url, headers=None, timeout=120):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
        info = {'source_url': url, 'status': response.status, 'content_type': response.headers.get('Content-Type'),
                'docker_content_digest': response.headers.get('Docker-Content-Digest'), 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(), 'observed_at_utc': utc()}
    return data, info


def source_json(url, name, headers=None):
    raw, info = fetch(url, headers)
    (EVIDENCE / 'sources').mkdir(parents=True, exist_ok=True)
    preserve_source(EVIDENCE / 'sources' / (name + '.json'), raw)
    save(EVIDENCE / 'sources' / (name + '.source.json'), info)
    return json.loads(raw), info


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def download_verified(url, dest, expected_size=None, expected_sha256=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    attempt = {'started_at_utc': utc(), 'source_url': url, 'destination': str(dest),
               'expected_size': expected_size, 'expected_sha256': expected_sha256, 'status': 'started'}
    record = EVIDENCE / 'attempts' / (dest.name + '.' + timestamp() + '.json')
    partial = dest.with_name(dest.name + '.attempt-' + timestamp() + '.part')
    attempt['partial_path'] = str(partial)
    save(record, attempt)
    try:
        if dest.exists():
            actual_sha = file_hash(dest)
            actual_size = dest.stat().st_size
            if (expected_sha256 is None or actual_sha == expected_sha256) and (expected_size is None or actual_size == expected_size):
                attempt.update(status='verified-existing', actual_size=actual_size, actual_sha256=actual_sha, finished_at_utc=utc())
                save(record, attempt)
                return attempt
            raise RuntimeError('Existing destination does not match expected identity; preserved without overwrite.')
        if expected_size and shutil.disk_usage(dest.parent).free < expected_size * 2:
            raise RuntimeError('Insufficient free space for artifact and retained partials.')
        request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        started = time.monotonic()
        count = 0
        next_message = 128 * 1024 * 1024
        with urllib.request.urlopen(request, timeout=120) as response, partial.open('xb') as target:
            attempt.update(http_status=response.status, content_length=response.headers.get('Content-Length'), final_host=urllib.parse.urlsplit(response.geturl()).hostname)
            for block in iter(lambda: response.read(8 * 1024 * 1024), b''):
                target.write(block)
                count += len(block)
                if count >= next_message:
                    print(f'{dest.name}: {count // (1024 * 1024)} MiB written', flush=True)
                    next_message += 128 * 1024 * 1024
            target.flush()
            os.fsync(target.fileno())
        actual_size = partial.stat().st_size
        actual_sha = file_hash(partial)
        attempt.update(actual_size=actual_size, actual_sha256=actual_sha, elapsed_seconds=round(time.monotonic() - started, 3))
        if expected_size is not None and actual_size != expected_size:
            raise RuntimeError('Actual on-disk byte count differs from publisher metadata.')
        if expected_sha256 is not None and actual_sha != expected_sha256:
            raise RuntimeError('Actual on-disk SHA256 differs from publisher metadata.')
        if not expected_sha256:
            attempt['publisher_checksum_boundary'] = 'No publisher SHA256 exposed; observed SHA256 identifies received bytes but does not independently authenticate them.'
        os.replace(partial, dest)
        attempt.update(status='verified-bytes' if expected_sha256 else 'observed-bytes-no-publisher-hash', finished_at_utc=utc())
        save(record, attempt)
        print(f"{dest.name}: {attempt['status']} {actual_size} bytes sha256={actual_sha}", flush=True)
    except Exception as error:
        attempt.update(status='failed', error=safe_error(error), finished_at_utc=utc(), retained_partial_bytes=partial.stat().st_size if partial.exists() else 0)
        save(record, attempt)
        print(f'{dest.name}: failed; retained attempt {record.name}', flush=True)
    return attempt


def qualify_models():
    results = []
    for model in MODELS:
        url = f"https://huggingface.co/api/models/{model['repo']}/revision/{model['revision']}?blobs=true"
        metadata, info = source_json(url, model['name'] + '.publisher')
        selected = next(x for x in metadata['siblings'] if x['rfilename'] == model['name'])
        assert metadata['sha'] == model['revision'], 'Publisher revision differs from selected ADR pin'
        assert selected['size'] == model['size'] and selected['lfs']['sha256'] == model['sha256'], 'Publisher artifact metadata differs from selected ADR pin'
        model['source_metadata_sha256'] = info['sha256']
        model['license'] = metadata.get('cardData', {}).get('license')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        pending = {executor.submit(download_verified,
                    f"https://huggingface.co/{m['repo']}/resolve/{m['revision']}/{m['name']}?download=true",
                    CACHE / 'models' / m['name'], m['size'], m['sha256']): m for m in MODELS}
        for future in concurrent.futures.as_completed(pending):
            result = future.result()
            result['model'] = pending[future]
            results.append(result)
            save(EVIDENCE / 'model-artifacts.json', {'observed_at_utc': utc(), 'scope': 'On-disk artifact identity only; no inference or model quality proof', 'artifacts': results})
    return results


def registry_get(host, repo, suffix, token=None):
    url = f'https://{host}/v2/{repo}/{suffix}'
    headers = {'Accept': ACCEPT}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        raw, info = fetch(url, headers)
        return raw, info, token
    except urllib.error.HTTPError as error:
        if error.code != 401 or token:
            raise
        challenge = error.headers.get('WWW-Authenticate', '')
        attrs = dict(re.findall(r'(\w+)="([^"]+)"', challenge))
        realm = attrs['realm']
        if urllib.parse.urlsplit(realm).hostname not in {'auth.docker.io', 'quay.io'}:
            raise RuntimeError('Unexpected registry bearer token realm')
        token_url = realm + '?' + urllib.parse.urlencode({k: v for k, v in attrs.items() if k != 'realm'})
        token_raw, _ = fetch(token_url)
        token = json.loads(token_raw).get('token') or json.loads(token_raw).get('access_token')
        return registry_get(host, repo, suffix, token)


def qualify_registries():
    entries = []
    for label, host, repo, tag in IMAGES:
        entry = {'name': label, 'registry': host, 'repository': repo, 'tag': tag, 'observed_at_utc': utc()}
        try:
            raw, info, token = registry_get(host, repo, 'manifests/' + tag)
            manifest = json.loads(raw)
            index_digest = 'sha256:' + hashlib.sha256(raw).hexdigest()
            if info['docker_content_digest'] and info['docker_content_digest'] != index_digest:
                raise RuntimeError('Index response bytes do not match registry digest header')
            source_dir = EVIDENCE / 'sources'
            source_dir.mkdir(parents=True, exist_ok=True)
            preserve_source(source_dir / (label + '.index.json'), raw)
            save(source_dir / (label + '.index.source.json'), info)
            entry.update(index_digest=index_digest, index_media_type=manifest.get('mediaType'))
            candidates = [m for m in manifest.get('manifests', []) if m.get('platform', {}).get('os') == 'linux' and m.get('platform', {}).get('architecture') == 'amd64']
            if len(candidates) != 1:
                raise RuntimeError(f'Expected one linux/amd64 platform descriptor; found {len(candidates)}')
            platform = candidates[0]
            raw_platform, platform_info, token = registry_get(host, repo, 'manifests/' + platform['digest'], token)
            actual_platform_digest = 'sha256:' + hashlib.sha256(raw_platform).hexdigest()
            if actual_platform_digest != platform['digest']:
                raise RuntimeError('Platform manifest bytes do not match index descriptor')
            platform_manifest = json.loads(raw_platform)
            preserve_source(source_dir / (label + '.linux-amd64.manifest.json'), raw_platform)
            save(source_dir / (label + '.linux-amd64.manifest.source.json'), platform_info)
            config_descriptor = platform_manifest['config']
            config_raw, config_info, _ = registry_get(host, repo, 'blobs/' + config_descriptor['digest'], token)
            if 'sha256:' + hashlib.sha256(config_raw).hexdigest() != config_descriptor['digest']:
                raise RuntimeError('Config bytes do not match platform manifest descriptor')
            config = json.loads(config_raw)
            preserve_source(source_dir / (label + '.linux-amd64.config.json'), config_raw)
            save(source_dir / (label + '.linux-amd64.config.source.json'), config_info)
            env = config.get('config', {}).get('Env', [])
            relevant_env = [e for e in env if re.match(r'(PG_VERSION|RABBITMQ_VERSION|ERLANG|JAVA|KC_|VALKEY|QDRANT|UBUNTU|DEBIAN)', e)]
            entry.update(status='verified-registry-metadata', platform=platform['platform'], linux_amd64_digest=platform['digest'],
                         pull_reference=f'{host}/{repo}@{platform["digest"]}', config_digest=config_descriptor['digest'],
                         config_architecture=config.get('architecture'), config_os=config.get('os'), created=config.get('created'),
                         version_environment=relevant_env, published_labels=config.get('config', {}).get('Labels', {}),
                         base_os_java_erlang_boundary='Config and history preserved; exact installed /etc/os-release and Java/Erlang package versions require actual container inspection by primary.')
            print(f'{label}: {entry["pull_reference"]}', flush=True)
        except Exception as error:
            entry.update(status='failed', error=safe_error(error))
            print(f'{label}: metadata qualification failed: {entry["error"]}', flush=True)
        entries.append(entry)
        save(EVIDENCE / 'container-manifests.json', {'observed_at_utc': utc(), 'scope': 'Registry index/platform/config bytes only; no image pull, filesystem inspection or provider execution', 'images': entries})
    return entries


def qualify_binaries():
    entries = []
    for label, repo, tag in [('ollama', 'ollama/ollama', 'v0.40.11'), ('llama-cpp', 'ggml-org/llama.cpp', 'v0.7.0')]:
        release, info = source_json(f'https://api.github.com/repos/{repo}/releases/tags/{tag}', label + '.release')
        assets = release['assets']
        marker_chain = None
        if label == 'llama-cpp' and len(assets) == 1 and assets[0]['name'] == 'nightly-tag.txt':
            marker_asset = assets[0]
            marker, marker_info = fetch(marker_asset['browser_download_url'])
            assert hashlib.sha256(marker).hexdigest() == marker_asset['digest'].removeprefix('sha256:'), 'Nightly marker checksum mismatch'
            nightly_tag = marker.decode('ascii').strip()
            if not re.fullmatch(r'b[0-9]+', nightly_tag):
                raise RuntimeError('Unexpected official nightly marker value')
            preserve_source(EVIDENCE / 'sources' / 'llama-cpp.nightly-tag.txt', marker)
            save(EVIDENCE / 'sources' / 'llama-cpp.nightly-tag.source.json', marker_info)
            nightly, nightly_info = source_json(f'https://api.github.com/repos/{repo}/releases/tags/{nightly_tag}', 'llama-cpp.nightly-release')
            ref, _ = source_json(f'https://api.github.com/repos/{repo}/git/ref/tags/{nightly_tag}', 'llama-cpp.nightly-ref')
            assert ref['object']['type'] == 'commit' and ref['object']['sha'] == release['target_commitish'] == nightly['target_commitish'], 'Versioned and nightly source commits differ'
            marker_chain = {'versioned_release': tag, 'nightly_tag': nightly_tag, 'source_commit': ref['object']['sha'], 'marker_sha256': marker_info['sha256'], 'nightly_release_metadata_sha256': nightly_info['sha256']}
            assets = nightly['assets']
        if label == 'ollama':
            selected = [a for a in assets if a['name'] in {'ollama-linux-amd64.tar.zst', 'ollama-linux-amd64.tgz', 'ollama-linux-amd64.tar.gz'}]
        else:
            binary_tag = marker_chain['nightly_tag'] if marker_chain else tag
            selected = [a for a in assets if a['name'] == f'llama-{binary_tag}-bin-ubuntu-x64.tar.gz']
        if len(selected) != 1:
            entries.append({'name': label, 'status': 'asset-selection-pending', 'candidate_assets': [{'name': a['name'], 'size': a['size'], 'digest': a.get('digest'), 'url': a['browser_download_url']} for a in assets]})
            continue
        asset = selected[0]
        sha256 = (asset.get('digest') or '').removeprefix('sha256:') or None
        result = download_verified(asset['browser_download_url'], CACHE / 'binaries' / label / tag / asset['name'], asset['size'], sha256)
        result.update(name=label, repository=repo, release_tag=tag, release_published_at=release['published_at'], asset_name=asset['name'],
                      publisher_asset_digest=asset.get('digest'), published_release_metadata_sha256=info['sha256'],
                      official_nightly_marker_chain=marker_chain,
                      build_isa_boundary='Linux x64 release asset selected; exact CPU ISA, dynamic loader and linked libraries pending safe archive/ELF inspection and primary runtime smoke.')
        entries.append(result)
        save(EVIDENCE / 'inference-binaries.json', {'observed_at_utc': utc(), 'scope': 'Archive identity only; binaries not executed', 'binaries': entries})
    save(EVIDENCE / 'inference-binaries.json', {'observed_at_utc': utc(), 'scope': 'Archive identity only; binaries not executed', 'binaries': entries})
    return entries


def extract_and_inspect():
    entries = json.loads((EVIDENCE / 'inference-binaries.json').read_text(encoding='utf-8'))['binaries']
    results = []
    for entry in entries:
        name = entry['name']
        archive = Path(entry['destination'])
        target = archive.parent / 'runtime'
        resolved_cache = CACHE.resolve()
        if not target.resolve().is_relative_to(resolved_cache):
            raise RuntimeError('Extraction target is outside owned tools cache')
        if file_hash(archive) != entry['actual_sha256']:
            raise RuntimeError('Archive bytes changed after qualification')
        listing = subprocess.run(['tar.exe', '-tf', str(archive)], capture_output=True, check=True).stdout.decode('utf-8').splitlines()
        verbose = subprocess.run(['tar.exe', '-tvf', str(archive)], capture_output=True, check=True).stdout.decode('utf-8', errors='replace').splitlines()
        for member in listing:
            if not re.fullmatch(r'[A-Za-z0-9_.+/-]+', member) or member.startswith('/') or '..' in member.split('/'):
                raise RuntimeError('Unsafe archive member name')
        for line in verbose:
            if line[0] not in '-dlh':
                raise RuntimeError('Archive contains a non-regular/directory/link member')
            if ' -> ' in line:
                left, link_target = line.rsplit(' -> ', 1)
                member = next((m for m in listing if left.endswith(' ' + m)), None)
                if member is None or link_target.startswith('/') or not re.fullmatch(r'[A-Za-z0-9_.+/-]+', link_target):
                    raise RuntimeError('Unrecognized or unsafe symlink target')
                normalized = posixpath.normpath(posixpath.join(posixpath.dirname(member), link_target))
                if normalized == '..' or normalized.startswith('../'):
                    raise RuntimeError('Archive symlink escapes extraction root')
            elif line[0] in 'lh':
                raise RuntimeError('Unrecognized link listing; refuse extraction')
        exclusions = ['lib/ollama/cuda_v12*', 'lib/ollama/cuda_v13*', 'lib/ollama/vulkan*'] if name == 'ollama' else ['llama-b11669/rpc-server', 'llama-b11669/libggml-rpc.so']
        record = {'name': name, 'archive_path': str(archive), 'archive_sha256': entry['actual_sha256'],
                  'runtime_root': str(target), 'excluded_archive_patterns': exclusions,
                  'archive_member_name_link_boundary': 'All listed names/types/link targets validated before extraction; links may not escape root; devices/FIFOs rejected.'}
        marker = target / '.cehpalon-extraction-complete.json'
        if target.exists():
            if not marker.exists() or json.loads(marker.read_text())['archive_sha256'] != entry['actual_sha256']:
                raise RuntimeError('Existing runtime directory lacks matching complete marker; preserved without overwrite')
        else:
            target.mkdir(parents=True)
            cmd = ['tar.exe', '-xf', str(archive), '-C', str(target), *['--exclude=' + value for value in exclusions]]
            process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            record['extraction_exit_code'] = process.returncode
            record['extraction_stderr'] = process.stderr
            if process.returncode:
                record['status'] = 'extraction-failed-partial-preserved'
                save(EVIDENCE / (name + '.runtime-inspection.json'), record)
                results.append(record)
                continue
            marker.write_text(json.dumps({'archive_sha256': entry['actual_sha256'], 'exclusions': exclusions}) + '\n', encoding='utf-8')
        executable = target / ('bin/ollama' if name == 'ollama' else 'llama-b11669/llama-server')
        wsl_binary = '/mnt/' + executable.drive[0].lower() + '/' + '/'.join(executable.parts[1:])
        record['executable_path'] = str(executable)
        record['executable_sha256'] = file_hash(executable)
        record['commands'] = []
        commands = [
            ['wsl.exe', '-d', 'Ubuntu', '--', 'uname', '-a'],
            ['wsl.exe', '-d', 'Ubuntu', '--', 'cat', '/etc/os-release'],
            ['wsl.exe', '-d', 'Ubuntu', '--', 'ldd', '--version'],
            ['wsl.exe', '-d', 'Ubuntu', '--', 'readelf', '-h', '-n', wsl_binary],
            ['wsl.exe', '-d', 'Ubuntu', '--', 'ldd', wsl_binary],
            ['wsl.exe', '-d', 'Ubuntu', '--', 'env', 'OLLAMA_HOST=http://127.0.0.1:65534', wsl_binary, '--version'],
        ]
        for command in commands:
            process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            record['commands'].append({'argv': command, 'exit_code': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr})
        version = record['commands'][-1]
        record['status'] = 'version-smoke-passed' if version['exit_code'] == 0 else 'version-smoke-failed'
        record['proof_boundary'] = 'Only --version and loader/ELF metadata; no server started, no model inference, no RPC/mmproj/multimodal execution or performance claims.'
        save(EVIDENCE / (name + '.runtime-inspection.json'), record)
        results.append(record)
        print(f'{name}: {record["status"]}; {version["stdout"][:400]} {version["stderr"][:400]}', flush=True)
    save(EVIDENCE / 'runtime-binary-inspection.json', {'observed_at_utc': utc(), 'runners': results})
    return results


def qualify_local_dependency():
    record = {'name': 'llama-cpp-local-libgomp1', 'observed_at_utc': utc(), 'status': 'started',
              'scope': 'Read signed Ubuntu metadata, download package, extract one library app-locally; no apt install or maintainer scripts'}
    try:
        release_url = 'https://archive.ubuntu.com/ubuntu/dists/jammy-updates/InRelease'
        release_raw, release_info = fetch(release_url)
        release_path = EVIDENCE / 'sources/ubuntu-jammy-updates.InRelease'
        preserve_source(release_path, release_raw)
        save(EVIDENCE / 'sources/ubuntu-jammy-updates.InRelease.source.json', release_info)
        wsl_release = '/mnt/d/' + '/'.join(release_path.parts[1:])
        signature_command = ['wsl.exe', '-d', 'Ubuntu', '--', 'gpgv', '--keyring', '/usr/share/keyrings/ubuntu-archive-keyring.gpg', wsl_release]
        signature = subprocess.run(signature_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        keyring = subprocess.run(['wsl.exe', '-d', 'Ubuntu', '--', 'sha256sum', '/usr/share/keyrings/ubuntu-archive-keyring.gpg'], capture_output=True, text=True, encoding='utf-8', check=True)
        record.update(release_source=release_info, gpgv={'argv': signature_command, 'exit_code': signature.returncode, 'stdout': signature.stdout, 'stderr': signature.stderr}, trusted_system_keyring_sha256=keyring.stdout.split()[0])
        if signature.returncode:
            raise RuntimeError('Ubuntu InRelease signature did not verify against existing Ubuntu archive keyring')
        release_text = release_raw.decode('utf-8')
        valid_match = re.search(r'^Valid-Until: (.+)$', release_text, re.MULTILINE)
        record['release_date'] = re.search(r'^Date: (.+)$', release_text, re.MULTILINE).group(1)
        record['release_valid_until'] = valid_match.group(1) if valid_match else None
        release_date = parsedate_to_datetime(record['release_date'])
        if release_date < datetime.now(timezone.utc) - timedelta(days=7) or release_date > datetime.now(timezone.utc) + timedelta(days=1):
            raise RuntimeError('Signed Ubuntu release date falls outside declared freshness window')
        record['release_freshness_policy'] = 'Reject signed Release older than seven days or dated more than one day in the future; record Valid-Until separately if publisher supplies it.'
        if valid_match and parsedate_to_datetime(valid_match.group(1)) < datetime.now(timezone.utc):
            raise RuntimeError('Signed Ubuntu release is expired')
        index_match = re.search(r'^ ([0-9a-f]{64}) +(\d+) +main/binary-amd64/Packages.xz$', release_text, re.MULTILINE)
        if not index_match:
            raise RuntimeError('Signed Release has no expected Packages.xz SHA256 entry')
        index_sha, index_size = index_match.group(1), int(index_match.group(2))
        index_url = 'https://archive.ubuntu.com/ubuntu/dists/jammy-updates/main/binary-amd64/Packages.xz'
        index_path = CACHE / 'packages/ubuntu/jammy-updates/main-binary-amd64.Packages.xz'
        index_attempt = download_verified(index_url, index_path, index_size, index_sha)
        record['signed_index'] = index_attempt
        if index_attempt['status'] not in {'verified-bytes', 'verified-existing'}:
            raise RuntimeError('Signed package index download/hash validation failed')
        packages = lzma.decompress(index_path.read_bytes()).decode('utf-8')
        paragraph = next(x for x in packages.split('\n\n') if x.startswith('Package: libgomp1\n'))
        package = dict(line.split(': ', 1) for line in paragraph.splitlines() if line and not line.startswith(' ') and ': ' in line)
        if package.get('Architecture') != 'amd64' or not package['Filename'].startswith('pool/main/g/gcc-'):
            raise RuntimeError('Unexpected Ubuntu package identity or architecture')
        preserve_source(EVIDENCE / 'sources/ubuntu-libgomp1.signed-package-entry.txt', (paragraph + '\n').encode('utf-8'))
        package_url = 'https://archive.ubuntu.com/ubuntu/' + package['Filename']
        package_path = CACHE / 'packages/ubuntu' / Path(package['Filename']).name
        package_attempt = download_verified(package_url, package_path, int(package['Size']), package['SHA256'])
        record.update(package_metadata=package, package_bytes=package_attempt)
        if package_attempt['status'] not in {'verified-bytes', 'verified-existing'}:
            raise RuntimeError('Ubuntu package actual bytes differ from signed Packages entry')
        wsl_package = '/mnt/d/' + '/'.join(package_path.parts[1:])
        data_tar = subprocess.run(['wsl.exe', '-d', 'Ubuntu', '--', 'dpkg-deb', '--fsys-tarfile', wsl_package], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data_tar), mode='r:') as archive:
            matches = [m for m in archive.getmembers() if m.name.endswith('/libgomp.so.1.0.0') and m.isfile()]
            if len(matches) != 1:
                raise RuntimeError('Package does not contain one regular expected libgomp runtime library')
            library_data = archive.extractfile(matches[0]).read()
        dependency_root = CACHE / 'binaries/llama-cpp/v0.7.0/runtime/lib'
        dependency_root.mkdir(parents=True, exist_ok=True)
        dependency_path = dependency_root / 'libgomp.so.1'
        if not dependency_path.resolve().is_relative_to(CACHE.resolve()):
            raise RuntimeError('Dependency path escaped owned cache')
        if dependency_path.exists() and dependency_path.read_bytes() != library_data:
            raise RuntimeError('Existing app-local dependency differs; preserved without overwrite')
        dependency_path.write_bytes(library_data)
        record.update(extracted_member=matches[0].name, app_local_library=str(dependency_path), library_sha256=file_hash(dependency_path), library_size=dependency_path.stat().st_size,
                      package_license_boundary='Source gcc-12 runtime library; full transitive license/notices and GCC Runtime Library Exception packaging review still required before redistribution.')
        runner = CACHE / 'binaries/llama-cpp/v0.7.0/runtime/llama-b11669/llama-server'
        wsl_runner = '/mnt/d/' + '/'.join(runner.parts[1:])
        wsl_library = '/mnt/d/' + '/'.join(dependency_root.parts[1:])
        record['commands'] = []
        for args in [['ldd', wsl_runner], [wsl_runner, '--version'], [wsl_runner, '--help']]:
            command = ['wsl.exe', '-d', 'Ubuntu', '--', 'env', 'LD_LIBRARY_PATH=' + wsl_library, *args]
            process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            record['commands'].append({'argv': command, 'exit_code': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr})
        record['status'] = 'dependency-smoke-passed' if all(x['exit_code'] == 0 for x in record['commands']) and 'not found' not in record['commands'][0]['stdout'] else 'dependency-smoke-failed'
        print(f"App-local libgomp1 {package['Version']}: {record['status']}", flush=True)
        print(record['commands'][1]['stdout'] + record['commands'][1]['stderr'], flush=True)
    except Exception as error:
        record.update(status='failed', error=safe_error(error))
        print('App-local dependency qualification failed: ' + record['error'], flush=True)
    save(EVIDENCE / 'llama-cpp-local-dependency.json', record)
    return [record]


def selftest():
    global EVIDENCE
    destination_evidence = EVIDENCE
    root = CACHE / 'artifact-tests' / timestamp()
    root.mkdir(parents=True)
    cases = []
    try:
        EVIDENCE = root / 'evidence'
        payload = b'cehpalon-test-artifact-v1'
        source = root / 'source.bin'
        source.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        result = download_verified(source.as_uri(), root / 'good.bin', len(payload), digest)
        cases.append({'name': 'verified artifact uses actual on-disk bytes/hash', 'passed': result['status'] == 'verified-bytes'})
        old_time = (root / 'good.bin').stat().st_mtime_ns
        result = download_verified(source.as_uri(), root / 'good.bin', len(payload), digest)
        cases.append({'name': 'matching existing artifact is never overwritten', 'passed': result['status'] == 'verified-existing' and (root / 'good.bin').stat().st_mtime_ns == old_time})
        result = download_verified(source.as_uri(), root / 'bad-checksum.bin', len(payload), '0' * 64)
        cases.append({'name': 'checksum failure retains bytes and does not promote destination', 'passed': result['status'] == 'failed' and not (root / 'bad-checksum.bin').exists() and Path(result['partial_path']).read_bytes() == payload})
        protected = root / 'protected.bin'
        protected.write_bytes(b'existing-wrong-bytes')
        result = download_verified(source.as_uri(), protected, len(payload), digest)
        cases.append({'name': 'mismatched existing destination is preserved', 'passed': result['status'] == 'failed' and protected.read_bytes() == b'existing-wrong-bytes'})
        save(EVIDENCE / 'retention.json', {'v': 1})
        save(EVIDENCE / 'retention.json', {'v': 2})
        prior = list((EVIDENCE / 'retained-observations').glob('retention.json.*.previous'))
        cases.append({'name': 'changed JSON retains the specific prior observation', 'passed': len(prior) == 1 and json.loads(prior[0].read_text()) == {'v': 1}})
        preserve_source(EVIDENCE / 'sources/raw.txt', b'first')
        preserve_source(EVIDENCE / 'sources/raw.txt', b'second')
        cases.append({'name': 'changed source retains both content hashes', 'passed': all((EVIDENCE / 'source-bytes' / (hashlib.sha256(value).hexdigest() + '.raw')).read_bytes() == value for value in [b'first', b'second'])})
    finally:
        EVIDENCE = destination_evidence
    report = {'observed_at_utc': utc(), 'status': 'passed' if all(c['passed'] for c in cases) else 'failed',
              'scope': 'Offline local-file artifact safety checks; no network, downloaded binary or model execution', 'retained_test_root': str(root),
              'passed': sum(c['passed'] for c in cases), 'total': len(cases), 'cases': cases}
    save(EVIDENCE / 'tool-validation.json', report)
    print(f'Artifact tool offline checks: {report["passed"]}/{report["total"]}', flush=True)
    return [report]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['models', 'registries', 'binaries', 'inspect', 'dependency', 'selftest'])
    action = parser.parse_args().action
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    results = {'models': qualify_models, 'registries': qualify_registries, 'binaries': qualify_binaries, 'inspect': extract_and_inspect, 'dependency': qualify_local_dependency, 'selftest': selftest}[action]()
    failures = [r for r in results if r.get('status') in {'failed', 'asset-selection-pending', 'version-smoke-failed', 'extraction-failed-partial-preserved', 'dependency-smoke-failed'}]
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
