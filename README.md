# 公若渡河 · Session 0 kit (Foundry VTT, CoC7)

Bilingual (中文 / English) Foundry VTT adventure module for the first session of the wuxia Call of Cthulhu scenario **公若渡河** by 江涔 (Dicecho / 魔都). For private use at your own table; the scenario text belongs to its author.

## Requirements 需求
- Foundry VTT v12–v14
- Call of Cthulhu 7th edition system **CoC7** (8.x) installed

## Install 安装
The repository is private, so install from git (Foundry's manifest-URL installer cannot reach it).

1. Clone into your Foundry user data folder; the folder name **must** be `gongruo-session0` (Foundry matches it against the module id):
   `git clone https://github.com/chunfortam/--foundary.git "<FoundryData>/Data/modules/gongruo-session0"`
   (Windows default: `%LOCALAPPDATA%\FoundryVTT\Data\modules\gongruo-session0`)
2. Restart Foundry, open your CoC7 world, enable **公若渡河 Session 0** in Manage Modules.
3. On the next load the module asks to import the adventure; click Yes. (Manual route: run `game.gongruo.reimport()` in a script macro or the F12 console.)
4. Give each player **Observer** permission on their own HO journal only (right-click the journal → Configure Ownership). The Player Primer is already visible to all players.

## Update 更新
`git pull` in the module folder, then reload Foundry (F5). When the module version has changed, a dialog offers to re-import; document IDs are stable, so existing actors, scenes, journals and the playlist are **updated in place** (your edits to those documents are overwritten; copies you made under other names are untouched). To re-import at any time, run `game.gongruo.reimport()` in a script macro.

The adventure ships as plain `adventure.json` (no compendium database), so a pull always delivers the new content and the module folder never shows local modifications.

## Contents 内容
- Actors: 3 pre-built investigators (HO1 游侠 / HO2 商贾 / HO3 命官) with the scenario's mandatory bonuses and the custom skill 点穴 Acupoint Strike; NPCs for session 0 (Marshal Ashu, Duan Driftwood, Niu the Archer, Captain Liu, Doctor Yue, Mongol soldiers and horsemen, the Jiang twins, Winding Stream, the boatman); creatures (Gla'aki's spine, Undying Servant).
- Title and idle scenes: scene 0 is the title page — the scenario's cover art (by the author, `assets/cover_zh.jpg`) re-lettered in English as "Crossing the Han" (`assets/cover.webp`); scene 0a is a looping ink-wash pagoda video (`assets/intro.webm`, our own render) for breaks. Both play the Banquet track. Scene 0c is a bilingual ink-wash regional map of the Han River with Fencewall 樊城 (north bank) and Southbright 襄阳 (south bank) (`assets/map_twin_cities.webp`), for the Primer and "where are we" questions.
- Portrait macros: three macros "肖像 …" (Macro Directory, the folder icon left of the hotbar). Drag them onto hotbar slots; one click opens the HO portrait full-screen for the GM and pushes it to every player (`ImagePopout.shareImage`). Players close it with the X.
- Journals: player pages are English-first with Chinese only on names/terms (`content.player()` strips the Chinese paragraphs and annotates the first mention of each name from `content.NAMES`). The Player Primer opens with "故事 The story so far" and "人物 Who's who" (portraits from `assets/portraits`); each HO handout opens with "Who you are"; the GM runbook has a GM "Who's who" (secrets in red) and "The whole story & timeline".
- Campaign (Days 1–6): `build/campaign.py` builds the GM journal "主持人 · GM: Campaign (Days 1–6)" (sandbox rules, the five districts location by location, the Street Crossing rescue, the Temple, the assassination, the warship raid, the Watchtower finale, optional/personal events, endings, campaign NPC stats) and the player journal "规则卡与文书 · Rules cards & handouts" (the two set-piece rules cards the book shows to players, and every letter/page/poem as a handout). English-first with Chinese on names; condensed from pp. 16–56 of the scenario.
- Scenes (80 px grid = 1 inch on a 55" 4K table): the Victory Banquet, the North Gate, the Magistracy, Night Crossing of the Han River, the Coffin Shop, and the Street Crossing for the optional Day One extension (GM Runbook → 加时 Extended: Day One).
- Journals: Player Primer + Cheat Sheet + Glossary (players); HO1/HO2/HO3 handouts (private); GM Runbook with the three personal intros and the Night Crossing, NPC quick reference, timeline and truth.
- Printables: `print/character-sheets.pdf` (one page per pregen + one secret handout per player) and `print/gm-pack.pdf` (GM checklist, agenda, scene beats with every roll, NPC card), both A4 and generated from the same data.

## Known gaps 已知缺口
- The scenario's 点穴 rules attachment is not in the published PDF; the cheat sheet contains a house rule to use until you get the attachment from the author's QQ group (1095875707).
- Niu the Archer has no stats in the original; the sheet uses GM estimates.
- Portraits and round tokens for all 16 actors are AI-generated (OpenAI gpt-image) in a Chinese ink-wash style.
- Sound effects: playlist 音效 Sound effects — 斩 Slash (HO2 intro), 箭 Arrows (Night Crossing volley), 战 Battle (sword-on-sword loop for fights); mp3s from pixabay.com under the Pixabay Content License.
- Music: a playlist of six Kevin MacLeod tracks linked to the scenes (Eastern Thought, Teller of the Tales, Asian Drums, Temple of the Manes, Lotus, Lightless Dawn). Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0 https://creativecommons.org/licenses/by/4.0/
- Maps are AI-generated (OpenAI gpt-image) for this kit, 3072x2048, gridless art with the Foundry grid set per scene (128 px = 1.5 m; coffin shop 256 px). Nudge the grid in Scene Configuration if squares feel off.


## Rebuilding 重新生成
Edit `build/content.py` (text) or `build/build.py` (actors/scenes), then from the repo root:
```
python3 build/build.py
```
Requires Python 3 with Pillow. This regenerates `adventure.json` and `module.json`.

Printables: `python3 build/print_sheets.py` and `python3 build/print_gm.py` (need Chrome/Chromium and the Noto CJK fonts) regenerate `print/character-sheets.pdf` and `print/gm-pack.pdf`.
