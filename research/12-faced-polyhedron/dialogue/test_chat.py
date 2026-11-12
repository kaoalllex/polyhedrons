"""Protocol and HTTP tests, isolated from real dialogue threads."""
from contextlib import redirect_stdout
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

SCRIPT = Path(__file__).with_name('chat.py')
SPEC = importlib.util.spec_from_file_location('dialogue_chat', SCRIPT)
chat = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(chat)


def start_server(test, hub):
    server = chat.make_server(hub, 0)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    test.addCleanup(thread.join)
    test.addCleanup(server.server_close)
    test.addCleanup(server.shutdown)
    return 'http://127.0.0.1:{}'.format(server.server_port)


def request(base, url, data=None, origin=True):
    payload = None if data is None else json.dumps(data).encode('utf-8')
    headers = {'Origin': base} if origin is True else ({'Origin': origin} if origin else {})
    try:
        with urlopen(Request(base + url, data=payload, headers=headers), timeout=10) as response:
            return response.status, json.load(response)
    except HTTPError as exc:
        with exc:
            return exc.code, json.load(exc)


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'test'
        chat.new_thread(self.path)
        self.prefix = self.prefix_for(self.root)

    @staticmethod
    def prefix_for(root):
        return (
            'import importlib.util,pathlib,sys;'
            's=importlib.util.spec_from_file_location("chat",{!r});'
            'c=importlib.util.module_from_spec(s);s.loader.exec_module(c);'
            'c.THREADS=pathlib.Path({!r});sys.exit(c.main(sys.argv[1:]))'
        ).format(str(SCRIPT), str(root))

    def command(self, *args):
        return subprocess.run([sys.executable, '-c', self.prefix, *args],
                              capture_output=True, text=True, timeout=15)

    def floor(self):
        return chat.snapshot(self.path)['floor']

    def post(self, author, nxt, body='Answer', label='R1'):
        return chat.post(self.path, author, nxt, body, label)

    def test_floor_and_close(self):
        self.assertEqual(self.floor(), ['owner'])
        self.post('owner', 'claude')
        self.post('owner', 'keep')
        self.assertEqual(self.floor(), ['claude'])
        self.post('claude', 'astra')
        self.assertEqual(self.floor(), ['astra'])
        self.post('astra', 'owner')
        self.assertEqual(self.floor(), ['owner'])
        self.post('owner', 'both')
        self.post('owner', 'astra')
        self.assertEqual(self.floor(), ['astra'])
        self.post('owner', 'pause')
        self.assertEqual(self.floor(), [])
        self.post('owner', 'close')
        self.assertEqual(self.command('wait', 'test', '--as', 'claude', '--timeout', '0').returncode, 3)
        before = sorted(self.path.rglob('*'))
        with self.assertRaisesRegex(chat.Refused, 'closed'):
            self.post('owner', 'both')
        self.assertEqual(before, sorted(self.path.rglob('*')))

    def test_refusal_writes_nothing(self):
        body = self.root / 'body.txt'
        body.write_text('Answer', encoding='utf-8')
        before = sorted(self.path.rglob('*'))
        result = self.command('post', 'test', '--as', 'astra', '--next', 'claude', '--file', str(body))
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertIn('Not on the floor', result.stderr)
        self.assertEqual(before, sorted(self.path.rglob('*')))
        for author, nxt, text in [('unknown', 'both', 'a'), ('owner', 'bad', 'a'), ('owner', 'keep', '  ')]:
            with self.assertRaises(chat.Refused):
                self.post(author, nxt, text)
        self.assertEqual(before, sorted(self.path.rglob('*')))

    def test_parallel_sealing(self):
        self.post('owner', 'both', 'Question')
        self.assertEqual(self.post('claude', 'owner', 'Secret'), 'held')
        self.assertEqual(self.floor(), ['astra'])
        result = self.command('wait', 'test', '--as', 'astra', '--timeout', '0')
        self.assertEqual(result.returncode, 0)
        self.assertIn('Question', result.stdout)
        self.assertNotIn('Secret', result.stdout)
        self.assertEqual(self.command('wait', 'test', '--as', 'claude', '--timeout', '0').returncode, 2)
        with self.assertRaises(chat.Refused):
            self.post('claude', 'owner')
        self.assertEqual(self.post('astra', 'claude'), '0002-astra.md')
        state = chat.snapshot(self.path)
        self.assertEqual([(m['n'], m['author']) for m in state['messages']],
                         [(1, 'owner'), (2, 'astra'), (3, 'claude')])
        self.assertEqual(state['floor'], ['claude', 'owner'])
        self.assertEqual(state['held'], [])

    def test_parallel_answers_reach_both_models(self):
        self.post('owner', 'both', 'Question')
        self.post('claude', 'both', 'From claude')
        self.post('astra', 'both', 'From astra')
        for author, other in (('astra', 'From claude'), ('claude', 'From astra')):
            result = self.command('wait', 'test', '--as', author, '--timeout', '0')
            self.assertEqual(result.returncode, 0)
            self.assertIn(other, result.stdout)
            self.assertNotIn('Question', result.stdout)
        self.post('claude', 'owner', 'Second')
        self.assertEqual(self.post('astra', 'owner', 'Second too'), '0004-astra.md')
        self.assertEqual(self.floor(), ['owner'])

    def test_owner_flushes_held_before_override(self):
        for nxt, floor in [('astra', ['astra']), ('pause', []), ('close', [])]:
            with self.subTest(nxt=nxt):
                path = self.root / nxt
                chat.new_thread(path)
                chat.post(path, 'owner', 'both', 'Question')
                chat.post(path, 'claude', 'both', 'Held')
                chat.post(path, 'owner', 'keep', 'Interjection')
                self.assertEqual(len(chat.snapshot(path)['held']), 1)
                chat.post(path, 'owner', nxt, 'Override')
                state = chat.snapshot(path)
                self.assertEqual(state['floor'], floor)
                self.assertEqual([m['body'] for m in state['messages']],
                                 ['Question', 'Interjection', 'Held', 'Override'])
                self.assertEqual(state['held'], [])

    def test_concurrent_owner_posts(self):
        body = self.root / 'body.txt'
        body.write_text('Complete\n\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u0442\u0435\u043a\u0441\u0442\nEnd', encoding='utf-8')
        processes = [subprocess.Popen([sys.executable, '-c', self.prefix, 'post', 'test',
                                      '--as', 'owner', '--next', 'keep', '--file', str(body)],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for _ in range(20)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertTrue(stdout.strip().endswith('-owner.md'))
        messages = chat.snapshot(self.path)['messages']
        self.assertEqual([m['n'] for m in messages], list(range(1, 21)))
        self.assertEqual(len(list(self.path.glob('*.md'))), 20)
        self.assertTrue(all(m['body'] == body.read_text(encoding='utf-8') for m in messages))

    def test_max_lines_and_restart(self):
        self.post('owner', 'claude', 'First question')
        before = sorted(self.path.rglob('*'))
        with self.assertRaisesRegex(chat.Refused, 'max_lines'):
            self.post('claude', 'astra', '\n'.join(['x'] * 61))
        with self.assertRaises(chat.Refused):
            self.post('claude', 'keep')
        self.assertEqual(before, sorted(self.path.rglob('*')))
        self.post('claude', 'astra', '\n'.join(['x'] * 60))
        self.post('astra', 'claude', 'New answer')
        self.post('owner', 'keep', 'Latest question\n' * 70)
        expected = '\n'.join(chat.message_text(m) for m in chat.snapshot(self.path)['messages'][2:]) + '\n'
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(chat.wait(self.path, 'claude', 0), 0)
        self.assertEqual(output.getvalue(), expected)
        restarted = self.command('wait', 'test', '--as', 'claude', '--timeout', '0')
        self.assertEqual(restarted.returncode, 0)
        self.assertEqual(restarted.stdout, expected)

    def test_stale_lock_and_thread_name(self):
        import os
        import time
        lock = self.path / '.lock'
        lock.mkdir()
        os.utime(lock, (time.time() - 11, time.time() - 11))
        self.post('owner', 'keep')
        self.assertFalse(lock.exists())
        for name in ('../escape', 'Upper', '', '-bad', 'x/y'):
            with self.assertRaises(chat.Refused):
                chat.thread_path(name)

    def test_restart_with_held_answer_and_pause(self):
        self.post('owner', 'both', 'Opening')
        self.post('astra', 'both', 'Held position')
        restarted = self.command('status', 'test')
        self.assertEqual(restarted.returncode, 0, restarted.stderr)
        state = json.loads(restarted.stdout)
        self.assertEqual(state['floor'], ['claude'])
        self.assertEqual(state['held'], ['astra'])
        waiting = self.command('wait', 'test', '--as', 'claude', '--timeout', '0')
        self.assertEqual(waiting.returncode, 0)
        self.assertIn('Opening', waiting.stdout)
        self.assertNotIn('Held position', waiting.stdout)
        body = self.root / 'resumed.md'
        body.write_text('Resumed position', encoding='utf-8')
        posted = self.command('post', 'test', '--as', 'claude', '--next', 'both', '--file', str(body))
        self.assertEqual(posted.returncode, 0, posted.stderr)
        self.assertEqual(len(chat.snapshot(self.path)['messages']), 3)
        self.post('owner', 'pause', 'Until tomorrow')
        self.assertEqual(self.command('wait', 'test', '--as', 'astra', '--timeout', '0').returncode, 2)
        self.post('owner', 'both', 'Continue')
        self.assertEqual(self.command('wait', 'test', '--as', 'astra', '--timeout', '0').returncode, 0)

    def test_server_and_escaping(self):
        base = start_server(self, chat.Hub(self.root, dispatch=False))
        port = int(base.rsplit(':', 1)[1])
        payload = json.dumps({'body': '<script>alert("x")</script>\n\u041f\u0440\u0438\u0432\u0435\u0442', 'next': 'both',
                              'author': 'astra', 'thread': 'test'}).encode('utf-8')
        for headers in ({'Origin': 'https://evil.example'},
                        {'Origin': base, 'Host': 'evil.example'}, {}):
            with self.assertRaises(HTTPError) as result:
                urlopen(Request(base + '/post', data=payload, headers=headers), timeout=5)
            self.assertEqual(result.exception.code, 403)
            result.exception.close()
        self.assertEqual(chat.snapshot(self.path)['messages'], [])
        with urlopen(Request(base + '/post', data=payload, headers={'Origin': base}), timeout=5) as response:
            self.assertEqual(response.status, 200)
        with urlopen(base + '/messages?thread=test', timeout=5) as response:
            state = json.load(response)
        self.assertEqual(state['messages'][0]['author'], 'owner')
        rendered = state['messages'][0]['html']
        self.assertIn('&lt;script&gt;', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('\u041f\u0440\u0438\u0432\u0435\u0442', rendered)
        local = 'http://localhost:{}'.format(port)
        with urlopen(Request(local + '/post', data=payload, headers={'Origin': local}), timeout=5) as response:
            self.assertEqual(response.status, 200)
        with self.assertRaises(HTTPError) as result:
            urlopen(Request(base + '/messages?thread=test', headers={'Host': 'evil.example'}), timeout=5)
        self.assertEqual(result.exception.code, 403)
        result.exception.close()
        with urlopen(base, timeout=5) as response:
            page = response.read().decode('utf-8')
        self.assertIn('content.innerHTML = m.html', page)
        self.assertNotIn('<script src=', page)
        self.assertEqual(request(base, '/messages?thread=../x')[0], 400)
        status, data = request(base, '/threads')
        self.assertEqual([t['name'] for t in data['threads']], ['test'])
        self.assertEqual(request(base, '/new', {'thread': 'second'})[0], 200)
        self.assertEqual(request(base, '/new', {'thread': '../evil'})[0], 400)
        self.assertEqual([t['name'] for t in request(base, '/threads')[1]['threads']], ['second', 'test'])
        self.assertEqual(chat.snapshot(self.root / 'second')['agents'], [])

    def test_markdown(self):
        body = '# Title\n\n**bold** *italic* `code` [link](https://example.com)\n- one\n- two\n1. first\n2. second\n```\n<script>\n```\n| A | B |\n| --- | --- |\n| <img> | value |'
        rendered = chat.render_markdown(body)
        for fragment in ('<h1>Title</h1>', '<strong>bold</strong>', '<em>italic</em>',
                         '<code>code</code>', '<ul>', '<ol start="1">', '<table>', '&lt;img&gt;',
                         '&lt;script&gt;', '[link](https://example.com)'):
            self.assertIn(fragment, rendered)
        self.assertNotIn('<img>', rendered)
        self.assertNotIn('<a ', rendered)
        self.assertEqual(chat.render_markdown('E = a * b * c\nwrapped line'), '<p>E = a * b * c wrapped line</p>')
        self.assertEqual(chat.render_markdown('3. first\n   wrapped\n   - nested\n\n4. second\ntext'),
                         '<ol start="3"><li>first wrapped<br>- nested</li><li>second</li></ol><p>text</p>')


FAKE_AGENT = r'''
import importlib.util, pathlib, re, sys, time
script, threads, prompt, name, thread, plan = sys.argv[1:7]
counter = pathlib.Path(prompt).parent / 'count'
count = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(count + 1))
actions = plan.split(',')
action = actions[min(count, len(actions) - 1)]
text = pathlib.Path(prompt).read_text(encoding='utf-8')
for extra in sys.argv[7:]:
    print(extra)
if action == 'fail':
    print('boom')
    sys.exit(1)
if action == 'quiet':
    sys.exit(0)
if action == 'limit':
    print('Usage limit reached. Try again at 3:45 PM.')
    sys.exit(1)
if action == 'sleep':
    time.sleep(60)
    sys.exit(0)
spec = importlib.util.spec_from_file_location('chat', script)
chat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chat)
chat.THREADS = pathlib.Path(threads)
body = pathlib.Path(prompt).with_suffix('.body')
body.write_text('From {} {}'.format(name, count + 1), encoding='utf-8')
seen = re.search(r'--seen (\d+)', text)[1]
sys.exit(chat.main(['post', thread, '--as', name, '--next', action.split(':')[1], '--seen', seen, '--file', str(body)]))
'''


class DispatchTests(unittest.TestCase):
    """Fake agents only: no test starts a real model session."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'test'
        chat.new_thread(self.path)
        self.fake = self.root / 'fake_agent.py'
        self.fake.write_text(FAKE_AGENT, encoding='utf-8')
        self.addCleanup(setattr, chat, 'ROOT', chat.ROOT)
        chat.ROOT = self.root
        self.now = datetime(2026, 11, 12, 14, 0).timestamp()
        self.dispatchers = []
        self.addCleanup(self.kill_all)
        self.prefix = ChatTests.prefix_for(self.root)

    cli = ChatTests.command

    def kill_all(self):
        for dispatcher in self.dispatchers:
            for proc in dispatcher.procs.values():
                proc.kill()
                proc.wait()

    def dispatcher(self):
        dispatcher = chat.Dispatcher(self.path, clock=lambda: self.now)
        self.dispatchers.append(dispatcher)
        return dispatcher

    def register(self, name, plan, **options):
        entry = {'argv': [sys.executable, str(self.fake), str(SCRIPT), str(self.root), '{prompt_file}', '{name}',
                          '{thread}', plan], 'mode': 'resume', 'limit_pattern': None, 'turn_timeout': 60}
        entry.update(options)
        chat.set_agent(self.path, name, entry)

    def settle(self, dispatcher):
        for _ in range(30):
            dispatcher.step()
            if not dispatcher.procs:
                return
            for proc in list(dispatcher.procs.values()):
                proc.wait(timeout=30)
        self.fail('Dispatcher did not settle')

    def count(self, name):
        counter = self.path / 'work' / name / 'count'
        return int(counter.read_text()) if counter.exists() else 0

    def messages(self):
        return [(m['n'], m['author'], m['next']) for m in chat.snapshot(self.path)['messages']]

    def prompt_messages(self, name, seen):
        text = (self.path / 'work' / name / 'turn-{}.md'.format(seen)).read_text(encoding='utf-8')
        return text.split('## Unseen messages\n\n', 1)[1].split('\n## Your step', 1)[0]

    def test_alternation(self):
        def no_wait(*args):
            raise AssertionError('wait called')
        self.addCleanup(setattr, chat, 'wait', chat.wait)
        chat.wait = no_wait
        self.register('claude', 'post:astra')
        self.register('astra', 'post:owner')
        chat.post(self.path, 'owner', 'claude', 'Question')
        self.settle(self.dispatcher())
        self.assertEqual(self.messages(), [(1, 'owner', 'claude'), (2, 'claude', 'astra'), (3, 'astra', 'owner')])
        state = chat.snapshot(self.path)
        expected = lambda numbers: ''.join(chat.message_text(m) + '\n' for m in state['messages'] if m['n'] in numbers)
        self.assertEqual(self.prompt_messages('claude', 1), expected({1}))
        self.assertEqual(self.prompt_messages('astra', 2), expected({1, 2}))
        self.assertIn('--seen 2', (self.path / 'work' / 'astra' / 'turn-2.md').read_text(encoding='utf-8'))

    def test_parallel_step(self):
        self.register('claude', 'post:owner')
        self.register('astra', 'post:owner')
        chat.post(self.path, 'owner', 'both', 'Question')
        dispatcher = self.dispatcher()
        dispatcher.step()
        self.assertEqual(sorted(dispatcher.procs), ['astra', 'claude'])
        self.settle(dispatcher)
        self.assertEqual(self.messages(), [(1, 'owner', 'both'), (2, 'astra', 'owner'), (3, 'claude', 'owner')])
        for name in ('astra', 'claude'):
            self.assertNotIn('From', self.prompt_messages(name, 1))
            self.assertIn('Question', self.prompt_messages(name, 1))

    def test_retry_after_failures(self):
        self.register('claude', 'fail,fail,post:owner')
        chat.post(self.path, 'owner', 'claude', 'Question')
        dispatcher = self.dispatcher()
        start = self.now
        for offset, attempts in ((0, 1), (59, 1), (60, 2), (60 + 299, 2), (60 + 300, 3)):
            self.now = start + offset
            self.settle(dispatcher)
            self.assertEqual(self.count('claude'), attempts, offset)
        self.assertEqual(self.messages(), [(1, 'owner', 'claude'), (2, 'claude', 'owner')])
        self.assertEqual(dispatcher.view()['agents']['claude']['state'], 'idle')
        self.assertEqual(sorted(p.name for p in (self.path / 'work' / 'claude').glob('wake-*.log')),
                         ['wake-1-1.log', 'wake-1-2.log', 'wake-1-3.log'])

    def test_limit_reset_time(self):
        self.register('claude', 'limit,post:owner', limit_pattern=r'Try again at (?P<reset>[0-9:]+ [AP]M)')
        chat.post(self.path, 'owner', 'claude', 'Question')
        dispatcher = self.dispatcher()
        self.settle(dispatcher)
        view = dispatcher.view()['agents']['claude']
        self.assertEqual(view['state'], 'backoff')
        self.assertEqual(view['next_try'], datetime(2026, 11, 12, 15, 46).timestamp())
        self.assertIn('Try again at 3:45 PM', view['error'])
        self.now = view['next_try'] - 1
        self.settle(dispatcher)
        self.assertEqual(self.count('claude'), 1)
        self.now += 1
        self.settle(dispatcher)
        self.assertEqual(len(self.messages()), 2)
        seconds = re.search(r'in (?P<seconds>\d+) s', 'in 90 s')
        self.assertEqual(chat.limit_time(seconds, 100.0), 190.0)

    def test_quiet_exits_stall(self):
        self.register('claude', 'quiet')
        chat.post(self.path, 'owner', 'claude', 'Question')
        dispatcher = self.dispatcher()
        for offset in (0, 60, 360, 100000):
            self.now += offset
            self.settle(dispatcher)
        self.assertEqual(self.count('claude'), 3)
        self.assertEqual(dispatcher.view()['agents']['claude']['state'], 'stalled')
        dispatcher.wake('claude')
        self.settle(dispatcher)
        self.assertEqual(self.count('claude'), 4)
        self.assertEqual(dispatcher.view()['agents']['claude']['state'], 'stalled')

    def test_single_process_per_model(self):
        self.register('claude', 'sleep')
        chat.post(self.path, 'owner', 'claude', 'Question')
        first = self.dispatcher()
        first.step()
        proc = first.procs['claude']
        with self.assertRaisesRegex(chat.Refused, 'already running'):
            first.wake('claude')
        restarted = self.dispatcher()
        restarted.step()
        self.assertEqual(restarted.data['agents']['claude']['pid'], proc.pid)
        self.assertEqual(restarted.view()['agents']['claude']['state'], 'running')
        with self.assertRaisesRegex(chat.Refused, 'already running'):
            restarted.wake('claude')
        self.assertEqual(len(list((self.path / 'work' / 'claude').glob('wake-*.log'))), 1)
        data = json.loads((self.path / 'dispatch.json').read_text(encoding='utf-8'))
        data['server'] = proc.pid
        (self.path / 'dispatch.json').write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(chat.Refused, 'Another dispatcher'):
            chat.Dispatcher(self.path, clock=lambda: self.now)
        proc.kill()
        proc.wait()
        first.procs.clear()
        data['server'] = None
        (self.path / 'dispatch.json').write_text(json.dumps(data), encoding='utf-8')
        after = self.dispatcher()
        after.step()
        record = after.data['agents']['claude']
        self.assertNotIn('pid', record)
        self.assertEqual(after.view()['agents']['claude']['state'], 'backoff')

    def test_post_seen(self):
        chat.post(self.path, 'owner', 'claude', 'Question')
        chat.post(self.path, 'owner', 'keep', 'Interjection')
        body = self.root / 'answer.md'
        body.write_text('Answer', encoding='utf-8')
        before = sorted(self.path.rglob('*'))
        result = self.cli('post', 'test', '--as', 'claude', '--next', 'owner', '--seen', '1', '--file', str(body))
        self.assertEqual(result.returncode, 5, result.stderr)
        self.assertIn('Interjection', result.stdout)
        self.assertNotIn('Question', result.stdout)
        self.assertEqual(before, sorted(self.path.rglob('*')))
        result = self.cli('post', 'test', '--as', 'claude', '--next', 'owner', '--seen', '2', '--file', str(body))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.messages()[-1], (3, 'claude', 'owner'))

    def test_turn_limit_and_pause(self):
        config = json.loads((self.path / 'thread.json').read_text(encoding='utf-8'))
        config['max_auto_turns'] = 2
        (self.path / 'thread.json').write_text(json.dumps(config), encoding='utf-8')
        self.register('claude', 'post:astra')
        self.register('astra', 'post:claude')
        chat.post(self.path, 'owner', 'claude', 'Question')
        dispatcher = self.dispatcher()
        self.settle(dispatcher)
        self.assertEqual(len(self.messages()), 3)
        self.assertEqual(dispatcher.view()['auto'], 'turn limit')
        chat.post(self.path, 'owner', 'keep', 'Go on')
        self.assertEqual(dispatcher.view()['auto'], 'on')
        self.settle(dispatcher)
        self.assertEqual(len(self.messages()), 6)
        dispatcher.set_paused(False)
        dispatcher.set_paused(True)
        self.settle(dispatcher)
        self.assertEqual(dispatcher.view()['auto'], 'paused')
        self.assertEqual(len(self.messages()), 6)
        dispatcher.set_paused(False)
        self.settle(dispatcher)
        self.assertEqual(len(self.messages()), 8)

    def test_no_command_injection(self):
        self.register('claude', 'post:owner')
        agents_before = (self.path / 'agents.json').read_bytes()
        marker = self.root / 'X'
        other = self.root / 'Y'
        chat.post(self.path, 'owner', 'claude', '$(touch {})\n; touch {}\n`touch {}`'.format(marker, other, other))
        dispatcher = self.dispatcher()
        hub = chat.Hub(self.root, clock=lambda: self.now)
        hub.dispatchers['test'] = dispatcher
        base = start_server(self, hub)
        payload = json.dumps({'thread': 'test', 'name': 'claude', 'argv': ['touch', str(marker)], 'mode': 'fresh',
                              'runner': 'claude', 'model': 'm', 'effort': 'e'}).encode('utf-8')
        urls = ('/wake', '/pause', '/resume', '/connect', '/new', '/post', '/agent')
        for url in urls + ('/disconnect',):
            with self.assertRaises(HTTPError) as result:
                urlopen(Request(base + url, data=payload, headers={'Origin': 'https://evil.example'}), timeout=5)
            self.assertEqual(result.exception.code, 403)
            result.exception.close()
        self.assertEqual(dispatcher.procs, {})
        self.assertEqual(self.count('claude'), 0)
        with urlopen(Request(base + '/wake', data=payload, headers={'Origin': base}), timeout=5) as response:
            self.assertEqual(response.status, 200)
        self.settle(dispatcher)
        self.assertEqual(self.messages()[-1][1], 'claude')
        for url in urls:
            try:
                urlopen(Request(base + url, data=payload, headers={'Origin': base}), timeout=5).close()
            except HTTPError as exc:
                exc.close()
        self.assertEqual((self.path / 'agents.json').read_bytes(), agents_before)
        self.assertFalse(marker.exists())
        self.assertFalse(other.exists())
        with urlopen(base + '/messages?thread=test', timeout=5) as response:
            self.assertEqual(set(json.load(response)['dispatch']['agents']), {'astra', 'claude'})

    def runner(self, **extra):
        self.addCleanup(setattr, chat, 'RUNNERS', chat.RUNNERS)
        chat.RUNNERS = self.root / 'runners.json'
        base = [sys.executable, str(self.fake), str(SCRIPT), str(self.root), '{prompt_file}', '{name}', '{thread}']
        runner = {'models': ['m1', 'm2'], 'efforts': ['low', 'high'],
                  'new': base + ['{plan}', 'new', 'session={session}', 'model={model}', 'effort={effort}'],
                  'resume': base + ['{plan}', 'resume', 'session={session}', 'model={model}']}
        runner.update(extra)
        chat.RUNNERS.write_text(json.dumps({'fake': runner, '_comment': 'ignored'}), encoding='utf-8')

    def log(self, name, seen, attempt=1):
        return (self.path / 'work' / name / 'wake-{}-{}.log'.format(seen, attempt)).read_text(encoding='utf-8')

    def test_runner_sessions(self):
        for name, extra in (('claude', {'session': 'uuid'}),
                            ('astra', {'session_pattern': r'"thread_id": "(?P<session>[0-9a-f-]{36})"'})):
            with self.subTest(runner=name):
                self.runner(**extra)
                chat.connect(self.path, {'name': name, 'runner': 'fake', 'model': 'm2', 'effort': 'high', 'mode': 'resume'})
                runner = json.loads(chat.RUNNERS.read_text(encoding='utf-8'))['fake']
                for key in ('new', 'resume'):
                    runner[key] = [arg.replace('{plan}', 'post:' + name) for arg in runner[key]]
                if name == 'astra':
                    runner['new'].append('{"type": "thread.started", "thread_id": "11111111-2222-3333-4444-555555555555"}')
                chat.RUNNERS.write_text(json.dumps({'fake': runner}), encoding='utf-8')
                messages = len(self.messages())
                chat.post(self.path, 'owner', name, 'Question')
                dispatcher = self.dispatcher()
                self.settle(dispatcher)
                first = self.log(name, messages + 1)
                self.assertIn('new\n', first)
                self.assertIn('model=m2\neffort=high', first)
                session = chat.agents(self.path)[name]['session']
                self.assertRegex(session, chat.UUID)
                self.assertIn('session=' + (session if name == 'claude' else '\n'), first)
                chat.post(self.path, 'owner', name, 'Again')
                self.settle(dispatcher)
                second = self.log(name, messages + 3)
                self.assertIn('resume\nsession={}\nmodel=m2'.format(session), second)
                self.assertEqual(self.messages()[-1][1], name)
                self.dispatchers.remove(dispatcher)
                (self.path / 'dispatch.json').unlink()

    def test_connect_from_page(self):
        self.runner()
        hub = chat.Hub(self.root, clock=lambda: self.now)
        base = start_server(self, hub)
        good = {'thread': 'test', 'name': 'critic', 'runner': 'fake', 'model': 'm1', 'effort': 'low', 'mode': 'fresh'}
        for change in ({'runner': 'other'}, {'model': 'm3'}, {'effort': 'max'}, {'mode': 'shell'},
                       {'name': 'owner'}, {'name': 'Bad'}, {'name': 'all'}, {'session': 'x; touch y'},
                       {'turn_timeout': 0}, {'thread': '../x'}):
            self.assertEqual(request(base, '/connect', dict(good, **change))[0], 400, change)
        self.assertEqual(request(base, '/connect', good, origin='https://evil.example')[0], 403)
        self.assertEqual(chat.agents(self.path), {})
        status, data = request(base, '/connect', dict(good, argv=['touch', str(self.root / 'Z')]))
        self.assertEqual(status, 200, data)
        entry = chat.agents(self.path)['critic']
        self.assertNotIn('argv', entry)
        self.assertEqual((entry['runner'], entry['model'], entry['effort'], entry['mode']), ('fake', 'm1', 'low', 'fresh'))
        self.assertEqual(chat.snapshot(self.path)['agents'], ['astra', 'claude', 'critic'])
        status, data = request(base, '/threads')
        self.assertEqual(data['runners'], {'fake': {'label': 'fake', 'models': ['m1', 'm2'], 'efforts': ['low', 'high']}})
        agents_view = data['threads'][0]['dispatch']['agents']
        self.assertEqual((agents_view['critic']['model'], agents_view['critic']['state']), ('m1', 'idle'))
        self.assertEqual(request(base, '/disconnect', {'thread': 'test', 'name': 'critic'})[0], 200)
        self.assertEqual(chat.agents(self.path), {})
        self.assertEqual(chat.snapshot(self.path)['agents'], ['astra', 'claude'])
        self.assertFalse((self.root / 'Z').exists())

    def test_three_agents_and_roster(self):
        chat.set_agent(self.path, 'critic', {'argv': ['true']})
        chat.post(self.path, 'owner', 'all', 'Question')
        self.assertEqual(chat.post(self.path, 'claude', 'owner', 'C'), 'held')
        self.assertEqual(chat.post(self.path, 'astra', 'owner', 'A'), 'held')
        self.assertEqual(chat.snapshot(self.path)['floor'], ['critic'])
        self.assertEqual(chat.post(self.path, 'critic', 'owner', 'K'), '0004-critic.md')
        self.assertEqual(self.messages(), [(1, 'owner', 'all'), (2, 'astra', 'owner'), (3, 'claude', 'owner'),
                                           (4, 'critic', 'owner')])
        before = chat.snapshot(self.path)
        chat.set_agent(self.path, 'critic', None, roster=True)
        chat.set_agent(self.path, 'fourth', {'argv': ['true']})
        after = chat.snapshot(self.path)
        self.assertEqual([m.get('batch') for m in before['messages']], [m.get('batch') for m in after['messages']])
        self.assertEqual(after['floor'], ['owner'])
        self.assertEqual(after['agents'], ['astra', 'claude', 'fourth'])
        chat.post(self.path, 'owner', 'both', 'Second')
        self.assertEqual(chat.snapshot(self.path)['floor'], ['astra', 'claude', 'fourth'])
        with self.assertRaisesRegex(chat.Refused, 'Unknown --next'):
            chat.post(self.path, 'owner', 'critic', 'Back?')

    def test_console_rendering(self):
        work = self.path / 'work' / 'claude'
        lines = [
            {'type': 'system', 'subtype': 'init', 'session_id': 's1', 'model': 'opus'},
            {'type': 'assistant', 'message': {'content': [{'type': 'text', 'text': 'Checking #27'},
                                                          {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'ls'}}]}},
            {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': [{'type': 'text', 'text': 'a\nb'}]}]}},
            {'type': 'result', 'subtype': 'success', 'num_turns': 2, 'total_cost_usd': 0.5},
            {'type': 'thread.started', 'thread_id': 't1'},
            {'type': 'item.started', 'item': {'type': 'command_execution', 'command': 'pytest'}},
            {'type': 'item.completed', 'item': {'type': 'command_execution', 'aggregated_output': 'ok', 'exit_code': 0}},
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Posted'}},
            {'type': 'turn.failed', 'error': {'message': 'limit'}},
        ]
        (work / 'wake-3-1.log').write_text('\n'.join(json.dumps(x) for x in lines) + '\nplain <b>text</b>\n', encoding='utf-8')
        (work / 'wake-12-1.log').write_text('later\n', encoding='utf-8')
        latest = chat.console(self.path, 'claude')
        self.assertEqual((latest['logs'], latest['log'], latest['lines']), (['wake-3-1.log', 'wake-12-1.log'], 'wake-12-1.log', [['raw', 'later']]))
        kinds = [kind for kind, _ in chat.console(self.path, 'claude', 'wake-3-1.log')['lines']]
        self.assertEqual(kinds, ['info', 'text', 'tool', 'output', 'info', 'info', 'tool', 'output', 'text', 'error', 'raw'])
        for name, log in (('claude', '../thread.json'), ('../x', None), ('claude', 'wake-9-9.log')):
            with self.assertRaises(chat.Refused):
                chat.console(self.path, name, log)

    def test_turn_timeout(self):
        self.register('claude', 'sleep', turn_timeout=1)
        chat.post(self.path, 'owner', 'claude', 'Question')
        dispatcher = self.dispatcher()
        dispatcher.step()
        proc = dispatcher.procs['claude']
        self.now += 59
        dispatcher.step()
        self.assertIsNone(proc.poll())
        self.now += 1
        dispatcher.step()
        self.assertNotEqual(proc.wait(timeout=10), 0)
        dispatcher.step()
        view = dispatcher.view()['agents']['claude']
        self.assertEqual(view['state'], 'backoff')
        self.assertTrue(view['error'].startswith('turn timeout'))
        self.assertEqual(view['attempt'], 1)

    def test_agent_command(self):
        run = lambda *args: self.cli('agent', 'test', *args)
        result = run('--as', 'astra', '--mode', 'fresh', '--limit-pattern', r'in (?P<seconds>\d+)s', '--',
                     'codex', 'exec', '--flag', '{prompt_file}')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(chat.agents(self.path)['astra']['argv'], ['codex', 'exec', '--flag', '{prompt_file}'])
        self.assertEqual(run('--as', 'owner', '--', 'x').returncode, 4)
        self.assertEqual(run('--as', 'claude', '--limit-pattern', '(', '--', 'x').returncode, 4)
        self.assertEqual(run('--as', 'astra', '--off').returncode, 0)
        self.assertEqual(chat.agents(self.path), {})


if __name__ == '__main__':
    unittest.main()
