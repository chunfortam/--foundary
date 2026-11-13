# -*- coding: utf-8 -*-
# Bilingual content for the 公若渡河 session-0 Foundry adventure. Chinese original (condensed/paraphrased from the scenario by 江涔) + natural English.
MOD = "gongruo-session0"
def bi(zh, en):
    return f'<p class="zh">{zh}</p><p class="en"><em>{en}</em></p>'
def h(zh, en, lvl=2):
    return f'<h{lvl}>{zh} · {en}</h{lvl}>'
def ul(pairs):
    return '<ul>' + ''.join(f'<li>{zh}<br><em>{en}</em></li>' for zh, en in pairs) + '</ul>'
def table(headers, rows):
    s = '<table><thead><tr>' + ''.join(f'<th>{x}</th>' for x in headers) + '</tr></thead><tbody>'
    for r in rows: s += '<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>'
    return s + '</tbody></table>'

GLOSSARY = [
 ("地名 · Places", [
  ("襄阳", "Southbright", "the holdout city on the south bank; 阳 = the sunlit side"),
  ("樊城", "Fencewall", "the surrendered city on the north bank; 樊 = fence"),
  ("汉江 / 汉水", "the Han River", "real river, keeps its English name"),
  ("临安府", "Haven, the capital", "the Song capital (today's Hangzhou)"),
  ("岘山 / 岘首山", "Mount Crag", "the hermit's mountain"),
  ("大理", "Dali", "the south-western kingdom; real place, keeps its name"),
  ("解佩亭", "the Pavilion of the Untied Pendant", "riverside pavilion where the stone was kept"),
  ("芦苇荡", "the Reed Marsh", "east of Fencewall, where the boats leave"),
  ("前街 / 后街", "Front Street / Back Street", ""),
  ("衙署", "the Magistracy", "the government compound"),
  ("李家瓦子", "the Plum Playhouse", "李 = plum; a ruined theatre"),
  ("王五分茶", "Old Five's Teahouse", "the big restaurant run by Old Five Wang"),
  ("酒肆", "the Wineshop", "where the knights-errant meet"),
  ("棺材铺", "the Coffin Shop", "your safe house"),
  ("塔楼", "the Watchtower", "the 50 m wooden tower on the bank"),
  ("会馆", "the Merchants' Hall", "now the Mongol officers' lodging"),
 ]),
 ("人物 · People", [
  ("兀良哈·阿术", "Marshal Ashu of the Uriankhai", "Mongol commander-in-chief (Mongol name kept)"),
  ("兀良哈·脱欢", "Toghan", "Ashu's brutal deputy; killed HO2's father"),
  ("段游衍", "Duan Driftwood", "Song turncoat general, HO1's old classmate (游衍 = drifting)"),
  ("范天顺", "Commander Fan", "Fencewall's late commander, hanged himself"),
  ("范玉楼", "Magistrate Fan", "his nephew, now runs the city"),
  ("范玉莹", "Lady Fan", "the commander's daughter"),
  ("牛富", "Niu the Archer", "the famous bowman, now in the gaol"),
  ("刘卿堂", "Captain Liu", "HO3's childhood friend"),
  ("越南柯", "Doctor Yue, the Hollow Physician", "空空郎中; HO2's foster brother, con-man thief"),
  ("山阳道人 (陈阳山)", "the Hermit of Mount Crag", "HO1's master"),
  ("许德显", "Prefect Xu", "fat, corrupt treasurer"),
  ("方未名", "Nameless Fang", "the night watchman boy"),
  ("姜楼 / 姜阁", "the Jiang twins, Tower and Loft", "identical twins, strong swimmers"),
  ("曲流", "Winding Stream", "the coffin-maker, your host"),
  ("秋筠", "Autumn", "the scarred woman (a bandit, now undying)"),
  ("凌代秋 / 凌序春", "Ling the Elder / Ling the Younger", "fisher siblings; he is called the Wave-Breaking Dragon"),
  ("杜观山", "Du Mountain-Gazer", "wineshop keeper"),
  ("王五条", "Old Five Wang", "teahouse owner"),
  ("宋择一", "Song the Tea Master", ""),
  ("赤松子", "Red Pine, the Rain Master", "legendary immortal"),
  ("汉江神女", "the Lady of the Han", "river goddess of legend"),
  ("忽必烈 / 贾似道 / 吕文焕", "Kublai Khan / Chancellor Jia / General Lü", "historical figures"),
 ]),
 ("物品与术语 · Things & terms", [
  ("止水", "Stillwater", "the hermit's famous sword"),
  ("雨师墨", "Rainmaster's Ink", "a poison that stops wounds from healing"),
  ("格拉基", "Gla'aki", "the thing in the river (Mythos name kept)"),
  ("何罗鱼", "the Many-Headed Fish", "its name in old travel books / 山海经"),
  ("不死仆从", "the Undying Servants", "Gla'aki's thralls"),
  ("绿腐术", "the Green Decay", "a curse delivered with a green leaf"),
  ("梦引", "the Dream-Call", "Gla'aki's nightly POW contest"),
  ("点穴", "Acupoint Strike", "custom skill; kills an Undying Servant outright"),
  ("轻功", "Lightness", "in this scenario = Climb and Jump"),
  ("神臂弓", "the God-Arm Bow", "Niu's bow, shoots 400 paces"),
  ("太湖石", "the Grand Lake Stone", "the 81-holed rock with a shard in it"),
  ("绣花针", "the Ling family needles", "Acupoint Strike +10%"),
  ("游侠", "knight-errant / wanderer", "a jianghu swordsman who rights wrongs"),
  ("江湖", "the jianghu", "the world of wanderers, sects and outlaws"),
 ]),
]

def glossary_html():
    s = h("名词对照表", "Glossary", 1)
    s += bi("人名保留姓氏读音，名字与地名在读得自然时译成英文；真实存在的大地名（汉江、大理、临安）用通行英文名。",
            "Surnames keep their sound; given names and places are rendered in English where that reads naturally; well-known real places (the Han River, Dali, the capital) keep their usual English names.")
    for title, rows in GLOSSARY:
        s += f'<h2>{title}</h2>' + table(["中文", "English", "Note"], rows)
    return s


# ---------------- PREGEN CHARACTERS: public description (no secrets; for picking a role and introducing yourself) ----------------
PC_PUBLIC = {
 1: dict(name='陆青崖 Lu Bluecliff', looks_zh='二十四岁，衣着朴素，话少，背上裹着一柄从不示人的剑', looks_en='24; plainly dressed, says little; a wrapped sword on his back he never shows',
   zh="陆青崖，二十四岁。岘山山阳道人门下的游侠：衣着朴素，腰间一柄佩刀，背上另裹着一柄更好的剑，从不在人前拔出。话少，眼睛不闲着。自幼习武，上墙如走平地，落地无声，出剑快得看不清；人情世故却不是他的本事。认准了的事就会去做——而且他心里压着一件不能对生人说的事。",
   en="Lu Bluecliff 陆青崖 (\"blue cliff\", after the mountain he grew up on), 24. A wanderer of the jianghu 江湖: plainly dressed, a sabre at his hip and a second, finer sword wrapped on his back that he never draws in front of people. Says little, misses nothing. Trained since childhood by a famous hermit swordsman on Mount Crag 岘山, he can run up a wall, land without a sound and cut faster than you can see (Sword 75, Climb 60, Stealth 60, Dodge 60). What he cannot do is talk his way out of trouble (Credit Rating 20). Play him as a man who has decided what is right and will do it, and who is quietly carrying something he cannot tell strangers."),
 2: dict(name='沈怀珠 Shen Pearl', looks_zh='二十岁，外袍朴素、内里绫罗，手上没有茧，带着药箱', looks_en='20; plain travelling coat over silk, soft hands, a medicine chest',
   zh="沈怀珠，二十岁。临安大药行的少东家：外袍朴素，内里是绫罗，手上没有茧，随身一只药箱和一方药行印信，天下任何一家分号的掌柜见了都要作揖。聪明，口舌利，习惯用钱解决事情；会看病抓药。家传一门点穴之术，指头按对地方能让人半边身子发麻。不是打手，爱走偏锋。她这辈子头一回体会到什么叫无能为力。",
   en="Shen Pearl 沈怀珠 (\"holding a pearl\"), 20. Heir to one of the great pharmacy houses of the capital, Lin'an 临安: silk under a plain travelling coat, soft hands, a medicine chest, and a seal that any branch manager in the empire will bow to. Clever, quick-tongued and used to money solving things (Credit Rating 60, Medicine 65, Persuade / Fast Talk / Charm 50–55, Appraise, Accounting). The family also hands down a secret art, Acupoint Strike 点穴: a finger pressed to the right spot numbs an arm or drops a man (base 50). Not a fighter; thinks sideways. Play her as someone who, until this month, had never once been powerless."),
 3: dict(name='谢云骧 Xie Cloudmane', looks_zh='二十二岁，相貌出众，举止雍容，身上有一处未愈的伤', looks_en='22; handsome, graceful, carries an unhealed wound',
   zh="谢云骧，二十二岁。临安高门子弟，朝廷亲封的宣抚使，印绶在身。相貌出众，学问极好，从小就是让人听话的那一个。自幼围猎，一手好弓，是三人里最会射箭的；剑也拿得起来，勉强。他是带着一支军队来的，如今身上一处伤口不肯收口，也不知道他的人去了哪里。头一回体会到：没人非得听你的时候，名头值几个钱。",
   en="Xie Cloudmane 谢云骧 (\"a horse galloping through clouds\"), 22. Youngest son of one of the great families of the capital and now, with the seal to prove it, an imperial Commissioner sent to relieve the twin cities. Handsome, beautifully educated, raised to be obeyed (APP 75, EDU 80, Credit Rating 75, Persuade 65, Law, History). He has hunted since boyhood and is the best archer at the table (Bow 75); he can hold a sword, barely. He arrived with an army; he has a wound that will not close and no idea what happened to his men. Play him as someone finding out, for the first time, what his name is worth when nobody has to obey it."),
}
def pc_public_html(n):
    d = PC_PUBLIC[n]
    return bi(f"<b>{d['name']}</b>——{d['zh']}", d['en'])

# ---------------- PRIMER (player-facing) ----------------
def primer_html():
    s = h("玩家入门：一二六八年的汉江", "Player Primer: the Han River, 1268", 1)
    s += bi("这是一个武侠故事，发生在真实的历史时刻。你们不是超级英雄，而是乱世中的普通人——只是比旁人多了一身本事。",
            "This is a wuxia story set at a real moment in history. You are not superheroes; you are ordinary people in a collapsing world who happen to have skills.")
    s += h("时局", "The situation")
    s += bi("南宋末年。朝廷腐败，皇帝忙着修道成仙，权臣贾似道把持朝政。北方，忽必烈的蒙古铁骑连战连胜。",
            "It is the last years of the Southern Song dynasty. The court is corrupt, the emperor is busy chasing immortality, and Chancellor Jia runs the government. In the north, Kublai Khan's Mongol cavalry wins every battle.")
    s += bi("汉江两岸有一对双城：北岸的樊城，南岸的襄阳。它们是南方的大门。襄阳三面环水，易守难攻；樊城易攻难守。两城之间原有一座浮桥，围城时已被元军截断。",
            "Two cities face each other across the Han River: Fencewall on the north bank and Southbright on the south. They are the gate to the whole south. Southbright is ringed by water and nearly impregnable; Fencewall is not. A pontoon bridge once joined them; the Mongols cut it.")
    s += bi("一二六八年一月三日，元军总攻樊城。守将范天顺自缢殉国；他的侄子范玉楼献城投降。蒙古统帅兀良哈·阿术下令不得劫掠，城里百姓照常过日子——只是街上到处是巡逻兵。元军准备六日后渡江攻打襄阳。",
            "On 3 January 1268 the Mongols stormed Fencewall. Commander Fan hanged himself rather than surrender; his nephew, Magistrate Fan, opened the gates. Marshal Ashu forbade looting, so life goes on, except for the patrols on every street. In six days the army crosses to attack Southbright.")
    s += bi("就在此时，汉江起了反常的浓雾。百姓说梦见了汉江神女；关于雨师赤松子的旧传说又流传开来。",
            "And now an unnatural fog has settled on the river. Townsfolk dream of the Lady of the Han; old tales of Red Pine the Rain Master are told again.")
    s += h("你们是谁", "Who you are")
    s += bi("三个预设角色，三种过日子的法子。选一个；名字和细节都可以改。", "Three pre-built characters, three different ways of living. Pick one; names and details are yours to change.")
    s += h("HO1 游侠", "HO1 The Wanderer", 3) + pc_public_html(1)
    s += h("HO2 商贾", "HO2 The Merchant Heir", 3) + pc_public_html(2)
    s += h("HO3 命官", "HO3 The Commissioner", 3) + pc_public_html(3)
    s += bi("三人各有不得不离开樊城的理由，也各有不能告人的秘密。你们必须在元军眼皮下渡过汉江。",
            "Each of you has a reason you must leave Fencewall, and a secret you keep from the others. You must cross the Han River under the Mongols' noses.")
    s += h("什么是江湖", "What the jianghu is")
    s += bi("江湖是官府管不到的世界：门派、游侠、镖师、盗匪、郎中、说书人。游侠讲“义”：路见不平，拔刀相助；恩要报，仇也要报。轻功让人翻墙上房；内功与点穴是传说中的高深武学。",
            "The jianghu is the world the government cannot reach: sects, wanderers, caravan guards, bandits, quack doctors, storytellers. A wanderer lives by yi, righteousness: help the wronged, repay kindness, repay insult. Lightness skill lets you leap walls; inner power and acupoint strikes are the stuff of legend. Think Crouching Tiger, Hidden Dragon; Hero; Kung Fu Hustle.")
    s += h("公开人物", "Public figures")
    s += ul([
      ("<b>兀良哈·阿术</b>——征南都元帅，蒙古军总指挥。传说勇武过项王。", "<b>Marshal Ashu of the Uriankhai</b>, Mongol commander-in-chief, Kublai's right arm; a brilliant general and a terrifying fighter."),
      ("<b>段游衍</b>——南宋降将，大理段氏，先降宋再降蒙，见风使舵的好手，儒生最爱骂的人。", "<b>Duan Driftwood</b>, a Song general who surrendered; from the Dali clan; changed sides twice and is the man every scholar loves to curse."),
      ("<b>范天顺</b>——樊城都统制，勤政爱民，城破时自缢。", "<b>Commander Fan</b>, Fencewall's beloved commander, dead by his own hand."),
      ("<b>牛富</b>——樊城钤辖，神射手，拒降被囚。", "<b>Niu the Archer</b>, the garrison's famous bowman, refused to surrender and is now in the gaol."),
      ("<b>范玉楼</b>——范天顺之侄，献城后掌管樊城。", "<b>Magistrate Fan</b>, the nephew who surrendered the city and now runs it."),
    ])
    s += h("历史提示", "A note on history")
    s += bi("模组改动了史实（真实的襄樊之战持续到一二七三年）。你们可以改变具体事件，但无法改变历史的结局。",
            "The scenario bends history (the real siege lasted until 1273). You can change what happens to people here; you cannot change how the war ends.")
    return s

# ---------------- OPENING NARRATIVE (read aloud, English table) ----------------
OPENING = [
 "Listen.",
 "There is a river in the middle of China called the Han 汉江. In winter it runs grey and wide and slow, and for a thousand years it has been the line between north and south. On its two banks stand two walled cities, close enough that on a clear day a man on one wall can watch the sentries pace on the other: Fencewall 樊城 to the north, Southbright 襄阳 to the south. Between them, until last week, there was a bridge.",
 "The year is 1268. The empire of the Song 宋 is old and gold and soft, and it has forgotten how to fight. Out of the north have come the Mongols, who have never forgotten. They have broken kingdoms from the Yellow Sea to the gates of Europe, and now their horses stand on the north bank of the Han, and their marshal, a man called Ashu 阿术 of the Uriankhai, has taken Fencewall in three days. The commander of the garrison hanged himself. The magistrate opened the gates. The bridge is gone. Across the water Southbright still holds, its watch-fires small and stubborn in the dark, and everyone in Fencewall who has somewhere else to be is looking at those fires and wondering how to reach them.",
 "This is not a world of monsters. This is a world of people: of soldiers and merchants and officials, and of another kind of people who live in the cracks between them, in what is called the jianghu 江湖, the rivers and lakes. Wanderers. Swordsmen who owe nothing to the emperor and everything to their masters. People who can run up a wall and down the other side, who can put a finger on your neck and stop your arm, who carry old grudges and older swords. If you have seen a film where two fighters duel on the roof of a teahouse, you know them.",
 "Three of those people are in Fencewall tonight.",
 "One of you is a wanderer 游侠, young and fast and poor, with a sword that does not belong to you and a thing you did ten nights ago that the whole city is whispering about.",
 "One of you is the heir to a great house of medicine 商贾, from the capital far to the south, who came north with a convoy and a father and will go home with neither.",
 "One of you is a commissioner of the court 命官, born to one of the oldest families in the empire, sent here with five thousand men to save a city that has already fallen, and still carrying the wound that kept you from leaving with the rest.",
 "None of you has met the others. Each of you has a reason to cross the river. Each of you has a secret you would rather keep.",
 "It is the eleventh of January. There is no moon. The guards on the bank change at midnight, and for a few minutes nobody is watching the reeds east of the city, where a one-armed boatman has promised, for a price, to take passengers across.",
 "And it is foggy. In midwinter. Over a river that has never, in anyone's memory, made fog in January.",
 "Let's meet you.",
]
def opening_html():
    s = h("开场", "Opening narrative", 1)
    s += '<p class="en"><em>主持人朗读。Read aloud by the GM, lights low, title screen on, before the three personal intros. Then each player gives a name and one visible detail.</em></p>'
    s += ''.join(f'<p class="narr">{p}</p>' for p in OPENING)
    return s

# ---------------- EXTENDED SESSION 0: DAY ONE (p16 tail, p17, p23, p29, p46 of the original) ----------------
def extended_html():
    s = h("加时：第一日（一月十二日）", "Extended session 0: Day One (12 January)", 1)
    s += bi("若时间充裕，姜汁酥糖之后不要停，继续到十三日拂晓。约再加一到一个半小时。只用一张新地图（街口）；其余回到棺材铺与汉江岸。",
            "If you have time after the ginger candy, keep going to dawn on the 13th: about 60–90 more minutes, one new map (the Street Crossing), the rest back at the Coffin Shop and the riverbank.")
    s += h("向玩家公布：行动轮", "Tell the players: action rounds 行动轮")
    s += bi("从明天起，每天分早、午、晚三轮。去一个地点、做一件事，消耗一轮。吃饭、回棺材铺、去酒肆不消耗。今晚先睡。",
            "From tomorrow the day has three rounds: morning, noon, evening. Going to a place and doing one thing there costs a round. Eating, going home to the Coffin Shop and the Wineshop are free. Tonight you sleep.")
    s += bi("前街到处是元军巡逻和HO1的通缉令（段游衍画像时故意画得模糊，只说个轮廓）。HO1若乔装失败，以队伍中最低的幸运检定是否被认出；再失败则敏捷逃脱，且本轮去不了目的地。",
            "Front Street is full of patrols and wanted posters for HO1 (Duan 段游衍 drew the face deliberately vague: give a silhouette, no more). If HO1 fails Disguise, the lowest Luck in the party decides whether a soldier recognises him; fail that and it is a DEX roll to get away and the round is lost.")
    s += h("十一日夜：第一次梦引（仅HO3）", "Night of the 11th: the first Dream-Call 梦引 (HO3 only)")
    s += bi("HO3梦中似有熟悉的声音呼唤其名，诱其赴约。检定意志；失败则听见波涛翻涌、船只折断、人们凄厉惨叫，理智损失1/1D3。",
            "As HO3 falls asleep a familiar voice calls their name, inviting them somewhere. Roll POW. On a failure they hear waves heaving, timbers snapping and people screaming: SAN 1/1D3. Do this quietly with the HO3 player; the others only see them wake badly.")
    s += h("十二日早：棺材铺白天（场景：棺材铺）", "Morning of the 12th: the Coffin Shop by day (scene: the Coffin Shop)")
    s += bi("粟米粥、白面饼子、咸菜。铺面不大，殡葬用品堆得拥挤；几台完工的棺材掀着盖晾漆。侦查：棺材内壁有放置物品的暗格。",
            "Millet porridge, flatbread, pickles. The shopfront is small and crammed with funeral goods; a few finished coffins stand open to dry their lacquer. Spot Hidden: the inner walls have hidden compartments for grave goods.")
    s += ul([
      ("棺材：战时死人多，家家用得上。她手艺高，范天顺的棺材也是她做的。", "Coffins: in wartime every family needs one. She is good; she made Commander Fan's 范天顺 coffin too."),
      ("暗格：有人把死者随身物放进暗格，防偷防腐；范玉楼也提过同样的要求。", "Compartments: people put the dead's belongings inside against thieves and rot. Magistrate Fan 范玉楼 asked for one as well."),
    ])
    s += bi("然后让他们商量今天去哪里：主持人只需简述四区——前街（商铺、药行分号、瓦子）、后街（会馆、寺庙）、衙署一带、江岸（码头、芦苇荡）。本加时只跑午时街口；其余留给第一次正式聚会。",
            "Then let them plan the day. You only need to name the four districts: Front Street (shops, HO2's pharmacy branch, the playhouse), Back Street (the Merchants' Hall where Duan lives, the temple), the Magistracy quarter, the riverbank (docks, reed marsh). This extension only plays the noon event at the Street Crossing; whatever else they choose, say \"you spend the morning on it; we pick it up next time\" and move to noon.")
    s += h("十二日午：街口固定事件（场景：街口）", "Noon of the 12th: the Street Crossing 街口 (scene: the Street Crossing)")
    s += bi("前街后街的交汇口，必经之地。行脚店、茶摊；死刑犯在此弃市，午时三刻问斩，尸体挂到子时。",
            "The junction of Front and Back Street; everyone passes here. An inn, a tea stall; this is where the condemned are executed, at a quarter past noon, and left hanging until midnight.")
    s += bi("午时，街口人头攒动，气氛诡谲凝重。今日弃市的是个白发老叟，缺一条手臂，枪尖自喉咙穿过，挑起身体悬于半空。HO1认出是恩师山阳道人。他面容安详，似早料到有此劫。若师父对HO1重要：理智1/1D3。",
            "At noon the crossing is packed and the mood is strange and heavy. Today's dead man is a white-haired old man with one arm missing, a spear through his throat, hoisted so the body hangs in the air. HO1 recognises their master, the Hermit of Mount Crag 山阳道人. His face is calm, as if he had expected this. If the master mattered to HO1: SAN 1/1D3. Let the HO1 player react; do not rush it.")
    s += bi("路人：", "From the crowd:")
    s += ul([
      ("兀良哈为报徒弟一剑之仇，上岘首山抓走年逾七十的山阳道人，也还他一刀。止水不过三尺，阿术一把斩马刀却能将人拦腰砍断。", "\"Ashu went up Mount Crag himself to pay the old man back for his pupil's cut. Seventy years old. That little sword of his, Stillwater, is three feet long; the Marshal's horse-cutter took a man in half at the waist.\""),
      ("阿术要斩不肯投降的宋臣，包括还关在监牢里的牛富等人。幸亏小范大人投降得快，殃及不到咱们平头百姓。", "\"The Marshal is going to execute every Song officer who won't surrender, Niu the Archer 牛富 in the gaol among them. Thank heaven the young Magistrate gave in fast, or it'd be us.\""),
    ])
    s += bi("主持人注意：牛富将在十五日午时在此处斩首，押送队伍可被劫（原书p29的规则）。这是第一次正式聚会的大场面；今天只埋下这句话。",
            "GM note: Niu is to be beheaded here at noon on the 15th and the convoy can be ambushed (rules on p29 of the original). That is the set-piece of the next session; today you only plant the line.")
    s += h("十二日晚：越南柯来访（场景：棺材铺）", "Evening of the 12th: Doctor Yue 越南柯 calls (scene: the Coffin Shop)")
    s += bi("回到棺材铺，一位江湖郎中打扮的人正和曲流攀谈：HO2的师兄“空空郎中”越南柯。他关心众人、尤其HO2的身体。",
            "Back at the shop a man dressed as a wandering healer is chatting with Winding Stream: HO2's foster brother, Doctor Yue 越南柯, the Hollow Physician. He fusses over everyone's health, HO2's most. Play the reunion; HO2 has not seen him in years.")
    s += ul([
      ("船只：两封未寄出的信，都是荆湖通判许德显写的。一封给蒙古军营，表投诚之心，说家里还有三艘画舫、五艘小船愿双手奉上；一封给襄阳吕文焕，字字泣血表忠心。越南柯借看诊之名偷来，可用来胁迫许德显。", "Boats: two unsent letters, both by Prefect Xu 许德显. One to the Mongol camp offering to surrender and hand over his three pleasure-barges and five small boats; one to Governor Lü 吕文焕 in Southbright, weeping loyalty to the Song. Yue stole them during a 'consultation'. Either letter would ruin Xu; together they are a lever to get his boats."),
      ("解毒：他懂得不多，但若是本地传说中的毒，地方图志上没准有记述。", "The poison (Rainmaster's Ink 雨师墨, if HO1 asks): he knows little, but if it is a local legend the county gazetteer 地方志 may record it. (Library 官学&书阁, next session.)"),
      ("疤脸女子：满脸疤痕，要么遭了不测，要么是该处死刑的囚犯。", "The scar-faced woman the town gossips about: a face like that means either a disaster or a condemned criminal."),
      ("范天顺：高瞻远瞩，对百姓尽心尽力，连偷几两灯油的人都要处以极刑。", "Commander Fan: far-sighted, devoted to the people; had a man executed for stealing a few ounces of lamp oil. (Said flat. Let them wonder.)"),
    ])
    s += h("十二日夜：第二次梦引（场景：汉江夜渡，调暗）", "Night of the 12th: the second Dream-Call (scene: Night Crossing, darkness up)")
    s += bi("格拉基再次梦引HO3，驱其独自前往江岸，并以光亮幻象引诱。梦中：", "Gla'aki 格拉基 calls HO3 again, drawing them alone to the riverbank with a lure of light. The dream (read aloud to HO3, SAN 1/1D3):")
    s += bi("你站在船头，脚下的水面波涛不宁。雾气升腾遮天蔽日，连对岸的城市都没了踪影。水下黑色的团状物紧随而来，攀住船身，折断船舷和龙骨，击穿甲板。你在风雨中坠落，直到有什么东西自你脊椎后方穿胸而过。你低下头，伤口正滋滋往外冒着绿色的腐烂液体……",
            "\"You stand at the bow. The water under you heaves. Fog rises until it hides the sky and the city on the far bank. Something black and shapeless comes up under the boat, clings to it, snaps the gunwale and the keel, punches through the deck. You fall through wind and rain, until something comes through your spine from behind and out of your chest. You look down. The wound is hissing, and what runs out of it is green and rotten...\"")
    s += bi("再检定意志：成功，睁眼发现自己在江岸边；失败，已走进汉江，水没过腰。江面寂静，雾气混沌，前方似有发光物闪烁；跟着走几步，水到胸口。闪光物一晃钻入水底，从后方刺向脊背：闪避成功躲开，失败受1D3擦伤。",
            "POW again. Success: HO3 opens their eyes standing at the water's edge. Failure: they are already in the Han, waist deep. The river is silent, the fog thick, a glow flickers ahead; a few steps after it and the water is at their chest. The glow dips under and strikes from behind at the spine: Dodge, or 1D3 scratch.")
    s += bi("刺来的是一根漆黑脊刺，布满鳞甲倒刺，末端纤细尖锐，与昨夜所见相同。此时刘卿堂出现在岸边，扔给HO3一把锈剑，进入战斗轮。脊刺：HP 10，敏捷50，斗殴40，伤害2+1D5。击败即脱险。",
            "It is a black spine, scaled and barbed, thin and sharp at the tip, the same as last night. And on the bank stands Captain Liu 刘卿堂, who throws HO3 a rusty sword. Combat: the spine has HP 10, DEX 50, Fighting 40, damage 2+1D5, armour 4. Beat it (or drive it off) and the danger ends. If HO3 is alone and losing, Liu takes the hits; he does not die tonight.")
    s += bi("刘卿堂被渔民所救，对自己和军队的遭遇一无所知；夜里出来查线索正好遇见HO3。他很高兴HO3平安，随HO3回棺材铺，此后全程参与HO3的行动。",
            "Liu was pulled out by fishermen and knows nothing of what happened to him or his men; he came out tonight to look for clues and found HO3 instead. He is overjoyed, walks HO3 back to the Coffin Shop and from now on goes wherever HO3 goes. GM only: Liu survived a spine on the 3rd and has a red web-shaped mark on his back (p5). He does not know. Do not reveal it; if a player examines him, let them find it and say nothing more.")
    s += h("停在这里", "Stop here")
    s += bi("十三日拂晓，刘卿堂在棺材铺。切回开场画面。预告：三轮一天，十五日午时牛富问斩，许德显的船，官学的地方志。",
            "Dawn on the 13th, Liu at the Coffin Shop. Back to the title screen. Tease next time: three rounds a day; Niu's execution at noon on the 15th; Prefect Xu's boats; the gazetteer in the Library. Players now hold two leads (the letters, the compartments) and one ally.")
    return s

# ---------------- HO handouts ----------------
HO = {}
HO[1] = dict(
  title_zh="HO1 游侠 · 弓背霞明剑，霜寒照吴钩", title_en="HO1 The Wanderer",
  public=bi("你是岘山高士的弟子，身怀绝技。推荐给敢爱敢恨、热爱传统武侠的玩家。任意一项战斗技能＋20。",
            "You are the disciple of the Hermit of Mount Crag, and you are very good at what you do. For players who love classic wuxia and act on their heart. Any one combat skill +20."),
  secret=(
    bi("你师承荆楚岘山的山阳道人，随他修习多年。山阳道人乃当世隐士，相传得神农时期雨师赤松子真传，能入火不焚，御风而行。虽说多为附会之辞，但你的确从他那里习得了一身游侠的本事。",
       "Your master is the Hermit of Mount Crag (his real name is Chen Yangshan 陈阳山). People say he inherited the arts of Red Pine the Rain Master and can walk through fire and ride the wind. Most of that is talk, but he did make you a true wanderer.") +
    bi("你有一位名叫段游衍的昔日同窗，大理人氏，曾追随山阳道人求学一年后离开。师父称赞他思维敏捷、见识过人，但不建议你与他深交。",
       "You had a classmate, Duan Driftwood, from the Dali clan, who studied under your master for a year and left. Your master praised his quick mind and wide learning, but told you not to grow close to him.") +
    bi("此番听闻樊城城破，师父赠你名剑【止水】，命你效仿聂政、荆轲，行刺元军统帅兀良哈·阿术。剑上淬有奇毒“雨师墨”，师父再三叮嘱不可轻率使用。",
       "When Fencewall fell, your master gave you his famous sword, Stillwater, and told you to do as the assassins of old did: kill the Mongol marshal, Ashu. The blade is coated with a rare poison, Rainmaster's Ink. He warned you three times not to use it lightly.") +
    bi("一月十日，元军在樊城衙署大设庆功宴。你成功潜入准备刺杀阿术，奈何他武艺高强、戒备森严，刺杀未果，仅在其肩头留下一道伤口。席间你遇见了已降蒙古的段游衍，有他相助你才得以脱身，如今藏匿于樊城中。",
       "On 10 January the Mongols held a victory banquet at the Magistracy. You got in. But Ashu is a formidable fighter and well guarded; you only cut his shoulder. At the banquet you saw Duan Driftwood, now serving the Mongols. He covered your escape, and you have been hiding in Fencewall since.") +
    bi("蒙古军队正在搜捕你。此地不宜久留，你须尽快离开樊城。",
       "The Mongols are hunting you. You must leave Fencewall, soon.")),
  build=ul([
    ("随身物品必须包括名剑【止水】。【止水】是山阳道人的武器，你自己的武器可以自行设定。", "You carry the sword Stillwater. It is your master's weapon; your own weapon is up to you."),
    ("你自幼习武，体迅飞凫：敏捷＋10，力量＋10，任一战斗技能＋20，攀爬或跳跃＋15。", "Trained since childhood: DEX +10, STR +10, one combat skill +20, Climb or Jump +15."),
    ("这些加值已在预设卡上计入。", "These bonuses are already on your pre-built sheet."),
  ]))
HO[2] = dict(
  title_zh="HO2 商贾 · 市井怀珠玉，往来人未逢", title_en="HO2 The Merchant Heir",
  public=bi("你是临安著名药行的少东家，家财万贯。推荐给思维活络、喜欢剑走偏锋的玩家。自定义技能：点穴，基础值50。",
            "You are the heir of a famous pharmacy house from the capital, and very rich. For players who think sideways. Custom skill: Acupoint Strike, base 50."),
  secret=(
    bi("你是临安府著名药行的少东家。家庭背景、药行的名字、经营理念和行事风格均自行拟定（官商勾结、为富不仁，或扶危济困……）。药行自庆历年间发家，分号遍布大江南北，地方分号难免有欺下瞒上、大肆敛财之事。",
       "Your family's pharmacy house in the capital is famous. You decide its name, its reputation and how it does business: in bed with officials, grasping and heartless, or charitable. It has branches across the empire since the 1040s, and some branch managers are crooks.") +
    bi("你有一位名叫越南柯的师兄，是你父亲故旧的孩子，与你一同长大。几年前他不辞而别独自闯荡江湖，你们之间只剩书信往来。",
       "You have a foster brother, Yue Nanke 越南柯, the son of your father's old friend, raised with you. A few years ago he vanished into the jianghu without a word; since then, only letters.") +
    bi("一二六七年腊月末，你和父亲奉朝廷之命押送一批药材作为军资，不幸在樊城外遭蒙古军队截获。父亲被蒙古人杀害，你趁乱只身逃入樊城。",
       "In the last month of 1267 you and your father escorted a convoy of medicine for the army. Outside Fencewall the Mongols stopped you. Your father was killed in front of you; you fled alone into the city.") +
    bi("父亲既已身故，药行群龙无首，你必须尽快离开樊城。",
       "With your father dead the house has no head. You must get home, which means leaving Fencewall.")),
  build=ul([
    ("商贾巨富：信誉＋10。请为药行命名并确定经营理念，这决定百姓对药行的风评。", "Credit Rating +10. Name the pharmacy house and decide its ethos; it determines how townsfolk treat you."),
    ("通晓看病问诊：医学＋30。药行在樊城有分号，掌柜认得你。", "Medicine +30. The Fencewall branch manager knows you."),
    ("家传点穴之术：自定义技能【点穴】基础值50。", "Family art: custom skill Acupoint Strike, base 50."),
    ("这些加值已在预设卡上计入。", "These bonuses are already on your pre-built sheet."),
  ]))
HO[3] = dict(
  title_zh="HO3 命官 · 翻弓骋猿臂，承箭惜貂裘", title_en="HO3 The Commissioner",
  public=bi("你是朝廷亲封的宣抚使，亲领印绶。推荐给喜欢交涉、了解人情世故的玩家。弓＋30。",
            "You are a Commissioner appointed by the court itself, seal and all. For players who like talking their way through. Bow +30."),
  secret=(
    bi("你出身临安高门大户，身份显赫，一路顺风顺水，在朝廷领着一份闲差。一二六七年，出于某种原因（自行拟定：遭权臣构陷，或主动请命），你临危受命督军援救襄樊。",
       "You come from one of the great families of the capital. Life has been easy; you hold a comfortable sinecure. In 1267, for reasons you decide (a rival's scheme, or your own idealism), you were made Commissioner and sent to relieve the siege of the twin cities.") +
    bi("你有一位名叫刘卿堂的发小，急公好义，颇具江湖豪气。听闻你督军，他主动请缨同往，率五千兵马随你出发。",
       "Your childhood friend Liu Qingtang 刘卿堂, hot-blooded and generous, volunteered to come with you and led your five thousand men.") +
    bi("宋军疲软，蒙古兵精粮足。你们直至一二六七年末方奋力突围进入樊城，仅余八百人，损失惨重。次年一月元军大举攻城，范天顺要求你们先撤往襄阳暂避。但你突围时受伤未愈（伤势自行拟定），难耐奔波，只得暂缓。一月三日，刘卿堂先率八百余人渡江赴襄阳。次日，范玉楼主事，樊城开城投降。",
       "The Mongols cut you to pieces. By the end of 1267 you broke through into Fencewall with eight hundred men left. In January the assault began and Commander Fan ordered you across to Southbright. You were still carrying a wound from the breakout (you decide what) and could not travel. On 3 January Liu took the eight hundred across the river. The next day Magistrate Fan surrendered the city.") +
    bi("汉江以北已尽入蒙古之手。你必须渡江南返，与同袍会合。",
       "Everything north of the river is Mongol now. You must cross to Southbright and rejoin your men.")),
  build=ul([
    ("高门贵胄，围猎常拔头筹：弓＋30。", "A noble's upbringing and a hunter's eye: Bow +30."),
    ("气质雍容：外貌＋10；名师大儒教导：教育＋10，且不低于70。", "APP +10; EDU +10 and never below 70."),
    ("朝廷文职，是否有行伍经历自行拟定。", "A civil post; whether you have seen battle before is up to you."),
    ("这些加值已在预设卡上计入。", "These bonuses are already on your pre-built sheet."),
  ]))

def ho_html(n):
    d = HO[n]
    s = f'<h1>{d["title_zh"]}<br><small>{d["title_en"]}</small></h1>'
    s += h("公开信息", "Public") + d["public"]
    s += h("你的秘密（仅本人阅读）", "Your secret (for your eyes only)") + d["secret"]
    s += h("车卡要求", "Character requirements") + d["build"]
    return s

# ---------------- CHEAT SHEET ----------------
def cheat_html():
    s = h("规则速查", "Rules Cheat Sheet", 1)
    s += h("一个核心规则", "The one rule")
    s += bi("掷d100，结果小于等于技能值即成功。小于一半为困难成功，小于五分之一为极难成功。01大成功；100（技能低于50时96–100）大失败。",
            "Roll d100. Equal to or under your skill = success. Under half = Hard success; under a fifth = Extreme. 01 is a critical; 100 (or 96–100 if the skill is below 50) is a fumble.")
    s += ul([
      ("奖励骰/惩罚骰：多掷一个十位骰，取好/取坏。", "Bonus / penalty die: roll an extra tens die, keep the better / worse."),
      ("孤注一掷：失败后可描述更冒险的做法重掷一次；再失败则有恶果。", "Push: after a failure, describe a riskier attempt and reroll once; fail again and something bad happens."),
      ("对抗：双方掷骰，成功等级高者胜。", "Opposed roll: both roll, higher success level wins."),
      ("幸运：可花幸运点把失败的骰子补成成功（1点换1）。", "Luck: spend Luck points one-for-one to turn a failed roll into a success."),
    ])
    s += h("战斗", "Combat")
    s += ul([
      ("按敏捷顺序行动，每轮一个动作。", "Act in DEX order, one action a round."),
      ("被攻击时选择闪避或反击；双方比较成功等级。", "When attacked, Dodge or Fight Back; compare success levels."),
      ("重伤：一次失去一半以上最大生命值 → 体质检定，否则昏迷。生命值归零且重伤 → 濒死。", "Major wound: lose half your max HP in one hit → CON roll or pass out. 0 HP with a major wound → dying."),
      ("护甲减去伤害。蒙古士兵护甲2。", "Armour subtracts from damage. Mongol soldiers have 2."),
    ])
    s += h("本模组的武侠规则", "This scenario's wuxia rules")
    s += ul([
      ("<b>轻功</b> = 攀爬与跳跃。翻城墙、上屋顶、飞身过河沟都用这两项。", "<b>Lightness</b> = Climb and Jump. Scaling walls, roofs and leaps use these two skills."),
      ("<b>点穴</b>：任何人都可以使用的自定义技能（HO2基础50，其他人基础10）。模组原附件缺失，在拿到作者附件前使用以下临时规则：对目标进行点穴对抗体质；成功则目标麻痹1D3轮或本次攻击无视护甲。对不死仆从：命中其脊背的注入点即直接杀死（决战中如此）。凌家绣花针＋10%。",
             "<b>Acupoint Strike</b>: a custom skill anyone may use (HO2 base 50, others base 10). The author's rules attachment is missing; until we have it, use this house rule: Acupoint Strike opposed by the target's CON; success paralyses the target for 1D3 rounds or lets this attack ignore armour. Against the Undying Servants a hit on the injection scar on the spine kills outright (as in the finale). The Ling family needles give +10%."),
      ("<b>属性与技能上限（作者参考值）</b>：属性80/30，技能75/55。HO加值可以超过上限。", "<b>Caps (author's reference)</b>: attributes 80 max / 30 min; skills 75 max / 55 for the second tier. HO bonuses may exceed them."),
      ("<b>不建议低意志</b>：江中之物每晚会尝试“梦引”，用意志对抗。", "<b>Don't go low on POW</b>: the thing in the river tries its Dream-Call every night, an opposed POW roll."),
      ("<b>行动轮</b>：正式开始后每天早、中、晚各一轮自由行动；吃饭、去酒肆、找秋筠帮忙不消耗行动轮。", "<b>Action rounds</b>: once the sandbox starts, three free-action rounds a day (morning, noon, evening). Meals, the Wineshop and Autumn's help do not cost a round."),
      ("<b>理智</b>：目睹怪异时掷理智；格式“0/1”表示通过失0、失败失1。", "<b>Sanity</b>: roll SAN when you see something wrong; \"0/1\" means lose 0 on a pass, 1 on a fail."),
    ])
    s += h("时间与距离", "Time and distance")
    s += ul([
      ("一个时辰 = 两小时。子时 = 深夜十一点至一点。", "One shichen = two hours. The Hour of the Rat = 11 pm to 1 am."),
      ("汉江襄樊段宽约四百五十丈（1.5公里）。今夜能见度约十米。", "The river between the two cities is about 1.5 km wide. Tonight you can see about 10 m."),
      ("一步 ≈ 1.5米；四百步 ≈ 600米。", "One pace ≈ 1.5 m; four hundred paces ≈ 600 m."),
    ])
    return s

# ---------------- GM RUNBOOK (session 0) ----------------
def runbook_html():
    s = h("主持人：第零次聚会流程", "GM Runbook: Session 0", 1)
    s += bi("目标：介绍三位角色、跑完三段个人导入和公共导入“夜渡汉水”，在公布樊城地图前停下。约2.5–3小时。",
            "Goal: introduce the three characters, run the three personal intros and the shared intro \"Night Crossing\", and stop just before the town map is revealed. About 2.5–3 hours.")
    s += h("流程", "Agenda")
    s += ul([
      ("15分钟：玩家入门（见《玩家入门》日志）。", "15 min: the Player Primer journal."),
      ("60分钟：发放各自的HO手册，调整预设卡（名字、药行、武器、伤口、背景）。", "60 min: hand out each HO journal privately; players personalise the pre-built sheets (name, pharmacy, weapon, wound, backstory)."),
      ("3×12分钟：个人导入，其他玩家暂时离席。", "3 × 12 min: personal intros, other players step out."),
      ("45分钟：公共导入“夜渡汉水”。", "45 min: the shared scene, Night Crossing."),
      ("收尾：到达棺材铺、吃到“酥糖”后停下，预告下次公布地图与行动轮。", "Wrap: stop at the coffin shop after the ginger \"candy\"; preview the map and action rounds for session 1."),
    ])
    s += h("导入前的注意", "Before you start")
    s += ul([
      ("先读《塔楼》终战规则（原文第41–42页）：牛富的神臂弓、凌家绣花针、火光信号都是终战前置物。", "Read the finale (Watchtower, pp. 41–42 of the original): Niu's God-Arm Bow, the Ling needles and a fire signal are prerequisites. Keep them in mind from day one."),
      ("作者提示：玩家可能觉得压力大，鼓励他们大胆行事。", "Author's note: players may feel the pressure; encourage them to act boldly."),
      ("导入只是正式开始前的一段；与关联NPC（段游衍、越南柯、刘卿堂）的相处可酌情加戏。", "The intros are a prologue; feel free to add scenes with each PC's linked NPC (Duan, Doctor Yue, Captain Liu)."),
    ])
    # HO1 intro
    s += h("个人导入 HO1：庆功宴刺杀（场景：樊城衙署·庆功宴）", "Personal intro HO1: the banquet (scene: The Victory Banquet)")
    s += bi("咸淳三年末，樊城三日即降。山阳道人不眠不休三日，于清晨将成名剑“止水”赠予你，要你效仿荆轲、聂政刺杀兀良哈·阿术。",
            "Fencewall fell in three days. The Hermit did not sleep for three nights, then at dawn gave you Stillwater and told you to kill Marshal Ashu as the assassins of old killed tyrants.")
    s += bi("<b>赠剑（读给玩家）：</b>第四天清晨，师父把一柄三尺长剑横放在你面前。剑鞘旧得发白，剑身却亮得照得见人，靠近剑锷处有一道墨痕，像一片没擦干的水迹。他说：这剑叫止水。",
            "<b>The sword (read aloud):</b> On the fourth morning your master lays a sword across the table in front of you. The sheath is worn pale; the blade is bright enough to show your face, and near the guard there is a dark stain, like water that never dried. \"Her name is Stillwater,\" he says.")
    s += '<blockquote>' + bi("“你师父我老啦，怕是走不进那蒙古鞑子十步。你虽年纪轻轻，但足有乱军之中取敌方首级的本事。不为那大宋稀里糊涂的官家，为的是汉水边的百姓！若是能取兀良哈这厮项上人头，今年清明就把他的首级跟着一壶梅子酒一壶枇杷酒两斤牛肉一个猪头两只烧鸡三个烧饼一起供给我；若是不能，你便自在逍遥闯荡江湖去，去哪都成，等到这中原安定了再回来！”",
            "\"Your master is old. I could not get within ten paces of that Mongol. You are young, and you can take a head out of the middle of an army. Not for that muddle-headed emperor; for the people on the banks of the Han! If you take Ashu's head, lay it on my grave-table this Tomb-Sweeping Day with a jug of plum wine, a jug of loquat wine, two catties of beef, a pig's head, two roast chickens and three sesame cakes. If you cannot, go and wander the jianghu, anywhere you like, and come home when the Central Plains are at peace.\"") + '</blockquote>'
    s += '<blockquote>' + bi("“剑上这道黑，是雨师墨。江湖上传是赤松子留下的仙术，其实是荆湖一带的毒。刀饮即腐：沾了它的伤口烂而不死，逢阴雨便发，一辈子好不了。所以不可轻率出剑；这东西沾了谁，谁便一辈子记得你。你自己的刀照旧用，止水只为一个人出鞘。”",
            "\"That black on the blade is Rainmaster's Ink. In the jianghu they say it is Red Pine's immortal art; it is only a poison from these river marshes. What it cuts, rots: the wound will not kill, and it will not heal, and every rainy day it opens again for the rest of a man's life. So do not draw her lightly. Whoever she touches will remember you until they die. Keep using your own blade; Stillwater leaves the sheath for one man only.\"") + '</blockquote>'
    s += bi("（师父把这话叮嘱了三遍。之后不必再解释；玩家自会在阿术伤口不愈时想起。）",
            "(He says this three times. Don't explain further; the player will remember it when Ashu's wound refuses to heal.)")
    s += bi("（段游衍已写信向山阳道人保证会保护HO1；若HO1追问，师父只会含糊其辞。）",
            "(Duan Driftwood has written to the Hermit promising to protect HO1. If HO1 presses, the master is evasive.)")
    s += bi("进城：城门有兵检查，混入需乔装/幸运；翻墙需攀爬/跳跃。阿术不许士兵劫掠，城中除遍地巡逻兵外百姓照常生活。",
            "Getting in: the gates are checked. Disguise or Luck to slip through; Climb or Jump to go over the wall. Ashu forbids looting, so the town is calm apart from patrols everywhere.")
    s += bi("今晚是犒赏三军的庆功宴，鸡鸭牛羊和美酒一车车运进衙署。宴会厅由宋官操办，却处处迎合蒙古口味：烤肉代替精致菜肴，酒盏换成手掌大的瓷碗，宋女歌舞，蒙古人看直了眼。",
            "Tonight is the victory feast; carts of poultry, beef, mutton and wine roll into the Magistracy. The hall was laid out by Song officials to Mongol taste: roast meat instead of delicacies, palm-sized bowls instead of wine cups, Song dancers the Mongols cannot stop staring at.")
    s += bi("阿术坐上首：身高八尺，体格健壮，皮肤粗糙，留胡须，戴毡帽，穿软甲，手边一把厚重马刀。段游衍坐在他右手下一位。范玉楼、许德显等宋官在座，范玉楼的吹捧尤其夸张。",
            "Ashu sits on the dais: well over six feet, heavy-built, weathered skin, bearded, in a felt hat and soft armour, a huge sabre at his hand. Duan Driftwood sits one seat down on his right. Song officials are present, Magistrate Fan and Prefect Xu among them; Fan's flattery is embarrassing.")
    s += bi("<b>出剑：</b>HO1趁阿术不备拔剑，他避过要害，剑刃落在惯用手肩膀。阿术踢开案几，抄起马刀劈来：闪避成功则躲开，否则受1D4伤害，伤口深可见骨，生命值上限-1。",
            "<b>The strike:</b> Ashu twists so the blade takes his sword-arm shoulder instead of his throat, kicks the table over and swings the sabre. Dodge to avoid it; otherwise 1D4 damage, a wound to the bone, and max HP -1.")
    s += bi("止水上的雨师墨使阿术的伤口无法愈合：整个模组中他的所有检定都带一个惩罚骰。",
            "The Rainmaster's Ink on Stillwater means Ashu's wound will not heal: every roll he makes for the rest of the scenario carries a penalty die.")
    s += bi("护卫围上，弓弦绞紧。HO1可与士兵搏斗或继续攻击阿术。一轮后段游衍挡在两人之间，表面护主，实则搅乱场面：",
            "Guards close in, bows drawn. HO1 may fight the soldiers or keep going for Ashu. After one round Duan steps between them, apparently to shield the marshal, actually to make chaos:")
    s += '<blockquote>' + bi("“谁敢放箭？！大帅还在这里呢！！大帅，您先走！！有末将在，这刺客定然没办法伤到您一根汗毛！！天啊，大帅竟然受伤了？！还不快护着大帅撤退！！你们还愣着干什么！！”",
            "\"Who dares shoot? The Marshal is right here! Marshal, go, go! While I stand here this assassin will not touch a hair of yours! Heaven, the Marshal is wounded! Get him out, get him out! What are you all standing there for?!\"") + '</blockquote>'
    s += bi("阿术要他让开，他也生生挡着。HO1趁乱脱身，藏入樊城。之后：被抓只是时间问题，浮桥已断，江岸有兵；但只要钱到位，总有人铤而走险。晚间你带着全副身家来到江岸芦苇丛，其他想过河的人也在那里。→ 公共导入。",
            "Even when Ashu tells him to move he stays put. HO1 slips away and goes to ground. Afterwards: it is only a matter of time before they find you. The bridge is cut and the bank is guarded, but money finds a boatman. That night you bring everything you own to the reeds on the bank, where other would-be passengers are waiting. → Night Crossing.")
    # HO2 intro
    s += h("个人导入 HO2：截杀与入城（场景：樊城·北门）", "Personal intro HO2: the convoy and the gate (scene: Fencewall, the North Gate)")
    s += bi("<b>时间与形势：</b>咸淳三年腊月末（1267年12月），比庆功宴早两周。樊城尚未陷落：元军已在城外扎营围城，城头仍是宋军旗帜，北门戒严。药行奉朝廷调令押送一批药材作军资，父亲亲自随行；车队从南边官道而来，在樊城北门外撞上元军的围城线。为首的蒙古将军汉话不利索，身后的汉人将军只好交涉。那是兀良哈·脱欢与段游衍，两人不太对付。",
            "<b>When and where:</b> the end of December 1267, two weeks before the banquet. Fencewall has not fallen yet: the Mongols are camped outside the walls laying siege, Song banners still fly on the battlements, and the North Gate is under martial law. The pharmacy is under court orders to deliver a convoy of medicine as army supplies; your father leads it himself. Coming up the road, the convoy runs straight into the Mongol siege line outside the North Gate. The Mongol officer barely speaks Chinese; the Chinese general beside him does the talking. They are Toghan and Duan Driftwood, and they do not like each other.")
    s += '<blockquote>' + bi("“他问你们，这批药材是送往何处？作何用途？你们是接了荆湖转运的调令吗？”汉人将军侧过头看了那蒙古将军一眼，压低声音：“这鞑子怕是知道你们是巨富，不让你们脱一层皮估计是讨不了好的。有什么值钱的玩意都先呈上来，向大汗和元帅表表心意……”",
            "\"He asks where this medicine is going and what for. Are you under orders from the Jinghu transport office?\" The Chinese general glances at the Mongol and lowers his voice. \"This Tartar knows your house is rich. He won't let you go without skinning you. Whatever you have of value, offer it up now, as a gift to the Khan and the Marshal...\"") + '</blockquote>'
    s += bi("无论答应与否，父亲都独自上前交涉，让HO2去队尾与伙计清点。伙计劝HO2偷偷离开。队首传来嘈杂声：交涉失败，父亲身首分离。<b>▶ 此时播放音效「斩 Slash」</b>（播放列表 → 音效 Sound effects）。",
            "Whatever you answer, your father goes forward alone and sends you to the rear to count stock with the clerks. The clerks beg you to slip away. Then noise from the front: the talk has failed, and your father is beheaded. <b>▶ Play the 斩 Slash sound effect here</b> (Playlists → 音效 Sound effects).")
    s += '<blockquote>' + bi("一蓬血雾扬起，紧接着是一颗随着刀刃的势头斜飞而出的头颅——你爹头一次飞这么高，掉落在地上又那般重。马蹄和车辙相继碾过去，这一滩血迹消失得无影无踪。",
            "A mist of blood, then a head flung sideways by the stroke of the blade. Your father never flew so high, and never fell so heavily. Hooves and cart-wheels roll over the spot until the stain is gone.") + '</blockquote>'
    s += bi("HO2只能逃入樊城：敏捷检定判断是否受伤，失败扣1D3且本模组内无法痊愈，生命值上限-1。",
            "You run for Fencewall. DEX roll: on a failure take 1D3, a wound that will not fully heal in this scenario, and max HP -1.")
    s += bi("城门戒严：守门的是宋兵，吊桥半起，城头弓弩对着城外。信誉/交涉说服卫兵放行。若表明是药行少东家领朝廷指令而来，巡视城门的牛富会上前交谈；即使不说，HO2也能注意到这位身背漆黑强弓的将军。牛富可告知樊城近况与范天顺在城中捉贼的消息，并答应HO2提出的任何合理请求。",
            "The gate is under martial law: Song soldiers hold it, the drawbridge is half up, crossbows on the wall point outward. Credit Rating or Persuade to get in. If you say you are the pharmacy heir on court business, Niu the Archer, inspecting the gate, comes to talk; even if not, you notice the general with the black bow on his back. He tells you the news (Commander Fan is hunting a thief in town) and promises to help with anything you ask.")
    s += '<blockquote>' + bi("<b>牛富（读给玩家）：</b>城头走下来一个人。四十来岁，黝黑精瘦，披一身旧铁甲，背上斜挂一把漆黑的长弓，比常人的弓长出一截，弓背上缠着磨白的皮条。目光如炬：先看你的手，再看你的车，最后才看你的脸。守门兵见了他都往后让半步。他只报了名号：牛富，樊城钤辖，范将军麾下掌兵。",
            "<b>Niu the Archer (read aloud):</b> A man comes down from the wall. Forties, dark-skinned, lean and hard as a drawn bowstring, in old iron armour. Slung across his back is a long black bow, a hand longer than any you have seen, its grip wrapped in leather worn pale. Eyes like torches: he looks at your hands first, then at your carts, and only then at your face. The gate guards step back half a pace as he passes. He gives only his name and office: Niu, garrison commander of Fencewall, under Commander Fan.") + '</blockquote>'
    s += bi("（牛富是樊城钤辖，范天顺之下掌兵马。两军对阵前他一箭射死了阿术的侄子，蒙古人记着这笔账。他对HO2直率、客气，说到做到——只要他还自由。）",
            "(Niu is the garrison commander under Commander Fan. Before the armies met he shot Ashu's nephew dead with a single arrow; the Mongols have not forgotten. With HO2 he is blunt, courteous, and keeps his word, for as long as he is free.)")
    s += bi("（这副可射四百步的神臂弓，不久后牛富入狱时会交到打更少年方未名手里。）",
            "(That bow shoots four hundred paces. When Niu is thrown in the gaol it will pass to Nameless Fang, the watchman boy.)")
    s += bi("住客栈或被百姓收留可听到街头琐碎情报：穷凶极恶的疤脸女亡命徒（秋筠）、寺庙的醉和尚、神出鬼没的打更人。",
            "At an inn or a townsman's house you pick up gossip: a scarred woman outlaw (Autumn), a drunk monk at the temple, a night watchman who is everywhere.")
    s += bi("<b>数日后（叙述）：</b>没安歇几天，元军总攻。一月三日，守将范天顺不肯降，在衙署自缢殉国；次日他的侄子范玉楼开城献降，以保全城中几万百姓。阿术下令不得劫掠，街上却到处是蒙古巡逻兵。牛富拒降，被下了大狱——他答应你的事，也就随他的自由一起没了。父亲身死的消息不知有没有传到江对岸，你家在临安府的偌大产业如今群龙无首：你必须回去。",
            "<b>Days later (narrate):</b> You have barely rested when the assault comes. On 3 January Commander Fan 范天顺 refuses to surrender and hangs himself in the Magistracy; the next day his nephew, Magistrate Fan 范玉楼, opens the gates to spare the tens of thousands inside. Marshal Ashu forbids looting, but Mongol patrols now walk every street. Niu refused to surrender and is in the gaol; his promises to you died with his freedom. Nobody knows if word of your father's death has reached the far bank, and your family's great house in the capital, Lin'an 临安, is leaderless. You have to get home.")
    s += bi("可汉江上连通襄樊的浮桥已被截断，江岸日夜有兵把守，城里的人很难和对岸通上消息。好在只要钱到位，总有人愿意铤而走险。你四处打听，入夜后带着全副身家，来到江岸边一处不引人注目的芦苇丛——别的想过河的人，也都聚在了那里。→ 公共导入。",
            "But the floating bridge between the two cities has been cut, soldiers watch the bank day and night, and no one in town can get word across. Still, where there is money there is someone willing to risk it. You ask around, and after dark you come, with everything you own, to an unremarkable clump of reeds on the riverbank, where the other people who mean to cross tonight have gathered too. → Night Crossing.")
    # HO3 intro
    s += h("个人导入 HO3：衙署逃脱（场景：樊城衙署）", "Personal intro HO3: escape from the Magistracy (scene: Fencewall Magistracy)")
    s += bi("朝廷命你为宣抚使发兵救援襄樊。刘卿堂请缨，率五千人随行。蒙古人以樊城为饵伏击，你们几乎毫无还手之力，幸得刘卿堂指挥，余八百人突入樊城。",
            "The court names you Commissioner and sends you to relieve the twin cities. Captain Liu volunteers and brings five thousand men. The Mongols ambush you outside Fencewall; only Liu's handling saves eight hundred, who break into the city.")
    s += bi("范天顺设宴接待：陪席的范玉楼、范天顺之女范玉莹、许德显、牛富皆无心享乐。牛富黝黑精瘦、孔武有力、目光如炬；许德显体态富贵、满面油光。宴后范玉楼领你去住所，一路寒暄夸捧，并暗示汉江异状：今冬暖和，水势很大。",
            "Commander Fan gives a dinner nobody enjoys. Present: Magistrate Fan, Lady Fan, Prefect Xu and Niu the Archer. Niu is dark, lean, hard-muscled, with eyes like torches; Xu is fat and shiny. Afterwards Magistrate Fan walks you to your lodging, flattering you all the way and dropping hints: a warm winter, the river running strangely high.")
    s += bi("未几蒙古全面攻城。范天顺请你与刘卿堂带余兵先往襄阳。出发定在中午；你因伤未愈留下休息。刚过午后，衙署外骚乱，晴天骤然阴沉如夜却无雨。仆役四散，蒙古骑兵闯入官邸抄家捉人。",
            "Then the full assault. Commander Fan orders you and Liu across to Southbright at noon; your wound keeps you in bed. Just past noon: uproar outside, the clear sky goes dark as night without a drop of rain, servants scatter, and Mongol cavalry ride into the compound seizing people.")
    s += bi("<b>检定：</b>用合理方式潜行/困难幸运离开衙署；失败则接受蒙古士兵不讲道理的盘问，任何可疑之处都会被抓。强行逃离也可以，失败可能添新伤。",
            "<b>Roll:</b> Stealth, or Hard Luck, to get out with some plausible plan; fail and you face soldiers who arrest anyone suspicious. Fighting your way out is allowed; a failure means another wound.")
    s += bi("之后HO3在城中暂时落脚。浮桥已断，江岸有兵，你必须马上到对岸与同袍汇合。好在只要钱到位……→ 公共导入。",
            "You hide in the town. The bridge is gone, the bank guarded; you must cross and rejoin your men. Money finds a boatman... → Night Crossing.")
    # Common intro
    s += h("公共导入：夜渡汉水（场景：汉江夜渡）", "Shared intro: Night Crossing (scene: Night Crossing of the Han River)")
    s += bi("一二六八年一月十一日子时。无星无月，浓雾遮天，远处只有近岸几点灯火——蒙古军日夜驻守。襄樊间河段宽四百五十丈，今夜能见度约十米。你们陆续来到樊城东的芦苇荡，守军三个时辰换岗，此刻正交接。芦苇一人多高，足以藏船。船夫来得稍迟；等候的有三人——今夜的旅客不止一位。",
            "Midnight, 11 January 1268. No stars, no moon, fog over everything; only a few watch-fires on the bank, where the Mongols keep guard day and night. The river is 1.5 km wide; tonight you can see ten metres. You arrive one by one at the Reed Marsh east of Fencewall. The guards change every six hours, and this is the change. The reeds stand taller than a man. The boatman is late; three of you are waiting. You are not the only passenger tonight.")
    s += ul([
      ("<b>侦查：</b>离岸不远有几只小船，均未点灯，行得极慢——其他趁夜渡河的人。", "<b>Spot Hidden:</b> several small boats offshore, unlit, barely moving: other night-crossers."),
      ("<b>灵感：</b>寒冬深夜，不是起雾的天气。", "<b>Idea:</b> midwinter, midnight; this is not fog weather."),
    ])
    s += bi("船夫姓王，粗麻布衣，斗笠，只剩一条手臂，腰缠脏毛巾。他看得出你们不是本地人，看得出HO3气度不凡。他痛骂蒙古人暴虐，抱怨朝廷不作为。可问出：",
            "The boatman is called Wang: coarse hemp, a straw hat, one arm, a filthy towel at his belt. He can tell you are not local and that HO3 is somebody. He curses the Mongols and the court. He will tell you:")
    s += ul([
      ("断臂：世代打渔，被征作民夫搬运粮草时被马车压断。", "The arm: fisherman for generations; crushed by an army cart when he was pressed as a porter."),
      ("范天顺：勤政爱民，治军严苛，能为卒吮脓；朝廷却尽派小娃娃领兵，害他自缢。", "Commander Fan: a man who would suck the pus from a soldier's wound; the court sent him children to command, and he hanged himself for it."),
      ("江上异象：汉水女神显灵，她温和自持，必会怜悯将士魂灵。", "The fog: the Lady of the Han, who is gentle and modest and surely pities the drowned soldiers."),
      ("刺杀阿术：他主动提起，游侠的美名传遍全城，只是生死不明。", "The assassination: he brings it up himself; the whole town praises the nameless wanderer, nobody knows if he lives."),
    ])
    s += bi("轻舟一叶，飘若浮萍。不敢点灯，行得极慢。离岸几十米，前方十米内有另一艘小渔船轮廓若隐若现（夜色漆黑，侦查-20）。",
            "A single light boat, drifting like a leaf. No lamp, dead slow. A few dozen metres out, the shape of another fishing boat shows ten metres ahead (Spot Hidden at -20 in the dark).")
    s += ul([
      ("<b>聆听：</b>前方木板折断的刺耳声，几声惊恐呼喊。", "<b>Listen:</b> the shriek of splitting planks ahead, then screams."),
      ("<b>侦查：</b>渔船剧烈晃动，闪动的人影皆持兵器。", "<b>Spot Hidden:</b> the boat rocks violently; the figures on it hold weapons."),
    ])
    s += bi("无论是否接近，那船上的人匆忙点灯。借那一点亮光，你们看见船体被一条巨大脊刺摧毁（<b>理智 0/1</b>）：",
            "Whether or not you close in, they light a lamp. By that scrap of light you see the boat destroyed by an enormous spine (<b>SAN 0/1</b>):")
    s += '<blockquote>' + bi("那艘渔船力胜不过二十石，被那样一条巨大触足横穿而过，几乎生生折断。触足末端卷曲，肥大柔软，表皮却极其坚硬，倒刺遍布，反射着凛凛寒光。浓雾中灯火照得人影绰绰，有人拿出武器，有人落水。那条触足只是沉默地将船舱挤压成碎片，船上的人没来得及求救就彻底没了声。",
            "A boat that could carry twenty bushels, run clean through and nearly snapped by a tentacle-like spine. Its tip curls, fat and soft, but the hide is hard as iron and bristling with barbs that catch the light. In the lamp-glow figures lurch, some drawing weapons, some going into the water. The spine simply, silently crushes the hull to splinters. Nobody has time to call for help before the sound stops.") + '</blockquote>'
    s += bi("岸上蒙古士兵发现动静，弓箭手射来，小船终将中箭沉没。<b>闪避</b>决定是否中箭（1D3）；<b>游泳</b>决定沉船后剩下多少随身物品（失败只剩调查员指定的三件）；<b>体质</b>决定是否被冰冷江水伤害（失败扣1D3）。",
            "The watch on the bank hears. Archers shoot; your boat will sink. <b>Dodge</b> or take an arrow (1D3). <b>Swim</b>: on a failure you keep only three named possessions. <b>CON</b>: on a failure the freezing water costs 1D3 HP.")
    s += bi("船夫丢下你们独自逃走。岸边两男一女游来救人。时间紧迫，他们暂不报名号，只说是城中游侠义勇，受越南柯越大夫所托守在岸边相助。随后沿小路带你们到前街一处小宅院：前半是店铺，已打烊。",
            "The boatman abandons you. From the bank two men and a woman swim out and drag you ashore. No time for names: they are townsmen, knights-errant, sent by Doctor Yue to wait for you. They lead you by back lanes to a small house on Front Street, shop in front, closed for the night.")
    s += bi("长相相似的两名男子是同卵兄弟姜楼与姜阁；高大健硕的女子曲流是店主。姜楼跳脱，姜阁沉稳，曲流严肃而细致体贴。炉火生起后才是聊天的时候：",
            "The two look-alikes are the twins Tower and Loft Jiang; the big, powerfully built woman is Winding Stream, who owns the shop. Tower is restless, Loft steady, Winding Stream stern but attentive. Once the stove is lit, they talk:")
    s += ul([
      ("<b>越南柯：</b>行走江湖，劫富济贫，来樊城不久却极受百姓爱戴。平日在前街问诊。他算出你们命中有此劫，特叫他们来相助。", "<b>Doctor Yue:</b> a wandering healer who robs the rich for the poor; new in town but adored. He sees patients on Front Street. He \"calculated\" that you would meet disaster tonight and sent them."),
      ("<b>渡河：</b>如今没人接这活了，得自己筹谋：船要坚固快速，船夫要熟水性。", "<b>Crossing:</b> nobody will take the job now; you will have to arrange it yourselves: a strong fast boat and a boatman who knows the water."),
      ("<b>船与船夫：</b>游侠中有水性极好的人，老渔夫也有经验，但钱未必打动人心。城内船只已被蒙古人征用；世家大族或官员或有藏私。", "<b>Boat and boatman:</b> some of the wanderers swim like fish, and the old fishermen know the river, but money may not be enough now. The Mongols have seized every boat in town; a great family or an official may have one hidden."),
      ("<b>脊刺：</b>曲流讶异，认为是荆楚巫师做法。姜阁：“蒙古人若要攻襄阳，非走水路不可。若汉水里盘踞着此物，蒙古人难道还能渡过去么？”", "<b>The spine:</b> Winding Stream is shocked and blames the shamans of the old Chu lands. Loft: \"If the Mongols want Southbright they must cross by water. With that thing in the river, can they?\""),
    ])
    s += bi("夜深了。曲流递给HO2一个越南柯留下的油纸包：几块酥糖，花生瓜子，色泽鲜艳，香气扑鼻。品尝就会发现其实是伪装成酥糖的生姜。",
            "It is late. Winding Stream hands HO2 an oil-paper packet left by Doctor Yue: a few pieces of nut brittle, glossy and fragrant. Taste one: it is raw ginger disguised as candy.")
    s += bi("<b>在此停下。</b>下次聚会：公布樊城地图，进入自由调查轮（每日早中晚三轮）。",
            "<b>Stop here.</b> Next session: reveal the Fencewall map and begin the free investigation rounds (three a day).")
    s += h("名词注释", "Terms")
    s += ul([
      ("沿街浮屋：百姓自支的小摊。分茶：大食楼。会馆：外商歇脚的宾馆，现为蒙古人占用。瓦子：表演娱乐场所。", "Street stalls; a 分茶 is a big restaurant; the Merchants' Hall is an inn now used by the Mongols; a 瓦子 is a playhouse."),
    ])
    return s

def timeline_html():
    s = h("主持人：时间线", "GM: Timeline", 1)
    s += table(["日期 Date", "事件", "Event"], [
      ("1266", "范天顺购得太湖石，内嵌格拉基碎片，置于解佩亭。", "Commander Fan buys the Grand Lake Stone with Gla'aki's shard and sets it in the Pavilion of the Untied Pendant."),
      ("1267 末 late", "蒙古进攻襄樊。HO2只身逃入樊城；HO3与刘卿堂退守樊城。", "The Mongols attack the twin cities. HO2 flees alone into Fencewall; HO3 and Captain Liu retreat into it."),
      ("1268-01-03", "元军总攻；范天顺在汉江召唤格拉基；刘卿堂船队全军覆没。", "Full assault; Fan summons Gla'aki in the river; Liu's flotilla is wiped out."),
      ("1268-01-04", "樊城投降。", "Fencewall surrenders."),
      ("1268-01-10", "HO1刺杀阿术未果。", "HO1 fails to kill Ashu."),
      ("1268-01-11", "公共导入：夜渡汉水失败。", "Shared intro: the night crossing fails."),
      ("1268-01-12", "浓雾翻涌，元军渡江推迟到十八日。", "Fog boils up; the Mongol crossing is postponed to the 18th."),
      ("1268-01-15 (预计 planned)", "牛富在街口问斩。", "Niu the Archer to be executed at the street corner."),
      ("1268-01-18 (预计 planned)", "元军水路三面围攻襄阳。", "Mongol river assault on Southbright."),
    ])
    s += h("真相速览（仅主持人）", "The truth in brief (GM only)")
    s += bi("范天顺1266年买下一块八十一孔太湖石，第四十六孔内嵌的青玉其实是旧日支配者格拉基的碎片（游记称“何罗鱼”，能在梦中引人走向水体）。他打算在危急时用它阻断元军渡江。元军总攻当日，他以死囚为祭在汉水中召唤格拉基，却因越南柯误触仪式提前发动，刘卿堂的八百人船队被毁，幸存者沦为不死仆从，刘卿堂成为逃脱控制的不死者。范天顺自缢。如今不死仆从昼伏夜出，混迹城中，把人诱到江边变成同类。元军无法渡江——但汉水里的东西比侵略者更可怕。",
            "In 1266 Commander Fan bought an 81-holed Grand Lake Stone; the green jade in hole 46 is a shard of the Great Old One Gla'aki (the \"Many-Headed Fish\" of old travel books, which lures people to water in dreams). He meant to use it to block a Mongol crossing. On the day of the assault he summoned it in the river with condemned prisoners as sacrifices, but Doctor Yue blundered into the rite and it fired early: Captain Liu's eight hundred were destroyed, the survivors became Undying Servants, and Liu himself became an undying man outside Gla'aki's control. Fan hanged himself. Now the Servants move by night through the town, luring victims to the bank. The Mongols cannot cross, but the thing in the river is worse than the invaders.")
    return s

def npc_ref_html():
    s = h("主持人：第零次聚会人物速查", "GM: Session-0 NPC quick reference", 1)
    s += table(["NPC", "数值 Stats", "要点 Notes"], [
      ("兀良哈·阿术 Marshal Ashu", "STR80 CON80 SIZ85 DEX70 APP50 INT75 POW60 EDU60 · HP16 DB+1D6 · 斗殴/马刀 Brawl/Sabre 75, 闪避 Dodge 70, 侦查 Spot 60", "被止水所伤后所有检定带惩罚骰。极具压迫感、几乎不可战胜。Every roll with a penalty die after Stillwater; an oppressive, near-unbeatable presence."),
      ("段游衍 Duan Driftwood", "STR65 CON65 SIZ70 DEX60 APP70 INT70 POW50 EDU65 · HP13 DB+1D4 · 剑 Sword 70, 说服 Persuade 70, 话术 Fast Talk 60, 闪避 Dodge 60, 侦查 Spot 60, 图书馆 Library 50", "贪生怕死、圆滑，对两朝皆无忠诚，却钦慕HO1的豪侠气。Cowardly and smooth, loyal to no dynasty, secretly admires HO1."),
      ("牛富 Niu the Archer", "未给数值 no stats given；按需用 use 刘卿堂 template", "黝黑精瘦，目光如炬。神臂弓射四百步。城破后被挑断手筋，囚于监牢。Lean, dark, eyes like torches. The God-Arm Bow shoots 400 paces. Tendons cut after the fall; in the gaol."),
      ("刘卿堂 Captain Liu", "STR70 CON70 SIZ70 DEX70 APP65 INT60 POW60 EDU70 · HP14 DB+1D4 · 斗殴 Brawl 75, 斧 Axe 75, 闪避 Dodge 60, 侦查 Spot 55", "逃脱控制的不死者：无脉搏，毒病无效，不死仆从优先攻击他。An undying man outside Gla'aki's control: no pulse, immune to poison and disease; the Servants target him first."),
      ("越南柯 Doctor Yue", "STR50 CON55 SIZ65 DEX50 APP75 INT75 POW60 EDU60 · HP12 DB0 · 妙手 Sleight of Hand 75, 话术 Fast Talk 70, 侦查 Spot 70, 闪避 Dodge 40", "不会武、不懂医，擅造假药与偷盗，钱散穷人。Can't fight, can't heal; fakes medicine, steals, gives to the poor."),
      ("蒙古士兵 Mongol soldier", "STR60 CON60 SIZ70 DEX45 APP45 INT45 POW50 EDU40 · HP12 DB+1D4 · 闪避 Dodge 40 · 步兵 foot: 斗殴 Brawl 40, 弓 Bow 45 · 骑兵 horse: 斗殴 45, 弓 45 · 护甲 Armour 2", "身上有武器、令牌、钱、文书，妙手可窃。Carry weapons, tokens, money, orders; Sleight of Hand to steal."),
      ("姜楼/姜阁 the Jiang twins", "STR65 CON60 SIZ65 DEX60 APP60 INT55 POW55 EDU55 · HP12 DB+1D4 · 游泳 Swim 70, 斗殴 Brawl 65, 闪避 40 · 姜楼攀爬 Tower Climb 55 / 姜阁跳跃 Loft Jump 65", "兄沉稳，弟跳脱。Elder steady, younger reckless."),
      ("曲流 Winding Stream", "STR70 CON65 SIZ70 DEX65 APP55 INT65 POW60 EDU65 · HP12 DB+1D4 · 斗殴(大刀) Brawl (big blade) 70, 闪避 65, 跳跃 Jump 60, 急救 First Aid 60", "前镖师，十年前一刀杀了偷腥的丈夫，独自经营棺材铺。性格温和，始终照顾调查员。Ex-caravan guard; killed her cheating husband ten years ago; runs the coffin shop alone. Gentle; looks after the PCs."),
      ("船夫王 Boatman Wang", "普通人 ordinary man; 驾船 Boat 60", "独臂，痛骂蒙古与朝廷；沉船后独自逃走。One-armed; curses Mongols and court; abandons you when the boat sinks."),
      ("格拉基脊刺 Gla'aki's spine", "每根脊刺护甲4、生命6（与本体共享）；斗殴40，伤害2+1D5，每轮一次。Each spine: armour 4, HP 6 (shared with the body); attack 40, 2+1D5, once a round.", "斩断一根后格拉基需休整一轮。畏火与强光；火焰穿透护甲。Cut one and it needs a round to grow another. Fears fire and light; fire ignores its armour."),
    ])
    return s
