# -*- coding: utf-8 -*-
# Campaign (Days 1–6) GM journal + player rules cards and handouts for 公若渡河.
# English first, Chinese on names and terms; condensed from the scenario by 江涔 (pp. 16–56).
from content import table

def H(en, zh='', lvl=2): return f'<h{lvl}>{en}' + (f' <span class="zh-tag">{zh}</span>' if zh else '') + f'</h{lvl}>'
def P(t): return f'<p>{t}</p>'
def R(t): return f'<blockquote class="read">{t}</blockquote>'            # read aloud / NPC line
def GM(t): return f'<p class="gmnote">{t}</p>'                             # GM-only mechanics note
def UL(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ROLL(x): return f'<b class="roll">{x}</b>'
def CARD(t): return f'<div class="card">{t}</div>'

# ---------------------------------------------------------------- 0. READING ORDER
def prep_html():
    s = H('Reading order and prep', '阅读顺序与准备', 1)
    s += P('Do not read it all. Prepare by session, and by <b>thread</b> (the gaol · the boats · the river) rather than by place. Everything not listed for the next evening is reference you look up at the table.')
    s += H('Once, before anything (about 40 minutes)', '只读一次')
    s += UL(['Player Primer → <b>The story so far</b>.', 'GM runbook → <b>The whole story & timeline</b>, and the GM <b>Who\'s who</b> (just the red lines).',
             'Campaign → <b>How the sandbox runs</b>: the fixed-events table, <i>What the finale needs</i> and <i>The clue web</i> are the three things to hold in your head.'])
    s += H('Before the first sandbox evening (Day One, 12 January)', '第一个沙盒之夜前')
    s += UL(['Session 0 runbook → <b>Extended: Day One</b>.', 'Campaign → <b>Front Street</b> only (stalls, the pharmacy & Ling Xuchun, the Teahouse, the coffin shop by day, the Wineshop) and <b>Street Crossing: 12 January</b>.',
             'Skim the Front Street people in Who\'s who: Du, Nameless Fang, the Lings, Wang Wu, Song, Autumn, Chen, the monk. Day one is spent on Front Street whatever they choose.'])
    s += H('Before each later evening', '之后每晚')
    s += UL(['At the end of a session ask the players where they mean to go tomorrow; read only those locations (Back Street, Magistracy quarter, Riverbank, Temple are ten minutes each).',
             'Check <i>The clue web</i>: which thread are they on, and what is its next node? Read that.'])
    s += H('Fixed points: read the night before', '固定事件：前一晚读')
    s += table(['When', 'Read'], [
      ('The 14th', 'Front Street → <i>The Wineshop</i> and <i>Planning the rescue</i>.'),
      ('The 15th', 'Street Crossing → <i>15 January: the rescue of Niu</i>, and the rescue <b>rules card</b>.'),
      ('The raid night (17th)', 'Riverbank → <i>The Mongol warships</i>; Back Street → <i>Duan\'s room</i> (Toghan\'s note) if they have not found it.'),
      ('Once they open Fan\'s coffin', 'Magistracy quarter → <i>The assassination plan</i>, <i>Ashu\'s sickroom</i>, <i>The fight</i>, <i>Lockdown</i>.'),
      ('The last night', 'Finale → <i>The Watchtower</i> and its <b>rules card</b>; then <i>Endings</i>.'),
    ])
    s += H('Never pre-read', '不必预读')
    s += UL(['<b>Optional & personal events</b>: pull one when a scene stalls. Doctor Yue is your hint-giver; Duan your rescuer; an Undying ambush your clock.',
             '<b>Handouts</b>: open each when it is found and Show Players.'])
    return s

# ---------------------------------------------------------------- 1. HOW THE SANDBOX RUNS
def sandbox_html():
    s = H('GM: how the sandbox runs', '主持人：自由调查轮', 1)
    s += P('After the ginger "candy" at the coffin shop, the town map comes out and the game becomes a semi-sandbox: <b>12–15 January</b> (four days), the warship raid on the <b>16th/17th</b>, the Mongol crossing planned for the <b>18th</b>. The book estimates about 40 hours in total. Keep the three threads in view: <b>the gaol</b> (Niu 牛富 and his bow), <b>the boats</b> (Prefect Xu 许德显, the fishermen, the Mongol warships) and <b>the thing in the river</b> (Fan\'s rite, the Undying, the Watchtower 塔楼).')
    s += H('Action rounds', '行动轮')
    s += UL([
      'Each day has <b>three rounds</b>: morning, noon, evening. One round = the party (together or split) goes to one place and does one thing there. Nights are for fixed events and dreams.',
      'Free (no round): eating at the restaurant or coffin shop, the hidden <b>wineshop 酒肆</b> once they know it, <b>Autumn\'s 秋筠</b> disguise help once a day, chance meetings on the street (optional events), and anything the book marks "does not cost a round".',
      'The <b>Street Crossing 街口</b> joins Front Street and Back Street; moving between them passes through it (noon on the 12th and 15th it has fixed events).',
      'Mongol patrols are everywhere. <b>HO1 is on the wanted posters</b> (Duan blurred the likeness: describe only an outline). Whenever HO1 is out undisguised: Disguise 乔装, or the party\'s lowest Luck; on a failure HO1 rolls DEX to shake the soldiers and loses that round\'s destination.',
      'Making a poison at the pharmacy (牵机药 / 十香软经散) is one Hard Medicine roll a day.',
      'Rolls in this scenario are never pushed inside set pieces (rescue, assassination, raid, finale).',
    ])
    s += H('The four districts', '四区')
    s += table(['District', 'Places', 'Who you meet'], [
      ('<b>Front Street 前街</b>', 'street stalls & old-book seller · Li Family Theatre 李家瓦子 · Wang Wu\'s Restaurant 王五分茶 · the pharmacy (HO2\'s house) · the Teahouse 茶楼 · the Coffin Shop 棺材铺 · the Undying family\'s house · the hidden Wineshop 酒肆', 'Doctor Yue, Autumn, Wang Wu, Chen the flag-bearer, Toghan at noon, Ling Xuchun, tea master Song, Du, the monk, Nameless Fang'),
      ('<b>Back Street 后街</b>', 'the Guildhall 会馆 (Mongol billet, Duan\'s room) · the burning house · Seven Treasures 七宝行 jeweller', 'Duan, Toghan\'s staff, the jeweller'),
      ('<b>Street Crossing 街口</b>', 'inns, tea stalls, the execution ground', 'crowds; the Hermit\'s body (12th); Niu\'s cage carts (15th)'),
      ('<b>Magistracy quarter 衙署</b>', 'Fan\'s residence & mourning hall · Prefect Xu\'s mansion · Niu\'s house (now Ashu\'s quarters) · the School & Library 官学/藏书阁 · the Gaol 监牢', 'Magistrate Fan, Xu, Ashu, the scholars, prisoners'),
      ('<b>Riverbank 汉江沿岸</b>', 'East dock: fishermen\'s huts, the Mongol warships · West dock: the ruined Pavilion 解佩亭 · the Watchtower 塔楼 · the reeds · the Temple 寺庙 by the wall', 'fishermen, Ling Daiqiu, dreamers at night, the Undying'),
    ])
    s += H('Fixed events, day by day', '固定事件')
    s += table(['When', 'Event', 'Page'], [
      ('11 Jan night', 'HO3\'s first Dream-Call (POW; SAN 1/1D3).', 'Optional & personal'),
      ('12 Jan noon', 'Street Crossing: the Hermit of Mount Crag 山阳道人 hangs on a spear. SAN 1/1D3 for HO1.', 'Street Crossing'),
      ('12 Jan', 'Wang Wu\'s Restaurant is shut (the watchman\'s brawl). The pharmacy: Ling Xuchun 凌序春 comes for medicine on the party\'s first visit.', 'Front Street'),
      ('12 Jan evening', 'Doctor Yue 越南柯 at the coffin shop with Xu\'s letters.', 'Front Street'),
      ('12 Jan night', 'HO3\'s second Dream-Call: the riverbank, the spine, Captain Liu 刘卿堂 joins.', 'Optional & personal'),
      ('From 13 Jan', 'Liu travels with HO3. The night events can fire: the Temple ambush (after Chen\'s invitation), the Undying house raid, the Rashomon alley meeting.', 'Temple / Front Street / Optional'),
      ('15 Jan noon', 'General Niu is brought to the Street Crossing to be beheaded: the rescue.', 'Street Crossing'),
      ('16 Jan', 'If Niu was rescued: he hands over the God-Arm Bow 神臂弓 through Nameless Fang 方未名.', 'Street Crossing'),
      ('17 Jan evening', 'Ashu\'s banquet for the army before the crossing; the warships are lightly held: the raid "沉舟绝渡".', 'Riverbank'),
      ('Any day after the plan', 'The assassination at Ashu\'s sickroom → the city locks down → the Watchtower finale that night.', 'Magistracy quarter / Finale'),
      ('18 Jan', 'Planned Mongol river assault on Southbright (never happens if Gla\'aki is still in the river).', '—'),
    ])
    s += H('Money and belongings (house rule)', '钱与随身物品')
    s += P('The book has no currency, prices or equipment lists; its only wealth number is <b>Credit Rating 信誉</b> (HO1 20, HO2 60, HO3 75). This is a house rule, not the book.')
    s += UL([
      '<b>Don\'t track coins.</b> Use Credit Rating.',
      '<b>Small things</b> (food, a rusty sword from the weapons stall, a small bribe such as Prefect Xu\'s servant): free for HO2 and HO3; a Credit Rating roll for HO1.',
      '<b>Big things</b> (buying Xu\'s household, calming the Mongol soldiers at the Teahouse with cash, hiring help): a Credit Rating roll, or send HO2 to the <b>Pharmacy 药铺</b>, where she may use the staff, the herbs and the money freely.',
      '<b>After the boat sinks:</b> on a failed Swim roll a player keeps three named things. Weapons count, and so does everything under Gear on the sheet. A purse that was not named is in the river, and that investigator cannot pay for anything until the Pharmacy gives them money. That makes the Pharmacy worth a visit on the 12th.',
      '<b>Money alone does not hire a boatman.</b> The book says so: "gold and goods may not move people now." Do not allow a Credit Rating roll for it.',
      '<b>Seven Treasures 七宝行</b> sells information for a stone-gambling Luck roll, as in the book; no stake is needed.',
    ])
    s += H('What the finale needs', '决战前置')
    s += UL([
      '<b>A boat and a boatman</b> who will row into the fog: Wang Wu\'s or the theatre\'s 乌篷船 boat; the fishermen (only if Ling Daiqiu 凌代秋 is cured) or the Jiang twins; or Prefect Xu\'s painted barges.',
      '<b>A light signal</b> from the boat: gunpowder from Xu or Magistrate Fan (Luck roll in the wet fog), or the Fire-Cloak spell from the Hermit\'s pages.',
      '<b>A bow that reaches mid-river</b>: only Niu\'s God-Arm Bow (400 paces). Mongol bows reach 300.',
      '<b>The Ling needles 凌家绣花针</b> for HO2\'s Acupoint Strike (+10%): recovered by killing Autumn.',
      '<b>Knowing the weakness</b>: a thin point driven into the healed wound on the spine kills an Undying outright (the Undying house, the torn pages, the physician\'s notes).',
    ])
    s += H('The clue web', '线索网')
    s += UL([
      'Doctor Yue → Xu\'s two letters → Xu\'s boats, gunpowder, gaol access.',
      'The Teahouse → tea master Song → the Wineshop address → Du, the monk, Nameless Fang → the rescue plan.',
      'The pharmacy → Ling Xuchun → Ling Daiqiu\'s poisoning → Autumn at the Li Theatre → the needles; the Library → Rainmaster\'s Ink vs the green mould (two different things).',
      'The Gaol or the burning house → the Undying family\'s house → the spine weakness → Nameless Fang on the wall.',
      'The Wang Wu restaurant → Chen 陈寻忠 → the Temple ambush → Liu\'s truth; Wang Wu himself → Fan\'s plan → the warship raid.',
      'Fan\'s study and coffin → the Many-Headed Fish 何罗鱼 and the pages → Magistrate Fan\'s assassination request.',
      'Seven Treasures jeweller → the Grand Lake Stone 太湖石 → the Pavilion ruins.',
      'Duan\'s room → Toghan\'s note (the banquet date) and the defence map (the Watchtower\'s view) → the raid and the finale.',
    ])
    return s

# ---------------------------------------------------------------- 2. FRONT STREET
def front_html():
    s = H('Front Street', '前街', 1)
    s += P('The commercial street, at a third of its old bustle. Mongol patrols pass constantly. Wanted posters for HO1 on the walls (blurred).')
    s += H('The street stalls and the old-book seller', '沿街浮屋 · 旧书摊')
    s += P('Stalls against the house-fronts: snacks, curios, household goods; worth a rummage. The book stall is run by <b>Wang Jianchuan 王见川</b>: thirty, heavy-browed, full-faced, built like a porter but dressed as a scholar (square cap, washed-out robe, feather fan), a voice like a bell. Magistrate Fan 范玉楼 and the school\'s scholars sometimes browse here and will talk (see Optional: "A chance meeting over books").')
    s += P('On the stall: popular novels, poetry, local tales of the strange. Two are useful (handouts "The Lost Pendant" and "The Rain Master"): the romance of Zheng Jiaofu 郑交甫 and the goddess of the Han, and the legend of Red Pine the Rain Master 赤松子 (the woodcutter whose axe-handle rotted while he watched one game of chess).')
    s += H('The Li Family Theatre', '李家瓦子')
    s += P('Fencewall\'s famous pleasure-house, now dead: a tall painted gate-tower outside, a square courtyard, the red doors hacked by axes and hooves. In the dry pool of the courtyard lies a stranded <b>black-awning boat 乌篷船</b>. Two-storey galleries, dusty hangings, an empty stage.')
    s += P('<b>Mistress Wang 王氏</b>, fifty-odd, the owner, invites the party in for tea. Husband and son taken for corvée labour; only she and her five-year-old daughter remain, "and a homeless young woman we took in". The performers fled; the men were pressed, the women went to relatives or were taken by soldiers. She will gladly lend the boat and help load it on a cart (moving it to the river needs the wanderers, Xu or Magistrate Fan).')
    s += P('<b>Autumn 秋筠</b> eavesdrops throughout. What happens depends on whether the party mentions "the scar-faced woman":')
    s += UL([
      '<b>Not mentioned</b>: ' + ROLL('Spot Hidden / Listen') + ' notices someone at the window. Followed, a veiled young woman comes forward and apologises: she is Autumn, lodging here; her husband is across the river in Southbright; she came to visit kin, was abused and cut across the face, tried to drown herself and failed; Mistress Wang took her in. She will not show her face. ' + ROLL('Spot Hidden') + ': thick calluses on her fingers, hard forearms ("rough work"). She begs to be taken across to her husband. She says she is good at disguise (fixed 70): while she lives, the party may ask her help once a day before acting, free. Tearing the veil off: opposed ' + ROLL('DEX vs 70') + ', win by a level: a face crossed with scars. Hard Spot Hidden: some cuts are too neat, of different ages; critical: under them, the tattooed characters of a condemned prisoner. <b>Accusing her of poisoning Ling Daiqiu starts the fight.</b>',
      '<b>Mentioned</b>: ' + ROLL('Spot Hidden') + ' sees the window open a crack and a white figure flash onto the roof; Listen hears light steps. ' + ROLL('DEX') + ' to catch her (bonus die if the first roll succeeded), then combat. Badly hurt, she shows the Undying form: first sight SAN 1/1D10 (1/1D4 if the party has already seen a Servant).',
    ])
    s += GM('Autumn (human): STR 60 DEX 70 POW 60 CON 65 APP 70 SIZ 60 INT 65 · HP 12 · Sword 70, Dodge 65, Jump 65, Disguise 70. A famous outlaw of the Jinghu country with "a thousand faces"; caught by Fan and sacrificed; still a thief as an Undying. She stole the Ling needles and cast Green Rot 绿腐 on Ling Daiqiu. When she dies the green mould on Ling Daiqiu vanishes and he recovers. Until exposed she genuinely helps the party.')
    s += P('<b>Autumn\'s room</b> (after the fight Mistress Wang goes to look): incense, good-smelling, but ' + ROLL('Listen') + ' catches the same damp rot under it. Neat bed; under the vase two pages (handout "Green Rot"): the spell <b>Green Rot 绿腐</b>: chant, give the victim a fresh green leaf; the organs rot for seven days until the body is a heap of green mould; the only cure is to kill the caster. Reading it: SAN 1/1D4.')
    s += H('Wang Wu\'s Restaurant', '王五分茶')
    s += P('The biggest eating-house in town (a 分茶). <b>Shut on the 12th</b>: last night the watchman accused them of hiding a thief; he and the owner fought and broke tables. From the 13th the waiters seat you warmly: beef noodles, braised duck tongues, all the local dishes. Eating here costs no round.')
    s += P('The "thief" is <b>Chen Xunzhong 陈寻忠</b>, Liu\'s standard-bearer, now an Undying Servant sheltered by Wang Wu; he stole medicine from HO2\'s pharmacy and Nameless Fang chased him here. <b>Toghan 脱欢</b> eats here every noon in the best upstairs room (two guards at the door who taste everything first): the chance for HO2\'s revenge ("Blood debt", below).')
    s += P('Table talk: Wang Wu 王五条 is kind, gives rice gruel to the poor, caught a thief and let him go with money. Toghan comes daily at noon, second floor, best room; his two Tartars look down their noses and taste every dish.')
    s += P('<b>Wang Wu</b> (found any time after the poisoned meal) apologises for it and tells what he knows: Fan "loved the people, but nothing comes without cost" — then the whole plan: the rite, the sacrificed prisoners, the flotilla, the thing in the river. Chen: "a man I found at the riverbank with nowhere to go". The banquet: "the men left on the ships are old men and Song turncoats; General Toghan ordered us to bring them wine and meat on the night of the 17th." <b>The raid</b>: after a pause he agrees to let the party, the wanderers and the fishermen go in disguised as his delivery crew. (If HO2 poisons Toghan here first, Wang Wu shuts the shop and will not open this door; he asks to cross the river with the party.)')
    s += P('<b>"Is this food poisoned?"</b> Liu goes grey over his noodles and vomits blood, then is fine in a moment. ' + ROLL('Medicine') + ': his pulse is far too steady for a living man; he is evasive. Tasting the food, ' + ROLL('Pharmacy / Medicine') + ': a numb tongue; fresh pokeweed 商陆, harmless in small doses, bleeds the stomach in large ones, worse with wine. ' + ROLL('Spot Hidden') + ': someone is watching (do not say who). After the meal Chen, dressed as a waiter, kneels weeping before Liu and HO3 and asks to meet them alone at midnight at the Street Crossing (→ Optional: "Rashomon alley"). Liu, overjoyed to see a comrade alive, waves the poisoning away as "drank too fast" and tries to keep HO3 out of what follows.')
    s += H('Blood debt: killing Toghan', '不共戴天')
    s += P('If Wang Wu once owed HO2\'s family (famine relief in HO2\'s backstory; a low-morals HO2 may have none), he helps with the poisoning, the disguise and the way in; otherwise everything is done behind his back and discovery means arrest as thieves. Waiter disguise needs no roll; a successful Disguise avoids notice at close quarters. Chen will cooperate.')
    s += UL([
      'Kitchen: three cooks, two helpers, runners. The ready dishes stand apart; a PC can carry them up or let others.',
      'Second floor, third room: an eight-immortals table, a silver incense burner, a screen inside the door, a decorative wardrobe (Stealth to hide in). Poison can go in the burner beforehand.',
      'Toghan inside with two guards; two more at the door. Any noise brings the door guards. Only Toghan and the two door guards eat; guards still standing will try to save the poisoned, so they must be dealt with.',
      '牵机药 (bitter, strong scent, mask with strong wine or tea; 15–30 min) · 十香软经散 (colourless, instant; must be added to the wine in the room: ' + ROLL('Sleight of Hand') + ' under Mongol eyes).',
      'Afterwards Wang Wu closes the shop in terror and asks to cross the river with the party. The warship raid can no longer start from here.',
    ])
    s += GM('Toghan: STR 75 DEX 60 POW 50 CON 70 APP 55 SIZ 80 INT 50 · HP 15 DB +1D4 · Brawl/Sabre 75, Dodge 70, Spot 60. Bad Chinese, violent, moody; killed HO2\'s father; despises Duan.')
    s += H('The pharmacy (HO2\'s house)', '药铺')
    s += P('Shut, two clerks busy inside. This branch is grasping: sky-high prices, clerks who size up a customer\'s purse. The manager fawns on the young master/mistress: HO2 may use staff, stock and cash freely. He produces two old recipes found in the storeroom (handout "Two poisons"): <b>牵机药 Bowstring</b> (from ripe strychnine seeds; bitter, peculiar scent; stiffness after 15 min, the body arched like a bow after 30, grinning spasm, fully conscious, death by suffocation in about an hour) and <b>十香软经散 Ten-Scent Powder</b> (ten spices with datura and 软骨草; white, odourless, tasteless; instant collapse of the limbs, martial skill gone after some days). Making either: Hard ' + ROLL('Medicine') + ', once a day.')
    s += P('<b>"A plea for medicine"</b> (first visit): a girl in red with a long and a short curved sabre is arguing over prices: <b>Ling Xuchun 凌序春</b>. Her brother <b>Ling Daiqiu 凌代秋</b> is dying of a strange poison and this is the only pharmacy with stock. What poison: <i>Rainmaster\'s Ink 雨师墨</i>, they say — "雨师墨黑，刀饮即腐；天若垂泪，骨露生蛆". Why: their family heirloom, embroidery needles thin as ox-hair and hard as iron, the perfect Acupoint tool, coveted by every master. They sheltered a woman; three days ago she stabbed her brother and ran with the needles; the blade was inked. The killer: <b>Autumn</b>, slender, a face crossed with scars; her brother found her by the river and took her for an orphan. Her brother: open-handed, nicknamed "排空击浪穿云翻天龙", the man every fisherman on the Han follows; if you need the fishermen, he can ask them, if he lives. The herbs she lists are all damp-dispelling: the neighbour doctor\'s recipe only eases the attacks. Leave word for her at the Wineshop. Cure him and she is yours for life; avenge him and the needles are yours.')
    s += P('<b>Visiting Ling Daiqiu</b>: a plain house in a lane on the river side of Front Street; fishermen call. He lies grey, breathing shallow, stinking of damp rot, the wound on chest and belly festering and not healing. ' + ROLL('Spot Hidden') + ': fresh patches of mould around the wound, spreading; in his palm a fresh green leaf. Cured (by killing Autumn), his word brings the fishermen into the raid.')
    s += GM('Ling Xuchun: HP 12, Sabre 70, Dodge 70, Climb 60, Swim 60. Ling Daiqiu: HP 13, Swim 75, Boat 70.')
    s += H('The Teahouse', '茶楼')
    s += P('Three floors; private rooms above, a wide hall below with a storyteller\'s dais and, behind a screen on the right, the tea master\'s table where a thin white-browed old man sits. Song and Mongol customers mixed; nobody looks at the party. The storyteller is mid-tale: the Liangshan outlaws rescuing Song Jiang from the execution ground at Jiangzhou 江州劫法场 (plant it: the rescue of Niu will be exactly this).')
    s += P('Clues from customers, waiter, Listen: <b>Niu shot Ashu\'s nephew</b> dead among ten thousand men; he has a God-Arm Bow that shoots four hundred paces, "unless the Mongols have it now". The waiter recommends the tea master <b>Song Zeyi 宋择一</b>, "瓯面弄泉", whose tea-paintings even the emperor praised, "and Commander Fan thought the world of him".')
    s += P('<b>Song Zeyi</b>: a five-foot tea table full of cups; a short goatee; smiles; asks what picture you would like in your foam (flowers and birds: "you care nothing for office"; coins: "the wealth of the world"; characters: he tells their story). He pours and whisks with perfect ease.')
    s += P('<b>"Tartar insolence"</b>: three Mongol soldiers at the next table laugh loud, insult the Song and the dead Commander Fan, kick the waiter over for weak tea, and shove the tea master\'s customers (the party included) aside to demand his tea. A scholar, <b>Zhou Wentong 周文通</b>, protests and is knocked down. Choices:')
    s += UL([
      '<b>Soft</b>: smooth it over (a woman\'s voice helps), bribe, or talk them down: a bonus die to any Sleight of Hand on them now. Ends with "The Mongols\' general" below.',
      '<b>Hard</b>: the soldiers draw. Song throws each PC a cup of tea with a picture — HO1 a red sun over crags, HO2 a willow bridge in wind, HO3 a dream of yellow millet — drink for a bonus die in the fight; then he stands on the screen and asks the party to settle it. Before each exchange he tosses another cup: ' + ROLL('DEX') + ' to catch, one bonus die each. Three soldiers (HP 12, Brawl 40, Dodge 40, armour 2); the house closes its doors and the patrols are not alerted for a while. Win and the owner cleans up; the general does not appear.',
      '<b>Watch</b>: Song answers back, the soldiers wreck the place. Step in at any point for a fight. Never step in and Song gives no wineshop address and turns cold.',
    ])
    s += P('Song afterwards: the river\'s strangeness is "just weather" (open ' + ROLL('Psychology') + ': he is hiding something). Fan was a good official who did everything himself; Song "helped him catch thieves" and knows nothing of what became of them or the condemned (opposed Psychology: hiding it). Boats: Prefect Xu\'s household keeps painted barges and fishing skiffs, "but the man guards his skin above all". Doctor Yue: he knows the "Hollow Physician" blackmailed Xu and disapproves — a wanderer should not break the law even for the poor. If the party helped, he gives the <b>Wineshop\'s address</b>: where the town\'s wanderers meet; going there costs no round.')
    s += GM('Song Zeyi: HP 11, Throw 70, Jump 70. He helped Fan gather the sacrifices and hides it; he takes no part in anything to do with Gla\'aki.')
    s += P('<b>"The Mongols\' general"</b>: a young Chinese general on horseback, <b>Duan Driftwood 段游衍</b>, passes the door, scolds the soldiers for brawling in town and wasting time, bows to the tea master and the party with perfect manners, looks twice at HO1 if present, and rides on.')
    s += H('The Coffin Shop by day', '棺材铺')
    s += P('Shop front, courtyard behind; millet gruel, flat bread, pickles. Finished coffins with lids off drying their lacquer; ' + ROLL('Spot Hidden') + ': hidden compartments in the walls. Winding Stream 曲流 works here by day: there are many dead in wartime; she made Commander Fan\'s coffin; people put the dead\'s belongings in the compartments against thieves and rot, "and young Master Fan asked for one too".')
    s += P('<b>Evening of the 12th</b>: Doctor Yue 越南柯 is chatting with her when the party returns (see the Session 0 runbook, Extended Day One). Boats: Xu\'s two unsent letters (handouts). Poison: "the local gazetteer might record it". Scar-faced woman: "either misfortune or a condemned convict". Fan: "far-sighted, devoted — executed a man for stealing a few taels of lamp oil".')
    s += H('The Undying family\'s house', '某处民宅')
    s += P('Address from the gaol (the bun) or the burning house. A cold front hall, door shut. A pale young girl answers: mother and she have the fever. Told of her aunt\'s family in the fire she goes weak at the knees and falls, carefully, against Liu. She asks Liu in to carry firewood; HO2, a doctor, may come too. <b>She and her brother are Undying</b>; without Liu present she admits no one.')
    s += P('Neighbours (for those outside): the father died early; the son was sentenced to death the other day; the widow and daughter went to the river to make offerings and came back with "the fever"; the girl took things to kin near the Back Street guildhall a few nights ago; a tall man in white climbs their back wall at night. ' + ROLL('Spot Hidden') + ' at the back wall: bricks worn by frequent climbing; damp rot on the air from the yard.')
    s += UL([
      '<b>By day</b>: Liu, walking to the yard to chop wood, is suddenly "sunstruck" and sits silent drinking water; the girl says mother is asleep and asks them to leave, crying "they bully a widow and orphan" at any push. Outside, Liu speaks of the stench and a bad feeling and proposes coming back at night.',
      '<b>By night</b>: Liu goes to the yard; the girl locks HO2 in an empty room (' + ROLL('STR / Locksmith') + ' to get out) and HO2 arrives to find her attacking Liu.',
      '<b>The night raid 夜闯民宅</b> (night only; by day the neighbours beat "burglars" to death): over the back wall, the stink of the yard; ' + ROLL('Spot Hidden') + ': the trough glows faint green, thick and foul, a bundle of clothes, two silver ornaments and a pair of embroidered shoes soaking in it (SAN 1/1D3). The girl and a tall white-clad man with tattooed cheeks appear on the porch and change: bones twisting, limbs drawn out into spines, skin rotting, nails long. First sight SAN 1/1D10 (1/1D4 if seen before). Combat; Liu is their first target.',
    ])
    s += P('Afterwards the bodies keep the monster shape: a healed wound on the spine, red web-lines over the back. ' + ROLL('Medicine') + ': something sharp was driven in violently; the spine is altered and brittle; a thin point would snap it. Then a boy with a copper mallet and gong and a long cloth-wrapped bundle is crouching on the wall: <b>Nameless Fang 方未名</b>, the night watchman. He asks, examines the bodies, and says he must tell Niu. Told Niu is in the gaol, he asks for help and names the Wineshop for tomorrow.')
    s += H('The Wineshop (hidden; no round)', '酒肆')
    s += P('In a lane off Front Street; address from the tea master or Ling Xuchun. Small, old, worn tables, two rows of great black-glazed wine jars under red cloth. The owner <b>Du Guanshan 杜观山</b> greets you warmly and remarks that HO3 "is not really one of us". Regulars: <b>Huaide the "Pagoda Arhat" 宝塔罗汉怀德和尚</b> and <b>Nameless Fang</b>.')
    s += P('<b>The monk</b>: "the great master from our temple — Iron Shirt and Golden Bell, try your acupoints on him, it\'s like pressing cotton! He\'s been here half a month and the temple dust must be a yard deep." Drinks or meditates at the wall. Each day he challenges one person to drink: three CON successes in a row win his <b>golden kasaya 金袈裟</b> (armour 2, immune to fire). Fail and try again tomorrow. Tell him about the locked side hall or the footprints at the temple and he comes to the Temple fight.')
    s += P('<b>Nameless Fang</b>: "Niu sent him to me to feed. He beats the watches all night, sleeps badly, can\'t talk to people, but he\'s pure gold; Niu thinks the world of him. Keeps saying he must give back what he carries on his back." If the party met him at the Undying house, he tells them he went to find Niu that night and was told he was in the gaol awaiting execution; he rolls up his sleeve to show a bruised arm, and asks them to rescue Niu. (Ask around the gaol: last night a watchman killed four guards with a copper mallet.)')
    s += GM('Du: HP 13, Blade 65, Dodge 60. Monk Huaide: use Du\'s numbers plus armour 2 and the kasaya. Nameless Fang: STR 70 DEX 70 POW 70 · HP 11 DB +1D4 · Mallet 75, Dodge 70, Climb 70, Spot 60. He carries the God-Arm Bow wrapped in cloth and does not know what it is.')
    s += P('<b>Planning the rescue 救援牛富</b>: the gaol is hard in and out; the condemned must pass along Front Street to the Street Crossing: "Like Jiangzhou! The street is lined with teahouse galleries and painted gate-towers — ambush from four sides like Chao Gai and Li Kui. Hands enough: Fang, Mistress Qu, the Jiang brothers, the Ling girl, Master Song from the teahouse, and me." (Only NPCs the party has actually met.) The wanderers\' skills: the Jiangs know every lane and swim like fish; "nobody in Fencewall dares cross the Ling girl"; Mistress Qu is stronger than she looks, "they say she held her husband under in the well"; Song is slippery as a loach. Du draws Front Street with a tea-wet finger: stalls, and the <b>painted gate-towers 彩楼</b> of silk and timber over shop doors, flimsy and ornate. The plan needs three parts: <b>stopping the carts</b> (who, how: topple a gate-tower, shoot the cart horses), <b>finding Niu</b> (three carts; only Fang knows his face, so only he can scout ahead and signal), <b>getting away</b> (route, who covers). Du fixes the meeting for noon-and-three-quarters on the 15th at the Street Crossing.')
    return s

# ---------------------------------------------------------------- 3. BACK STREET
def back_html():
    s = H('Back Street', '后街', 1)
    s += H('The Guildhall', '会馆')
    s += P('The merchants\' hostel, now the Mongol billet. Duan 段游衍 lodges here for convenience with his guards and adjutant; a gleaming fur carpet outside his door marks it. In by the front door with a token and a plausible story, or ' + ROLL('Climb') + ' up the back to the first floor (fail: injury).')
    s += P('<b>Duan\'s room</b>: a jumble of Ashu\'s gifts — an old curio shelf, a glittering coral tree, a painted wool carpet, literati paintings; two swords and a bow on the rack; on the wide desk brush, ink and paper, a short note, a letter, and a full <b>defence map of Fencewall and Southbright</b>.')
    s += UL([
      '<b>The letter</b> (handout "The Hermit\'s letter"), strong hand, signed Chen Yangshan 陈阳山: "You urged me several times to leave Mount Crag… I am old and my pupil is among wolves; how could I go alone? If HO1 succeeds, the name will be in the histories; if not, I beg you for old friendship\'s sake to save a life. I enclose what remains of Red Pine as payment…"',
      '<b>The note</b> (handout "Toghan\'s note"), curt, from one general to another: the Marshal feasts the army at the Magistracy; the assault follows next day. Wang Wu\'s restaurant will feed the men left on the warships — ten oxen, eight sheep, thirty each of chickens and ducks, fifteen jars of old wine — delivered by the restaurant\'s own people on the <b>evening of the 17th</b>. "Few men on the ships; be watchful, let no rogue slip in. General Duan, see to it." → most soldiers go to the feast; the ships are thinly held.',
      '<b>The map</b>: both banks, garrisons, places of note; the <b>Watchtower 塔楼</b> on the Fencewall side is marked separately: "Fine view. Boats in the river and troop movements on the Southbright bank all in sight."',
    ])
    s += H('The burning house', '会馆附近的民宅')
    s += P('Passing along Back Street the party meets a house on fire: dry winter, piled firewood, the neighbours helpless. An old woman begs for help: her niece\'s family, five people, two children under ten, trapped; the father died in the war last year and the pension never came.')
    s += P('The fire is an accident; the family are kin of the Undying house on Front Street and were all turned by the girl. <b>They fear fire and cannot flee it.</b> Beams and roof falling, smoke, burning furniture: ' + ROLL('DEX') + ' to get in or 1D3. The five hide in wardrobes and under beds; ' + ROLL('STR') + ' to drag one out — into the firelight, where its skin melts, spines push through and the body collapses into dark green liquid with a damp stench: SAN 1/1D10. The fire drives everyone out. Neighbours: "the whole family gone, only the cousin on Front Street left to bury them — and that house has had the fever and not come out for days." Ask, and they give the Front Street address.')
    s += H('Seven Treasures jeweller', '七宝行')
    s += P('Lavish, selling gems and curios; no custom; a manager and one assistant. Information is traded for a game of <b>stone gambling 赌石</b>: ' + ROLL('Luck') + ' decides the stone cut open — fail: serpentine or quartz; success: aventurine or goldstone; Hard: Nanyang jade or sugar jade; Extreme: bright-green jadeite or royal lapis; critical: imperial-green jadeite or tianhuang.')
    s += P('The manager knows all the gossip and the <b>Grand Lake Stone 太湖石</b>: "Commander Fan ordered it here: two zhang high, eighty-one holes, \'letting through the north wind and the sounds of heaven and earth\' — and in the forty-sixth hole a piece of green jade had grown. A wonder of the age; offered to the emperor it would have bought a marquisate. But the Commander wanted it brought into Fencewall to pray for the people of both banks, so I obliged him."')
    return s

# ---------------------------------------------------------------- 4. STREET CROSSING
def crossing_html():
    s = H('The Street Crossing', '街口', 1)
    s += P('Where Front and Back Street meet; you pass it going between them. Inns, tea stalls, and the execution ground: beheadings at noon-and-three-quarters, bodies hung until midnight.')
    s += H('12 January, noon: the Hermit', '一月十二日')
    s += P('A crowd, a strange heavy mood. Today\'s body is a white-haired old man with one arm, a spear through his throat holding him in the air: the <b>Hermit of Mount Crag 山阳道人</b>. His face is calm, as if he had long expected this. HO1: SAN 1/1D3 if he mattered. From the crowd: Ashu went up Mount Crag to repay the pupil\'s sword-cut and took the seventy-year-old hermit, "and gave him a cut back — the hermit\'s famous Stillwater is three feet long, and Ashu\'s horse-cutting sabre took him in half". And: Ashu will behead the Song officials who refuse to submit, Niu among them, in a few days, "lucky young Master Fan surrendered so fast".')
    s += H('15 January, noon: the rescue of Niu', '一月十五日 · 劫法场')
    s += P('Niu is brought from the gaol: ' + ROLL('1D4+2') + ' horsemen, ' + ROLL('1D4+4') + ' foot soldiers, three cage carts with draught horses. Secretly roll ' + ROLL('1D3') + ' for which cart holds Niu. <b>Show the players the rules card "The rescue".</b>')
    s += UL([
      'All friendly NPCs except Fang are commanded by the players and rolled by the GM. Players act, then soldiers; no DEX order. Soldiers attack whoever approaches the carts first. <b>After five rounds reinforcements arrive</b>; getting away with Niu is the win.',
      '<b>Stopping the road</b>: topple a painted gate-tower at the right moment, or kill the cart horses.',
      '<b>From the galleries</b>: anyone up high can attack any target with any ranged skill; a failure may hit a friend or a bystander.',
      '<b>Closing with horsemen or horses</b>: combined ' + ROLL('DEX or Dodge + fighting skill') + '; fail and a hoof does 2+1D3.',
      '<b>The carts</b>: one round to reach, one round of ' + ROLL('STR or Locksmith') + ' to open. Three shackled prisoners in each beg to be taken; one PC/NPC carries one prisoner; Niu tells you to take the others first, but is too wasted to resist being carried.',
      '<b>Leaving</b>: after five rounds the Mongols pour in. Horses, or into the lanes. Ranged PCs leave freely; melee PCs ' + ROLL('DEX') + ', fail and a wanderer covers them and dies doing it. Mounted: bonus die; carrying a prisoner: penalty die.',
    ])
    s += GM('Foot: HP 11, DEX 40, Blade 40, Dodge 40. Horse: HP 12, DEX 50, Blade 45, Dodge 40, armour 2.')
    s += P('<b>Niu rescued</b>: he tells all he knows and has Fang give the bow to the party ("I saw a young hero shoot like a god just now"); then he stays at the Wineshop and takes no further part. He knows Fan meant to "invite a god into the Han to stop the Mongols", not what it was: "he said he would take it to his grave". Before that Fan filled the death-cells with people whose crimes did not deserve it; a physician named Yue was nearly taken. The <b>God-Arm Bow 神臂弓</b>: 1D8+2, 400 paces; from the bank it reaches the middle of the river — the only bow in the scenario that does.')
    return s

# ---------------------------------------------------------------- 5. TEMPLE
def temple_html():
    s = H('The Temple', '寺庙', 1)
    s += P('A small temple by the city wall, incense cold, untouched because Kublai honours the Buddha. One main hall and one side hall whose heavy door is shut, seemingly locked from inside. ' + ROLL('Spot Hidden') + ' in the dust: fresh footprints of many sizes.')
    s += H('Night at the temple', '夜战山寺')
    s += P('Fires after the day\'s three rounds, on the night after Chen\'s invitation (Optional: "Rashomon alley"). If the party told the monk about the locked hall or the prints, he arrives during the fight.')
    s += UL([
      '<b>The others</b>: Liu proposes that he and HO3 keep Chen\'s appointment first "so as not to startle the snake". Let Nameless Fang\'s night round, or an Undying disguised as a passer-by, make the rest of the party suspect something.',
      '<b>HO3 and Liu</b>: Chen leads them in by the back gate, asks HO3 to go quietly (make a secret roll for tension). Dead silence; the back hall door is open. Inside, Chen shuts the door and snuffs the candle. In the dark ' + ROLL('1D4+2') + ' Undying wait. Chen: "Set your mind at rest, my lord. We were fortunate: the Lady of the Han received us and ferried us over the sea of suffering to the land of the Buddha. General Liu should have come too — why will he never go with the Lady? She misses him so!" Liu\'s face changes; he tells HO3 he should have died with his men rather than live as neither man nor ghost. The old soldiers take their monster form, unarmed, attacking everyone including Liu at random. <b>In the dark all HO3\'s and Liu\'s rolls are at −20</b> until the back door is opened and moonlight comes in. PCs outside arrive next round.',
    ])
    s += P('Afterwards Liu explains everything he knows: how the thing in the river turns people into its servants, and that he somehow escaped its control.')
    return s

# ---------------------------------------------------------------- 6. MAGISTRACY QUARTER
def magistracy_html():
    s = H('The Magistracy quarter', '衙署一带', 1)
    s += H('Commander Fan\'s residence', '范天顺的宅邸')
    s += P('Plain and quiet; most servants dismissed. Magistrate Fan 范玉楼 accompanies visitors to pay respects in the mourning hall. An everlasting lamp burns at the <b>study</b> door.')
    s += P('<b>The study</b>: simple, elegant; a mahogany desk facing the window; calligraphy from friends; no weapon rack, two crammed bookcases. ' + ROLL('Spot Hidden') + ': a nameless old book newly re-covered, pages very old, a traveller\'s record with several pages torn out; ' + ROLL('Library Use') + ' to skim (handout "The traveller\'s record"): "Beside Mount Qiao, in the Qiao river, lives a great fish called 何罗 He Luo: one head and ten bodies, like hundreds of fish entwined, writhing day and night… when I was exiled to Tanzhou, people near Lake Dongting had seen it: whenever it appears a great fog rises on the lake and no boat can pass." On the desk a Tang poem lies open (handout "The poem"): the poet carried off in a dream by a goddess and her attendants, waking on the shore of Lake Tai with voices still calling him.')
    s += P('<b>The mourning hall</b>: white banners, the three sacrifices on the altar, incense, a black-lacquered coffin in the centre. Winding Stream\'s hint about the compartment is the way in; the coffin can only be opened by sneaking in. ' + ROLL('STR') + ' to prise it: <b>empty</b>; ' + ROLL('Spot Hidden') + ' inside: the compartment, holding the torn pages (handout "The torn pages"): (1) "Who eats the flesh of the He Luo fish has his marrow washed and his spine drawn; a web of fine lines grows on his back. He needs no grain but cannot bear the sun, hiding by day and walking by night. All such learn the art called Green Rot… to undo it the person must be destroyed; there is no other way." (2) "The He Luo fish shuns light and heat and fears fire more than tigers, and so do those who eat it… it lies hidden on the river-bed and does not rise unless boats pass over…"')
    s += H('The assassination plan', '刺杀计划')
    s += P('When the coffin\'s secret is found, Magistrate Fan appears at the hall door with a lantern and coldly accuses the party of insulting the dead. Accused of harming the people, he says plainly that <i>it is this guest in the river that holds off the Mongol cavalry and shields the Song; the people of Fencewall have not had to live as slaves</i>. Liu rages about his drowned army; Fan explains nothing. Guards are posted all round the house: no one leaves unless they accept his request. He means to use Ashu\'s desperation for a cure: <b>kill Ashu</b>.')
    s += UL([
      '<b>The plan</b>: HO1 and HO3 go in as HO2\'s assistants to treat the Marshal, and strike.',
      '<b>Guards</b>: "the righteous have many helpers"; he will arrange a signal (the scholars).',
      '<b>Proof</b>: Ashu is suspicious; the party must show they can cure the Ink — a cured patient, for instance. There is no cure; he suggests they fake one.',
      '<b>Weapons</b>: none may be carried into Ashu\'s room; his guards are the pick of every tribe.',
      '<b>Help for the crossing</b>: gunpowder, weapons. And: "when the commander dies the city will be in chaos — cross then."',
    ])
    s += GM('Tell the players plainly: after the assassination they cannot move freely in Fencewall again (only the finale remains), so prepare everything first. If they refuse, hoofbeats outside: Fan, nervous, takes them for Mongols and lets the party out the back; outside, soldiers chase loose horses — Doctor Yue let them out of the Mongol lines to make the noise.')
    s += H('Prefect Xu\'s mansion', '许德显的宅邸')
    s += P('Glittering, gate shut, nobody calling; servants sweep the forecourt. Xu 许德显, the fat prefect who runs the treasury, sits in his study with curios and a few maids. He can provide <b>gunpowder, boats, and a way into the gaol</b> for anyone without a token. Get to him by talking/bribing the sweepers (friendly bargaining) or over the back wall by ' + ROLL('Climb / Jump') + ' (then it is coercion).')
    s += P('Bribery, blackmail with his two letters, or fear ("when the court retakes the twin cities it will try the turncoats" — best from HO3 and Liu) all work: "Don\'t you know? His Majesty has moved two hundred thousand men from Huguang and the Zhe circuits to hold the rear. Southbright is a fortress and Lü Wenhuan 吕文焕 no fool; if it falls the armies close in and the Mongols are fish in a jar. Refuse us now and all your money will not keep your head on your neck."')
    s += H('Niu\'s house: Ashu\'s sickroom', '牛富的宅邸 · 探怀出刃')
    s += P('Confiscated when Niu was gaoled; Ashu has taken it over. HO1 and HO3 disguised as HO2\'s assistants; Doctor Yue insists on coming as the experienced one (he can also supply fake-medicine materials). Facing the door an eight-immortals table under a painting of a general subduing barbarians; painted carpets, low tables, ox and sheep skulls, a horse-head fiddle; by the door a Mongol bow and <b>three white-fletched arrows</b>.')
    s += P('Ashu half-reclines on the bed: over eight feet, massive, the wounded arm bared, an eight-foot heavy sabre by his good hand. Kneeling beside him a Song girl who looks like Magistrate Fan (<b>Fan Yuying 范玉莹</b>, the Commander\'s daughter); behind the bed a Song physician. Two armoured Mongol guards inside and two outside, swords but no helmets, some acupoints (哑门 etc.) bare. ' + ROLL('Spot Hidden') + ' close up: the unwounded hand is less worn — not his sword hand.')
    s += P('Ashu knows of Ling Daiqiu\'s poisoning. To HO2 he is all kindness: condolences for the father, praise for the skill, rich promises. Suspicious, he allows no treatment until he holds a hostage: whoever HO2 names as kin, Doctor Yue steps forward as the elder brother and is led away. Then treatment may begin. His sabre stays by his left hand throughout; any sensitive move (a weapon, an acupoint touch) forces the fight. He talks all the while:')
    s += R('"My men came to the Central Plains and fell in love with its soft riches; none wants to go home. I only saw the south\'s charms myself when I came here. Look — that is Commander Fan\'s daughter. For all his loyalty, his daughter ends up holding a Mongol\'s broom. Doctor, tell me: what was it all for?"')
    s += R('"They say this place is thick with legends, the Lady of the Han above all. I used to wonder whether she was as lovely as they say. But since I came to Fencewall I have heard another version — that this goddess eats people. Is it true?"')
    s += UL([
      '<b>The physician</b> checks every medicine handed to Ashu; he can tell if it is tampered with, and says nothing.',
      '<b>Fan Yuying</b>: Ashu makes whoever brings the medicine taste it first; she will not fight but blocks one blow for a PC and, when Ashu swings at HO2, slips her a dagger.',
      '<b>The scholars</b>: during treatment, noise outside; a soldier reports scholars rioting at the gate, being dealt with; Ashu ignores it. This is Fan\'s signal: strike now and the outside guards do not come.',
    ])
    s += H('The fight: "the brave wins in a narrow pass"', '狭路相逢勇者胜')
    s += P('Ashu snatches the sabre and cuts at the nearest (off hand: −20%). HO2 may Dodge; on a failure Fan Yuying takes the cut and passes HO2 the dagger. The guards draw; outside, steel rings; no help is coming. DEX order. The physician hides; Fan Yuying absorbs one hit for the party. <b>After five rounds the deputy arrives and kills everyone</b> — do not let it come to that.')
    s += UL([
      'Guards: HP 12, DB +1D4, STR 65, DEX 40, Dodge 40, Blade 40.',
      'At this range a bow gets a bonus die and +1D4 damage; only the three white arrows are there. Grabbing the sabre is ' + ROLL('STR') + ' (1D8+DB). Taking bow or sabre costs a round.',
      'Ashu to HO1: "Last time you were lucky. Back again, not afraid to die? I had that old man\'s head hung half a day longer for you — did you not see? You Song talk of virtue and use poisoned tricks. No matter. Let me see how much real skill you have." To HO2: "Your father did not know his place and neither do you. I wonder how much your sworn brother loves you — what will he think when he sees your head?" To HO3: "The draw is almost right; a long way from your Niu. Child, you have never killed a man, have you?"',
    ])
    s += P('<b>Ashu at 0 HP ends it.</b> Outside: chaos, scholars dead on the ground. Hold up his head and shout it, or slip away; the wanderers cover the escape and townsfolk help all the way out of the quarter.')
    s += GM('<b>Lockdown.</b> The city goes under martial law; this is the night of the Watchtower. The Mongol attack on Southbright is postponed. Every move now needs ' + ROLL('Luck or Stealth') + '; fail and a chase round begins (see the Cheat Sheet). Doctor Yue is held in another empty house of the Magistracy; the wanderers bring back a letter from him explaining the early summoning, and the news that he has burned himself to death — unless the party had him rescued first; either way he was ready to die. Magistrate Fan is beheaded on the spot and his head hung on the Watchtower.')
    s += H('The School and the Library', '官学 · 藏书阁')
    s += P('Where the scholars lectured; unguarded, anyone may enter; a few scholars packing up. The library is inside. The scholar <b>Kong Liyue 孔礼岳</b> takes the party for soldier-ruffians: "This is the house of Confucius and Mencius… you do not look like readers; the books here are a hundred years old, rare copies — what if rough hands damage them?" <b>Zhou Wentong 周文通</b> rebukes him: he knows the town and can tell righteous men; Kong apologises.')
    s += P('Classics, histories, local gazetteers. Name the subject and ' + ROLL('Library Use') + ' (handouts "From the Library"):')
    s += UL([
      '<b>Rainmaster\'s Ink</b>: a local physician\'s notes: the wound festers and gives off a sick damp stench; the pulse clogs; the blood runs backward; deep poisoning spreads over the whole body; shallow poisoning festers for months or a year and then re-opens in every spell of rain. ' + ROLL('Idea') + ': not quite Ling Daiqiu\'s case — nothing here about green mould.',
      '<b>The Lady of the Han</b>: a book of local tales; one chapter is not the version you know: Zheng Jiaofu met the goddess, spoke rudely, asked for her pendant as a betrothal gift; she hid her anger, untied the pendant, and set a midnight tryst. He went and found no beauty, only a starving wolf five feet long, which ate him whole and left the pendant on the bank, unchewable. The place is called "the Lost Pendant Shoal".',
      '<b>Annotated Records of the Three Kingdoms</b>: the local battle marked: Guan Yu attacked Fencewall when the Han flooded, drowned seven armies, shook the empire — then Sun Quan broke faith, Lü Meng took Jiangling, and Guan Yu was taken and killed at Linju.',
    ])
    s += P('Other scholars approach, praising the party\'s deeds (the teahouse) and cursing the Mongols and the court: "We too wish to serve the country, but we cannot lift or carry — hiding here, shameful!" They are Fan\'s kindling for the assassination day.')
    s += H('The Gaol', '监牢')
    s += P('Heavily guarded; enter through Xu or with a token, and even then only the common cells — the Song officials who refused are deeper in. Damp mould, constant patrols, cold iron bars, most cells empty, a few haggard prisoners. From prisoners or guards: the empty cells held a batch of <b>tattooed condemned men</b>, some for petty theft, "taken out by Commander Fan to be beheaded a few days ago — not at the Street Crossing, and no bodies seen". And: Fan wanted to gaol the "Hollow Physician" too — "didn\'t he swindle Prefect Xu out of a fortune?"')
    s += P('<b>The bun (optional)</b>: a thin boy in a cell begs: a condemned man gave him a flatbread and asked him, when released, to visit his sick mother; he cannot keep the promise — will they? Accept and get the Undying house\'s address.')
    s += P('<b>Meeting Ashu</b>: as the party leaves, Ashu and several Mongols come out from the depths with Magistrate Fan beside them. If HO3 is present Fan steers Ashu away from the party; ' + ROLL('Listen') + ': Ashu smells of medicinal herbs. They talk loudly of Niu: "What a hard bone, this Niu!" "Stubborn, unbending, does not know that a wise bird chooses its tree. Hard bones or not, in a few days he goes to the Street Crossing — harder than our sabres?" Then <b>Nameless Fang</b> bursts in after Ashu has gone, grabbing people to ask where Niu is and about to fight the guards; stopped and calmed, he asks for help and names the Wineshop.')
    return s

# ---------------------------------------------------------------- 7. RIVERBANK
def riverbank_html():
    s = H('The riverbank', '汉江沿岸', 1)
    s += P('The Mongols garrison the high dock walls; few soldiers near the water itself. East dock: fishermen\'s huts. West dock: several Mongol warships moored, and desolation — a tall tower, a ruined pavilion, endless slender reeds.')
    s += H('East dock: the fishermen\'s huts', '东码头 · 渔民棚屋')
    s += P('A straggle of huts along the dock edge. The fishermen are warm even in want: tea and salt fish. Boats: the Mongols forbid any private boat, and nobody could sail in this fog anyway. The warships: "the Mongols can\'t build ships and the Song craftsmen they dragged off are no masters — that keel, that deck, those gunwales — anyone who knew his trade could snap them." Fan: "took a crowd to the west dock the other day, sacrificing to some god, maybe." Strange things: people climbing out of the Han at night; whole families running to the bank; "a dragon — I saw it lift its head and stare at the Mongols on the shore!" Liu: "a fine young gentleman washed up a few nights ago, unhurt but for a bruised wound on his back crawling with red lines." A boatman: <b>Ling Daiqiu</b>, their undisputed leader.')
    s += P('The fishermen will not join the raid unless Ling Daiqiu asks them. With him, plan it here: on the feast night the ships are thinly held; the fishermen and local wanderers deal with the ships and their crews, the party keeps the shore guard busy. "Seven men on each ship, nearly thirty on the dock; half that on feast night. You gentlemen can\'t swim, so keep the shore men busy — drink and eat with them till they\'re stupid! We\'ll slip aboard and hole their hulls, then a fire to burn their southern dream!"')
    s += H('The Mongol warships: "Sink the ships, deny the crossing"', '蒙古战船驻扎地 · 沉舟绝渡')
    s += P('Moored by the east dock, too well patrolled to approach — except on the night of the feast (17th), while Ashu lives. The party goes in with Wang Wu\'s delivery carts. ' + ROLL('1D10+5') + ' soldiers have deserted their posts to eat; almost all are Song turncoats; their <b>centurion</b> invites the party to join them.')
    s += P('Leave a few jars and some meat here; Liu takes the carts from ship to ship. The fishermen slip off the carts into the water to hole the hulls; the wanderers board to deal with the crews. Meanwhile the soldiers talk: home towns and families (the centurion has two small children), old trades (farmers, fishermen, pedlars), "we just followed our general; he surrendered, so we are Mongols now", and how the Mongols treat Song men like pigs and dogs. <b>Each topic</b>, secretly roll the centurion\'s ' + ROLL('Listen 50') + ' for all of them; <b>two successes</b> and he notices the ships: "When the farthest ship began to rock, the centurion came back from his dream of wine and grease to the cold. He gripped his weapon and stared at you in disbelief; the others came awake too, though the drink made their hands shake."')
    s += UL([
      'Combat. If the party poisoned the food, every soldier dies one round later.',
      'Soldiers: HP 10, STR 60, DEX 50, Blade 40, no armour, DB 0.',
      'Any soldier but the centurion below half HP leaves the fight to raise the alarm. Distance starts at 0; at 2 he is away. Each round he rolls ' + ROLL('DEX') + ' to gain 1; a PC needs a combined ' + ROLL('DEX + fighting skill') + ' to stop and strike him; bows need no DEX roll.',
      '<b>One escapes</b> = alarm: Ashu sends men at once; Duan, as commander of the vanguard, is executed under military law; every fisherman in the raid dies when the relief arrives. <b>None escapes</b>: Duan has time to leave; fishermen\'s losses by a GM 1D100.',
    ])
    s += R('The Han is blacker still at night under the low cloud, a pool of black water deep enough to eat a man. It has: Song flesh and Mongol flesh, men\'s blood and women\'s, the bones of wanderers, travellers, fishermen and generals crunched and swallowed. And now these monsters that boasted of conquering seas will sleep on its bank and never again grind a single inch of ground for their great lord.')
    s += P('Afterwards the assassination is still possible: Ashu\'s wound worsens and he seeks a cure more desperately.')
    s += H('West dock: the Pavilion of the Untied Pendant', '西码头 · 解佩亭')
    s += P('On the north bank, named for Zheng Jiaofu and the goddess; once a place for viewing the river, now ruined, reeking. Rotting corpses and the stone lie under the debris; ' + ROLL('STR') + ' to shift it. HO3 finds a token of Captain Liu\'s here, suggesting his death. <b>The bodies</b>: swollen, discoloured, unrecognisable, marks of violent impact, wounds a pulp: SAN 1/1D3; ' + ROLL('Spot Hidden') + ': prison clothes, tattooed faces. <b>The stone</b>: strange, twisting and rounded, full of holes; ' + ROLL('Idea / EDU') + ': a Grand Lake Stone, the Daoist "cave-heaven"; Spot Hidden on the base: the seal "七宝行 Seven Treasures".')
    s += H('"The goddess comes in dreams" (night, anywhere on the bank)', '神女入梦来')
    s += P('Fog and dim moon; someone wades into the river and stops only when the water is at their shoulders. <b>Not stopped</b>: next moment a spine pierces the chest. The rite takes two rounds — one to pierce, one to inject; pulled out between them the victim dies on the spot. After two rounds the spine detaches from whatever it joins below and leaves a lump on the body; the victim walks away. Stop them now and they are already dead but not yet turned: no response, and any damage kills. <b>Stopped</b> (' + ROLL('DEX') + '): they wake as from a dream — they were asleep at home a moment ago; they have been meeting the Lady of the Han in dreams night after night.')
    s += H('The reeds: forcing the crossing', '芦苇荡 · 三惑迷津')
    s += P('If the party tries to cross without dealing with Gla\'aki: three PCs and one boatman only. Gla\'aki prefers dreams to fighting. <b>Each failed temptation</b> is answered with reality: they wake in the freezing Han, the boat capsized, the boatman gone, spines circling — swim and fight for one round before the next dream takes them. Three dreams (read-aloud texts in the handouts page "The three temptations"):')
    s += UL([
      '<b>1 · The River Lord\'s dream 河伯入梦</b>: beyond the fog, calm open water; a giant turtle surfaces bearing a white-haired immortal fishing with a straight hook, three stools, a tea table, a bucket of small fish. "I am He Bo 冯夷, fishing for all the world. I waited five hundred years for the first fish, three hundred for the second…" A fish in the bucket swells to the size of a warship and swims off. "Mortal cares are heavy; stay and fish with me? One of these fish is a hundred years; one would feed both banks!" <b>Accept = all become Undying Servants, everyone LOST.</b> Refuse and the dream breaks, then the next begins.',
      '<b>2 · The goddess unties her pendant 神女解佩</b>: a goddess in bright robes walks on the fog and tells her story — a maid given to King Zhao of Zhou, drowned with him when the Chu sank the boat, "and do you know what lies on the bed of the Han? Ghosts and dragons waiting to gnaw my flesh. That is the price of loyalty." She seizes a random PC and shows a hideous twisted face: SAN 1/1D3; then, composed again, invites them: the Song is finished, how long will the Mongols last? Drift with her. <b>Accept = LOST.</b> Refuse and she gives the seized PC a jade pendant: its holder is not attacked by Gla\'aki this round.',
      '<b>3 · The Many-Headed Fish 何罗鱼</b>: a fish with one head and ten bodies rises, crying like a bird, the ten bodies swimming ten ways and shaking the whole river. ' + ROLL('POW') + ': fail and you believe you are a fish and leap in; others may ' + ROLL('STR') + ' to hold you while feeling the same pull. Twice. Whoever still knows they are human finds the weapon in their hand and the fish before them. The dream ends when they attack: they are washed up on the Southbright shore.',
    ])
    s += P('→ <b>Ending 2</b>.')
    return s

# ---------------------------------------------------------------- 8. FINALE
def finale_html():
    s = H('The Watchtower: the last night', '塔楼 · 决战', 1)
    s += P('The night of the lockdown, or the night the party chooses to end it. <b>Show the players the rules card "The Watchtower".</b> The tower is about fifteen zhang (50 m), all timber; climbing it is ' + ROLL('CON') + '. Two soldiers below and one above. If Magistrate Fan was executed his head hangs from the tower: SAN 0/1.')
    s += H('Preparation', '准备阶段')
    s += UL([
      '<b>HO1</b> meets the boatman alone in the reeds. Unless the party neither killed Ashu nor sank the ships, Duan is there chatting with the boatman: he wants to be bait with HO1, for friendship, not gain. If HO1 never won the monk\'s golden kasaya, Duan can hand it over (drop this to raise difficulty). HO1 may leave him on the bank. Duan: "Could you really leave a helpless civilian like me in this den of wolves? Take me with you, hero — I cannot close my eyes at night in this town. If you succeed I cross with you; if you fail I have no foothold here either. Let us gamble together."',
      '<b>HO2</b>: Doctor Yue, if alive, walks HO2 to the foot of the tower and confesses: "I was at the river the day Fencewall surrendered. I should not have gone. If I had not come to spy on the bank pretending to be a messenger, if the men preparing the rite had not seen me, if they had not started early… General Liu and his men would have crossed safely."',
      '<b>HO3</b>: on the tower, close enough to touch the sky, Liu talks to ease the nerves: what HO3 will do afterwards; what he himself now is.',
    ])
    s += H('The fight', '战斗')
    s += P('<b>HO1 on the water</b>: through the fog, two spine attacks before mid-river (the boatman dodges automatically). Then in the boat\'s light HO1 and the boatman see Gla\'aki: <b>SAN 1D3/1D20</b>; HO1 does not go mad (for the story\'s sake).')
    s += R('As on the night you first tried to leave, a leaf of a boat slides out over the heaving Han. The fog swallows everything; under the water, a muffled roaring. Thin quick shadows flick beneath the surface and in a blink break it, driving at the boat. The boatman leans on his pole, the hull swings, and two spines miss. Then something vast rises slowly under the water: an oval, slug-like body bristling with metallic spines that throw back colours like oil on water; one end foul as a catfish, porous and unclean; three eye-stalks growing from its head with huge eyeballs at their ends; under its belly hundreds of pale short feet, working. And beside your boat one spine waits.')
    s += UL([
      'One spine in the river each round, DEX order. HO1 in the boat: the spine attacks the boat (boatman rolls ' + ROLL('Boat') + '; <b>boat HP 20</b>, sunk at 0). HO1 in the air (Fire-Cloak): 1D2 for the target. <b>Cutting off a spine</b>: Gla\'aki cannot attack with one next round, and <b>loses 8 HP per spine</b>.',
      'Each round HO1 either <b>signals</b> (fire; gunpowder needs ' + ROLL('Luck') + ' in the wet fog; the Fire-Cloak makes HO1 the beacon) or attacks the spine.',
      '<b>HO2 at the tower\'s foot</b>: each round ' + ROLL('1D3+2') + ' Undying come, in monster form (SAN 1/1D8 first sight, 1/1D4 if seen before). HO2 acts first: ' + ROLL('DEX') + ' — fail / success / Extreme / critical = 1 / 2 / 3 / 4 actions; each action an ' + ROLL('Acupoint Strike') + ' (+10% with the needles) that <b>kills one Undying outright</b>. Other wanderers can hold Servants but not kill them (they do not know the spot, or cannot hit it); blocked and unkilled Servants carry to the next round; unblocked ones attack HO2.',
      '<b>HO3 on the tower</b>: may shoot only in a round HO1 signals: ' + ROLL('Bow') + ' at Gla\'aki; the fire shows only a rough position, so Liu ' + ROLL('Spot Hidden') + ' for the water — success gives HO3 a bonus die. HO3 is nearest the Dream-Call: ' + ROLL('POW') + ' every three rounds, fail = temporary insanity.',
    ])
    s += GM('Gla\'aki: give it about 40–60 HP for the table (each severed spine −8; each God-Arm arrow 1D8+2 with a Hard success doubling). It is a long way off: without the bow nothing on the bank reaches it. Spine: HP 10 (shared with the body), DEX 50, attack 40, 2+1D5, armour 4; fire ignores the armour.')
    s += P('<b>At 0 HP</b>: from the boat HO1 watches the fluids drain from the body and the husk crumble to dust; HO3 feels the calling that has been in his head for a week stop; every Servant at HO2\'s feet turns and leaves. The fog lifts from the river, and across the water Southbright stands clear.')
    return s

# ---------------------------------------------------------------- 9. OPTIONAL & PERSONAL EVENTS
def optional_html():
    s = H('Optional and personal events', '可选事件 · 个人事件', 1)
    s += H('Chance encounters (any street, any day)', '可选事件')
    s += UL([
      '<b>An old friend of medicine 岐黄旧识</b>: the first meeting with Doctor Yue, anywhere on Front/Back Street or the Crossing except the Theatre and Temple. He checks HO2 first (pulse, tongue, breath: "white coat, floating tight pulse, wind in the body — drink hot water"), then reads the others\' faces ("full brow but dark between the eyes — a hard road"; "noble bearing hiding decline — a pearl in dust"). While talking he picks one small item from a PC other than HO2: secret opposed ' + ROLL('Sleight of Hand 75 vs Spot Hidden') + '; success, the item is gone; failure, he apologises frankly ("checking who you are, for HO2\'s sake"). Either way he gives it to HO2 that night to return.',
      '<b>A stumbling horse 当道踬马</b>: Duan rides by with four or five men. If Yue is present he passes and dusts Duan\'s horse: it drops, vomiting and convulsing, and Duan goes over its head. Watch, or help: ' + ROLL('Medicine') + ' sees poison, Spot Hidden the powder in the mane; helping earns a favour; the bold can lift a token from Duan or his men — found out, he lets it go for HO1\'s sake.',
      '<b>A chance meeting over books 素书偶逢</b>: Magistrate Fan at the book stall or the Library; learned, happy to discuss, dropping hints; on the war he is iron-hard and unyielding — the opposite of the man who opened the gates. He pretends not to know HO3; named, he glosses over it.',
      '<b>The dead speak 尸假人言</b>: at night an Undying poses as someone asking help or directions and strikes; unwary targets give it a bonus die. Use anywhere at night to block, harden or tighten.',
      '<b>Riding you down 当途据鞍</b>: Toghan, going to or from Wang Wu\'s, recognises HO2 and rides straight at her, insulting her and her father in broken Chinese, describing his death. ' + ROLL('DEX') + ' or 1D3 under the hooves. Pick his or his men\'s pockets (tokens, the banquet note). If the party swallows it he leaves for his camp rounds; at drawn steel Duan may intervene; Toghan despises him but gives way.',
    ])
    s += H('HO1: the empty tomb', '先人衣冠')
    s += P('Asked about the Hermit\'s effects, Duan says he raised a cenotaph for him on the riverbank; the body Ashu threw to the dogs, the effects Duan gathered quietly and kept untouched. He will take HO1 alone, that night, with a jug of good wine. A stone with the name and dates, a few incense sticks and cold ash; a few steps off, the Han rolls east. Duan pours cold wine, then takes a wooden box from behind the stone: <b>a leather scabbard and a few ancient pages</b> protected between silk gauze with starch paste, the writing almost gone. Hard ' + ROLL('Spot Hidden / Library Use') + ' (or a whole round) reads a spell for walking on clouds wrapped in starfire — Red Pine\'s going and coming as he pleased. Learning it needs an ' + ROLL('Idea') + ' roll.')
    s += GM('<b>Fire-Cloak 火焰斗篷术</b> (Grand Grimoire p. 66): 12 MP, 1D6 SAN, 1 round to cast, lasts 4D4 rounds. Wrapped in white-hot light: flight; a bonus die to Dodge, DEX and melee; melee hits add a stacking burn, 1D3 per stack per round. Cost: 1D3 damage to the caster each round until 0 HP, and 1D6 extra SAN for the agony; all attacks on the caster take a penalty die; bare-handed attackers take 1D6 per hit. Seeing it: SAN 1/1D3. The Hermit never believed the legend and never read the pages.')
    s += P('Duan keeps urging HO1 to work with the Mongols to kill the river monster: his awkward position in the army, then a promise of safety for all the party; the answer changes nothing afterwards: "If it were only the crossing, for old times\' sake of course I would help. But the thing in the river threatens my army too — in a few days I lead the vanguard against Southbright, and one slip is a court-martial. Let us finish the monster together. You think stopping the army stops the Marshal? Without killing the monster, crossing means speed and luck, nine deaths in ten. You would dare it; I cannot rest easy." Let the players see it: killing Gla\'aki also lets the Mongols cross — the Fan uncle and nephew knew that.')
    s += H('HO3: the dreams and the Rashomon alley', '梦引 · 罗生门巷')
    s += P('<b>Night of the 11th</b>: a familiar voice calls HO3\'s name in sleep; ' + ROLL('POW') + ', fail: waves, snapping timbers, screams, SAN 1/1D3. <b>Night of the 12th</b>: the second Dream-Call draws HO3 alone to the bank with a false light (full text in the Session 0 runbook, Extended Day One): the dream of the boat breaking and a spine through the chest, SAN 1/1D3; POW, fail and HO3 is waist-deep following a light; the spine strikes from behind (Dodge, or 1D3); Liu appears, throws a rusty sword, fights the spine (HP 10, DEX 50, 40, 2+1D5) and joins for good.')
    s += P('<b>The Rashomon alley 罗生门巷</b>: the Undying are ordered to kill the one who took the gift and escaped — Liu. Chen 陈寻忠 arranges to meet Liu at night at the Street Crossing; if not invited along, Liu goes alone and reports afterwards. With HO3 present: a dark, cold, empty crossing. Chen reminisces and tells half-truths: the Fan uncle and nephew caused the horrors and have locked their drowned comrades in the temple\'s back hall — bait to draw Liu there for a mob attack. "My lord, you are thinner than in Lin\'an. You were the emperor\'s favourite then; to see you brought to this breaks my heart." "That storm mid-river was no act of heaven but the Fans\' sorcery. The water looked calm — even young General Liu was fooled — but the centre was bottomless and bubbleless, so I knew. The boatmen were their men. At mid-river fog and rain and a green light in the clouds, and the boats went over in an instant. I clung to a gunwale; our brothers sank like posts. At dawn I washed ashore and saw cage carts take our comrades into the temple\'s back hall. The Fans have called on some evil god — this Chu country loves human sacrifice; our men will feed the shamans!" Liu is furious and ashamed; Chen proposes rescuing the soldiers tomorrow night (uses the night). If HO3 wants the others along, Chen demurs (' + ROLL('Psychology') + ' sees another purpose): "the jianghu is full of schemers; what if they tell the Mongols?" He glances towards Back Street and hurries off; a watchman boy comes by — Nameless Fang, if met, recognises Chen as the thief he chased into the restaurant, whose owner would not believe him and made him pay for the broken tables.')
    return s

# ---------------------------------------------------------------- 10. ENDINGS
def endings_html():
    s = H('Endings', '结局', 1)
    s += H('1 · "Rise and fall are the work of men; the mountains and rivers are only a shape" 兴废由人事，山川空地形', '')
    s += P('<i>Stopped the crossing, dispelled Gla\'aki, crossed.</i> If Ashu is dead: Kublai has lost his right arm and the army its invincible general; a great man dead at a nobody\'s hand, as in a hundred histories — honour, or arrogance? Cold water on the fire of conquest: smoke everywhere, the fire not out. If the ships are sunk: horsemen who would walk on water need something to carry them; the ships lie on the bottom with their enemies, and it will take years, and the bones of more slaves and prisoners, to build again. Either way the Song court is not yet on fire: the people can pay a few more years of taxes, the ministers hear a few more years of songs, the city commanders send a few more letters asking for relief that never comes. The Han is quiet; the faithful servants who walked the night are gone. The goddess of the Han was a legend; perhaps once she was real, but the age of the sage-kings is long over — if goddesses could save dynasties, why did Xia fall to Shang and Han to Tang? Southbright rejoices. Its commander Lü Wenhuan 吕文焕 sends up a memorial for your honours and plans a stele on the bank for the fallen. HO1 and the Hermit go into the town\'s storytellers\' best tale; HO2\'s pharmacy is famous — "its medicine raises the dead and kills without a trace"; HO3 and Liu are pardoned for the failed relief. Ten thousand miles of road ahead, and nothing left in the world that can stop you like the Han did.')
    s += H('2 · "The old owl becomes a tree-spirit; laughter and green fire rise from the nest" 百年老鸮成木魅，笑声碧火巢中起', '')
    s += P('<i>Gla\'aki not dispelled; the party crossed (by the reeds, or otherwise).</i> Whatever the party did, the Mongols cannot cross while it lives. They never guess what lies under the Han; some smell danger and most pretend not to. The goddess\'s majesty means nothing to men who fear no Chinese god and have always taken victory with their hands; so she accepts the feast, and the living and the dead become her strength. She puts no rope on the people and makes no slaves, but she is a far worse enemy than the invaders. Across the water Southbright lives through something more dangerous than a siege: Lü Wenhuan does not even know where the enemy is. Every night townsfolk walk into the Han and are taken, and come back next day unharmed; the legend of the goddess rises again and almost everyone prays to her to carry the Song through. Apart from Fan in his grave, you alone know. Tell Lü Wenhuan? Another scholar-official — who says he would not think as the Fans did? Or keep silent and leave Southbright by night. It does not matter: south of the Central Plains the Song is still bright and beautiful.')
    s += H('3 · "Human affairs change; coming and going make the past and present" 人事有代谢，往来成古今', '')
    s += P('<i>Gla\'aki dispelled, crossing not stopped; the party crossed.</i> Everything returns to its track; the fog might never have been. When the Mongol banners fly over the Han, all the rise and fall that follows is natural. Lü Wenhuan hears of Fan\'s death and surrenders in three days, opening the broad road into the heartland. Within three years the Mongols are at Lin\'an; the emperor and the empress dowager surrender; the Southern Song is gone. You are not surprised: what wound of the Central Plains did not tell you the Song was doomed? For the people, rise and fall are both misery; for the great, a new set of winners at the table; for you, the road that had to be chosen.')
    s += H('Personal endings', '个人结局')
    s += UL([
      '<b>HO1</b> may wander on; with his skill he could serve anyone, even Kublai. Duan has no wish to hold office again, and his credit is nearly spent; if allowed, he follows HO1.',
      '<b>HO2</b>\'s house is famous; inherit and build it, or scatter the fortune on the resistance — HO2 decides how. Doctor Yue goes on robbing the rich for the poor, and gladly minds the pharmacy\'s affairs for HO2.',
      '<b>HO3</b>, without a deed to show in Fencewall, may face charges in Lin\'an, though the family can probably bury it; a rich idler, or an official trying to save the broken machine. Liu goes on fighting at the front; whatever HO3 chooses, Liu is HO3\'s truest friend.',
    ])
    return s

# ---------------------------------------------------------------- 11. NPC STATS (campaign)
def npcs_html():
    s = H('Campaign NPC reference', '人物速查（全剧本）', 1)
    s += table(['NPC', 'Stats', 'Notes'], [
      ('<b>Magistrate Fan 范玉楼</b>', 'STR 40 DEX 50 POW 60 CON 45 APP 70 EDU 75 SIZ 60 INT 75 · HP 10 · Dodge 40, Listen 50, Spot 50, Library 70', 'Raised by his uncle; met HO3 once in the capital and admires him (one reason he never hands the party to the Mongols). Knows gods are no long-term plan; asks for the assassination. Usually at the Magistracy; sometimes at the book stall.'),
      ('<b>Prefect Xu 许德显</b>', 'ordinary, fat', 'Runs the treasury; corrupt; two-faced and cowardly; his surrender letter was intercepted by Yue. Has painted barges, skiffs, gunpowder, gaol access.'),
      ('<b>Fan Yuying 范玉莹</b>', 'ordinary', 'The Commander\'s daughter, kept by Ashu; blocks one blow and passes HO2 a dagger.'),
      ('<b>Du Guanshan 杜观山</b>', 'STR 55 DEX 60 · HP 13 · Blade 65, Dodge 60, Listen 50, Spot 50, Jump 50', 'Wineshop owner; knows the town; proposes the Jiangzhou-style rescue.'),
      ('<b>Nameless Fang 方未名</b>', 'STR 70 DEX 70 POW 70 · HP 11 DB +1D4 · Mallet 75, Dodge 70, Climb 70, Listen 50, Spot 60', 'Night watchman boy; blunt, pure, enormously strong. Carries the God-Arm Bow wrapped in cloth. Killed four gaol guards with his mallet.'),
      ('<b>Ling Xuchun 凌序春</b>', 'STR 65 DEX 70 · HP 12 DB +1D4 · Sabre 70, Dodge 70, Spot 65, Climb 60, Swim 60', 'Hot-tempered, hates evil; makes a scene at the pharmacy; calls the party "benefactors" once her brother is cured.'),
      ('<b>Ling Daiqiu 凌代秋</b>', 'STR 60 DEX 60 · HP 13 DB +1D4 · Dodge 50, Swim 75, Boat 70', 'Fishermen\'s leader; took Autumn in and was Green-Rotted; cured when she dies.'),
      ('<b>Wang Wu 王五条</b>', 'STR 50 DEX 60 · HP 12 · Staff 65, Dodge 55', 'Restaurant owner; old friend of Fan; knows the plan; shelters Chen out of guilt; hates the Mongols; may owe HO2\'s family.'),
      ('<b>Song Zeyi 宋择一</b>', 'STR 45 DEX 50 · HP 11 · Throw 70, Jump 70, Dodge 45', 'Tea master; helped Fan collect the sacrifices and hides it; despises Yue\'s methods; takes no part against Gla\'aki.'),
      ('<b>Autumn 秋筠</b>', 'STR 60 DEX 70 POW 60 CON 65 APP 70 · HP 12 · Sword 70, Dodge 65, Jump 65, Disguise 70', 'Outlaw of a thousand faces; sacrificed by Fan; Undying; stole the Ling needles; Green Rot on Ling Daiqiu; hides at the Li Theatre.'),
      ('<b>Chen Xunzhong 陈寻忠</b>', 'use the Undying Servant', 'Liu\'s standard-bearer; Undying; sheltered by Wang Wu; poisons Liu\'s noodles; lures him to the Temple.'),
      ('<b>Huaide the monk 怀德和尚</b>', 'as Du; armour 2; Iron Shirt', 'Pagoda Arhat; drinking contest for the golden kasaya (armour 2, fire-immune); comes to the Temple fight if told.'),
      ('<b>The scholars 儒生</b>', 'ordinary', 'Kong Liyue, Zhou Wentong and the rest: hot-blooded, useless in a fight, easily roused; Fan\'s diversion at the assassination.'),
      ('<b>Gla\'aki 格拉基</b>', 'spines HP 10 (shared), DEX 50, attack 40, 2+1D5, armour 4; body ~40–60 HP for the table; −8 per severed spine', 'The thing in the river; fog; Dream-Call; fears fire and light; the dead it pierces walk again.'),
    ])
    return s

# ---------------------------------------------------------------- PLAYER: RULES CARDS & HANDOUTS
def rules_cards_html():
    s = H('Set-piece rules', '规则卡', 1)
    s += P('The book shows these two cards to the players before the scene.')
    s += H('The rescue of General Niu (15 January, noon)', '劫法场')
    s += CARD(UL([
      'You command every friendly wanderer except Nameless Fang; the GM rolls for them.',
      'Your side acts, then the soldiers. No DEX order. Soldiers go for whoever is nearest the carts.',
      '<b>Five rounds</b>, then Mongol reinforcements arrive. Leave with Niu = win.',
      'Stop the road: topple a painted gate-tower, or kill the cart horses.',
      'Anyone up in a gallery can shoot at any target with any ranged skill; a miss may hit a friend or a bystander.',
      'Closing with a horseman or a cart horse: DEX (or Dodge) and your fighting skill together; fail and a hoof does 2+1D3.',
      'One round to reach a cart; one round and STR or Locksmith to open it. Three shackled prisoners per cart; one person carries one prisoner. Only Fang knows Niu\'s face.',
      'Leaving: ranged fighters get away free; melee fighters roll DEX, and if they fail a wanderer covers them and dies. On a horse: bonus die. Carrying a prisoner: penalty die.',
    ]))
    s += H('The Watchtower (the last night)', '塔楼')
    s += CARD(UL([
      '<b>The Wanderer</b> goes out on the river with the boatman to draw the thing up, and shows the bank where it is with fire. Bring a boat, a boatman and a way to make light. Each round: signal, or attack the spine. Gunpowder may be too damp (Luck).',
      '<b>The Merchant Heir</b> holds the foot of the tower against the Undying; other wanderers may help; Doctor Yue will not be there. She acts first each round: DEX — fail / success / Extreme / critical = 1 / 2 / 3 / 4 actions; each action is an Acupoint Strike (+10% with the Ling needles) that kills one of them outright.',
      '<b>The Commissioner</b> shoots from the top of the tower with a bow that can reach mid-river, only in a round the Wanderer signals. Captain Liu watches the water: if he spots it, bonus die.',
      'The tower is 50 m of timber: CON to climb. Two guards below, one above.',
    ]))
    return s

HANDOUTS = []  # (page name, html): one journal page per handout so the GM can Show Players one at a time
def _hd(name, html): HANDOUTS.append((name, html))
_hd("许德显的两封信 Prefect Xu\\'s two letters (from Doctor Yue)", H("Prefect Xu\\'s two letters (from Doctor Yue)", '许德显的两封信', 1) + R('<b>To the Mongol camp</b>: "…your servant Xu, prefect of this circuit, has long admired the Great Khan\'s virtue and the Marshal\'s might… the city cannot stand; I beg to be of use when the gates open. My household keeps three painted barges and five skiffs, which I offer with both hands…"') + R('<b>To Governor Lü Wenhuan at Southbright</b>: "…every word written in blood… my loyalty to the Song could be cut open and shown to the sun and moon… if the city falls I will die with it, and ask only that Your Excellency remember a faithful servant…"'))
_hd("陈阳山的信 The Hermit\\'s letter (Duan\\'s room)", H("The Hermit\\'s letter (Duan\\'s room)", '陈阳山的信', 1) + R('"You urged me more than once to leave Mount Crag. I know the times are bad and that going is best, but I am old and cannot bear the road, and my pupil is in a den of wolves — how could I leave alone? If HO1 succeeds, the name will be known under heaven and written in the histories; if not, I beg you, for the sake of old days, to save a life. I enclose what remains of Red Pine as payment. The cliff is high and the road long; take care of yourself." — Chen Yangshan 陈阳山'))
_hd("脱欢的短讯 Toghan\\'s note (Duan\\'s room)", H("Toghan\\'s note (Duan\\'s room)", '脱欢的短讯', 1) + R('"The Marshal feasts the three armies at the Magistracy; fed and watered, we take the city the day after. Wang Wu\'s restaurant in Fencewall will feed the men left on the warships: ten oxen, eight sheep, thirty fowl each, fifteen jars of old wine, delivered by the restaurant\'s own people on the evening of the 17th. The men on the ships are few; stay alert; let no rogue slip in among them. General Duan will see to it."'))
_hd("樊城襄阳布防图 The defence map (Duan\\'s room)", H("The defence map (Duan\\'s room)", '樊城襄阳布防图', 1) + P('Both banks, garrisons and places of note. The tower on the Fencewall bank is marked separately, with a note in small characters: "Fine view: boats in the river and the movements of the Southbright garrison all in sight."'))
_hd('两张古方 Two old recipes (the pharmacy)', H('Two old recipes (the pharmacy)', '两张古方', 1) + P('<b>牵机药 Bowstring</b>: from ripe strychnine seeds; very bitter, a peculiar scent. After a quarter hour the muscles tighten and the mind grows anxious; after half an hour the back arches until head meets heels and the face is locked in a grin; fully conscious throughout; death by suffocation in about an hour.<br><b>十香软经散 Ten-Scent Powder</b>: ten spices with datura and 软骨草; a white powder without colour or smell. Instant: the whole body goes slack and cannot move; after some days the martial skill is gone for good.'))
_hd("绿腐 Green Rot (Autumn\\'s room)", H("Green Rot (Autumn\\'s room)", '绿腐', 1) + R('"…chant the sutra, and give the cursed one a fresh green leaf. For seven days the organs rot within, until what is left is a heap of green mould. There is one release only: the death of the one who cast it."'))
_hd("游记 The traveller\\'s record (Fan\\'s study)", H("The traveller\\'s record (Fan\\'s study)", '游记', 1) + R('"Beside Mount Qiao, in the waters of the Qiao, lives a great fish called He Luo 何罗: one head and ten bodies, like hundreds of fish twined together, turning and turning without rest. I had thought it lived only in the Qiao; but when I was banished to Tanzhou, people near Lake Dongting had seen it. They told me that whenever He Luo appears a great fog rises over the lake, and no boat can pass."'))
_hd("案头的诗 The poem on the desk (Fan\\'s study)", H("The poem on the desk (Fan\\'s study)", '案头的诗', 1) + R('Dawn on the Jingzhou road, night on the dyke of Lake Tai. / The lake ten thousand acres; waves rolling a thousand years. / Cold moon, heavy frost; a crow cries, breaking sleep. / I walk in moonlight to find the tide and lightly leave the world. / Riding cloud and coloured mist, bending light to blue smoke, / the goddess lays a hand on my head; her attendants laugh. / Silk of every colour; wine poured for a feast. / Lucky to see this; joy at its height. / A cold wind rises; I wake as from lightning, / a lifetime away, standing by Lake Tai, / and hear a voice calling me, calling, so sad. / I dare not stay, and write this of the night.'))
_hd("棺中残页 The torn pages (Fan\\'s coffin)", H("The torn pages (Fan\\'s coffin)", '棺中残页', 1) + R('"Who eats the flesh of the He Luo fish has his marrow washed and his sinews changed, his spine drawn out; a web of fine lines grows on his back. He needs no grain, but cannot bear the sun, and hides by day to walk at night. All who eat it learn the art called Green Rot… To end the art, end the man; there is no other way…"') + R('"The He Luo fish shuns light and heat and fears fire more than tigers; so do those who have eaten it, the one like lips to the other\'s teeth… It lies on the river-bed and does not rise unless a boat passes over…"'))
_hd('书摊 From the book stall', H('From the book stall', '书摊', 1) + R('<b>The Lost Pendant 遗佩情事</b>: Zheng Jiaofu 郑交甫 of Jin met the two jewelled daughters of the Han on its bank, lost his heart, and begged their pendants with a poem. When the goddesses had gone the pendants vanished from his hands. "The spirit-consort, lovely and free, seen at times on the river\'s brink; fine robes, light steps, a glance that gives grace. Jiaofu met her and spoke his private heart; the ringing pendant thrown away, her shadow gone past following."') + R('<b>The Rain Master 雨师记</b>: Red Pine 赤松子, first of the ten immortals of old, Rain Master to the Divine Farmer; he walked into fire unburnt and rose and fell with wind and rain… One day he played chess in the mountains with his elder brother Red Beard; a woodcutter set down his axe to watch. Red Pine had him hold a date-stone in his mouth, and his hunger and thirst were gone. When the game ended and the woodcutter stooped for his load, the axe-handle had rotted away.'))
_hd('藏书阁 From the Library', H('From the Library', '藏书阁', 1) + R('<b>A physician\'s notes on Rainmaster\'s Ink</b>: the wound festers and gives off a sick damp stench; the pulse clogs; the blood runs backward. Deep poisoning festers over the whole body; shallow poisoning festers for months or a year, then re-opens in every spell of rain.') + R('<b>The Lady of the Han, another version</b>: Zheng Jiaofu met the goddess of the Han, liked her looks, spoke rudely, and asked her pendant as a betrothal gift. She hid her anger and untied it, and named a midnight meeting. He went and found no beauty: a starving wolf five feet long stood in the way and ate him whole, leaving only the pendant on the bank, which it could not chew. The place is called the Lost Pendant Shoal.') + R('<b>Annotated Records of the Three Kingdoms</b>: Guan Yu attacked Fencewall when the Han flooded, drowned the seven armies and shook the empire; then Sun Quan broke faith, Lü Meng took Jiangling, Guan Yu\'s men scattered, and he was taken and killed at Linju.'))
_hd('三惑迷津 The three temptations (the reeds)', H('The three temptations (the reeds)', '三惑迷津', 1) + R('<b>The River Lord</b>: "I am He Bo 冯夷, and I fish here for all the world. I waited five hundred years for the first fish and three hundred for the second. When the fish bites, white waves stand like mountains and the sea shakes with a sound like gods and ghosts, dread for a thousand miles. I give the fish to the people of both banks and they are not hungry for a year… Good, good. The dust of the world is all entanglement; better to be an idle guest. Friends, will you fish here with me? One fish is a hundred years; one feeds both banks."') + R('<b>The goddess</b>: "I was a maid of Eastern Ou given to King Zhao of Zhou, and sailed the river with him. The men of Chu plotted; the boat sank mid-river, the king drowned, and I and my sisters followed him into the water. The world calls us loyal and chaste — but do you know what lies on the bed of the Han? Ghosts, and horned dragons, waiting to gnaw my flesh. That is the price of loyalty… The Song\'s number is up; how long will the Yuan last? Drift with me on the river, free."') + R('<b>The Many-Headed Fish</b>: a fish with one head and ten bodies rises from the boiling river, crying like a bird, clear and long; the ten bodies swim ten ways and the whole Han shakes — the very He Luo of the Classic of Mountains and Seas.'))

# ---------------------------------------------------------------- NPC DOSSIER (look · background · events with book pages · role)
# Book pages are the printed numbers on the scenario PDF (江涔《公若渡河》0508); journal = page of this module to open.
DOSSIER = [
 ("The investigators' linked NPCs · 关联人物", [
  ('duan.webp', 'Duan Driftwood 段游衍', 'HO1\'s old classmate',
   'HO1\'s age; handsome (APP 70), well-spoken, dressed in Ashu\'s gifts; rides with four or five men. Smooth, pleasant, a coward who knows it.',
   'Of the Dali 段 clan; came over to the Song with his father, then to the Mongols when they invaded. Studied a year under the Hermit, who liked his mind and distrusted his heart. Ashu values his generalship and has made him vanguard commander for the crossing; the Mongol officers (Toghan above all) resent him. Loyal to no dynasty, tired of office, in love with the idea of the jianghu, and quietly in awe of HO1.',
   [('Session 0', 'Banquet: covers HO1\'s escape; North Gate: speaks for Toghan', 'p.11–13 · Session 0 runbook'),
    ('Any day', 'Rides past the Teahouse brawl and ends it ("The Mongols\' general")', 'p.21 · Front Street'),
    ('Back Street', 'His room at the Guildhall: the Hermit\'s letter, Toghan\'s note, the defence map', 'p.26 · Back Street'),
    ('Any street', '"A stumbling horse": Yue poisons his horse; tokens can be lifted', 'p.42 · Optional'),
    ('HO1 night', '"The empty tomb": the Hermit\'s cenotaph, the Fire-Cloak pages; urges HO1 to kill the monster with the Mongols', 'p.44 · Optional'),
    ('Finale', 'Waits in the reeds to be bait with HO1; can hand over the golden kasaya', 'p.40 · Finale'),
    ('Raid', 'Executed under military law if a ship guard escapes to raise the alarm', 'p.37 · Riverbank')],
   'The party\'s inside man and HO1\'s mirror: he shows the players that the Mongols also want the monster gone, and so that killing Gla\'aki opens the river to them. His letter and map hand over the raid date and the Watchtower. Ending: follows HO1 if allowed.'),
  ('yue.webp', 'Doctor Yue 越南柯, the Hollow Physician', 'HO2\'s foster brother',
   'Three years older than HO2; handsome (APP 75), charming, hands like a conjurer\'s, a medicine chest full of beautifully packaged fakes.',
   'Orphaned, raised by HO2\'s father; left the pharmacy for the road. Cannot fight, cannot heal; sells fake elixirs to the rich, steals from them, gives to the poor — the jianghu calls him 空空郎中. In Fencewall he blackmailed Prefect Xu and took his surrender letter, dodged Commander Fan\'s arrests, and on 3 January blundered into Fan\'s rite at the Pavilion, firing it early into Liu\'s flotilla. He has told no one and is eaten by guilt.',
   [('11 Jan', 'Sent the Jiangs and Winding Stream to the bank; left the ginger "candy"', 'p.15 · Session 0 runbook'),
    ('12 Jan evening', 'At the coffin shop with Xu\'s two letters; hints at the gazetteer and the scarred woman', 'p.22 · Front Street'),
    ('Any day', '"An old friend of medicine": checks HO2, reads faces, pickpockets a PC to vet them', 'p.42 · Optional'),
    ('Any street', 'Poisons Duan\'s horse', 'p.42 · Optional'),
    ('Assassination', 'Volunteers as Ashu\'s hostage; held in an empty house; burns himself unless rescued', 'p.32–33 · Magistracy quarter'),
    ('Finale', 'Walks HO2 to the tower and confesses the rite', 'p.40 · Finale')],
   'The hint-giver when the table stalls, and the cause of the catastrophe. His letters are the lever for Xu\'s boats; his confession gives the finale its weight for HO2. Ending: keeps robbing the rich; minds the pharmacy for HO2.'),
  ('liu.webp', 'Captain Liu 刘卿堂', 'HO3\'s oldest friend',
   'HO3\'s age; a general\'s son, strong (STR 70), open-faced, hot-blooded; an axe man. Since the 3rd: no pulse, a bruised wound on his back under a red web of lines, poison and sickness roll off him.',
   'Military family of the capital, childhood friend of HO3; volunteered to lead HO3\'s five thousand, lost most of them, held Fencewall with eight hundred, and took them across the river on Fan\'s order on 3 January — straight into the rite. Drowned, came back with his own mind, was pulled out by fishermen. Remembers nothing clear; when he learns the truth he blames himself.',
   [('12 Jan night', 'Appears at the bank, throws HO3 a rusty sword, fights the spine, joins', 'p.45 · Optional'),
    ('From the 13th', 'Travels with HO3; advises on tactics', 'p.50 · NPCs'),
    ('Restaurant', '"Is this food poisoned?": vomits blood over noodles; Chen kneels to him', 'p.19 · Front Street'),
    ('Night', 'The Rashomon alley: Chen\'s half-truths; agrees to the temple', 'p.45–46 · Optional'),
    ('Temple', 'Ambushed in the dark side hall; learns what he is', 'p.29 · Temple'),
    ('Undying house', 'First target of the girl and her brother', 'p.23 · Front Street'),
    ('Raid', 'Drives the carts from ship to ship', 'p.37 · Riverbank'),
    ('Mourning hall', 'Rages at Magistrate Fan over his drowned men', 'p.31 · Magistracy quarter'),
    ('Finale', 'On the tower with HO3; Spot Hidden for the bonus die', 'p.40–41 · Finale')],
   'The walking proof of what is in the river, and the Undying\'s number-one target — which is why Chen, the Undying house and the temple ambush all exist. Ending: back to the front; always HO3\'s friend.'),
 ]),
 ("The Mongols · 蒙古", [
  ('ashu.webp', 'Marshal Ashu 兀良哈·阿术', 'Commander-in-chief',
   'Over six feet, heavy, bearded, felt hat and soft armour, an eight-foot sabre; left-handed since the banquet. STR 80 CON 80 SIZ 85 · HP 16.',
   'Kublai\'s most trusted general, undefeated in the Central Plains; took Fencewall in three days, forbids looting, modest with his officers and arrogant with the Song. Stillwater\'s Rainmaster\'s Ink has given him a wound that will not heal (penalty die on everything); he is hunting a cure.',
   [('Session 0', 'The banquet: HO1 cuts his shoulder', 'p.11–12 · Session 0 runbook'),
    ('12 Jan', 'Has the Hermit killed and hung at the Street Crossing', 'p.28 · Street Crossing'),
    ('Gaol', 'Comes out of the deep cells with Magistrate Fan, talking of Niu\'s execution; smells of herbs', 'p.35 · Magistracy quarter'),
    ('15 Jan', 'Orders Niu beheaded', 'p.28 · Street Crossing'),
    ('17 Jan', 'Feasts the army before the crossing (the raid\'s window)', 'p.26, 36 · Back Street, Riverbank'),
    ('Assassination', 'The sickroom: talks, suspects, takes a hostage, fights off-hand at −20', 'p.32–34 · Magistracy quarter')],
   'The unbeatable antagonist and the clock: the crossing happens when he says. His death is one of the two ways to stop the crossing (Ending 1) and the trigger for the lockdown and the finale.'),
  ('toghan.webp', 'General Toghan 兀良哈·脱欢', 'Ashu\'s deputy',
   'Big (SIZ 80), violent, moody, bad Chinese; two guards who taste his food. HP 15.',
   'Ashu\'s kinsman and right hand, trusted with his life; despises Duan the smooth-talker. Killed HO2\'s father on the road. Loves Wang Wu\'s cooking and eats there every noon in the best upstairs room.',
   [('Session 0', 'Stops the convoy; HO2\'s father beheaded', 'p.12–13 · Session 0 runbook'),
    ('Daily noon', 'Wang Wu\'s restaurant, second floor, third room', 'p.18 · Front Street'),
    ('Back Street', 'His note to Duan sets the feast and the delivery of the 17th', 'p.26 · Back Street'),
    ('Any street', '"Riding you down": rides at HO2, mocks her father', 'p.42–43 · Optional'),
    ('HO2\'s choice', '"Blood debt": poisoned in his room (牵机药 / 十香软经散)', 'p.43 · Front Street'),
    ('Assassination', 'His relief kills everyone after five rounds', 'p.33 · Magistracy quarter')],
   'HO2\'s personal revenge, and a fork: kill him at the restaurant and Wang Wu will not open the door to the warship raid.'),
 ]),
 ("The Song · 宋", [
  ('', 'Commander Fan 范天顺', 'The dead commander of Fencewall',
   'Dead. A scholar-official\'s study (no weapon rack, two full bookcases); a plain black coffin, empty.',
   'Loved by the people, severe with wrongdoers (executed a man for a few taels of lamp oil). Knew Fencewall could not hold; in 1266 bought the Grand Lake Stone with Gla\'aki\'s shard from Seven Treasures, set it in the Pavilion, filled the death cells with petty criminals as sacrifices (Song and Wang Wu helped), and on 3 January summoned the thing to block the crossing. Yue\'s blunder fired it early into Liu\'s boats. Hanged himself that night and left the plan to his nephew.',
   [('Backstory', 'The stone, the rite, the flotilla', 'p.4–5, 51 · The whole story'),
    ('Front Street', 'Winding Stream made his coffin, with a compartment', 'p.22 · Front Street'),
    ('Magistracy', 'Study: the traveller\'s record, the Tang poem; mourning hall: the torn pages in the coffin', 'p.30 · Magistracy quarter'),
    ('Riverbank', 'The Pavilion: the stone and the sacrificed prisoners', 'p.38 · Riverbank'),
    ('Teahouse / fishermen / Wang Wu', 'Everyone has a piece of what he did', 'p.21, 36, 19 · Front Street, Riverbank')],
   'The absent author of the whole horror: a patriot who chose the dynasty\'s honour over the people\'s lives. His books and coffin are the main clue trail to the weakness of the Undying.'),
  ('fan_yulou.webp', 'Magistrate Fan 范玉楼', 'The nephew who opened the gates',
   'Late twenties, pale, refined, intelligent, tired (APP 70, EDU 75, Library 70). HP 10.',
   'Raised by his uncle; met HO3 once in the capital and admires him. Surrendered the city to save it and now flatters Ashu — but on the war he is iron. Knows gods are no long-term plan, so he wants Ashu dead by the party\'s hand, and will rouse the scholars to make the opening.',
   [('Session 0', 'Flatters Ashu at the banquet; opens the gates on the 4th', 'p.11–12 · Session 0 runbook'),
    ('Front Street', 'Browses the book stall; "A chance meeting over books"', 'p.16, 42 · Front Street, Optional'),
    ('Mourning hall', 'Receives mourners; appears with a lantern when the coffin is opened: the assassination plan', 'p.30–31 · Magistracy quarter'),
    ('Gaol', 'Beside Ashu in the deep cells; steers him away from HO3', 'p.35 · Magistracy quarter'),
    ('Assassination', 'The scholars\' riot is his signal; beheaded afterwards, head hung on the Watchtower', 'p.33, 40 · Magistracy quarter, Finale')],
   'Turns the investigation into a plan: he gives the party the assassination and the gunpowder, and pays for it with his head.'),
  ('xu.webp', 'Prefect Xu 许德显', 'The fat prefect',
   'Fat, rich, jewelled; a shut mansion, a few maids; afraid of everything.',
   'Runs the treasury and has filled his pockets. Wrote to the Mongols offering his three painted barges and five skiffs, and to Lü Wenhuan swearing loyalty — Yue stole both letters. Has gunpowder and the keys to the gaol.',
   [('12 Jan', 'His two letters arrive via Yue', 'p.22 · Front Street; handouts'),
    ('Teahouse', 'Song mentions his barges and skiffs', 'p.21 · Front Street'),
    ('Magistracy', 'His mansion: bribe, blackmail or frighten him for boats, gunpowder, gaol access', 'p.31–32 · Magistracy quarter'),
    ('Gaol', 'His word gets the party in', 'p.35 · Magistracy quarter')],
   'The boats thread\'s easy answer and the scenario\'s portrait of the turncoat official: a boat for the finale without fighting for it.'),
  ('niu.webp', 'General Niu 牛富', 'Garrison commander, in the gaol',
   'Forties, dark, lean as a bowstring, eyes like torches; now wasted, hand-tendons cut.',
   'Fan\'s military deputy; shot Ashu\'s nephew dead before the siege. Knew Fan meant to "invite a god" but not what; refused to surrender; gaoled, to be beheaded at noon on the 15th. Gave the God-Arm Bow (400 paces, the only bow that reaches mid-river) to the watchman boy.',
   [('Session 0', 'Meets HO2 at the North Gate; promises help', 'p.12–13 · Session 0 runbook'),
    ('Teahouse', 'The story of the nephew and the bow', 'p.20 · Front Street'),
    ('Gaol', 'In the deep cells; Ashu mocks his "hard bones"', 'p.35 · Magistracy quarter'),
    ('15 Jan', 'The rescue at the Street Crossing', 'p.28–29 · Street Crossing'),
    ('After', 'Tells what he knows; has Fang hand over the bow; stays at the Wineshop', 'p.29 · Street Crossing')],
   'The gaol thread: his rescue is the set piece of the 15th and the only way to the bow the finale needs.'),
  ('yuying.webp', 'Fan Yuying 范玉莹', 'Commander Fan\'s daughter',
   'Twenty, pale, composed, resembles her cousin the Magistrate; a servant in Ashu\'s quarters.',
   'Kept by Ashu as a trophy of the Song\'s loyalty ("his daughter holds a Mongol\'s broom"). Says nothing and waits.',
   [('Assassination', 'Kneels by the bed; tastes medicine; blocks one blow; slips HO2 a dagger', 'p.32–33 · Magistracy quarter')],
   'The one ally inside the sickroom; the human cost of her father\'s choice made visible.'),
  ('hermit.webp', 'The Hermit of Mount Crag 山阳道人 (Chen Yangshan 陈阳山)', 'HO1\'s master',
   'Seventy-odd, white hair and beard, one arm, Stillwater at his shoulder.',
   'The best sword of the Jinghu country; recluse on Mount Crag; taught HO1 and, for a year, Duan. When Duan wrote urging him to leave, he chose instead to give HO1 a name in the histories: Stillwater, and Ashu. Stayed to be taken; gave Duan Red Pine\'s pages as payment for saving his pupil.',
   [('Session 0', 'Gives Stillwater and the three warnings', 'p.11 · Session 0 runbook'),
    ('12 Jan noon', 'His body on a spear at the Street Crossing', 'p.28 · Street Crossing'),
    ('Back Street', 'His letter in Duan\'s room', 'p.26 · Back Street; handouts'),
    ('HO1 night', 'The cenotaph; his effects and the Fire-Cloak pages', 'p.44 · Optional')],
   'HO1\'s motive and loss; his pages give the finale its fire signal.'),
  ('scholar.webp', 'The scholars 儒生 (Zhou Wentong 周文通, Kong Liyue 孔礼岳)', 'Students of the town school',
   'Young, thin, outspoken; Zhou gets knocked down in the teahouse; Kong is rude at the library door.',
   'Patriots with nothing to fight with; the party\'s deeds become their example and Magistrate Fan\'s kindling.',
   [('Teahouse', 'Zhou protests the soldiers and is hit', 'p.21 · Front Street'),
    ('Library', 'Kong\'s suspicion, Zhou\'s rebuke; praise for the party', 'p.34 · Magistracy quarter'),
    ('Assassination', 'Riot at Ashu\'s gate; many killed', 'p.33 · Magistracy quarter')],
   'The signal and the diversion for the assassination; the cost of Fan\'s plan in ordinary lives.'),
 ]),
 ("People of Fencewall · 樊城人", [
  ('qu.webp', 'Winding Stream 曲流', 'The coffin-maker',
   'About fifty, tall and heavy-set, a big blade on her back; gentle, serious, attentive. STR 70 · Brawl (blade) 70 · First Aid 60.',
   'Not local; came with her husband, an ex-caravan guard; they ran the coffin shop together until she caught him cheating ten years ago and killed him with one cut. Makes the best coffins in town, Commander Fan\'s included.',
   [('11 Jan', 'Pulls the party from the river with the Jiangs; shelters them', 'p.15 · Session 0 runbook'),
    ('By day', 'The shop: coffins with compartments; Fan\'s coffin; the Magistrate asked for one', 'p.22 · Front Street'),
    ('15 Jan', 'One of the rescuers Du can call on', 'p.24–25 · Front Street')],
   'The party\'s home base and the planted clue to the coffin compartment.'),
  ('jiang_tower.webp', 'The Jiang twins 姜楼 · 姜阁', 'Fishermen brothers',
   'Identical; Tower the steady elder, Loft the reckless younger; superb swimmers.',
   'Fencewall natives who know every lane and reed-bed; Yue sent them to the bank on the 11th.',
   [('11 Jan', 'Rescue at the Night Crossing; "if the thing is in the river, can the Mongols cross?"', 'p.15 · Session 0 runbook'),
    ('15 Jan', 'Rescuers for Niu', 'p.24–25 · Front Street'),
    ('Raid', 'Swimmers who hole the hulls', 'p.36–37 · Riverbank')],
   'Muscle and water-skill for the rescue and the raid; the first to say aloud that the monster blocks the Mongols too.'),
  ('boatman.webp', 'Boatman Wang 船夫王', 'The one-armed boatman',
   'Hemp and a straw hat; one arm; curses Mongols and court alike.',
   'Will row anyone for money; abandons his passengers when the boat sinks.',
   [('11 Jan', 'The Night Crossing', 'p.14–15 · Session 0 runbook')],
   'The failed first crossing that shows the party the thing in the river.'),
  ('du.webp', 'Du Guanshan 杜观山', 'Keeper of the hidden Wineshop',
   'Forties, homely, hearty, a ladle in his hand; Blade 65.',
   'Old jianghu hand who settled behind two rows of wine jars; knows the town and everyone in it; remarks that HO3 "isn\'t one of us".',
   [('Any day', 'The Wineshop: regulars, the monk\'s contest, Fang', 'p.24 · Front Street'),
    ('14 Jan', 'Proposes and draws the Jiangzhou-style rescue; fixes the time', 'p.24–25 · Front Street'),
    ('15 Jan', 'Fights in the rescue', 'p.28–29 · Street Crossing')],
   'The planner who turns the gaol thread into a workable ambush; the players\' voice of the jianghu.'),
  ('fang.webp', 'Nameless Fang 方未名', 'The night watchman',
   'Sixteen, broad, round honest face, gong and copper mallet, a cloth-wrapped bundle on his back; STR 70, Mallet 75, Climb 70.',
   'Pure, blunt, strong as an ox, bad with people; Niu\'s protégé, fed by Du, taught letters by Song. Carries Niu\'s God-Arm Bow without knowing what it is. Killed four gaol guards with his mallet looking for Niu.',
   [('Front Street', 'Chased Chen from the pharmacy into the restaurant', 'p.18 · Front Street'),
    ('Undying house', 'On the wall after the fight; examines the bodies; names the Wineshop', 'p.23–24 · Front Street'),
    ('Gaol', 'Bursts in after Ashu leaves', 'p.35 · Magistracy quarter'),
    ('Wineshop', 'Asks for the rescue; shows his bruised arm', 'p.24 · Front Street'),
    ('15 Jan', 'Only he can identify Niu\'s cart; he scouts and signals', 'p.25, 28–29 · Street Crossing'),
    ('After', 'Hands the bow to the party on Niu\'s word', 'p.29 · Street Crossing')],
   'The bearer of the bow and the key to the rescue; the kindest person in the book.'),
  ('ling_xuchun.webp', 'Ling Xuchun 凌序春', 'The swordswoman in red',
   'Nineteen, two curved sabres, a temper; Sabre 70, Dodge 70.',
   'Travelled the jianghu; came home to nurse her poisoned brother. The family heirloom — embroidery needles thin as ox-hair, hard as iron, the perfect Acupoint tool — was stolen by the woman they sheltered.',
   [('Pharmacy', '"A plea for medicine": the poison, the needles, Autumn, the reward', 'p.19 · Front Street'),
    ('Her house', 'Visiting Ling Daiqiu', 'p.19–20 · Front Street'),
    ('15 Jan', 'A rescuer ("nobody in Fencewall dares cross her")', 'p.24–25 · Front Street'),
    ('After Autumn', 'Calls the party "benefactors"; the needles are theirs', 'p.53 · NPCs')],
   'Opens the needles thread and ties the pharmacy to the Li Theatre.'),
  ('ling_daiqiu.webp', 'Ling Daiqiu 凌代秋', 'The fishermen\'s leader',
   'Thirty, big, grey-green with sickness, a fresh leaf in his hand, mould at the wound; Swim 75, Boat 70.',
   '"排空击浪穿云翻天龙": the man every fisherman follows. Took Autumn in as an orphan; she stabbed him and cast Green Rot on him.',
   [('Front Street', 'Lies dying in the lane by the river', 'p.20 · Front Street'),
    ('Cure', 'Recovers the moment Autumn dies', 'p.18 · Front Street'),
    ('Riverbank', 'Without him the fishermen refuse the raid; with him they plan it', 'p.36 · Riverbank')],
   'The gate to the fishermen and so to sinking the warships (Ending 1).'),
  ('wangwu.webp', 'Wang Wu 王五条', 'Owner of the big restaurant',
   'Forty-eight, stout, kind, bearded, a staff; Staff 65.',
   'Merchant family; a wandering staff-fighter in his youth; settled and opened the biggest eating-house in town. Fan\'s close friend who helped him catch "thieves" (Yue included) and knows the whole plan; shelters Chen out of pity for the sacrificed. May owe HO2\'s family a famine debt.',
   [('12 Jan', 'Shop shut after fighting the watchman over Chen', 'p.18 · Front Street'),
    ('Any day', 'Talk; the poisoned noodles happen in his house', 'p.18–19 · Front Street'),
    ('When pressed', 'Tells Fan\'s plan, the sacrifices, the flotilla; the delivery of the 17th', 'p.18 · Front Street'),
    ('17 Jan', 'Lends the delivery carts for the raid', 'p.36–37 · Riverbank'),
    ('If Toghan is poisoned here', 'Closes the shop; asks to cross with the party; no raid from here', 'p.43 · Front Street')],
   'The witness who can tell the truth plainly, and the door to the warship raid.'),
  ('song.webp', 'Song Zeyi 宋择一', 'Tea master',
   'Fifty, thin, goatee, smiling; paints pictures in tea foam; Throw 70, Jump 70.',
   '"瓯面弄泉", praised by the emperor and by Fan; a minor jianghu name in youth. Shares Fan\'s ideals and helped gather the sacrifices; despises Yue\'s lawbreaking even for the poor. Hides what he knows and stays out of anything to do with the monster.',
   [('Teahouse', 'The tea pictures; the brawl (cups for bonus dice); the Wineshop address', 'p.20–21 · Front Street'),
    ('15 Jan', 'A rescuer ("slippery as a loach")', 'p.24–25 · Front Street')],
   'The teahouse set piece and the road to the Wineshop; a good man complicit in Fan\'s crime.'),
  ('autumn.webp', 'Autumn 秋筠', 'The veiled lodger',
   'Twenty-six, slender, all in white, veiled; callused fingers; under the veil, scars over a convict\'s tattoo. Sword 70, Disguise 70; Undying form when badly hurt.',
   'A famous outlaw of the Jinghu country with "a thousand faces"; caught by Fan and sacrificed; came back as an Undying and stayed a thief. Took the Lings\' needles, Green-Rotted Ling Daiqiu, and hid at the Li Theatre as a pitiful bride.',
   [('Li Theatre', 'Eavesdrops; begs passage; offers disguise help daily; or flees to the roof and fights', 'p.17–18 · Front Street'),
    ('Her room', 'The Green Rot pages', 'p.18 · Front Street; handouts'),
    ('Her death', 'Ling Daiqiu recovers; the needles are recovered', 'p.18, 53 · Front Street')],
   'A useful ally who is the villain of the needles thread: the needles (+10% Acupoint) and the fishermen both hang on killing her.'),
  ('chen.webp', 'Chen Xunzhong 陈寻忠', 'The waiter who was a soldier',
   'Thirty-five, tall, pale, damp at the collar, eager and tearful; Undying.',
   'Liu\'s standard-bearer, drowned on the 3rd and raised; Wang Wu found him on the bank. Under Gla\'aki\'s order to kill Liu, the one who escaped.',
   [('Front Street', 'Stole from the pharmacy; chased by Fang into the restaurant', 'p.18 · Front Street'),
    ('Restaurant', 'Poisons Liu\'s noodles with pokeweed; kneels; asks for a midnight meeting', 'p.19 · Front Street'),
    ('Night', 'The Rashomon alley: half-truths about the Fans and the temple', 'p.45–46 · Optional'),
    ('Temple', 'Leads HO3 and Liu into the dark hall; the ambush', 'p.29 · Temple')],
   'The Undying\'s human face and the trap-layer for Liu; his lies point at the Fans and are half true.'),
  ('monk.webp', 'Huaide 怀德, the Pagoda Arhat', 'The drinking monk',
   'Fifty, huge, shaven, flushed, beads and a wine gourd; Iron Shirt (armour 2).',
   'The temple\'s famous monk who has not been home in half a month; lives at the Wineshop drinking and meditating at the wall.',
   [('Wineshop', 'Daily drinking contest: three CON wins = golden kasaya (armour 2, fire-immune)', 'p.24 · Front Street'),
    ('Temple', 'Arrives in the fight if told about the locked hall or the footprints', 'p.29 · Temple'),
    ('Finale', 'His kasaya protects HO1 on the water (or Duan supplies it)', 'p.40 · Finale')],
   'Comic relief with the finale\'s armour in his pocket.'),
  ('bookseller.webp', 'Wang Jianchuan 王见川', 'The old-book seller',
   'Thirty, burly, scholar\'s cap and feather fan, a voice like a bell.',
   'Keeps a stall of novels, poems and tales of the strange on Front Street.',
   [('Stalls', 'The Lost Pendant and The Rain Master; Magistrate Fan browses here', 'p.16 · Front Street; handouts')],
   'Delivers the two legends that frame the river goddess and Red Pine.'),
  ('mistress_wang.webp', 'Mistress Wang 王氏', 'Owner of the Li Theatre',
   'Fifty-odd, tired, kind; a five-year-old daughter at her sleeve.',
   'Husband and son pressed for labour; the performers fled; she took in "a homeless young woman".',
   [('Li Theatre', 'Tea and talk; lends the boat in the dry pool; looks into Autumn\'s room afterwards', 'p.17–18 · Front Street')],
   'Provides a boat for the finale and unknowingly shelters Autumn.'),
  ('physician.webp', 'The Song physician 宋人郎中', 'Ashu\'s doctor',
   'Sixty, stooped, cautious.',
   'A Chinese doctor in the marshal\'s household.',
   [('Assassination', 'Checks every medicine; knows when it is tampered with; says nothing; hides in the fight', 'p.32–33 · Magistracy quarter')],
   'Silent permission for the fake cure to pass.'),
  ('turncoat.webp', 'The Song turncoats 降卒 (and their centurion)', 'Ship guards',
   'Farmers, fishermen, pedlars in Song jackets with Mongol belts; the centurion has two small children. HP 10, no armour.',
   'Followed their generals into Mongol service; left to guard the warships on feast night.',
   [('Raid', 'Eat and talk with the party; Listen 50 twice = alarm; runners below half HP flee to tell', 'p.37 · Riverbank')],
   'The raid\'s tension and its moral weight: the men the party must stop are Song.'),
  ('servant.webp', 'The Undying 不死仆从 (the girl, her brother, the burnt family, the temple soldiers)', 'Gla\'aki\'s servants',
   'Human by day; at night bones twist, limbs draw out into spines, skin rots; a healed wound on the spine under a red web.',
   'Everyone the thing pierced in the river or at the bank: the sacrificed convicts, Liu\'s drowned men, townsfolk lured in dreams. They fear fire and sunlight, need no food, and obey.',
   [('Undying house', 'The widow\'s daughter and her condemned brother', 'p.23–24 · Front Street'),
    ('Burning house', 'Their kin, unable to flee the fire', 'p.27 · Back Street'),
    ('Temple', 'Liu\'s old soldiers in the side hall', 'p.29 · Temple'),
    ('Night', '"The dead speak"; "The goddess comes in dreams"', 'p.42, 38 · Optional, Riverbank'),
    ('Finale', '1D3+2 a round at the foot of the tower', 'p.41 · Finale')],
   'The horror thread\'s foot-soldiers and the reason HO2\'s Acupoint Strike matters.'),
  ('glaaki.webp', 'Gla\'aki 格拉基, the Many-Headed Fish 何罗鱼', 'The thing in the river',
   'A vast spined slug with three eye-stalks and hundreds of pale feet, on the river-bed under its own fog; one spine at a time above the water. SAN 1D3/1D20 to see.',
   'A shard of it grew as green jade in the forty-sixth hole of a Grand Lake Stone; Fan bought the stone and woke it. It calls in dreams (the River Lord, the goddess, the fish), pierces the dreamer\'s chest and makes the drowned walk. It fears fire and light.',
   [('Backstory', 'What it is and does', 'p.9–10 · The whole story'),
    ('Every night', 'Dream-Call to HO3', 'p.45 · Optional'),
    ('Riverbank', '"The goddess comes in dreams"; the reeds\' three temptations', 'p.38–39 · Riverbank'),
    ('Finale', 'Rises to the boat\'s light; dies to spines cut and arrows from the tower', 'p.40–41 · Finale')],
   'The scenario\'s secret engine: it blocks the Mongols, and killing it frees the river for them — the dilemma every ending turns on.'),
 ]),
]
# Plain-language summaries keyed by portrait file: (who they are, what they want, how to use them at the table).
PLAIN = {
 'duan': ('A Chinese general who now serves the Mongols. He is HO1\'s old classmate: they had the same sword teacher for one year. He is polite, clever and afraid of dying.',
          'To stay alive and keep his position. He also likes HO1 and secretly wishes he could live free like him.',
          'He is on the players\' side without saying so. He stops Mongol soldiers from hurting them. His room has three useful papers (the teacher\'s letter, the feast note, the map). At the end he offers to go out on the river with HO1.'),
 'yue': ('HO2\'s foster brother. He pretends to be a doctor. He cannot heal and cannot fight. He sells fake medicine to rich people, steals from them, and gives the money to the poor.',
         'To keep HO2 safe. He feels guilty: on 3 January he walked into Commander Fan\'s ritual by mistake, the ritual started too early, and Captain Liu\'s soldiers drowned. He has told nobody.',
         'Use him to give hints when the players are stuck. He gives them Prefect Xu\'s two letters (to force Xu to lend boats). In the assassination he offers himself as Ashu\'s hostage. Before the last fight he tells HO2 the truth.'),
 'liu': ('HO3\'s best friend since childhood, and the officer who led HO3\'s soldiers. He drowned with them on 3 January and came back alive, but changed: no heartbeat, cannot be poisoned, a red web mark on his back. He does not understand what happened to him.',
         'To find his soldiers and protect HO3.',
         'From the night of 12 January he follows HO3 everywhere and fights well. The river monster wants him dead, so its servants attack him first (poisoned noodles, the temple trap, the family house). He is how the players learn what the monster does to people.'),
 'ashu': ('The Mongol commander. Very big, very strong, very smart. HO1 cut his shoulder with a poisoned sword, and the wound will never heal (every roll he makes has a penalty die).',
          'A cure for the wound, and to cross the river and take Southbright on 18 January.',
          'He is the main enemy and should feel impossible to beat in a fair fight. The players can kill him only in his sickroom, pretending to be doctors. When he dies the city is locked down and the last night begins.'),
 'toghan': ('Ashu\'s deputy. Cruel, bad-tempered, speaks little Chinese. He killed HO2\'s father.',
            'To serve Ashu, bully the Chinese, and eat lunch at Wang Wu\'s restaurant every day.',
            'He is HO2\'s chance for revenge: poison his lunch. Warning: if the players do this at the restaurant, the owner will be too scared to help with the warship raid later.'),
 'fan': ('The Chinese commander of Fencewall. He is dead: he hanged himself the night the city fell. People loved him.',
         'He wanted to stop the Mongols at any price. He bought a strange stone with a piece of the river monster in it, killed prisoners as a sacrifice, and called the monster into the river.',
         'He never appears. The players discover what he did from his study, his empty coffin (hidden pages inside), the ruined pavilion, and people who helped him. He is the reason for everything bad in the river.'),
 'fan_yulou': ('Commander Fan\'s nephew, about 28, a scholar. He opened the gates to the Mongols and now runs the town for them. He looks like a traitor.',
               'He is not a traitor. He knows about the monster and is continuing his uncle\'s plan. He wants Ashu killed.',
               'When the players open the coffin he catches them and asks them to kill Ashu. He gives gunpowder and arranges a riot as a distraction. After the killing the Mongols cut off his head.'),
 'xu': ('A fat, rich, cowardly official in charge of the town\'s money.',
        'To be safe whoever wins. He wrote one letter offering his boats to the Mongols and another swearing loyalty to the Song. Doctor Yue stole both.',
        'Threaten him with the letters (or bribe or frighten him) and he gives boats, gunpowder, and a way into the gaol.'),
 'niu': ('The garrison\'s second-in-command and a famous archer. He refused to surrender. The Mongols cut the tendons in his hands and put him in gaol.',
         'To die with honour. He will be beheaded at noon on 15 January.',
         'The players rescue him on the way to the execution. In thanks he gives them his special bow, the only bow that can shoot far enough to hit the monster from the shore.'),
 'yuying': ('Commander Fan\'s daughter, about 20. Ashu keeps her as a servant to shame her family.',
            'Revenge, quietly.',
            'In the sickroom fight she takes one sword blow for a player and secretly passes HO2 a dagger.'),
 'hermit': ('HO1\'s sword teacher, over 70, with one arm. A famous hermit.',
            'He wanted HO1 to become famous by killing Ashu. He knew he would die for it and stayed home to wait.',
            'On 12 January the players find his body displayed at the Street Crossing. Later Duan shows HO1 his grave and gives HO1 some old pages with a fire spell that helps in the last fight.'),
 'scholar': ('Young students from the town school. Brave talkers, no fighting skill.',
             'To do something for their country.',
             'The players meet them at the teahouse and library. On the day of the assassination they riot outside Ashu\'s house so the guards are busy. Many of them die.'),
 'qu': ('The coffin-maker, about 50, tall and strong. She shelters the players in her shop. Ten years ago she killed her cheating husband.',
        'To help decent people.',
        'Her shop is the players\' home. She tells them coffins can have a hidden box inside, and that she made Commander Fan\'s coffin. This points them to the secret pages.'),
 'jiang_tower': ('Twin brothers, fishermen, excellent swimmers. Tower is calm, Loft is reckless.',
                 'To help their town.',
                 'They pull the players out of the river on the first night. Later they can help rescue Niu and sink the Mongol ships.'),
 'boatman': ('A one-armed man who rows people across for money.', 'Money.', 'He rows the players out on the first night and swims away when the boat sinks. He is not seen again.'),
 'du': ('Owner of a small hidden wine shop where the town\'s fighters meet. Friendly, knows everyone.',
        'To help Niu and hurt the Mongols.',
        'He explains the plan to rescue Niu (ambush the prison carts in the street) and brings helpers.'),
 'fang': ('A 16-year-old night watchman. Very strong, honest, bad at talking. Niu looked after him.',
          'To save Niu, and to give back the long wrapped thing Niu asked him to carry (it is the special bow).',
          'He asks the players to rescue Niu. Only he knows Niu\'s face, so only he can tell which prison cart Niu is in. After the rescue he hands over the bow.'),
 'ling_xuchun': ('A 19-year-old swordswoman in red, quick to anger.',
                 'Medicine for her dying brother, and revenge on the woman who stabbed him and stole the family\'s special needles.',
                 'The players meet her arguing at HO2\'s pharmacy. She leads them to her brother and to the thief (Autumn). If they help, she fights for them and gives them the needles.'),
 'ling_daiqiu': ('Ling Xuchun\'s older brother, leader of the fishermen. He is dying: his wound is rotting and has green mould.',
                 'To live.',
                 'He gets well the moment Autumn is killed. Then he asks the fishermen to help the players sink the Mongol ships. Without him the fishermen say no.'),
 'wangwu': ('Owner of the big restaurant. Kind and generous. He was Commander Fan\'s friend and knew about the ritual.',
            'To make up for what he helped do. He hates the Mongols.',
            'If asked directly he tells the whole truth about the ritual. He lets the players dress as his delivery men to get near the Mongol ships on 17 January.'),
 'song': ('The tea master at the teahouse. Thin, smiling, very skilled. He also helped Commander Fan find prisoners for the ritual, and hides it.',
          'A quiet life; he respects brave people.',
          'When Mongol soldiers bully people in the teahouse and the players step in, he helps (thrown cups of tea give bonus dice) and tells them where the hidden wine shop is.'),
 'autumn': ('A young woman in a white veil living in the ruined theatre. She says she wants to cross the river to her husband. She is lying.',
            'She is a famous thief. Commander Fan sacrificed her and she came back as one of the monster\'s servants. She stole the Ling family\'s needles and put a rotting curse on Ling Daiqiu.',
            'She is helpful (free disguise help once a day) until the players accuse her. Then she fights. When she dies, Ling Daiqiu is cured and the players get the needles (+10% to HO2\'s Acupoint Strike).'),
 'chen': ('A waiter at Wang Wu\'s restaurant. He was Captain Liu\'s flag-bearer. He drowned and is now one of the monster\'s servants.',
          'The monster has ordered him to kill Liu.',
          'He poisons Liu\'s noodles (Liu survives), cries, and asks Liu and HO3 to meet him at night. He tells a half-true story and leads them into a dark temple hall full of other servants.'),
 'monk': ('A huge, cheerful monk who drinks all day at the wine shop. His body is as hard as iron.',
          'Wine.',
          'Beat him at a drinking game (three CON rolls in a row) to win his golden robe: armour 2 and fire cannot hurt the wearer. Tell him about the strange temple hall and he comes to help in that fight.'),
 'bookseller': ('A big man dressed as a scholar who sells old books on Front Street.', 'To sell books.', 'His stall has two old stories the players should hear: the river goddess, and Red Pine the Rain Master.'),
 'mistress_wang': ('The owner of the ruined theatre, about 50, with a small daughter.', 'To get by.', 'She lends the players a boat. She does not know her lodger (Autumn) is dangerous.'),
 'physician': ('Ashu\'s old Chinese doctor.', 'To survive.', 'He checks the players\' medicine. If it is fake or poisoned he notices and says nothing. He hides during the fight.'),
 'turncoat': ('Chinese soldiers whose general joined the Mongols, so they did too. They guard the warships. Ordinary homesick men.',
              'To eat, drink and go home.',
              'On 17 January the players eat with them while fishermen secretly sink the ships. If the soldiers notice, there is a fight. If even one runs away to warn the Mongols, Duan is executed and the fishermen die.'),
 'servant': ('People killed by the river monster and brought back. By day they look normal. At night they become monsters with spines.',
             'They obey the monster: bring more people to the river, and kill Captain Liu.',
             'They are afraid of fire and sunlight. Weak point: the scar on the backbone. A sharp point there kills at once (HO2\'s Acupoint Strike).'),
 'glaaki': ('The monster in the river: a giant slug with metal spines and three eyes on stalks. It makes the fog. In the Chinese books it is called the He Luo fish.',
            'To make more servants. It calls sleeping people to the water and stabs them with a spine.',
            'While it lives, nobody can cross, not even the Mongols. If the players kill it, the Mongols can cross too. That choice is the heart of the ending. It is killed on the last night: HO1 lights it up from a boat, HO3 shoots it from the tower, HO2 guards the tower.'),
}
def dossier_key(img): return img.replace('.webp', '') or 'fan'
def dossier_block(row):
    from npc_zh import ZH
    img, name, role, look, back, events, contrib = row
    key = dossier_key(img)
    who, wants, use = PLAIN[key]
    pic = f'<img src="{P_}{img}" width="64" height="64" class="cast-pic">' if img else ''
    s = f'<div class="dossier"><table class="cast"><tr><td class="cast-pic-cell">{pic}</td><td><b>{name}</b><br><small>{role}</small></td></tr></table>'
    s += f'<p><b>Who.</b> {who}</p><p><b>Wants.</b> {wants}</p><p><b>At the table.</b> {use}</p>'
    s += '<table><tr><th>When</th><th>Scene</th><th>Book · journal</th></tr>' + ''.join(f'<tr><td>{w}</td><td>{e}</td><td>{pg}</td></tr>' for w, e, pg in events) + '</table>'
    if ZH.get(key): s += f'<p class="zh-orig"><b>原文</b> {ZH[key]}</p>'
    return s + '</div>'
def dossier_html():
    s = H('NPC dossier', '人物档案', 1)
    s += P('One block per character, in plain words: who they are, what they want, how to use them. Then every scene they appear in (book page, and which page of this journal to open). The original Chinese from the scenario is quoted underneath.')
    for group, rows in DOSSIER:
        s += f'<h2>{group}</h2>' + ''.join(dossier_block(r) for r in rows)
    return s
# Names that turn into a link to that person's page in the "People" journal. Only unambiguous forms: a bare "Fan", "Wang",
# "Ling" or "Song" is left alone because it could be two people (or the dynasty).
ALIASES = {
 'duan': ['Duan Driftwood', '段游衍', 'Duan'], 'yue': ['Doctor Yue', 'Yue Nanke', '越南柯', 'Hollow Physician', 'Yue'], 'liu': ['Captain Liu', 'Liu Qingtang', '刘卿堂', 'Liu'],
 'ashu': ['Marshal Ashu', '兀良哈·阿术', '阿术', 'Ashu'], 'toghan': ['General Toghan', '兀良哈·脱欢', '脱欢', 'Toghan'], 'fan': ['Commander Fan', '范天顺'],
 'fan_yulou': ['Magistrate Fan', '范玉楼', 'Fan Yulou'], 'xu': ['Prefect Xu', '许德显', 'Xu'], 'niu': ['General Niu', '牛富', 'Niu'], 'yuying': ['Fan Yuying', '范玉莹', 'Yuying'],
 'hermit': ['The Hermit of Mount Crag', 'the Hermit of Mount Crag', 'Hermit of Mount Crag', '山阳道人', 'Chen Yangshan', '陈阳山', 'the Hermit', 'The Hermit'],
 'scholar': ['Zhou Wentong', '周文通', 'Kong Liyue', '孔礼岳', '儒生'], 'qu': ['Winding Stream', '曲流'], 'jiang_tower': ['the Jiang twins', 'The Jiang twins', 'Jiang twins', '姜楼', '姜阁'],
 'boatman': ['Boatman Wang', '船夫王'], 'du': ['Du Guanshan', '杜观山'], 'fang': ['Nameless Fang', '方未名', 'Fang'], 'ling_xuchun': ['Ling Xuchun', '凌序春', 'Xuchun'],
 'ling_daiqiu': ['Ling Daiqiu', '凌代秋', 'Daiqiu'], 'wangwu': ['Wang Wu', '王五条'], 'song': ['Song Zeyi', '宋择一', 'tea master Song', 'Tea master Song'], 'autumn': ['Autumn', '秋筠'],
 'chen': ['Chen Xunzhong', '陈寻忠'], 'monk': ['Huaide', '怀德'], 'bookseller': ['Wang Jianchuan', '王见川'], 'mistress_wang': ['Mistress Wang', '王氏'],
 'physician': ['Song physician', '宋人郎中'], 'turncoat': ['Song turncoats', '降卒'], 'servant': ['Undying Servants', 'the Undying', 'The Undying', '不死仆从'],
 'glaaki': ["Gla'aki", '格拉基', '何罗鱼', 'Many-Headed Fish'],
}
import re as _re, html as _html
def _alias_re(names):
    return '(?:' + '|'.join((r'(?<![A-Za-z])' + _re.escape(n) + r'(?![A-Za-z])') if n[0].isascii() else _re.escape(n) for n in sorted(names, key=len, reverse=True)) + ')'
_ANY = _re.compile('|'.join(f'(?P<{k}>{_alias_re(v)})' for k, v in sorted(ALIASES.items(), key=lambda kv: -max(map(len, kv[1])))))
_SAME = {k: _re.compile(r'[\s,，(（]{0,2}' + _alias_re(v) + r'[)）]?') for k, v in ALIASES.items()}
def link_people(html, uuid, skip=None):
    """Wrap every NPC name in running text in a link to that person's page. `uuid` maps dossier key -> page UUID.
    Headings, existing links and the person's own page (`skip`) are left alone. "Wang Jianchuan 王见川" becomes one link."""
    out, depth = [], 0
    for part in _re.split(r'(<[^>]+>)', html):
        if part.startswith('<'):
            m = _re.match(r'<(/?)(h[1-6]|a|th)\b', part)
            if m: depth += -1 if m.group(1) else 1
            out.append(part); continue
        if depth: out.append(part); continue
        res, pos = [], 0
        while True:
            m = _ANY.search(part, pos)
            if not m: break
            key, end = m.lastgroup, m.end()
            if key != 'wangwu' or not part.startswith(' Jianchuan', end):
                m2 = _SAME[key].match(part, end)
                if m2: end = m2.end()
            if key == skip: res.append(part[pos:end])
            else:
                tip = _html.escape(_re.sub(r'<[^>]+>', '', PLAIN[key][0]), quote=True)
                pid = uuid[key].split('.')[-1]
                res.append(part[pos:m.start()] + f'<a class="content-link npc-link" draggable="true" data-link data-uuid="{uuid[key]}" data-id="{pid}" data-type="JournalEntryPage" data-tooltip="{tip}">{part[m.start():end]}</a>')
            pos = end
        res.append(part[pos:]); out.append(''.join(res))
    return ''.join(out)
P_ = f'modules/{__import__("content").MOD}/assets/portraits/'
