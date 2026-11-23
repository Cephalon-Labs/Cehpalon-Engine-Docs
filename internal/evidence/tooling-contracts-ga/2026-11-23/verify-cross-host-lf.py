"""Verify published contract bytes across two complete clean GA runs."""
from hashlib import sha256
import json
from pathlib import Path
import sys


def require(condition, description):
    if not condition:
        raise ValueError(description)


def read_result(root, revision):
    report = json.loads((root / 'manifest.json').read_bytes())
    wire = json.loads((root / 'schema-wire-proof.json').read_bytes())
    require(report['status'] == 'passed' and report['engine_revision'] == revision
            and report['source_state'] == 'exact clean committed source'
            and report['sdk'] == '11.0.100' and len(report['checks']) == 160
            and wire['passed'] == 25 and wire['failed'] == 0,
            'run must pass the complete matrix on exact clean GA source')
    return report


def verify(windows, wsl, baseline_wsl, output):
    revision = '6fe7254404cf6b148370bd95befe8331e8932354'
    original = 'c18757f7ef4df2c78c73e902aa39d05424e6bcff'
    reports = [read_result(windows, revision), read_result(wsl, revision),
               read_result(baseline_wsl, original)]
    registry = reports[0]['generated_registry_sha256']
    require(all(report['generated_registry_sha256'] == registry for report in reports),
            'actual emitted operation registry changed')
    observations = [report['observed_source_manifest'] for report in reports]
    require(observations[0]['sourceRoot'] != observations[1]['sourceRoot']
            and observations[0]['inputs'] == observations[1]['inputs'],
            'generated checkout provenance must retain its actual source root and input digests')

    expected = {
        'api': {'manifest.json', 'openapi.json'},
        'both': {'manifest.json', 'openapi.json', 'schema.graphql'},
        'graphql': {'manifest.json', 'schema.graphql'},
        'off': {'manifest.json'},
    }
    verified = []
    for profile, names in expected.items():
        directories = [root / ('export-' + profile) for root in (windows, wsl, baseline_wsl)]
        require(all({path.name for path in directory.iterdir()} == names for directory in directories),
                'unexpected artifact set for ' + profile)
        files = {}
        for name in sorted(names):
            copies = [(directory / name).read_bytes() for directory in directories]
            require(copies[0] == copies[1] == copies[2],
                    f'bytes differ from the other host or unchanged LF baseline for {profile}/{name}')
            payload = copies[0]
            require(b'\r' not in payload and payload.endswith(b'\n') and not payload.endswith(b'\n\n'),
                    f'noncanonical line endings for {profile}/{name}')
            files[name] = {'bytes': len(payload), 'sha256': sha256(payload).hexdigest()}
        manifest = json.loads((directories[0] / 'manifest.json').read_bytes())
        recorded = {field['name']: {'bytes': field['bytes'], 'sha256': field['sha256']}
                    for field in manifest['artifacts']}
        require(len(manifest['artifacts']) == len(names) - 1
                and recorded == {name: info for name, info in files.items() if name != 'manifest.json'},
                'manifest does not describe exactly the published artifact bytes')
        verified.append({'profile': profile, 'files': files})

    result = {'engine': revision, 'baseline_engine': original, 'sdk': '11.0.100',
              'checks_per_host': 160, 'wire_differential_per_host': 25,
              'generated_registry_sha256': registry, 'canonical_artifacts': verified,
              'scope': 'Exact artifact-byte comparison against paired hosts and the previous LF baseline. Fixture correctness only.'}
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(f'{sum(len(item["files"]) for item in verified)} exact byte-identical artifacts verified')


if __name__ == '__main__':
    verify(*(Path(argument) for argument in sys.argv[1:]))

