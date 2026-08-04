/**
 * QrMake — UI (proprietary)
 * © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
 * All rights reserved. Do not strip copyright notices.
 */
(() => {
  "use strict";
  // © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed

  const SUITE_I18N = {
    fr: {
      tagline: "QR · multi-payloads",
      copyright: "Copyright © 2026 Mr-Aurevo-X — tous droits réservés",
      title: "QrMake",
      subtitle: "Aperçu live · ECC · PNG",
      featuresTitle: "Fonctions",
      features:
        "Texte, URL, Wi‑Fi, contact, email, tel, SMS, geo, événement, WhatsApp, brut — aperçu live, PNG local.",
      privacy:
        "Mr-Aurevo-X ne collecte aucune donnée. Génération QR 100 % locale. Seul appel réseau optionnel : vérif. de mise à jour GitHub.",
      badgeFree: "100 % gratuit",
      legalFree: "100 % gratuit",
      legalLocal: "100 % local — aucun cloud, aucune télémétrie",
      legalUpdates: "Mise à jour non garantie — vérif. optionnelle GitHub",
      aboutTitle: "À propos — QrMake",
      aboutBody:
        "Générateur de QR codes Mr-Aurevo-X. 100 % gratuit, 100 % local. Mise à jour non garantie (pas d’obligation). L’app peut vérifier GitHub Releases et proposer une mise à jour des sources (git pull / zip).",
      aboutRights:
        "Redistribution, reverse engineering ou suppression du copyright interdits sans accord écrit.",
      btnAbout: "À propos",
      btnClose: "Fermer",
      updateTitle: "Nouvelle version disponible",
      updateDetail: "v{local} → v{remote}",
      btnUpdate: "Mettre à jour",
      btnLater: "Plus tard",
      updateApplying: "Mise à jour des sources…",
      updateDone: "Sources à jour — relancez Lancer.bat",
      updateFail: "Mise à jour impossible",
      hostMissing: "Host indisponible",
      ready: "Prêt",
      fail: "Échec",
      loading: "Génération…",
      btnGenerate: "Générer",
      btnSave: "Sauver PNG",
      btnPrint: "Imprimer",
      btnCopyImg: "Copier image",
      btnCopyPayload: "Copier payload",
      printed: "Impression lancée",
      printFail: "Impression impossible",
      copied: "Copié",
      copyFail: "Copie impossible",
      saved: "PNG enregistré",
      cancelled: "Annulé",
      emptyPreview: "Aperçu ici",
      payloadLabel: "Payload",
      modeText: "Texte",
      modeUrl: "URL",
      modeWifi: "Wi‑Fi",
      modePassword: "Mot de passe",
      modeVcard: "Contact",
      modeEmail: "Email",
      modeTel: "Tél",
      modeSms: "SMS",
      modeGeo: "Geo",
      modeEvent: "Événement",
      modeWhatsapp: "WhatsApp",
      modeRaw: "Brut",
      fieldText: "Texte",
      fieldUrl: "URL",
      fieldSsid: "SSID",
      fieldPassword: "Mot de passe",
      fieldAuth: "Sécurité",
      fieldHidden: "Réseau masqué",
      fieldHidePw: "Masquer le champ",
      fieldFullName: "Nom complet",
      fieldOrg: "Organisation",
      fieldTitle: "Titre",
      fieldTel: "Téléphone",
      fieldEmail: "Email",
      fieldNote: "Note",
      fieldTo: "Destinataire",
      fieldSubject: "Sujet",
      fieldBody: "Message",
      fieldLat: "Latitude",
      fieldLon: "Longitude",
      fieldLabel: "Libellé",
      fieldSummary: "Titre",
      fieldLocation: "Lieu",
      fieldStart: "Début",
      fieldEnd: "Fin",
      fieldAllDay: "Journée entière",
      fieldDescription: "Description",
      fieldRaw: "Payload brut",
      ecc: "ECC",
      size: "Taille PNG",
      border: "Bordure",
    },
    en: {
      tagline: "QR · multi-payloads",
      copyright: "Copyright © 2026 Mr-Aurevo-X — all rights reserved",
      title: "QrMake",
      subtitle: "Live preview · ECC · PNG",
      featuresTitle: "Features",
      features:
        "Text, URL, Wi‑Fi, contact, email, tel, SMS, geo, event, WhatsApp, raw — live preview, local PNG.",
      privacy:
        "Mr-Aurevo-X does not collect your data. 100% local QR generation. Only optional network call: GitHub update check.",
      badgeFree: "100% free",
      legalFree: "100% free",
      legalLocal: "100% local — no cloud, no telemetry",
      legalUpdates: "Updates not guaranteed — optional GitHub check",
      aboutTitle: "About — QrMake",
      aboutBody:
        "Mr-Aurevo-X QR generator. 100% free, 100% local. Updates not guaranteed (no obligation). The app can check GitHub Releases and offer a source update (git pull / zip).",
      aboutRights:
        "Redistribution, reverse engineering, or stripping copyright is forbidden without written consent.",
      btnAbout: "About",
      btnClose: "Close",
      updateTitle: "New version available",
      updateDetail: "v{local} → v{remote}",
      btnUpdate: "Update",
      btnLater: "Later",
      updateApplying: "Updating sources…",
      updateDone: "Sources updated — relaunch Lancer.bat",
      updateFail: "Update failed",
      hostMissing: "Host unavailable",
      ready: "Ready",
      fail: "Failed",
      loading: "Generating…",
      btnGenerate: "Generate",
      btnSave: "Save PNG",
      btnPrint: "Print",
      btnCopyImg: "Copy image",
      btnCopyPayload: "Copy payload",
      printed: "Print started",
      printFail: "Print failed",
      copied: "Copied",
      copyFail: "Copy failed",
      saved: "PNG saved",
      cancelled: "Cancelled",
      emptyPreview: "Preview here",
      payloadLabel: "Payload",
      modeText: "Text",
      modeUrl: "URL",
      modeWifi: "Wi‑Fi",
      modePassword: "Password",
      modeVcard: "Contact",
      modeEmail: "Email",
      modeTel: "Phone",
      modeSms: "SMS",
      modeGeo: "Geo",
      modeEvent: "Event",
      modeWhatsapp: "WhatsApp",
      modeRaw: "Raw",
      fieldText: "Text",
      fieldUrl: "URL",
      fieldSsid: "SSID",
      fieldPassword: "Password",
      fieldAuth: "Security",
      fieldHidden: "Hidden network",
      fieldHidePw: "Hide field",
      fieldFullName: "Full name",
      fieldOrg: "Organization",
      fieldTitle: "Title",
      fieldTel: "Phone",
      fieldEmail: "Email",
      fieldNote: "Note",
      fieldTo: "To",
      fieldSubject: "Subject",
      fieldBody: "Message",
      fieldLat: "Latitude",
      fieldLon: "Longitude",
      fieldLabel: "Label",
      fieldSummary: "Title",
      fieldLocation: "Location",
      fieldStart: "Start",
      fieldEnd: "End",
      fieldAllDay: "All day",
      fieldDescription: "Description",
      fieldRaw: "Raw payload",
      ecc: "ECC",
      size: "PNG size",
      border: "Border",
    },
  };

  let suiteLang = "fr";
  const t = (key) => (SUITE_I18N[suiteLang] && SUITE_I18N[suiteLang][key]) || SUITE_I18N.fr[key] || key;

  // © 2026 Mr-Aurevo-X · QrMake · provenance marker
  const MODES = [
    { id: "text", key: "modeText" },
    { id: "url", key: "modeUrl" },
    { id: "wifi", key: "modeWifi" },
    { id: "password", key: "modePassword" },
    { id: "vcard", key: "modeVcard" },
    { id: "email", key: "modeEmail" },
    { id: "tel", key: "modeTel" },
    { id: "sms", key: "modeSms" },
    { id: "geo", key: "modeGeo" },
    { id: "event", key: "modeEvent" },
    { id: "whatsapp", key: "modeWhatsapp" },
    { id: "raw", key: "modeRaw" },
  ];

  const state = {
    mode: "text",
    ecc: "M",
    size: 512,
    border: 2,
    hidePw: true,
    fields: {
      text: "QrMake — Mr-Aurevo-X",
      url: "https://github.com/Mr-Aurevo-X",
      ssid: "",
      password: "",
      auth: "WPA",
      hidden: false,
      fullName: "",
      org: "",
      title: "",
      tel: "",
      email: "",
      note: "",
      to: "",
      subject: "",
      body: "",
      lat: "48.8566",
      lon: "2.3522",
      label: "Paris",
      summary: "",
      location: "",
      start: "",
      end: "",
      allDay: false,
      description: "",
      raw: "",
    },
    payload: "",
    dataUrl: "",
  };

  const el = {
    status: document.getElementById("status"),
    modeTabs: document.getElementById("modeTabs"),
    controls: document.getElementById("controls"),
    sharedOpts: document.getElementById("sharedOpts"),
    qrPreview: document.getElementById("qrPreview"),
    qrEmpty: document.getElementById("qrEmpty"),
    payloadOut: document.getElementById("payloadOut"),
    btnGenerate: document.getElementById("btnGenerate"),
    btnSave: document.getElementById("btnSave"),
    btnPrint: document.getElementById("btnPrint"),
    btnCopyImg: document.getElementById("btnCopyImg"),
    btnCopyPayload: document.getElementById("btnCopyPayload"),
    btnAbout: document.getElementById("btnAbout"),
    aboutDialog: document.getElementById("aboutDialog"),
    updateBanner: document.getElementById("updateBanner"),
    updateTitle: document.getElementById("updateTitle"),
    updateDetail: document.getElementById("updateDetail"),
    btnUpdateNow: document.getElementById("btnUpdateNow"),
    btnUpdateLater: document.getElementById("btnUpdateLater"),
  };

  let pendingRemoteVersion = null;
  let debounceTimer = null;

  function applyAccent(hex) {
    const accent = String(hex || "#e03545").trim();
    if (!(accent.startsWith("#") && (accent.length === 4 || accent.length === 7))) return;
    let h = accent.slice(1);
    if (h.length === 3) h = h.split("").map((c) => c + c).join("");
    const r = parseInt(h.slice(0, 2), 16);
    const g = parseInt(h.slice(2, 4), 16);
    const b = parseInt(h.slice(4, 6), 16);
    const root = document.documentElement;
    root.style.setProperty("--accent", accent);
    root.style.setProperty("--accent-dim", `rgba(${r}, ${g}, ${b}, 0.2)`);
    root.style.setProperty("--accent-glow", `rgba(${r}, ${g}, ${b}, 0.4)`);
  }

  async function bootSuite(api) {
    const suite = window.MrAurevoXSuite;
    if (!suite) {
      if (api && api.get_suite_settings) {
        try {
          const s = await api.get_suite_settings();
          if (s && s.accent) applyAccent(s.accent);
          if (s && s.language === "en") suiteLang = "en";
        } catch (_) {}
      }
      return suiteLang;
    }
    const settings = await suite.loadSuiteSettings(api);
    suiteLang = settings.language === "en" ? "en" : "fr";
    suite.applyAccent(settings.accent);
    suite.applyI18n(suiteLang, SUITE_I18N);
    return suiteLang;
  }

  function apiReady() {
    return new Promise((resolve) => {
      if (window.pywebview && window.pywebview.api) return resolve(window.pywebview.api);
      window.addEventListener("pywebviewready", () => resolve(window.pywebview.api), { once: true });
      setTimeout(() => resolve(window.pywebview && window.pywebview.api), 2500);
    });
  }

  function setStatus(msg) {
    el.status.textContent = msg || "";
  }

  function scheduleGenerate() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(generate, 220);
  }

  function textField(key, label, opts) {
    const wrap = document.createElement("label");
    wrap.className = "field";
    const span = document.createElement("span");
    span.textContent = label;
    const input = document.createElement(opts && opts.multiline ? "textarea" : "input");
    if (!(opts && opts.multiline)) {
      input.type = (opts && opts.type) || "text";
    } else {
      input.rows = opts.rows || 3;
    }
    input.value = state.fields[key] || "";
    if (opts && opts.placeholder) input.placeholder = opts.placeholder;
    input.addEventListener("input", (e) => {
      state.fields[key] = e.target.value;
      scheduleGenerate();
    });
    wrap.appendChild(span);
    wrap.appendChild(input);
    return wrap;
  }

  function checkField(key, label) {
    const wrap = document.createElement("label");
    wrap.className = "check";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !!state.fields[key];
    input.addEventListener("change", (e) => {
      state.fields[key] = !!e.target.checked;
      scheduleGenerate();
    });
    const span = document.createElement("span");
    span.textContent = label;
    wrap.appendChild(input);
    wrap.appendChild(span);
    return wrap;
  }

  function selectField(key, label, options) {
    const wrap = document.createElement("label");
    wrap.className = "field";
    const span = document.createElement("span");
    span.textContent = label;
    const sel = document.createElement("select");
    options.forEach((o) => {
      const opt = document.createElement("option");
      opt.value = o.value;
      opt.textContent = o.label;
      if (state.fields[key] === o.value) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", (e) => {
      state.fields[key] = e.target.value;
      scheduleGenerate();
    });
    wrap.appendChild(span);
    wrap.appendChild(sel);
    return wrap;
  }

  function renderModes() {
    el.modeTabs.innerHTML = "";
    MODES.forEach((m) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "mode-tab" + (state.mode === m.id ? " active" : "");
      btn.textContent = t(m.key);
      btn.addEventListener("click", () => {
        state.mode = m.id;
        renderModes();
        renderControls();
        scheduleGenerate();
      });
      el.modeTabs.appendChild(btn);
    });
  }

  // © 2026 Mr-Aurevo-X · QrMake · mode controls
  function renderControls() {
    el.controls.innerHTML = "";
    const grid = document.createElement("div");
    grid.className = "grid";
    const m = state.mode;

    if (m === "text") {
      grid.appendChild(textField("text", t("fieldText"), { multiline: true, rows: 5 }));
    } else if (m === "url") {
      grid.appendChild(textField("url", t("fieldUrl"), { placeholder: "example.com" }));
    } else if (m === "wifi") {
      grid.appendChild(textField("ssid", t("fieldSsid")));
      grid.appendChild(
        textField("password", t("fieldPassword"), { type: state.hidePw ? "password" : "text" })
      );
      grid.appendChild(
        selectField("auth", t("fieldAuth"), [
          { value: "WPA", label: "WPA/WPA2" },
          { value: "WEP", label: "WEP" },
          { value: "NOPASS", label: "nopass" },
        ])
      );
      grid.appendChild(checkField("hidden", t("fieldHidden")));
      const hide = document.createElement("label");
      hide.className = "check";
      hide.innerHTML = `<input type="checkbox" ${state.hidePw ? "checked" : ""} /> <span>${t("fieldHidePw")}</span>`;
      hide.querySelector("input").addEventListener("change", (e) => {
        state.hidePw = !!e.target.checked;
        renderControls();
      });
      grid.appendChild(hide);
    } else if (m === "password") {
      grid.appendChild(
        textField("password", t("fieldPassword"), { type: state.hidePw ? "password" : "text" })
      );
      const hide = document.createElement("label");
      hide.className = "check";
      hide.innerHTML = `<input type="checkbox" ${state.hidePw ? "checked" : ""} /> <span>${t("fieldHidePw")}</span>`;
      hide.querySelector("input").addEventListener("change", (e) => {
        state.hidePw = !!e.target.checked;
        renderControls();
        scheduleGenerate();
      });
      grid.appendChild(hide);
    } else if (m === "vcard") {
      grid.appendChild(textField("fullName", t("fieldFullName")));
      grid.appendChild(textField("org", t("fieldOrg")));
      grid.appendChild(textField("title", t("fieldTitle")));
      grid.appendChild(textField("tel", t("fieldTel")));
      grid.appendChild(textField("email", t("fieldEmail")));
      grid.appendChild(textField("url", t("fieldUrl")));
      grid.appendChild(textField("note", t("fieldNote"), { multiline: true }));
    } else if (m === "email") {
      grid.appendChild(textField("to", t("fieldTo")));
      grid.appendChild(textField("subject", t("fieldSubject")));
      grid.appendChild(textField("body", t("fieldBody"), { multiline: true }));
    } else if (m === "tel") {
      grid.appendChild(textField("tel", t("fieldTel")));
    } else if (m === "sms") {
      grid.appendChild(textField("tel", t("fieldTel")));
      grid.appendChild(textField("body", t("fieldBody"), { multiline: true }));
    } else if (m === "geo") {
      grid.appendChild(textField("lat", t("fieldLat")));
      grid.appendChild(textField("lon", t("fieldLon")));
      grid.appendChild(textField("label", t("fieldLabel")));
    } else if (m === "event") {
      grid.appendChild(textField("summary", t("fieldSummary")));
      grid.appendChild(textField("location", t("fieldLocation")));
      grid.appendChild(textField("start", t("fieldStart"), { type: "datetime-local" }));
      grid.appendChild(textField("end", t("fieldEnd"), { type: "datetime-local" }));
      grid.appendChild(checkField("allDay", t("fieldAllDay")));
      grid.appendChild(textField("description", t("fieldDescription"), { multiline: true }));
    } else if (m === "whatsapp") {
      grid.appendChild(textField("tel", t("fieldTel"), { placeholder: "33601020304" }));
      grid.appendChild(textField("body", t("fieldBody"), { multiline: true }));
    } else if (m === "raw") {
      grid.appendChild(textField("raw", t("fieldRaw"), { multiline: true, rows: 6 }));
    }

    el.controls.appendChild(grid);
  }

  function renderShared() {
    el.sharedOpts.innerHTML = "";
    const grid = document.createElement("div");
    grid.className = "grid shared-grid";

    const ecc = document.createElement("label");
    ecc.className = "field";
    ecc.innerHTML = `<span>${t("ecc")}</span>`;
    const eccSel = document.createElement("select");
    ["L", "M", "Q", "H"].forEach((v) => {
      const o = document.createElement("option");
      o.value = v;
      o.textContent = v;
      if (state.ecc === v) o.selected = true;
      eccSel.appendChild(o);
    });
    eccSel.addEventListener("change", (e) => {
      state.ecc = e.target.value;
      scheduleGenerate();
    });
    ecc.appendChild(eccSel);

    const size = document.createElement("label");
    size.className = "field";
    size.innerHTML = `<span>${t("size")} <strong class="range-val">${state.size}</strong></span>`;
    const sizeIn = document.createElement("input");
    sizeIn.type = "range";
    sizeIn.min = "256";
    sizeIn.max = "1024";
    sizeIn.step = "64";
    sizeIn.value = String(state.size);
    sizeIn.addEventListener("input", (e) => {
      state.size = +e.target.value;
      size.querySelector(".range-val").textContent = String(state.size);
      scheduleGenerate();
    });
    size.appendChild(sizeIn);

    grid.appendChild(ecc);
    grid.appendChild(size);
    el.sharedOpts.appendChild(grid);
  }

  function collectFields() {
    const f = { ...state.fields };
    if (state.mode === "password") f.password = state.fields.password;
    if (state.mode === "whatsapp") {
      f.tel = state.fields.tel;
      f.text = state.fields.body;
    }
    return f;
  }

  function showPreview(dataUrl) {
    if (dataUrl) {
      el.qrPreview.src = dataUrl;
      el.qrPreview.hidden = false;
      el.qrEmpty.hidden = true;
    } else {
      el.qrPreview.hidden = true;
      el.qrEmpty.hidden = false;
    }
  }

  async function generate() {
    const api = await apiReady();
    if (!api || !api.generate) {
      setStatus(t("hostMissing"));
      return;
    }
    setStatus(t("loading"));
    try {
      const res = await api.generate(state.mode, collectFields(), state.ecc, state.size, state.border);
      if (!res || !res.ok) {
        setStatus((res && res.error) || t("fail"));
        showPreview("");
        el.payloadOut.value = "";
        return;
      }
      state.payload = res.payload || "";
      state.dataUrl = res.dataUrl || "";
      el.payloadOut.value = state.payload;
      showPreview(state.dataUrl);
      setStatus(t("ready"));
    } catch (e) {
      setStatus(String(e.message || e));
    }
  }

  async function savePng() {
    const api = await apiReady();
    if (!api || !api.save_png) return;
    try {
      const res = await api.save_png("qrmake.png");
      if (res && res.ok) setStatus(t("saved") + (res.path ? " — " + res.path : ""));
      else if (res && res.error === "cancelled") setStatus(t("cancelled"));
      else setStatus((res && res.error) || t("fail"));
    } catch (e) {
      setStatus(String(e.message || e));
    }
  }

  async function copyImage() {
    const api = await apiReady();
    try {
      if (api && api.copy_image) {
        const res = await api.copy_image();
        if (res && res.ok) {
          setStatus(t("copied"));
          return;
        }
      }
      setStatus(t("copyFail"));
    } catch (_) {
      setStatus(t("copyFail"));
    }
  }

  async function printImage() {
    const api = await apiReady();
    if (!api || !api.print_image) {
      setStatus(t("printFail"));
      return;
    }
    try {
      const res = await api.print_image();
      if (res && res.ok) setStatus(t("printed"));
      else setStatus((res && res.error) || t("printFail"));
    } catch (e) {
      setStatus(String(e.message || e) || t("printFail"));
    }
  }

  async function copyPayload() {
    const api = await apiReady();
    const text = state.payload || "";
    if (!text) return;
    try {
      if (api && api.copy_payload) {
        const res = await api.copy_payload(text);
        if (res && res.ok) {
          setStatus(t("copied"));
          return;
        }
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        setStatus(t("copied"));
        return;
      }
      setStatus(t("copyFail"));
    } catch (_) {
      setStatus(t("copyFail"));
    }
  }

  function refreshChromeLabels() {
    el.btnGenerate.textContent = t("btnGenerate");
    el.btnSave.textContent = t("btnSave");
    if (el.btnPrint) el.btnPrint.textContent = t("btnPrint");
    el.btnCopyImg.textContent = t("btnCopyImg");
    el.btnCopyPayload.textContent = t("btnCopyPayload");
    el.btnAbout.textContent = t("btnAbout");
    el.qrEmpty.textContent = t("emptyPreview");
    if (el.updateTitle) el.updateTitle.textContent = t("updateTitle");
    if (el.btnUpdateNow) el.btnUpdateNow.textContent = t("btnUpdate");
    if (el.btnUpdateLater) el.btnUpdateLater.textContent = t("btnLater");
  }

  function showUpdateBanner(info) {
    if (!el.updateBanner || !info) return;
    pendingRemoteVersion = info.remote || null;
    const detail = t("updateDetail")
      .replace("{local}", info.local || "?")
      .replace("{remote}", info.remote || "?");
    if (el.updateDetail) el.updateDetail.textContent = detail;
    if (el.updateTitle) el.updateTitle.textContent = t("updateTitle");
    if (el.btnUpdateNow) el.btnUpdateNow.textContent = t("btnUpdate");
    if (el.btnUpdateLater) el.btnUpdateLater.textContent = t("btnLater");
    el.updateBanner.hidden = false;
  }

  function hideUpdateBanner() {
    if (el.updateBanner) el.updateBanner.hidden = true;
  }

  async function runUpdateCheck(api) {
    if (!api || !api.check_for_update) return;
    try {
      const info = await api.check_for_update();
      if (!info || !info.ok || !info.updateAvailable) return;
      if (info.autoUpdate && api.apply_update) {
        setStatus(t("updateApplying"));
        const res = await api.apply_update();
        if (res && res.ok && res.applied) {
          setStatus(t("updateDone"));
          return;
        }
      }
      showUpdateBanner(info);
    } catch (_) {
      /* offline / rate-limit — silent */
    }
  }

  async function applyUpdateNow() {
    const api = await apiReady();
    if (!api || !api.apply_update) return;
    if (el.btnUpdateNow) el.btnUpdateNow.disabled = true;
    setStatus(t("updateApplying"));
    try {
      const res = await api.apply_update();
      if (res && res.ok && res.applied) {
        setStatus(t("updateDone"));
        hideUpdateBanner();
        return;
      }
      setStatus((res && res.error) || t("updateFail"));
    } catch (e) {
      setStatus(String(e.message || e) || t("updateFail"));
    } finally {
      if (el.btnUpdateNow) el.btnUpdateNow.disabled = false;
    }
  }

  async function dismissUpdateLater() {
    const api = await apiReady();
    hideUpdateBanner();
    try {
      if (api && api.dismiss_update) await api.dismiss_update(pendingRemoteVersion || "");
    } catch (_) {}
  }

  el.btnGenerate.addEventListener("click", generate);
  el.btnSave.addEventListener("click", savePng);
  if (el.btnPrint) el.btnPrint.addEventListener("click", printImage);
  el.btnCopyImg.addEventListener("click", copyImage);
  el.btnCopyPayload.addEventListener("click", copyPayload);
  el.btnAbout.addEventListener("click", () => {
    if (el.aboutDialog && el.aboutDialog.showModal) el.aboutDialog.showModal();
  });
  if (el.btnUpdateNow) el.btnUpdateNow.addEventListener("click", applyUpdateNow);
  if (el.btnUpdateLater) el.btnUpdateLater.addEventListener("click", dismissUpdateLater);

  (async () => {
    const api = await apiReady();
    await bootSuite(api);
    refreshChromeLabels();
    renderModes();
    renderControls();
    renderShared();
    await generate();
    // Non-blocking: schedule after first paint / generate
    setTimeout(() => {
      runUpdateCheck(api);
    }, 800);
  })();
})();
