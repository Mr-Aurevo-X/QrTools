/**
 * Copyright (c) 2026 Mr-Aurevo-X. All rights reserved.
 * SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
 * Author: Mr-Aurevo-X | https://github.com/Mr-Aurevo-X
 */
/**
 * QrTools — top-level Simple | Lot tabs
 * © 2026 Mr-Aurevo-X · QrTools
 */
(() => {
  "use strict";

  const TOP_I18N = {
    fr: {
      tabSimple: "Simple",
      tabBatch: "Lot",
      subtitleSimple: "Aperçu live · ECC · PNG",
      subtitleBatch: "Liste ou CSV → dossier PNG (+ ZIP optionnel)",
      featuresSimple:
        "Texte, URL, Wi‑Fi, contact, email, tel, SMS, geo, événement, WhatsApp, brut — aperçu live, PNG, impression locale.",
      featuresBatch:
        "Une entrée par ligne (ou CSV) → un QR par ligne. ECC/taille partagés. Export dossier PNG + ZIP optionnel. 100 % local.",
    },
    en: {
      tabSimple: "Simple",
      tabBatch: "Batch",
      subtitleSimple: "Live preview · ECC · PNG",
      subtitleBatch: "List or CSV → PNG folder (+ optional ZIP)",
      featuresSimple:
        "Text, URL, Wi‑Fi, contact, email, phone, SMS, geo, event, WhatsApp, raw — live preview, PNG, local print.",
      featuresBatch:
        "One entry per line (or CSV) → one QR per line. Shared ECC/size. Export PNG folder + optional ZIP. 100% local.",
    },
  };

  let lang = "fr";
  const t = (key) => (TOP_I18N[lang] && TOP_I18N[lang][key]) || TOP_I18N.fr[key] || key;

  function setTopMode(mode) {
    const simple = mode === "simple";
    document.querySelectorAll(".top-mode-tab").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.topMode === mode);
    });
    const panelSimple = document.getElementById("panel-simple");
    const panelBatch = document.getElementById("panel-batch");
    if (panelSimple) panelSimple.hidden = !simple;
    if (panelBatch) panelBatch.hidden = simple;
    const meta = document.getElementById("meta");
    if (meta) meta.textContent = t(simple ? "subtitleSimple" : "subtitleBatch");
    const feat = document.querySelector("#featureDesc span[data-i18n='features']");
    if (feat) feat.textContent = t(simple ? "featuresSimple" : "featuresBatch");
    if (simple && window.QrToolsBatch && window.QrToolsBatch.pause) {
      window.QrToolsBatch.pause();
    } else if (!simple && window.QrToolsBatch && window.QrToolsBatch.resume) {
      window.QrToolsBatch.resume();
    }
  }

  function refreshLabels() {
    document.querySelectorAll(".top-mode-tab").forEach((btn) => {
      const key = btn.dataset.topMode === "batch" ? "tabBatch" : "tabSimple";
      btn.textContent = t(key);
    });
  }

  document.querySelectorAll(".top-mode-tab").forEach((btn) => {
    btn.addEventListener("click", () => setTopMode(btn.dataset.topMode || "simple"));
  });

  window.QrToolsTabs = {
    setLanguage(next) {
      lang = next === "en" ? "en" : "fr";
      refreshLabels();
      const active = document.querySelector(".top-mode-tab.active");
      setTopMode((active && active.dataset.topMode) || "simple");
    },
  };

  setTopMode("simple");
})();
