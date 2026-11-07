"""Research graph: check the headers of ideas, hypotheses and experiments, and build map/graph.json.

Schema: PROTOCOL.md section 4. Nodes are the files ideas/I-*.md, hypotheses/H-*.md, experiments/E-*/README.md plus
the things they reference (FD# / DR# rows of STATUS.md, W:<witness>, C:<certificate folder>, L:<source key>, owner).
Links are stored once on the child (origin, tests, produces); reverse links are computed by the map page.

Usage: python3 trace.py           check, then write map/graph.json
       python3 trace.py --check   check, and fail if map/graph.json is out of date (used by verify_all)
Exit status 1 on any error."""
import glob
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
GRAPH = os.path.join(ROOT, 'map', 'graph.json')
GRAPH_JS = os.path.join(ROOT, 'map', 'graph.js')   # same data as a script, so the map opens from file://
ID_RE = re.compile(r'^([IHE])-(\d{6})-(\d{2,3})$')
KINDS = {'I': ('idea', 'ideas/I-*.md', {'open', 'tried', 'parked'}),
         'H': ('hypothesis', 'hypotheses/H-*.md', {'open', 'supported', 'weakened', 'refuted', 'proved'}),
         'E': ('experiment', 'experiments/E-*/README.md', {'planned', 'running', 'done', 'killed'})}
LINKS = ('origin', 'tests', 'produces')


def header(path):
    """The key: value / key: [a, b] lines between the first two '---' lines."""
    lines = open(path, encoding='utf-8').read().split('\n')
    if not lines or lines[0].strip() != '---':
        raise ValueError('no header')
    out = {}
    for ln in lines[1:]:
        if ln.strip() == '---':
            return out
        ln = ln.split(' #')[0].rstrip()
        if not ln.strip():
            continue
        k, sep, v = ln.partition(':')
        if not sep or not re.fullmatch(r'[a-z_]+', k):
            raise ValueError('bad header line: %r' % ln)
        v = v.strip()
        out[k] = [x.strip() for x in v[1:-1].split(',') if x.strip()] if v.startswith('[') and v.endswith(']') else v
    raise ValueError('header not closed')


def ledger():
    """External node titles: FD/DR rows, witnesses, certificates, literature keys."""
    titles = {'owner': ('owner', 'Project owner', '')}
    status = open(os.path.join(ROOT, 'STATUS.md'), encoding='utf-8').read()
    for m in re.finditer(r'^\| (FD\d+|DR\d+) \| ([^|]+)\|', status, re.M):
        titles[m.group(1)] = ('foundation' if m.group(1).startswith('FD') else 'direction', m.group(2).strip(), 'STATUS.md')
    for w in json.load(open(os.path.join(ROOT, 'witnesses', 'witnesses.json'))):
        titles['W:' + w['id']] = ('witness', w['title'], w['source'])
    for d in sorted(glob.glob(os.path.join(ROOT, 'verification', 'certificates', '*', ''))):
        name = os.path.basename(d.rstrip('/'))
        titles['C:' + name] = ('certificate', name.replace('_', ' '), os.path.relpath(d, ROOT))
    lit = open(os.path.join(ROOT, 'literature', 'README.md'), encoding='utf-8').read()
    for m in re.finditer(r'^\| `([a-z0-9-]+)` \| ([^|]+)\|', lit, re.M):
        titles['L:' + m.group(1)] = ('source', re.sub(r'[*`]', '', m.group(2)).strip()[:120], 'literature/README.md')
    return titles


def build():
    errors, nodes, edges = [], {}, []
    for letter, (kind, pattern, statuses) in KINDS.items():
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            rel = os.path.relpath(path, ROOT)
            try:
                h = header(path)
            except ValueError as e:
                errors.append('%s: %s' % (rel, e))
                continue
            nid = h.get('id', '')
            m = ID_RE.match(nid)
            stem = os.path.basename(os.path.dirname(path)) if letter == 'E' else os.path.basename(path)
            if not m or m.group(1) != letter:
                errors.append('%s: bad id %r' % (rel, nid))
                continue
            if not stem.startswith(nid + '-') and stem != nid + '.md':
                errors.append('%s: file name does not start with its id %s' % (rel, nid))
            if h.get('date', '').replace('-', '')[2:] != m.group(2):
                errors.append('%s: date %r does not match id %s' % (rel, h.get('date'), nid))
            if h.get('concluded') and not (re.fullmatch(r'\d{4}-\d{2}-\d{2}', h['concluded']) and h['concluded'] >= h.get('date', '')):
                errors.append('%s: concluded %r is not a date on or after %r' % (rel, h['concluded'], h.get('date')))
            if not h.get('title'):
                errors.append('%s: no title' % rel)
            if h.get('status') not in statuses:
                errors.append('%s: status %r not in %s' % (rel, h.get('status'), sorted(statuses)))
            if nid in nodes:
                errors.append('%s: duplicate id %s (also %s)' % (rel, nid, nodes[nid]['path']))
            for k in LINKS:
                if k in h and not isinstance(h[k], list):
                    errors.append('%s: %s must be a [list]' % (rel, k))
            nodes[nid] = {'id': nid, 'kind': kind, 'title': h.get('title', ''), 'status': h.get('status', ''),
                          'date': h.get('date', ''), 'concluded': h.get('concluded', ''), 'path': rel, 'direction': h.get('direction', []),
                          'verdict': h.get('verdict', ''), 'preregistered': h.get('preregistered', ''), '_h': h}
    ext = ledger()
    used = set()
    for nid, n in nodes.items():
        h = n.pop('_h')
        for k in LINKS:
            for ref in h.get(k, []):
                if ref in nodes or ref in ext:
                    edges.append({'from': ref, 'to': nid, 'kind': k} if k == 'origin' else
                                 {'from': nid, 'to': ref, 'kind': k})
                    used.add(ref)
                else:
                    errors.append('%s: %s refers to unknown %s' % (n['path'], k, ref))
                if k == 'tests' and not ref.startswith('H-'):
                    errors.append('%s: tests must list hypotheses, got %s' % (n['path'], ref))
        for d in n['direction'] if isinstance(n['direction'], list) else [n['direction']]:
            if d not in ext:
                errors.append('%s: unknown direction %s' % (n['path'], d))
    for ref in sorted(used):
        if ref in ext:
            kind, title, path = ext[ref]
            nodes[ref] = {'id': ref, 'kind': kind, 'title': title, 'status': '', 'date': '', 'concluded': '', 'path': path,
                          'direction': [], 'verdict': '', 'preregistered': ''}
    graph = {'nodes': sorted(nodes.values(), key=lambda n: n['id']),
             'edges': sorted(edges, key=lambda e: (e['from'], e['to'], e['kind'])),
             'directions': {k: v[1] for k, v in sorted(ext.items()) if k.startswith('DR')}}   # lane titles of map/timeline.html
    return errors, graph


def main():
    errors, graph = build()
    for e in errors:
        print('ERROR', e)
    text = json.dumps(graph, ensure_ascii=False, indent=1) + '\n'
    counts = {}
    for n in graph['nodes']:
        counts[n['kind']] = counts.get(n['kind'], 0) + 1
    summary = '%d nodes (%s), %d edges' % (len(graph['nodes']), ', '.join('%s %d' % kv for kv in sorted(counts.items())),
                                          len(graph['edges']))
    if '--check' in sys.argv:
        stale = any(not os.path.exists(f) or open(f, encoding='utf-8').read() != t
                    for f, t in ((GRAPH, text), (GRAPH_JS, 'window.GRAPH = ' + text)))
        print('graph %s; %s; %d error(s)' % ('OUT OF DATE (run verification/trace.py)' if stale else 'in sync', summary,
                                             len(errors)))
        sys.exit(1 if errors or stale else 0)
    os.makedirs(os.path.dirname(GRAPH), exist_ok=True)
    open(GRAPH, 'w', encoding='utf-8').write(text)
    open(GRAPH_JS, 'w', encoding='utf-8').write('window.GRAPH = ' + text)
    print('wrote map/graph.json: %s; %d error(s)' % (summary, len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
