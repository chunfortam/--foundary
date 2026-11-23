"""Verify the 15 January staging and preserve the original adventure documents."""
import hashlib
import json
import math
from pathlib import Path
import string
import subprocess
import sys


root = Path(__file__).resolve().parents[1]
ref = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
old = json.loads(subprocess.check_output(['git', 'show', f'{ref}:adventure.json'], cwd=root))
new = json.loads((root / 'adventure.json').read_text())
for key, before in old.items():
    if isinstance(before, list):
        by_id = {doc['_id']: doc for doc in new[key]}
        assert len(by_id) == len(new[key]), key
        for doc in before:
            assert by_id.get(doc['_id']) == doc, (key, doc['name'])
    else:
        assert new[key] == before, key

before_module = json.loads(subprocess.check_output(['git', 'show', f'{ref}:module.json'], cwd=root))
after_module = json.loads((root / 'module.json').read_text())
assert tuple(map(int, after_module['version'].split('.'))) > tuple(map(int, before_module['version'].split('.')))
print('PASS: Existing documents are unchanged (including Day One and both Fans); module version increased.')

(scene,) = [s for s in new['scenes'] if s['name'].startswith('S1 · ')]
alphabet = string.ascii_letters + string.digits
digest = hashlib.sha256(b'scene:crossing:niu-rescue').digest()
assert scene['_id'] == ''.join(alphabet[b % len(alphabet)] for b in digest[:16])
assert (scene['width'], scene['height'], scene['grid']['size']) == (1536, 1024, 64)
assert scene['background']['src'].endswith('/street_niu.webp')
assert scene['levels'][0]['background'] == scene['background']
assert (root / scene['background']['src'].split('/', 2)[2]).is_file()

journal = next(j for j in new['journal'] if j['_id'] == scene['journal'])
page = next(p for p in journal['pages'] if p['_id'] == scene['journalEntryPage'])
flags = scene['flags']['gongruo-session0']
assert page['name'] == '街口 Street Crossing'
assert flags == {'journal': journal['_id'], 'page': page['_id'], 'heading': '15 January, noon: the rescue of Niu'}
assert flags['heading'] in page['text']['content']
print('PASS: S1 uses its namespaced ID, separate background, and the 15 January GM journal heading.')

tokens = scene['tokens']
actors = {a['_id']: a for a in new['actors']}
assert len({t['name'] for t in tokens}) == len(tokens)
all_ids = [t['_id'] for s in new['scenes'] for t in s['tokens']]
assert len(set(all_ids)) == len(all_ids)
grid = scene['grid']['size']
width, height = scene['width'], scene['height']
left, top = [math.ceil(s * scene['padding'] / grid) * grid for s in (width, height)]
for token in tokens:
    assert token['actorId'] in actors and (root / token['texture']['src'].split('/', 2)[2]).is_file()
    assert left <= token['x'] <= left + width - token['width'] * grid, token['name']
    assert top <= token['y'] <= top + height - token['height'] * grid, token['name']


def named(part):
    return [t for t in tokens if part in t['name']]


for i in range(1, 4):
    (cart,) = named(f'Cage cart {i}')
    (horse,) = named(f'Draught horse {i}')
    assert not cart['hidden'] and not horse['hidden'] and horse['x'] > cart['x']
    prisoners = named(f'Prisoner {i}.')
    assert len(prisoners) == 3
    for p in prisoners:
        assert p['hidden']
        assert cart['x'] <= p['x'] <= cart['x'] + (cart['width'] - p['width']) * grid
        assert cart['y'] <= p['y'] <= cart['y'] + (cart['height'] - p['height']) * grid
assert len(named('Cage cart')) == len(named('Draught horse')) == 3
assert len(named('Prisoner')) == 9
for part, minimum, maximum, dex, hp, blade, armor in (
        ('Escort horseman', 3, 6, 50, 12, 45, 2), ('Escort foot soldier', 5, 8, 40, 11, 40, None)):
    group = named(part)
    assert len(group) == maximum and [t['hidden'] for t in group] == [False] * minimum + [True] * (maximum - minimum)
    (actor_id,) = {t['actorId'] for t in group}
    actor = actors[actor_id]
    system = actor['system']
    assert system['characteristics']['dex']['value'] == dex and system['attribs']['hp']['max'] == hp
    assert system['attribs'].get('armor', {}).get('value') == armor
    skills = {i['name']: i['system']['adjustments']['personal'] for i in actor['items'] if i['type'] == 'skill'}
    assert dex // 2 + skills['Dodge'] == 40 and 20 + skills['Fighting (Sword)'] == blade

for part in ('General Niu', 'Nameless Fang', 'Du Guanshan', 'Winding Stream', 'Tower Jiang',
             'Loft Jiang', 'Ling Xuchun', 'Song Zeyi', 'reinforcements (group marker)', 'God-Arm Bow'):
    (token,) = named(part)
    assert token['hidden'], token['name']
assert all(not t['hidden'] for t in named('Painted gate-tower') + named('Bystander'))
assert len(named('Painted gate-tower')) == 1 and len(named('Bystander')) == 3
assert sum(actors[t['actorId']]['type'] == 'character' for t in tokens) == 3
assert not named('Hermit') and not named('Sentry')
print('PASS: All escort rolls, three horse-drawn carts, nine anonymous prisoner slots, concealed Niu, allies, and late reinforcements are staged.')
