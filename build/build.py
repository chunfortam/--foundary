# -*- coding: utf-8 -*-
import json, os, glob, random, string, re, shutil, copy, hashlib
from PIL import Image, ImageDraw, ImageFont
import content as C
import campaign as CP
random.seed(20260111)
MOD = C.MOD
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f'{ROOT}/assets/tokens', exist_ok=True); os.makedirs(f'{ROOT}/styles', exist_ok=True)
ALNUM = string.ascii_letters + string.digits
def rid(key=None):
    # Stable IDs: keyed IDs for top-level documents, seeded stream for embedded ones, so re-importing
    # the adventure updates existing world documents instead of duplicating them.
    if key is None: return ''.join(random.choice(ALNUM) for _ in range(16))
    h = hashlib.sha256(key.encode('utf-8')).digest()
    return ''.join(ALNUM[b % len(ALNUM)] for b in h[:16])
SK = {}
for f in glob.glob('/tmp/coc7/unpacked/en-skills/*.json'):
    j = json.load(open(f)); SK[j['flags']['CoC7']['cocidFlag']['id']] = j
CJK = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
def token_img(name, ch, color):
    p = f'{ROOT}/assets/tokens/{name}.webp'
    if os.path.exists(p): return f'modules/{MOD}/assets/tokens/{name}.webp'
    im = Image.new('RGBA', (256, 256), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.ellipse([6,6,250,250], fill=color, outline=(30,25,20,255), width=10)
    d.ellipse([22,22,234,234], outline=(255,245,220,120), width=4)
    f = ImageFont.truetype(CJK, 150); d.text((128,120), ch, font=f, fill=(255,248,230,255), anchor='mm')
    im.save(p, quality=90); return f'modules/{MOD}/assets/tokens/{name}.webp'
def portrait(tok):
    if not tok.startswith(f'modules/{MOD}/'): return tok
    p = tok.replace('/tokens/', '/portraits/')
    return p if os.path.exists(f'{ROOT}/' + p.split(f'{MOD}/')[1]) else tok
def eval_base(base, ch):
    if isinstance(base, (int, float)): return int(base)
    s = str(base)
    if '@' not in s: return int(float(s)) if s.strip() else 0
    for k, v in ch.items(): s = s.replace('@'+k.upper(), str(v)).replace('@'+k, str(v))
    try: return int(eval(s))
    except Exception: return 0
def skill(cocid, total, ch, personal=True):
    t = copy.deepcopy(SK[cocid]); t['_id'] = rid(); t.pop('_key', None); t.pop('folder', None)
    t['system']['description'] = {'value': ''}
    base = t['system'].get('base', 0); b = eval_base(base, ch)
    t['system']['adjustments'] = {'base': base if isinstance(base, str) else b, ('personal' if personal else 'occupation'): max(0, total - b)}
    t['flags']['CoC7']['cocidFlag']['lang'] = 'en'
    return t
def custom_skill(name_zh, name_en, total, spec='', props=None):
    nm = f'{name_en} {name_zh}'
    return {'_id': rid(), 'name': nm if not spec else f'{spec} ({nm})', 'type': 'skill', 'img': 'systems/CoC7/assets/icons/skills/fighting_brawl.svg',
            'system': {'description': {'value': ''}, 'base': 0, 'adjustments': {'base': 0, 'personal': total}, 'skillName': nm, 'specialization': spec,
                       'properties': dict({'push': True}, **(props or {}))}, 'flags': {}, 'effects': []}
def weapon(name, damage, skill_cocid=None, skill_id=None, rngd=False, rng=None, addb=False, ahdb=False, img='icons/weapons/swords/sword-guard-steel.webp'):
    sys = {'description': {'value': ''}, 'skill': {'main': ({'id': skill_id} if skill_id else {'name': skill_cocid})}, 'range': {'normal': {'damage': damage}},
           'properties': {'rngd': rngd, 'addb': addb, 'ahdb': ahdb}}
    if rng: sys['range']['normal']['value'] = rng; sys['bullets'] = 1; sys['usesPerRound'] = {'normal': 1}
    return {'_id': rid(), 'name': name, 'type': 'weapon', 'img': img, 'system': sys, 'flags': {}, 'effects': []}
def item(name, desc=''):
    return {'_id': rid(), 'name': name, 'type': 'item', 'img': 'icons/svg/item-bag.svg', 'system': {'description': {'value': desc}}, 'flags': {}, 'effects': []}
def chars(**k): return {c: {'value': v} for c, v in k.items()}
def hpcalc(ch): return (ch['con'] + ch['siz']) // 10
# Renamed documents keep the name their IDs were first derived from, so a rename updates the world documents in place
# (actor, its embedded items, and its scene tokens) instead of orphaning saved references.
IDNAME = {'牛富 General Niu': '牛富 Niu the Archer', '兀良哈·脱欢 General Toghan': '兀良哈·脱欢 Toghan'}
# ids are seeded from the names things first shipped with, so a rename updates the same document on re-import
IDNAME.update({'范玉楼 Commander Fan': '范玉楼 Magistrate Fan', 'Commander Fan 范玉楼': 'Magistrate Fan 范玉楼', 'Magistrate Fan 范天顺': 'Commander Fan 范天顺',
               "12 · 范天顺灵堂 Magistrate Fan's mourning hall": "12 · 范天顺灵堂 Commander Fan's mourning hall"})
IDNAME.update({'茶楼说书人 Teahouse storyteller': 'The Teahouse Storyteller (茶楼说书人)', '茶楼跑堂 Teahouse waiter': 'Teahouse Server (茶楼跑堂)', '宋人茶客 Song tea patron': 'Song Tea Patron (宋人茶客)', '蒙古茶客 Mongol tea patron': 'Mongol Tea Patron (蒙古茶客)'})
IDNAME.update({f"范家卫兵 Commander Fan's guard {i}": f"范家卫兵 Fan's guard {i}" for i in range(1, 5)})
def actor(name, atype, ch, skills, weapons, items, tok, bio_zh='', bio_en='', disposition=0, extra=None, link=True, san=None, luck=50, armor=None, sanloss=None, occupation='', age='', idkey=None, tokname=None):
    idkey = idkey or IDNAME.get(name, name); random.seed('actor:' + idkey); hp = hpcalc(ch); mp = ch['pow'] // 5
    sys = {'characteristics': chars(**ch), 'attribs': {'hp': {'value': hp, 'max': hp}, 'mp': {'value': mp, 'max': mp}, 'lck': {'value': luck}, 'san': {'value': san if san is not None else ch['pow'], 'max': 99, 'dailyLimit': 10}},
           'infos': {'occupation': occupation, 'age': age}, 'flags': {'locked': True}}
    if armor is not None: sys['attribs']['armor'] = {'value': armor}
    if atype == 'character':
        sys['biography'] = [{'title': 'Personal Description 外貌', 'value': bio_zh}, {'title': 'Background 背景', 'value': bio_en}]
        sys['flags'] = {'skillListMode': False, 'skillShowUncommon': True}
    else:
        sys['biography'] = {'personalDescription': {'value': bio_zh + bio_en}}
        if sanloss: sys['special'] = {'sanLoss': {'checkPassed': sanloss[0], 'checkFailled': sanloss[1]}, 'attacksPerRound': 1}
    if extra: sys.update(extra)
    its = skills + weapons + items
    a = {'_id': rid('actor:' + idkey), 'name': name, 'type': atype, 'img': portrait(tok), 'system': sys, 'items': its, 'effects': [], 'flags': {}, 'folder': None,
         'prototypeToken': {'name': tokname or name, 'actorLink': link, 'disposition': disposition, 'texture': {'src': tok}, 'width': 1, 'height': 1, 'sight': {'enabled': atype == 'character'}, 'displayName': 30, 'displayBars': 40 if atype != 'character' else 50, 'bar1': {'attribute': 'attribs.hp'}}}
    return a
ACT = {}
# ---------------- pregens ----------------
ch1 = dict(str=70, con=65, siz=60, dex=80, app=60, int=65, pow=65, edu=55)
t1 = token_img('pc_wanderer', '侠', (70, 90, 140, 255))
sw = skill('i.skill.fighting-sword', 75, ch1); dodge = skill('i.skill.dodge', 60, ch1)
sk1 = [sw, dodge, skill('i.skill.climb', 60, ch1), skill('i.skill.jump', 50, ch1), skill('i.skill.stealth', 60, ch1), skill('i.skill.spot-hidden', 55, ch1), skill('i.skill.listen', 45, ch1),
       skill('i.skill.disguise', 40, ch1), skill('i.skill.throw', 40, ch1), skill('i.skill.swim', 40, ch1), skill('i.skill.ride', 40, ch1), skill('i.skill.intimidate', 40, ch1),
       skill('i.skill.first-aid', 40, ch1), skill('i.skill.natural-world', 30, ch1), skill('i.skill.credit-rating', 20, ch1), skill('i.skill.language-own', 55, ch1), skill('i.skill.fighting-brawl', 50, ch1),
       skill('i.skill.track', 30, ch1), skill('i.skill.navigate', 30, ch1), skill('i.skill.psychology', 30, ch1), custom_skill('点穴', 'Acupoint Strike', 10)]
w1 = [weapon('止水 Stillwater (poisoned sword)', '1D8', 'i.skill.fighting-sword', addb=True, img='icons/weapons/swords/sword-flanged-lightning.webp'),
      weapon('佩刀 Own sabre', '1D8', 'i.skill.fighting-sword', addb=True, img='icons/weapons/swords/scimitar-worn-blue.webp'),
      weapon('飞刀 Throwing knives', '1D4', 'i.skill.throw', rngd=True, rng=10, ahdb=True, img='icons/weapons/thrown/dagger-ringed-steel.webp'),
      weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True, img='systems/CoC7/assets/icons/skills/fighting_brawl.svg')]
ACT['pc1'] = actor('陆青崖 Lu Bluecliff (HO1 The Wanderer)', 'character', ch1, sk1, w1, [item('止水 Stillwater', '师父的名剑，淬有雨师墨。The master\'s sword, coated with Rainmaster\'s Ink.'), item('行囊 Pack', '全副身家。Everything you own.')], t1,
    bio_zh='<p>'+C.PC_PUBLIC[1]['zh']+'</p>', bio_en='<p>'+C.PC_PUBLIC[1]['en']+'</p>', disposition=1, luck=60, occupation='游侠 Wanderer', age='24', idkey='HO1 游侠 · The Wanderer (陆青崖 Lu Bluecliff)', tokname='陆青崖 Lu Bluecliff')
ch2 = dict(str=50, con=60, siz=55, dex=65, app=70, int=75, pow=70, edu=70)
t2 = token_img('pc_merchant', '商', (150, 95, 60, 255))
dx = custom_skill('点穴', 'Acupoint Strike', 60)
sk2 = [dx, skill('i.skill.credit-rating', 60, ch2), skill('i.skill.medicine', 65, ch2), skill('i.skill.fighting-brawl', 50, ch2), skill('i.skill.dodge', 45, ch2), skill('i.skill.persuade', 55, ch2),
       skill('i.skill.fast-talk', 50, ch2), skill('i.skill.charm', 50, ch2), skill('i.skill.psychology', 50, ch2), skill('i.skill.appraise', 50, ch2), skill('i.skill.accounting', 45, ch2), skill('i.skill.spot-hidden', 50, ch2),
       skill('i.skill.listen', 40, ch2), skill('i.skill.science-pharmacy', 55, ch2), skill('i.skill.first-aid', 50, ch2), skill('i.skill.library-use', 40, ch2), skill('i.skill.language-own', 70, ch2), skill('i.skill.ride', 30, ch2),
       skill('i.skill.swim', 35, ch2), skill('i.skill.natural-world', 40, ch2), skill('i.skill.climb', 25, ch2), skill('i.skill.jump', 25, ch2), skill('i.skill.stealth', 30, ch2)]
w2 = [weapon('点穴 Acupoint Strike', '1D3', skill_id=dx['_id'], img='icons/skills/melee/unarmed-punch-fist.webp'),
      weapon('匕首 Dagger', '1D4+2', 'i.skill.fighting-brawl', addb=True, img='icons/weapons/daggers/dagger-straight-blue.webp'),
      weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True, img='systems/CoC7/assets/icons/skills/fighting_brawl.svg')]
ACT['pc2'] = actor('沈怀珠 Shen Pearl (HO2 The Merchant Heir)', 'character', ch2, sk2, w2, [item('药箱 Medicine chest'), item('药行印信 Pharmacy seal', '樊城分号掌柜认得你。The Fencewall branch manager knows you.')], t2,
    bio_zh='<p>'+C.PC_PUBLIC[2]['zh']+'</p>', bio_en='<p>'+C.PC_PUBLIC[2]['en']+'</p>', disposition=1, luck=65, occupation='商贾 Merchant heir', age='20', idkey='HO2 商贾 · The Merchant Heir (沈怀珠 Shen Pearl)', tokname='沈怀珠 Shen Pearl')
ch3 = dict(str=55, con=55, siz=65, dex=60, app=75, int=70, pow=65, edu=80)
t3 = token_img('pc_official', '官', (120, 60, 90, 255))
sk3 = [skill('i.skill.firearms-bow', 75, ch3), skill('i.skill.credit-rating', 75, ch3), skill('i.skill.persuade', 65, ch3), skill('i.skill.charm', 55, ch3), skill('i.skill.intimidate', 50, ch3), skill('i.skill.history', 55, ch3),
       skill('i.skill.law', 50, ch3), skill('i.skill.library-use', 55, ch3), skill('i.skill.ride', 55, ch3), skill('i.skill.spot-hidden', 50, ch3), skill('i.skill.listen', 45, ch3), skill('i.skill.psychology', 45, ch3),
       skill('i.skill.fighting-sword', 45, ch3), skill('i.skill.dodge', 40, ch3), skill('i.skill.stealth', 35, ch3), skill('i.skill.swim', 30, ch3), skill('i.skill.art-craft-any', 40, ch3), skill('i.skill.language-own', 80, ch3),
       skill('i.skill.navigate', 30, ch3), skill('i.skill.fighting-brawl', 30, ch3), skill('i.skill.climb', 25, ch3), skill('i.skill.jump', 25, ch3), custom_skill('点穴', 'Acupoint Strike', 10)]
for s in sk3:
    if s['name'].startswith('Art/Craft'): s['name'] = 'Art/Craft (Calligraphy 书法)'; s['system']['skillName'] = 'Calligraphy 书法'
w3 = [weapon('弓 Bow', '1D6', 'i.skill.firearms-bow', rngd=True, rng=30, ahdb=True, img='icons/weapons/bows/shortbow-recurve.webp'),
      weapon('佩剑 Sword', '1D8', 'i.skill.fighting-sword', addb=True, img='icons/weapons/swords/sword-guard-steel.webp'),
      weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True, img='systems/CoC7/assets/icons/skills/fighting_brawl.svg')]
ACT['pc3'] = actor('谢云骧 Xie Cloudmane (HO3 The Commissioner)', 'character', ch3, sk3, w3, [item('宣抚使印绶 Commissioner\'s seal'), item('未愈的伤 An unhealed wound', '突围时所受，自行拟定。From the breakout; you decide what it is.')], t3,
    bio_zh='<p>'+C.PC_PUBLIC[3]['zh']+'</p>', bio_en='<p>'+C.PC_PUBLIC[3]['en']+'</p>', disposition=1, luck=55, occupation='宣抚使 Commissioner', age='22', idkey='HO3 命官 · The Commissioner (谢云骧 Xie Cloudmane)', tokname='谢云骧 Xie Cloudmane')
# Every investigator's sheet lists the same skills: whatever one of them has, plus the ones the book rolls that none of them
# trained (Sleight of Hand, Locksmith, Acting), at the starting value. Art/Craft (Calligraphy) stays HO3's own specialism.
# Period belongings give the "keep three named possessions" choice on the night crossing something to bite on.
# Both are added from their own seeded stream, with the main stream restored afterwards, so no existing ID changes.
GEAR = {'pc1': [('钱袋 Purse', '一串铜钱，几块碎银。A string of copper cash and a few bits of broken silver.'),
                ('火折子 Fire-striker', '火镰、火石、火绒。Flint, steel and tinder in an oiled pouch.'),
                ('绳钩 Rope and grapple', '三丈长，翻墙上房用。Ten metres of rope with an iron hook, for walls and roofs.'),
                ('夜行衣 Night clothes', '一身黑衣，蒙面巾。Dark clothes and a face-cloth.'),
                ('师父的酒葫芦 The master\'s wine gourd', '下山时师父塞给你的。He pushed it into your hands when you left the mountain.')],
        'pc2': [('钱袋 Purse of silver', '银锭、碎银，还有一叠会子。Silver ingots, loose silver and a fold of paper notes 会子.'),
                ('路引 Travel pass', '临安府签发，写明药行少东家北上办货。Issued in Lin\'an 临安: the pharmacy heir, travelling north to buy stock.'),
                ('火折子 Fire-striker', '火镰、火石、火绒。Flint, steel and tinder in an oiled pouch.'),
                ('账簿 Account book', '樊城分号的往来账。The Fencewall branch\'s accounts, in your father\'s hand.'),
                ('父亲的玉扳指 Father\'s jade thumb ring', '从他手上取下的。You took it from his hand.')],
        'pc3': [('钱袋 Purse of silver', '银锭与碎银。Silver ingots and loose silver.'),
                ('告身 Letter of appointment', '朝廷任命你为宣抚使的文书。The court\'s commission naming you Commissioner.'),
                ('火折子 Fire-striker', '火镰、火石、火绒。Flint, steel and tinder in an oiled pouch.'),
                ('箭囊 Quiver', '十二支箭。Twelve arrows.'),
                ('母亲的平安符 Mother\'s charm', '离家时母亲缝在你衣襟里的。She sewed it into your coat the day you left.')]}
PACK = '干粮、水囊、铺盖、磨刀石。Dry rations, a water skin, a bedroll and a whetstone.'
_cid = lambda it: it.get('flags', {}).get('CoC7', {}).get('cocidFlag', {}).get('id')
ROWS = sorted({_cid(it) for k in ('pc1', 'pc2', 'pc3') for it in ACT[k]['items'] if it['type'] == 'skill' and _cid(it)} - {'i.skill.art-craft-any'}
              | {'i.skill.sleight-of-hand', 'i.skill.locksmith', 'i.skill.art-craft-acting'})
_state = random.getstate()
for k, ch_ in (('pc1', ch1), ('pc2', ch2), ('pc3', ch3)):
    random.seed('sheet-rows:' + k)
    have = {_cid(it) for it in ACT[k]['items']}
    ACT[k]['items'] += [skill(c, 0, ch_) for c in ROWS if c not in have] + [item(n, d) for n, d in GEAR[k]]
    for it in ACT[k]['items']:
        if it['name'] == '行囊 Pack': it['system']['description']['value'] = PACK
        if it['name'] == '药箱 Medicine chest': it['system']['description']['value'] = '药材、膏药、绷带、银针。Herbs, plasters, bandages and silver needles.'
        if it['name'] == '宣抚使印绶 Commissioner\'s seal': it['system']['description']['value'] = '朝廷亲授。宋人见印如见官。The court\'s own seal: to any Song subject it is your rank.'
random.setstate(_state)
# ---------------- NPCs ----------------
def npc(key, name, ch, sk, wp, ch_tok, color, notes_zh, notes_en, armor=None, disposition=-1, atype='npc', sanloss=None, link=False, hp=None):
    tok = token_img(key, ch_tok, color)
    skills = [skill(c, v, ch, personal=True) for c, v in sk if c in SK] + [custom_skill(z, e, v) for c, v in sk if c not in SK for z, e in [c.split('|')]]
    a = actor(name, atype, ch, skills, wp, [], tok, notes_zh, notes_en, disposition=disposition, armor=armor, sanloss=sanloss, link=link)
    if hp: a['system']['attribs']['hp'] = {'value': hp, 'max': hp}
    ACT[key] = a; return a
npc('ashu', '兀良哈·阿术 Marshal Ashu', dict(str=80, con=80, siz=85, dex=70, app=50, int=75, pow=60, edu=60), [('i.skill.fighting-brawl', 75), ('i.skill.fighting-sword', 75), ('i.skill.dodge', 70), ('i.skill.spot-hidden', 60), ('i.skill.ride', 80), ('i.skill.intimidate', 70)],
    [weapon('马刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True, img='icons/weapons/swords/scimitar-broad-worn.webp'), weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True)], '术', (140, 40, 40, 255),
    '<p>征南都元帅。身高八尺，体格健壮，皮肤粗糙，留须，毡帽软甲，手边一把厚重马刀。被止水刺伤后所有检定带一个惩罚骰。</p>', '<p>Commander-in-chief. Over six feet, heavy, weathered, bearded; felt hat, soft armour, a huge sabre at hand. After Stillwater: every roll with a penalty die. Fights with wits, is courteous to his officers and arrogant to the Song. Meant to feel unbeatable.</p>', armor=1, hp=16, link=True)
npc('duan', '段游衍 Duan Driftwood', dict(str=65, con=65, siz=70, dex=60, app=70, int=70, pow=50, edu=65), [('i.skill.fighting-sword', 70), ('i.skill.dodge', 60), ('i.skill.spot-hidden', 60), ('i.skill.fast-talk', 60), ('i.skill.persuade', 70), ('i.skill.library-use', 50)],
    [weapon('剑 Sword', '1D8', 'i.skill.fighting-sword', addb=True)], '段', (90, 110, 70, 255),
    '<p>南宋降将，大理段氏，HO1的旧同窗。贪生怕死、圆滑，对两朝皆无忠诚，却向往江湖、钦慕HO1。宴会上会挡在阿术与HO1之间搅乱场面。</p>', '<p>Song turncoat general, HO1\'s old classmate. Cowardly and smooth, loyal to neither dynasty, secretly longs for the jianghu and admires HO1. At the banquet he blocks Ashu and makes chaos so HO1 can escape. Appointed to lead the river assault; will look for a way to disperse Gla\'aki.</p>', disposition=0, link=True)
npc('niu', '牛富 General Niu', dict(str=70, con=70, siz=65, dex=75, app=50, int=60, pow=65, edu=50), [('i.skill.firearms-bow', 85), ('i.skill.fighting-sword', 65), ('i.skill.dodge', 55), ('i.skill.spot-hidden', 60), ('i.skill.intimidate', 60)],
    [weapon('神臂弓 God-Arm Bow', '1D8+2', 'i.skill.firearms-bow', rngd=True, rng=300, ahdb=True, img='icons/weapons/bows/longbow-recurve-leather-brown.webp'), weapon('刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True)], '牛', (60, 60, 60, 255),
    '<p>樊城钤辖，神射手。黝黑精瘦，目光如炬。原文未给数值，此处为主持人估值。城破后拒降，被挑断手筋，囚于监牢。</p>', '<p>Garrison officer and famous bowman. Dark, lean, eyes like torches. The original gives no stats; these are GM estimates. Refused to surrender; tendons cut; in the gaol. His God-Arm Bow (400 paces) is the only bow that reaches mid-river.</p>', disposition=1, link=True)
npc('liu', '刘卿堂 Captain Liu', dict(str=70, con=70, siz=70, dex=70, app=65, int=60, pow=60, edu=70), [('i.skill.fighting-brawl', 75), ('i.skill.fighting-axe', 75), ('i.skill.dodge', 60), ('i.skill.spot-hidden', 55), ('i.skill.library-use', 50)],
    [weapon('斧 Axe', '1D8+2', 'i.skill.fighting-axe', addb=True, img='icons/weapons/axes/axe-battle-black.webp')], '刘', (70, 100, 120, 255),
    '<p>HO3的发小，将门之后。逃脱控制的不死者：无脉搏，毒病无效；不死仆从优先攻击他。</p>', '<p>HO3\'s childhood friend, a general\'s son. An undying man outside Gla\'aki\'s control: no pulse, immune to poison and disease; the Servants target him first. Does not remember the attack on his flotilla.</p>', disposition=1, link=True)
npc('yue', '越南柯 Doctor Yue, the Hollow Physician', dict(str=50, con=55, siz=65, dex=50, app=75, int=75, pow=60, edu=60), [('i.skill.sleight-of-hand', 75), ('i.skill.fast-talk', 70), ('i.skill.spot-hidden', 70), ('i.skill.dodge', 40), ('i.skill.library-use', 50), ('i.skill.charm', 65)],
    [], '越', (160, 120, 50, 255), '<p>“空空郎中”。不会武、不懂医，擅造假药与偷盗，钱散穷人。HO2的师兄。1月3日误触仪式，心怀愧疚。</p>', '<p>The Hollow Physician. Can\'t fight, can\'t heal; sells fake elixirs to the rich, steals, gives to the poor. HO2\'s foster brother. Blundered into the rite on 3 January and is quietly guilty about it.</p>', disposition=1, link=True)
npc('toghan', '兀良哈·脱欢 General Toghan', dict(str=75, con=70, siz=80, dex=60, app=55, int=50, pow=50, edu=45), [('i.skill.fighting-brawl', 75), ('i.skill.fighting-sword', 75), ('i.skill.dodge', 70), ('i.skill.spot-hidden', 60), ('i.skill.ride', 70)],
    [weapon('马刀 Sabre', '1D8+1', 'i.skill.fighting-sword', addb=True)], '脱', (90, 50, 40, 255),
    '阿术的副将，同属兀良哈部。汉话很差，性格暴虐，喜怒无常；杀死HO2父亲的凶手，爱羞辱败将。看不起段游衍，认为他全凭花言巧语得宠。常带几名亲兵光顾城内王五分茶。',
    "Ashu's deputy, of the same Uriankhai clan. Speaks bad Chinese, brutal and moody; he is the man who beheaded HO2's father, and he enjoys humiliating the beaten. Despises Duan, whom he thinks talked his way into the Marshal's favour. Often eats at Wang Wu's Restaurant in town with a few bodyguards.", armor=2, hp=15)
npc('soldier', '蒙古士兵 Mongol soldier', dict(str=60, con=60, siz=70, dex=45, app=45, int=45, pow=50, edu=40), [('i.skill.fighting-brawl', 40), ('i.skill.fighting-sword', 40), ('i.skill.firearms-bow', 45), ('i.skill.dodge', 40), ('i.skill.spot-hidden', 40)],
    [weapon('弯刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True), weapon('弓 Bow', '1D6', 'i.skill.firearms-bow', rngd=True, rng=30, ahdb=True), weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True)], '兵', (110, 70, 50, 255),
    '<p>步兵。身上有武器、身份令牌、钱、指令文书；妙手可窃。护甲2。</p>', '<p>Foot soldier. Carries weapons, an identity token, money and written orders; Sleight of Hand to steal them. Armour 2.</p>', armor=2, hp=12)
npc('rider', '蒙古骑兵 Mongol horseman', dict(str=60, con=60, siz=70, dex=45, app=45, int=45, pow=50, edu=40), [('i.skill.fighting-brawl', 45), ('i.skill.fighting-sword', 45), ('i.skill.firearms-bow', 45), ('i.skill.dodge', 40), ('i.skill.ride', 70)],
    [weapon('弯刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True), weapon('弓 Bow', '1D6', 'i.skill.firearms-bow', rngd=True, rng=30, ahdb=True)], '骑', (90, 50, 40, 255),
    '<p>骑兵。衙署抄家与第四日劫法场事件出现。护甲2。</p>', '<p>Cavalry. Raid the Magistracy; appear again at the execution on day 4. Armour 2.</p>', armor=2, hp=12)
npc('jiang_tower', '姜楼 Tower Jiang', dict(str=65, con=60, siz=65, dex=60, app=60, int=55, pow=55, edu=55), [('i.skill.swim', 70), ('i.skill.fighting-brawl', 65), ('i.skill.dodge', 40), ('i.skill.climb', 55)], [weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True)], '楼', (60, 120, 90, 255), '<p>双胞胎中的兄长，沉稳。水性极好。</p>', '<p>The elder twin, steady. A superb swimmer.</p>', disposition=1, link=True)
npc('jiang_loft', '姜阁 Loft Jiang', dict(str=65, con=60, siz=65, dex=60, app=60, int=55, pow=55, edu=55), [('i.skill.swim', 70), ('i.skill.fighting-brawl', 65), ('i.skill.dodge', 40), ('i.skill.jump', 65)], [weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True)], '阁', (60, 140, 110, 255), '<p>双胞胎中的弟弟，跳脱莽撞。水性极好。</p>', '<p>The younger twin, restless and reckless. A superb swimmer.</p>', disposition=1, link=True)
npc('qu', '曲流 Winding Stream', dict(str=70, con=65, siz=70, dex=65, app=55, int=65, pow=60, edu=65), [('i.skill.fighting-brawl', 70), ('i.skill.dodge', 65), ('i.skill.jump', 60), ('i.skill.first-aid', 60)], [weapon('大刀 Big blade', '1D8', 'i.skill.fighting-brawl', addb=True, img='icons/weapons/swords/sword-broad-red.webp')], '曲', (120, 80, 110, 255),
    '<p>棺材铺老板，前镖师。身材健硕，性格温和，始终照顾调查员。十年前一刀结果了偷腥的丈夫。</p>', '<p>Coffin-maker, former caravan guard. Big and strong, gentle in manner; looks after the PCs throughout. Killed her cheating husband ten years ago.</p>', disposition=1, link=True)
npc('boatman', '船夫王 Boatman Wang', dict(str=50, con=55, siz=60, dex=50, app=40, int=50, pow=45, edu=30), [('i.skill.swim', 60), ('i.skill.dodge', 30), ('i.skill.natural-world', 40), ('驾船|Boat handling', 60)], [], '船', (80, 80, 60, 255),
    '<p>独臂船夫，粗麻布衣，斗笠。痛骂蒙古与朝廷。沉船后独自逃走。</p>', '<p>One-armed boatman in hemp and a straw hat. Curses the Mongols and the court. Abandons the PCs when the boat sinks.</p>', disposition=0)
# ---------------- Campaign NPCs (Days 1–6) ----------------
SAB = lambda: weapon('刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True)
FIST = lambda: weapon('拳脚 Fists', '1D3', 'i.skill.fighting-brawl', addb=True)
npc('fan_yulou', '范玉楼 Commander Fan', dict(str=40, con=45, siz=60, dex=50, app=70, int=75, pow=60, edu=75), [('i.skill.dodge', 40), ('i.skill.listen', 50), ('i.skill.spot-hidden', 50), ('i.skill.library-use', 70), ('i.skill.persuade', 60)], [], '范', (60, 90, 70, 255),
    '<p>范天顺之侄，献城后主事樊城。曾在临安见过HO3一面。会提出刺杀阿术的要求。</p>', '<p>Magistrate Fan\'s nephew; runs the town for the Mongols. Met HO3 once in the capital. Will ask the party to kill Ashu.</p>', disposition=0, link=True)
npc('xu', '许德显 Prefect Xu', dict(str=40, con=45, siz=80, dex=35, app=45, int=60, pow=40, edu=65), [('i.skill.dodge', 25), ('i.skill.persuade', 50), ('i.skill.accounting', 70)], [], '许', (120, 70, 130, 255),
    '<p>樊城通判，贪生怕死。有画舫三艘、小船五艘、火药，能带人进监牢。两封信可胁迫他。</p>', '<p>The prefect; corrupt and cowardly. Three painted barges, five skiffs, gunpowder, a way into the gaol. His two letters are the lever.</p>', disposition=0, link=True)
npc('du', '杜观山 Du Guanshan', dict(str=55, con=55, siz=65, dex=60, app=40, int=55, pow=55, edu=55), [('i.skill.fighting-brawl', 65), ('i.skill.dodge', 60), ('i.skill.listen', 50), ('i.skill.spot-hidden', 50), ('i.skill.jump', 50)], [SAB(), FIST()], '杜', (140, 90, 40, 255),
    '<p>酒肆老板，对樊城了如指掌，提出“江州劫法场”式的救援计划。</p>', '<p>Wineshop owner; knows the town; proposes the Jiangzhou-style rescue.</p>', disposition=1, link=True)
npc('fang', '方未名 Nameless Fang', dict(str=70, con=55, siz=60, dex=70, app=55, int=50, pow=70, edu=40), [('i.skill.fighting-brawl', 75), ('i.skill.dodge', 70), ('i.skill.listen', 50), ('i.skill.spot-hidden', 60), ('i.skill.climb', 70)], [weapon('铜槌 Copper mallet', '1D8', 'i.skill.fighting-brawl', addb=True, img='icons/weapons/hammers/hammer-double-steel.webp'), FIST()], '方', (50, 80, 140, 255),
    '<p>打更少年，力大如牛，心思纯善。背着布裹的神臂弓，不知其为何物。</p>', '<p>The night-watchman boy, strong as an ox, pure of heart. Carries the God-Arm Bow wrapped in cloth and does not know what it is.</p>', disposition=1, link=True)
npc('ling_xuchun', '凌序春 Ling Xuchun', dict(str=65, con=60, siz=65, dex=70, app=65, int=60, pow=50, edu=45), [('i.skill.fighting-sword', 70), ('i.skill.dodge', 70), ('i.skill.spot-hidden', 65), ('i.skill.climb', 60), ('i.skill.swim', 60)], [weapon('双弯刀 Twin sabres', '1D8', 'i.skill.fighting-sword', addb=True, img='icons/weapons/swords/scimitar-worn-blue.webp'), FIST()], '凌', (170, 40, 40, 255),
    '<p>直爽泼辣的少女，为兄长求药。兄长得救后称调查员为恩人。</p>', '<p>Hot-tempered young swordswoman begging medicine for her brother; calls the party "benefactors" once he is cured.</p>', disposition=1, link=True)
npc('ling_daiqiu', '凌代秋 Ling Daiqiu', dict(str=60, con=65, siz=70, dex=60, app=50, int=55, pow=55, edu=45), [('i.skill.dodge', 50), ('i.skill.swim', 75), ('驾船|Boat handling', 70)], [FIST()], '秋', (70, 110, 90, 255),
    '<p>渔民领袖，中了绿腐之术。秋筠死则痊愈，可召渔民参与沉舟绝渡。</p>', '<p>The fishermen\'s leader, under Green Rot; recovers when Autumn dies and can bring the fishermen into the raid.</p>', disposition=1, link=True)
npc('wangwu', '王五条 Wang Wu', dict(str=50, con=60, siz=60, dex=60, app=45, int=65, pow=50, edu=50), [('i.skill.fighting-brawl', 65), ('i.skill.dodge', 55), ('i.skill.persuade', 55)], [weapon('棍 Staff', '1D8', 'i.skill.fighting-brawl', addb=True, img='icons/weapons/staves/staff-simple.webp')], '王', (40, 70, 120, 255),
    '<p>分茶老板，范天顺故交，知其计划；收留陈寻忠。可提供运酒肉的车队。</p>', '<p>Restaurant owner, Magistrate Fan\'s old friend; knows the plan; shelters Chen; lends the delivery carts for the raid.</p>', disposition=1, link=True)
npc('song', '宋择一 Song Zeyi', dict(str=45, con=50, siz=60, dex=50, app=45, int=65, pow=60, edu=65), [('i.skill.throw', 70), ('i.skill.jump', 70), ('i.skill.dodge', 45), ('i.skill.psychology', 55)], [weapon('茶盏 Thrown tea bowl', '1D3', 'i.skill.throw', rngd=True, rng=10, img='icons/containers/kitchenware/bowl-clay-brown.webp')], '宋', (110, 110, 110, 255),
    '<p>茶博士，曾助范天顺搜集祭品，隐瞒此事。给酒肆地址。</p>', '<p>Tea master; helped Magistrate Fan collect the sacrifices and hides it; gives the Wineshop address.</p>', disposition=0, link=True)
npc('autumn', '秋筠 Autumn', dict(str=60, con=65, siz=60, dex=70, app=70, int=65, pow=60, edu=45), [('i.skill.fighting-sword', 70), ('i.skill.dodge', 65), ('i.skill.jump', 65), ('i.skill.disguise', 70)], [SAB(), FIST()], '筠', (200, 200, 200, 255),
    '<p>千面江洋大盗，被范天顺献祭，成为不死仆从。窃走凌家绣花针，给凌代秋施绿腐。</p>', '<p>The outlaw of a thousand faces, sacrificed by Magistrate Fan and now Undying. Stole the Ling needles and cast Green Rot on Ling Daiqiu.</p>', disposition=0, link=True)
npc('chen', '陈寻忠 Chen Xunzhong', dict(str=65, con=60, siz=70, dex=60, app=50, int=55, pow=50, edu=40), [('i.skill.fighting-brawl', 50), ('i.skill.dodge', 45), ('i.skill.fast-talk', 60)], [FIST()], '陈', (60, 100, 90, 255),
    '<p>刘卿堂的执旗手，已成不死仆从，在分茶帮工。给刘卿堂下毒，诱他去寺庙。</p>', '<p>Liu\'s standard-bearer, now Undying, working at the restaurant. Poisons Liu\'s noodles and lures him to the Temple.</p>', disposition=-1, link=True)
npc('monk', '怀德和尚 Huaide, the Pagoda Arhat', dict(str=80, con=80, siz=85, dex=50, app=40, int=50, pow=65, edu=50), [('i.skill.fighting-brawl', 70), ('i.skill.dodge', 50)], [FIST()], '僧', (160, 120, 40, 255),
    '<p>金钟罩铁布衫，好酒。拼酒三胜得金袈裟（护甲2，免疫火焰）。</p>', '<p>Iron Shirt and Golden Bell; a drinker. Three CON wins in a row earn his golden kasaya (armour 2, fire-immune).</p>', armor=2, disposition=1, link=True)
npc('yuying', '范玉莹 Fan Yuying', dict(str=40, con=50, siz=55, dex=55, app=75, int=65, pow=65, edu=60), [('i.skill.dodge', 40), ('i.skill.stealth', 50)], [], '莹', (150, 150, 170, 255),
    '<p>范天顺之女，被阿术留在身边。替调查员挡一刀，暗中递给HO2匕首。</p>', '<p>Magistrate Fan\'s daughter, kept by Ashu. Takes one blow for the party and slips HO2 a dagger.</p>', disposition=1, link=True)
npc('hermit', '山阳道人 The Hermit of Mount Crag', dict(str=50, con=55, siz=60, dex=65, app=45, int=75, pow=80, edu=70), [('i.skill.fighting-sword', 90), ('i.skill.dodge', 70)], [weapon('止水 Stillwater', '1D8', 'i.skill.fighting-sword', addb=True)], '陈', (90, 90, 120, 255),
    '<p>本名陈阳山，HO1之师，独臂。一月十二日被阿术所杀，悬于街口。</p>', '<p>Chen Yangshan, HO1\'s master, one-armed. Killed by Ashu and hung at the Street Crossing on 12 January.</p>', disposition=1, link=True)
npc('scholar', '儒生 Scholar (Zhou Wentong 周文通 and the others)', dict(str=45, con=50, siz=60, dex=50, app=55, int=70, pow=55, edu=75), [('i.skill.library-use', 70), ('i.skill.persuade', 50), ('i.skill.dodge', 30)], [FIST()], '儒', (80, 110, 160, 255),
    '<p>学馆儒生，热血而无用，易被煽动。刺杀日在门外闹事，多有死伤。</p>', '<p>The school\'s scholars: hot-blooded, useless in a fight, easily roused; the diversion on the assassination day, at a cost.</p>', disposition=1)
npc('bookseller', '王见川 Wang Jianchuan, the bookseller', dict(str=70, con=65, siz=75, dex=50, app=60, int=65, pow=55, edu=70), [('i.skill.library-use', 60), ('i.skill.persuade', 55)], [FIST()], '书', (130, 100, 60, 255),
    '<p>旧书摊老板，声如洪钟。摊上有《遗佩情事》《雨师记》。</p>', '<p>The old-book seller with a voice like a bell. His stall has The Lost Pendant and The Rain Master.</p>', disposition=1)
npc('mistress_wang', '王氏 Mistress Wang', dict(str=40, con=50, siz=55, dex=45, app=55, int=60, pow=55, edu=45), [('i.skill.persuade', 45)], [], '氏', (140, 60, 70, 255),
    '<p>李家瓦子老板娘，与五岁女儿同住，收留了秋筠。愿借乌篷船。</p>', '<p>Owner of the Li Family Theatre; lives there with her five-year-old daughter and took Autumn in. Lends the boat.</p>', disposition=1)
npc('physician', '宋人郎中 The Song physician', dict(str=40, con=50, siz=60, dex=50, app=45, int=70, pow=55, edu=70), [('i.skill.medicine', 70), ('i.skill.first-aid', 60), ('i.skill.spot-hidden', 60)], [], '医', (100, 80, 50, 255),
    '<p>阿术的医者。能辨出动过手脚的药，但不揭穿。</p>', '<p>Ashu\'s physician. Can tell when medicine has been tampered with, and says nothing.</p>', disposition=0)
npc('turncoat', '降卒 Song turncoat (ship guard)', dict(str=60, con=55, siz=65, dex=50, app=45, int=45, pow=45, edu=35), [('i.skill.fighting-brawl', 40), ('i.skill.fighting-sword', 40), ('i.skill.dodge', 35)], [SAB()], '卒', (80, 100, 60, 255),
    '<p>随将军降蒙的宋兵，守战船。生命10，无护甲；生命低于一半即逃去报信。</p>', '<p>Song soldiers who followed their general over; guard the ships. HP 10, no armour; below half HP they run to raise the alarm.</p>', hp=10)
npc('glaaki', '格拉基 Gla\'aki', dict(str=400, con=200, siz=600, dex=50, app=0, int=80, pow=300, edu=0), [('i.skill.fighting-brawl', 40)], [weapon('脊刺 Spine thrust', '2+1D5', 'i.skill.fighting-brawl', img='icons/creatures/tentacles/tentacle-thorned-green.webp')], '基', (40, 90, 80, 255),
    '<p>江中之物。每根脊刺护甲4；砍断一根则本体−8。畏火与强光；火焰穿透护甲。直视：理智1D3/1D20。</p>', '<p>The thing in the river. Each spine has armour 4; sever one and the body loses 8. Fears fire and light; fire ignores its armour. Seeing it: SAN 1D3/1D20.</p>', atype='creature', sanloss=('1D3', '1D20'), hp=50)
npc('spine', '格拉基脊刺 Gla\'aki\'s spine', dict(str=200, con=100, siz=450, dex=50, app=0, int=50, pow=300, edu=0), [('i.skill.fighting-brawl', 40)],
    [weapon('脊刺 Spine thrust', '2+1D5', 'i.skill.fighting-brawl', img='icons/creatures/tentacles/tentacle-thorned-green.webp')], '刺', (40, 90, 80, 255),
    '<p>从雾中江面刺出的一根脊刺。护甲4、生命6（与本体共享：每根脊刺削减格拉基8点）。斩断后格拉基一轮内无法再刺。畏火与强光，火焰穿透护甲。直视格拉基本体：理智1D3/1D20。</p>', '<p>A single spine thrusting out of the fog. Armour 4, HP 6 (shared with the body: each severed spine costs Gla\'aki 8 HP). Once cut, no spine attack for a round. Fears fire and bright light; fire ignores its armour. Seeing the body itself: SAN 1D3/1D20. Tonight it only destroys the other boat; the PCs roll SAN 0/1.</p>', atype='creature', armor=4, hp=6, sanloss=('0', '1'))
npc('servant', '不死仆从 Undying Servant', dict(str=50, con=105, siz=65, dex=15, app=30, int=50, pow=50, edu=30), [('i.skill.fighting-brawl', 40), ('i.skill.dodge', 10)],
    [weapon('生前武器 Weapon from life', '1D6', 'i.skill.fighting-brawl', addb=True)], '仆', (70, 110, 60, 255),
    '<p>格拉基之仆。人形时生命首次降至一半即显露不死形态（理智1/1D8；目睹分解1/1D10）。弱点：脊背注入点，点穴命中即死；强光使其绿腐。</p>', '<p>Gla\'aki\'s thrall. In human form until first dropped to half HP, then reveals the undying shape (SAN 1/1D8; watching it dissolve 1/1D10). Weak point: the injection scar on the spine; an Acupoint Strike hit kills it outright. Sunlight brings on Green Rot. Not used in session 0; included for later.</p>', atype='creature', hp=17, sanloss=('1', '1D8'))
# Civilian roles from the Teahouse scene; invented details are labelled in each biography.
TEAHOUSE_NPCS = [
    ('storyteller', '茶楼说书人 Teahouse storyteller', 'icons/svg/book.svg',
     dict(str=35, con=45, siz=50, dex=45, app=55, int=65, pow=50, edu=65),
     [('i.skill.persuade', 55), ('i.skill.listen', 50), ('i.skill.history', 40)],
     '<p>Book: Front Street, The Teahouse (p.20–21). The unnamed storyteller is on the dais, telling how the Liangshan outlaws rescued Song Jiang from the execution ground at Jiangzhou (江州劫法场). Let the tale plant the seed of General Niu\'s rescue; do not give away the coming scene.</p><p>GM convenience: civilian statistics. No personal name or secret allegiance is supplied by the book.</p>'),
    ('tea_server', '茶楼跑堂 Teahouse waiter', 'icons/svg/tankard.svg',
     dict(str=40, con=50, siz=50, dex=60, app=45, int=50, pow=45, edu=40),
     [('i.skill.listen', 50), ('i.skill.dodge', 35), ('i.skill.charm', 40)],
     '<p>Book: Front Street, The Teahouse (p.20–21). The waiter recommends tea master Song 宋择一, whose pictures in tea foam won imperial praise and Magistrate Fan\'s admiration. Customers and the waiter can pass on the rumour of Niu\'s God-Arm Bow. The soldiers kick the waiter down over weak tea.</p><p>GM convenience: civilian statistics; keep this unnamed server out of the fighting once helped to safety.</p>'),
    ('tea_patron_song', '宋人茶客 Song tea patron', 'icons/svg/coins.svg',
     dict(str=40, con=45, siz=50, dex=45, app=45, int=55, pow=45, edu=50),
     [('i.skill.listen', 45), ('i.skill.accounting', 40), ('i.skill.persuade', 35)],
     '<p>GM convenience: an invented cloth seller among the book\'s mixed Song and Mongol customers. War has thinned the trade, but a good tale still earns a cup of tea. Falls silent when soldiers raise their voices; offers a steadying hand to anyone knocked down. Civilian statistics are invented. No extra clues or hidden loyalties.</p>'),
    ('tea_patron_mongol', '蒙古茶客 Mongol tea patron', 'icons/svg/item-bag.svg',
     dict(str=45, con=50, siz=55, dex=45, app=45, int=50, pow=45, edu=40),
     [('i.skill.listen', 40), ('i.skill.ride', 40), ('i.skill.charm', 35)],
     '<p>GM convenience: an invented civilian pack trader among the book\'s mixed Song and Mongol customers, not one of the three soldiers. Sets down a bowl to hear the storyteller\'s next turn; draws back from the brawl rather than joining it. Civilian statistics are invented. No extra clues or hidden loyalties.</p>'),
]
for key, name, image, ch, sk, biography in TEAHOUSE_NPCS:
    ACT[key] = actor(name, 'npc', ch, [skill(c, v, ch) for c, v in sk], [], [], image,
                     bio_en=biography, disposition=0, link=True)
# The Pharmacy branch manager: the book gives no name or statistics, only his manner.
npc('pharmacy_manager', '药铺掌柜 Pharmacy manager', dict(str=40, con=50, siz=65, dex=40, app=45, int=65, pow=45, edu=60),
    [('i.skill.accounting', 65), ('i.skill.appraise', 60), ('i.skill.science-pharmacy', 50), ('i.skill.medicine', 30), ('i.skill.fast-talk', 55), ('i.skill.psychology', 50), ('i.skill.credit-rating', 45)],
    [FIST()], '掌', (60, 70, 110, 255),
    '<p>樊城分号掌柜。对少东家（HO2）百般逢迎：店里的伙计、药材与银钱任她取用。这家分号贪利，价高，伙计看人下菜。从库房翻出两张古方（牵机药、十香软经散）。</p><p>主持人方便：姓名不详，数值为自拟。</p>',
    '<p>Book: Front Street, the pharmacy (p.19). Manager of the Fencewall branch of HO2\'s family house. He fawns on the young master/mistress: HO2 may use the staff, the stock and the cash freely. The branch is grasping: sky-high prices, two clerks who size up a customer\'s purse. He produces the two old recipes from the storeroom (handout "Two old recipes": Bowstring 牵机药 and Ten-Scent Powder 十香软经散).</p><p>GM convenience: the book gives him no name or statistics; these are invented. No secret allegiance.</p>',
    disposition=1)
# ---------------- journals ----------------
# Scene props as tokens (no sheet of interest, bars off) so the GM can show a before/after on the map.
def prop(key, name, tok_file, notes_zh, notes_en):
    a = actor(name, 'npc', dict(str=0, con=10, siz=10, dex=0, app=0, int=0, pow=0, edu=0), [], [], [], f'modules/{MOD}/assets/tokens/{tok_file}.webp', notes_zh, notes_en, disposition=0, link=False)
    a['prototypeToken']['displayBars'] = 0; ACT[key] = a; return a
prop('boat', '渡船 River boat', 'boat', '<p>汉江上的小渔船/渡船，长约八米，可载二十石。场景道具：夜渡场景中有完好与残骸两种标记，攻击发生时切换可见性。</p>',
     '<p>A small Han River fishing boat / ferry, about 8 m, twenty bushels. Scene prop: the Night Crossing scene has an intact and a wrecked token for each boat; toggle visibility when the spine strikes and when the arrows sink the ferry.</p>')
ACT['boat']['prototypeToken']['width'] = 5; ACT['boat']['prototypeToken']['height'] = 1.6
prop('wagon', '药车 Medicine cart', 'wagon', '<p>沈家药行的牛车，载药材北上樊城。场景道具：北门场景中有完好与残骸两种标记，父亲被杀时切换可见性。</p>',
     '<p>One of the Shen pharmacy\'s ox carts carrying medicine to Fencewall. Scene prop: the North Gate scene has an intact and a wrecked token; toggle visibility when the father is killed.</p>')
def dims(tok_file, long_side):
    # token footprint in grid squares from the image aspect, so props keep their proportions
    im = Image.open(f'{ROOT}/assets/tokens/{tok_file}.webp'); r = im.width / im.height
    return (long_side, round(long_side / r, 2)) if r >= 1 else (round(long_side * r, 2), long_side)
WAGON_W, WAGON_H = dims('wagon', 3.2); WAGON_WRECK_W, WAGON_WRECK_H = dims('wagon_wreck', 3.6)
ACT['wagon']['prototypeToken']['width'] = WAGON_W; ACT['wagon']['prototypeToken']['height'] = WAGON_H
_state = random.getstate()
npc('fisherman', '渔民 Fisherman', dict(str=45, con=50, siz=55, dex=50, app=45, int=50, pow=45, edu=35), [('i.skill.swim', 55), ('驾船|Boat handling', 50), ('i.skill.listen', 40), ('i.skill.fighting-brawl', 25)], [FIST()], '渔', (70, 110, 90, 255),
    '<p>主持人便利用：渔民群像标记，数值为方便主持临时拟定，原书未提供。贫困而热情，以茶和咸鱼待客；听从凌代秋。无额外线索。</p>', '<p>GM convenience: a crowd token for the book\'s fishermen. Modest civilian statistics are invented; the book gives none. Poor but hospitable, offering tea and salt fish; follows Ling Daiqiu. No extra clues.</p>', disposition=0)
random.setstate(_state)
# handout page ids were seeded from the names they first shipped with (stray backslashes, bare "Fan's")
IDNAME.update({n: n.replace("(Magistrate Fan's", "(Fan's").replace("'", "\\'") for n, _ in CP.HANDOUTS if "'" in n})
def journal(name, pages, default_perm=0, folder=None):
    return {'_id': rid('journal:' + name), 'name': name, 'folder': folder, 'ownership': {'default': default_perm},
            'pages': [{'_id': rid(f'journal:{name}:{IDNAME.get(pn, pn)}'), 'name': pn, 'type': 'text', 'title': {'show': False, 'level': 1}, 'text': {'format': 1, 'content': html}, 'ownership': {'default': -1}, 'sort': i*100000} for i, (pn, html) in enumerate(pages)], 'flags': {}, 'sort': 0}
FOLD = {k: {'_id': rid('folder:' + k), 'name': n, 'type': t, 'folder': None, 'sorting': 'a', 'sort': 0, 'color': c, 'flags': {}} for k, (n, t, c) in {
    'f_pc': ('调查员 Investigators', 'Actor', '#3b5a8c'), 'f_npc': ('人物 NPCs', 'Actor', '#8c3b3b'), 'f_mon': ('怪物 Creatures', 'Actor', '#3b6b5a'), 'f_prop': ('道具 Props', 'Actor', '#5a5a3b'),
    'f_player': ('玩家手册 Player handouts', 'JournalEntry', '#3b5a8c'), 'f_gm': ('主持人 GM only', 'JournalEntry', '#8c3b3b'), 'f_scene': ('第零次聚会 Session 0', 'Scene', '#5a5a3b')}.items()}
for k in ('pc1', 'pc2', 'pc3'): ACT[k]['folder'] = FOLD['f_pc']['_id']
for k in ('pc1', 'pc2', 'pc3', 'ashu', 'toghan', 'duan', 'niu', 'liu', 'yue', 'boatman', 'qu', 'jiang_tower', 'jiang_loft', 'fan_yulou', 'xu', 'du', 'fang', 'ling_xuchun', 'ling_daiqiu', 'wangwu', 'song', 'autumn', 'chen', 'monk', 'yuying', 'hermit', 'bookseller', 'mistress_wang', 'glaaki', 'pharmacy_manager'): ACT[k]['prototypeToken']['displayName'] = 50  # ALWAYS
for k in ('spine', 'servant', 'glaaki'): ACT[k]['folder'] = FOLD['f_mon']['_id']
for k in ('boat', 'wagon'): ACT[k]['folder'] = FOLD['f_prop']['_id']
for k in ACT:
    if ACT[k]['folder'] is None: ACT[k]['folder'] = FOLD['f_npc']['_id']
JR = [
 journal('玩家入门 · Player Primer', [('故事 The story so far', C.player(C.story_html())), ('人物 Who\'s who', C.player(C.cast_html(False))), ('开场 Opening', C.player(C.opening_html())), ('入门 Primer', C.player(C.primer_html())), ('规则速查 Cheat Sheet', C.player(C.cheat_html())), ('名词对照 Glossary', C.glossary_html())], 2, FOLD['f_player']['_id']),
 journal('HO1 游侠 · The Wanderer（仅HO1玩家）', [('HO1', C.player(C.ho_html(1)))], 0, FOLD['f_player']['_id']),
 journal('HO2 商贾 · The Merchant Heir（仅HO2玩家）', [('HO2', C.player(C.ho_html(2)))], 0, FOLD['f_player']['_id']),
 journal('HO3 命官 · The Commissioner（仅HO3玩家）', [('HO3', C.player(C.ho_html(3)))], 0, FOLD['f_player']['_id']),
 journal('规则卡与文书 · Rules cards & handouts', [('规则卡 Set-piece rules', CP.rules_cards_html())] + [(n, h) for n, h in CP.HANDOUTS], 0, FOLD['f_player']['_id']),
 journal('主持人 · GM: Campaign (Days 1–6)', [('阅读顺序 Reading order & prep', CP.prep_html()), ('沙盒 How the sandbox runs', CP.sandbox_html()), ('前街 Front Street', CP.front_html()), ('后街 Back Street', CP.back_html()), ('街口 Street Crossing', CP.crossing_html()), ('寺庙 Temple', CP.temple_html()), ('衙署 Magistracy quarter', CP.magistracy_html()), ('汉江沿岸 Riverbank', CP.riverbank_html()), ('塔楼 Finale: the Watchtower', CP.finale_html()), ('可选与个人 Optional & personal events', CP.optional_html()), ('结局 Endings', CP.endings_html()), ('人物 Campaign NPCs', CP.npcs_html()), ('人物档案 NPC dossier', CP.dossier_html())], 0, FOLD['f_gm']['_id']),
 journal('主持人 · GM: Session 0 Runbook', [('流程 Runbook', C.runbook_html()), ('加时：第一日 Extended: Day One', C.extended_html()), ('人物速查 NPC reference', C.npc_ref_html()), ('人物 Who\'s who (GM)', C.cast_html(True)), ('故事全貌 The whole story & timeline', C.timeline_html()), ('伤势与治疗 Wounds & Healing', C.healing_html())], 0, FOLD['f_gm']['_id']),
]
# One page per person, so a name anywhere in the GM journals can link straight to who they are.
PEOPLE = journal('主持人 · GM: People 人物卡', [(row[1], CP.dossier_block(row)) for _, rows in CP.DOSSIER for row in rows], 0, FOLD['f_gm']['_id'])
PEOPLE_KEY = {pg['_id']: CP.dossier_key(row[0]) for pg, row in zip(PEOPLE['pages'], [row for _, rows in CP.DOSSIER for row in rows])}
PEOPLE_UUID = {k: f"JournalEntry.{PEOPLE['_id']}.JournalEntryPage.{pid}" for pid, k in PEOPLE_KEY.items()}
JR.append(PEOPLE)
for j_ in JR:
    if j_['folder'] != FOLD['f_gm']['_id']: continue   # players cannot open the GM's People journal
    for pg_ in j_['pages']: pg_['text']['content'] = CP.link_people(pg_['text']['content'], PEOPLE_UUID, skip=PEOPLE_KEY.get(pg_['_id']))
# ---------------- scenes ----------------
# AI-generated maps, 3072x2048. Grid size per scene so that one square ~ 1.5 m on that map.
LEVEL = 'defaultLevel0000'  # Foundry 14 scene level; v12/13 strip the unknown fields and use `background` instead
def level(name, img_src):
    return {'_id': LEVEL, 'name': name, 'background': {'src': img_src}, 'elevation': {'bottom': 0, 'top': None}, 'sort': 0, 'flags': {}}
# gx, gy are canvas squares: Foundry pads the scene by `padding` (10%) rounded up to whole squares, so the map's top-left corner
# is at ceil(0.1*w/G), ceil(0.1*h/G) = (3, 2) squares on the 3072x2048/128 maps and (4, 3) on the 2304x1536/64 river map.
def tok(a, gx, gy, G, tid, hidden=False, name=None, w=1, h=1, texture=None):
    return {'_id': tid, 'name': name or a['prototypeToken']['name'], 'actorId': a['_id'], 'actorLink': a['prototypeToken']['actorLink'], 'texture': {'src': texture or a['prototypeToken']['texture']['src']}, 'x': int(gx*G), 'y': int(gy*G), 'width': w, 'height': h,
            'disposition': a['prototypeToken']['disposition'], 'hidden': hidden, 'level': LEVEL, 'displayName': a['prototypeToken']['displayName'], 'displayBars': a['prototypeToken']['displayBars'], 'bar1': {'attribute': 'attribs.hp'}, 'sight': {'enabled': a['type'] == 'character'}, 'elevation': 0, 'rotation': 0, 'alpha': 1, 'flags': {}}
def scene(name, img, G, tokens, darkness=0.0, notes='', w=3072, h=2048, weather=''):
    # Token IDs are keyed by scene + token name (+ ordinal for repeats), not by position in the list, so adding a token
    # does not reassign the IDs of the others (saved combatants reference tokens by ID).
    seen = {}; toks = []
    for t in tokens:
        tname = t[1].get('name') or t[0][0]['prototypeToken']['name']; tname = IDNAME.get(tname, tname); n = seen[tname] = seen.get(tname, 0) + 1
        toks.append(tok(*t[0], G, rid(f'token:{IDNAME.get(name, name)}:{tname}#{n}'), **t[1]))
    return {'_id': rid('scene:' + IDNAME.get(name, name)), 'name': name, 'folder': FOLD['f_scene']['_id'], 'background': {'src': f'modules/{MOD}/assets/maps/{img}'}, 'levels': [level(name, f'modules/{MOD}/assets/maps/{img}')], 'initialLevel': LEVEL, 'width': w, 'height': h, 'padding': 0.1, 'navigation': True, 'active': False,
            'grid': {'type': 1, 'size': G, 'style': 'solidLines', 'thickness': 1, 'color': '#000000', 'alpha': 0.08, 'distance': 1.5, 'units': 'm'},
            'tokenVision': False, 'fog': {'exploration': False}, 'weather': weather, 'environment': {'darknessLevel': darkness, 'globalLight': {'enabled': True}},
            'tokens': toks, 'walls': [], 'lights': [], 'notes': [], 'drawings': [], 'sounds': [], 'templates': [], 'tiles': [], 'regions': [], 'flags': {}, 'sort': 0, 'initial': None, 'description': notes}
A = ACT
BOAT_WRECK = f'modules/{MOD}/assets/tokens/boat_wreck.webp'
WAGON_WRECK = f'modules/{MOD}/assets/tokens/wagon_wreck.webp'
T = lambda a, x, y, **k: ((a, x, y), k)
SC = [
 # 24 x 16 squares
 scene('1 · 樊城衙署·庆功宴 The Victory Banquet (HO1)', 'banquet.webp', 128,
       [T(A['ashu'], 11, 2.3), T(A['duan'], 13, 2.3), T(A['pc1'], 10, 13.6, name='陆青崖 Lu Bluecliff (disguised)')] + [T(A['soldier'], x, y, name=f'卫兵 Guard {i+1}') for i, (x, y) in enumerate([(4.3, 4.5), (19.2, 4.5), (4.3, 9.5), (19.2, 9.5), (8.5, 13.3), (15.3, 13.3), (2.2, 6.5), (21.5, 12.2)])], 0.15),
 # The convoy is a token of the 'wagon' prop: the intact cart on the road, its wreck hidden on the same spot; swap them at the Slash cue.
 scene('2 · 樊城·北门 The North Gate (HO2)', 'gate.webp', 128,
       [T(A['pc2'], 15.9, 10.2), T(A['toghan'], 14.1, 6.9), T(A['duan'], 15.8, 7.3), T(A['niu'], 14.9, 3.1),
        T(A['wagon'], 15.0 - WAGON_W / 2, 9.6 - WAGON_H / 2, name='药车 The medicine cart', w=WAGON_W, h=WAGON_H),
        T(A['wagon'], 15.0 - WAGON_WRECK_W / 2, 9.6 - WAGON_WRECK_H / 2, name='药车·残骸 The medicine cart, wrecked', hidden=True, w=WAGON_WRECK_W, h=WAGON_WRECK_H, texture=WAGON_WRECK)] + [T(A['soldier'], x, y, name=f'蒙古兵 Mongol soldier {i+1}') for i, (x, y) in enumerate([(12.5, 8.3), (16.9, 8.5), (13.1, 11.1), (16.5, 11.3), (15.1, 12.7)])] + [T(A['soldier'], x, y, name=f'宋兵 Song guard {i+1}') for i, (x, y) in enumerate([(8.5, 3.5), (12.2, 3.5), (17.6, 3.5), (21.4, 3.5)])], 0.0,
       '<p>标记操作：父亲被杀（播放“斩”音效）时显示“药车·残骸”、隐藏“药车”。右键标记→切换可见。</p><p>Token cue: when the father is killed (play the 斩 Slash sound), reveal "The medicine cart, wrecked" and hide "The medicine cart". Right-click a token → toggle visibility.</p>'),
 scene('3 · 樊城衙署 The Magistracy (HO3)', 'magistracy.webp', 128,
       [T(A['pc3'], 2.4, 6.4)] + [T(A['rider'], x, y, name=f'骑兵 Horseman {i+1}') for i, (x, y) in enumerate([(10.5, 13.4), (13.5, 13.4), (9, 9.5), (15, 9.5), (12, 6.5), (21, 10)])], 0.45),
 # 36 x 24 squares on a 2304x1536 map: open water above and to the right, the reed bank and jetty along the bottom. Foundry's fog weather drifts over it.
 # The boats are tokens of the 'boat' prop so the GM can show before/after: reveal the wreck + spine and hide the intact fishing boat when it strikes;
 # reveal "Wang's ferry, sinking" and hide the ferry when the arrows come.
 scene('4 · 汉江夜渡 Night Crossing of the Han River', 'river.webp', 64,
       [T(A['pc1'], 1.4, 20.3), T(A['pc2'], 3.6, 20.8), T(A['pc3'], 7.6, 20.3), T(A['boatman'], 6.2, 18.9),
        T(A['boat'], 7.4, 18.3, name='船夫王的渡船 Wang\'s ferry', w=5, h=1.6),
        T(A['boat'], 11.5, 12.2, name='渡船·沉没 Wang\'s ferry, sinking', hidden=True, w=5.5, h=2.6, texture=BOAT_WRECK),
        T(A['boat'], 17.2, 7.6, name='前方渔船 The fishing boat ahead', w=5, h=1.6),
        T(A['boat'], 16.9, 7.1, name='渔船残骸 The fishing boat, wrecked', hidden=True, w=5.5, h=2.6, texture=BOAT_WRECK),
        T(A['spine'], 19.4, 5.6, hidden=True, w=2, h=2),
        T(A['soldier'], 15.5, 21.6, name='岸上弓手 Archer 1'), T(A['soldier'], 27, 22, name='岸上弓手 Archer 2'),
        T(A['jiang_tower'], 0.6, 22.3, hidden=True), T(A['jiang_loft'], 2.2, 22.7, hidden=True), T(A['qu'], 3.8, 22.3, hidden=True)], 0.4,
       '<p>标记操作：划船时拖动“船夫王的渡船”；脊刺攻击时显示“渔船残骸”与脊刺、隐藏“前方渔船”；中箭沉船时显示“渡船·沉没”、隐藏渡船。右键标记→切换可见。</p>'
       '<p>Token cues: drag Wang\'s ferry out as they row. At the spine attack, reveal "The fishing boat, wrecked" and the spine and hide "The fishing boat ahead". When the arrows sink them, reveal "Wang\'s ferry, sinking" and hide the ferry. Right-click a token → toggle visibility (eye icon).</p>',
       w=2304, h=1536, weather='fog'),
 # 12 x 8 squares: a small shop, bigger squares
 scene('5 · 曲流的棺材铺 The Coffin Shop', 'coffinshop.webp', 256,
       [T(A['pc1'], 5.2, 1.4), T(A['pc2'], 7.3, 1.8), T(A['pc3'], 9.4, 1.4), T(A['qu'], 2.6, 4.6), T(A['jiang_tower'], 4.6, 5.2), T(A['jiang_loft'], 7.2, 5.6), T(A['yue'], 3.4, 3.2, hidden=True), T(A['liu'], 9.2, 2.6, hidden=True)], 0.3,
       '<p>越南柯（十二日晚）与刘卿堂（十三日晨）为隐藏标记，加时用。Doctor Yue (evening of the 12th) and Captain Liu (dawn of the 13th) are hidden tokens for the extended Day One.</p>'),
]
# ---------------- music (Kevin MacLeod, incompetech.com, CC BY 4.0) ----------------
# One track per scene: (title, file, scene number, what it is for). Lightless Dawn is a spare for any Gla'aki moment.
TRACKS = [('Eastern Thought', 'Eastern_Thought.ogg', ('0', '0a', '1'), '标题·庆功宴 Title, idle screen, Banquet'),
          ('River Flute', 'River_Flute.ogg', ('0c', 'R1'), '汉江两岸·渔民棚屋 Regional map, fishermen\'s huts'),
          ('Teller of the Tales', 'Teller_of_the_Tales.ogg', ('2',), '北门 North Gate'),
          ('Asian Drums', 'Asian_Drums.ogg', ('3',), '衙署 Magistracy raid'),
          ('Temple of the Manes', 'Temple_of_the_Manes.ogg', ('4',), '汉江夜渡 Night Crossing'),
          ('Decline', 'Decline.ogg', ('5',), '棺材铺 Coffin Shop'),
          ('Dark Times', 'Dark_Times.ogg', ('6',), '街口 Street Crossing, the Hermit\'s body'),
          ('Overheat', 'Overheat.ogg', ('7',), '樊城城图 Town map, action rounds'),
          ('Guzheng City', 'Guzheng_City.ogg', ('8', '8a'), '茶楼·药铺 Teahouse, Pharmacy'),
          ('Nu Flute', 'Nu_Flute.ogg', ('9',), '李家瓦子 Li Family Theatre'),
          ('Himalayan Atmosphere', 'Himalayan_Atmosphere.ogg', ('10',), '寺庙 Temple at night'),
          ('Ghost Story', 'Ghost_Story.ogg', ('11',), '某处民宅 The Undying family\'s house'),
          ('Night Vigil', 'Night_Vigil.ogg', ('12',), '灵堂 Magistrate Fan\'s mourning hall'),
          ('Drums of the Deep', 'Drums_of_the_Deep.ogg', ('13',), '阿术病榻 Ashu\'s sickroom'),
          ('Land of Phantoms', 'Land_of_Phantoms.ogg', ('14',), '监牢 Gaol'),
          ('Mountain Emperor', 'Mountain_Emperor.ogg', ('15',), '东码头 Warship raid'),
          ('Ripples', 'Ripples.ogg', ('16',), '解佩亭 Ruined Pavilion'),
          ('Clash Defiant', 'Clash_Defiant.ogg', ('17',), '塔楼 Watchtower, the last night'),
          ('Lightless Dawn', 'Lightless_Dawn.ogg', ('R2',), '芦苇荡 · 格拉基 The reeds, Gla\'aki dread')]
PL = {'_id': rid('playlist:session0'), 'name': '公若渡河 · Music', 'description': 'Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0', 'mode': 0, 'playing': False, 'fade': 2000, 'channel': 'music', 'sort': 0, 'seed': 0, 'flags': {}, 'folder': None,
      'sounds': [{'_id': rid('sound:' + f), 'name': f'{t} — {use}', 'path': f'modules/{MOD}/assets/music/{f}', 'channel': 'music', 'playing': False, 'repeat': True, 'volume': 0.5, 'fade': 2000, 'sort': i, 'flags': {}, 'description': f'{t} Kevin MacLeod (incompetech.com) CC BY 4.0'} for i, (t, f, nums, use) in enumerate(TRACKS)]}
# Extended session 0: the Street Crossing at noon on the 12th (1536x1024 map, 24x16 squares).
STREET = scene('6 · 街口 The Street Crossing (Day One, noon)', 'street.webp', 64,
               [T(A['pc1'], 6.4, 12.8), T(A['pc2'], 10.2, 12.4), T(A['pc3'], 14, 12.8)] +
               [T(A['soldier'], x, y, name=f'哨兵 Sentry {i+1}') for i, (x, y) in enumerate([(9.5, 6.3), (14.5, 6.3), (12, 2.3), (16.5, 11.5)])], 0.1,
               '<p>中央长枪上挑着山阳道人的遗体。The body on the spear in the centre is the Hermit of Mount Crag; crowd fills the square at noon.</p>', w=1536, h=1024)
SC.append(STREET)
# ---------------- Campaign scenes (Days 1–6): 1536x1024 maps, 24x16 squares ----------------
TOWN = scene('7 · 樊城城图 Fencewall: the town (action rounds)', 'town.webp', 64, [T(A['pc1'], 20.2, 9.2), T(A['pc2'], 20.9, 9.2), T(A['pc3'], 21.6, 9.2)], 0.0,
             '<p>行动轮用的城图：每天早/中/晚各一轮，把三枚调查员标记拖到要去的地方。前街在下、后街在上、街口居中、衙署一带在左上、汉江沿岸在城外。</p><p>The town map for the action rounds: drag the three investigator tokens to where they go each round. Front Street below, Back Street above, the Street Crossing between, the Magistracy quarter top-left, the riverbank outside the wall.</p><p><b>GM:</b> each place label can be shown or hidden. Run the macro “城图 Town map: places” (Macro Directory; drag it to your hotbar) and tick the places the players know. Five start hidden: the Wineshop, the Lings, the burning house, the widow’s house, the reeds.</p>', w=1536, h=1024)
TOWN['grid']['alpha'] = 0
# Place labels are tiles, not paint: the GM shows or hides each one from the "Town map: places" macro (scripts/update.mjs).
# The map sits 3 squares right and 2 down inside the padded canvas (10% padding rounded up to whole 64 px squares).
import town_labels as TL
from PIL import Image as _Im
for key_, zh_, en_, cx_, cy_, red_, shown_, group_, when_ in TL.PLACES:
    tw_, th_ = _Im.open(f'{ROOT}/assets/maps/town_labels/{key_}.webp').size
    TOWN['tiles'].append({'_id': rid('tile:town:' + key_), 'texture': {'src': f'modules/{MOD}/assets/maps/town_labels/{key_}.webp'}, 'x': 192 + int(cx_ - tw_ / 2), 'y': 128 + int(cy_ - th_ / 2),
                          'width': tw_, 'height': th_, 'hidden': not shown_, 'locked': True, 'level': LEVEL, 'elevation': 0, 'sort': 0, 'rotation': 0, 'alpha': 1,
                          'flags': {MOD: {'place': key_, 'name': f'{en_} {zh_}', 'group': group_, 'when': when_, 'start': bool(shown_)}}})
TEAHOUSE = scene('8 · 茶楼 The Teahouse', 'teahouse.webp', 64,
                 [T(A['pc1'], 10.2, 13.2), T(A['pc2'], 11.6, 13.2), T(A['pc3'], 13, 13.2)] +
                 [T(A['soldier'], x, y, name=f'蒙古兵 Mongol soldier {i+1}') for i, (x, y) in enumerate([(14.2, 7.6), (16.2, 7.0), (15.6, 8.9)])] +
                 [T(A['song'], 20.6, 8.6), T(A['scholar'], 12.4, 8.4, name='周文通 Zhou Wentong'), T(A['duan'], 12, 15.2, hidden=True)] +
                 [T(A['storyteller'], 12, 4), T(A['tea_server'], 17.5, 9.5),
                  T(A['tea_patron_song'], 7, 8), T(A['tea_patron_mongol'], 7, 11)], 0.05,
                 '<p>说书台在上，茶博士宋择一在右侧屏风后。三名蒙古兵闹事；段游衍（隐藏）事后从门口经过。</p><p>Storyteller\'s dais at the top; tea master Song behind the screen on the right. Three Mongol soldiers make trouble; Duan (hidden) rides past the door afterwards.</p>', w=1536, h=1024)
THEATRE = scene('9 · 李家瓦子 The Li Family Theatre', 'theatre.webp', 64,
                [T(A['pc1'], 10.6, 14.4), T(A['pc2'], 12, 14.4), T(A['pc3'], 13.4, 14.4), T(A['mistress_wang'], 14.6, 11.4), T(A['autumn'], 21.6, 12.6, hidden=True), T(A['servant'], 22.5, 3.5, name='秋筠·不死 Autumn, undying form', hidden=True)], 0.1,
                '<p>干涸水池里的乌篷船可借。秋筠藏在右下角的房间，被点破时上屋顶。</p><p>The boat in the dry pool can be borrowed. Autumn lodges in the room bottom-right and takes to the roof when exposed.</p>', w=1536, h=1024)
TEMPLE = scene('10 · 寺庙 The Temple (night)', 'temple.webp', 64,
               [T(A['pc3'], 11.2, 14.2), T(A['liu'], 12.6, 14.2), T(A['pc1'], 9.8, 15.2, hidden=True), T(A['pc2'], 14.2, 15.2, hidden=True)] +
               [T(A['servant'], x, y, name=f'不死仆从 Undying {i+1}', hidden=True) for i, (x, y) in enumerate([(17.4, 5.6), (19.2, 5.2), (20.8, 6.4), (18.6, 7.4)])], 0.7,
               '<p>偏殿在右，门从内锁；伏击的不死仆从（1D4+2）隐藏其中。黑暗中HO3与刘卿堂检定−20，直到后门打开。</p><p>Side hall on the right, locked from inside; the ambushers (1D4+2) are hidden tokens there. In the dark HO3 and Liu roll at −20 until the back door is opened.</p>', w=1536, h=1024)
HOUSE = scene('11 · 某处民宅 The Undying family\'s house (night)', 'house.webp', 64,
              [T(A['pc2'], 9.6, 10.6), T(A['liu'], 8.2, 4.2), T(A['pc1'], 11.4, 15.4, hidden=True), T(A['pc3'], 12.8, 15.4, hidden=True),
               T(A['servant'], 10.6, 7.2, name='少女·不死 The girl, undying', hidden=True), T(A['servant'], 12.6, 7.0, name='死囚·不死 The brother, undying', hidden=True)], 0.7,
              '<p>后院水槽泛绿光；少女与其兄在门廊现出原形。刘卿堂是他们的首要目标。</p><p>The trough in the back yard glows green; the girl and her brother change on the porch. Liu is their first target.</p>', w=1536, h=1024)
PHARMACY = scene('8a · 药铺 The Pharmacy (HO2\'s house)', 'pharmacy.webp', 64,
                 # positions include the padding (map origin at 3, 2 squares)
                 [T(A['pc1'], 13.5, 13), T(A['pc2'], 15, 13), T(A['pc3'], 16.5, 13),
                  T(A['pharmacy_manager'], 17, 8.6), T(A['ling_xuchun'], 12, 7.6)], 0.05,
                 '<p>前街上HO2家的分号：初访时关着门，两个伙计在里面忙。掌柜在柜台后；凌序春在柜台前为药价争吵（「求药」，初访时）。左侧是诊脉桌，左上是库房（两张古方），右侧是药炉与晾药架。</p><p>HO2\'s family branch on Front Street: shut on the first visit, two clerks busy inside. The manager is behind the counter; Ling Xuchun argues over prices in front of it ("A plea for medicine", first visit). Pulse-taking table on the left, storeroom top-left (the two old recipes), stove and drying racks on the right. GM convenience: the shop layout is our own; the book only names who is there.</p>', w=1536, h=1024)
for sc_ in (TOWN, TEAHOUSE, PHARMACY, THEATRE, TEMPLE, HOUSE): SC.append(sc_)
MOURNING = scene('12 · 范天顺灵堂 Magistrate Fan\'s mourning hall', 'mourning.webp', 64,
                 [T(A['pc1'], 9.2, 14.6), T(A['pc2'], 10.6, 14.6), T(A['pc3'], 12, 14.6), T(A['liu'], 13.4, 14.6), T(A['fan_yulou'], 12.0, 12.6, hidden=True)] +
                 [T(A['soldier'], x, y, name=f'范家卫兵 Commander Fan\'s guard {i+1}', hidden=True) for i, (x, y) in enumerate([(2.2, 9.2), (21.6, 9.2), (7.4, 15.4), (16.2, 15.4)])], 0.55,
                 '<p>棺材空的，内侧暗格藏残页。书房在左。发现秘密后范玉楼提灯出现，卫兵（隐藏）围住宅邸。</p><p>The coffin is empty; the torn pages are in the compartment inside. The study is on the left. When the secret is found Commander Fan appears with a lantern and his guards (hidden tokens) close the house.</p>', w=1536, h=1024)
SICKROOM = scene('13 · 牛富宅邸·阿术病榻 Ashu\'s sickroom (the assassination)', 'sickroom.webp', 64,
                 [T(A['ashu'], 3.2, 6.2, w=2, h=2), T(A['pc2'], 6.6, 7.4), T(A['pc1'], 8.4, 9.6, name='陆青崖 Lu Bluecliff (as assistant)'), T(A['pc3'], 10.2, 9.6, name='谢云骧 Xie Cloudmane (as assistant)'), T(A['yue'], 11.8, 11.2), T(A['yuying'], 5.4, 8.0), T(A['physician'], 2.4, 9.4)] +
                 [T(A['soldier'], x, y, name=f'亲卫 Guard {i+1}') for i, (x, y) in enumerate([(13.6, 6.0), (18.4, 8.4), (8.6, 14.2), (15.0, 14.2)])], 0.05,
                 '<p>床边马刀在阿术左手；门边墙上蒙古弓与三支白羽箭。屋内两名亲卫、门外两名。五回合后副将到场。</p><p>The sabre lies by Ashu\'s left hand; the bow and three white arrows hang by the door. Two guards inside, two outside; after five rounds the deputy arrives.</p>', w=1536, h=1024)
GAOL = scene('14 · 监牢 The Gaol', 'gaol.webp', 64,
             [T(A['pc1'], 2.6, 9.4), T(A['pc2'], 3.4, 10.6), T(A['pc3'], 2.6, 11.8), T(A['niu'], 20.8, 10.6, name='牛富（深牢）Niu, in the deep cells')] +
             [T(A['soldier'], x, y, name=f'狱卒 Gaoler {i+1}') for i, (x, y) in enumerate([(3.2, 7.4), (10.4, 8.0), (16.8, 7.6)])] +
             [T(A['ashu'], 17.6, 9.6, hidden=True, w=2, h=2), T(A['fan_yulou'], 16.2, 10.8, hidden=True), T(A['fang'], 1.6, 13.2, hidden=True)], 0.5,
             '<p>右侧铁门后是深牢（牛富）。离开时阿术（隐藏）与范玉楼从深处走出。</p><p>Beyond the iron door on the right are the deep cells (Niu). Ashu (hidden) and Commander Fan come out from the depths as the party leaves.</p>', w=1536, h=1024)
DOCK = scene('15 · 东码头·蒙古战船 The East dock and the warships (the raid)', 'dock.webp', 64,
             [T(A['pc1'], 8.4, 12.0), T(A['pc2'], 9.6, 12.6), T(A['pc3'], 10.8, 12.0), T(A['liu'], 13.6, 11.8), T(A['jiang_tower'], 17.6, 9.0, hidden=True), T(A['jiang_loft'], 18.6, 9.6, hidden=True)] +
             [T(A['turncoat'], x, y, name=f'守船兵 Ship guard {i+1}') for i, (x, y) in enumerate([(7.0, 11.0), (9.4, 10.6), (11.6, 11.2), (6.6, 13.4), (12.8, 13.4), (4.8, 10.6), (15.4, 8.2), (6.4, 4.6)])], 0.7,
             '<p>十七日晚犒赏：岸上1D10+5名士兵（多为宋人降卒）围着篝火吃喝；渔民从酒肉车上溜下水凿船，游侠登船。右侧是渔民棚屋。</p><p>Feast night: 1D10+5 soldiers (mostly Song turncoats) eat round the fire; the fishermen slip off the carts into the water to hole the hulls while the wanderers board. Fishermen\'s huts on the right.</p>', w=1536, h=1024)
for sc_ in (MOURNING, SICKROOM, GAOL, DOCK): SC.append(sc_)
HUTS = scene('R1 · 渔民棚屋 The fishermen\'s huts (East dock)', 'huts.webp', 64,
             [T(A['pc1'], 22.0, 9.3), T(A['pc2'], 23.3, 9.3), T(A['pc3'], 24.6, 9.3),
              T(A['jiang_tower'], 12.0, 11.0), T(A['jiang_loft'], 14.0, 11.0),
              T(A['liu'], 6.2, 4.3, hidden=True), T(A['ling_daiqiu'], 15.0, 6.3, hidden=True)] +
             [T(A['fisherman'], x, y, name=f'渔民 Fisherman {i+1}') for i, (x, y) in enumerate([(10.8, 8.7), (15.0, 11.3), (11.7, 12.1), (17.0, 7.1)])], 0.2,
             '<p>原书第36页：姜楼、姜阁在火旁，渔民以茶和咸鱼待客。调查员从码头小路进入。刘卿堂隐藏于棚屋内，供重现渔民救起并照料他的情景时显示；通常他已随HO3同行。凌代秋起初病倒在前街江边巷内，痊愈后来此才显示。渔民群像标记及数值为主持人便利用，非原书人物数值。</p><p>Book p.36: Jiang Tower and Jiang Loft by the fire; the fishermen offer tea and salt fish. PCs enter along the jetty lane. Liu is hidden inside a hut: reveal to stage his rescue and nursing by the fishermen; normally he already accompanies HO3. Ling Daiqiu starts dying in a lane off Front Street: reveal here only after he is cured and arrives. The fisherman crowd tokens and statistics are GM convenience, not book statistics.</p>', w=1536, h=1024)
SC.append(HUTS)
PAVILION = scene('16 · 解佩亭 The ruined Pavilion (west dock)', 'pavilion.webp', 64,
                 [T(A['pc1'], 8.6, 14.4), T(A['pc2'], 10.0, 14.8), T(A['pc3'], 11.4, 14.4), T(A['liu'], 12.8, 14.8), T(A['spine'], 17.6, 7.0, hidden=True, w=2, h=2)], 0.75,
                 '<p>废墟下是太湖石与刺字囚犯的尸体；底座有「七宝行」印。夜间江边任意处可触发「神女入梦来」（脊刺为隐藏标记）。</p><p>Under the rubble: the Grand Lake Stone and the tattooed prisoners\' bodies; the base bears the Seven Treasures seal. At night anywhere on the bank "The goddess comes in dreams" can fire (the spine is a hidden token).</p>', w=1536, h=1024, weather='fog')
TOWER = scene('17 · 塔楼 The Watchtower (the last night)', 'tower.webp', 64,
              [T(A['pc3'], 11.6, 10.6, name='谢云骧 Xie Cloudmane (on the tower)'), T(A['liu'], 12.6, 10.6, name='刘卿堂 Captain Liu (on the tower)'),
               T(A['pc2'], 11.8, 13.6, name='沈怀珠 Shen Pearl (at the foot)'), T(A['pc1'], 11.8, 6.6, name='陆青崖 Lu Bluecliff (in the boat)'), T(A['boatman'], 12.6, 6.8, name='船夫 The boatman'), T(A['duan'], 10.8, 7.0, hidden=True),
               T(A['spine'], 5.4, 3.2, w=2, h=2), T(A['spine'], 19.4, 3.4, w=2, h=2, name='格拉基脊刺 Gla\'aki\'s spine 2', hidden=True)] +
              [T(A['servant'], x, y, name=f'不死仆从 Undying {i+1}', hidden=True) for i, (x, y) in enumerate([(8.6, 14.8), (14.8, 15.0), (9.4, 12.2), (14.6, 12.0), (12.0, 15.8)])] +
              [T(A['soldier'], x, y, name=f'塔楼守兵 Tower guard {i+1}') for i, (x, y) in enumerate([(10.4, 12.6), (13.4, 12.6)])], 0.8,
              '<p>决战：格拉基画在江心雾中。HO1乘船在江上（拖动小船标记），HO2守塔下（每轮1D3+2不死仆从，隐藏标记逐个显示），HO3与刘卿堂在塔顶。每砍断一根脊刺格拉基−8。</p><p>The finale: Gla\'aki is painted into the fog at mid-river. HO1 is in the boat (drag it), HO2 holds the foot of the tower (reveal 1D3+2 Undying a round), HO3 and Liu are on top. Each severed spine takes 8 off Gla\'aki.</p>', w=1536, h=1024, weather='fog')
for sc_ in (PAVILION, TOWER): SC.append(sc_)
REEDS = scene('R2 · 芦苇荡 The reeds (forcing the crossing)', 'reeds.webp', 64,
              [T(A['boat'], 14.0, 8.6, name='渡船 The ferry', w=3.8, h=1.3),
               T(A['pc1'], 12.7, 7.0, w=0.8, h=0.8), T(A['pc2'], 17.1, 7.0, w=0.8, h=0.8),
               T(A['pc3'], 12.7, 10.3, w=0.8, h=0.8), T(A['boatman'], 17.1, 10.3, name='船夫 The boatman', w=0.8, h=0.8),
               T(A['glaaki'], 19.0, 3.5, name='河伯冯夷 River Lord He Bo', hidden=True, texture=f'modules/{MOD}/assets/tokens/hebo.webp', w=2, h=2),
               T(A['glaaki'], 20.0, 8.2, name='汉水女神 The Lady of the Han', hidden=True, texture=f'modules/{MOD}/assets/tokens/goddess.webp', w=2, h=2),
               T(A['glaaki'], 21.2, 11.8, name='何罗鱼 The Many-Headed Fish', hidden=True, w=3, h=3)] +
              [T(A['spine'], x, y, name=f'脊刺 Spine {i+1}', hidden=True) for i, (x, y) in enumerate([(12.5, 7.8), (18.7, 7.8), (15.6, 10.5)])], 0.6,
              '<p>原书第38–39页：三名调查员与一名未具名船夫强渡。依次显示河伯冯夷、汉水女神、何罗鱼，一次只显示一个梦象；三者均为格拉基的梦中诱饵。河伯与女神标记仅为主持人便利用的梦象美术，并非独立人物。梦境破裂时隐藏梦象、倾覆渡船和失踪的船夫，显示环船脊刺，游泳与战斗一轮后进入下一梦。第三梦攻击何罗鱼后冲上襄阳岸。</p><p>Book pp.38–39: three PCs and one unnamed boatman force the crossing. Reveal the River Lord, the Lady of the Han, then the Many-Headed Fish, one dream image at a time; all three are Gla\'aki\'s lures. He Bo and goddess tokens are GM-convenience art for dream images, not separate people. When a temptation breaks, hide its image, the capsized ferry and missing boatman; reveal the circling spines and swim/fight for one round before the next dream. Attack the fish in the third dream to wash up on the Southbright shore.</p>', w=1536, h=1024, weather='fog')
SC.insert(SC.index(PAVILION) + 1, REEDS)
# Title page for the table TV: the scenario's cover re-lettered in English.
TITLE = scene('0 · 公若渡河 Crossing the Han (title screen)', '../cover.webp', 128, [], w=1536, h=1024,
              notes='<p>开场画面 / Title page. Activate while players sit down; the title track (Eastern Thought) plays.</p>')
TITLE['background']['src'] = TITLE['levels'][0]['background']['src'] = f'modules/{MOD}/assets/cover.webp'; TITLE['grid']['alpha'] = 0; TITLE['padding'] = 0
SC.insert(0, TITLE)
# Idle screen: looping ink-wash pagoda video (assets/intro.webm, our own render) for breaks and waiting.
IDLE = scene('0a · 云中塔 Pagoda in the Clouds (idle screen)', '../cover.webp', 128, [], w=1536, h=1024,
             notes='<p>待机画面 / Idle screen: looping video, no text. Use for breaks or while waiting; the title track (Eastern Thought) plays.</p>')
IDLE['background']['src'] = IDLE['levels'][0]['background']['src'] = f'modules/{MOD}/assets/intro.webm'; IDLE['grid']['alpha'] = 0; IDLE['padding'] = 0
SC.insert(1, IDLE)
# Regional map: the Han River with Fencewall (north bank, Mongol-held) and Southbright (south bank, Song), bilingual labels (assets/map_twin_cities.webp).
TWIN = scene('0c · 汉江两岸 The Han and the twin cities (map)', '../cover.webp', 128, [], w=1536, h=1024,
             notes='<p>地图 / Regional map: Fencewall 樊城 on the north bank, Southbright 襄阳 on the south, the cut pontoon bridge, Ashu\'s camps, the jetty. Show it while reading the Primer or whenever players ask where they are; the title track (Eastern Thought) plays.</p>')
TWIN['background']['src'] = TWIN['levels'][0]['background']['src'] = f'modules/{MOD}/assets/map_twin_cities.webp'; TWIN['grid']['alpha'] = 0; TWIN['padding'] = 0
SC.insert(2, TWIN)
# Music: every scene plays its own track when activated (scene number -> track, from TRACKS).
SOUND = {n: PL['sounds'][i]['_id'] for i, (t, f, nums, use) in enumerate(TRACKS) for n in nums}
for sc_ in SC:
    sc_['playlist'] = PL['_id']; sc_['playlistSound'] = SOUND[sc_['name'].split(' · ')[0]]
# Hotbar macros: one click opens an HO portrait full-screen for the GM and pushes it to every player (the TV).
def portrait_macro(key, img, title):
    src = f'modules/{MOD}/assets/portraits/{img}'
    cmd = (f'const src = "{src}", title = "{title}";\n'
           'const IP = foundry.applications?.apps?.ImagePopout;\n'
           'const ip = IP ? new IP({src, window: {title}, showTitle: true}) : new ImagePopout(src, {title, shareable: true});  // v13+ / v12\n'
           'ip.render(true); ip.shareImage();')
    return {'_id': rid('macro:' + key), 'name': title, 'type': 'script', 'author': None, 'img': f'modules/{MOD}/assets/tokens/{img}', 'scope': 'global', 'command': cmd, 'folder': None, 'sort': 0, 'ownership': {'default': 0}, 'flags': {}}
PLACES_MACRO = {'_id': rid('macro:town-places'), 'name': '城图 Town map: places', 'type': 'script', 'author': None, 'img': 'icons/svg/village.svg', 'scope': 'global',
                'command': 'game.gongruo.places();', 'folder': None, 'sort': 0, 'ownership': {'default': 0}, 'flags': {}}
NOTES_MACRO = {'_id': rid('macro:scene-journal'), 'name': "本场景笔记 Open this scene's journal", 'type': 'script', 'author': None, 'img': 'icons/svg/book.svg', 'scope': 'global',
               'command': 'game.gongruo.sceneJournal();', 'folder': None, 'sort': 0, 'ownership': {'default': 0}, 'flags': {}}
MACROS = [portrait_macro('pc1', 'pc_wanderer.webp', '肖像 陆青崖 Lu Bluecliff · HO1 The Wanderer'),
          portrait_macro('pc2', 'pc_merchant.webp', '肖像 沈怀珠 Shen Pearl · HO2 The Merchant Heir'),
          portrait_macro('pc3', 'pc_official.webp', '肖像 谢云骧 Xie Cloudmane · HO3 The Commissioner')]
SFX_FILES = [('slash', '斩 Slash — the father\'s head (HO2 intro)', '54427377-sword-slash-476148.mp3', False),
             ('arrow', '箭 Arrows — the volley from the bank (Night Crossing)', 'dennish18-arrow-146420.mp3', False),
             ('battle', '战 Battle — sword on sword, loop (fights)', 'freesound_community-sword-against-sword-6341.mp3', True)]
SFX = {'_id': rid('playlist:sfx'), 'name': '音效 Sound effects', 'description': 'Sound effects from pixabay.com (Pixabay Content License)', 'mode': -1, 'playing': False, 'fade': 0, 'channel': 'interface', 'sort': 1, 'seed': 0, 'flags': {}, 'folder': None,
       'sounds': [{'_id': rid('sound:' + k), 'name': n, 'path': f'modules/{MOD}/assets/sfx/{f}', 'channel': 'interface', 'playing': False, 'repeat': rep, 'volume': 1.0, 'fade': 0, 'sort': i, 'flags': {}, 'description': f'{f} — pixabay.com, Pixabay Content License'} for i, (k, n, f, rep) in enumerate(SFX_FILES)]}
# ---------------- adventure + module ----------------
# Scene order: Foundry's default folder sort is by name as text ("14" before "2"), so sort the folder manually in build order,
# and give the navigation bar the same order.
FOLD['f_scene']['sorting'] = 'm'
for i_, sc_ in enumerate(SC): sc_['sort'] = sc_['navOrder'] = (i_ + 1) * 100000
# Each scene points at the GM journal page (and heading) that runs it: scene number -> (journal, page, heading text).
# `journal`/`journalEntryPage` feed Foundry's own "Scene Notes" entry in the scene's right-click menu; the flag adds the heading
# for the "Open this scene's journal" macro (scripts/update.mjs).
RUN_, CAMP_ = '主持人 · GM: Session 0 Runbook', '主持人 · GM: Campaign (Days 1–6)'
SCENE_PAGE = {
    '0': (RUN_, '流程 Runbook', 'Agenda'), '0a': (RUN_, '流程 Runbook', 'Agenda'), '0c': (RUN_, '故事全貌 The whole story & timeline', ''),
    '1': (RUN_, '流程 Runbook', 'Personal intro HO1'), '2': (RUN_, '流程 Runbook', 'Personal intro HO2'), '3': (RUN_, '流程 Runbook', 'Personal intro HO3'),
    '4': (RUN_, '流程 Runbook', 'Shared intro: Night Crossing'), '5': (CAMP_, '前街 Front Street', 'The Coffin Shop by day'),
    '6': (CAMP_, '街口 Street Crossing', '12 January, noon'), '7': (CAMP_, '沙盒 How the sandbox runs', 'Action rounds'),
    '8': (CAMP_, '前街 Front Street', 'The Teahouse'), '8a': (CAMP_, '前街 Front Street', 'The pharmacy'), '9': (CAMP_, '前街 Front Street', 'The Li Family Theatre'), '10': (CAMP_, '寺庙 Temple', 'Night at the temple'),
    '11': (CAMP_, '前街 Front Street', "The Undying family's house"), '12': (CAMP_, '衙署 Magistracy quarter', "Magistrate Fan's residence"),
    '13': (CAMP_, '衙署 Magistracy quarter', "Niu's house"), '14': (CAMP_, '衙署 Magistracy quarter', 'The Gaol'),
    '15': (CAMP_, '汉江沿岸 Riverbank', 'The Mongol warships'), '16': (CAMP_, '汉江沿岸 Riverbank', 'West dock'), '17': (CAMP_, '塔楼 Finale: the Watchtower', 'Preparation'),
    'R1': (CAMP_, '汉江沿岸 Riverbank', "East dock: the fishermen's huts"), 'R2': (CAMP_, '汉江沿岸 Riverbank', 'The reeds: forcing the crossing'),
}
for sc_ in SC:
    jn_, pn_, hd_ = SCENE_PAGE[sc_['name'].split(' · ')[0]]
    j_ = next(j for j in JR if j['name'] == jn_); pg_ = next(p for p in j_['pages'] if p['name'] == pn_)
    assert not hd_ or re.search(r'<h[1-3][^>]*>[^<]*' + re.escape(hd_), pg_['text']['content']), (sc_['name'], hd_)
    sc_['journal'], sc_['journalEntryPage'] = j_['_id'], pg_['_id']
    sc_['flags'][MOD] = {'journal': j_['_id'], 'page': pg_['_id'], 'heading': hd_}
adv = {'_id': rid('adventure:session0'), 'name': '公若渡河 · 第零次聚会 / Session 0: Crossing the Han', 'img': f'modules/{MOD}/assets/cover.webp',
       'caption': '南宋末年武侠 CoC7 · bilingual session-0 kit', 'description': '<p>三位预设调查员、三段个人导入与“夜渡汉水”的场景、主持人流程、双语手册与规则速查。导入后请为每位玩家单独设置对应HO日志的权限。</p><p>Three pre-built investigators, the five session-0 scenes, a GM runbook, bilingual handouts and a cheat sheet. After importing, give each player Observer permission on their own HO journal only.</p><p>Scenario by 江涔 (Dicecho / 魔都). Conversion for private table use only.</p>',
       'actors': list(ACT.values()), 'journal': JR, 'scenes': SC, 'folders': list(FOLD.values()), 'items': [], 'tables': [], 'macros': MACROS + [PLACES_MACRO, NOTES_MACRO], 'playlists': [PL, SFX], 'cards': [], 'combats': [], 'sort': 0, 'flags': {}}
adv['_key'] = f"!adventures!{adv['_id']}"
# Shipped as plain JSON (no LevelDB pack): scripts/update.mjs imports it directly, so `git pull` always delivers the content.
json.dump(adv, open(f'{ROOT}/adventure.json', 'w'), ensure_ascii=False, indent=1)
modj = {'id': MOD, 'title': '公若渡河 Session 0 (CoC7, bilingual)', 'description': 'Session-0 kit for the wuxia Call of Cthulhu scenario 公若渡河 by 江涔: pre-built investigators, scenes, GM runbook and bilingual Chinese/English handouts. For private use at your own table.',
        'version': '0.6.15', 'esmodules': ['scripts/update.mjs'], 'url': 'https://github.com/chunfortam/--foundary', 'compatibility': {'minimum': '12', 'verified': '14'}, 'authors': [{'name': 'Devin for chunfortam'}],
        'relationships': {'systems': [{'id': 'CoC7', 'type': 'system', 'compatibility': {'minimum': '8'}}]},
        'styles': ['styles/gongruo.css']}
json.dump(modj, open(f'{ROOT}/module.json', 'w'), ensure_ascii=False, indent=2)
open(f'{ROOT}/styles/gongruo.css', 'w').write('.journal-page-content p.en{color:inherit;opacity:.85;margin-top:-0.4em;margin-bottom:0.9em}.journal-page-content p.zh{margin-bottom:0.15em}.journal-page-content li em{color:inherit;opacity:.85}.journal-page-content table td{vertical-align:top;font-size:0.92em}a.content-link.npc-link{background:none;border:none;border-bottom:1px dotted currentColor;border-radius:0;padding:0;color:inherit;white-space:normal;word-break:normal}a.content-link.npc-link:hover{text-shadow:none;border-bottom-style:solid}\n')
print('actors', len(ACT), 'journals', len(JR), 'scenes', len(SC), 'tokens', sum(len(s['tokens']) for s in SC))
