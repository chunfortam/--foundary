"""Verify Front Street scenes and preservation against a git revision (default origin/main)."""
import hashlib
import json
import re
import subprocess
import string
import sys
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[1]
base = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
old = json.loads(subprocess.check_output(['git', 'show', f'{base}:adventure.json'], cwd=root))
new = json.loads((root / 'adventure.json').read_text())
for key, value in old.items():
    if isinstance(value, list):
        existing = {v['_id']: v for v in new[key] if isinstance(v, dict) and '_id' in v}
        assert len(existing) == sum(isinstance(v, dict) and '_id' in v for v in new[key]), f'Duplicate IDs in {key}'
        for document in value:
            if isinstance(document, dict) and '_id' in document:
                assert existing[document['_id']] == document, (key, document.get('name'))
            else:
                assert document in new[key], key
    else:
        assert new[key] == value, f'Existing adventure data changed: {key}'
before = {s['_id']: s for s in old['scenes']}
after = {s['_id']: s for s in new['scenes']}
for sid, scene in before.items():
    assert after[sid] == scene, f'Existing scene changed: {scene["name"]}'
added = [s for key in ('F1', 'F2', 'F3', 'F4') for s in new['scenes'] if s['name'].split(' · ')[0] == key]
assert [s['name'].split(' · ')[0] for s in added] == ['F1', 'F2', 'F3', 'F4']
assert any(s['name'].startswith('8a · ') for s in new['scenes'])
assert [s['sort'] for s in added] == [s['navOrder'] for s in added]
assert all(a['sort'] < b['sort'] for a, b in zip(added, added[1:]))
assert len(after) == len(new['scenes']), 'Duplicate scene IDs'
for scene, key in zip(added, ['stalls', 'wangwu', 'lings', 'wineshop']):
    alphabet = string.ascii_letters + string.digits
    expected_id = ''.join(alphabet[b % len(alphabet)] for b in hashlib.sha256(f'scene:front:{key}'.encode()).digest()[:16])
    assert scene['_id'] == expected_id
expected = [4, 11, 5, 6]
sounds = {s['_id']: s['name'] for p in new['playlists'] for s in p['sounds']}
for scene, count in zip(added, expected):
    assert (scene['width'], scene['height'], scene['grid']['size']) == (1536, 1024, 64)
    assert len(scene['tokens']) == count
    image = root / scene['background']['src'].split('/gongruo-session0/')[1]
    assert Image.open(image).size == (1536, 1024)
    flag = scene['flags']['gongruo-session0']
    journal = next(j for j in new['journal'] if j['_id'] == scene['journal'] == flag['journal'])
    page = next(p for p in journal['pages'] if p['_id'] == scene['journalEntryPage'] == flag['page'])
    assert re.search(r'<h[1-3][^>]*>[^<]*' + re.escape(flag['heading']), page['text']['content'])
    assert scene['playlistSound'] in sounds
    assert 'GM convenience' in scene['description']
    for token in scene['tokens']:
        assert any(a['_id'] == token['actorId'] for a in new['actors'])
        assert 192 <= token['x'] < 1728 and 128 <= token['y'] < 1152
    print(scene['name'])
    print('  tokens:', ', '.join(t['name'] + (' [hidden]' if t['hidden'] else '') for t in scene['tokens']))
    print(f"  journal: {journal['name']} / {page['name']} / {flag['heading']}")
    print(f"  journal IDs: {scene['journal']} / {scene['journalEntryPage']}")
    print(f"  playlistSound: {scene['playlistSound']} ({sounds[scene['playlistSound']]})")
assert sum(t['hidden'] for t in added[0]['tokens']) == 1
assert sum(t['hidden'] for t in added[1]['tokens']) == 6
print(f'PASS: {len(before)} existing scenes and all other adventure data unchanged (including all existing IDs and pc1).')
print('PASS: four Front Street scenes, 26 tokens, valid journal headings, maps and existing playlist sounds.')
print('PASS: F1–F4 have front-namespaced IDs and ordered sort/navOrder; Pharmacy 8a intact.')
