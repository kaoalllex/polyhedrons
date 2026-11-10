#!/usr/bin/env python3
"""Local, file-backed dialogue transport. See TRANSPORT.md for the protocol."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

PARTICIPANTS = ('astra', 'claude', 'owner')
MODELS = {'astra', 'claude'}
THREADS = Path(__file__).resolve().parent / 'threads'


class Refused(ValueError):
    pass


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
        'participants': list(PARTICIPANTS), 'max_lines': 60,
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
        elif floor == MODELS or pending is not None:
            if pending is None:
                pending = {'remaining': set(MODELS), 'next': set()}
            pending['remaining'].discard(author)
            pending['next'].update(speakers(nxt))
            if not pending['remaining']:
                floor = pending['next']
                pending = None
        else:
            floor.discard(author)
            floor.update(speakers(nxt))
    held = [read_message(p) for p in sorted((path / 'sealed').glob('*.md'))]
    waiting = (pending['remaining'] if pending else floor) - {m['author'] for m in held}
    return {'config': config, 'messages': messages, 'floor': sorted(waiting),
            'closed': closed, 'held': held}


def snapshot(path):
    with locked(path):
        return snapshot_unlocked(path)


def post(path, author, nxt, body, round_label=''):
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

        if author != 'owner' and (set(state['floor']) == MODELS or state['held']):
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


def wait(path, author, timeout):
    if author not in PARTICIPANTS:
        raise Refused('Unknown participant')
    deadline = time.monotonic() + timeout
    while True:
        state = snapshot(path)
        if state['closed']:
            return 3
        if author in state['floor']:
            last = max((m['n'] for m in state['messages'] if m['author'] == author), default=0)
            for message in state['messages']:
                if message['n'] > last:
                    print(message_text(message), end='\n')
            return 0
        if time.monotonic() >= deadline:
            return 2
        time.sleep(0.5)


def inline(text):
    """Escape each source fragment before emitting any renderer-owned HTML."""
    pattern = r'(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)'
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
        elif re.match(r'^\s*(?:[-*+] |\d+\. )', line):
            ordered = bool(re.match(r'^\s*\d+\. ', line))
            tag = 'ol' if ordered else 'ul'
            output.append('<' + tag + '>')
            pattern = r'^\s*\d+\. (.*)' if ordered else r'^\s*[-*+] (.*)'
            while i < len(lines):
                match = re.match(pattern, lines[i])
                if not match:
                    break
                output.append('<li>' + inline(match[1]) + '</li>')
                i += 1
            output.append('</' + tag + '>')
            continue
        elif line.strip():
            output.append('<p>' + inline(line) + '</p>')
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
</style><header><h1>Dialogue</h1><div id="status"></div></header><main id="messages"></main>
<form id="composer"><textarea id="body" aria-label="Message" placeholder="Write a message…"></textarea><div class="controls"><label>Who answers <select id="next"></select></label><button>Send</button><span id="error" role="alert"></span></div></form>
<script>
const messages=document.querySelector('#messages'),statusLine=document.querySelector('#status'),
body=document.querySelector('#body'),next=document.querySelector('#next'),error=document.querySelector('#error');
let previous='',busy=false;
function bubble(m){const b=document.createElement('article');b.className='bubble '+m.author;
 const meta=document.createElement('div');meta.className='meta';meta.textContent='#'+m.n+' · '+m.author+' · '+m.round+' · '+m.time;b.append(meta);
 const content=document.createElement('div');content.innerHTML=m.html;b.append(content);return b;}
async function refresh(){try{const response=await fetch('/messages');if(!response.ok)throw Error('Cannot read thread');const s=await response.json();
 const signature=JSON.stringify(s);if(signature===previous)return;previous=signature;
 const bottom=window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-100;
 const expanded=new Set([...messages.querySelectorAll('details[open]')].map(d=>d.dataset.author));messages.replaceChildren();
 for(const m of s.messages)messages.append(bubble(m));
 for(const m of s.held){const d=document.createElement('details');d.dataset.author=m.author;d.open=expanded.has(m.author);
 const label=document.createElement('summary');label.textContent=m.author+' has answered; hidden until '+(m.author==='astra'?'claude':'astra')+' answers';d.append(label,bubble(m));messages.append(d);}
 statusLine.textContent=s.closed?'Thread closed':('Waiting for: '+(s.floor.join(', ')||'paused'));
 const values=(s.floor.some(x=>x!=='owner')?['keep']:[]).concat(['both','claude','astra','pause','close']);
 const selected=next.value;next.replaceChildren();if(!values.includes(selected)){const option=document.createElement('option');option.value='';option.textContent='Choose who answers';option.disabled=true;option.selected=true;if(!values.includes('keep'))next.append(option);}
 for(const value of values){const option=document.createElement('option');option.value=value;option.textContent=value;next.append(option);}
 if(values.includes(selected))next.value=selected;else if(values.includes('keep'))next.value='keep';
 body.disabled=s.closed;document.querySelector('button').disabled=s.closed;if(bottom)window.scrollTo(0,document.documentElement.scrollHeight);
 }catch(e){error.textContent=e.message;}}
document.querySelector('form').addEventListener('submit',async e=>{e.preventDefault();if(busy)return;if(!next.value){error.textContent='Choose who answers';return;}busy=true;error.textContent='';try{
 const response=await fetch('/post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({body:body.value,next:next.value})});
 const result=await response.json();if(!response.ok)throw Error(result.error);body.value='';next.value='';await refresh();
 }catch(e){error.textContent=e.message;}finally{busy=false;}});
body.addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();document.querySelector('form').requestSubmit();}});
refresh();setInterval(refresh,2000);
</script></html>'''


def make_server(path, port):
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

        def do_GET(self):
            if self.path == '/':
                self.respond(200, PAGE, 'text/html; charset=utf-8')
            elif self.path == '/messages':
                state = snapshot(path)
                for message in state['messages'] + state['held']:
                    message['html'] = render_markdown(message['body'])
                self.respond(200, state)
            else:
                self.respond(404, {'error': 'Not found'})

        def do_POST(self):
            host = '127.0.0.1:{}'.format(self.server.server_port)
            if self.headers.get('Host') != host or self.headers.get('Origin') != 'http://' + host:
                self.respond(403, {'error': 'Foreign Origin or Host'})
                return
            if self.path != '/post':
                self.respond(404, {'error': 'Not found'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0:
                    raise ValueError('Invalid length')
                data = json.loads(self.rfile.read(length).decode('utf-8'))
                if not isinstance(data, dict) or not isinstance(data.get('body'), str) or not isinstance(data.get('next'), str):
                    raise ValueError('Expected body and next strings')
                filename = post(path, 'owner', data['next'], data['body'])
                self.respond(200, {'file': filename})
            except (ValueError, UnicodeError) as exc:
                self.respond(400, {'error': str(exc)})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('new', 'status', 'wait', 'post', 'serve'):
        sub = commands.add_parser(command)
        sub.add_argument('thread')
        if command in ('post', 'wait'):
            sub.add_argument('--as', dest='author', required=True)
        if command == 'wait':
            sub.add_argument('--timeout', type=float, default=540)
        if command == 'post':
            sub.add_argument('--next', required=True)
            sub.add_argument('--round', default='')
            sub.add_argument('--file', type=Path, required=True)
        if command == 'serve':
            sub.add_argument('--port', type=int, default=8765)
    args = parser.parse_args(argv)
    try:
        path = thread_path(args.thread)
        if args.command == 'new':
            new_thread(path)
            print(path)
        elif args.command == 'post':
            print(post(path, args.author, args.next, args.file.read_text(encoding='utf-8'), args.round))
        elif args.command == 'wait':
            return wait(path, args.author, args.timeout)
        elif args.command == 'status':
            state = snapshot(path)
            print(json.dumps({'floor': state['floor'], 'closed': state['closed'],
                              'last': state['messages'][-1] if state['messages'] else None,
                              'held': [m['author'] for m in state['held']]}, ensure_ascii=False))
        else:
            snapshot(path)
            server = make_server(path, args.port)
            print('http://127.0.0.1:{}/'.format(server.server_port), flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
        return 0
    except (Refused, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
