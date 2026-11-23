"""Verify riverbank scene references and preservation against a git revision."""
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = sys.argv[1] if len(sys.argv) > 1 else 'main'
old = json.loads(subprocess.check_output(['git', 'show', f'{base}:adventure.json'], cwd=root))
new = json.loads((root / 'adventure.json').read_text())


def documents(value):
    found = {}
    if isinstance(value, dict):
        if '_id' in value:
            found[value['_id']] = value
        for child in value.values():
            found.update(documents(child))
    elif isinstance(value, list):
        for child in value:
            found.update(documents(child))
    return found


def fields(value):
    if isinstance(value, dict):
        return {k: fields(v) for k, v in value.items() if k not in ('sort', 'navOrder', 'version')}
    if isinstance(value, list):
        if all(isinstance(v, dict) and '_id' in v for v in value):
            return [v['_id'] for v in value if v['_id'] in before]
        return [fields(v) for v in value]
    return value


before, after = documents(old), documents(new)
assert before.keys() <= after.keys(), 'Existing document IDs removed or changed'
renamed_sounds = {'River_Flute.ogg', 'Lightless_Dawn.ogg'}
exceptions = []
for key, original in before.items():
    a, b = fields(original), fields(after[key])
    if original.get('path', '').split('/')[-1] in renamed_sounds:
        exceptions.append(f"{key}: {a['name']} -> {b['name']}")
        a.pop('name'); b.pop('name')
    assert a == b, f'Unexpected existing document change: {key} {original.get("name")}'
print(f'PASS: all {len(before)} existing document IDs preserved; existing actors/items unchanged (including HO1).')
print('Existing-field exceptions beyond sort/navOrder/version:')
for change in exceptions:
    print('  playlist sound name:', change)

actors = {a['_id']: a for a in new['actors']}
journals = {j['_id']: j for j in new['journal']}
sounds = {s['_id']: s for p in new['playlists'] for s in p['sounds']}
scenes = {s['name'].split(' · ')[0]: s for s in new['scenes']}
order = list(scenes)
assert order.index('R1') == order.index('15') + 1
assert order.index('R2') == order.index('16') + 1
assert len(actors) == len(old['actors']) + 1
assert len(new['scenes']) == len(old['scenes']) + 2
for number, heading, track, count in [
    ('R1', "East dock: the fishermen's huts", 'River_Flute.ogg', 11),
    ('R2', 'The reeds: forcing the crossing', 'Lightless_Dawn.ogg', 11),
]:
    scene = scenes[number]
    background = root / scene['background']['src'].split('/', 2)[2]
    assert background.is_file()
    assert (scene['width'], scene['height'], scene['grid']['size']) == (1536, 1024, 64)
    assert len(scene['tokens']) == count
    print(f"SCENE {number} _id={scene['_id']} background={scene['background']['src']} exists={background.is_file()}")
    for token in scene['tokens']:
        assert token['actorId'] in actors
        assert (root / token['texture']['src'].split('/', 2)[2]).is_file()
        print(f"  {token['name']} hidden={token['hidden']} actorId={token['actorId']} resolves=True")
    journal = journals[scene['journal']]
    page = next(p for p in journal['pages'] if p['_id'] == scene['journalEntryPage'])
    assert journal['name'] == '主持人 · GM: Campaign (Days 1–6)'
    assert page['name'] == '汉江沿岸 Riverbank'
    assert scene['flags']['gongruo-session0']['heading'] == heading
    assert heading in page['text']['content']
    sound = sounds[scene['playlistSound']]
    assert sound in next(p for p in new['playlists'] if p['_id'] == scene['playlist'])['sounds']
    assert sound['path'].endswith(track)
    print(f"  journal={journal['_id']} page={page['_id']} resolves={journal['name']} / {page['name']}")
    print(f"  heading={heading}; playlistSound={sound['_id']} ({track})")
fisherman = next(a for a in actors.values() if a['name'] == '渔民 Fisherman')
assert 'GM convenience' in fisherman['system']['biography']['personalDescription']['value']
assert sum(t['actorId'] == fisherman['_id'] for t in scenes['R1']['tokens']) == 4
assert sum(t['hidden'] for t in scenes['R1']['tokens']) == 2
assert sum(t['hidden'] for t in scenes['R2']['tokens']) == 6
lures = [t for t in scenes['R2']['tokens'] if t['name'] in ('河伯冯夷 River Lord He Bo', '汉水女神 The Lady of the Han', '何罗鱼 The Many-Headed Fish')]
assert len(lures) == 3 and len({t['actorId'] for t in lures}) == 1
assert actors[lures[0]['actorId']]['name'].startswith('格拉基')
for key in ('fisherman', 'hebo', 'goddess'):
    with Image.open(root / f'assets/portraits/{key}.webp') as im:
        assert im.size == (512, 512) and im.mode == 'RGB'
    with Image.open(root / f'assets/tokens/{key}.webp') as im:
        assert im.size == (512, 512) and im.mode == 'RGBA'
        assert im.getpixel((0, 0))[3] == 0
print('PASS: scene order, assets, actor/journal/music references, visibility and dream-lure actor reuse.')
