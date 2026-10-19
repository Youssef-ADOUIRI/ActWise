// Build the ActWise end-to-end pipeline deck: every stage, with a diagram and an explanation.
//
//   node docs/deck/build_pipeline.js    # write docs/deck/ActWise_Pipeline.pptx
//
// Stage statuses (built / in_progress / planned) come from content.json -> pipeline.stages,
// live numbers from facts.json. Style and helpers are shared with build_deck.js (common.js).
"use strict";

const path = require("path");
const { PALETTE, FONTS, W, MX, CW, TOP, CHIP, status, isBuilt, readJson, createDeck, helpers, writeTheme, HERE } = require("./common");

const OUT = path.join(HERE, "ActWise_Pipeline.pptx");
const content = readJson("content.json");
const facts = readJson("facts.json");
const meta = content.meta;
const ST = (content.pipeline || {}).stages || {};
const corpus = facts.corpus || {};
const fmt = (n) => Number(n || 0).toLocaleString("en-US");
const per = corpus.per_lang || {};
const TOK = {
  chunks: fmt(corpus.total_chunks),
  en_chunks: fmt((per.en || {}).chunks),
  fr_chunks: fmt((per.fr || {}).chunks),
  median: String((corpus.words || {}).median || "?"),
};
const fill = (s) =>
  String(s == null ? "" : s)
    .replace(/\{(\w+)\}/g, (m, k) => (k in TOK ? TOK[k] : m))
    .replace(/[–—]/g, "-");

const pres = createDeck({
  title: "ActWise: the end-to-end pipeline",
  subject: "How ActWise turns EU AI Act and GDPR text into cited answers and risk tiers",
  author: meta.author,
  footer: `ActWise  ·  End-to-end pipeline  ·  ${meta.date}`,
});
const H = helpers(pres, fill);
const { oid, text, box, chip, numberBadge, arrow, contentSlide, th, td, tdStatus, tableOpts, iconCircle } = H;

// ---------------------------------------------------------------- diagram primitives
const DASH = "8C98AA";
// A diagram node. status: built | in_progress | planned; kind: step | store | decision | io | neutral.
function node(s, label, x, y, w, h, o = {}) {
  const st = o.status || "planned";
  const kind = o.kind || "step";
  let fillC = PALETTE.white, lineO = { color: DASH, width: 1, dashType: "dash" }, color = PALETTE.ink2, bold = true;
  if (kind === "io") { fillC = PALETTE.ink; lineO = { type: "none" }; color = PALETTE.white; }
  else if (kind === "neutral") { fillC = PALETTE.mist; lineO = { type: "none" }; color = PALETTE.ink; }
  else if (kind === "decision") { fillC = PALETTE.goldSoft; lineO = { color: PALETTE.gold, width: 1.25 }; color = PALETTE.ink; }
  else if (isBuilt(st)) { fillC = PALETTE.teal; lineO = { type: "none" }; color = PALETTE.white; }
  else if (st === "in_progress") { fillC = PALETTE.goldSoft; lineO = { color: PALETTE.gold, width: 1.25 }; color = PALETTE.ink; }
  if (o.fill) fillC = o.fill;
  const shape = kind === "store" ? pres.shapes.CAN : kind === "decision" ? pres.shapes.DIAMOND : pres.shapes.ROUNDED_RECTANGLE;
  const fs = o.fontSize || 12.5;
  const runs = [{ text: fill(label), options: { bold, fontSize: fs, breakLine: !!o.sub, fontFace: o.mono ? FONTS.mono : undefined } }];
  if (o.sub) runs.push({ text: fill(o.sub), options: { bold: false, fontSize: o.subSize || fs - 1.5 } });
  s.addText(runs, {
    shape, x, y, w, h, rectRadius: kind === "step" || kind === "io" || kind === "neutral" ? 0.07 : undefined,
    fill: { color: fillC }, line: lineO, color, align: o.align || "center", valign: "middle",
    margin: o.margin || [0.03, 0.07, 0.03, 0.07], isTextBox: true, objectName: oid(`node-${kind}`),
  });
}
// Poly-line through points; arrowhead on the last segment only.
function path_(s, pts, o = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
    arrow(s, x1, y1, x2, y2, { ...o, head: i === pts.length - 2 && o.head !== false });
  }
}
function label(s, t, x, y, w, o = {}) {
  text(s, t, { x, y, w, h: o.h || 0.24, fontSize: o.fontSize || 10.5, italic: o.italic !== false, color: o.color || PALETTE.slate, align: o.align || "left", valign: "middle" });
}
function legend(s) {
  chip(s, "Built", 9.35, 0.42, 0.9, "teal", { h: 0.28 });
  s.addText("In progress", { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: 10.37, y: 0.42, w: 1.12, h: 0.28, fill: { color: PALETTE.goldSoft }, line: { color: PALETTE.gold, width: 1 }, color: PALETTE.ink, fontSize: 11, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("legend") });
  s.addText("Planned", { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: 11.61, y: 0.42, w: 1.12, h: 0.28, fill: { color: PALETTE.white }, line: { color: DASH, width: 1, dashType: "dash" }, color: PALETTE.ink2, fontSize: 11, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("legend") });
}
function mono(s, t, x, y, w, h, o = {}) {
  s.addText(fill(t), {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x, y, w, h, fill: { color: o.fill || PALETTE.graySoft },
    line: { color: PALETTE.line, width: 0.75 }, fontFace: FONTS.mono, fontSize: o.fontSize || 10.5, color: PALETTE.ink,
    align: "left", valign: o.valign || "top", margin: [0.1, 0.12, 0.1, 0.12], isTextBox: true, objectName: oid("code"),
  });
}
function bullets(s, items, x, y, w, h, o = {}) {
  text(s, items.map((t, i, a) => ({ text: fill(t), options: { bullet: true, breakLine: i < a.length - 1 } })),
    { x, y, w, h, fontSize: o.fontSize || 13, color: o.color || PALETTE.ink2, paraSpaceAfter: o.space || 5 });
}
function card(s, head, body, x, y, w, h, o = {}) {
  box(s, { x, y, w, h, fill: o.fill || PALETTE.mist });
  text(s, head, { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: 0.3, fontSize: o.headSize || 13, bold: true });
  text(s, body, { x: x + 0.15, y: y + 0.42, w: w - 0.27, h: h - 0.5, fontSize: o.fontSize || 12, color: PALETTE.ink2 });
}
const stageKicker = (n, name) => `Stage ${n} of 11  ·  ${name}`;

// ================================================================= 1. Title
pres.addSection({ title: "Overview" });
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Overview" });
  s.addText("ActWise, end to end", { placeholder: "title", fontSize: 50 });
  s.addText("How a legal question becomes a cited answer: every stage of the pipeline, with diagrams", { placeholder: "subtitle" });
  s.addText([
    { text: `${meta.author}  ·  ${meta.role}`, options: { breakLine: true } },
    { text: `${meta.date}  ·  companion to the project review deck` },
  ], { placeholder: "meta" });
  const chain = ["EUR-Lex HTML", "Parse + chunk", "Embed + index", "Hybrid retrieval", "LLM gateway", "Verify citations", "[AIA-Art6-2]"];
  chain.forEach((c, i) => {
    const last = i === chain.length - 1, y = 0.9 + i * 0.82;
    if (i > 0) s.addShape(pres.shapes.LINE, { x: 10.7, y: y - 0.36, w: 0, h: 0.36, line: { color: PALETTE.navyLine, width: 1.5 }, objectName: oid("chain") });
    s.addText(c, {
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.12, x: 9.2, y, w: 3.0, h: 0.46,
      fill: { color: last ? PALETTE.gold : PALETTE.navy2 }, line: { color: last ? PALETTE.gold : PALETTE.navyLine, width: 1 },
      fontFace: last ? FONTS.mono : undefined, fontSize: last ? 15 : 14, bold: true, color: last ? PALETTE.ink : PALETTE.onDark,
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("chain-chip"),
    });
  });
  s.addNotes("This deck walks through ActWise from raw legal text to a cited answer, one stage at a time. Each stage slide has a diagram, what it does, and why it is built that way. Green boxes are built today; dashed boxes are planned. It is the companion to the project review deck, which tracks progress and metrics.");
}

// ================================================================= 2. The pipeline on one page
{
  const s = contentSlide("Overview", "Overview", {
    title: "The pipeline on one page",
    takeaway: "Build the index once, answer every request from it, and measure and ship around both.",
    notes: "Three lanes. The top lane runs offline, once per version of the law: it turns EUR-Lex pages into searchable indexes. The middle lane runs for each request: a client calls the API, which retrieves passages and asks an LLM, then checks every citation. The bottom lane holds what keeps the system honest and alive: evaluation, the fine-tuned embedder, deployment and observability. Gold numbers point to the stage slides that follow.",
  });
  legend(s);
  const lanes = [
    ["Offline", "once per corpus version", 2.12],
    ["Per request", "every question", 3.65],
    ["Around it", "quality and operations", 5.18],
  ];
  const LH = 1.3, NX = 2.4, NW = 1.75, STEP = (W - MX - NX - NW) / 4, NH = 0.8;
  lanes.forEach(([a, b, y]) => {
    s.addShape(pres.shapes.RECTANGLE, { x: MX, y, w: CW, h: LH, fill: { color: "F6F8FB" }, line: { type: "none" }, objectName: oid("lane") });
    text(s, a, { x: MX + 0.15, y: y + 0.38, w: 1.6, h: 0.3, fontSize: 15, bold: true });
    text(s, b, { x: MX + 0.15, y: y + 0.68, w: 1.6, h: 0.3, fontSize: 11, color: PALETTE.slate });
  });
  const nx = (i) => NX + i * STEP;
  const ny = (lane) => lanes[lane][2] + (LH - NH) / 2;
  const badge = (n, x, y) => numberBadge(s, n, x - 0.12, y - 0.13, 0.32, { fontSize: 11 });
  const A = [
    ["EUR-Lex HTML", "AI Act + GDPR, EN/FR", ST.ingest, "step", 1],
    ["Parse + chunk", "articles → paragraphs", ST.ingest, "step", 1],
    ["chunks.jsonl", "{chunks} chunks", ST.ingest, "store", 1],
    ["Embed", "BGE-M3 / MiniLM int8", ST.index, "step", 2],
    ["Indexes", "Qdrant · NumPy · BM25", ST.index, "store", 2],
  ];
  const B = [
    ["Clients", "UI · Slack · MCP · HTTP", ST.integrations, "io", 7],
    ["FastAPI + guards", "API key · daily cap", ST.api, "step", 7],
    ["Hybrid retrieval", "dense + BM25 + RRF", ST.retrieval, "step", 3],
    ["LLM gateway", "cache · retry · fallback", ST.gateway, "step", 4],
    ["Answer or verdict", "citations verified", ST.answer, "step", 5],
  ];
  [A, B].forEach((row, lane) => row.forEach(([l, sub, st, kind, n], i) => {
    node(s, l, nx(i), ny(lane), NW, NH, { status: st, kind, sub, fontSize: 13, subSize: 11 });
    badge(n, nx(i), ny(lane));
    if (i < row.length - 1) arrow(s, nx(i) + NW, ny(lane) + NH / 2, nx(i + 1), ny(lane) + NH / 2);
  }));
  // Indexes feed retrieval
  const midY = (lanes[0][2] + LH + lanes[1][2]) / 2;
  path_(s, [[nx(4) + NW / 2, ny(0) + NH], [nx(4) + NW / 2, midY], [nx(2) + NW / 2, midY], [nx(2) + NW / 2, ny(1)]], { color: PALETTE.gold, width: 1.75 });
  label(s, "the same indexes serve every request", nx(2) + NW / 2 + 0.1, midY - 0.25, 3.2);
  const C = [
    ["Evaluation harness", "scores retrieval and answers", ST.eval, 8],
    ["Fine-tuned embedder", "feeds the Embed step", ST.finetune, 9],
    ["CI/CD + Cloud Run", "ships the API at EUR 0", ST.deploy, 10],
    ["Observability", "traces, logs, cost", ST.observe, 11],
  ];
  const CW4 = 2.35, CSTEP = (W - MX - NX - CW4) / 3;
  C.forEach(([l, sub, st, n], i) => {
    node(s, l, NX + i * CSTEP, ny(2), CW4, NH, { status: st, sub, fontSize: 13, subSize: 11 });
    badge(n, NX + i * CSTEP, ny(2));
  });
}

// ================================================================= 3. Two request paths
{
  const s = contentSlide("Overview", "Overview", {
    title: "Two request paths, one shared core",
    takeaway: "Q&A is a fixed pipeline. Classification is an agent loop. Both use the same retriever and LLM gateway.",
    notes: "There are two ways to use ActWise. Asking a question runs a fixed pipeline: one retrieval, one LLM call, one citation check, so cost and latency are predictable. Classifying a system runs an agent: the model decides what to search for, possibly several times, then submits a structured verdict that is validated before anyone sees it. Both paths reuse the same retriever, gateway and ID scheme, so improvements to one lift the other.",
  });
  legend(s);
  node(s, "Client", MX, 3.45, 1.45, 0.9, { kind: "io", sub: "question or system", fontSize: 13 });
  node(s, "FastAPI", 2.4, 3.45, 1.55, 0.9, { status: ST.api, sub: "guards", fontSize: 13 });
  arrow(s, MX + 1.45, 3.9, 2.4, 3.9);
  const X0 = 4.55, NW = 1.85, G = 0.22, r1 = 2.5, r2 = 4.4, NH = 0.8;
  const xs = [0, 1, 2, 3].map((i) => X0 + i * (NW + G));
  text(s, "/ask: one retrieval, one LLM call", { x: X0, y: r1 - 0.36, w: 6, h: 0.3, fontSize: 13, bold: true, color: PALETTE.ink });
  text(s, "/classify and /upload: an agent loop, several calls", { x: X0, y: r2 - 0.36, w: 6, h: 0.3, fontSize: 13, bold: true, color: PALETTE.ink });
  const row1 = [["Retrieve top 5", "hybrid, once", ST.retrieval], ["Generate", "1 call, temperature 0", ST.answer], ["Verify citations", "strip invented IDs", ST.answer], ["Cited answer", "or refusal, EN/FR", null]];
  const row2 = [["Agent loop", "LLM ⇄ search_corpus", ST.classifier], ["Submit", "submit_classification", ST.classifier], ["Validate", "schema + cited IDs", ST.classifier], ["Risk tier JSON", "+ Sheets register row", null]];
  [[row1, r1], [row2, r2]].forEach(([row, y]) => row.forEach(([l, sub, st], i) => {
    node(s, l, xs[i], y, NW, NH, { status: st || "planned", kind: st ? "step" : "io", sub, fontSize: 13, subSize: 11 });
    if (i < row.length - 1) arrow(s, xs[i] + NW, y + NH / 2, xs[i + 1], y + NH / 2);
  }));
  path_(s, [[3.95, 3.75], [4.25, 3.75], [4.25, r1 + NH / 2], [X0, r1 + NH / 2]]);
  path_(s, [[3.95, 4.05], [4.25, 4.05], [4.25, r2 + NH / 2], [X0, r2 + NH / 2]]);
  // Shared core
  const cx = X0, cw = W - MX - X0;
  box(s, { x: cx, y: 5.62, w: cw, h: 1.12, fill: PALETTE.mist });
  text(s, "Shared core used by both paths", { x: cx + 0.2, y: 5.7, w: cw - 0.4, h: 0.3, fontSize: 13, bold: true });
  ["HybridRetriever", "LLM gateway", "Chunk IDs + labels", "Guards + logging"].forEach((c, i) => {
    const w = (cw - 0.4 - 3 * 0.15) / 4;
    node(s, c, cx + 0.2 + i * (w + 0.15), 6.08, w, 0.5, { kind: "neutral", fontSize: 12, fill: PALETTE.white });
  });
  card(s, "Why two paths", "Q&A needs predictable cost and latency, so it is a fixed chain. Classification needs the model to choose what to read, so it is an agent with strict guards on its output.", MX, 4.75, 3.4, 1.99, { fontSize: 12.5 });
}

// ================================================================= 4. Stage 1: ingestion
pres.addSection({ title: "Data" });
{
  const s = contentSlide("Data", stageKicker(1, "Ingestion"), {
    title: "From EUR-Lex pages to chunks",
    takeaway: "A line-based parser turns four official pages into one record per paragraph, recital or annex point.",
    notes: "Ingestion is built and tested. Four pages are saved from EUR-Lex and committed, so the pipeline is reproducible offline. html_to_text strips markup. normalise_lines repairs the places where EUR-Lex splits a marker from its text. parse_regulation reads lines, not CSS classes, so it survives markup changes. chunk_units makes one chunk per paragraph and cuts paragraphs longer than 150 words into overlapping windows. The corpus test checks every official count in both languages on each run.",
  });
  legend(s);
  const steps = [
    ["4 EUR-Lex pages", "AI Act + GDPR, EN + FR, saved as HTML and committed", "store"],
    ["html_to_text", "BeautifulSoup + lxml. Drops scripts, styles, menus; turns non-breaking spaces into spaces", "step"],
    ["normalise_lines", "Collapses spaces, glues a lone \"(a)\" or \"1.\" to its text, removes footnote marks", "step"],
    ["parse_regulation", "Recitals, articles, annexes. Skips CHAPTER and SECTION headings; stops at \"Done at\"", "step"],
    ["chunk_units", "One chunk per paragraph. Over 150 words: windows with 25 words of overlap", "step"],
    ["chunks.jsonl", "{chunks} records with stable, language-free IDs", "store"],
  ];
  const n = steps.length, g = 0.22, w = (CW - g * (n - 1)) / n;
  steps.forEach(([l, d, kind], i) => {
    const x = MX + i * (w + g);
    node(s, l, x, TOP + 0.15, w, 0.85, { status: ST.ingest, kind, fontSize: 13, mono: kind === "step" });
    if (i < n - 1) arrow(s, x + w, TOP + 0.575, x + w + g, TOP + 0.575);
    text(s, d, { x: x + 0.05, y: TOP + 1.2, w: w - 0.1, h: 1.6, fontSize: 12.5, color: PALETTE.ink2 });
  });
  const facts4 = [
    ["{chunks}", "chunks in total"],
    ["{en_chunks} / {fr_chunks}", "English / French chunks"],
    ["{median}", "median words per chunk"],
    ["6 vs 7", "windows for Article 5(1), EN vs FR"],
  ];
  const fw = (CW - 3 * 0.22) / 4;
  facts4.forEach(([v, l], i) => {
    const x = MX + i * (fw + 0.22);
    box(s, { x, y: 5.05, w: fw, h: 1.0 });
    text(s, v, { x: x + 0.2, y: 5.12, w: fw - 0.4, h: 0.5, fontFace: FONTS.head, fontSize: 22, bold: true });
    text(s, l, { x: x + 0.2, y: 5.6, w: fw - 0.4, h: 0.35, fontSize: 12, color: PALETTE.slate });
  });
  text(s, "Safety net: tests/test_corpus.py asserts 180 recitals, 113 articles, 13 annexes (AI Act) and 173 recitals, 99 articles (GDPR) in both languages on every run.", { x: MX, y: 6.25, w: CW, h: 0.45, fontSize: 12.5, italic: true, color: PALETTE.slate });
}

// ================================================================= 5. Worked example: Article 6
{
  const s = contentSlide("Data", stageKicker(1, "Ingestion"), {
    title: "One paragraph through the parser",
    takeaway: "Article 6(2) of the AI Act, from raw text lines to the record that every later stage uses.",
    notes: "This is real output from the repo. On the left, the lines html_to_text produces for Article 6: note that point markers like (a) sit on their own line. The parser groups lines into a unit with numbered paragraphs; points stay inside their paragraph. Paragraph 2 becomes one chunk with the ID AIA-Art6-2. The French page produces a chunk with the same ID, stored under the key AIA-Art6-2@fr.",
  });
  const cols = [[MX, 3.95, "1. Raw text lines"], [4.95, 3.45, "2. Parsed unit"], [8.8, W - MX - 8.8, "3. Chunk record (one JSON line)"]];
  cols.forEach(([x, w, h]) => text(s, h, { x, y: TOP, w, h: 0.3, fontSize: 14, bold: true }));
  const y0 = TOP + 0.38, hh = 2.95;
  mono(s, [
    "Article 6",
    "Classification rules for high-risk AI systems",
    "1.   Irrespective of whether an AI system is placed on the market ...",
    "(a)",
    "the AI system is intended to be used as a safety component ...",
    "2.   In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.",
    "3.   By derogation from paragraph 2, ...",
  ].join("\n"), MX, y0, 3.95, hh, { fontSize: 10 });
  mono(s, [
    "kind:    article",
    "number:  6",
    "title:   Classification rules",
    "         for high-risk AI systems",
    "paragraphs:",
    "  1  Irrespective of ...",
    "     (a) ... (b) ...",
    "  2  In addition to ...",
    "  3  By derogation ...",
    "  4 to 8 ...",
  ].join("\n"), 4.95, y0, 3.45, hh, { fontSize: 10.5 });
  mono(s, [
    "{\"id\": \"AIA-Art6-2\",",
    " \"law\": \"ai_act\", \"lang\": \"en\",",
    " \"kind\": \"article\", \"number\": \"6\",",
    " \"paragraph\": \"2\", \"part\": 1,",
    " \"title\": \"Classification rules for",
    "   high-risk AI systems\",",
    " \"text\": \"In addition to the high-risk",
    "   AI systems referred to in paragraph 1,",
    "   AI systems referred to in Annex III",
    "   shall be considered to be high-risk.\"}",
  ].join("\n"), 8.8, y0, W - MX - 8.8, hh, { fontSize: 10.5, fill: PALETTE.tealSoft });
  arrow(s, MX + 3.95 + 0.05, y0 + hh / 2, 4.9, y0 + hh / 2, { color: PALETTE.gold, width: 2 });
  arrow(s, 4.95 + 3.45 + 0.05, y0 + hh / 2, 8.75, y0 + hh / 2, { color: PALETTE.gold, width: 2 });
  const by = 5.65;
  text(s, "embed_text: what the embedder and BM25 read", { x: MX, y: by - 0.05, w: 6.2, h: 0.28, fontSize: 12.5, bold: true });
  mono(s, "AI Act Article 6(2): Classification rules for high-risk AI systems\nIn addition to the high-risk AI systems referred to in paragraph 1, ...", MX, by + 0.27, 6.2, 0.82, { fontSize: 10 });
  text(s, "French twin: same ID, storage key AIA-Art6-2@fr", { x: 7.05, y: by - 0.05, w: W - MX - 7.05, h: 0.28, fontSize: 12.5, bold: true });
  mono(s, "Règlement IA Article 6(2): Règles relatives à la classification de systèmes d'IA comme systèmes à haut risque\nOutre les systèmes d'IA à haut risque visés au paragraphe 1, ...", 7.05, by + 0.27, W - MX - 7.05, 0.82, { fontSize: 10 });
}

// ================================================================= 6. Stable IDs
{
  const s = contentSlide("Data", stageKicker(1, "Ingestion"), {
    title: "Stable IDs: one key for every module",
    takeaway: "The ID never contains the language. Ingestion, search, evaluation and citations all speak it.",
    notes: "The ID is the contract between modules. It encodes the law, the unit, the number, the paragraph and the window part, and nothing else. Because it has no language, a French question is scored against the same gold article as an English one. Each module derives what it needs from it: the article level for metrics, a storage key with the language for databases, a human label for the UI, and the bracketed form the model must cite.",
  });
  legend(s);
  // Anatomy
  const segs = [["AIA", "law", 1.15], ["-", null, 0.3], ["Art", "unit type", 1.0], ["5", "number", 0.85], ["-", null, 0.3], ["1", "paragraph", 0.95], ["#3", "window part", 1.05]];
  let x = MX + 0.1;
  const ay = TOP + 0.15;
  segs.forEach(([t, l, w]) => {
    if (l) {
      s.addText(t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x, y: ay, w, h: 0.8, fill: { color: PALETTE.ink }, color: PALETTE.white, fontFace: FONTS.mono, fontSize: 26, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("seg") });
      text(s, l, { x: x - 0.2, y: ay + 0.88, w: w + 0.4, h: 0.28, fontSize: 12, color: PALETTE.slate, align: "center" });
    } else {
      text(s, t, { x, y: ay, w, h: 0.8, fontFace: FONTS.mono, fontSize: 26, bold: true, align: "center", valign: "middle", color: PALETTE.ink });
    }
    x += w + 0.1;
  });
  // Derived forms
  const uses = [
    ["article_id()", "AIA-Art5", "Gold-label level: metrics count an article once"],
    [".key", "AIA-Art5-1#3@fr", "Storage key in Qdrant, NumPy and BM25, so French never overwrites English"],
    ["human_label()", "AI Act, Art. 5(1)", "What users see. Never sent to the model"],
    ["citation", "[AIA-Art5-1#3]", "How the model cites; checked against what was retrieved"],
  ];
  const cw = 3.15, ch = 1.22;
  uses.forEach(([fn, v, d], i) => {
    const cx = MX + (i % 2) * (cw + 0.2), cy = 3.75 + Math.floor(i / 2) * (ch + 0.2);
    box(s, { x: cx, y: cy, w: cw, h: ch });
    text(s, fn, { x: cx + 0.15, y: cy + 0.1, w: cw - 0.3, h: 0.26, fontSize: 11.5, color: PALETTE.slate, fontFace: FONTS.mono });
    text(s, v, { x: cx + 0.15, y: cy + 0.36, w: cw - 0.3, h: 0.3, fontSize: 13.5, bold: true, fontFace: FONTS.mono, color: PALETTE.tealDark });
    text(s, d, { x: cx + 0.15, y: cy + 0.68, w: cw - 0.3, h: 0.5, fontSize: 12, color: PALETTE.ink2 });
  });
  // Examples table
  const tx = 7.4, tw = W - MX - tx;
  text(s, "Examples from the corpus", { x: tx, y: TOP, w: tw, h: 0.3, fontSize: 14, bold: true });
  const rows = [[th("ID"), th("English label"), th("French label")]];
  [
    ["AIA-Art6-2", "AI Act, Art. 6(2)", "Règlement IA, Art. 6(2)"],
    ["AIA-AnnexIII-4", "AI Act, Annex III, point 4", "Règlement IA, Annexe III, point 4"],
    ["AIA-AnnexVIII-b.1", "AI Act, Annex VIII, Section B, point 1", "Règlement IA, Annexe VIII, Section B, point 1"],
    ["AIA-Rec63", "AI Act, Recital 63", "Règlement IA, considérant 63"],
    ["GDPR-Art17-1", "GDPR, Art. 17(1)", "RGPD, Art. 17(1)"],
  ].forEach(([a, b, c]) => rows.push([td(a, { fontFace: FONTS.mono, fontSize: 10.5, bold: true }), td(b, { fontSize: 12 }), td(c, { fontSize: 12 })]));
  s.addTable(rows, tableOpts(tx, TOP + 0.38, [1.95, 1.65, tw - 3.6], [0.38, 0.5, 0.5, 0.62, 0.5, 0.5]));
  box(s, { x: tx, y: 5.6, w: tw, h: 1.05, fill: PALETTE.goldSoft });
  text(s, "Rule: an ID never contains the language. EN and FR chunks of a paragraph share one ID, so one gold label scores both.", { x: tx + 0.2, y: 5.6, w: tw - 0.4, h: 1.05, fontSize: 13, valign: "middle" });
}

// ================================================================= 7. Stage 2: indexing
{
  const s = contentSlide("Data", stageKicker(2, "Indexing"), {
    title: "Indexing: three ways to find a chunk",
    takeaway: "Vectors go to Qdrant and a NumPy copy; words go to BM25. One embedder serves passages and queries.",
    notes: "Each chunk's embed_text, the header plus the text, is embedded. Locally that is BGE-M3, a strong multilingual model. In the cloud it is our fine-tuned MiniLM exported to int8 ONNX, so the container needs no PyTorch. Vectors go to a Qdrant collection, and a NumPy copy ships inside the image so search keeps working if the free Qdrant cluster is suspended. BM25 is built in memory from the same text, with no extra service. Point IDs are a UUID of the storage key, so re-indexing overwrites rather than duplicates.",
  });
  legend(s);
  const st = ST.index;
  node(s, "chunks.jsonl", MX, 3.3, 1.55, 1.15, { status: ST.ingest, kind: "store", sub: "{chunks}", fontSize: 13 });
  node(s, "embed_text", 2.55, 3.43, 1.85, 0.9, { status: ST.ingest, sub: "header + text", fontSize: 13, mono: true });
  arrow(s, MX + 1.55, 3.875, 2.55, 3.875);
  // Embedder group
  const gx = 4.85, gw = 3.2;
  box(s, { x: gx, y: TOP + 0.05, w: gw, h: 3.4, fill: PALETTE.mist });
  text(s, "Embedder (same for passages and queries)", { x: gx + 0.15, y: TOP + 0.13, w: gw - 0.3, h: 0.5, fontSize: 12.5, bold: true });
  node(s, "Local: BGE-M3", gx + 0.2, TOP + 0.7, gw - 0.4, 1.15, { status: st, sub: "1024 dimensions · sentence-transformers · PyTorch", fontSize: 13 });
  node(s, "Cloud: MiniLM, fine-tuned", gx + 0.2, TOP + 2.05, gw - 0.4, 1.2, { status: ST.finetune, sub: "384 dimensions · ONNX int8 · no PyTorch", fontSize: 13 });
  arrow(s, 4.4, 3.875, gx, 3.875);
  // Stores
  const sx = 9.25, sw = W - MX - sx;
  const stores = [
    ["Qdrant collection", "point id = uuid5(id@lang); payload: id, law, lang", 2.2],
    ["NumPy index.npz", "inside the Docker image; automatic fallback", 3.38],
    ["BM25 index", "built in memory from embed_text; no service", 4.56],
  ];
  stores.forEach(([l, sub, y]) => node(s, l, sx, y, sw, 0.98, { status: st, kind: "store", sub, fontSize: 13, subSize: 11 }));
  const fx = 8.65;
  arrow(s, gx + gw, 3.875, fx, 3.875, { head: false });
  arrow(s, fx, 2.69, fx, 3.875, { head: false });
  arrow(s, fx, 2.69, sx, 2.69);
  arrow(s, fx, 3.87, sx, 3.87);
  label(s, "vectors", gx + gw + 0.05, 3.9, 0.6);
  path_(s, [[3.475, 4.33], [3.475, 5.85], [sx + sw / 2, 5.85], [sx + sw / 2, 5.54]], { color: PALETTE.gold, width: 1.5 });
  label(s, "words, not vectors", 5.0, 5.6, 2.5);
  const notes = [
    "Same embedder for queries and passages, or the scores mean nothing.",
    "uuid5 of the storage key makes re-indexing idempotent.",
    "Starts in Steps 3-4: the chunks it needs are ready.",
  ];
  notes.forEach((t, i) => {
    const w = (CW - 0.4) / 3, x = MX + i * (w + 0.2);
    iconCircle(s, "check", x, 6.17, 0.36, PALETTE.ink);
    text(s, t, { x: x + 0.48, y: 6.1, w: w - 0.5, h: 0.6, fontSize: 12.5, color: PALETTE.ink2, valign: "middle" });
  });
}

// ================================================================= 8. Stage 3: hybrid retrieval
pres.addSection({ title: "Retrieval and generation" });
{
  const s = contentSlide("Retrieval and generation", stageKicker(3, "Retrieval"), {
    title: "Hybrid retrieval: meaning plus exact words",
    takeaway: "Dense and BM25 each return 30 candidates; rank fusion merges them; an optional reranker picks the final 5.",
    notes: "A query goes two ways at once. The dense side embeds it and finds passages with similar meaning, which handles paraphrases and French wording. The sparse side, BM25, rewards exact words, which matters for references like Annex III or Article 50. Reciprocal rank fusion merges the two ranked lists using only ranks, so there are no weights to tune. A cross-encoder reranker can reorder the top 20; it is measured as an ablation first because it costs latency.",
  });
  legend(s);
  const st = ST.retrieval;
  node(s, "Query", MX, 3.55, 1.0, 0.8, { kind: "io", sub: "EN or FR", fontSize: 13 });
  node(s, "Embed query", 1.95, 2.55, 1.4, 0.75, { status: st, fontSize: 12.5 });
  node(s, "Dense top 30", 3.6, 2.55, 1.45, 0.75, { status: st, sub: "cosine · Qdrant / NumPy", fontSize: 12.5, subSize: 10 });
  node(s, "Tokenize", 1.95, 4.6, 1.4, 0.75, { status: st, fontSize: 12.5 });
  node(s, "BM25 top 30", 3.6, 4.6, 1.45, 0.75, { status: st, sub: "own code", fontSize: 12.5, subSize: 10 });
  node(s, "RRF fuse", 5.35, 3.55, 1.0, 0.8, { status: st, fontSize: 12.5 });
  node(s, "Rerank top 20", 6.6, 3.55, 1.4, 0.8, { status: st, sub: "cross-encoder, optional", fontSize: 12.5, subSize: 10 });
  node(s, "Top 5", 8.25, 3.55, 0.85, 0.8, { kind: "io", sub: "hits", fontSize: 13 });
  path_(s, [[1.6, 3.8], [1.78, 3.8], [1.78, 2.925], [1.95, 2.925]]);
  path_(s, [[1.6, 4.1], [1.78, 4.1], [1.78, 4.975], [1.95, 4.975]]);
  arrow(s, 3.35, 2.925, 3.6, 2.925);
  arrow(s, 3.35, 4.975, 3.6, 4.975);
  path_(s, [[5.05, 2.925], [5.2, 2.925], [5.2, 3.85], [5.35, 3.85]]);
  path_(s, [[5.05, 4.975], [5.2, 4.975], [5.2, 4.05], [5.35, 4.05]]);
  arrow(s, 6.35, 3.95, 6.6, 3.95);
  arrow(s, 8.0, 3.95, 8.25, 3.95);
  label(s, "dense: meaning", 1.95, TOP + 0.1, 2.5, { fontSize: 11.5, color: PALETTE.ink2 });
  label(s, "sparse: exact words", 1.95, 5.4, 2.5, { fontSize: 11.5, color: PALETTE.ink2 });
  card(s, "BM25 catches exact references", "\"Annex III\", \"Article 50\", \"erasure\": words a vector can blur.", MX, 5.85, 4.1, 0.92, { fontSize: 12 });
  card(s, "Dense catches meaning", "Paraphrases and French wording that share no word with the text.", MX + 4.3, 5.85, 4.2, 0.92, { fontSize: 12 });
  // RRF worked example
  const px = 9.4, pw = W - MX - px;
  box(s, { x: px, y: TOP + 0.05, w: pw, h: 4.67, fill: PALETTE.mist });
  text(s, "RRF, worked example", { x: px + 0.18, y: TOP + 0.15, w: pw - 0.36, h: 0.3, fontSize: 14, bold: true });
  mono(s, "score = Σ 1/(60 + rank)", px + 0.18, TOP + 0.55, pw - 0.36, 0.42, { fontSize: 11, fill: PALETTE.white, valign: "middle" });
  const rows = [[th("Chunk", { fontSize: 11 }), th("Dense", { fontSize: 11, align: "center" }), th("BM25", { fontSize: 11, align: "center" }), th("Score", { fontSize: 11, align: "center" })]];
  [["A", "1", "3", "0.0323"], ["B", "2", "none", "0.0161"], ["C", "none", "1", "0.0164"]].forEach(([a, b, c, d]) => rows.push([td(a, { bold: true, fontSize: 12 }), td(b, { align: "center", fontSize: 12 }), td(c, { align: "center", fontSize: 12 }), td(d, { align: "center", fontSize: 12, bold: true })]));
  s.addTable(rows, { ...tableOpts(px + 0.18, TOP + 1.12, [0.7, 0.68, 0.68, pw - 0.36 - 2.06], 0.36), fill: { color: PALETTE.white } });
  text(s, [
    { text: "Result: A, then C, then B.", options: { bold: true, breakLine: true } },
    { text: "A chunk both retrievers rank well wins. Only ranks are used, so there are no weights to tune and the two score scales never need to match." },
  ], { x: px + 0.18, y: TOP + 2.75, w: pw - 0.36, h: 1.85, fontSize: 12.5, color: PALETTE.ink2 });
}

// ================================================================= 9. Stage 4: LLM gateway
{
  const s = contentSlide("Retrieval and generation", stageKicker(4, "LLM gateway"), {
    title: "The LLM gateway: one chat() for every model",
    takeaway: "Free providers in a fallback chain, wrapped in retries and a disk cache. The pipeline never imports an SDK.",
    notes: "Everything that talks to a model goes through one chat function with a provider-neutral message format. The outer layer is a disk cache: re-running an evaluation costs zero API calls. Inside, a fallback chain tries Gemini first, then Groq, then a local Ollama model. Each remote provider is wrapped in a retry layer that waits and retries on rate limits. Gemini, Groq and Ollama all speak the OpenAI protocol, so one adapter serves three. The Anthropic adapter is written and tested with a fake client, and runs live only with credits.",
  });
  legend(s);
  const st = ST.gateway;
  const gw = 7.55;
  node(s, "Caller: RagPipeline.ask() or classify()", MX, TOP + 0.05, gw, 0.55, { kind: "io", sub: "llm.chat(messages, tools, temperature)", fontSize: 12.5, subSize: 11 });
  arrow(s, 2.6, TOP + 0.6, 2.6, 3.05);
  arrow(s, 5.6, 3.05, 5.6, TOP + 0.6);
  label(s, "request", 2.7, 2.75, 1.2);
  label(s, "LLMResponse: text, tool calls, tokens", 5.7, 2.75, 2.6);
  box(s, { x: MX, y: 3.05, w: gw, h: 3.7, fill: PALETTE.white, line: PALETTE.slate });
  text(s, [
    { text: "CachedLLM  ", options: { bold: true, fontFace: FONTS.mono } },
    { text: "disk cache in .cache/llm; key = hash of messages, tools, temperature, model names and max_tokens" },
  ], { x: MX + 0.2, y: 3.13, w: gw - 0.4, h: 0.5, fontSize: 12, color: PALETTE.ink2 });
  box(s, { x: MX + 0.2, y: 3.7, w: gw - 0.4, h: 2.88, fill: PALETTE.mist });
  text(s, [
    { text: "FallbackLLM  ", options: { bold: true, fontFace: FONTS.mono } },
    { text: "tries providers in LLM_PROVIDER_ORDER; the first answer wins" },
  ], { x: MX + 0.4, y: 3.78, w: gw - 0.8, h: 0.3, fontSize: 12, color: PALETTE.ink2 });
  const provs = [
    ["Gemini", "OpenAI SDK\nfree tier\nretry, 4 s spacing", "planned"],
    ["Groq", "OpenAI SDK\ngpt-oss-20b\nretry, 2 s spacing", "planned"],
    ["Ollama", "OpenAI SDK\nlocal qwen3:4b\nno retry", "planned"],
    ["Anthropic", "Anthropic SDK\nonly with credits\nretry", "optional"],
  ];
  const pw = (gw - 0.8 - 3 * 0.3) / 4;
  provs.forEach(([n, d, kind], i) => {
    const x = MX + 0.4 + i * (pw + 0.3);
    node(s, n, x, 4.3, pw, 2.05, { status: st, sub: d, fontSize: 14, subSize: 11.5 });
    if (i < 2) arrow(s, x + pw, 5.325, x + pw + 0.3, 5.325, { color: PALETTE.gold, width: 2 });
  });
  // Why panel
  const px = 8.45, pw2 = W - MX - px;
  box(s, { x: px, y: TOP + 0.05, w: pw2, h: 4.65, fill: PALETTE.mist });
  text(s, "Why this layer exists", { x: px + 0.2, y: TOP + 0.15, w: pw2 - 0.4, h: 0.3, fontSize: 14, bold: true });
  bullets(s, [
    "Free tiers have rate limits: retries ride out 429 and 5xx with backoff (2, 4, 8 s).",
    "One OpenAI-protocol adapter covers Gemini, Groq and Ollama via base_url.",
    "The Anthropic adapter moves the system prompt out and merges tool results into one user message.",
    "Serving fails over fast (2 tries) so a request fits Cloud Run's 60 s.",
    "The cache makes evaluation reruns free and repeatable.",
  ], px + 0.2, TOP + 0.55, pw2 - 0.35, 4.1, { fontSize: 12.5 });
}

// ================================================================= 10. Stage 5: cited answers
{
  const s = contentSlide("Retrieval and generation", stageKicker(5, "Cited answers"), {
    title: "Cited answers: generate, then verify",
    takeaway: "The model may only cite what was retrieved. Anything else is removed before the user sees it.",
    notes: "A question first passes cheap guardrails: personal data is redacted before anything is logged, and obvious injections are flagged. Retrieval returns five passages, each tagged with its ID in the prompt. The model answers at temperature zero and must cite an ID after each rule, or reply NOT_COVERED. A NOT_COVERED reply becomes a polite refusal in the user's language. Otherwise every cited ID is checked against the retrieved set; invented ones are stripped as exact tokens and logged, and valid ones become human-readable labels.",
  });
  legend(s);
  const st = ST.answer;
  const xs = [MX, 3.1, 5.6, 8.1, 10.6], w = 2.1, y1 = TOP + 0.15, h1 = 0.78;
  const row = [["Question + lang", null, "io"], ["Guardrails", "redact PII · flag injection"], ["Retrieve top 5", "hybrid (stage 3)"], ["Build prompt", "sources tagged [ID]"], ["LLM", "temperature 0 (stage 4)"]];
  row.forEach(([l, sub, kind], i) => {
    node(s, l, xs[i], y1, w, h1, { status: st, kind: kind || "step", sub, fontSize: 13, subSize: 11 });
    if (i < row.length - 1) arrow(s, xs[i] + w, y1 + h1 / 2, xs[i + 1], y1 + h1 / 2);
  });
  const dx = 10.65, dy = 3.4, dw = 2.0, dh = 1.05;
  arrow(s, 11.65, y1 + h1, 11.65, dy);
  node(s, "Not covered?", dx, dy, dw, dh, { kind: "decision", fontSize: 12.5, margin: 0 });
  const r2y = 3.55, r2h = 0.75;
  node(s, "Verify citations", 7.85, r2y, 2.35, r2h, { status: st, sub: "invented = cited − retrieved", fontSize: 13, subSize: 11 });
  node(s, "Human labels", 5.3, r2y, 2.2, r2h, { status: st, sub: "AIA-Art6-2 → AI Act, Art. 6(2)", fontSize: 13, subSize: 10.5 });
  node(s, "AskResult", 2.85, r2y, 2.1, r2h, { kind: "io", sub: "answer · citations · sources", fontSize: 13, subSize: 10.5 });
  arrow(s, dx, dy + dh / 2, 10.2, r2y + r2h / 2);
  label(s, "no", 10.22, 3.62, 0.4);
  arrow(s, 7.85, r2y + r2h / 2, 7.5, r2y + r2h / 2);
  arrow(s, 5.3, r2y + r2h / 2, 4.95, r2y + r2h / 2);
  node(s, "Refusal", 10.6, 4.85, 2.1, 0.72, { status: st, sub: "in the user's language", fontSize: 13, subSize: 11 });
  arrow(s, 11.65, dy + dh, 11.65, 4.85);
  label(s, "yes", 11.72, 4.5, 0.5);
  path_(s, [[10.6, 5.21], [3.9, 5.21], [3.9, r2y + r2h]]);
  label(s, "refused = true, no citations", 6.0, 4.92, 2.6);
  card(s, "Invented ID", "Model cites [AIA-Art6] but only AIA-Art6-2 was retrieved: [AIA-Art6] is removed and logged; AIA-Art6-2 stays.", MX, 3.4, 2.05, 2.15, { fontSize: 11.5, fill: PALETTE.coralSoft });
  text(s, "Answer prompt rules (configs/prompts/answer.v1.md)", { x: MX, y: 5.82, w: 8, h: 0.3, fontSize: 13, bold: true });
  ["Use only the sources", "Cite [ID] after each rule", "Answer in the question's language", "Reply NOT_COVERED if missing", "Never judge a company's compliance"].forEach((t, i) => {
    const cw = (CW - 4 * 0.12) / 5;
    node(s, t, MX + i * (cw + 0.12), 6.17, cw, 0.55, { kind: "neutral", fontSize: 12 });
  });
}

// ================================================================= 11. Stage 6: classifier agent
{
  const s = contentSlide("Retrieval and generation", stageKicker(6, "Risk classifier"), {
    title: "The classifier agent loop",
    takeaway: "The model searches the Act as often as it needs, but it can only finish with a valid, grounded verdict.",
    notes: "The classifier is a tool-calling loop. The model gets the system description and an ordered list of checks. It can call search_corpus as often as it likes; every returned ID is added to a seen set. It finishes only by calling submit_classification. The arguments are validated against a Pydantic schema, and every cited ID must be one it actually retrieved. If not, the error goes back to the model as a tool result and it tries again. A plain-text reply gets one nudge, and a step budget of eight stops endless loops.",
  });
  legend(s);
  const st = ST.classifier;
  node(s, "AI system description", MX, TOP + 0.15, 2.7, 0.85, { kind: "io", sub: "+ ordered checks in the system prompt", fontSize: 13, subSize: 11 });
  node(s, "LLM with 2 tools", 4.0, TOP + 0.15, 2.3, 0.85, { status: st, sub: "temperature 0", fontSize: 13 });
  node(s, "search_corpus", 7.55, TOP + 0.15, 2.4, 0.85, { status: st, sub: "query, top_k ≤ 8 → retriever", fontSize: 13, mono: true, subSize: 10.5 });
  arrow(s, MX + 2.7, TOP + 0.575, 4.0, TOP + 0.575);
  arrow(s, 6.3, TOP + 0.38, 7.6, TOP + 0.38);
  arrow(s, 7.6, TOP + 0.8, 6.3, TOP + 0.8);
  label(s, "query", 6.65, TOP + 0.13, 0.8);
  label(s, "chunks + IDs", 6.4, TOP + 0.84, 1.2);
  node(s, "submit_classification", 4.0, 3.55, 2.3, 0.75, { status: st, sub: "tier, reasons, citations ...", fontSize: 11.5, mono: true, subSize: 10.5 });
  arrow(s, 5.15, TOP + 1.0, 5.15, 3.55);
  node(s, "Valid schema and only retrieved IDs?", 3.9, 4.65, 2.5, 1.15, { kind: "decision", fontSize: 11 });
  arrow(s, 5.15, 4.3, 5.15, 4.65);
  node(s, "ClassifyResult JSON", 7.3, 4.85, 2.6, 0.75, { kind: "io", sub: "validated, grounded", fontSize: 13, subSize: 11 });
  arrow(s, 6.4, 5.225, 7.3, 5.225);
  label(s, "yes", 6.55, 4.95, 0.5);
  node(s, "Sheets register row", 10.3, 4.85, W - MX - 10.3, 0.75, { status: ST.integrations, sub: "hash only, never raw text", fontSize: 12.5, subSize: 10.5 });
  arrow(s, 9.9, 5.225, 10.3, 5.225);
  node(s, "Error fed back", MX, 4.85, 2.7, 0.75, { status: st, sub: "as a tool result", fontSize: 13, subSize: 11 });
  arrow(s, 3.9, 5.225, MX + 2.7, 5.225);
  label(s, "no", 3.42, 4.95, 0.4);
  path_(s, [[1.95, 4.85], [1.95, 3.32], [4.55, 3.32], [4.55, TOP + 1.0]], { color: PALETTE.coral });
  label(s, "the model tries again", 2.05, 3.05, 2.0);
  // Guards panel
  const gx = 10.3, gw = W - MX - gx;
  box(s, { x: gx, y: TOP + 0.15, w: gw, h: 2.45, fill: PALETTE.mist });
  text(s, "Guards in the loop", { x: gx + 0.15, y: TOP + 0.23, w: gw - 0.3, h: 0.3, fontSize: 13, bold: true });
  bullets(s, ["Schema errors go back to the model", "Only IDs it retrieved can be cited", "A plain-text reply gets one nudge", "8 steps max, then ClassificationError"], gx + 0.15, TOP + 0.58, gw - 0.25, 1.95, { fontSize: 12 });
  box(s, { x: MX, y: 6.0, w: CW, h: 0.75, fill: PALETTE.goldSoft });
  text(s, "Order of checks: 1 Art. 5 prohibited  →  2 Art. 6(1) + Annex I  →  3 Art. 6(2) + Annex III  →  4 Art. 50 transparency  →  else minimal risk.  Missing facts: needs_more_info.", { x: MX + 0.2, y: 6.0, w: CW - 0.4, h: 0.75, fontSize: 13, valign: "middle" });
}

// ================================================================= 12. The AI Act ladder
{
  const s = contentSlide("Retrieval and generation", stageKicker(6, "Risk classifier"), {
    title: "How the agent decides: the AI Act ladder",
    takeaway: "Stop at the first rule that applies. The verdict cites the articles it read.",
    notes: "The system prompt encodes the legal order of analysis. First, is it a prohibited practice under Article 5, like social scoring or emotion recognition at work? If not, is it high risk, either as a safety component of a regulated product under Annex I, or as a listed use case in Annex III, like ranking job applicants? If not, does Article 50 impose transparency duties, as for chatbots or generated images? Otherwise it is minimal risk. If the description lacks the facts a rule needs, the answer is needs_more_info with follow-up questions. The JSON on the right is illustrative.",
  });
  const steps = [
    ["Prohibited", PALETTE.coral, PALETTE.white, "Art. 5", "Social scoring for public housing; emotion recognition at work"],
    ["High risk", PALETTE.gold, PALETTE.ink, "Art. 6 + Annex I or III", "Ranks job applicants (III.4); grades entrance essays (III.3); credit scoring (III.5)"],
    ["Transparency", PALETTE.blue, PALETTE.white, "Art. 50", "Customer-support chatbot; generated marketing images"],
    ["Minimal risk", PALETTE.teal, PALETTE.white, "none of the above", "Spam filter in a mailbox"],
  ];
  steps.forEach(([tier, c, tc, basis, ex], i) => {
    const x = MX + i * 0.75, y = TOP + 0.05 + i * 1.08, w = 4.95, h = 0.93;
    box(s, { x, y, w, h, fill: PALETTE.mist });
    numberBadge(s, i + 1, x + 0.15, y + 0.25, 0.42);
    s.addText(tier, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: x + 0.72, y: y + 0.12, w: 1.45, h: 0.3, fill: { color: c }, color: tc, fontSize: 12, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("tier") });
    text(s, basis, { x: x + 2.3, y: y + 0.1, w: w - 2.4, h: 0.36, fontSize: 12, bold: true, valign: "middle" });
    text(s, ex, { x: x + 0.72, y: y + 0.47, w: w - 0.85, h: 0.42, fontSize: 12, color: PALETTE.ink2 });
    if (i < steps.length - 1) {
      arrow(s, x + 0.36, y + h, x + 0.36, y + 1.08, { color: PALETTE.slate });
      label(s, "no", x + 0.42, y + h - 0.02, 0.4, { h: 0.18, fontSize: 10 });
    }
  });
  box(s, { x: MX, y: 5.55, w: 2.05, h: 1.2, fill: PALETTE.graySoft, line: PALETTE.line });
  text(s, "needs_more_info", { x: MX + 0.12, y: 5.62, w: 1.85, h: 0.3, fontSize: 12, bold: true, fontFace: FONTS.mono });
  text(s, "Facts missing for a rule: ask follow-up questions instead of guessing.", { x: MX + 0.12, y: 5.93, w: 1.85, h: 0.8, fontSize: 11.5, color: PALETTE.ink2 });
  const jx = 8.35, jw = W - MX - jx;
  text(s, "Output: validated JSON (illustrative)", { x: jx, y: TOP, w: jw, h: 0.3, fontSize: 14, bold: true });
  mono(s, [
    "{",
    "  \"tier\": \"high_risk\",",
    "  \"reasons\": [",
    "    \"Not a practice listed in Art. 5\",",
    "    \"Recruitment use case, Annex III point 4\"",
    "  ],",
    "  \"citations\": [\"AIA-AnnexIII-4\",",
    "                \"AIA-Art6-2\"],",
    "  \"confidence\": 0.9,",
    "  \"follow_up_questions\": [],",
    "  \"disclaimer\": \"Information only,",
    "                 not legal advice.\"",
    "}",
  ].join("\n"), jx, TOP + 0.38, jw, 3.25, { fontSize: 11 });
  box(s, { x: jx, y: 5.85, w: jw, h: 0.9, fill: PALETTE.goldSoft });
  text(s, "AI Omnibus (Reg. 2026/1744): Annex III obligations now apply from 2 Dec 2027. The classification rules did not change.", { x: jx + 0.15, y: 5.85, w: jw - 0.3, h: 0.9, fontSize: 12, valign: "middle" });
}

// ================================================================= 13. Stage 7: API and integrations
pres.addSection({ title: "Serving" });
{
  const s = contentSlide("Serving", stageKicker(7, "API and integrations"), {
    title: "One API, many front doors",
    takeaway: "Every client is a thin HTTP caller of the same FastAPI service, so guards, logs and tests live in one place.",
    notes: "The FastAPI service exposes five endpoints. Only ask, classify and upload call an LLM, and those sit behind a daily cap that returns 429 after 200 requests, which keeps a public demo inside free quotas. Search makes no LLM call, so load tests use it. The Streamlit UI, the Slack command and the MCP server are thin clients of this API. Each classification appends a row to a Google Sheets register with a hash of the description, never the text itself, and a Sheets outage never breaks the response.",
  });
  legend(s);
  const sti = ST.integrations;
  const clients = [["Streamlit UI", "ask and classify tabs"], ["Slack /actwise", "Socket Mode; ack within 3 s"], ["MCP server", "stdio; ask_ai_act, classify_ai_system"], ["Any HTTP client", "curl, scripts"]];
  const ax = 4.45, aw = 4.3, ay = TOP + 0.15, ah = 3.85;
  clients.forEach(([l, sub], i) => {
    const y = TOP + 0.15 + i * 0.98;
    node(s, l, MX, y, 3.05, 0.8, { status: i === 3 ? "planned" : sti, kind: i === 3 ? "io" : "step", sub, fontSize: 13, subSize: 11 });
    arrow(s, MX + 3.05, y + 0.4, ax, y + 0.4);
  });
  box(s, { x: ax, y: ay, w: aw, h: ah, fill: PALETTE.white, line: PALETTE.ink, lineWidth: 1.5 });
  text(s, "FastAPI on Cloud Run", { x: ax + 0.2, y: ay + 0.1, w: aw - 0.4, h: 0.32, fontSize: 15, bold: true });
  box(s, { x: ax + 0.2, y: ay + 0.5, w: aw - 0.4, h: 0.62, fill: PALETTE.goldSoft });
  text(s, "X-API-Key (optional) · daily cap of 200 on LLM endpoints, then 429", { x: ax + 0.3, y: ay + 0.5, w: aw - 0.6, h: 0.62, fontSize: 12, valign: "middle" });
  [["GET", "/health", "liveness, version"], ["GET", "/search", "top chunks, no LLM, no cap"], ["POST", "/ask", "cited answer"], ["POST", "/classify", "risk tier"], ["POST", "/upload", "file, then classify"]].forEach(([m, p, d], i) => {
    const y = ay + 1.28 + i * 0.49;
    chip(s, m, ax + 0.2, y + 0.06, 0.62, m === "GET" ? "gray" : "teal", { h: 0.28, fontSize: 10 });
    text(s, p, { x: ax + 0.92, y, w: 1.2, h: 0.4, fontSize: 12.5, bold: true, fontFace: FONTS.mono, valign: "middle" });
    text(s, d, { x: ax + 2.15, y, w: aw - 2.3, h: 0.4, fontSize: 12, color: PALETTE.ink2, valign: "middle" });
  });
  const rx = 9.2, rw = W - MX - rx;
  const outs = [["Google Sheets register", "time · hash · tier · confidence · IDs · model", 1.12], ["File upload", "PDF, DOCX or TXT up to 2 MB; text cut at 20,000 characters", 1.12], ["Langfuse + JSON logs", "traces, tokens, latency (stage 11)", 0.95]];
  let oy = TOP + 0.15;
  outs.forEach(([l, sub, h], i) => {
    node(s, l, rx, oy, rw, h, { status: i === 2 ? ST.observe : sti, sub, fontSize: 13, subSize: 11 });
    arrow(s, ax + aw, oy + h / 2, rx, oy + h / 2);
    oy += h + 0.25;
  });
  box(s, { x: MX, y: 6.2, w: CW, h: 0.58, fill: PALETTE.mist });
  text(s, "Privacy by design: the register stores a 12-character hash of the description, never the text. A Sheets outage is ignored, so /classify still answers.", { x: MX + 0.2, y: 6.2, w: CW - 0.4, h: 0.58, fontSize: 12.5, valign: "middle", color: PALETTE.ink2 });
}

// ================================================================= 14. Stage 8: evaluation
pres.addSection({ title: "Quality" });
{
  const s = contentSlide("Quality", stageKicker(8, "Evaluation"), {
    title: "The evaluation harness",
    takeaway: "Split by article first, then build questions, then score. Retrieval runs on every PR; LLM scoring runs weekly from a cache.",
    notes: "Evaluation starts by splitting articles, not chunks, into train, dev and test, so neighbouring text cannot leak from training into the reported numbers. The golden set mixes hand-written and reviewed synthetic questions, a third in French. One runner scores retrieval with no LLM call, cheap enough for every pull request, and generation with an LLM judge, run weekly in slices from the cache. The judge is trusted only after it agrees with my own labels: Cohen's kappa of 0.6 or more, otherwise the judge prompt is rewritten.",
  });
  legend(s);
  const st = ST.eval;
  const y1 = TOP + 0.12, h1 = 0.8, w = 1.65, g = 0.28;
  const xs = [0, 1, 2, 3].map((i) => MX + i * (w + g));
  [["chunks.jsonl", ST.ingest, "store"], ["splits.json", st, "step"], ["golden_qa.jsonl", st, "store"], ["run_eval.py", st, "step"]].forEach(([l, sst, kind], i) => {
    node(s, l, xs[i], y1, w, h1, { status: sst, kind, fontSize: 12.5, mono: true });
    if (i < 3) arrow(s, xs[i] + w, y1 + h1 / 2, xs[i + 1], y1 + h1 / 2);
  });
  const ds = ["{chunks} chunks; unit of the split is the article", "70 / 15 / 15 by article, seed 42; no leakage", "50 hand-written + 100 synthetic, all reviewed; 30% French; 5 types", "--split dev|test  --llm on|off  --slice 0/3"];
  ds.forEach((d, i) => text(s, d, { x: xs[i] + 0.03, y: y1 + 0.9, w: w - 0.06, h: 0.95, fontSize: 11.5, color: PALETTE.ink2 }));
  const bx = xs[3] + w + 0.45, bw = 2.25;
  node(s, "Retrieval metrics", bx, TOP - 0.02, bw, 0.62, { status: st, sub: "no LLM · every PR · gate -2 pts", fontSize: 12.5, subSize: 10.5 });
  node(s, "Generation metrics", bx, TOP + 0.85, bw, 0.62, { status: st, sub: "LLM judge · weekly · cached", fontSize: 12.5, subSize: 10.5 });
  path_(s, [[xs[3] + w, y1 + 0.25], [bx - 0.25, y1 + 0.25], [bx - 0.25, TOP + 0.29], [bx, TOP + 0.29]]);
  path_(s, [[xs[3] + w, y1 + 0.55], [bx - 0.25, y1 + 0.55], [bx - 0.25, TOP + 1.16], [bx, TOP + 1.16]]);
  const rx = bx + bw + 0.3, rw = W - MX - rx;
  node(s, "evals/reports", rx, y1, rw, h1, { status: st, kind: "store", sub: "JSON + markdown", fontSize: 12, subSize: 10.5 });
  arrow(s, bx + bw, TOP + 0.29, rx, y1 + 0.3);
  arrow(s, bx + bw, TOP + 1.16, rx, y1 + 0.55);
  text(s, "README results table and the review deck read these reports.", { x: bx, y: TOP + 1.6, w: W - MX - bx, h: 0.4, fontSize: 11.5, italic: true, color: PALETTE.slate });
  // Judge calibration loop
  const ly = 4.35;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: ly, w: CW, h: 2.42, fill: { color: "F6F8FB" }, line: { type: "none" }, objectName: oid("lane") });
  text(s, "Judge calibration", { x: MX + 0.15, y: ly + 0.12, w: 2.5, h: 0.3, fontSize: 14, bold: true });
  text(s, "Before trusting the LLM judge", { x: MX + 0.15, y: ly + 0.42, w: 2.5, h: 0.3, fontSize: 11, color: PALETTE.slate });
  const cy = ly + 0.95;
  node(s, "60 answers", MX + 0.15, cy, 1.5, 0.7, { kind: "io", fontSize: 12.5 });
  node(s, "You rate 1 to 5", 2.6, ly + 0.55, 1.85, 0.6, { status: st, sub: "human_labels.csv", fontSize: 12, subSize: 10 });
  node(s, "Judge rates 1 to 5", 2.6, ly + 1.4, 1.85, 0.6, { status: st, fontSize: 12 });
  path_(s, [[MX + 1.65, cy + 0.35], [2.4, cy + 0.35], [2.4, ly + 0.85], [2.6, ly + 0.85]]);
  path_(s, [[2.4, cy + 0.35], [2.4, ly + 1.7], [2.6, ly + 1.7]]);
  node(s, "Cohen's kappa", 4.95, cy, 1.8, 0.7, { status: st, sub: "score ≥ 4 = faithful", fontSize: 12.5, subSize: 10 });
  arrow(s, 4.45, ly + 0.85, 4.95, cy + 0.2);
  arrow(s, 4.45, ly + 1.7, 4.95, cy + 0.5);
  node(s, "κ ≥ 0.6?", 7.2, cy - 0.12, 1.6, 0.95, { kind: "decision", fontSize: 13 });
  arrow(s, 6.75, cy + 0.35, 7.2, cy + 0.35);
  node(s, "Use the judge in evals", 9.3, cy, 1.9, 0.7, { status: st, fontSize: 12.5 });
  arrow(s, 8.8, cy + 0.35, 9.3, cy + 0.35);
  label(s, "yes", 8.85, cy + 0.05, 0.4);
  node(s, "Rewrite judge prompt", 9.3, ly + 1.75, 1.9, 0.55, { status: st, fontSize: 12 });
  path_(s, [[8.0, cy + 0.83], [8.0, ly + 2.02], [9.3, ly + 2.02]]);
  label(s, "no", 8.07, ly + 1.72, 0.4);
  path_(s, [[11.2, ly + 2.02], [11.45, ly + 2.02], [11.45, ly + 2.3], [3.52, ly + 2.3], [3.52, ly + 2.0]], { color: PALETTE.coral });
  text(s, "Faithfulness = (score - 1) / 4, averaged over answers.", { x: 11.3, y: cy, w: W - MX - 11.35, h: 0.75, fontSize: 11, color: PALETTE.ink2 });
}

// ================================================================= 15. Metrics defined
{
  const s = contentSlide("Quality", stageKicker(8, "Evaluation"), {
    title: "Every metric, in one line",
    takeaway: "Retrieval is scored at article level; generation by a calibrated judge; the classifier against labels checked by hand.",
    notes: "These are the numbers the review deck tracks. Retrieval metrics are computed at article level, so five windows of one article count as one hit. Faithfulness and citation precision come from the calibrated judge. Invented citations shown to users is a hard guardrail with a target of zero. Classifier accuracy is measured on forty scenarios whose labels I checked against the text, with ambiguous cases scored separately.",
  });
  const rows = [[th("Metric"), th("Definition"), th("Target", { align: "center" }), th("Runs", { align: "center" })]];
  [
    ["Recall@5", "Share of gold articles found in the top 5 (windows of one article count once)", "≥ 0.85", "every PR"],
    ["MRR@10", "1 / rank of the first gold article, averaged over questions", "≥ 0.70", "every PR"],
    ["nDCG@10", "Rank-weighted hits, divided by the best possible ranking", "reported", "every PR"],
    ["Faithfulness", "Judge score 1 to 5 mapped to (score - 1) / 4", "≥ 0.85", "weekly"],
    ["Citation precision", "Cited IDs whose article is gold (strict) or that support the sentence (lenient)", "≥ 0.90", "weekly"],
    ["Invented citations", "Cited IDs not in the retrieved set that reach the user", "0", "every answer"],
    ["Refusal accuracy", "Out-of-scope questions answered with a refusal", "≥ 95%", "weekly"],
    ["Tier accuracy", "Correct tier on the non-ambiguous risk scenarios (40 in total)", "≥ 85%", "weekly"],
    ["Cohen's kappa", "Judge vs human agreement beyond chance, on 60 answers", "≥ 0.6", "per judge prompt"],
  ].forEach(([a, b, c, d]) => rows.push([td(a, { bold: true }), td(b, { fontSize: 13, color: PALETTE.ink2 }), td(c, { align: "center" }), td(d, { align: "center", fontSize: 13, color: PALETTE.slate })]));
  s.addTable(rows, tableOpts(MX, TOP, [2.2, 6.9, 1.35, 1.68], [0.4, ...Array(9).fill(0.47)]));
}

// ================================================================= 16. Stage 9: fine-tuning
{
  const s = contentSlide("Quality", stageKicker(9, "Fine-tuning"), {
    title: "Fine-tune the embedder, then shrink it",
    takeaway: "Train only on train-split articles, prove the lift on the test split, and ship an int8 ONNX model with no PyTorch.",
    notes: "The fine-tuning stage teaches a small multilingual model what compliance questions about these laws look like. An LLM writes one English and one French question for each sampled train chunk; I review a sample and drop bad pairs. A leakage test guarantees no dev or test article is in the pairs. Training uses the multiple negatives ranking loss, where every other passage in the batch is a negative, so no hard-negative mining is needed. The model is scored with our own harness against the base model, then exported to ONNX and quantised to int8; the quantised model must lose one point of Recall@5 or less.",
  });
  legend(s);
  const st = ST.finetune;
  const r1 = [["Train-split chunks", "about 800 sampled"], ["LLM writes questions", "1 EN + 1 FR each, cached"], ["Review by hand", "read 50, drop bad pairs"], ["1,000 to 1,600 pairs", "(question, passage)"], ["Leakage test", "no dev or test article"]];
  const r2 = [["MNRL training", "Colab/Kaggle GPU, 3 epochs"], ["Base vs fine-tuned", "test split, own harness"], ["ONNX export", "optimum"], ["int8 quantization", "dynamic, onnxruntime"], ["Parity check", "cos ≥ 0.98; drop ≤ 1 pt"], ["Hugging Face Hub", "then the cloud index"]];
  const draw = (row, y, h) => {
    const g = 0.24, w = (CW - g * (row.length - 1)) / row.length;
    row.forEach(([l, sub], i) => {
      const x = MX + i * (w + g);
      node(s, l, x, y, w, h, { status: st, sub, fontSize: 12.5, subSize: 10.5 });
      if (i < row.length - 1) arrow(s, x + w, y + h / 2, x + w + g, y + h / 2);
    });
    return { w, g };
  };
  text(s, "Data", { x: MX, y: TOP, w: 2, h: 0.28, fontSize: 12, bold: true, color: PALETTE.slate });
  const a = draw(r1, TOP + 0.3, 0.82);
  text(s, "Model", { x: MX, y: 3.6, w: 2, h: 0.28, fontSize: 12, bold: true, color: PALETTE.slate });
  draw(r2, 3.9, 0.82);
  const lastX = MX + 4 * (a.w + a.g) + a.w / 2;
  path_(s, [[lastX, TOP + 1.12], [lastX, 3.5], [MX + 0.9, 3.5], [MX + 0.9, 3.9]], { color: PALETTE.gold, width: 1.5 });
  const cards = [
    ["Base model", "paraphrase-multilingual-MiniLM-L12-v2: 118M parameters, 384 dimensions, 50+ languages; max length raised to 256 tokens."],
    ["Why MNRL", "Every other passage in a batch of 32 acts as a negative, so no hard-negative mining is needed."],
    ["Honest reporting", "Report hand-written and synthetic questions separately; aim for +5 points Recall@5, explain a smaller lift."],
  ];
  const cw = (CW - 2 * 0.25) / 3;
  cards.forEach(([h, b], i) => card(s, h, b, MX + i * (cw + 0.25), 5.05, cw, 1.4, { fontSize: 12.5 }));
}

// ================================================================= 17. Stage 10: CI/CD and Cloud Run
pres.addSection({ title: "Operations" });
{
  const s = contentSlide("Operations", stageKicker(10, "Ship"), {
    title: "From git push to Cloud Run",
    takeaway: "Every push is linted and tested. A green main deploys a candidate revision that must pass a smoke test before it gets traffic.",
    notes: "CI runs on every push: ruff, mypy and pytest with an 80 percent coverage gate. Pull requests that touch retrieval also run the retrieval evaluation and fail on a two-point drop. When main is green, the deploy workflow authenticates to Google Cloud with workload identity federation, so no key file sits in GitHub. It builds a small image without PyTorch, pushes it to Artifact Registry and deploys it with no traffic under a candidate tag. Only if the smoke test passes on the candidate URL does traffic move; otherwise the old revision keeps serving.",
  });
  legend(s);
  const sd = ST.deploy;
  const y1 = TOP + 0.15, h = 0.85;
  node(s, "git push", MX, y1, 1.35, h, { kind: "io", fontSize: 13 });
  node(s, "ci.yml", 2.25, y1, 2.55, h, { status: ST.ci, sub: "ruff · mypy · pytest, coverage ≥ 80%", fontSize: 13, mono: true, subSize: 10.5 });
  node(s, "eval.yml", 5.2, y1, 2.45, h, { status: sd, sub: "PRs touching retrieval; fail on -2 pts", fontSize: 13, mono: true, subSize: 10.5 });
  node(s, "deploy.yml", 8.05, y1, 2.1, h, { status: sd, sub: "after CI is green on main", fontSize: 13, mono: true, subSize: 10.5 });
  node(s, "Keyless auth", 10.55, y1, W - MX - 10.55, h, { status: sd, sub: "Workload Identity Federation", fontSize: 13, subSize: 10.5 });
  arrow(s, MX + 1.35, y1 + h / 2, 2.25, y1 + h / 2);
  arrow(s, 4.8, y1 + h / 2, 5.2, y1 + h / 2, { dash: "dash" });
  arrow(s, 7.65, y1 + h / 2, 8.05, y1 + h / 2);
  arrow(s, 10.15, y1 + h / 2, 10.55, y1 + h / 2);
  const y2 = 3.6;
  const r2 = [["Build image", "no PyTorch; < 450 MB", MX, 1.95], ["Push", "Artifact Registry", 2.95, 1.8], ["Deploy candidate", "--no-traffic --tag candidate", 5.15, 2.25]];
  r2.forEach(([l, sub, x, w], i) => {
    node(s, l, x, y2, w, h, { status: sd, sub, fontSize: 13, subSize: 10.5 });
    if (i < r2.length - 1) arrow(s, x + w, y2 + h / 2, r2[i + 1][2], y2 + h / 2);
  });
  path_(s, [[W - MX - 1.09, y1 + h], [W - MX - 1.09, 3.35], [MX + 0.97, 3.35], [MX + 0.97, y2]], { color: PALETTE.gold, width: 1.5 });
  node(s, "Smoke test", 7.8, y2, 1.75, h, { status: sd, sub: "/health, /search", fontSize: 13, subSize: 10.5 });
  arrow(s, 7.4, y2 + h / 2, 7.8, y2 + h / 2);
  node(s, "pass?", 9.95, y2 - 0.08, 1.15, 1.0, { kind: "decision", fontSize: 12.5 });
  arrow(s, 9.55, y2 + h / 2, 9.95, y2 + h / 2);
  node(s, "Shift traffic", 11.45, y2, W - MX - 11.45, h, { status: sd, sub: "--to-latest", fontSize: 12.5, subSize: 10.5 });
  arrow(s, 11.1, y2 + h / 2, 11.45, y2 + h / 2);
  label(s, "yes", 11.1, y2 + 0.08, 0.4);
  node(s, "Old revision keeps serving", 9.55, 4.78, 1.95, 0.55, { kind: "neutral", fontSize: 11.5 });
  arrow(s, 10.525, y2 + 0.92, 10.525, 4.78);
  label(s, "no", 10.6, 4.5, 0.4);
  const cards = [
    ["Cloud Run settings", "europe-west1 · scale 0 to 2 instances · 1 vCPU, 1 GiB · concurrency 8 · 60 s timeout"],
    ["Secrets", "Gemini, Groq, Qdrant keys and the Sheets service account live in Secret Manager, never in the image or git."],
    ["EUR 0 by design", "Scale to zero, 200 LLM requests a day, one image kept, EUR 1 budget alert, Gemini key in a project without billing."],
  ];
  const cw = (CW - 2 * 0.25) / 3;
  cards.forEach(([hd, b], i) => card(s, hd, b, MX + i * (cw + 0.25), 5.5, cw, 1.25, { fontSize: 12, headSize: 12.5 }));
}

// ================================================================= 18. Stage 11: observability
{
  const s = contentSlide("Operations", stageKicker(11, "Observe"), {
    title: "Observability: what did each request cost?",
    takeaway: "One trace and one JSON log line per request answer: how long, which provider, how many tokens, what was cited.",
    notes: "Every request leaves two records. A Langfuse trace shows each span: guardrails, retrieval and each LLM call with its tokens and latency. A JSON line on stdout becomes a structured Cloud Logging entry with the same headline fields. From token counts and a provider's public price we compute what a request would cost on a paid plan, even though the bill is zero. Personal data is redacted before anything is traced, and classify inputs are not captured at all. The timings shown are illustrative, based on the example log line in the project guide.",
  });
  legend(s);
  const st = ST.observe;
  const lx = MX, lw = 2.55, tx = 3.3, tw = 4.6, scale = tw / 2.0; // 0 to 2.0 s
  text(s, "Trace of one /ask (illustrative)", { x: lx, y: TOP, w: 7, h: 0.3, fontSize: 14, bold: true });
  [0, 0.5, 1.0, 1.5, 2.0].forEach((t) => {
    const x = tx + t * scale;
    s.addShape(pres.shapes.LINE, { x, y: TOP + 0.62, w: 0, h: 3.0, line: { color: "E3E7EE", width: 0.75 }, objectName: oid("grid") });
    text(s, `${t.toFixed(1)} s`, { x: x - 0.3, y: TOP + 0.36, w: 0.6, h: 0.24, fontSize: 10, color: PALETTE.slate, align: "center" });
  });
  const spans = [
    ["POST /ask", 0, 1.84, PALETTE.ink, "1,840 ms"],
    ["guardrails + redaction", 0, 0.01, PALETTE.blue, ""],
    ["retrieve: dense + BM25 + RRF", 0.01, 0.13, PALETTE.blue, ""],
    ["llm.chat: gemini", 0.13, 1.8, PALETTE.gold, "2,150 in / 210 out tokens"],
    ["verify citations", 1.8, 1.81, PALETTE.blue, ""],
    ["log_event", 1.81, 1.84, PALETTE.blue, ""],
  ];
  spans.forEach(([n, a, b, c, note], i) => {
    const y = TOP + 0.75 + i * 0.47;
    text(s, n, { x: lx + (i ? 0.2 : 0), y, w: lw, h: 0.34, fontSize: 12.5, bold: i === 0, valign: "middle" });
    s.addShape(pres.shapes.RECTANGLE, { x: tx + a * scale, y: y + 0.05, w: Math.max(0.05, (b - a) * scale), h: 0.24, fill: { color: c }, line: { type: "none" }, objectName: oid("span") });
    if (note) text(s, note, { x: tx + a * scale + 0.08, y: y + 0.05, w: 3.0, h: 0.24, fontSize: 10.5, bold: true, color: c === PALETTE.gold ? PALETTE.ink : PALETTE.white, valign: "middle" });
  });
  const jx = 8.35, jw = W - MX - jx;
  text(s, "The JSON log line", { x: jx, y: TOP, w: jw, h: 0.3, fontSize: 14, bold: true });
  mono(s, [
    "{\"severity\": \"INFO\",",
    " \"event\": \"ask\",",
    " \"provider\": \"gemini\",",
    " \"cache_hit\": false,",
    " \"latency_ms\": 1840,",
    " \"input_tokens\": 2150,",
    " \"output_tokens\": 210,",
    " \"n_citations\": 3,",
    " \"invented\": 0,",
    " \"refused\": false}",
  ].join("\n"), jx, TOP + 0.38, jw, 2.95, { fontSize: 11 });
  const cards = [
    ["Cost per query", "input tokens × input price + output tokens × output price, at paid-tier prices. Reported in the README."],
    ["Privacy", "redact_pii runs before tracing; /classify inputs are never captured."],
    ["Free-tier watch", "Langfuse Hobby: 50,000 units a month. Near the limit, trace 1 request in 5."],
  ];
  const cw = (CW - 2 * 0.25) / 3;
  cards.forEach(([h, b], i) => card(s, h, b, MX + i * (cw + 0.25), 5.6, cw, 1.15, { fontSize: 12 }));
  void st;
}

// ================================================================= 19. Resilience map
{
  const s = contentSlide("Operations", "Operations  ·  Resilience", {
    title: "When something fails, something takes over",
    takeaway: "Every failure mode has a fallback, a user-visible behaviour and a test that proves it.",
    notes: "This is the failure map for the whole pipeline. Free tiers run out, clusters get suspended, models invent things and users try injections. For each case the design names what takes over and what the user sees, and a test pins the behaviour. Three of these become live drills before release: exhausting the cap, removing the Gemini key, and stopping Qdrant.",
  });
  const rows = [[th("Failure"), th("What takes over"), th("User sees"), th("Proved by")]];
  [
    ["Gemini 429 or quota", "Retry with backoff, then Groq, then Ollama", "An answer, a bit slower", "test_fallback_chain"],
    ["Qdrant cluster suspended", "NumPy index inside the image", "An answer", "test_store_failover"],
    ["Google Sheets down", "Register error ignored", "The classification", "test_register_failure_is_ignored"],
    ["200 requests used today", "API stops calling the LLM", "429: try tomorrow", "test_daily_cap_resets_next_day"],
    ["Model invents a citation", "Invented ID stripped and logged", "Only verified citations", "test_rag_strips_invented_citations"],
    ["Answer not in the sources", "NOT_COVERED becomes a refusal", "A refusal in EN or FR", "test_rag_refuses_in_user_language"],
    ["Prompt injection", "Sources-only prompt + citation check", "A grounded answer", "safety suite, 40 prompts"],
    ["Slack 3-second limit", "Acknowledge first, answer after", "\"Looking it up...\"", "test_slack_handler"],
    ["Agent loops or bad output", "Schema errors fed back; 8-step budget", "A valid verdict or an error", "test_schema_errors_fed_back"],
  ].forEach(([a, b, c, d]) => rows.push([td(a, { bold: true, fontSize: 13 }), td(b, { fontSize: 13, color: PALETTE.ink2 }), td(c, { fontSize: 13 }), td(d, { fontSize: 10.5, fontFace: FONTS.mono, color: PALETTE.tealDark })]));
  s.addTable(rows, tableOpts(MX, TOP, [2.75, 3.75, 2.4, 3.23], [0.4, ...Array(9).fill(0.47)]));
}

// ================================================================= 20. Walkthrough: one question
pres.addSection({ title: "Walkthroughs" });
{
  const s = contentSlide("Walkthroughs", "Walkthrough  ·  /ask", {
    title: "One French question, end to end",
    takeaway: "\"Quelles pratiques d'IA sont interdites ?\" through all six steps. The passage shown is real corpus text.",
    notes: "Here is the Q&A path as one story. A French question arrives with lang set to fr. Guards check the key and the daily cap, and redact personal data for the logs. Hybrid retrieval should bring back Article 5 paragraph 1, which the French corpus splits into seven windows. The model sees five tagged sources and answers in French with bracketed IDs. The verifier keeps only IDs that were retrieved and turns them into French labels. The response and one log line close the request. Retrieval results here are the expected gold article, not a measured run.",
  });
  const steps = [
    ["Request", "POST /ask\n{\"question\": \"Quelles pratiques d'IA sont interdites ?\", \"lang\": \"fr\"}", true],
    ["Guards", "API key checked; daily cap counts 1 of 200; emails and phone numbers redacted before logging.", false],
    ["Retrieve", "Dense + BM25 + RRF. Expected top hit: AIA-Art5-1#1, \"Les pratiques en matière d'IA suivantes sont interdites: a) la mise sur le marché ...\"", false],
    ["Generate", "Five sources tagged [ID]; temperature 0; the answer is written in French and cites [AIA-Art5-1#1] after each rule.", false],
    ["Verify", "Every cited ID was retrieved; invented IDs removed. Label: \"Règlement IA, Art. 5(1)\".", false],
    ["Respond", "{answer, citations, sources, refused: false}, plus one JSON log line and a trace.", true],
  ];
  const cw = (CW - 2 * 0.45) / 3, ch = 1.92;
  steps.forEach(([h, b, isCode], i) => {
    const x = MX + (i % 3) * (cw + 0.45), y = TOP + 0.05 + Math.floor(i / 3) * (ch + 0.35);
    box(s, { x, y, w: cw, h: ch });
    numberBadge(s, i + 1, x + 0.18, y + 0.16, 0.42);
    text(s, h, { x: x + 0.75, y: y + 0.18, w: cw - 0.9, h: 0.38, fontSize: 15, bold: true, valign: "middle" });
    if (isCode) mono(s, b, x + 0.18, y + 0.72, cw - 0.36, ch - 0.88, { fontSize: 10.5, fill: PALETTE.white });
    else text(s, b, { x: x + 0.2, y: y + 0.72, w: cw - 0.4, h: ch - 0.85, fontSize: 12.5, color: PALETTE.ink2 });
    if (i % 3 < 2) arrow(s, x + cw + 0.05, y + ch / 2, x + cw + 0.4, y + ch / 2, { color: PALETTE.gold, width: 2 });
  });
  path_(s, [[MX + 2 * (cw + 0.45) + cw / 2, TOP + 0.05 + ch], [MX + 2 * (cw + 0.45) + cw / 2, TOP + ch + 0.22], [MX + cw / 2, TOP + ch + 0.22], [MX + cw / 2, TOP + ch + 0.4]], { color: PALETTE.gold, width: 2 });
  text(s, "Illustrative walkthrough: the hit shown is the expected gold article, not a measured run.", { x: MX, y: 6.55, w: CW, h: 0.28, fontSize: 11.5, italic: true, color: PALETTE.slate });
}

// ================================================================= 21. Walkthrough: one classification (sequence diagram)
{
  const s = contentSlide("Walkthroughs", "Walkthrough  ·  /classify", {
    title: "One classification, as a sequence",
    takeaway: "\"Ranks job applicants from their CVs\": the agent reads Article 5, then Annex III, and submits a grounded verdict.",
    notes: "This sequence diagram shows who talks to whom during one classification. The API hands the description to the agent. The agent first searches the prohibited practices, finds nothing that matches, then searches the employment use cases and finds Annex III point 4 and Article 6 paragraph 2. It submits high risk citing those two IDs; the validator accepts because both were retrieved. The API logs a hashed row to the Sheets register and returns the verdict with its disclaimer. The exact searches the model makes will vary; this is illustrative.",
  });
  const lanes = [["Client", 1.3], ["FastAPI", 3.65], ["Agent (LLM)", 6.25], ["HybridRetriever", 9.1], ["Sheets", 11.85]];
  const hy = TOP + 0.02, hw = 1.75, ly0 = hy + 0.42, ly1 = 6.55;
  lanes.forEach(([n, x], i) => {
    s.addText(n, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.07, x: x - hw / 2, y: hy, w: hw, h: 0.4, fill: { color: i === 0 ? PALETTE.ink : PALETTE.mist }, color: i === 0 ? PALETTE.white : PALETTE.ink, fontSize: 12.5, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("lifeline-head") });
    s.addShape(pres.shapes.LINE, { x, y: ly0, w: 0, h: ly1 - ly0, line: { color: "AEB7C4", width: 1, dashType: "dash" }, objectName: oid("lifeline") });
  });
  const X = Object.fromEntries(lanes.map(([n, x]) => [n, x]));
  const msgs = [
    ["Client", "FastAPI", "POST /classify (description)"],
    ["FastAPI", "Agent (LLM)", "classify(description)"],
    ["Agent (LLM)", "HybridRetriever", "search(\"Art. 5 practices, hiring\")"],
    ["HybridRetriever", "Agent (LLM)", "AIA-Art5-1#1 ... no matching practice"],
    ["Agent (LLM)", "HybridRetriever", "search(\"Annex III, recruitment\")"],
    ["HybridRetriever", "Agent (LLM)", "AIA-AnnexIII-4, AIA-Art6-2"],
    ["Agent (LLM)", "FastAPI", "submit: high_risk, cites both IDs → valid"],
    ["FastAPI", "Sheets", "append row: time, hash, tier, IDs"],
    ["FastAPI", "Client", "tier, reasons, citations, disclaimer"],
  ];
  msgs.forEach(([a, b, m], i) => {
    const y = ly0 + 0.4 + i * 0.44;
    const x1 = X[a], x2 = X[b], back = x2 < x1;
    arrow(s, x1, y, x2, y, { color: back ? PALETTE.blue : PALETTE.ink, dash: back ? "dash" : "solid", width: 1.25 });
    const lx = Math.min(x1, x2) + 0.1, lw = Math.abs(x2 - x1) - 0.2;
    text(s, m, { x: lx, y: y - 0.25, w: Math.max(lw, 2.4), h: 0.23, fontSize: 10.5, color: PALETTE.ink2, align: "center", valign: "bottom" });
  });
  text(s, "Illustrative: the searches the model chooses will vary from run to run. search = search_corpus.", { x: MX, y: 6.7, w: 8, h: 0.24, fontSize: 11, italic: true, color: PALETTE.slate });
}

// ================================================================= 22. Status
pres.addSection({ title: "Status and glossary" });
{
  const s = contentSlide("Status and glossary", "Status", {
    title: "Where the pipeline stands today",
    takeaway: "Ingestion is built and tested. The rest follows the ten-week plan, with retrieval and its baseline next.",
    notes: "Statuses come from content.json, so this slide changes as stages land. Today the ingestion stage is built and verified, CI exists but its green badge is not yet confirmed, and every other stage is planned. The next stage to build is the measured baseline and hybrid retrieval.",
  });
  const rows = [[th("#", { align: "center" }), th("Stage"), th("What it delivers"), th("Milestone", { align: "center" }), th("Status", { align: "center" })]];
  [
    [1, "Ingestion + IDs", "chunks.jsonl with stable IDs, EN and FR", "M0", ST.ingest],
    [2, "Indexing", "Qdrant collection, NumPy index, BM25", "M1-M2", ST.index],
    [3, "Hybrid retrieval", "dense + BM25 + RRF, optional rerank", "M2", ST.retrieval],
    [4, "LLM gateway", "chat() with cache, retries, fallback", "M3", ST.gateway],
    [5, "Cited answers", "verified citations, refusals, guardrails", "M3", ST.answer],
    [6, "Risk classifier", "tool-calling agent with validated output", "M4", ST.classifier],
    [7, "API + integrations", "FastAPI, UI, Slack, MCP, Sheets, upload", "M4, M6", ST.api],
    [8, "Evaluation", "splits, golden set, metrics, judge", "M1-M3", ST.eval],
    [9, "Fine-tuning", "MiniLM fine-tuned, int8 ONNX on the Hub", "M5", ST.finetune],
    [10, "Ship", "CI, keyless deploy, Cloud Run", "M0, M7", ST.ci === "in_progress" ? "in_progress" : ST.deploy],
    [11, "Observe", "Langfuse traces, JSON logs, cost", "M6", ST.observe],
  ].forEach(([n, a, b, c, st]) => rows.push([td(String(n), { align: "center", bold: true, fontSize: 13 }), td(a, { bold: true, fontSize: 13 }), td(b, { fontSize: 13, color: PALETTE.ink2 }), td(c, { align: "center", fontSize: 13 }), tdStatus(st)]));
  s.addTable(rows, tableOpts(MX, TOP, [0.6, 2.6, 5.43, 1.6, 1.9], [0.38, ...Array(11).fill(0.395)]));
}

// ================================================================= 23. Glossary
{
  const s = contentSlide("Status and glossary", "Glossary", {
    title: "Glossary",
    takeaway: "The terms used in this deck, in one line each.",
    notes: "A reference slide for non-specialists.",
  });
  const terms = [
    ["RAG", "Retrieve passages first, then let the model answer only from them"],
    ["Chunk", "One paragraph, recital or annex point; long ones split into windows"],
    ["Embedding", "A vector that places texts with similar meaning close together"],
    ["BM25", "Classic keyword scoring: rare words that match count most"],
    ["RRF", "Reciprocal rank fusion: merges ranked lists using ranks only"],
    ["Cross-encoder", "A model that reads query and passage together to rerank"],
    ["Recall@5 / MRR", "Was the right article in the top 5 / how high was it"],
    ["LLM judge", "An LLM that scores answers; trusted only once calibrated"],
    ["Cohen's kappa", "Agreement between two raters beyond chance"],
    ["MNRL", "Contrastive loss using other batch items as negatives"],
    ["ONNX int8", "Portable model format with 8-bit weights: small, fast on CPU"],
    ["MCP", "Model Context Protocol: lets AI clients call ActWise as tools"],
    ["Cloud Run", "Google's container service that scales to zero"],
    ["WIF", "Workload Identity Federation: deploy from GitHub with no key file"],
  ];
  const half = Math.ceil(terms.length / 2), tw = (CW - 0.3) / 2;
  [terms.slice(0, half), terms.slice(half)].forEach((list, k) => {
    const rows = [[th("Term"), th("Meaning")]];
    list.forEach(([a, b]) => rows.push([td(a, { bold: true, fontSize: 13 }), td(b, { fontSize: 12.5, color: PALETTE.ink2 })]));
    s.addTable(rows, tableOpts(MX + k * (tw + 0.3), TOP, [1.7, tw - 1.7], [0.38, ...Array(list.length).fill(0.6)]));
  });
}

// ---------------------------------------------------------------- write
(async () => {
  await pres.writeFile({ fileName: OUT });
  await writeTheme(OUT);
  console.log(`wrote ${path.relative(process.cwd(), OUT)} (${pres.slides.length} slides)`);
})().catch((e) => { console.error(e); process.exit(1); });
