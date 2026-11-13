# -*- coding: utf-8 -*-
"""Printable A4 character sheets (bilingual) for the three pregens + one secret handout page each.
Reads build/src/session0/adventure.json (run build.py first). Renders HTML -> PDF with headless Chrome.
Usage: python3 build/print_sheets.py   -> print/character-sheets.pdf"""
import json, os, re, subprocess, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from content import HO, PC_PUBLIC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADV = json.load(open(os.path.join(ROOT, 'build/src/session0/adventure.json')))
PCS = [a for a in ADV['actors'] if a['type'] == 'character']

CHAR = [('str', 'STR 力量'), ('con', 'CON 体质'), ('siz', 'SIZ 体型'), ('dex', 'DEX 敏捷'),
        ('app', 'APP 外貌'), ('int', 'INT 智力'), ('pow', 'POW 意志'), ('edu', 'EDU 教育')]
ZH = {'Accounting': '会计', 'Acupoint Strike 点穴': '', 'Appraise': '估价', 'Charm': '魅惑', 'Climb': '攀爬（轻功）',
      'Credit Rating': '信誉', 'Disguise': '乔装', 'Dodge': '闪避', 'Fast Talk': '话术', 'Fighting (Brawl)': '格斗（拳脚）',
      'Fighting (Sword)': '剑术', 'Firearms (Bow)': '弓', 'First Aid': '急救', 'History': '历史', 'Intimidate': '恐吓',
      'Jump': '跳跃（轻功）', 'Language (Own)': '母语', 'Law': '法律', 'Library Use': '图书馆使用', 'Listen': '聆听',
      'Medicine': '医学', 'Natural World': '博物', 'Navigate': '导航', 'Persuade': '说服', 'Psychology': '心理学',
      'Ride': '骑术', 'Science (Pharmacy)': '药学', 'Spot Hidden': '侦查', 'Stealth': '潜行', 'Swim': '游泳',
      'Throw': '投掷', 'Track': '追踪', 'Art/Craft (Calligraphy)': '书法'}
SKILLKEY = {'i.skill.fighting-sword': 'Fighting (Sword)', 'i.skill.fighting-brawl': 'Fighting (Brawl)',
            'i.skill.throw': 'Throw', 'i.skill.firearms-bow': 'Firearms (Bow)'}

def strip(s): return re.sub('<[^>]+>', '', s or '').strip()

def skill_value(sk, ch):
    adj = sk['system']['adjustments']
    total = 0
    for k, v in adj.items():
        if isinstance(v, str):
            expr = v.replace('@', '').lower()
            for c in ch: expr = expr.replace(c, str(ch[c]))
            v = int(eval(expr))
        total += int(v or 0)
    return total

def db_build(s):
    if s <= 64: return '-2', -2
    if s <= 84: return '-1', -1
    if s <= 124: return '0', 0
    if s <= 164: return '+1D4', 1
    return '+1D6', 2

def mov(ch):
    n = (ch['str'] >= ch['siz']) + (ch['dex'] >= ch['siz'])
    return 7 + n

def actor_page(a):
    name = a['name']
    m = re.match(r'(.+?) \((HO\d) (.+)\)', name)
    pname, ho, role_en = m.groups()
    role_zh = a['system']['infos']['occupation'].split()[0]
    pub = PC_PUBLIC[int(ho[2])]
    ch = {k: a['system']['characteristics'][k]['value'] for k, _ in CHAR}
    at = a['system']['attribs']
    db, build = db_build(ch['str'] + ch['siz'])
    img = os.path.join(ROOT, a['img'].replace('modules/gongruo-session0/', ''))
    skills = sorted([s for s in a['items'] if s['type'] == 'skill'], key=lambda s: s['name'])
    weapons = [w for w in a['items'] if w['type'] == 'weapon']
    gear = [g for g in a['items'] if g['type'] == 'item']
    bio = {b['title'].split()[0]: strip(b['value']) for b in a['system']['biography']}
    H = f'''<section class="sheet">
<header>
 <img src="file://{img}">
 <div class="title">
  <div class="role">{ho} {role_zh} · {role_en}</div>
  <div class="line"><span class="lbl">姓名 Name</span><span class="fill">{pname}</span></div>
  <div class="line"><span class="lbl">职业 Occupation</span><span class="fill">{a['system']['infos']['occupation']}</span>
   <span class="lbl">年龄 Age</span><span class="fill short">{a['system']['infos']['age']}</span></div>
  <div class="line"><span class="lbl">外貌 Looks</span><span class="fill looks">{pub["looks_en"]}</span></div>
 </div>
 <div class="brand">公若渡河<br><small>Crossing the Han · CoC 7e</small></div>
</header>
<div class="row">
 <table class="chars"><tr><th>属性 Characteristic</th><th>值</th><th>½</th><th>⅕</th></tr>'''
    for k, lbl in CHAR:
        v = ch[k]; H += f'<tr><td>{lbl}</td><td class="v">{v}</td><td>{v//2}</td><td>{v//5}</td></tr>'
    H += f'''</table>
 <table class="derived">
  <tr><th>HP 生命</th><td><span class="big">{at['hp']['max']}</span><div class="track">{"☐"*at['hp']['max']}</div></td></tr>
  <tr><th>MP 魔力</th><td><span class="big">{at['mp']['max']}</span><div class="track">{"☐"*at['mp']['max']}</div></td></tr>
  <tr><th>SAN 理智</th><td><span class="big">{at['san']['value']}</span> <small>now ____ &nbsp; (lose 5+ at once → shaken)</small></td></tr>
  <tr><th>Luck 幸运</th><td><span class="big">{at['lck']['value']}</span> <small>now ____ &nbsp; spend 1:1 to fix a failed skill roll</small></td></tr>
  <tr><th>DB 伤害加值</th><td><span class="big">{db}</span> <small>Build 体格 {build:+d}</small></td></tr>
  <tr><th>MOV 移动</th><td><span class="big">{mov(ch)}</span></td></tr>
 </table>
</div>
<h3>技能 Skills <small>— tick ☐ when the GM says the roll "counts" for improvement; ½ = Hard, ⅕ = Extreme</small></h3>
<div class="skills">'''
    for s in skills:
        v = skill_value(s, ch)
        zh = ZH.get(s['name'], '')
        H += f'<div class="sk"><span class="box">☐</span><span class="nm">{s["name"]} <span class="zh">{zh}</span></span><span class="val">{v}</span><span class="hf">{v//2}</span><span class="hf">{v//5}</span></div>'
    H += '</div><div class="row2"><div><h3>武器 Weapons</h3><table class="weap"><tr><th>武器 Weapon</th><th>技能 Skill</th><th>伤害 Damage</th><th>射程 Range</th></tr>'
    for w in weapons:
        mn = w['system']['skill']['main'].get('name', ''); sk = SKILLKEY.get(mn, mn)
        skv = next((skill_value(s, ch) for s in skills if s['name'] == sk), None)
        if w['name'].startswith('点穴'): sk, skv = 'Acupoint Strike 点穴', next((skill_value(s, ch) for s in skills if s['name'].startswith('Acupoint')), '')
        rn = w['system']['range']['normal']
        dmg = rn['damage'] + (' + DB' if w['system']['properties'].get('addb') else (' + ½DB' if w['system']['properties'].get('ahdb') else ''))
        rng = f"{rn.get('value')} m" if rn.get('value') else '—'
        H += f'<tr><td>{w["name"]}</td><td>{sk} {skv}</td><td>{dmg}</td><td>{rng}</td></tr>'
    H += '</table></div><div><h3>随身 Gear</h3><ul class="gear">'
    for g in gear: H += f'<li><b>{g["name"]}</b> {strip(g["system"].get("description", {}).get("value"))}</li>'
    H += '<li>&nbsp;</li><li>&nbsp;</li></ul></div></div>'
    prompts = {'HO1': ['师门与剑法 — what style did the Hermit of Mount Crag 山阳道人 teach you?', '为何刺杀失败 — why did your strike at Marshal Ashu 阿术 fail? (fear, pity, bad luck…)'],
               'HO2': ['药行名号 — name of your pharmacy house:', '经营理念 — its ethos (medicine before money? officials in your pocket?):'],
               'HO3': ['未愈的伤 — what is your wound and how did you get it?', '出身 — which great family of the capital 临安 are you from?']}[ho]
    H += f'<h3>背景 Background <small>— public; your secret is on the folded page</small></h3><p class="desc"><span class="zh">{pub["looks_zh"]}。</span><br>{pub["en"]}</p>'
    for p in prompts: H += f'<p class="prompt">{p}</p><div class="rule"></div>'
    H += '''<footer>掷 d100 ≤ 技能值即成功；≤½ 困难；≤⅕ 极难；96–100 大失败（技能&lt;50时）。失败可「孤注一掷」推骰一次，再败有后果。
<br><em>Roll d100 ≤ skill: success; ≤ half: Hard; ≤ fifth: Extreme; 96–100 fumble (if skill &lt; 50). A failed roll may be <b>pushed</b> once with a reason; a pushed failure has consequences.</em></footer>
</section>'''
    return H

def secret_page(n):
    d = HO[n]
    s = f'<section class="secret"><div class="warn">仅限 HO{n} 玩家阅读 · For the HO{n} player only — fold and hand over</div>'
    s += f'<h1>{d["title_zh"]}<br><small>{d["title_en"]}</small></h1>'
    s += '<h2>公开信息 · Public</h2>' + d['public']
    s += '<h2>你的秘密 · Your secret</h2>' + d['secret']
    s += '<h2>车卡要求 · Character requirements</h2>' + d['build'] + '</section>'
    return s

CSS = '''
@page { size: A4; margin: 9mm 10mm; }
body { font-family: "Noto Serif CJK SC", "Noto Serif", serif; font-size: 9.2pt; color: #1a1a1a; margin: 0; }
section { page-break-after: always; }
header { display: flex; gap: 10px; border-bottom: 2px solid #000; padding-bottom: 6px; align-items: stretch; }
header img { width: 96px; height: 96px; object-fit: cover; border: 1px solid #444; }
.title { flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
.role { font-size: 14pt; font-weight: bold; }
.line { display: flex; gap: 6px; align-items: baseline; margin-top: 3px; }
.lbl { font-size: 8pt; color: #555; white-space: nowrap; }
.fill { flex: 1; border-bottom: 1px solid #777; font-size: 11pt; padding: 0 4px; min-height: 14pt; }
.fill.short { flex: 0 0 40px; } .fill.looks { font-size: 8.5pt; }
.brand { text-align: right; font-size: 15pt; font-weight: bold; line-height: 1.1; }
.brand small { font-size: 7.5pt; font-weight: normal; color: #555; }
.row { display: flex; gap: 10px; margin-top: 6px; }
table { border-collapse: collapse; }
.chars { flex: 0 0 48%; } .chars th, .chars td { border: 1px solid #888; padding: 2px 5px; text-align: center; }
.chars td:first-child, .chars th:first-child { text-align: left; }
.chars td.v { font-weight: bold; font-size: 11pt; }
.derived { flex: 1; } .derived th { text-align: left; padding: 1px 6px 1px 0; white-space: nowrap; vertical-align: top; font-size: 8.5pt; }
.derived td { padding: 1px 0; vertical-align: top; }
.big { font-size: 13pt; font-weight: bold; } .track { letter-spacing: 1px; font-size: 10pt; line-height: 1; } small { color: #555; font-size: 7.5pt; }
h3 { margin: 7px 0 3px; font-size: 10pt; border-bottom: 1px solid #000; } h3 small { font-weight: normal; }
.skills { column-count: 3; column-gap: 12px; }
.sk { display: flex; gap: 4px; break-inside: avoid; border-bottom: 1px dotted #bbb; padding: 1px 0; align-items: baseline; }
.sk .nm { flex: 1; font-size: 8.5pt; } .sk .zh { color: #555; font-size: 7.5pt; } .sk .val { font-weight: bold; width: 22px; text-align: right; }
.sk .hf { width: 18px; text-align: right; color: #666; font-size: 8pt; }
.row2 { display: flex; gap: 12px; } .row2 > div { flex: 1; }
.weap { width: 100%; } .weap th, .weap td { border: 1px solid #888; padding: 2px 4px; text-align: left; font-size: 8.5pt; }
.gear { margin: 0; padding-left: 16px; } .gear li { border-bottom: 1px dotted #bbb; padding: 2px 0; }
.desc { margin: 2px 0 4px; } .prompt { margin: 5px 0 0; font-size: 8.5pt; color: #333; }
.rule { border-bottom: 1px solid #999; height: 14pt; }
footer { margin-top: 8px; border-top: 1px solid #000; padding-top: 4px; font-size: 8pt; color: #333; }
.secret { font-size: 10.5pt; line-height: 1.45; }
.secret .warn { border: 2px dashed #000; padding: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; }
.secret h1 { font-size: 16pt; margin: 0 0 6px; } .secret h1 small { font-size: 11pt; color: #444; }
.secret h2 { font-size: 11.5pt; border-bottom: 1px solid #000; margin: 12px 0 4px; }
.secret p { margin: 4px 0; } .secret .en { color: #333; margin-bottom: 8px; } .secret li { margin-bottom: 5px; }
'''
pages = ''.join(actor_page(a) for a in PCS) + ''.join(secret_page(n) for n in (1, 2, 3))
doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{pages}</body></html>'
out_dir = os.path.join(ROOT, 'print'); os.makedirs(out_dir, exist_ok=True)
html_path = os.path.join(out_dir, 'character-sheets.html'); open(html_path, 'w').write(doc)
pdf = os.path.join(out_dir, 'character-sheets.pdf')
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={pdf}', 'file://' + html_path], check=True, capture_output=True)
os.remove(html_path)
print('wrote', pdf)
