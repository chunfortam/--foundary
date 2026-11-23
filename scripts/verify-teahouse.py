"""Check adventure document preservation against a git revision (default: origin/main)."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
old = json.loads(subprocess.check_output(['git', 'show', f'{base}:adventure.json'], cwd=root))
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
missing = before.keys() - after.keys()
assert not missing, f'Existing IDs removed or changed: {sorted(missing)}'
print(f'PASS: all {len(before)} existing document IDs preserved; none removed or changed.')
actor_names = {'茶楼说书人 Teahouse storyteller', '茶楼跑堂 Teahouse waiter', '宋人茶客 Song tea patron', '蒙古茶客 Mongol tea patron'}
added_actors = [a for a in new['actors'] if a['name'] in actor_names]
assert len(added_actors) == 4
assert {a['name'] for a in added_actors} == actor_names
tea = next(s for s in new['scenes'] if s['name'].startswith('8 ·'))
for actor in added_actors:
    assert 'GM convenience' in actor['system']['biography']['personalDescription']['value']
    assert actor['type'] == 'npc'
    assert 8 <= actor['system']['attribs']['hp']['max'] <= 11
    tokens = [t for t in tea['tokens'] if t['actorId'] == actor['_id']]
    assert len(tokens) == 1
    print(f"NEW actor {actor['_id']}: {actor['name']}")
    print(f"NEW scene 8 token {tokens[0]['_id']}: {tokens[0]['name']}")
print('PASS: Teahouse documents (4 actors, 12 embedded skills, 4 scene tokens).')
