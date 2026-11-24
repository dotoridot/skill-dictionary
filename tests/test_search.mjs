import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { runInNewContext } from "node:vm";

const load = path => readFileSync(new URL(path, import.meta.url), "utf8");
const rank = runInNewContext(load("../skills/skill-dictionary/assets/search.js") + `
  (items, input) => items.map(item => ({ id: item.id, score: searchScore(item, normalizeSearch(input)) }))
    .filter(hit => hit.score >= 0).sort((a, b) => b.score - a.score).map(hit => hit.id)
`);
const items = ["pstack", "matt-pocock"].flatMap(id => JSON.parse(load("../catalogs/" + id + ".json")).items);

test("같은 작업의 다른 표현으로도 관련 스킬을 찾는다", () => {
  for (const [id, terms] of [
    ["figure-it-out", ["계획", "설계"]], ["code-review", ["코드 리뷰", "코드 검토"]],
    ["diagnosing-bugs", ["디버깅", "원인 조사"]], ["tdd", ["테스트", "시험"]],
    ["technical-writing", ["문서화", "기술 문서"]]
  ]) {
    for (const term of terms) assert.ok(rank(items, term).includes(id), term + " → " + id);
  }
  assert.ok(!rank(items, "계획").includes("principle-type-system-discipline"));
  assert.equal(rank(items, "없는검색어 리뷰").length, 0);
});

test("이름과 요약을 우선하고 빈 검색은 원래 순서를 유지한다", () => {
  assert.equal(rank(items, "$Code_Review")[0], "code-review");
  assert.equal(rank(items, "코드 검토")[0], "code-review");
  const hits = rank(items, "계획");
  assert.ok(hits.indexOf("grill-me") < hits.indexOf("figure-it-out"));
  assert.deepEqual(rank(items, ""), items.map(item => item.id));
});
