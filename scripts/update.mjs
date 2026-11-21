// After `git pull`, re-import the adventure when the module version changed.
// The adventure ships as plain JSON (adventure.json) rather than a LevelDB pack: Foundry rewrites pack
// databases on every launch, which left pulled packs pointing at stale local files.
// Document IDs are stable, so the import updates existing world documents in place.
const MOD = "gongruo-session0";

async function reimport() {
  const res = await fetch(`modules/${MOD}/adventure.json?v=${game.modules.get(MOD).version}`, { cache: "no-store" });
  if (!res.ok) return ui.notifications.error(`${MOD}: adventure.json not found (${res.status})`);
  const Adventure = CONFIG.Adventure.documentClass;
  const adventure = new Adventure(await res.json());
  // Adventure#import also records compendium bookkeeping that needs a pack; this is the same workflow without it.
  const importData = await adventure.prepareImport({ importFields: [] });
  // The import overwrites scenes; keep which town-map places the GM has revealed so far.
  const shown = new Map(placeTiles().map(t => [t.id, t.hidden]));
  await adventure.importContent(importData);
  const restore = placeTiles().filter(t => shown.has(t.id) && shown.get(t.id) !== t.hidden).map(t => ({ _id: t.id, hidden: shown.get(t.id) }));
  if (restore.length) await townScene().updateEmbeddedDocuments("Tile", restore);
  await ui.sidebar.render();
  await game.settings.set(MOD, "importedVersion", game.modules.get(MOD).version);
  ui.notifications.info(`公若渡河: adventure re-imported (v${game.modules.get(MOD).version}).`);
}

// Town map (scene 7): every place label is a tile flagged with its place key. A hidden tile is invisible to players.
function townScene() { return game.scenes.find(s => s.tiles.some(t => t.flags?.[MOD]?.place)); }
function placeTiles() { return townScene()?.tiles.filter(t => t.flags?.[MOD]?.place) ?? []; }

// GM dialog: tick the places the players know about. Changes apply at once.
async function places() {
  if (!game.user.isGM) return;
  const scene = townScene();
  if (!scene) return ui.notifications.warn("公若渡河: town map scene not found; re-import the adventure.");
  const esc = foundry.utils.escapeHTML ?? (s => s);
  const groups = {};
  for (const t of placeTiles()) (groups[t.flags[MOD].group] ??= []).push(t);
  const rows = Object.entries(groups).map(([g, ts]) => `<h4 style="margin:8px 0 2px;border-bottom:1px solid #8884">${esc(g)}</h4>` + ts.map(t => {
    const f = t.flags[MOD];
    return `<label style="display:flex;gap:6px;align-items:baseline;padding:1px 0"><input type="checkbox" data-place="${t.id}" ${t.hidden ? "" : "checked"}>
      <span><b>${esc(f.name)}</b>${f.when ? `<br><small style="opacity:.75">${esc(f.when)}</small>` : ""}</span></label>`;
  }).join("")).join("");
  const content = `<p style="margin:0 0 4px">Ticked = players see the label. Unticked = only you see it, faded.<br>勾选＝玩家可见；未勾选＝仅主持人可见。</p>
    <p style="margin:0 0 4px"><button type="button" data-preset="start">Start of the 12th 一月十二日开局</button>
    <button type="button" data-preset="all">Show all 全部显示</button> <button type="button" data-preset="none">Hide all 全部隐藏</button></p>
    <div style="max-height:60vh;overflow-y:auto">${rows}</div>`;
  const set = updates => updates.length ? scene.updateEmbeddedDocuments("Tile", updates) : null;
  const wire = root => {
    root.querySelectorAll("input[data-place]").forEach(el => el.addEventListener("change", () => set([{ _id: el.dataset.place, hidden: !el.checked }])));
    root.querySelectorAll("button[data-preset]").forEach(b => b.addEventListener("click", async () => {
      const show = t => b.dataset.preset === "all" ? true : b.dataset.preset === "none" ? false : !!t.flags[MOD].start;
      await set(placeTiles().filter(t => t.hidden === show(t)).map(t => ({ _id: t.id, hidden: !show(t) })));
      for (const t of placeTiles()) { const el = root.querySelector(`input[data-place="${t.id}"]`); if (el) el.checked = !t.hidden; }
    }));
  };
  const title = "城图 Town map: places";
  const V2 = foundry.applications?.api?.DialogV2;
  if (V2) {
    const dlg = new V2({ window: { title }, position: { width: 420 }, content, buttons: [{ action: "close", label: "Close 关闭", default: true }] });
    await dlg.render({ force: true });
    wire(dlg.element);
  } else new Dialog({ title, content, buttons: { close: { label: "Close 关闭" } }, render: html => wire(html[0] ?? html) }, { width: 420 }).render(true);
}

async function confirm(title, content) {
  const V2 = foundry.applications?.api?.DialogV2;
  if (V2) return V2.confirm({ window: { title }, content, rejectClose: false, modal: true });
  return Dialog.confirm({ title, content });
}

Hooks.once("init", () => {
  game.settings.register(MOD, "importedVersion", { scope: "world", config: false, type: String, default: "" });
  game.gongruo = { reimport, places };
});

Hooks.once("ready", async () => {
  if (!game.user.isGM) return;
  const current = game.modules.get(MOD).version;
  if (game.settings.get(MOD, "importedVersion") === current) return;
  const ok = await confirm(
    `公若渡河 Session 0 · v${current}`,
    `<p>模组已更新到 v${current}，是否重新导入冒险内容？<br>
     Module updated to v${current}. Re-import the adventure now?</p>
     <p style="font-size:0.9em">已导入的角色、场景、日志与播放列表会被原地更新（你对它们的修改会被覆盖）。<br>
     Imported actors, scenes, journals and playlists are updated in place (your edits to them are overwritten).
     You can run it later with <code>game.gongruo.reimport()</code> in a script macro.</p>`
  );
  if (ok) await reimport();
  else if (ok === false) await game.settings.set(MOD, "importedVersion", current); // explicit "No" skips this version; closing the dialog asks again next launch
});
