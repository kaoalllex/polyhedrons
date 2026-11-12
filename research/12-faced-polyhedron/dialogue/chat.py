#!/usr/bin/env python3
"""Local, file-backed dialogue transport. See TRANSPORT.md for the protocol."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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

PARTICIPANTS = ('astra', 'claude', 'owner')
MODELS = {'astra', 'claude'}
THREADS = Path(__file__).resolve().parent / 'threads'
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


def new_thread(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.mkdir()
    except FileExistsError:
        raise Refused('Thread already exists')
    (path / 'sealed').mkdir()
    for author in MODELS:
        (path / 'work' / author).mkdir(parents=True)
    atomic_write(path / 'thread.json', json.dumps({
        'participants': list(PARTICIPANTS), 'max_lines': 60, 'max_auto_turns': 12,
        'created': datetime.now().isoformat(timespec='seconds'),
    }, indent=2) + '\n')


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


def speakers(value):
    return set(MODELS) if value == 'both' else {value}


def snapshot_unlocked(path):
    config = json.loads((path / 'thread.json').read_text(encoding='utf-8'))
    files = [p for p in path.glob('*.md') if re.fullmatch(r'\d+-[a-z]+\.md', p.name)]
    messages = [read_message(p) for p in sorted(files, key=lambda p: int(p.name.split('-')[0]))]
    floor, closed, pending = {'owner'}, False, None
    for message in messages:
        author, nxt = message['author'], message['next']
        if author == 'owner':
            if nxt != 'keep':
                pending = None
                closed = nxt == 'close'
                floor = set() if nxt in ('close', 'pause') else speakers(nxt)
        elif MODELS <= floor or pending is not None:
            if pending is None:
                pending = {'remaining': set(MODELS), 'next': set(), 'first': message['n']}
            message['batch'] = pending['first']
            pending['remaining'].discard(author)
            pending['next'].update(speakers(nxt))
            if not pending['remaining']:
                floor = (floor - MODELS) | pending['next']
                pending = None
        else:
            floor.discard(author)
            floor.update(speakers(nxt))
    held = [read_message(p) for p in sorted((path / 'sealed').glob('*.md'))]
    waiting = ((floor - MODELS) | pending['remaining'] if pending else floor) - {m['author'] for m in held}
    return {'config': config, 'messages': messages, 'floor': sorted(waiting),
            'closed': closed, 'held': held}


def snapshot(path):
    with locked(path):
        return snapshot_unlocked(path)


def post(path, author, nxt, body, round_label='', seen=None):
    """The sole writer path for both CLI and HTTP messages."""
    with locked(path):
        state = snapshot_unlocked(path)
        if author not in state['config']['participants'] or author not in PARTICIPANTS:
            raise Refused('Unknown participant')
        if state['closed']:
            raise Refused('Thread is closed')
        allowed = {'astra', 'claude', 'both', 'owner'}
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

        if author != 'owner' and (MODELS <= set(state['floor']) or state['held']):
            atomic_write(path / 'sealed' / (author + '.md'), message_text(message))
            held = [read_message(p) for p in sorted((path / 'sealed').glob('*.md'))]
            if len(held) < 2:
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
    if author not in PARTICIPANTS:
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


def set_agent(path, name, entry):
    """Local configuration only: the CLI is the sole writer of agents.json."""
    if name not in MODELS:
        raise Refused('Unknown model')
    with locked(path):
        data = agents(path)
        if entry is None:
            data.pop(name, None)
        else:
            data[name] = entry
        atomic_write(path / 'agents.json', json.dumps(data, indent=2) + '\n')


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


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

    def turns(self, state):
        start = max([m['n'] for m in state['messages'] if m['author'] == 'owner'] + [self.data['resumed_at']])
        return sum(1 for m in state['messages'] if m['n'] > start and m['author'] in MODELS)

    def auto(self, state):
        if self.data['paused']:
            return 'paused'
        if self.turns(state) >= state['config'].get('max_auto_turns', 12):
            return 'turn limit'
        return 'on'

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
        values = {'{prompt_file}': str(prompt), '{thread}': self.path.name, '{name}': name}
        argv = list(command['argv'])
        for key, value in values.items():
            argv = [arg.replace(key, value) for arg in argv]
        for key in ('force', 'stalled', 'next_try'):
            record.pop(key, None)
        try:
            with open(log, 'a', encoding='utf-8') as output:
                proc = subprocess.Popen(argv, shell=False, stdin=subprocess.DEVNULL, stdout=output,
                                        stderr=subprocess.STDOUT, cwd=ROOT, start_new_session=True)
        except OSError as exc:
            self.fail(record, command, None, '', 'cannot start: {}'.format(exc))
            return
        self.procs[name] = proc
        record.update(pid=proc.pid, since=self.clock(), mark=own_count(state, name), log=str(log))

    def finish(self, name, record, code, state, command):
        self.procs.pop(name, None)
        try:
            text = Path(record['log']).read_bytes()[-65536:].decode('utf-8', 'replace')
        except OSError:
            text = ''
        timed_out = 'term_at' in record
        posted = own_count(state, name) != record['mark']
        for key in ('pid', 'since', 'mark', 'log', 'term_at'):
            record.pop(key, None)
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
        match = re.search(command['limit_pattern'], text) if command.get('limit_pattern') else None
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
            commands, state, result = agents(self.path), snapshot(self.path), {}
            for name in sorted(MODELS):
                record = self.data['agents'].get(name, {})
                result[name] = {
                    'state': ('running' if record.get('pid') else 'off' if name not in commands else
                              'stalled' if record.get('stalled') else 'backoff' if record.get('next_try') else 'idle'),
                    'since': record.get('since'), 'next_try': record.get('next_try'),
                    'attempt': record.get('attempt', 0), 'error': record.get('error')}
            return {'auto': self.auto(state), 'turns': self.turns(state),
                    'max_auto_turns': state['config'].get('max_auto_turns', 12), 'agents': result}


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


PAGE = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dialogue</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f5f8;color:#202530;font:16px/1.5 system-ui,sans-serif}
header,main,form{max-width:1100px;margin:auto;padding:16px}header{position:sticky;top:0;background:#f4f5f8;z-index:1;border-bottom:1px solid #ddd}
h1{font-size:1.3em;margin:0}#messages{padding-bottom:24px}.bubble{width:fit-content;max-width:90%;margin:16px 0;padding:14px 18px;border-radius:16px;background:#e1ebff;overflow-wrap:anywhere}
.bubble.claude{background:#f5e7d9}.bubble.owner{background:#d9eee4;margin-left:auto}.meta{font-size:12px;color:#505765;margin-bottom:8px}
p{margin:6px 0}pre{overflow:auto;background:#ffffff90;padding:12px;border-radius:6px}code{font-family:monospace;white-space:pre-wrap}pre code{white-space:pre}
.table{max-width:100%;overflow-x:auto}table{border-collapse:collapse}th,td{border:1px solid #b5bdc8;padding:6px 10px;white-space:pre-wrap;min-width:90px}
form{position:sticky;bottom:0;background:#f4f5f8;border-top:1px solid #ddd}textarea{display:block;width:100%;resize:vertical;min-height:90px;font:inherit;padding:10px;border:1px solid #aaa;border-radius:8px}
.controls{display:flex;gap:12px;align-items:center;margin-top:8px}button,select{font:inherit;padding:7px 12px}#error{color:#a82020}details{margin:12px 0;padding:12px;border:1px dashed #888;border-radius:8px}summary{cursor:pointer}
.chip{display:inline-flex;gap:8px;align-items:center;margin:6px 8px 0 0;padding:3px 10px;border-radius:12px;background:#e3e6ed;font-size:13px}.chip button{padding:2px 8px;font-size:12px}
</style><header><h1>Dialogue</h1><div id="status"></div><div id="agents"></div></header><main id="messages"></main>
<form id="composer"><textarea id="body" aria-label="Message" placeholder="Write a message…"></textarea><div class="controls"><label>Who answers <select id="next"></select></label><button>Send</button><span id="error" role="alert"></span></div></form>
<script>
const messages=document.querySelector('#messages'),statusLine=document.querySelector('#status'),
body=document.querySelector('#body'),next=document.querySelector('#next'),error=document.querySelector('#error'),agentsBar=document.querySelector('#agents');
let previous='',busy=false;
function control(label,url,data){const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',async()=>{error.textContent='';try{
 const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data||{})});const result=await response.json();if(!response.ok)throw Error(result.error);previous='';await refresh();
 }catch(e){error.textContent=e.message;}});return b;}
function clock(t){return new Date(t*1000).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
function dispatchBar(d){agentsBar.replaceChildren();if(!d)return;
 for(const [name,a] of Object.entries(d.agents)){const chip=document.createElement('span');chip.className='chip';let text=name+': '+a.state;
  if(a.state==='running')text+=' '+Math.floor((Date.now()/1000-a.since)/60)+' min';if(a.state==='backoff')text+=', next try '+clock(a.next_try);if(a.error)text+=' · '+a.error;
  chip.textContent=text;if(a.state!=='off'&&a.state!=='running')chip.append(control('wake now','/wake',{name}));agentsBar.append(chip);}
 const auto=document.createElement('span');auto.className='chip';auto.textContent='auto: '+d.auto+' ('+d.turns+' of '+d.max_auto_turns+' turns)';
 auto.append(d.auto==='on'?control('pause auto','/pause'):control('resume auto','/resume'));agentsBar.append(auto);}
const labels={keep:'nobody new (interjection, the floor stays)',both:'both, in parallel (answers sealed)',claude:'claude',astra:'astra',pause:'nobody (pause)',close:'nobody (close the thread)'};
function bubble(m){const b=document.createElement('article');b.className='bubble '+m.author;
 const meta=document.createElement('div');meta.className='meta';meta.textContent=['#'+m.n,m.author,m.round,m.time].filter(Boolean).join(' · ');b.append(meta);
 const content=document.createElement('div');content.innerHTML=m.html;b.append(content);return b;}
async function refresh(){try{const response=await fetch('/messages');if(!response.ok)throw Error('Cannot read thread');const s=await response.json();dispatchBar(s.dispatch);
 const signature=JSON.stringify(s);if(signature===previous)return;previous=signature;
 const bottom=window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-100;
 const expanded=new Set([...messages.querySelectorAll('details[open]')].map(d=>d.dataset.author));messages.replaceChildren();
 for(const m of s.messages)messages.append(bubble(m));
 for(const m of s.held){const d=document.createElement('details');d.dataset.author=m.author;d.open=expanded.has(m.author);
 const label=document.createElement('summary');label.textContent=m.author+' has answered; hidden until '+(m.author==='astra'?'claude':'astra')+' answers';d.append(label,bubble(m));messages.append(d);}
 statusLine.textContent=s.closed?'Thread closed':('Waiting for: '+(s.floor.join(', ')||'paused'));
 const values=(s.floor.some(x=>x!=='owner')?['keep']:[]).concat(['both','claude','astra','pause','close']);
 const selected=next.value;next.replaceChildren();if(!values.includes(selected)){const option=document.createElement('option');option.value='';option.textContent='Choose who answers';option.disabled=true;option.selected=true;if(!values.includes('keep'))next.append(option);}
 for(const value of values){const option=document.createElement('option');option.value=value;option.textContent=labels[value];next.append(option);}
 if(values.includes(selected))next.value=selected;else if(values.includes('keep'))next.value='keep';
 body.disabled=s.closed;document.querySelector('form button').disabled=s.closed;if(bottom)window.scrollTo(0,document.documentElement.scrollHeight);
 }catch(e){error.textContent=e.message;}}
document.querySelector('form').addEventListener('submit',async e=>{e.preventDefault();if(busy)return;if(!next.value){error.textContent='Choose who answers';return;}busy=true;error.textContent='';try{
 const response=await fetch('/post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({body:body.value,next:next.value})});
 const result=await response.json();if(!response.ok)throw Error(result.error);body.value='';next.value='';await refresh();
 }catch(e){error.textContent=e.message;}finally{busy=false;}});
body.addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();document.querySelector('form').requestSubmit();}});
refresh();setInterval(refresh,2000);
</script></html>'''


def make_server(path, port, dispatcher=None):
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
            elif self.path == '/':
                self.respond(200, PAGE, 'text/html; charset=utf-8')
            elif self.path == '/messages':
                state = snapshot(path)
                for message in state['messages'] + state['held']:
                    message['html'] = render_markdown(message['body'])
                if dispatcher:
                    state['dispatch'] = dispatcher.view()
                self.respond(200, state)
            else:
                self.respond(404, {'error': 'Not found'})

        def do_POST(self):
            if not self.local() or self.headers.get('Origin') != 'http://' + self.headers.get('Host'):
                self.respond(403, {'error': 'Foreign Origin or Host'})
                return
            if self.path != '/post' and (dispatcher is None or self.path not in ('/wake', '/pause', '/resume')):
                self.respond(404, {'error': 'Not found'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0:
                    raise ValueError('Invalid length')
                data = json.loads(self.rfile.read(length).decode('utf-8') or '{}')
                if not isinstance(data, dict):
                    raise ValueError('Expected a JSON object')
                if self.path == '/wake':
                    if not isinstance(data.get('name'), str):
                        raise ValueError('Expected a name string')
                    dispatcher.wake(data['name'])
                    self.respond(200, {'woken': data['name']})
                elif self.path != '/post':
                    dispatcher.set_paused(self.path == '/pause')
                    self.respond(200, {'paused': self.path == '/pause'})
                else:
                    if not isinstance(data.get('body'), str) or not isinstance(data.get('next'), str):
                        raise ValueError('Expected body and next strings')
                    filename = post(path, 'owner', data['next'], data['body'])
                    self.respond(200, {'file': filename})
            except (ValueError, UnicodeError) as exc:
                self.respond(400, {'error': str(exc)})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('new', 'status', 'wait', 'post', 'serve', 'agent'):
        sub = commands.add_parser(command)
        sub.add_argument('thread')
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
        path = thread_path(args.thread)
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
            snapshot(path)
            dispatcher = None if args.no_dispatch else Dispatcher(path)
            server = make_server(path, args.port, dispatcher)
            print('http://127.0.0.1:{}/'.format(server.server_port), flush=True)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                while True:
                    if dispatcher:
                        try:
                            dispatcher.step()
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
