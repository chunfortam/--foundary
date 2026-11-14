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
- Title-screen scene: the scenario's cover art (by the author, `assets/cover_zh.jpg`) re-lettered in English as "Crossing the Han" (`assets/cover.webp`), linked to the Banquet track.
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
