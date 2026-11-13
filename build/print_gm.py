# -*- coding: utf-8 -*-
"""GM pack for session 0 (A4, English with Chinese inline): checklist, agenda, scene beats with every roll, NPC card.
Usage: python3 build/print_gm.py -> print/gm-pack.pdf"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import OPENING
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADV = json.load(open(os.path.join(ROOT, 'build/src/session0/adventure.json')))

def sv(sk, ch):
    t = 0
    for v in sk['system']['adjustments'].values():
        if isinstance(v, str):
            e = v.replace('@', '').lower()
            for c in ch: e = e.replace(c, str(ch[c]))
            v = int(eval(e))
        t += int(v or 0)
    return t
def db(s):
    return '-2' if s <= 64 else '-1' if s <= 84 else '0' if s <= 124 else '+1D4' if s <= 164 else '+1D6' if s <= 204 else '+2D6' if s <= 284 else f'+{(s-205)//80+2}D6'

NOTES = {'Marshal Ashu': 'Wounded at the banquet: penalty die on every roll he makes from then on (Rainmaster&#39;s Ink 雨师墨). Not meant to die in session 0.',
         'Duan Driftwood': 'Serves the Mongols, loyal to nobody, likes HO1. Talks his way out of everything.',
         'Niu the Archer': 'Stats are my estimate (none in the book). The God-Arm Bow 神臂弓 shoots 400 paces; it matters in the finale.',
         'Captain Liu': 'HO3&#39;s friend; offstage in session 0 (crossed with 800 men on 3 Jan).',
         'Doctor Yue': 'HO2&#39;s foster brother 越南柯; offstage in session 0, he sent the rescuers and the ginger.',
         'Mongol soldier': 'Leather + felt, armour 2. Patrols of 4–6. Not clever; they shout for help.',
         'Mongol horseman': 'Same but mounted; Ride 70. Only in the Magistracy raid.',
         'Tower Jiang': 'Twin, restless; swims like a fish. Rescuer at the river.',
         'Loft Jiang': 'Twin, steady; the one who asks the smart question about the spine.',
         'Winding Stream': 'Owns the coffin shop; stern, attentive, killed her husband ten years ago (do not tell yet).',
         'Boatman Wang': 'One arm, hates both sides, talks about the Lady of the Han. Abandons the PCs when the arrows fly.',
         "Gla'aki's spine": 'A single spine of something vast under the river. HP is "per spine". Armour 4. SAN 0/1. Do not fight it tonight: it sinks the boat and leaves.',
         'Undying Servant': 'Not in session 0. Listed so you know what the river makes of the drowned. SAN 1/1D8. A hit on the spine scar kills it.'}

def npc_rows():
    rows = []
    for x in ADV['actors']:
        if x['type'] == 'character': continue
        ch = {k: v['value'] for k, v in x['system']['characteristics'].items()}
        hp = x['system']['attribs']['hp']['max']
        arm = (x['system']['attribs'].get('armor') or {}).get('value') or 0
        sks = ', '.join(f"{s['name'].replace('Fighting (', '').replace('Firearms (', '').replace(')', '')} {sv(s, ch)}" for s in x['items'] if s['type'] == 'skill')
        wps = '; '.join(f"{w['name']} {w['system']['range']['normal'].get('damage')}{' + DB' if w['system']['properties'].get('addb') else ''}" for w in x['items'] if w['type'] == 'weapon') or '—'
        key = next(k for k in NOTES if k in x['name'])
        dbv = '&mdash;' if ch['str'] + ch['siz'] > 300 else db(ch['str'] + ch['siz'])
        chs = ' '.join(f"{k.upper()} {v}" for k, v in ch.items() if k not in ('app', 'edu') and v)
        rows.append(f'<tr><td><b>{x["name"]}</b><br><small>{chs}</small></td><td class="c">{hp}</td><td class="c">{arm}</td><td class="c">{dbv}</td><td>{sks}</td><td>{wps}</td><td class="note">{NOTES[key]}</td></tr>')
    return ''.join(rows)

def q(zh, en): return f'<div class="quote"><div class="zh">{zh}</div><div>{en}</div></div>'
def R(x): return f'<span class="roll">{x}</span>'

OPEN = ''.join(f'<p>{p}</p>' for p in OPENING)
BODY = f'''
<section class="opening">
<h1>Opening narrative 开场 <small>read aloud, lights low, title screen on, before the personal intros</small></h1>
{OPEN}
<p class="after">Then round the table: each player gives their character's name and one visible detail. Then: "Ten nights earlier..." and the first intro.</p>
</section>

<section>
<h1>公若渡河 · Session 0 GM Pack <small>Crossing the Han · Call of Cthulhu 7e · for the GM only</small></h1>
<div class="cols">
<div>
<h2>Before the session 开场前</h2>
<ul class="check">
<li>Foundry: quit → GitHub Desktop Discard All → Pull → launch → Yes to re-import. Module v0.4.2 or later.</li>
<li>TV: open the world, activate scene <b>0 · Crossing the Han</b>; the Banquet track should start (click once in the window if the browser blocks audio).</li>
<li>Check each scene once: tokens on the map, grid opacity you like, music changes when you activate it.</li>
<li>Print: 3 character sheets (pp1–3) + 3 secret handouts (pp4–6) of character-sheets.pdf; this pack.</li>
<li>Dice: 2×d10 (percentile) per player, d8, d6, d4, d3 (d6 halved). Pencils, erasers.</li>
<li>Read p1–2, p7–8, p12–16 of the PDF (done). Keep p50–52 open for stats, or use the card on p4 here.</li>
<li>Decide: do the other two players step out during intros (book) or stay and listen (fine)?</li>
</ul>
<h2>Agenda 流程 (≈3 h)</h2>
<table class="agenda">
<tr><td>0:00</td><td>Title screen on. Who are you, what is CoC, the one rule (10 min).</td></tr>
<tr><td>0:10</td><td>Players pick HO1/2/3. Read the three public blurbs; hand out sheets + secrets.</td></tr>
<tr><td>0:20</td><td>Personalise: names, looks, pharmacy name, wound, sword style. Practice roll each.</td></tr>
<tr><td>0:50</td><td>Intro HO1 · Banquet (12 min)</td></tr>
<tr><td>1:05</td><td>Intro HO2 · North Gate (12 min)</td></tr>
<tr><td>1:20</td><td>Intro HO3 · Magistracy (12 min)</td></tr>
<tr><td>1:35</td><td>Break</td></tr>
<tr><td>1:45</td><td>Night Crossing (45 min)</td></tr>
<tr><td>2:30</td><td>Coffin Shop, ginger, stop. Tease the Fencewall map.</td></tr>
</table>
</div>
<div>
<h2>Running the rules 主持要点</h2>
<ul>
<li><b>One rule.</b> d100 ≤ skill. You only name the difficulty: Regular / Hard (½) / Extreme (⅕). Default Regular; Hard when it is wet, dark, guarded.</li>
<li><b>Fail = something happens.</b> Describe the problem, then offer: push (one re-roll, disaster on failure) or spend Luck 1:1. Never both.</li>
<li><b>Bonus/penalty die</b> instead of modifiers: roll two tens dice, keep better/worse. The book's "Spot −20" = one penalty die.</li>
<li><b>Opposed</b> (Stealth vs Spot): both roll, higher success level wins, tie → defender (or higher skill).</li>
<li><b>Combat:</b> DEX order; attacker rolls skill, defender Dodge or Fight Back; damage − armour; half max HP in one hit = Major Wound (CON or fall); 0 HP = dying.</li>
<li><b>SAN:</b> "0/1" = roll SAN; pass lose 0, fail lose 1. Only two SAN rolls tonight.</li>
<li><b>Keep it moving.</b> Intros are 12 minutes: one entrance, one problem, one escape. Say yes, pick a roll, move on.</li>
<li><b>Scenes & music</b> auto-switch when you activate a scene (Scenes tab → right-click → Activate). Move tokens by dragging; players may touch the TV.</li>
</ul>
<h2>Wording 用词</h2>
<p>Southbright 襄阳 · Fencewall 樊城 · the Han River 汉江 · Marshal Ashu 阿术 · Duan Driftwood 段游衍 · Commander Fan 范天顺 (the general, hanged himself) · Magistrate Fan 范玉楼 (surrendered) · Niu the Archer 牛富 · Captain Liu 刘卿堂 · Doctor Yue 越南柯 · the Hermit of Mount Crag 山阳道人 · Stillwater 止水 · Rainmaster's Ink 雨师墨 · Lightness 轻功 (= Climb/Jump) · Acupoint Strike 点穴.</p>
<h2>Dates 日期</h2>
<p>Late 1267: HO2's convoy, HO3's breakout. 3 Jan 1268: Liu crosses with 800. 4 Jan: Fencewall surrenders. 10 Jan: victory banquet, HO1's strike. <b>11 Jan, midnight: Night Crossing.</b> 12–18 Jan: session 1.</p>
</div></div>
<h2>Damage & wounds quick table</h2>
<table class="agenda"><tr><td>Sabre / sword</td><td>1D8 + DB</td><td>Bow</td><td>1D6 (+½DB), 30 m</td><td>Arrow in the fog</td><td>1D3</td></tr>
<tr><td>Fists</td><td>1D3 + DB</td><td>Throwing knife</td><td>1D4 + ½DB</td><td>Cold water</td><td>1D3 (CON fail)</td></tr>
<tr><td>Stillwater 止水</td><td>1D8 + DB, wound never heals</td><td>Acupoint Strike 点穴</td><td>1D3; opposed vs CON: stun 1D3 rounds or ignore armour</td><td>Major Wound</td><td>≥ half max HP in one hit: CON or fall</td></tr></table>
<h2>If a player…</h2>
<ul>
<li><b>wants to fight the whole banquet:</b> let one round happen, then Duan's intervention; archers "would have" shot. HO1 escapes; Ashu lives. Say so plainly if needed: this is a prologue.</li>
<li><b>wants to save HO2's father:</b> no. Narrate it in the past tense; it already happened.</li>
<li><b>refuses to board the boat:</b> the fog thickens, the guard changes, another boat offers; the spine happens anyway.</li>
<li><b>attacks the spine:</b> Armour 4, one spine is HP 6; it withdraws when hurt. Nobody has died from heroism yet tonight.</li>
<li><b>asks who the Lady of the Han is:</b> a river goddess the fishermen pray to. Nothing more tonight.</li>
<li><b>asks about the dark sky at noon:</b> "nobody knows". Write down who asked.</li>
</ul>
</section>

<section class="beats">
<h1>Scene beats 场景节拍 <small>every roll the book asks for, in order</small></h1>
<div class="cols">
<div>
<h2>1 · Banquet 庆功宴 — HO1 alone <small>scene: The Victory Banquet</small></h2>
<p><b>Open:</b> Fencewall fell in three days; the Hermit 山阳道人 did not sleep for three nights. On the fourth morning he lays a sword across the table: worn sheath, blade bright enough to show your face, a dark stain near the guard like water that never dried. "Her name is Stillwater 止水." Then his speech (plum wine, pig's head, Tomb-Sweeping Day), and the warning, said three times:</p>
{q('“剑上这道黑，是雨师墨。刀饮即腐：伤口烂而不死，逢阴雨便发，一辈子好不了。不可轻率出剑；止水只为一个人出鞘。”', '"That black on the blade is Rainmaster’s Ink 雨师墨. What it cuts, rots: the wound will not kill and will not heal, and every rainy day it opens again for the rest of a man’s life. Do not draw her lightly. Stillwater leaves the sheath for one man only."')}
{q('“你年轻，能从千军万马里取一颗头。不为那个糊涂皇帝，为汉水两岸的百姓！”', '"You are young; you can take a head out of the middle of an army. Not for that muddle-headed emperor: for the people on the banks of the Han." If you succeed, bring the head to my grave at Tomb-Sweeping with plum wine, loquat wine, beef, a pig&#39;s head, two chickens and three sesame cakes. If not, wander, and come home when the Central Plains are at peace.')}
<p><b>Getting in:</b> {R('Disguise')} or {R('Luck')} at the gate; {R('Climb')}/{R('Jump')} over the wall. Patrols everywhere, no looting (Ashu's order).</p>
<p><b>The hall:</b> roast meat, bowls the size of a palm, Song dancers. Ashu on the dais: huge, bearded, felt hat, soft armour, a sabre at hand. Duan 段游衍 one seat to his right. Magistrate Fan grovelling.</p>
<p><b>The strike:</b> let the player describe it; no roll needed to reach him, or {R('Stealth')} if they sneak. Ashu twists, the blade takes his shoulder, he kicks the table over and swings: {R('Dodge')} or 1D4, a wound to the bone, max HP −1. <i>Ashu's wound will never heal: penalty die on all his rolls from now on.</i></p>
<p><b>Guards close, bows drawn.</b> One round: fight (Sword 75 vs soldier Dodge 40) or press Ashu again (he Fights Back, Sword 75 with a penalty die). Then Duan steps in:</p>
{q('“谁敢放箭？元帅在此！元帅快走！有我在，这刺客休想伤你一根头发！天哪，元帅受伤了，快送元帅出去！”', '"Who dares shoot? The Marshal is right here! Marshal, go, go! While I stand here this assassin will not touch a hair of you! Heaven, the Marshal is wounded, get him out!"')}
<p><b>Out:</b> HO1 slips away in the chaos ({R('Stealth')} or {R('Climb')} if they want a roll). Hiding since. The bridge is cut, the bank guarded; money finds a boatman. → the reeds at midnight.</p>

<h2>2 · North Gate 北门 — HO2 alone <small>scene: Fencewall, the North Gate</small></h2>
<p><b>Open:</b> late 1267, the medicine convoy, father in front. Soldiers stop you: a Mongol who barely speaks Chinese (Toghan) and a Chinese general (Duan 段游衍) who does the talking.</p>
{q('“这鞑子知道你们家有钱，不剥层皮不会放人。有什么值钱的，现在就献出来……”', '"This Tartar knows your house is rich. He won&#39;t let you go without skinning you. Whatever you have of value, offer it now, as a gift to the Khan and the Marshal..."')}
<p>Whatever HO2 says, father goes forward alone and sends them to count stock. The clerks beg them to run. Then: a mist of blood, a head flung sideways. Carts roll over the stain until it is gone.</p>
<p><b>Run for the gate:</b> {R('DEX')}; fail = 1D3, a wound that never fully heals, max HP −1.</p>
<p><b>The gate under martial law:</b> {R('Credit Rating')} or {R('Persuade')}. Claim court business → Niu the Archer 牛富 comes over (dark, lean, black bow). He tells them Commander Fan is hunting a thief in town, and promises help with anything.</p>
<p><b>Days pass</b> (narrate): gossip of a scarred woman outlaw, a drunk monk, a watchman who is everywhere; the assault, Commander Fan's suicide, surrender, Niu arrested. The house is leaderless. → the reeds.</p>
</div>
<div>
<h2>3 · Magistracy 衙署 — HO3 alone <small>scene: Fencewall Magistracy</small></h2>
<p><b>Open:</b> named Commissioner, Captain Liu 刘卿堂 brings 5,000; ambushed, 800 break into Fencewall. Commander Fan's joyless dinner: Magistrate Fan, Lady Fan, Prefect Xu (fat, shiny), Niu (eyes like torches). Magistrate Fan walks you home, flattering, hinting: a warm winter, the river running strangely high.</p>
<p><b>Then:</b> the assault. Fan orders you and Liu to Southbright at noon; your wound keeps you in bed. Liu crosses with the 800. Next day: uproar, the clear sky goes black without rain, servants scatter, Mongol cavalry ride into the compound seizing people.</p>
<p><b>Escape:</b> {R('Stealth')}, or {R('Luck (Hard)')} with a plausible plan; fail = soldiers who arrest anyone suspicious. Fighting out is allowed (Sword 45 / Bow 75 vs horsemen); a failed fight = another wound.</p>
<p><b>Out:</b> hiding in town; everything north of the river is Mongol. → the reeds.</p>

<h2>4 · Night Crossing 汉江夜渡 — all <small>scene: Night Crossing of the Han River</small></h2>
<p><b>Midnight, 11 Jan 1268.</b> No moon, fog, ten metres of sight, watch-fires on the bank, the guard changing. Reed Marsh east of Fencewall, reeds taller than a man. They arrive one by one: <i>let them meet in character; 10 minutes</i>. The boatman is late.</p>
<p>{R('Spot Hidden')}: unlit boats offshore, other night-crossers. {R('Idea/INT')}: midwinter midnight is not fog weather.</p>
<p><b>Boatman Wang 船夫王:</b> hemp, straw hat, one arm, filthy towel. Hates Mongols and court alike. Volunteers: his arm (army cart); Commander Fan ("would suck the pus from a soldier's wound; the court sent him children; he hanged himself"); the fog (the Lady of the Han pities the drowned); the assassin (the whole town praises the nameless wanderer — watch HO1's face).</p>
<p><b>On the water:</b> dead slow, no lamp. A shape ten metres ahead: {R('Spot Hidden, penalty die')}. {R('Listen')}: splitting planks, screams. {R('Spot')}: the boat rocks, armed figures.</p>
<p><b>The spine:</b> they light a lamp. A twenty-bushel boat run through by a tentacle-like spine, tip soft and curling, hide like iron, barbed; it crushes the hull to splinters in silence. <b>{R('SAN 0/1')}</b>.</p>
<p><b>The bank hears.</b> Archers: {R('Dodge')} or an arrow 1D3. The boat sinks: {R('Swim')}, fail = keep only three named possessions. {R('CON')}, fail = 1D3 from the cold. Wang abandons them.</p>
<p><b>Rescue:</b> two men and a woman swim out and drag them ashore; back lanes to a shop on Front Street. → Coffin Shop.</p>

<h2>5 · Coffin Shop 棺材铺 — all <small>scene: Winding Stream's Coffin Shop</small></h2>
<p>Twins Tower 姜楼 (restless) and Loft Jiang 姜阁 (steady); Winding Stream 曲流, big, stern, attentive. Stove lit. They give: Doctor Yue 越南柯 sent them ("he calculated you'd meet disaster tonight"); nobody will ferry anyone now, you need your own strong boat and a boatman; the Mongols seized every boat, a great family or official may have one hidden; the spine: Winding Stream blames Chu shamans; Loft: <i>"If the Mongols want Southbright they must cross by water. With that thing in the river, can they?"</i></p>
<p><b>Close:</b> Winding Stream hands HO2 an oil-paper packet from Doctor Yue: glossy nut brittle. Taste: raw ginger disguised as candy. <b>Stop.</b> Switch to the title screen. Tease: next time, the Fencewall map and three action rounds a day, 12–18 January.</p>
</div></div>
</section>

<section>
<h1>Day One 加时：第一日 <small>optional extension, 60–90 min: 12 January, from the ginger candy to dawn on the 13th</small></h1>
<div class="cols">
<div>
<h2>Tell the players: action rounds 行动轮</h2>
<p>From tomorrow each day has three rounds: <b>morning, noon, evening</b>. Going to one place and doing one thing there costs a round. Eating, going home to the Coffin Shop and the Wineshop are free. Front Street is full of patrols and wanted posters for HO1 (face drawn vague by Duan 段游衍). HO1 fails {R('Disguise')} → lowest {R('Luck')} in the party decides if a soldier looks twice → {R('DEX')} to get away, round lost.</p>

<h2>Night of the 11th — first Dream-Call 梦引 <small>HO3 only, quietly</small></h2>
<p>A familiar voice calls HO3's name in sleep. {R('POW')}; fail = waves heaving, timbers snapping, people screaming. <b>{R('SAN 1/1D3')}</b>. The others only see them wake badly.</p>

<h2>Morning of the 12th — Coffin Shop by day <small>scene: the Coffin Shop</small></h2>
<p>Millet porridge, flatbread, pickles. Shopfront crammed with funeral goods; finished coffins stand open to dry their lacquer. {R('Spot Hidden')}: hidden compartments in the coffin walls.</p>
<p><b>Winding Stream 曲流 tells:</b> wartime, everyone needs a coffin; she made Commander Fan's 范天顺. Compartments hold the dead's belongings against thieves and rot; Magistrate Fan 范玉楼 asked for one too.</p>
<p><b>Planning:</b> name the four districts only: Front Street (shops, HO2's pharmacy branch, playhouse), Back Street (Merchants' Hall where Duan lives, temple), the Magistracy quarter, the riverbank (docks, reed marsh). Whatever they pick for the morning: "you spend it on that; we pick it up next time." → noon.</p>

<h2>Noon of the 12th — the Street Crossing 街口 <small>scene: the Street Crossing</small></h2>
<p>Junction of Front and Back Street; inn, tea stall; the execution ground. Packed crowd, a strange heavy mood. Today's dead man: white-haired, one arm missing, a spear through the throat hoisting the body into the air. <b>HO1 recognises the Hermit of Mount Crag 山阳道人.</b> His face is calm, as if he expected it. If the master mattered: <b>{R('SAN 1/1D3')}</b>. Let the player sit with it.</p>
{q('“兀良哈为报徒弟一剑之仇，上岘首山抓走年逾七十的山阳道人，也还他一刀。止水不过三尺，阿术一把斩马刀却能将人拦腰砍断。”', '"Ashu went up Mount Crag himself to pay the old man back for his pupil’s cut. Seventy years old. That little sword Stillwater is three feet long; the Marshal’s horse-cutter took him in half at the waist."')}
{q('“阿术要斩不肯投降的宋臣，包括还关在监牢里的牛富。幸亏小范大人投降得快。”', '"The Marshal will execute every Song officer who won’t surrender, Niu the Archer 牛富 in the gaol among them. Thank heaven the young Magistrate gave in fast, or it’d be us."')}
<p><i>GM: Niu dies here at noon on the 15th unless rescued (p29). Next session's set-piece; today only plant the line.</i></p>
</div>
<div>
<h2>Evening of the 12th — Doctor Yue 越南柯 calls <small>scene: the Coffin Shop</small></h2>
<p>A wandering healer is chatting with Winding Stream: HO2's foster brother, the Hollow Physician. He fusses over everyone's health, HO2's most. Play the reunion. He gives:</p>
<p><b>Boats:</b> two unsent letters by Prefect Xu 许德显: one to the Mongol camp offering surrender and his three pleasure-barges and five small boats; one to Governor Lü 吕文焕 in Southbright weeping loyalty. Stolen during a "consultation". Either ruins Xu; together, a lever for his boats.</p>
<p><b>The poison</b> (Rainmaster's Ink 雨师墨): knows little; a local legend may be in the county gazetteer 地方志 (Library, next session). <b>Scar-faced woman:</b> a disaster, or a condemned criminal. <b>Commander Fan:</b> far-sighted, devoted to the people, executed a man for stealing lamp oil. (Said flat.)</p>

<h2>Night of the 12th — second Dream-Call <small>scene: Night Crossing, darkness up; HO3 + Liu</small></h2>
<p>Gla'aki 格拉基 calls HO3 to the bank alone, with a lure of light. Read, then <b>{R('SAN 1/1D3')}</b>:</p>
{q('你站在船头，脚下的水面波涛不宁。雾气遮天蔽日。水下黑色的团状物攀住船身，折断船舷和龙骨，击穿甲板。有什么东西自你脊椎后方穿胸而过。你低下头，伤口正滋滋往外冒着绿色的腐烂液体……', '"You stand at the bow. The water heaves. Fog hides the sky and the far bank. Something black and shapeless comes up under the boat, snaps gunwale and keel, punches through the deck. Then something comes through your spine from behind and out of your chest. You look down. The wound hisses, and what runs out is green and rotten..."')}
<p>{R('POW')}: success = awake at the water's edge; fail = already waist-deep in the Han. Silence, fog, a glow ahead; a few steps and the water is at the chest. The glow dips and strikes from behind: {R('Dodge')} or 1D3.</p>
<p><b>The spine:</b> black, scaled, barbed, same as last night. <b>Captain Liu 刘卿堂</b> appears on the bank, throws HO3 a rusty sword. <b>Spine: HP 10, DEX 50, Fighting 40, dmg 2+1D5, armour 4.</b> Beat it or drive it off. If HO3 is losing, Liu takes the hits; he does not die tonight.</p>
<p>Liu was pulled out by fishermen and knows nothing of what happened to his men; he came out looking for clues. Overjoyed; walks HO3 home; from now on goes wherever HO3 goes. <i>GM only: a red web-shaped mark on his back (he survived a spine on the 3rd). Never volunteer it.</i></p>

<h2>Stop</h2>
<p>Dawn on the 13th, Liu at the Coffin Shop. Title screen. Tease: three rounds a day; Niu at noon on the 15th; Xu's boats; the gazetteer. They hold two leads (letters, compartments) and one ally.</p>
</div></div>
</section>

<section>
<h1>NPC card 人物速查 <small>from the module sheets; Niu's numbers are an estimate</small></h1>
<table class="npc"><tr><th>Who</th><th>HP</th><th>Arm</th><th>DB</th><th>Skills</th><th>Weapons</th><th>Notes</th></tr>{npc_rows()}</table>
</section>
'''

CSS = '''
@page { size: A4; margin: 9mm 10mm; }
body { font-family: "Noto Serif CJK SC", "Noto Serif", serif; font-size: 8.5pt; color: #111; margin: 0; line-height: 1.32; }
section { page-break-after: always; }
h1 { font-size: 15pt; margin: 0 0 6px; border-bottom: 2px solid #000; padding-bottom: 3px; } h1 small { font-size: 9pt; font-weight: normal; color: #555; }
h2 { font-size: 10.5pt; margin: 8px 0 3px; border-bottom: 1px solid #000; } h2 small { font-weight: normal; color: #555; font-size: 8pt; }
.cols { display: flex; gap: 12px; } .cols > div { flex: 1; min-width: 0; }
p { margin: 3px 0; } ul { margin: 2px 0; padding-left: 16px; } li { margin-bottom: 2px; }
ul.check li { list-style: none; margin-left: -14px; } ul.check li:before { content: "☐ "; }
.quote { border-left: 3px solid #999; padding: 2px 8px; margin: 4px 0; background: #f4f4f4; font-size: 8.5pt; }
.quote .zh { color: #333; }
.roll { font-weight: bold; background: #e8e8e8; padding: 0 3px; border-radius: 2px; white-space: nowrap; }
table { border-collapse: collapse; width: 100%; } td, th { border: 1px solid #999; padding: 2px 4px; vertical-align: top; text-align: left; }
.agenda td:first-child { white-space: nowrap; width: 1%; font-weight: bold; }
.npc { font-size: 8pt; } .npc td:first-child { width: 17%; } .npc td.c { text-align: center; white-space: nowrap; } .npc td.note { font-size: 7.5pt; color: #333; } .npc th { background: #eee; }
small { font-size: 7.5pt; color: #444; }
section.beats { font-size: 8.1pt; line-height: 1.27; } section.beats .quote { font-size: 8.1pt; margin: 3px 0; } section.beats h2 { margin: 6px 0 2px; }
.opening p { font-size: 11pt; line-height: 1.5; margin: 8px 0; }
.opening p.after { font-size: 9.5pt; color: #444; border-top: 1px solid #000; padding-top: 6px; margin-top: 16px; }
'''
doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{BODY}</body></html>'
out = os.path.join(ROOT, 'print'); os.makedirs(out, exist_ok=True)
hp = os.path.join(out, 'gm-pack.html'); open(hp, 'w').write(doc)
pdf = os.path.join(out, 'gm-pack.pdf')
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + hp], check=True, capture_output=True)
os.remove(hp); print('wrote', pdf)
