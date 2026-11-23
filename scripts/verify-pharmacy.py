"""Check the Pharmacy scene against a git revision (default: origin/main): old IDs kept, new scene and manager present."""
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
print(f'PASS: all {len(before)} existing document IDs preserved.')
old_actors = {a['_id'] for a in old['actors']}
added = [a for a in new['actors'] if a['_id'] not in old_actors]
assert [a['name'] for a in added] == ['药铺掌柜 Pharmacy manager'], [a['name'] for a in added]
manager = added[0]
assert 'GM convenience' in manager['system']['biography']['personalDescription']['value']
assert manager['prototypeToken']['texture']['src'].endswith('/tokens/pharmacy_manager.webp')
added_scenes = [s for s in new['scenes'] if s['_id'] not in {s['_id'] for s in old['scenes']}]
assert len(added_scenes) == 1
ph = added_scenes[0]
assert ph['name'].startswith('8a · 药铺') and ph['background']['src'].endswith('/maps/pharmacy.webp')
assert (root / 'assets/maps/pharmacy.webp').exists()
ling = next(a for a in new['actors'] if a['name'] == '凌序春 Ling Xuchun')
assert ling['_id'] in old_actors
on_scene = {t['actorId'] for t in ph['tokens']}
assert {manager['_id'], ling['_id']} <= on_scene
assert ph['journalEntryPage'] and ph['flags']['gongruo-session0']['heading'] == 'The pharmacy' and ph['playlistSound']
names = [s['name'] for s in new['scenes']]
assert names.index(ph['name']) == names.index('8 · 茶楼 The Teahouse') + 1
print(f"NEW scene {ph['_id']}: {ph['name']} ({len(ph['tokens'])} tokens)")
print(f"NEW actor {manager['_id']}: {manager['name']}; Ling Xuchun keeps {ling['_id']}")
