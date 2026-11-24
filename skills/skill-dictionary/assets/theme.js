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
  window.addEventListener("pageshow", restore);
  window.addEventListener("storage", event => { if (event.key === key || event.key === null) restore(); });
})();
