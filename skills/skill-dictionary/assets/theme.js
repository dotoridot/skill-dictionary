(() => {
  const key = "commeng.skill-dictionary.theme";
  const root = document.documentElement;
  function apply(value) {
    root.dataset.theme = value === "dark" ? "dark" : "light";
    document.querySelector("[data-theme-toggle]")?.setAttribute("aria-pressed", String(root.dataset.theme === "dark"));
  }
  function restore() {
    try { apply(localStorage.getItem(key)); } catch { apply(root.dataset.theme); }
  }
  restore();
  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("[data-theme-toggle]");
    apply(root.dataset.theme);
    button.addEventListener("click", () => {
      apply(root.dataset.theme === "dark" ? "light" : "dark");
      try { localStorage.setItem(key, root.dataset.theme); } catch { /* Restricted storage keeps this page's choice. */ }
    });
  });
  document.addEventListener("pointerdown", event => {
    if (event.target.id === "query" && event.button === 0) event.target.dataset.pointerFocus = "";
  });
  document.addEventListener("focusout", event => {
    if (event.target.id === "query") delete event.target.dataset.pointerFocus;
  });
  document.addEventListener("click", event => {
    if (event.target.id !== "query" || !event.detail) return;
    if (matchMedia("(prefers-reduced-motion: reduce), (forced-colors: active)").matches) return;
    const light = document.querySelector(".search-light rect");
    for (const previous of light.getAnimations()) previous.cancel();
    light.animate([
      { strokeDashoffset: "9", opacity: 0 },
      { opacity: 1, offset: .05 },
      { opacity: 1, offset: .88 },
      { strokeDashoffset: "-91", opacity: 0 }
    ], { duration: 850, easing: "linear" });
  });
  window.addEventListener("pageshow", restore);
  window.addEventListener("storage", event => { if (event.key === key || event.key === null) restore(); });
})();
