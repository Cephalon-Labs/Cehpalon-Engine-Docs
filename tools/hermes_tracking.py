"""Project the committed Engine tracking snapshot onto a non-dispatchable Hermes board."""
import argparse
from contextlib import closing
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys

from pull_tracking import PROJECT_ID, REPO

BOARD = 'cephalon-engine-mirror'
OWNER = 'cephalon-engine-mirror-v1'
PROJECT = 'https://github.com/orgs/Cephalon-Labs/projects/4'
ENGINE = f'https://github.com/{REPO}'
DOCS = 'https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs'
SNAPSHOT = 'internal/evidence/tracking/github-observed.json'
REFERENCES = (
    ('Program plan', 'internal/planning/2026-10-27-program-plan.md'),
    ('Task mirrors and acceptance criteria', 'tasks/README.md'),
    ('Program memory and document entry points', 'internal/memory/README.md'),
    ('Tracking synchronization runbook', 'internal/standards/tracking-sync-usage.md'),
    ('Shared Engine governance skill', 'skills/cehpalon-engine/SKILL.md'),
)
MARKER = re.compile(r'<!-- cephalon-engine-mirror:(issue:[1-9][0-9]*|milestone:[1-9][0-9]*|docs:engine) -->\n')


@dataclass(frozen=True)
class Card:
    title: str
    body: str


def load(root):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])

    sha = git('rev-parse', '--verify', 'HEAD').decode().strip()
    def blob(path):
        return git('show', f'{sha}:{path}')

    source = json.loads(blob(SNAPSHOT))
    observed = source['observed_at_utc']
    if source['project_id'] != PROJECT_ID or source['schema_version'] != 1 or not source['issues']:
        raise ValueError('Unrecognized or empty Project 4 snapshot')
    def doc(path):
        return f'{DOCS}/blob/{sha}/{path}'

    cards = {}
    def add(key, title, text):
        if key in cards or not title.strip() or '\n' in title or '\r' in title:
            raise ValueError(f'Duplicate key or invalid title: {key}')
        cards[key] = Card(title, f'<!-- cephalon-engine-mirror:{key} -->\n'
                                 'Reference only; do not assign or dispatch. Hermes blocked is not Engine status.\n\n'
                                 f'Observed GitHub snapshot: {observed} (not a live Project query)\n'
                                 f'Snapshot: {doc(SNAPSHOT)}\nProject 4: {PROJECT}\n\n{text}')

    milestones = set()
    for item in source['milestones']:
        n = item['number']
        if type(n) is not int or n < 1:
            raise ValueError('Invalid milestone identity')
        milestones.add(n)
        add(f'milestone:{n}', f"[Milestone {n}] {item['title']}",
            f"GitHub: {ENGINE}/milestone/{n}\nState: {item['state']}\nDue: {item['due_on'] or 'not set'}\n"
            f"Open / closed: {item['open_issues']} / {item['closed_issues']}\n"
            f"Program plan: {doc(REFERENCES[0][1])}\n")

    for n, issue in sorted(source['issues'].items(), key=lambda entry: int(entry[0])):
        path = f'tasks/{n}.md'
        if (not re.fullmatch(r'[1-9][0-9]*', n) or str(issue['number']) != n
                or issue['url'] != f'{ENGINE}/issues/{n}' or not issue['item_id']
                or issue['milestone_number'] not in milestones | {None}):
            raise ValueError(f'Unexpected issue identity or milestone: #{n}')
        if hashlib.sha256(blob(path)).hexdigest() != issue['mirror_sha256']:
            raise ValueError(f'Committed Docs mirror differs from snapshot: {path}')
        milestone = issue['milestone_number']
        milestone_link = f'{ENGINE}/milestone/{milestone}' if milestone is not None else 'not set'
        fields = '\n'.join(f'- {k}: {json.dumps(v, ensure_ascii=False)}'
                           for k, v in sorted(issue['fields'].items()) if k != 'Title')
        add(f'issue:{n}', f"[Engine #{n}] {issue['title']}",
            f"GitHub issue: {issue['url']}\nProject item ID: {issue['item_id']}\n"
            f"Native state/type: {issue['state']} / {issue['type']}\nMilestone: {milestone_link}\n"
            f"Docs task, acceptance, checklist and evidence links: {doc(path)}\n"
            f"Native sub-issues (live GitHub): {issue['url']}\n\nProject fields (observed):\n{fields}\n")

    for _, path in REFERENCES:
        blob(path)  # Reject a broken pinned entry point before any card writes.
    links = '\n'.join(f'- [{title}]({doc(path)})' for title, path in REFERENCES)
    add('docs:engine', '[Docs] Engine plans and tracking index', links + '\n')
    return source, cards


def plan(cards, rows):
    existing = {}
    ids = set()
    for row in rows:
        match = MARKER.match(row['body'] or '')
        if not match or row['created_by'] != OWNER or row['assignee'] is not None or row['status'] != 'blocked':
            raise ValueError(f"Unmanaged, assigned or non-blocked card: {row['id']}")
        key = match[1]
        if key in existing or row['id'] in ids or key not in cards:
            raise ValueError(f'Duplicate or missing source for {key}; reconcile manually')
        existing[key] = row
        ids.add(row['id'])
    ops = []
    for key, card in cards.items():
        row = existing.get(key)
        if row is None:
            ops.append(('create', key, None))
        elif (row['title'], row['body']) != (card.title, card.body):
            ops.append(('edit', key, row['id']))
    return ops


def board_directory(home):
    return home / 'kanban' / 'boards' / BOARD


def read_board(home):
    directory = board_directory(home)
    for path in (directory.parent.parent, directory.parent, directory):
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f'Unexpected board path: {path}')
    if not directory.exists():
        return None
    metadata, db = directory / 'board.json', directory / 'kanban.db'
    for path in (metadata, db):
        if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
            raise ValueError(f'Incomplete or redirected mirror board: {path}')
    for suffix in ('-wal', '-shm', '-journal'):
        path = db.with_name(db.name + suffix)
        if path.is_symlink() or (path.exists() and (not path.is_file() or path.stat().st_nlink != 1)):
            raise ValueError(f'Redirected mirror database journal: {path}')
    meta = json.loads(metadata.read_text(encoding='utf-8'))
    if not isinstance(meta, dict) or meta.get('slug') != BOARD or meta.get('archived') is not False:
        raise ValueError('Unexpected or archived mirror board metadata')
    # CLI `list` may promote tasks. Read all statuses without schema init or dispatch.
    with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(
            'SELECT id, created_by, title, body, assignee, status FROM tasks ORDER BY id')]


def write_env(home, environ):
    env = {key: value for key, value in environ.items() if not key.startswith('HERMES_KANBAN_')}
    env.update(HERMES_KANBAN_HOME=str(home), HERMES_KANBAN_BOARD=BOARD,
               HERMES_KANBAN_DB=str(board_directory(home) / 'kanban.db'))
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hermes', default='hermes', help='Hermes executable')
    parser.add_argument('--kanban-home', required=True, type=Path, help='Shared Hermes Kanban root (not a profile directory)')
    parser.add_argument('--apply', action='store_true', help='Write only to the dedicated Hermes mirror board')
    args = parser.parse_args()
    home = args.kanban_home.expanduser().resolve(strict=True)
    if not home.is_dir():
        raise ValueError('Kanban root must be an existing directory')
    env = write_env(home, os.environ)

    def call(*argv, input=None):
        return subprocess.check_output([args.hermes, 'kanban', *argv], input=input,
                                       text=True, timeout=45, env=env)

    def board(*argv, input=None):
        return call('--board', BOARD, *argv, input=input)


    root = Path(__file__).resolve().parents[1]
    snapshot, cards = load(root)
    # Scope: one checkout/controller; prevent concurrent cooperating applies.
    lock = home / f'.{BOARD}.lock'
    if args.apply:
        with os.fdopen(os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as handle:
            handle.write(f'{os.getpid()}\n')
    try:
        rows = read_board(home)
        ops = plan(cards, rows or [])
        if args.apply:
            if rows is None:
                call('boards', 'create', BOARD, '--name', 'Cephalon Engine — reference mirror',
                     '--description', 'Project 4 snapshot references only. Not an execution board. Do not assign or dispatch.')
                rows = read_board(home)
                if rows != []:
                    raise ValueError('New board was not empty')
            for op, key, task_id in ops:
                if read_board(home) != rows:
                    raise ValueError('Mirror changed during apply; read back before retrying')
                card = cards[key]
                if op == 'create':
                    board('create', '--initial-status', 'blocked', '--created-by', OWNER,
                          '--idempotency-key', f'{REPO}:{PROJECT_ID}:{key}', '--body-file', '-',
                          '--json', '--', card.title, input=card.body)
                else:
                    board('edit', f'--title={card.title}', f'--body={card.body}', '--', task_id)
                current = read_board(home)
                if current is None:
                    raise ValueError('Mirror disappeared after write')
                plan(cards, current)  # Reject invalid ownership, status, keys, and IDs.
                expected = {row['id']: row for row in rows}
                actual = {row['id']: row for row in current}
                if op == 'create':
                    added = actual.keys() - expected.keys()
                    if len(added) != 1:
                        raise ValueError('Expected exactly one new mirror card')
                    task_id = next(iter(added))
                expected[task_id] = dict(id=task_id, created_by=OWNER, title=card.title,
                                         body=card.body, assignee=None, status='blocked')
                if actual != expected:
                    raise ValueError('Unexpected mirror readback after write; reconcile manually')
                rows = current
            final_rows = read_board(home)
            if final_rows is None or final_rows != rows or plan(cards, final_rows):
                raise ValueError('Hermes final readback does not match the verified cards')
            rows = final_rows
        report = dict(board=BOARD, kanban_home=str(home), observed_at=snapshot['observed_at_utc'],
                      desired=len(cards), create=sum(op[0] == 'create' for op in ops),
                      edit=sum(op[0] == 'edit' for op in ops), applied=args.apply)
        if args.apply:
            report['ids'] = {MARKER.match(row['body'])[1]: row['id'] for row in rows}
        print(json.dumps(report, indent=2))
    finally:
        if args.apply:
            lock.unlink()


if __name__ == '__main__':
    try:
        main()
    except (KeyError, ValueError, OSError, sqlite3.Error, subprocess.SubprocessError) as error:
        sys.exit(f'Hermes mirror stopped: {error}')
