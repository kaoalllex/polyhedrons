#!/usr/bin/env python3
"""Local, file-backed dialogue transport. See TRANSPORT.md for the protocol."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid

DEFAULT_AGENTS = ('astra', 'claude')
RESERVED = {'owner', 'all', 'both', 'keep', 'pause', 'close'}
HERE = Path(__file__).resolve().parent
THREADS = HERE / 'threads'
RUNNERS = HERE / 'runners.json'
ROOT = Path(__file__).resolve().parents[3]
RETRY = (60, 300, 900, 1800)


class Refused(ValueError):
    pass


class Unseen(Refused):
    def __init__(self, messages):
        super().__init__('New messages by others since --seen; amend your answer and post again')
        self.messages = messages


def thread_path(name):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
        raise Refused('Invalid thread name')
    return THREADS / name


def agent_name(name):
    if not isinstance(name, str) or not re.fullmatch(r'[a-z][a-z0-9]{0,15}', name) or name in RESERVED:
        raise Refused('Invalid agent name')
    return name


def new_thread(path, names=DEFAULT_AGENTS):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.mkdir()
    except FileExistsError:
        raise Refused('Thread already exists')
    (path / 'sealed').mkdir()
    for author in names:
        (path / 'work' / agent_name(author)).mkdir(parents=True)
    atomic_write(path / 'thread.json', json.dumps({
        'participants': sorted(names) + ['owner'], 'max_lines': 60, 'max_auto_turns': 12,
        'created': datetime.now().isoformat(timespec='seconds'),
        'roster': [{'n': 0, 'join': author} for author in sorted(names)],
    }, indent=2) + '\n')


def models_at(config, before=float('inf')):
    """Agents in the dialogue for a message numbered `before`; `all` expands to them."""
    if 'roster' not in config:
        return set(config['participants']) - {'owner'}
    active = set()
    for event in config['roster']:
        if event['n'] < before:
            if 'join' in event:
                active.add(event['join'])
            else:
                active.discard(event['leave'])
    return active


def set_roster(path, name, join):
    """Join or leave the dialogue from the next message on; history keeps its meaning."""
    config = json.loads((path / 'thread.json').read_text(encoding='utf-8'))
    if join == (name in models_at(config)):
        return
    files = [p for p in path.glob('*.md') if re.fullmatch(r'\d+-[a-z][a-z0-9]*\.md', p.name)]
    last = max([int(p.name.split('-')[0]) for p in files] + [0])
    config.setdefault('roster', [{'n': 0, 'join': author} for author in sorted(models_at(config))])
    config['roster'].append({'n': last, 'join' if join else 'leave': name})
    if name not in config['participants']:
        config['participants'].insert(-1 if config['participants'][-1:] == ['owner'] else len(config['participants']), name)
    (path / 'work' / name).mkdir(parents=True, exist_ok=True)
    atomic_write(path / 'thread.json', json.dumps(config, indent=2) + '\n')


def atomic_write(path, text):
    fd, name = tempfile.mkstemp(prefix='.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(path):
    if not (path / 'thread.json').is_file():
        raise Refused('Unknown thread')
    lock = path / '.lock'
    while True:
        try:
            lock.mkdir()
            identity = lock.stat().st_ino
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > 10:
                    lock.rmdir()
            except FileNotFoundError:
                pass
            except OSError:
                pass
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            if lock.stat().st_ino == identity:
                lock.rmdir()
        except FileNotFoundError:
            pass


def read_message(path):
    text = path.read_text(encoding='utf-8')
    header, body = text[4:].split('\n---\n', 1)
    message = dict(line.split(': ', 1) for line in header.splitlines())
    message['n'] = int(message['n'])
    message['body'] = body
    message['file'] = path.name
    return message


def message_text(message):
    return '---\n' + ''.join('{}: {}\n'.format(key, message[key])
                                 for key in ('n', 'author', 'next', 'round', 'time')) + '---\n' + message['body']


def speakers(value, models):
    return set(models) if value in ('all', 'both') else {value}


def snapshot_unlocked(path):
    config = json.loads((path / 'thread.json').read_text(encoding='utf-8'))
    files = [p for p in path.glob('*.md') if re.fullmatch(r'\d+-[a-z][a-z0-9]*\.md', p.name)]
    messages = [read_message(p) for p in sorted(files, key=lambda p: int(p.name.split('-')[0]))]
    floor, closed, pending = {'owner'}, False, None
    for message in messages:
        author, nxt, models = message['author'], message['next'], models_at(config, message['n'])
        if author == 'owner':
            if nxt != 'keep':
                pending = None
                closed = nxt == 'close'
                floor = set() if nxt in ('close', 'pause') else speakers(nxt, models)
        elif pending is not None or len(floor - {'owner'}) > 1:
            if pending is None:
                group = floor - {'owner'}
                pending = {'group': group, 'remaining': set(group), 'next': set(), 'first': message['n']}
            message['batch'] = pending['first']
            pending['remaining'].discard(author)
            pending['next'].update(speakers(nxt, models))
            if not pending['remaining']:
                floor = (floor - pending['group']) | pending['next']
                pending = None
        else:
            floor.discard(author)
            floor.update(speakers(nxt, models))
    held = [read_message(p) for p in sorted((path / 'sealed').glob('*.md'))]
    group = pending['remaining'] if pending else floor - {'owner'}
    waiting = ((floor - pending['group']) | pending['remaining'] if pending else floor) - {m['author'] for m in held}
    return {'config': config, 'messages': messages, 'floor': sorted(waiting), 'closed': closed, 'held': held,
            'parallel': sorted(group) if len(group) > 1 or held else [], 'agents': sorted(models_at(config))}


def snapshot(path):
    with locked(path):
        return snapshot_unlocked(path)


def post(path, author, nxt, body, round_label='', seen=None):
    """The sole writer path for both CLI and HTTP messages."""
    with locked(path):
        state = snapshot_unlocked(path)
        if author not in state['config']['participants']:
            raise Refused('Unknown participant')
        if state['closed']:
            raise Refused('Thread is closed')
        allowed = set(state['agents']) | {'all', 'both', 'owner'}
        if author == 'owner':
            allowed.update(('keep', 'pause', 'close'))
        if nxt not in allowed:
            raise Refused('Unknown --next')
        if author != 'owner' and author not in state['floor']:
            raise Refused('Not on the floor')
        if not body.strip():
            raise Refused('Empty body')
        if author != 'owner' and len(body.splitlines()) > state['config']['max_lines']:
            raise Refused('Body exceeds max_lines')
        if '\n' in round_label or '\r' in round_label:
            raise Refused('Round label must be a single line')
        if seen is not None:
            newer = [m for m in state['messages'] if m['n'] > seen and m['author'] != author]
            if newer:
                raise Unseen(newer)
        message = {'n': 0, 'author': author, 'next': nxt, 'round': round_label,
                   'time': datetime.now().isoformat(timespec='seconds'), 'body': body}
        number = state['messages'][-1]['n'] + 1 if state['messages'] else 1

        def publish(item):
            nonlocal number
            item['n'] = number
            target = path / '{:04d}-{}.md'.format(number, item['author'])
            atomic_write(target, message_text(item))
            number += 1
            return target.name

        if author != 'owner' and state['parallel']:
            atomic_write(path / 'sealed' / (author + '.md'), message_text(message))
            held = [read_message(p) for p in sorted((path / 'sealed').glob('*.md'))]
            if not {m['author'] for m in held} >= set(state['parallel']):
                return 'held'
            result = None
            for item in held:
                filename = publish(item)
                if item['author'] == author:
                    result = filename
            for item in held:
                (path / 'sealed' / item['file']).unlink()
            return result
        if author == 'owner' and nxt != 'keep':
            for item in state['held']:
                publish(item)
                (path / 'sealed' / item['file']).unlink()
        return publish(message)


def unseen(state, author):
    """Published messages by others since the author's last post (or its parallel batch)."""
    own = [m for m in state['messages'] if m['author'] == author]
    last = own[-1].get('batch', own[-1]['n'] + 1) - 1 if own else 0
    return [m for m in state['messages'] if m['n'] > last and m['author'] != author]


def wait(path, author, timeout):
    if author not in snapshot(path)['config']['participants']:
        raise Refused('Unknown participant')
    deadline = time.monotonic() + timeout
    while True:
        state = snapshot(path)
        if state['closed']:
            return 3
        if author in state['floor']:
            for message in unseen(state, author):
                print(message_text(message), end='\n')
            return 0
        if time.monotonic() >= deadline:
            return 2
        time.sleep(0.5)


def agents(path):
    try:
        return json.loads((path / 'agents.json').read_text(encoding='utf-8'))
    except FileNotFoundError:
        return {}


def set_agent(path, name, entry, roster=False):
    """Write one agents.json entry; with `roster`, also join (or, for None, leave) the dialogue."""
    agent_name(name)
    with locked(path):
        data = agents(path)
        if entry is None:
            data.pop(name, None)
        else:
            data[name] = entry
        if roster or entry is not None:
            set_roster(path, name, entry is not None)
        atomic_write(path / 'agents.json', json.dumps(data, indent=2) + '\n')


def runners():
    try:
        return json.loads(RUNNERS.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return {}


UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def connect(path, data):
    """The page's "connect agent": values are checked against runners.json; argv never comes from the page."""
    name = agent_name(data.get('name'))
    runner = runners().get(data.get('runner'))
    if not isinstance(runner, dict):
        raise Refused('Unknown runner')
    if data.get('model') not in runner.get('models', []) or data.get('effort') not in runner.get('efforts', []):
        raise Refused('Model or effort not offered by this runner')
    if data.get('mode') not in ('resume', 'fresh'):
        raise Refused('Mode must be resume or fresh')
    session = data.get('session') or None
    if session is not None and (not isinstance(session, str) or not re.fullmatch(UUID, session)):
        raise Refused('Session must be a UUID')
    timeout = data.get('turn_timeout', 60)
    if not isinstance(timeout, (int, float)) or not 1 <= timeout <= 600:
        raise Refused('Turn timeout must be 1 to 600 minutes')
    if snapshot(path)['closed']:
        raise Refused('Thread is closed')
    entry = {'runner': data['runner'], 'model': data['model'], 'effort': data['effort'], 'mode': data['mode'],
             'session': session, 'turn_timeout': timeout}
    set_agent(path, name, entry)
    return entry


def command_argv(path, name, entry, prompt, session):
    """The argv of one turn: the registered argv, or the runner's `new` / `resume` template."""
    if 'runner' not in entry:
        template = entry['argv']
    else:
        runner = runners().get(entry['runner'])
        if not isinstance(runner, dict):
            raise Refused('Runner {} is not in runners.json'.format(entry['runner']))
        template = runner['resume' if entry['mode'] == 'resume' and entry.get('session') else 'new']
    values = {'{prompt_file}': str(prompt), '{thread}': path.name, '{name}': name, '{session}': session or '',
              '{model}': entry.get('model', ''), '{effort}': entry.get('effort', '')}
    argv = list(template)
    for key, value in values.items():
        argv = [arg.replace(key, value) for arg in argv]
    return argv


def runner_of(entry):
    runner = runners().get(entry.get('runner')) if 'runner' in entry else None
    return runner if isinstance(runner, dict) else {}


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


def log_order(name):
    return [int(part) for part in re.findall(r'\d+', name)]


def own_count(state, name):
    return sum(m['author'] == name for m in state['messages'] + state['held'])


def limit_time(match, now):
    """The time a usage limit resets, from the named groups `seconds` or `reset` (a clock time)."""
    groups = match.groupdict()
    try:
        if groups.get('seconds'):
            return now + float(groups['seconds'])
    except ValueError:
        return None
    clock = re.fullmatch(r'\s*(\d{1,2})(?::(\d{2}))?(?::\d{2})?\s*(?:([ap])\.?m\.?)?\s*', groups.get('reset') or '', re.I)
    if not clock:
        return None
    hour, minute = int(clock[1]), int(clock[2] or 0)
    if clock[3]:
        hour = hour % 12 + (12 if clock[3].lower() == 'p' else 0)
    if hour > 23 or minute > 59:
        return None
    target = datetime.fromtimestamp(now).replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target.timestamp() <= now:
        target += timedelta(days=1)
    return target.timestamp()


def turn_prompt(path, name, state, seen, fresh):
    here = Path(__file__).resolve().parent
    work = path / 'work' / name
    draft = work / '{:04d}-draft.md'.format(seen + 1)
    messages = unseen(state, name)
    lines = [
        '# Turn of `{}` in thread `{}`'.format(name, path.name), '',
        'You are `{}` in the dialogue thread `{}`. The chat dispatcher started this turn because you are on the floor.'
        .format(name, path.name), '',
        '* Contract: {}'.format(here / 'TRANSPORT.md'),
        '* Brief: {}'.format(here / state['config'].get('brief', 'BRIEF_{}.md'.format(path.name))),
        '* Your notes: {}'.format(work / 'NOTES.md'), '',
        'This is a fresh session. Read first: the contract, the brief, your notes and {} if it exists.'
        .format(path / 'HANDOVER.md') if fresh else
        'Read the contract and the brief only if they are not in your context.', '',
        '## Unseen messages', '',
        ''.join(message_text(m) + '\n' for m in messages) if messages else '(none)\n',
        '## Your step', '',
        '1. Do the step the brief prescribes; answer owner messages first.',
        '2. Write your message to {} and post it once:'.format(draft),
        '   `python3 {} post {} --as {} --next WHO [--round LABEL] --seen {} --file {}`'
        .format(Path(__file__).resolve(), path.name, name, seen, draft),
        '   Exit code 5 means new messages arrived; they are printed. Take them into account and post again with'
        ' `--seen` set to the highest number printed.',
        '3. Append at most 30 lines to your notes: decisions, open items, files.',
        '4. End your turn. Do not call `wait` or `status` and do not poll: the dispatcher starts you again when you'
        ' are on the floor.', '',
    ]
    return '\n'.join(lines)


class Dispatcher:
    """Starts a model's registered command when the model is on the floor (TRANSPORT.md §4).

    Retry bookkeeping lives in dispatch.json; the floor is still derived from the message files.
    """

    def __init__(self, path, clock=time.time):
        self.path, self.clock, self.lock, self.procs = path, clock, threading.Lock(), {}
        try:
            self.data = json.loads((path / 'dispatch.json').read_text(encoding='utf-8'))
        except FileNotFoundError:
            self.data = {}
        server = self.data.get('server')
        if server and server != os.getpid() and alive(server):
            raise Refused('Another dispatcher serves this thread (pid {})'.format(server))
        self.data['server'] = os.getpid()
        for key, value in (('paused', False), ('resumed_at', 0), ('agents', {})):
            self.data.setdefault(key, value)
        self.save()

    def save(self):
        atomic_write(self.path / 'dispatch.json', json.dumps(self.data, indent=2) + '\n')

    def auto(self, state):
        return dispatch_view(self.path, self.data, state, True)['auto']

    def kill(self, record, sig):
        try:
            os.killpg(record['pid'], sig)
        except (ProcessLookupError, PermissionError):
            pass

    def step(self):
        with self.lock:
            commands, now, exits = agents(self.path), self.clock(), {}
            for name, record in self.data['agents'].items():
                if not record.get('pid'):
                    continue
                proc = self.procs.get(name)
                if proc is not None:
                    code = proc.poll()
                else:
                    code = None if alive(record['pid']) else 'unknown'
                if code is not None:
                    exits[name] = code
                elif now - record['since'] >= commands.get(name, {}).get('turn_timeout', 60) * 60:
                    if 'term_at' not in record:
                        self.kill(record, signal.SIGTERM)
                        record['term_at'] = now
                    elif now - record['term_at'] >= 10:
                        self.kill(record, signal.SIGKILL)
            state = snapshot(self.path)
            for name, code in exits.items():
                self.finish(name, self.data['agents'][name], code, state, commands.get(name, {}))
            auto = self.auto(state) == 'on'
            for name in sorted(commands):
                record = self.data['agents'].setdefault(name, {})
                if record.get('pid'):
                    continue
                if state['closed'] or name not in state['floor']:
                    record.clear()
                elif record.get('force') or (auto and not record.get('stalled') and record.get('next_try', 0) <= now):
                    self.start(name, record, state, commands[name])
            self.save()

    def start(self, name, record, state, command):
        seen = state['messages'][-1]['n'] if state['messages'] else 0
        attempt = record.get('attempt', 0) + 1
        work = self.path / 'work' / name
        work.mkdir(parents=True, exist_ok=True)
        prompt = work / 'turn-{}.md'.format(seen)
        atomic_write(prompt, turn_prompt(self.path, name, state, seen, command.get('mode') == 'fresh'))
        log = work / 'wake-{}-{}.log'.format(seen, attempt)
        session = command.get('session') if command.get('mode') == 'resume' else None
        if not session and runner_of(command).get('session') == 'uuid':
            session = str(uuid.uuid4())
        for key in ('force', 'stalled', 'next_try'):
            record.pop(key, None)
        try:
            argv = command_argv(self.path, name, command, prompt, session)
            with open(log, 'a', encoding='utf-8') as output:
                proc = subprocess.Popen(argv, shell=False, stdin=subprocess.DEVNULL, stdout=output,
                                        stderr=subprocess.STDOUT, cwd=ROOT, start_new_session=True)
        except (OSError, Refused, KeyError) as exc:
            self.fail(record, command, None, '', 'cannot start: {}'.format(exc))
            return
        self.procs[name] = proc
        record.update(pid=proc.pid, since=self.clock(), mark=own_count(state, name), log=str(log), session=session)

    def finish(self, name, record, code, state, command):
        self.procs.pop(name, None)
        try:
            text = Path(record['log']).read_bytes()[-65536:].decode('utf-8', 'replace')
        except OSError:
            text = ''
        timed_out = 'term_at' in record
        posted = own_count(state, name) != record['mark']
        session = record.get('session')
        for key in ('pid', 'since', 'mark', 'log', 'term_at', 'session'):
            record.pop(key, None)
        if posted and command.get('mode') == 'resume' and not command.get('session'):
            pattern = runner_of(command).get('session_pattern')
            match = re.search(pattern, text) if pattern else None
            session = match['session'] if match else session
            current = agents(self.path).get(name)
            if session and current and current.get('runner') == command.get('runner') and not current.get('session'):
                current['session'] = session
                set_agent(self.path, name, current)
        if posted or state['closed'] or name not in state['floor']:
            record.clear()
        elif timed_out:
            self.fail(record, command, code, text, 'turn timeout')
        elif code == 'unknown':
            self.fail(record, command, code, text, 'exited without a post while untracked')
        else:
            self.fail(record, command, code, text, 'exit {} without a post'.format(code))

    def fail(self, record, command, code, text, reason):
        now = self.clock()
        record['attempt'] = record.get('attempt', 0) + 1
        record.setdefault('first_failure', now)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        record['error'] = (reason + (': ' + lines[-1] if lines else ''))[:200]
        retry = now + RETRY[min(record['attempt'], len(RETRY)) - 1]
        pattern = command.get('limit_pattern') or runner_of(command).get('limit_pattern')
        match = re.search(pattern, text) if pattern else None
        if match:
            reset = limit_time(match, now)
            if reset is not None:
                retry = reset + 60
        elif code == 0 and reason.startswith('exit'):
            record['quiet'] = record.get('quiet', 0) + 1
        if record.get('quiet', 0) >= 3 or now - record['first_failure'] >= 86400:
            record['stalled'] = True
            record.pop('next_try', None)
        else:
            record['next_try'] = retry

    def wake(self, name):
        """Owner's "wake now": one attempt now, also when stalled or paused; never a second process."""
        with self.lock:
            if name not in agents(self.path):
                raise Refused('No command registered for {}'.format(name))
            record = self.data['agents'].setdefault(name, {})
            if record.get('pid'):
                raise Refused('{} is already running'.format(name))
            state = snapshot(self.path)
            if state['closed'] or name not in state['floor']:
                raise Refused('{} is not on the floor'.format(name))
            record['force'] = True
            self.save()
        self.step()

    def set_paused(self, paused):
        with self.lock:
            self.data['paused'] = paused
            if not paused:
                messages = snapshot(self.path)['messages']
                self.data['resumed_at'] = messages[-1]['n'] if messages else 0
            self.save()

    def view(self):
        with self.lock:
            return dispatch_view(self.path, self.data, snapshot(self.path), True)


def inline(text):
    """Escape each source fragment before emitting any renderer-owned HTML."""
    pattern = r'(`[^`]+`|\*\*(?=\S)[^*]+(?<=\S)\*\*|\*(?=\S)[^*]+(?<=\S)\*)'
    parts = re.split(pattern, text)
    output = []
    for part in parts:
        if part.startswith('`') and part.endswith('`') and len(part) > 1:
            output.append('<code>' + html.escape(part[1:-1]) + '</code>')
        elif part.startswith('**') and part.endswith('**') and len(part) > 3:
            output.append('<strong>' + html.escape(part[2:-2]) + '</strong>')
        elif part.startswith('*') and part.endswith('*') and len(part) > 1:
            output.append('<em>' + html.escape(part[1:-1]) + '</em>')
        else:
            output.append(html.escape(part))
    return ''.join(output)


ITEM = r'^(\s*)([-*+] |\d+\. )(.*)'
BLOCK = r'^(```|#{1,6} |\s*(?:[-*+] |\d+\. )|.*\|)'


def render_markdown(body):
    lines, output, i = body.splitlines(), [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            output.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
        elif re.match(r'^#{1,6} ', line):
            level = len(line.split(' ', 1)[0])
            output.append('<h{0}>{1}</h{0}>'.format(level, inline(line[level + 1:])))
        elif i + 1 < len(lines) and '|' in line and re.fullmatch(r'\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*', lines[i + 1]):
            def cells(row, tag):
                return '<tr>' + ''.join('<{0}>{1}</{0}>'.format(tag, inline(c.strip())) for c in row.strip().strip('|').split('|')) + '</tr>'
            table = ['<div class="table"><table>', cells(line, 'th')]
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                table.append(cells(lines[i], 'td'))
                i += 1
            output.append(''.join(table) + '</table></div>')
            continue
        elif re.match(ITEM, line):
            first = re.match(ITEM, line)
            ordered, items = first[2][0].isdigit(), []
            while i < len(lines):
                match = re.match(ITEM, lines[i])
                if match and match[1] == first[1] and match[2][0].isdigit() == ordered:
                    items.append(inline(match[3]))
                elif match and len(match[1]) > len(first[1]):
                    items[-1] += '<br>' + html.escape(match[2]) + inline(match[3])
                elif lines[i].startswith((' ', '\t')) and lines[i].strip():
                    items[-1] += ' ' + inline(lines[i].strip())
                elif not lines[i].strip() and i + 1 < len(lines) and re.match(ITEM, lines[i + 1]):
                    pass
                else:
                    break
                i += 1
            start = ' start="{}"'.format(int(first[2][:-2])) if ordered else ''
            output.append('<{0}{1}>{2}</{0}>'.format('ol' if ordered else 'ul', start,
                                                     ''.join('<li>' + item + '</li>' for item in items)))
            continue
        elif line.strip():
            paragraph = [line.strip()]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(BLOCK, lines[i + 1]):
                i += 1
                paragraph.append(lines[i].strip())
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
        i += 1
    return ''.join(output)


def compact(value, limit=300):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + ' …'


def flatten(content):
    if isinstance(content, list):
        return '\n'.join(c.get('text', '') if isinstance(c, dict) else str(c) for c in content)
    return content if isinstance(content, str) else compact(content)


def console_event(event):
    """Readable lines of one JSON event of `claude -p --output-format stream-json` or `codex exec --json`."""
    kind = event.get('type')
    if kind in ('assistant', 'user'):
        lines = []
        for part in (event.get('message') or {}).get('content') or []:
            if not isinstance(part, dict):
                continue
            if part.get('type') == 'text':
                lines.append(['text', part.get('text', '')])
            elif part.get('type') == 'thinking':
                lines.append(['think', part.get('thinking', '')])
            elif part.get('type') == 'tool_use':
                lines.append(['tool', '{} {}'.format(part.get('name'), compact(part.get('input')))])
            elif part.get('type') == 'tool_result':
                lines.append(['output', compact(flatten(part.get('content')), 4000)])
        return lines
    if kind == 'system':
        return [['info', 'session {} · {}'.format(event.get('session_id'), event.get('model'))]] if event.get('subtype') == 'init' else []
    if kind == 'result':
        return [['error' if event.get('is_error') else 'info', 'result: {} · {} turns · cost {}'.format(
            event.get('subtype'), event.get('num_turns'), event.get('total_cost_usd'))]]
    if kind == 'thread.started':
        return [['info', 'session {}'.format(event.get('thread_id'))]]
    if kind in ('item.started', 'item.completed'):
        item = event.get('item') or {}
        done, sort = kind == 'item.completed', item.get('type')
        if sort == 'command_execution':
            return [['tool', item.get('command', '')]] if not done else [
                ['output', compact('{}\n(exit {})'.format(item.get('aggregated_output', ''), item.get('exit_code')), 4000)]]
        if not done:
            return []
        if sort == 'agent_message':
            return [['text', item.get('text', '')]]
        if sort == 'reasoning':
            return [['think', item.get('text', '')]]
        if sort == 'file_change':
            return [['tool', 'edit ' + ', '.join(str(c.get('path')) for c in item.get('changes', []) if isinstance(c, dict))]]
        if sort == 'error':
            return [['error', item.get('message', '')]]
        return [['info', compact(item)]]
    if kind in ('turn.started', 'item.updated', 'stream_event'):
        return []
    if kind == 'turn.completed':
        return [['info', 'turn completed · usage {}'.format(compact(event.get('usage')))]]
    if kind in ('turn.failed', 'error'):
        return [['error', compact(event.get('error') or event.get('message'), 2000)]]
    return None


def console(path, name, log=None):
    """The rendered tail of one wake log of an agent (the latest by default)."""
    work = path / 'work' / agent_name(name)
    logs = sorted((p.name for p in work.glob('wake-*.log')), key=log_order)
    if log is None and logs:
        log = logs[-1]
    if log is None:
        return {'logs': [], 'log': None, 'lines': []}
    if not re.fullmatch(r'wake-\d+-\d+\.log', log) or log not in logs:
        raise Refused('Unknown log')
    data = (work / log).read_bytes()
    text = data[-524288:].decode('utf-8', 'replace')
    if len(data) > 524288:
        text = text.split('\n', 1)[-1]
    lines = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            event = None
        rendered = console_event(event) if isinstance(event, dict) else None
        if rendered is None and line.strip():
            rendered = [['raw', compact(line, 2000)]]
        lines.extend(rendered or [])
    return {'logs': logs, 'log': log, 'lines': lines}


def dispatch_view(path, data, state, dispatching):
    commands, result = agents(path), {}
    records = data.get('agents', {})
    for name in sorted(set(state['agents']) | set(commands)):
        record, command = records.get(name, {}), commands.get(name, {})
        result[name] = {
            'runner': command.get('runner') or ('custom' if command else None), 'model': command.get('model'),
            'effort': command.get('effort'), 'mode': command.get('mode'), 'session': command.get('session'),
            'in_dialogue': name in state['agents'], 'on_floor': name in state['floor'],
            'state': ('running' if record.get('pid') else 'off' if name not in commands else
                      'stalled' if record.get('stalled') else 'backoff' if record.get('next_try') else 'idle'),
            'since': record.get('since'), 'next_try': record.get('next_try'),
            'attempt': record.get('attempt', 0), 'error': record.get('error')}
    start = max([m['n'] for m in state['messages'] if m['author'] == 'owner'] + [data.get('resumed_at', 0)])
    turns = sum(1 for m in state['messages'] if m['n'] > start and m['author'] != 'owner')
    limit = state['config'].get('max_auto_turns', 12)
    auto = ('off' if not dispatching else 'paused' if data.get('paused') else 'turn limit' if turns >= limit else 'on')
    return {'auto': auto, 'turns': turns, 'max_auto_turns': limit, 'agents': result}


class Hub:
    """Every thread under one root, with one dispatcher per thread that has agents.json."""

    def __init__(self, root, dispatch=True, clock=time.time):
        self.root, self.dispatch, self.clock = root, dispatch, clock
        self.dispatchers, self.errors, self.lock = {}, {}, threading.Lock()

    def path(self, name):
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
            raise Refused('Invalid thread name')
        path = self.root / name
        if not (path / 'thread.json').is_file():
            raise Refused('Unknown thread')
        return path

    def names(self):
        return sorted(p.parent.name for p in self.root.glob('*/thread.json'))

    def dispatcher(self, name):
        if not self.dispatch:
            return None
        with self.lock:
            if name not in self.dispatchers:
                try:
                    self.dispatchers[name] = Dispatcher(self.path(name), self.clock)
                except Refused as exc:
                    if self.errors.get(name) != str(exc):
                        print('{}: {}'.format(name, exc), file=sys.stderr, flush=True)
                    self.errors[name] = str(exc)
                    return None
            return self.dispatchers[name]

    def step(self):
        for name in self.names():
            if name in self.dispatchers or (self.root / name / 'agents.json').is_file():
                dispatcher = self.dispatcher(name)
                if dispatcher:
                    dispatcher.step()

    def view(self, name, state=None):
        path = self.path(name)
        state = state or snapshot(path)
        dispatcher = self.dispatchers.get(name)
        if dispatcher:
            with dispatcher.lock:
                return dispatch_view(path, dispatcher.data, state, True)
        return dispatch_view(path, {}, state, self.dispatch)

    def summary(self):
        result = []
        for name in self.names():
            state = snapshot(self.path(name))
            last = state['messages'][-1] if state['messages'] else None
            result.append({'name': name, 'closed': state['closed'], 'floor': state['floor'],
                           'count': len(state['messages']), 'last': last and last['time'],
                           'dispatch': self.view(name, state), 'error': self.errors.get(name)})
        return result


PAGE = HERE / 'page.html'


def make_server(hub, port):
    class Handler(BaseHTTPRequestHandler):
        def respond(self, code, data, content_type='application/json; charset=utf-8'):
            payload = data.encode('utf-8') if isinstance(data, str) else json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass

        def local(self):
            return self.headers.get('Host') in ('{}:{}'.format(name, self.server.server_port)
                                                for name in ('127.0.0.1', 'localhost'))

        def do_GET(self):
            if not self.local():
                self.respond(403, {'error': 'Foreign Host'})
                return
            route, _, query = self.path.partition('?')
            params = {key: values[0] for key, values in parse_qs(query).items()}
            try:
                if route == '/':
                    self.respond(200, PAGE.read_text(encoding='utf-8'), 'text/html; charset=utf-8')
                elif route == '/threads':
                    self.respond(200, {'threads': hub.summary(),
                                       'runners': {name: {'label': r.get('label', name), 'models': r.get('models', []),
                                                          'efforts': r.get('efforts', [])}
                                                   for name, r in runners().items() if isinstance(r, dict)}})
                elif route == '/messages':
                    state = snapshot(hub.path(params.get('thread')))
                    for message in state['messages'] + state['held']:
                        message['html'] = render_markdown(message['body'])
                    state['dispatch'] = hub.view(params['thread'], state)
                    self.respond(200, state)
                elif route == '/console':
                    self.respond(200, console(hub.path(params.get('thread')), params.get('agent'), params.get('log')))
                else:
                    self.respond(404, {'error': 'Not found'})
            except (ValueError, OSError) as exc:
                self.respond(400, {'error': str(exc)})

        def do_POST(self):
            if not self.local() or self.headers.get('Origin') != 'http://' + self.headers.get('Host'):
                self.respond(403, {'error': 'Foreign Origin or Host'})
                return
            routes = ('/post', '/new', '/connect', '/disconnect', '/wake', '/pause', '/resume')
            if self.path not in routes:
                self.respond(404, {'error': 'Not found'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0:
                    raise ValueError('Invalid length')
                data = json.loads(self.rfile.read(length).decode('utf-8') or '{}')
                if not isinstance(data, dict):
                    raise ValueError('Expected a JSON object')
                if self.path == '/new':
                    if not isinstance(data.get('thread'), str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', data['thread']):
                        raise Refused('Invalid thread name')
                    new_thread(hub.root / data['thread'], ())
                    self.respond(200, {'thread': data['thread']})
                    return
                path = hub.path(data.get('thread'))
                if self.path == '/post':
                    if not isinstance(data.get('body'), str) or not isinstance(data.get('next'), str):
                        raise ValueError('Expected body and next strings')
                    self.respond(200, {'file': post(path, 'owner', data['next'], data['body'])})
                elif self.path == '/connect':
                    self.respond(200, {'agent': connect(path, data)})
                elif self.path == '/disconnect':
                    name = agent_name(data.get('name'))
                    dispatcher = hub.dispatcher(path.name)
                    if dispatcher and dispatcher.data['agents'].get(name, {}).get('pid'):
                        raise Refused('{} is running; wait for its turn to end'.format(name))
                    set_agent(path, name, None, roster=True)
                    self.respond(200, {'removed': name})
                else:
                    dispatcher = hub.dispatcher(path.name)
                    if dispatcher is None:
                        raise Refused('Dispatching is off for this thread')
                    if self.path == '/wake':
                        dispatcher.wake(data.get('name'))
                    else:
                        dispatcher.set_paused(self.path == '/pause')
                    self.respond(200, {'ok': True})
            except (ValueError, UnicodeError) as exc:
                self.respond(400, {'error': str(exc)})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('new', 'status', 'wait', 'post', 'serve', 'agent'):
        sub = commands.add_parser(command)
        sub.add_argument('thread', nargs='?' if command == 'serve' else None)
        if command in ('post', 'wait', 'agent'):
            sub.add_argument('--as', dest='author', required=True)
        if command == 'wait':
            sub.add_argument('--timeout', type=float, default=540)
        if command == 'post':
            sub.add_argument('--next', required=True)
            sub.add_argument('--round', default='')
            sub.add_argument('--file', type=Path, required=True)
            sub.add_argument('--seen', type=int)
        if command == 'serve':
            sub.add_argument('--port', type=int, default=8765)
            sub.add_argument('--no-dispatch', action='store_true')
        if command == 'agent':
            sub.add_argument('--mode', choices=('resume', 'fresh'), default='resume')
            sub.add_argument('--limit-pattern')
            sub.add_argument('--turn-timeout', type=float, default=60, help='minutes')
            sub.add_argument('--off', action='store_true')
            sub.add_argument('argv', nargs='*', help='the command after --; {prompt_file}, {thread}, {name} are substituted')
    args = parser.parse_args(argv)
    try:
        path = thread_path(args.thread) if args.thread else None
        if args.command == 'new':
            new_thread(path)
            print(path)
        elif args.command == 'post':
            print(post(path, args.author, args.next, args.file.read_text(encoding='utf-8'), args.round, args.seen))
        elif args.command == 'wait':
            return wait(path, args.author, args.timeout)
        elif args.command == 'status':
            state = snapshot(path)
            print(json.dumps({'floor': state['floor'], 'closed': state['closed'],
                              'last': state['messages'][-1] if state['messages'] else None,
                              'held': [m['author'] for m in state['held']]}, ensure_ascii=False))
        elif args.command == 'agent':
            if args.off != (not args.argv):
                raise Refused('Give either --off or the command after --')
            if args.limit_pattern:
                try:
                    re.compile(args.limit_pattern)
                except re.error as exc:
                    raise Refused('Invalid --limit-pattern: {}'.format(exc))
            entry = None if args.off else {'argv': args.argv, 'mode': args.mode, 'limit_pattern': args.limit_pattern,
                                           'turn_timeout': args.turn_timeout}
            set_agent(path, args.author, entry)
            print(json.dumps({args.author: entry}, ensure_ascii=False))
        else:
            if path:
                snapshot(path)
            THREADS.mkdir(exist_ok=True)
            hub = Hub(THREADS, dispatch=not args.no_dispatch)
            server = make_server(hub, args.port)
            print('http://127.0.0.1:{}/{}'.format(server.server_port, '#' + path.name if path else ''), flush=True)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                while True:
                    try:
                        hub.step()
                    except Exception as exc:
                        print('dispatcher: {}'.format(exc), file=sys.stderr, flush=True)
                    time.sleep(2)
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
        return 0
    except Unseen as exc:
        for message in exc.messages:
            print(message_text(message), end='\n')
        print(str(exc), file=sys.stderr)
        return 5
    except (Refused, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
