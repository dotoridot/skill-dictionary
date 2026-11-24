import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { runInNewContext } from "node:vm";

const script = readFileSync(new URL("../skills/skill-dictionary/assets/theme.js", import.meta.url), "utf8");

function openPage(localStorage) {
  const events = {};
  const button = {
    setAttribute(key, value) { this[key] = value; },
    addEventListener(key, fn) { events[key] = fn; }
  };
  const document = {
    documentElement: { dataset: {} },
    addEventListener(key, fn) { events[key] = fn; },
    querySelector() { return button; }
  };
  const window = { addEventListener(key, fn) { events[key] = fn; } };
  runInNewContext(script, { document, window, localStorage });
  events.DOMContentLoaded();
  return { events, button, root: document.documentElement };
}

test("새 문서에서도 테마와 토글 상태를 복원한다", () => {
  const values = new Map();
  const storage = { getItem: key => values.get(key), setItem: (key, value) => values.set(key, value) };
  const first = openPage(storage);
  assert.equal(first.root.dataset.theme, "light");
  first.events.click();
  assert.equal(first.button["aria-pressed"], "true");
  const next = openPage(storage);
  assert.equal(next.root.dataset.theme, "dark");
  next.events.click();
  first.events.pageshow();
  assert.equal(first.root.dataset.theme, "light");
});

test("저장소 접근이 차단된 파일에서도 현재 테마를 바꾼다", () => {
  const denied = () => { throw Error("storage blocked"); };
  const page = openPage({ getItem: denied, setItem: denied });
  page.events.click();
  page.events.pageshow();
  assert.equal(page.root.dataset.theme, "dark");
  assert.equal(page.button["aria-pressed"], "true");
});
