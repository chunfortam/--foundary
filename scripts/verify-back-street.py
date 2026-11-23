"""Verify additive Back Street documents against origin/main."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
old = json.loads(subprocess.check_output(['git', 'show', 'origin/main:adventure.json'], cwd=root))
new = json.loads((root / 'adventure.json').read_text())


def documents(value, path='adventure'):
    found = {}
    if isinstance(value, dict):
        if '_id' in value:
            path += '/' + value['_id']
            found[path] = value.get('name', '(unnamed)')
        for key, child in value.items():
            found.update(documents(child, path + '/' + key))
    elif isinstance(value, list):
        for child in value:
            found.update(documents(child, path))
    return found


before, after = documents(old), documents(new)
assert not before.keys() - after.keys(), 'Existing IDs removed or changed'
print(f'PASS: all {len(before)} existing document IDs preserved; none removed or changed.')
for key, values in old.items():
    if isinstance(values, list):
        existing = {v['_id']: v for v in new[key] if isinstance(v, dict) and '_id' in v}
        for value in values:
            if isinstance(value, dict) and '_id' in value:
                assert existing[value['_id']] == value, (key, value.get('name'))
    else:
        assert new[key] == values, key
print('PASS: every existing document is byte-for-byte equivalent as parsed JSON, including pc1 and all skills.')
added_actors = [a for a in new['actors'] if a['_id'] not in {a['_id'] for a in old['actors']}]
added_scenes = [s for s in new['scenes'] if s['_id'] not in {s['_id'] for s in old['scenes']}]
assert len(added_actors) == len(added_scenes) == 3
for actor in added_actors:
    assert 'GM convenience' in actor['system']['biography']['personalDescription']['value']
    assert actor['items'] == []
    for src in (actor['img'], actor['prototypeToken']['texture']['src']):
        assert (root / src.split('/', 2)[2]).is_file(), src
for scene, number, count, heading in zip(added_scenes, ('B1', 'B2', 'B3'), (7, 9, 5), ('The Guildhall', 'The burning house', 'Seven Treasures jeweller')):
    assert scene['name'].startswith(number + ' · ')
    assert (scene['width'], scene['height'], scene['grid']['size']) == (1536, 1024, 64)
    assert len(scene['tokens']) == count
    assert scene['flags']['gongruo-session0']['heading'] == heading
    page = next(p for j in new['journal'] for p in j['pages'] if p['_id'] == scene['journalEntryPage'])
    assert page['name'] == '后街 Back Street'
    assert sum(t['hidden'] for t in scene['tokens']) == {'B1': 1, 'B2': 5, 'B3': 0}[number]
    for token in scene['tokens']:
        assert 192 <= token['x'] < 1728 and 128 <= token['y'] < 1152
assert added_scenes[1]['environment']['darknessLevel'] == 0.4
print(f'PASS: {len(after) - len(before)} new documents: 3 actors, 3 scenes, 3 scene levels, 21 tokens.')
print('PASS: scene dimensions, token counts/visibility/bounds, assets, empty inventories and Back Street journal headings verified.')

for collection in ('actors', 'scenes'):
    ids = [doc['_id'] for doc in new[collection]]
    names = [doc['name'] for doc in new[collection]]
    assert len(ids) == len(set(ids)), collection
    assert len(names) == len(set(names)), collection
token_ids = [t['_id'] for s in new['scenes'] for t in s['tokens']]
assert len(token_ids) == len(set(token_ids))
actor_ids = {a['_id'] for a in new['actors']}
assert all(t['actorId'] in actor_ids for s in added_scenes for t in s['tokens'])
assert {s['name'].split(' · ')[0] for s in added_scenes} == {'B1', 'B2', 'B3'}
assert not {'21', '22', '23'} & {s['name'].split(' · ')[0] for s in new['scenes']}
print('PASS: B1–B3 keys are district-specific; all scene/actor names and IDs and token IDs are unique; actor references resolve.')
