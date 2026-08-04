/**
 * Hub-style frameless chrome wiring (L'Atelier PC Command launcher pattern).
 * Requires pywebview js_api from WindowChromeMixin:
 * window_start_drag, window_start_resize, window_minimize,
 * window_toggle_maximize, window_close.
 * Skips when ?embed=1 / body.pcd-embed.
 */
(function () {
  "use strict";

  function isEmbed() {
    try {
      if (document.documentElement.classList.contains("pcd-embed")) return true;
      if (document.body && document.body.classList.contains("pcd-embed")) return true;
      return /(?:^|[?&])embed=1(?:&|$)/.test(location.search || "");
    } catch (_) {
      return false;
    }
  }

  function ensureResizeEdges() {
    if (document.querySelector(".hub-resize-edges")) return;
    const edges = document.createElement("div");
    edges.className = "hub-resize-edges";
    edges.setAttribute("aria-hidden", "true");
    edges.innerHTML =
      '<div class="hub-resize-edge n" data-edge="top"></div>' +
      '<div class="hub-resize-edge s" data-edge="bottom"></div>' +
      '<div class="hub-resize-edge e" data-edge="right"></div>' +
      '<div class="hub-resize-edge w" data-edge="left"></div>' +
      '<div class="hub-resize-edge nw" data-edge="top-left"></div>' +
      '<div class="hub-resize-edge ne" data-edge="top-right"></div>' +
      '<div class="hub-resize-edge sw" data-edge="bottom-left"></div>' +
      '<div class="hub-resize-edge se" data-edge="bottom-right"></div>';
    document.body.appendChild(edges);
  }

  function wire() {
    if (isEmbed()) return;
    document.body.classList.add("frameless");
    ensureResizeEdges();

    const titlebar = document.getElementById("hubTitlebar");
    if (!titlebar) return;

    let apiRef = null;
    const ensureApi = () => {
      if (apiRef) return Promise.resolve(apiRef);
      return new Promise((resolve) => {
        let tries = 0;
        const tick = () => {
          const api = window.pywebview && window.pywebview.api;
          if (api) {
            apiRef = api;
            resolve(api);
            return;
          }
          if (++tries > 80) {
            resolve(null);
            return;
          }
          setTimeout(tick, 50);
        };
        tick();
      });
    };

    const call = async (method, ...args) => {
      try {
        const api = await ensureApi();
        if (api && typeof api[method] === "function") await api[method](...args);
      } catch (_) {}
    };

    const callSync = (method, ...args) => {
      if (apiRef && typeof apiRef[method] === "function") {
        try {
          apiRef[method](...args);
          return true;
        } catch (_) {}
      }
      if (window.pywebview?.api && typeof window.pywebview.api[method] === "function") {
        try {
          window.pywebview.api[method](...args);
          apiRef = window.pywebview.api;
          return true;
        } catch (_) {}
      }
      call(method, ...args);
      return false;
    };

    ensureApi().catch(() => {});

    document.getElementById("winMin")?.addEventListener("click", () => call("window_minimize"));
    document.getElementById("winMax")?.addEventListener("click", () => call("window_toggle_maximize"));
    document.getElementById("winClose")?.addEventListener("click", () => call("window_close"));

    titlebar.addEventListener("dblclick", (ev) => {
      const t = ev.target;
      if (t && t.closest("a,button,input,.win-controls,.win-btn")) return;
      call("window_toggle_maximize");
    });

    titlebar.addEventListener("mousedown", (ev) => {
      if (ev.button !== 0) return;
      const t = ev.target;
      if (t && t.closest("a,button,input,.win-controls,.win-btn,.hub-resize-edge")) return;
      callSync("window_start_drag");
    });

    document.querySelectorAll(".hub-resize-edge").forEach((el) => {
      el.addEventListener("mousedown", (ev) => {
        if (ev.button !== 0) return;
        ev.preventDefault();
        ev.stopPropagation();
        callSync("window_start_resize", el.getAttribute("data-edge") || "right");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
