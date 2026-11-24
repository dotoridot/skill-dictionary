function normalizeSearch(value) {
  return value.normalize("NFKC").toLowerCase().replace(/[$/_-]/g, " ").trim().replace(/\s+/g, " ");
}

function searchScore(item, query, collection = "") {
  if (!query) return 0;
  const name = normalizeSearch(item.name);
  if (name === query) return Infinity;
  const summary = normalizeSearch(item.summary);
  const keywords = (item.keywords || []).map(normalizeSearch);
  const context = normalizeSearch([item.category, item.when, collection].join(" "));
  let score = 0;
  for (const term of query.split(" ")) {
    if (name.includes(term) || summary.includes(term)) score += 4;
    else if (keywords.includes(term)) score += 3;
    else if (keywords.some(keyword => keyword.includes(term))) score += 2;
    else if (context.includes(term)) score += 1;
    else return -1;
  }
  return score;
}
