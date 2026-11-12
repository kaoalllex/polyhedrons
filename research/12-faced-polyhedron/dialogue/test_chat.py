"""Protocol and HTTP tests, isolated from real dialogue threads."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
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


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'test'
        chat.new_thread(self.path)
        self.prefix = (
            'import importlib.util,pathlib,sys;'
            's=importlib.util.spec_from_file_location("chat",{!r});'
            'c=importlib.util.module_from_spec(s);s.loader.exec_module(c);'
            'c.THREADS=pathlib.Path({!r});sys.exit(c.main(sys.argv[1:]))'
        ).format(str(SCRIPT), str(self.root))

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
        server = chat.make_server(self.path, 0)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        base = 'http://127.0.0.1:{}'.format(server.server_port)
        payload = json.dumps({'body': '<script>alert("x")</script>\n\u041f\u0440\u0438\u0432\u0435\u0442', 'next': 'both',
                              'author': 'astra', 'thread': 'other'}).encode('utf-8')
        for headers in ({'Origin': 'https://evil.example'},
                        {'Origin': base, 'Host': 'evil.example'}, {}):
            with self.assertRaises(HTTPError) as result:
                urlopen(Request(base + '/post', data=payload, headers=headers), timeout=5)
            self.assertEqual(result.exception.code, 403)
            result.exception.close()
        self.assertEqual(chat.snapshot(self.path)['messages'], [])
        with urlopen(Request(base + '/post', data=payload, headers={'Origin': base}), timeout=5) as response:
            self.assertEqual(response.status, 200)
        with urlopen(base + '/messages', timeout=5) as response:
            state = json.load(response)
        self.assertEqual(state['messages'][0]['author'], 'owner')
        rendered = state['messages'][0]['html']
        self.assertIn('&lt;script&gt;', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('\u041f\u0440\u0438\u0432\u0435\u0442', rendered)
        local = 'http://localhost:{}'.format(server.server_port)
        with urlopen(Request(local + '/post', data=payload, headers={'Origin': local}), timeout=5) as response:
            self.assertEqual(response.status, 200)
        with self.assertRaises(HTTPError) as result:
            urlopen(Request(base + '/messages', headers={'Host': 'evil.example'}), timeout=5)
        self.assertEqual(result.exception.code, 403)
        result.exception.close()
        with urlopen(base, timeout=5) as response:
            page = response.read().decode('utf-8')
        self.assertIn('content.innerHTML=m.html', page)
        self.assertNotIn('<script src=', page)

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


if __name__ == '__main__':
    unittest.main()
