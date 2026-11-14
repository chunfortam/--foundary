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
  await adventure.importContent(importData);
  await ui.sidebar.render();
  await game.settings.set(MOD, "importedVersion", game.modules.get(MOD).version);
  ui.notifications.info(`公若渡河: adventure re-imported (v${game.modules.get(MOD).version}).`);
}

async function confirm(title, content) {
  const V2 = foundry.applications?.api?.DialogV2;
  if (V2) return V2.confirm({ window: { title }, content, rejectClose: false, modal: true });
  return Dialog.confirm({ title, content });
}

Hooks.once("init", () => {
  game.settings.register(MOD, "importedVersion", { scope: "world", config: false, type: String, default: "" });
  game.gongruo = { reimport };
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
