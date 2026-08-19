/**
 * QrTools — Lot (batch) panel
 * © 2026 Mr-Aurevo-X · QrTools
 */
(() => {
  "use strict";

  const BATCH_I18N = {
    fr: {
      inputTitle: "Entrées (une par ligne)",
      btnImport: "Importer CSV/TXT",
      btnClearInput: "Vider",
      csvMode: "Mode CSV — colonne 1 = contenu, colonne 2 = nom de fichier",
      previewEmpty: "Aperçu du 1ᵉʳ QR",
      optEcc: "Correction d'erreur (ECC)",
      optSize: "Taille (px)",
      optBorder: "Marge (modules)",
      makeZip: "Créer aussi une archive ZIP",
      btnGenerateBatch: "Générer le lot…",
      btnOpenFolder: "Ouvrir le dossier",
      countZero: "0 entrée",
      countOne: "1 entrée",
      countN: "{n} entrées",
      truncated: " (limité à {max})",
      generating: "Génération de {n} QR codes…",
      resultOk: "{n}/{total} QR générés dans « {folder} »",
      resultZip: " · ZIP créé",
      resultFail: "{n} échec(s)",
      errEmpty: "Aucune entrée à générer.",
      errCancelled: "Annulé.",
      errGeneric: "Erreur : {err}",
      importedName: "Importé : {name} ({n} lignes)",
    },
    en: {
      inputTitle: "Entries (one per line)",
      btnImport: "Import CSV/TXT",
      btnClearInput: "Clear",
      csvMode: "CSV mode — column 1 = content, column 2 = file name",
      previewEmpty: "Preview of the 1st QR",
      optEcc: "Error correction (ECC)",
      optSize: "Size (px)",
      optBorder: "Margin (modules)",
      makeZip: "Also create a ZIP archive",
      btnGenerateBatch: "Generate batch…",
      btnOpenFolder: "Open folder",
      countZero: "0 entry",
      countOne: "1 entry",
      countN: "{n} entries",
      truncated: " (capped at {max})",
      generating: "Generating {n} QR codes…",
      resultOk: "{n}/{total} QR generated in \u201c{folder}\u201d",
      resultZip: " · ZIP created",
      resultFail: "{n} failure(s)",
      errEmpty: "No entries to generate.",
      errCancelled: "Cancelled.",
      errGeneric: "Error: {err}",
      importedName: "Imported: {name} ({n} lines)",
    },
  };

  let lang = "fr";
  const t = (key) => (BATCH_I18N[lang] && BATCH_I18N[lang][key]) || BATCH_I18N.fr[key] || key;
  const fmt = (key, vars) => {
    let s = t(key);
    Object.keys(vars || {}).forEach((k) => {
      s = s.split("{" + k + "}").join(vars[k]);
    });
    return s;
  };

  const $ = (id) => document.getElementById(id);
  const setStatus = (m) => {
    const el = $("statusBatch");
    if (el) el.textContent = m || "";
  };

  function apiReady() {
    return new Promise((resolve) => {
      if (window.pywebview && window.pywebview.api) return resolve(window.pywebview.api);
      window.addEventListener("pywebviewready", () => resolve(window.pywebview.api), { once: true });
      setTimeout(() => resolve(window.pywebview && window.pywebview.api), 2500);
    });
  }

  const MAX_ROWS = 2000;
  let lastFolder = null;
  let previewTimer = null;
  let active = false;

  function readOpts() {
    return {
      text: ($("inputText") && $("inputText").value) || "",
      ecc: ($("optEcc") && $("optEcc").value) || "M",
      size: parseInt(($("optSize") && $("optSize").value) || "512", 10) || 512,
      border: Math.max(1, Math.min(16, parseInt(($("optBorder") && $("optBorder").value) || "2", 10) || 2)),
      csv_mode: $("csvMode") && $("csvMode").checked,
    };
  }

  function countText(n, truncated) {
    let s = n === 0 ? t("countZero") : n === 1 ? t("countOne") : fmt("countN", { n });
    if (truncated) s += fmt("truncated", { max: MAX_ROWS });
    return s;
  }

  async function refreshPreview() {
    if (!active) return;
    const api = await apiReady();
    if (!api || !api.preview) return;
    const o = readOpts();
    try {
      const res = await api.preview(o.text, o.ecc, o.size, o.border, o.csv_mode);
      if (!res || !res.ok) return;
      if ($("countLine")) $("countLine").textContent = countText(res.count, res.truncated);
      const img = $("previewImg");
      const empty = $("previewEmpty");
      if (res.previewUrl && img && empty) {
        img.src = res.previewUrl;
        img.hidden = false;
        empty.hidden = true;
      } else if (img && empty) {
        img.hidden = true;
        empty.hidden = false;
      }
      const btn = $("btnGenerateBatch");
      if (btn) btn.disabled = res.count === 0;
    } catch (_) {
      /* ignore */
    }
  }

  function schedulePreview() {
    clearTimeout(previewTimer);
    previewTimer = setTimeout(refreshPreview, 250);
  }

  async function importFile() {
    const api = await apiReady();
    if (!api || !api.import_file) return;
    try {
      const res = await api.import_file();
      if (!res || !res.ok) {
        if (res && res.error && res.error !== "cancelled") setStatus(fmt("errGeneric", { err: res.error }));
        return;
      }
      if ($("inputText")) $("inputText").value = res.text || "";
      const lines = (res.text || "").split(/\r?\n/).filter((l) => l.trim()).length;
      setStatus(fmt("importedName", { name: res.name || "?", n: lines }));
      refreshPreview();
    } catch (e) {
      setStatus(fmt("errGeneric", { err: String((e && e.message) || e) }));
    }
  }

  async function generate() {
    const api = await apiReady();
    if (!api || !api.generate_batch) return;
    const o = readOpts();
    const preview = await api.preview(o.text, o.ecc, o.size, o.border, o.csv_mode);
    const n = (preview && preview.count) || 0;
    if (!n) {
      setStatus(t("errEmpty"));
      return;
    }
    const btn = $("btnGenerateBatch");
    if (btn) btn.disabled = true;
    setStatus(fmt("generating", { n }));
    try {
      const res = await api.generate_batch(
        o.text,
        o.ecc,
        o.size,
        o.border,
        o.csv_mode,
        $("makeZip") && $("makeZip").checked
      );
      if (!res || !res.ok) {
        if (res && res.error === "cancelled") setStatus(t("errCancelled"));
        else if (res && res.error === "empty") setStatus(t("errEmpty"));
        else setStatus(fmt("errGeneric", { err: (res && res.error) || "?" }));
        return;
      }
      lastFolder = res.folder;
      let msg = fmt("resultOk", { n: res.count, total: res.total, folder: res.folder });
      if (res.zipPath) msg += t("resultZip");
      if (res.failures && res.failures.length) msg += " · " + fmt("resultFail", { n: res.failures.length });
      if ($("resultText")) $("resultText").textContent = msg;
      if ($("resultCard")) $("resultCard").hidden = false;
      setStatus("");
    } catch (e) {
      setStatus(fmt("errGeneric", { err: String((e && e.message) || e) }));
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  async function openFolder() {
    const api = await apiReady();
    if (api && api.reveal && lastFolder) {
      try {
        await api.reveal(lastFolder);
      } catch (_) {
        /* ignore */
      }
    }
  }

  function refreshLabels() {
    document.querySelectorAll("#panel-batch [data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (key && BATCH_I18N.fr[key]) el.textContent = t(key);
    });
  }

  function wire() {
    const btnImport = $("btnImport");
    const btnClear = $("btnClearInput");
    const btnGen = $("btnGenerateBatch");
    const btnOpen = $("btnOpenFolder");
    const input = $("inputText");
    const csv = $("csvMode");
    if (btnImport) btnImport.addEventListener("click", importFile);
    if (btnClear) {
      btnClear.addEventListener("click", () => {
        if (input) input.value = "";
        if ($("resultCard")) $("resultCard").hidden = true;
        refreshPreview();
      });
    }
    if (btnGen) btnGen.addEventListener("click", generate);
    if (btnOpen) btnOpen.addEventListener("click", openFolder);
    if (input) input.addEventListener("input", schedulePreview);
    if (csv) csv.addEventListener("change", refreshPreview);
    ["optEcc", "optSize", "optBorder"].forEach((id) => {
      const el = $(id);
      if (el) el.addEventListener("change", refreshPreview);
    });
  }

  window.QrToolsBatch = {
    setLanguage(next) {
      lang = next === "en" ? "en" : "fr";
      refreshLabels();
    },
    pause() {
      active = false;
      clearTimeout(previewTimer);
    },
    resume() {
      active = true;
      refreshPreview();
    },
  };

  wire();
  active = false;
})();
