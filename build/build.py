# -*- coding: utf-8 -*-
import json, os, glob, random, string, re, shutil, copy, hashlib
from PIL import Image, ImageDraw, ImageFont
import content as C
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
def actor(name, atype, ch, skills, weapons, items, tok, bio_zh='', bio_en='', disposition=0, extra=None, link=True, san=None, luck=50, armor=None, sanloss=None, occupation='', age='', idkey=None, tokname=None):
    random.seed('actor:' + (idkey or name)); hp = hpcalc(ch); mp = ch['pow'] // 5
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
    a = {'_id': rid('actor:' + (idkey or name)), 'name': name, 'type': atype, 'img': portrait(tok), 'system': sys, 'items': its, 'effects': [], 'flags': {}, 'folder': None,
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
npc('niu', '牛富 Niu the Archer', dict(str=70, con=70, siz=65, dex=75, app=50, int=60, pow=65, edu=50), [('i.skill.firearms-bow', 85), ('i.skill.fighting-sword', 65), ('i.skill.dodge', 55), ('i.skill.spot-hidden', 60), ('i.skill.intimidate', 60)],
    [weapon('神臂弓 God-Arm Bow', '1D8+2', 'i.skill.firearms-bow', rngd=True, rng=300, ahdb=True, img='icons/weapons/bows/longbow-recurve-leather-brown.webp'), weapon('刀 Sabre', '1D8', 'i.skill.fighting-sword', addb=True)], '牛', (60, 60, 60, 255),
    '<p>樊城钤辖，神射手。黝黑精瘦，目光如炬。原文未给数值，此处为主持人估值。城破后拒降，被挑断手筋，囚于监牢。</p>', '<p>Garrison officer and famous bowman. Dark, lean, eyes like torches. The original gives no stats; these are GM estimates. Refused to surrender; tendons cut; in the gaol. His God-Arm Bow (400 paces) is the only bow that reaches mid-river.</p>', disposition=1, link=True)
npc('liu', '刘卿堂 Captain Liu', dict(str=70, con=70, siz=70, dex=70, app=65, int=60, pow=60, edu=70), [('i.skill.fighting-brawl', 75), ('i.skill.fighting-axe', 75), ('i.skill.dodge', 60), ('i.skill.spot-hidden', 55), ('i.skill.library-use', 50)],
    [weapon('斧 Axe', '1D8+2', 'i.skill.fighting-axe', addb=True, img='icons/weapons/axes/axe-battle-black.webp')], '刘', (70, 100, 120, 255),
    '<p>HO3的发小，将门之后。逃脱控制的不死者：无脉搏，毒病无效；不死仆从优先攻击他。</p>', '<p>HO3\'s childhood friend, a general\'s son. An undying man outside Gla\'aki\'s control: no pulse, immune to poison and disease; the Servants target him first. Does not remember the attack on his flotilla.</p>', disposition=1, link=True)
npc('yue', '越南柯 Doctor Yue, the Hollow Physician', dict(str=50, con=55, siz=65, dex=50, app=75, int=75, pow=60, edu=60), [('i.skill.sleight-of-hand', 75), ('i.skill.fast-talk', 70), ('i.skill.spot-hidden', 70), ('i.skill.dodge', 40), ('i.skill.library-use', 50), ('i.skill.charm', 65)],
    [], '越', (160, 120, 50, 255), '<p>“空空郎中”。不会武、不懂医，擅造假药与偷盗，钱散穷人。HO2的师兄。1月3日误触仪式，心怀愧疚。</p>', '<p>The Hollow Physician. Can\'t fight, can\'t heal; sells fake elixirs to the rich, steals, gives to the poor. HO2\'s foster brother. Blundered into the rite on 3 January and is quietly guilty about it.</p>', disposition=1, link=True)
npc('toghan', '兀良哈·脱欢 Toghan', dict(str=75, con=70, siz=80, dex=60, app=55, int=50, pow=50, edu=45), [('i.skill.fighting-brawl', 75), ('i.skill.fighting-sword', 75), ('i.skill.dodge', 70), ('i.skill.spot-hidden', 60), ('i.skill.ride', 70)],
    [weapon('马刀 Sabre', '1D8+1', 'i.skill.fighting-sword', addb=True)], '脱', (90, 50, 40, 255),
    '阿术的副将，同属兀良哈部。汉话很差，性格暴虐，喜怒无常；杀死HO2父亲的凶手，爱羞辱败将。看不起段游衍，认为他全凭花言巧语得宠。常带几名亲兵光顾城内王五分茶。',
    "Ashu's deputy, of the same Uriankhai clan. Speaks bad Chinese, brutal and moody; he is the man who beheaded HO2's father, and he enjoys humiliating the beaten. Despises Duan, whom he thinks talked his way into the Marshal's favour. Often eats at Wang Five's tea-house in town with a few bodyguards.", armor=2, hp=15)
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
npc('spine', '格拉基脊刺 Gla\'aki\'s spine', dict(str=200, con=100, siz=450, dex=50, app=0, int=50, pow=300, edu=0), [('i.skill.fighting-brawl', 40)],
    [weapon('脊刺 Spine thrust', '2+1D5', 'i.skill.fighting-brawl', img='icons/creatures/tentacles/tentacle-thorned-green.webp')], '刺', (40, 90, 80, 255),
    '<p>从雾中江面刺出的一根脊刺。护甲4、生命6（与本体共享：每根脊刺削减格拉基8点）。斩断后格拉基一轮内无法再刺。畏火与强光，火焰穿透护甲。直视格拉基本体：理智1D3/1D20。</p>', '<p>A single spine thrusting out of the fog. Armour 4, HP 6 (shared with the body: each severed spine costs Gla\'aki 8 HP). Once cut, no spine attack for a round. Fears fire and bright light; fire ignores its armour. Seeing the body itself: SAN 1D3/1D20. Tonight it only destroys the other boat; the PCs roll SAN 0/1.</p>', atype='creature', armor=4, hp=6, sanloss=('0', '1'))
npc('servant', '不死仆从 Undying Servant', dict(str=50, con=105, siz=65, dex=15, app=30, int=50, pow=50, edu=30), [('i.skill.fighting-brawl', 40), ('i.skill.dodge', 10)],
    [weapon('生前武器 Weapon from life', '1D6', 'i.skill.fighting-brawl', addb=True)], '仆', (70, 110, 60, 255),
    '<p>格拉基之仆。人形时生命首次降至一半即显露不死形态（理智1/1D8；目睹分解1/1D10）。弱点：脊背注入点，点穴命中即死；强光使其绿腐。</p>', '<p>Gla\'aki\'s thrall. In human form until first dropped to half HP, then reveals the undying shape (SAN 1/1D8; watching it dissolve 1/1D10). Weak point: the injection scar on the spine; an Acupoint Strike hit kills it outright. Sunlight brings on the Green Decay. Not used in session 0; included for later.</p>', atype='creature', hp=17, sanloss=('1', '1D8'))
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
def journal(name, pages, default_perm=0, folder=None):
    return {'_id': rid('journal:' + name), 'name': name, 'folder': folder, 'ownership': {'default': default_perm},
            'pages': [{'_id': rid(f'journal:{name}:{pn}'), 'name': pn, 'type': 'text', 'title': {'show': False, 'level': 1}, 'text': {'format': 1, 'content': html}, 'ownership': {'default': -1}, 'sort': i*100000} for i, (pn, html) in enumerate(pages)], 'flags': {}, 'sort': 0}
FOLD = {k: {'_id': rid('folder:' + k), 'name': n, 'type': t, 'folder': None, 'sorting': 'a', 'sort': 0, 'color': c, 'flags': {}} for k, (n, t, c) in {
    'f_pc': ('调查员 Investigators', 'Actor', '#3b5a8c'), 'f_npc': ('人物 NPCs', 'Actor', '#8c3b3b'), 'f_mon': ('怪物 Creatures', 'Actor', '#3b6b5a'), 'f_prop': ('道具 Props', 'Actor', '#5a5a3b'),
    'f_player': ('玩家手册 Player handouts', 'JournalEntry', '#3b5a8c'), 'f_gm': ('主持人 GM only', 'JournalEntry', '#8c3b3b'), 'f_scene': ('第零次聚会 Session 0', 'Scene', '#5a5a3b')}.items()}
for k in ('pc1', 'pc2', 'pc3'): ACT[k]['folder'] = FOLD['f_pc']['_id']
for k in ('pc1', 'pc2', 'pc3', 'ashu', 'toghan', 'duan', 'niu', 'liu', 'yue', 'boatman', 'qu', 'jiang_tower', 'jiang_loft'): ACT[k]['prototypeToken']['displayName'] = 50  # ALWAYS
for k in ('spine', 'servant'): ACT[k]['folder'] = FOLD['f_mon']['_id']
for k in ('boat', 'wagon'): ACT[k]['folder'] = FOLD['f_prop']['_id']
for k in ACT:
    if ACT[k]['folder'] is None: ACT[k]['folder'] = FOLD['f_npc']['_id']
JR = [
 journal('玩家入门 · Player Primer', [('开场 Opening', C.opening_html()), ('入门 Primer', C.primer_html()), ('规则速查 Cheat Sheet', C.cheat_html()), ('名词对照 Glossary', C.glossary_html())], 2, FOLD['f_player']['_id']),
 journal('HO1 游侠 · The Wanderer（仅HO1玩家）', [('HO1', C.ho_html(1))], 0, FOLD['f_player']['_id']),
 journal('HO2 商贾 · The Merchant Heir（仅HO2玩家）', [('HO2', C.ho_html(2))], 0, FOLD['f_player']['_id']),
 journal('HO3 命官 · The Commissioner（仅HO3玩家）', [('HO3', C.ho_html(3))], 0, FOLD['f_player']['_id']),
 journal('主持人 · GM: Session 0 Runbook', [('流程 Runbook', C.runbook_html()), ('加时：第一日 Extended: Day One', C.extended_html()), ('人物速查 NPC reference', C.npc_ref_html()), ('时间线与真相 Timeline & truth', C.timeline_html())], 0, FOLD['f_gm']['_id']),
]
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
        tname = t[1].get('name') or t[0][0]['prototypeToken']['name']; n = seen[tname] = seen.get(tname, 0) + 1
        toks.append(tok(*t[0], G, rid(f'token:{name}:{tname}#{n}'), **t[1]))
    return {'_id': rid('scene:' + name), 'name': name, 'folder': FOLD['f_scene']['_id'], 'background': {'src': f'modules/{MOD}/assets/maps/{img}'}, 'levels': [level(name, f'modules/{MOD}/assets/maps/{img}')], 'initialLevel': LEVEL, 'width': w, 'height': h, 'padding': 0.1, 'navigation': True, 'active': False,
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
TRACKS = [('Eastern Thought', 'Eastern_Thought.ogg', '庆功宴 Banquet'), ('Teller of the Tales', 'Teller_of_the_Tales.ogg', '北门 North Gate'), ('Asian Drums', 'Asian_Drums.ogg', '衙署 Magistracy raid'),
          ('Temple of the Manes', 'Temple_of_the_Manes.ogg', '汉江夜渡 Night Crossing'), ('Lotus', 'Lotus.ogg', '棺材铺 Coffin Shop'), ('Lightless Dawn', 'Lightless_Dawn.ogg', '备用 · 格拉基 Alternate: Gla\'aki dread')]
PL = {'_id': rid('playlist:session0'), 'name': '公若渡河 · Session 0 music', 'description': 'Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0', 'mode': 0, 'playing': False, 'fade': 2000, 'channel': 'music', 'sort': 0, 'seed': 0, 'flags': {}, 'folder': None,
      'sounds': [{'_id': rid('sound:' + f), 'name': f'{t} — {use}', 'path': f'modules/{MOD}/assets/music/{f}', 'channel': 'music', 'playing': False, 'repeat': True, 'volume': 0.5, 'fade': 2000, 'sort': i, 'flags': {}, 'description': f'{t} Kevin MacLeod (incompetech.com) CC BY 4.0'} for i, (t, f, use) in enumerate(TRACKS)]}
for sc, snd in zip(SC, PL['sounds'][:5]):
    sc['playlist'] = PL['_id']; sc['playlistSound'] = snd['_id']
# Extended session 0: the Street Crossing at noon on the 12th (1536x1024 map, 24x16 squares).
STREET = scene('6 · 街口 The Street Crossing (Day One, noon)', 'street.webp', 64,
               [T(A['pc1'], 6.4, 12.8), T(A['pc2'], 10.2, 12.4), T(A['pc3'], 14, 12.8)] +
               [T(A['soldier'], x, y, name=f'哨兵 Sentry {i+1}') for i, (x, y) in enumerate([(9.5, 6.3), (14.5, 6.3), (12, 2.3), (16.5, 11.5)])], 0.1,
               '<p>中央长枪上挑着山阳道人的遗体。The body on the spear in the centre is the Hermit of Mount Crag; crowd fills the square at noon.</p>', w=1536, h=1024)
STREET['playlist'] = PL['_id']; STREET['playlistSound'] = PL['sounds'][1]['_id']
SC.append(STREET)
# Title screen for the table TV: the scenario's cover re-lettered in English, Banquet music.
TITLE = scene('0 · 公若渡河 Crossing the Han (title screen)', '../cover.webp', 128, [], w=1536, h=1024,
              notes='<p>开场画面 / Title screen. Activate while players sit down; the Banquet track plays.</p>')
TITLE['background']['src'] = TITLE['levels'][0]['background']['src'] = f'modules/{MOD}/assets/cover.webp'; TITLE['grid']['alpha'] = 0; TITLE['padding'] = 0; TITLE['playlist'] = PL['_id']; TITLE['playlistSound'] = PL['sounds'][0]['_id']
SC.insert(0, TITLE)
SFX_FILES = [('slash', '斩 Slash — the father\'s head (HO2 intro)', '54427377-sword-slash-476148.mp3', False),
             ('arrow', '箭 Arrows — the volley from the bank (Night Crossing)', 'dennish18-arrow-146420.mp3', False),
             ('battle', '战 Battle — sword on sword, loop (fights)', 'freesound_community-sword-against-sword-6341.mp3', True)]
SFX = {'_id': rid('playlist:sfx'), 'name': '音效 Sound effects', 'description': 'Sound effects from pixabay.com (Pixabay Content License)', 'mode': -1, 'playing': False, 'fade': 0, 'channel': 'interface', 'sort': 1, 'seed': 0, 'flags': {}, 'folder': None,
       'sounds': [{'_id': rid('sound:' + k), 'name': n, 'path': f'modules/{MOD}/assets/sfx/{f}', 'channel': 'interface', 'playing': False, 'repeat': rep, 'volume': 1.0, 'fade': 0, 'sort': i, 'flags': {}, 'description': f'{f} — pixabay.com, Pixabay Content License'} for i, (k, n, f, rep) in enumerate(SFX_FILES)]}
# ---------------- adventure + module ----------------
adv = {'_id': rid('adventure:session0'), 'name': '公若渡河 · 第零次聚会 / Session 0: Crossing the Han', 'img': f'modules/{MOD}/assets/cover.webp',
       'caption': '南宋末年武侠 CoC7 · bilingual session-0 kit', 'description': '<p>三位预设调查员、三段个人导入与“夜渡汉水”的场景、主持人流程、双语手册与规则速查。导入后请为每位玩家单独设置对应HO日志的权限。</p><p>Three pre-built investigators, the five session-0 scenes, a GM runbook, bilingual handouts and a cheat sheet. After importing, give each player Observer permission on their own HO journal only.</p><p>Scenario by 江涔 (Dicecho / 魔都). Conversion for private table use only.</p>',
       'actors': list(ACT.values()), 'journal': JR, 'scenes': SC, 'folders': list(FOLD.values()), 'items': [], 'tables': [], 'macros': [], 'playlists': [PL, SFX], 'cards': [], 'combats': [], 'sort': 0, 'flags': {}}
adv['_key'] = f"!adventures!{adv['_id']}"
# Shipped as plain JSON (no LevelDB pack): scripts/update.mjs imports it directly, so `git pull` always delivers the content.
json.dump(adv, open(f'{ROOT}/adventure.json', 'w'), ensure_ascii=False, indent=1)
modj = {'id': MOD, 'title': '公若渡河 Session 0 (CoC7, bilingual)', 'description': 'Session-0 kit for the wuxia Call of Cthulhu scenario 公若渡河 by 江涔: pre-built investigators, scenes, GM runbook and bilingual Chinese/English handouts. For private use at your own table.',
        'version': '0.5.5', 'esmodules': ['scripts/update.mjs'], 'url': 'https://github.com/chunfortam/--foundary', 'compatibility': {'minimum': '12', 'verified': '14'}, 'authors': [{'name': 'Devin for chunfortam'}],
        'relationships': {'systems': [{'id': 'CoC7', 'type': 'system', 'compatibility': {'minimum': '8'}}]},
        'styles': ['styles/gongruo.css']}
json.dump(modj, open(f'{ROOT}/module.json', 'w'), ensure_ascii=False, indent=2)
open(f'{ROOT}/styles/gongruo.css', 'w').write('.journal-page-content p.en{color:inherit;opacity:.85;margin-top:-0.4em;margin-bottom:0.9em}.journal-page-content p.zh{margin-bottom:0.15em}.journal-page-content li em{color:inherit;opacity:.85}.journal-page-content table td{vertical-align:top;font-size:0.92em}\n')
print('actors', len(ACT), 'journals', len(JR), 'scenes', len(SC), 'tokens', sum(len(s['tokens']) for s in SC))
