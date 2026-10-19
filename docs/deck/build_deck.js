// Build the ActWise project review deck from content.json (narrative) and facts.json (measured).
//
//   python docs/deck/collect.py     # refresh facts.json from the repo
//   node docs/deck/build_deck.js    # write docs/deck/ActWise_Project_Review.pptx
//
// Style, layouts and drawing helpers are shared with build_pipeline.js in common.js.
"use strict";

const path = require("path");
const { PALETTE, FONTS, W, MX, CW, TOP, CHIP, status, readJson, createDeck, helpers, writeTheme, HERE } = require("./common");

const OUT = path.join(HERE, "ActWise_Project_Review.pptx");
const content = readJson("content.json");
const facts = readJson("facts.json");

// ---------------------------------------------------------------- facts -> tokens
const fmt = (n) => Number(n).toLocaleString("en-US");
const pct = (a, b) => (b ? `${Math.round((100 * a) / b)}%` : "n/a");
const corpus = facts.corpus || {};
const official = content.corpus.official;

function unitCounts() {
  const units = corpus.units || {};
  let expected = 0, matched = 0;
  const langs = ["en", "fr"];
  for (const lang of langs)
    for (const [law, kinds] of Object.entries(official))
      for (const [kind, n] of Object.entries(kinds)) {
        expected += n;
        matched += Math.min(units[`${law}|${lang}|${kind}`] || 0, n);
      }
  return { expected, matched, perLang: expected / langs.length };
}
const uc = unitCounts();
const tests = facts.tests && facts.tests.passed ? facts.tests : null;
const fb = content.engineering_fallback;
const progress = facts.progress || [];
const m0 = progress.find((p) => p.id === "M0") || { done: 0, total: 0 };
const hist = corpus.length_histogram || {};
const histKeys = Object.keys(hist);
const capBin = histKeys.length ? hist[histKeys[histKeys.length - 1]] : 0;

const TOKENS = {
  chunks: fmt(corpus.total_chunks || 0),
  units_pct: pct(uc.matched, uc.expected),
  units_per_lang: fmt(uc.perLang),
  tests: String(tests ? tests.passed : fb.tests_passed),
  coverage: `${tests && tests.coverage_pct != null ? tests.coverage_pct : fb.coverage_pct}%`,
  m0_done: `${m0.done}/${m0.total}`,
  windowed_pct: pct(corpus.windowed_chunks || 0, corpus.total_chunks || 0),
  windowed: fmt(corpus.windowed_chunks || 0),
  split_paragraphs: fmt(corpus.split_paragraphs || 0),
  cap_pct: pct(capBin, corpus.total_chunks || 0),
};
// Fill {tokens}, and keep long dashes out of the slides.
const fill = (s) =>
  String(s == null ? "" : s)
    .replace(/\{(\w+)\}/g, (m, k) => (k in TOKENS ? TOKENS[k] : m))
    .replace(/[–—]/g, "-");

// ---------------------------------------------------------------- presentation + helpers
const meta = content.meta;
const pres = createDeck({
  title: `ActWise project review, iteration ${meta.iteration}`,
  subject: "ActWise: citation-grounded EU AI Act and GDPR assistant",
  author: meta.author,
  footer: `ActWise  ·  Project review  ·  Iteration ${meta.iteration}  ·  ${meta.date}`,
});
const { oid, text, box, chip, statusChip, iconCircle, numberBadge, line, contentSlide, th, td, tdStatus, pending, tableOpts } = helpers(pres, fill);

// ================================================================= 1. Title
pres.addSection({ title: "Overview" });
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Overview" });
  s.addText("ActWise", { placeholder: "title" });
  s.addText("Citation-grounded assistant for the EU AI Act and GDPR, in English and French", { placeholder: "subtitle" });
  s.addText([
    { text: `${meta.author}  ·  ${meta.role}`, options: { breakLine: true } },
    { text: fill(`Project review, iteration ${meta.iteration}  ·  ${meta.date}  ·  ${meta.trigger}`) },
  ], { placeholder: "meta" });
  // Motif: citation chips, the thing ActWise promises on every answer.
  const ids = ["[AIA-Art6-2]", "[GDPR-Art17]", "[AIA-AnnexIII-4]", "[AIA-Art5-1]", "[GDPR-Art22-1]", "[AIA-Art50-1]"];
  const xs = [9.0, 10.15, 8.7, 9.75, 9.2, 10.35];
  ids.forEach((id, i) => {
    const hl = i === 2;
    s.addText(id, {
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.12, x: xs[i], y: 1.35 + i * 0.78, w: 2.75, h: 0.52,
      fill: { color: hl ? PALETTE.gold : PALETTE.navy2 }, line: { color: hl ? PALETTE.gold : PALETTE.navyLine, width: 1 },
      fontFace: FONTS.mono, fontSize: 16, bold: true, color: hl ? PALETTE.ink : PALETTE.onDark,
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("cite-chip"),
    });
  });
  s.addText(fill(`Stage: ${meta.stage}`), {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.14, x: 0.8, y: 4.75, w: 4.2, h: 0.42,
    fill: { color: PALETTE.navy2 }, line: { color: PALETTE.gold, width: 1 }, color: PALETTE.gold,
    fontSize: 14, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("stage"),
  });
  s.addNotes(fill(content.title_notes || ""));
}

// ================================================================= 2. Executive summary
{
  const sec = content.exec_summary;
  const s = contentSlide("Overview", "Overview", sec);
  const n = sec.stats.length, gap = 0.3, w = (CW - gap * (n - 1)) / n;
  sec.stats.forEach((st, i) => {
    const x = MX + i * (w + gap);
    box(s, { x, y: TOP, w, h: 1.7 });
    text(s, st.value, { x: x + 0.3, y: TOP + 0.2, w: w - 0.6, h: 0.8, fontFace: FONTS.head, fontSize: 44, bold: true, color: PALETTE.ink });
    text(s, st.label, { x: x + 0.3, y: TOP + 1.02, w: w - 0.6, h: 0.55, fontSize: 14, color: PALETTE.slate });
  });
  sec.points.forEach((p, i) => {
    const y = 4.15 + i * 0.66;
    const st = status(p.status);
    chip(s, p.tag, MX, y + 0.04, 1.05, st.tone, { h: 0.34, fontSize: 12 });
    text(s, p.text, { x: MX + 1.3, y, w: CW - 1.3, h: 0.5, fontSize: 15, valign: "middle", color: PALETTE.ink });
  });
}

// ================================================================= 3. Problem and product
pres.addSection({ title: "Product" });
{
  const sec = content.product;
  const s = contentSlide("Product", "Product", sec);
  const colW = 5.55, rightX = W - MX - colW;
  const col = (x, head, items, tone) => {
    text(s, head, { x, y: TOP, w: colW, h: 0.4, fontFace: FONTS.head, fontSize: 20, bold: true, color: PALETTE.ink });
    items.forEach((it, i) => {
      const y = TOP + 0.6 + i * 1.12;
      iconCircle(s, it.icon, x, y, 0.62, tone);
      text(s, it.head, { x: x + 0.85, y: y - 0.02, w: colW - 0.85, h: 0.32, fontSize: 16, bold: true });
      text(s, it.text, { x: x + 0.85, y: y + 0.31, w: colW - 0.85, h: 0.7, fontSize: 14, color: PALETTE.ink2 });
    });
  };
  col(MX, "The problem", sec.problem, PALETTE.coral);
  col(rightX, "What ActWise does", sec.solution, PALETTE.teal);
  s.addShape(pres.shapes.RIGHT_ARROW, { x: MX + colW + 0.32, y: 3.75, w: 0.62, h: 0.5, fill: { color: PALETTE.gold }, line: { type: "none" }, objectName: oid("arrow") });
  box(s, { x: MX, y: 6.08, w: CW, h: 0.62 });
  text(s, sec.users, { x: MX + 0.3, y: 6.08, w: CW - 0.6, h: 0.62, valign: "middle", fontSize: 14, color: PALETTE.ink2 });
}

// ================================================================= 4. Features
{
  const sec = content.features;
  const s = contentSlide("Product", "Product", sec);
  const cols = 4, gap = 0.25, w = (CW - gap * (cols - 1)) / cols, h = 2.18;
  sec.items.forEach((f, i) => {
    const x = MX + (i % cols) * (w + gap), y = TOP + Math.floor(i / cols) * (h + 0.25);
    box(s, { x, y, w, h });
    iconCircle(s, f.icon, x + 0.25, y + 0.25, 0.55, PALETTE.ink);
    text(s, `${f.id} · ${f.milestone}`, { x: x + 0.95, y: y + 0.3, w: 0.95, h: 0.3, fontSize: 12, bold: true, color: PALETTE.slate, valign: "middle" });
    statusChip(s, f.status, x + w - 1.15, y + 0.3, 0.9, { h: 0.3, fontSize: 11 });
    text(s, f.name, { x: x + 0.25, y: y + 0.95, w: w - 0.5, h: 0.34, fontSize: 16, bold: true });
    text(s, f.text, { x: x + 0.25, y: y + 1.32, w: w - 0.45, h: 0.78, fontSize: 14, color: PALETTE.ink2 });
  });
}

// ================================================================= 5. Architecture
{
  const sec = content.architecture;
  const s = contentSlide("Product", "Product", sec);
  // Legend, top right
  chip(s, "Built", 10.55, 0.42, 0.9, "teal", { h: 0.28 });
  s.addText("Planned", { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: 11.6, y: 0.42, w: 1.1, h: 0.28, fill: { color: PALETTE.white }, line: { color: "8C98AA", width: 1, dashType: "dash" }, color: PALETTE.ink2, fontSize: 11, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("legend") });
  const colW = 3.6, gap = (CW - 3 * colW) / 2, panelH = 3.72;
  const comp = (c, x, y, w, h) => {
    const built = ["done", "met", "fixed"].includes(c.status);
    const partial = ["in_progress", "partial"].includes(c.status);
    s.addText(fill(c.name), {
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.07, x, y, w, h,
      fill: { color: built ? PALETTE.teal : partial ? PALETTE.goldSoft : PALETTE.white },
      line: built ? { type: "none" } : { color: partial ? PALETTE.gold : "8C98AA", width: 1, dashType: partial ? "solid" : "dash" },
      color: built ? PALETTE.white : PALETTE.ink2, fontSize: 13, bold: built, align: "center", valign: "middle",
      margin: [0, 0.08, 0, 0.08], isTextBox: true, objectName: oid("component"),
    });
  };
  sec.columns.forEach((c, i) => {
    const x = MX + i * (colW + gap);
    box(s, { x, y: TOP, w: colW, h: panelH, fill: PALETTE.mist });
    text(s, c.name, { x: x + 0.2, y: TOP + 0.14, w: colW - 0.4, h: 0.32, fontSize: 15, bold: true });
    text(s, c.sub, { x: x + 0.2, y: TOP + 0.46, w: colW - 0.4, h: 0.26, fontSize: 12, color: PALETTE.slate });
    c.components.forEach((k, j) => comp(k, x + 0.2, TOP + 0.88 + j * 0.7, colW - 0.4, 0.56));
    if (i < sec.columns.length - 1)
      s.addShape(pres.shapes.RIGHT_ARROW, { x: x + colW + (gap - 0.4) / 2, y: TOP + panelH / 2 - 0.2, w: 0.4, h: 0.4, fill: { color: PALETTE.gold }, line: { type: "none" }, objectName: oid("arrow") });
  });
  const cc = sec.cross_cutting, ccW = (CW - 0.25 * (cc.length - 1)) / cc.length;
  text(s, "Across all layers", { x: MX, y: 5.98, w: 3, h: 0.25, fontSize: 12, bold: true, color: PALETTE.slate });
  cc.forEach((c, i) => comp(c, MX + i * (ccW + 0.25), 6.28, ccW, 0.48));
}

// ================================================================= 6. Roadmap
pres.addSection({ title: "Progress" });
{
  const sec = content.roadmap;
  const s = contentSlide("Progress", "Plan and progress", sec);
  const rows = progress.length ? progress : [];
  const rowH = 0.36, trackX = 6.45, trackW = 4.1;
  text(s, "Milestone", { x: MX, y: TOP - 0.05, w: 3, h: 0.25, fontSize: 12, bold: true, color: PALETTE.slate });
  text(s, "When", { x: 5.0, y: TOP - 0.05, w: 1.3, h: 0.25, fontSize: 12, bold: true, color: PALETTE.slate });
  text(s, "Checklist items done (TODO.md)", { x: trackX, y: TOP - 0.05, w: 4.2, h: 0.25, fontSize: 12, bold: true, color: PALETTE.slate });
  rows.forEach((r, i) => {
    const y = TOP + 0.28 + i * rowH;
    const st = r.done === 0 ? "planned" : r.done >= r.total ? "done" : "in_progress";
    if (i % 2 === 0) s.addShape(pres.shapes.RECTANGLE, { x: MX, y: y - 0.02, w: CW, h: rowH, fill: { color: "F7F8FB" }, line: { type: "none" }, objectName: oid("band") });
    text(s, r.id, { x: MX + 0.1, y, w: 0.75, h: rowH - 0.04, fontSize: 14, bold: true, valign: "middle" });
    text(s, r.name, { x: MX + 0.9, y, w: 3.45, h: rowH - 0.04, fontSize: 14, valign: "middle" });
    text(s, r.weeks ? r.weeks.replace(/^w/, "W") : "Before week 1", { x: 5.0, y, w: 1.4, h: rowH - 0.04, fontSize: 13, color: PALETTE.slate, valign: "middle" });
    const ty = y + rowH / 2 - 0.1;
    box(s, { x: trackX, y: ty, w: trackW, h: 0.16, fill: PALETTE.gray, radius: 0.08 });
    const frac = r.total ? r.done / r.total : 0;
    if (frac > 0) box(s, { x: trackX, y: ty, w: Math.max(0.16, trackW * frac), h: 0.16, fill: st === "done" ? PALETTE.teal : PALETTE.gold, radius: 0.08 });
    text(s, `${r.done}/${r.total}`, { x: trackX + trackW + 0.15, y, w: 0.75, h: rowH - 0.04, fontSize: 13, bold: true, valign: "middle", align: "right" });
    statusChip(s, st, W - MX - 1.12, y + rowH / 2 - 0.15, 1.1, { h: 0.27, fontSize: 11 });
  });
  text(s, sec.open_in_current, { x: MX, y: 6.5, w: CW, h: 0.3, fontSize: 13, italic: true, color: PALETTE.slate });
}

// ================================================================= 7. Metric tree
pres.addSection({ title: "Measurement" });
{
  const sec = content.metric_tree;
  const s = contentSlide("Measurement", "Measurement", sec);
  const L = 2.35, R = W - MX, RW = R - L; // label column | boxes
  const DY = 3.65, GY = 4.92, BH = 1.05; // driver row y, guardrail row y, box height
  const labels = [["North star", "what we optimise", TOP, 1.2], ["Drivers", "what we move", DY, BH], ["Guardrails", "what must not break", GY, BH]];
  labels.forEach(([a, b, y, h]) => {
    text(s, a, { x: MX, y: y + h / 2 - 0.3, w: 1.6, h: 0.32, fontSize: 16, bold: true });
    text(s, b, { x: MX, y: y + h / 2 + 0.02, w: 1.6, h: 0.28, fontSize: 12, color: PALETTE.slate });
  });
  const ns = sec.north_star, nsW = 6.6, nsX = L + (RW - nsW) / 2;
  box(s, { x: nsX, y: TOP, w: nsW, h: 1.2, fill: PALETTE.ink });
  text(s, ns.name, { x: nsX + 0.3, y: TOP + 0.12, w: nsW - 0.6, h: 0.4, fontFace: FONTS.head, fontSize: 20, bold: true, color: PALETTE.white });
  text(s, ns.definition, { x: nsX + 0.3, y: TOP + 0.52, w: nsW - 0.6, h: 0.6, fontSize: 14, color: PALETTE.onDark });
  const n = sec.drivers.length, gap = 0.25, bw = (RW - gap * (n - 1)) / n;
  const centers = sec.drivers.map((_, i) => L + i * (bw + gap) + bw / 2);
  line(s, nsX + nsW / 2, TOP + 1.2, 0, 0.21, PALETTE.slate);
  line(s, centers[0], TOP + 1.41, centers[n - 1] - centers[0], 0, PALETTE.slate);
  centers.forEach((cx) => line(s, cx, TOP + 1.41, 0, DY - TOP - 1.41, PALETTE.slate));
  const metricBox = (m, x, y, fillColor, targetText, targetColor, outline) => {
    box(s, { x, y, w: bw, h: BH, fill: fillColor, line: outline });
    text(s, m.name, { x: x + 0.2, y: y + 0.1, w: bw - 0.35, h: 0.52, fontSize: 15, bold: true, valign: "middle" });
    text(s, targetText, { x: x + 0.2, y: y + 0.66, w: bw - 0.35, h: 0.3, fontSize: 14, color: targetColor, bold: true });
  };
  sec.drivers.forEach((d, i) => metricBox(d, L + i * (bw + gap), DY, PALETTE.tealSoft, `Target ${d.target}`, PALETTE.tealDark));
  sec.guardrails.forEach((g, i) => metricBox(g, L + i * (bw + gap), GY, PALETTE.white, `Limit ${g.target}`, PALETTE.ink2, PALETTE.line));
  text(s, [
    { text: fill(ns.note), options: { italic: true, color: PALETTE.kicker, breakLine: true } },
    { text: fill(sec.companion), options: { color: PALETTE.ink2 } },
  ], { x: MX, y: 6.15, w: CW, h: 0.62, fontSize: 13 });
}

// ================================================================= 8. Scorecard: quality
{
  const sec = content.scorecard_quality;
  const s = contentSlide("Measurement", "Measurement", sec);
  const colW = [1.7, 4.23, 1.5, 1.5, 1.5, 1.7];
  const rows = [[th("Area"), th("Metric"), th("Target", { align: "center" }), th("Baseline", { align: "center" }), th("Current", { align: "center" }), th("Status", { align: "center" })]];
  sec.rows.forEach((r, i) => {
    const first = i === 0 || sec.rows[i - 1].area !== r.area;
    const span = sec.rows.filter((x) => x.area === r.area).length;
    const row = [];
    if (first) row.push(td(r.area, { bold: true, rowspan: span, valign: "middle", fill: { color: PALETTE.mist } }));
    row.push(td(r.metric), td(r.target, { align: "center" }), r.baseline ? td(r.baseline, { align: "center" }) : pending(), r.current ? td(r.current, { align: "center", bold: true }) : pending(), tdStatus(r.status));
    rows.push(row);
  });
  s.addTable(rows, tableOpts(MX, TOP, colW, [0.42, ...sec.rows.map(() => 0.42)]));
}

// ================================================================= 9. Scorecard: ops
{
  const sec = content.scorecard_ops;
  const s = contentSlide("Measurement", "Measurement", sec);
  const colW = [1.9, 4.73, 1.75, 1.75, 2.0];
  const rows = [[th("Area"), th("Metric"), th("Target", { align: "center" }), th("Current", { align: "center" }), th("Status", { align: "center" })]];
  sec.rows.forEach((r, i) => {
    const first = i === 0 || sec.rows[i - 1].area !== r.area;
    const span = sec.rows.filter((x) => x.area === r.area).length;
    const row = [];
    if (first) row.push(td(r.area, { bold: true, rowspan: span, fill: { color: PALETTE.mist } }));
    row.push(td(r.metric), td(r.target, { align: "center" }), r.current ? td(r.current, { align: "center", bold: true }) : pending(), tdStatus(r.status));
    rows.push(row);
  });
  s.addTable(rows, tableOpts(MX, TOP, colW, [0.42, ...sec.rows.map(() => 0.42)]));
  const tsrc = tests ? `pytest run on ${String(facts.generated_at || "").slice(0, 10)}` : fb.source;
  text(s, `Test and coverage source: ${tsrc}.`, { x: MX, y: 6.45, w: CW, h: 0.3, fontSize: 12, color: PALETTE.slate, italic: true });
}

// ================================================================= 10. Evaluation design
{
  const sec = content.eval_design;
  const s = contentSlide("Measurement", "Measurement", sec);
  const n = sec.steps.length, gap = 0.25, w = (CW - gap * (n - 1)) / n, d = 0.62;
  const cx = (i) => MX + i * (w + gap) + w / 2;
  line(s, cx(0), TOP + d / 2, cx(n - 1) - cx(0), 0, PALETTE.gold, 2);
  sec.steps.forEach((st, i) => {
    const x = MX + i * (w + gap);
    numberBadge(s, i + 1, cx(i) - d / 2, TOP, d);
    const by = TOP + 0.9, bh = 3.15;
    box(s, { x, y: by, w, h: bh });
    text(s, st.head, { x: x + 0.2, y: by + 0.18, w: w - 0.4, h: 0.36, fontSize: 16, bold: true });
    text(s, st.text, { x: x + 0.2, y: by + 0.6, w: w - 0.35, h: 1.85, fontSize: 14, color: PALETTE.ink2 });
    if (st.artifact)
      s.addText(fill(st.artifact), {
        shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, x: x + 0.15, y: by + bh - 0.55, w: w - 0.3, h: 0.4,
        fill: { color: PALETTE.white }, line: { color: PALETTE.line, width: 0.75 }, fontFace: FONTS.mono, fontSize: 11,
        color: PALETTE.ink2, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("artifact"),
      });
  });
  text(s, sec.footnote || "", { x: MX, y: 6.38, w: CW, h: 0.35, fontSize: 13, italic: true, color: PALETTE.slate });
}

// ================================================================= 11. Hypotheses
{
  const sec = content.hypotheses;
  const s = contentSlide("Measurement", "Measurement", sec);
  const colW = [0.6, 4.35, 3.6, 0.8, 1.3, 1.48];
  const rows = [[th("#"), th("Hypothesis"), th("How we test it"), th("Step", { align: "center" }), th("Status", { align: "center" }), th("Result", { align: "center" })]];
  sec.items.forEach((h) => rows.push([
    td(h.id, { bold: true }), td(h.text), td(h.test, { color: PALETTE.ink2, fontSize: 13 }), td(h.step, { align: "center" }),
    tdStatus(h.status), h.result ? td(h.result, { align: "center", fontSize: 13 }) : pending(),
  ]));
  s.addTable(rows, tableOpts(MX, TOP, colW, [0.42, ...sec.items.map(() => 0.66)]));
}

// ================================================================= 12. Corpus
pres.addSection({ title: "Findings" });
{
  const sec = content.corpus;
  const s = contentSlide("Findings", "Findings: data", sec);
  const g = corpus.by_group || {};
  const cats = [["ai_act", "en", "AI Act EN"], ["ai_act", "fr", "AI Act FR"], ["gdpr", "en", "GDPR EN"], ["gdpr", "fr", "GDPR FR"]];
  const kinds = [["article", "Articles"], ["recital", "Recitals"], ["annex", "Annexes"]];
  const data = kinds.map(([k, name]) => ({ name, labels: cats.map((c) => c[2]), values: cats.map(([law, lang]) => g[`${law}|${lang}|${k}`] || 0) }));
  s.addChart(pres.charts.BAR, data, {
    x: MX, y: TOP, w: 7.0, h: 4.3, barDir: "col", barGrouping: "stacked", chartColors: PALETTE.series,
    showTitle: true, title: `Chunks by law, language and kind (total ${TOKENS.chunks})`, titleFontSize: 14, titleColor: PALETTE.ink, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "ctr", dataLabelColor: PALETTE.white, dataLabelFontSize: 11, dataLabelFontFace: "+mn-lt",
    dataLabelFormatCode: "#,##0;;", // hide zero segments (GDPR has no annexes)
    showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: PALETTE.ink2, legendFontFace: "+mn-lt",
    catAxisLabelColor: PALETTE.ink2, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt",
    valAxisLabelColor: PALETTE.slate, valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt",
    valGridLine: { color: "E3E7EE", size: 0.75 }, catGridLine: { style: "none" }, barGapWidthPct: 60,
    objectName: oid("chart-corpus"),
  });
  // Official numbering vs parsed, per language
  const x = 8.0, w = W - MX - x;
  text(s, "Official units vs parsed", { x, y: TOP, w, h: 0.34, fontSize: 16, bold: true });
  const units = corpus.units || {};
  const rows = [[th("Law"), th("Unit"), th("Official", { align: "center" }), th("EN", { align: "center" }), th("FR", { align: "center" })]];
  const lawName = { ai_act: "AI Act", gdpr: "GDPR" };
  Object.entries(official).forEach(([law, ks]) => {
    const entries = Object.entries(ks);
    entries.forEach(([kind, n], j) => {
      const row = [];
      if (j === 0) row.push(td(lawName[law] || law, { bold: true, rowspan: entries.length, fill: { color: PALETTE.mist } }));
      const cell = (lang) => {
        const got = units[`${law}|${lang}|${kind}`] || 0;
        return td(String(got), { align: "center", bold: true, color: got === n ? PALETTE.tealDark : PALETTE.coral, fill: { color: got === n ? PALETTE.tealSoft : PALETTE.coralSoft } });
      };
      const plural = { recital: "Recitals", article: "Articles", annex: "Annexes" };
      row.push(td(plural[kind] || kind), td(String(n), { align: "center" }), cell("en"), cell("fr"));
      rows.push(row);
    });
  });
  s.addTable(rows, tableOpts(x, TOP + 0.45, [1.05, 1.3, 0.95, 0.72, 0.71], 0.42));
  text(s, "Green cell: parsed count equals the official numbering. Checked by tests/test_corpus.py on every run.", { x, y: TOP + 3.2, w, h: 0.6, fontSize: 12, color: PALETTE.slate });
  text(s, sec.note, { x: MX, y: 6.5, w: CW, h: 0.3, fontSize: 12, italic: true, color: PALETTE.slate });
}

// ================================================================= 13. Chunk-length finding
{
  const sec = content.chunk_finding;
  const s = contentSlide("Findings", "Findings: data", sec);
  const labels = histKeys.map((k) => k.replace(/[–—]/g, "-"));
  const values = histKeys.map((k) => hist[k]);
  s.addChart(pres.charts.BAR, [{ name: "Chunks", labels, values }], {
    x: MX, y: TOP, w: 6.6, h: 4.55, barDir: "col",
    chartColors: values.map((_, i) => (i === values.length - 1 ? PALETTE.gold : "4F6D99")),
    showTitle: true, title: "Chunk length in words (window cap: 150)", titleFontSize: 14, titleColor: PALETTE.ink, titleFontFace: "+mn-lt",
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: PALETTE.ink2, dataLabelFontSize: 11, dataLabelFontFace: "+mn-lt",
    showLegend: false, catAxisLabelColor: PALETTE.ink2, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt",
    valAxisLabelColor: PALETTE.slate, valAxisLabelFontSize: 11, valAxisLabelFontFace: "+mn-lt",
    valGridLine: { color: "E3E7EE", size: 0.75 }, catGridLine: { style: "none" }, barGapWidthPct: 40,
    showCatAxisTitle: true, catAxisTitle: "Words per chunk", catAxisTitleFontSize: 12, catAxisTitleColor: PALETTE.slate,
    objectName: oid("chart-lengths"),
  });
  const pl = corpus.per_lang || {};
  const en = pl.en || {}, fr = pl.fr || {};
  const stats = [
    [TOKENS.cap_pct, "of chunks sit at 126 to 150 words, the window cap"],
    [TOKENS.windowed_pct, `are windows of ${TOKENS.split_paragraphs} long paragraphs (${TOKENS.windowed} chunks)`],
    [`${fr.median_words || "?"} vs ${en.median_words || "?"}`, `median words, French vs English (${fmt(fr.chunks || 0)} vs ${fmt(en.chunks || 0)} chunks)`],
  ];
  const x = 7.6, w = W - MX - x, sh = 0.66;
  stats.forEach(([v, l], i) => {
    const sy = TOP + i * (sh + 0.14);
    box(s, { x, y: sy, w, h: sh });
    text(s, v, { x: x + 0.2, y: sy, w: 1.45, h: sh, fontFace: FONTS.head, fontSize: 24, bold: true, valign: "middle", color: i === 0 ? PALETTE.kicker : PALETTE.ink });
    text(s, l, { x: x + 1.75, y: sy, w: w - 1.9, h: sh, fontSize: 14, valign: "middle", color: PALETTE.ink2 });
  });
  text(s, "So what", { x, y: 4.6, w, h: 0.34, fontSize: 16, bold: true });
  text(s, sec.implications.map((t, i, a) => ({ text: fill(t), options: { bullet: true, breakLine: i < a.length - 1 } })), { x, y: 4.98, w, h: 1.8, fontSize: 14, color: PALETTE.ink2, paraSpaceAfter: 6 });
}

// ================================================================= 14. Edge cases
{
  const sec = content.edge_cases;
  const s = contentSlide("Findings", "Findings: engineering", sec);
  const cols = 3, gap = 0.25, w = (CW - gap * (cols - 1)) / cols, h = 1.78;
  sec.items.forEach((it, i) => {
    const x = MX + (i % cols) * (w + gap), y = TOP + Math.floor(i / cols) * (h + 0.22);
    box(s, { x, y, w, h });
    numberBadge(s, i + 1, x + 0.22, y + 0.22, 0.42);
    text(s, it.case, { x: x + 0.82, y: y + 0.2, w: w - 1.0, h: 0.85, fontSize: 14, bold: true });
    text(s, [{ text: "Fix: ", options: { bold: true } }, { text: fill(it.fix) }], { x: x + 0.82, y: y + 1.1, w: w - 1.0, h: 0.55, fontSize: 14, color: PALETTE.tealDark });
  });
  box(s, { x: MX, y: 6.12, w: CW, h: 0.62, fill: PALETTE.ink });
  iconCircle(s, "check", MX + 0.2, 6.2, 0.46, PALETTE.teal);
  text(s, sec.lesson, { x: MX + 0.85, y: 6.12, w: CW - 1.1, h: 0.62, fontSize: 15, color: PALETTE.white, valign: "middle" });
}

// ================================================================= 15. Decisions and review
{
  const sec = content.decisions;
  const s = contentSlide("Findings", "Findings: decisions", sec);
  const lw = 5.3;
  text(s, "Decision records (docs/decisions)", { x: MX, y: TOP, w: lw, h: 0.34, fontSize: 16, bold: true });
  const adrs = facts.decisions || [];
  const clean = (t) => fill(t).replace(/`/g, "");
  const cardH = 2.75;
  box(s, { x: MX, y: TOP + 0.45, w: lw, h: cardH });
  if (adrs.length === 1) {
    const a = adrs[0];
    iconCircle(s, "target", MX + 0.25, TOP + 0.65, 0.55, PALETTE.ink);
    text(s, `ADR ${a.title}`, { x: MX + 0.95, y: TOP + 0.62, w: lw - 1.15, h: 0.62, fontSize: 15, bold: true });
    text(s, [
      { text: "Chosen: ", options: { bold: true, color: PALETTE.ink } },
      { text: clean(a.chosen), options: { color: PALETTE.ink2, breakLine: true } },
      { text: " ", options: { fontSize: 6, breakLine: true } },
      { text: clean(sec.adr_notes[a.file] || ""), options: { color: PALETTE.ink2 } },
    ], { x: MX + 0.25, y: TOP + 1.38, w: lw - 0.45, h: cardH - 1.05, fontSize: 13 });
  } else {
    adrs.slice(-3).forEach((a, i) => { // the three most recent records
      const y = TOP + 0.6 + i * 0.92;
      text(s, `ADR ${a.title}`, { x: MX + 0.25, y, w: lw - 0.5, h: 0.3, fontSize: 14, bold: true });
      const c = clean(a.chosen);
      text(s, c.length > 120 ? c.slice(0, 117) + "..." : c, { x: MX + 0.25, y: y + 0.3, w: lw - 0.5, h: 0.55, fontSize: 12, color: PALETTE.ink2 });
    });
  }
  if (sec.upcoming && sec.upcoming.length) {
    const uy = TOP + 0.45 + cardH + 0.15;
    text(s, "Decisions due next", { x: MX, y: uy, w: lw, h: 0.3, fontSize: 14, bold: true, color: PALETTE.ink });
    sec.upcoming.slice(0, 3).forEach((u, i) => {
      const y = uy + 0.34 + i * 0.3;
      text(s, u.name, { x: MX, y, w: lw - 1.0, h: 0.3, fontSize: 13, color: PALETTE.ink2, valign: "middle" });
      text(s, u.when, { x: MX + lw - 1.0, y, w: 1.0, h: 0.3, fontSize: 12, color: PALETTE.slate, align: "right", valign: "middle" });
    });
  }
  const rx = MX + lw + 0.45, rw = W - MX - rx;
  const done = sec.review.filter((r) => ["fixed", "done"].includes(r.status)).length;
  text(s, `Reference-code review: ${done} of ${sec.review.length} fixed`, { x: rx, y: TOP, w: rw, h: 0.34, fontSize: 16, bold: true });
  const rh = 0.415;
  sec.review.forEach((r, i) => {
    const y = TOP + 0.45 + i * rh;
    if (i % 2 === 0) s.addShape(pres.shapes.RECTANGLE, { x: rx, y, w: rw, h: rh, fill: { color: "F7F8FB" }, line: { type: "none" }, objectName: oid("band") });
    text(s, r.id, { x: rx + 0.1, y, w: 0.55, h: rh, fontSize: 13, bold: true, valign: "middle" });
    text(s, r.text, { x: rx + 0.68, y, w: rw - 2.95, h: rh, fontSize: 13, valign: "middle", color: PALETTE.ink2 });
    text(s, r.when, { x: rx + rw - 2.22, y, w: 1.1, h: rh, fontSize: 12, valign: "middle", color: PALETTE.slate });
    statusChip(s, r.status, rx + rw - 1.05, y + (rh - 0.27) / 2, 0.98, { h: 0.27, fontSize: 11 });
  });
}

// ================================================================= 16. Risks
pres.addSection({ title: "Risks and next steps" });
{
  const sec = content.risks;
  const s = contentSlide("Risks and next steps", "Risks and next steps", sec);
  const cols = 3, gap = 0.25, w = (CW - gap * (cols - 1)) / cols, h = 2.25;
  const tone = { high: "coral", medium: "gold", low: "gray" };
  sec.items.forEach((r, i) => {
    const x = MX + (i % cols) * (w + gap), y = TOP + Math.floor(i / cols) * (h + 0.22);
    box(s, { x, y, w, h });
    text(s, r.head, { x: x + 0.22, y: y + 0.18, w: w - 1.45, h: 0.34, fontSize: 15, bold: true });
    chip(s, r.level[0].toUpperCase() + r.level.slice(1), x + w - 1.12, y + 0.2, 0.9, tone[r.level] || "gray", { h: 0.28 });
    text(s, r.text, { x: x + 0.22, y: y + 0.58, w: w - 0.4, h: 0.9, fontSize: 13, color: PALETTE.ink2 });
    text(s, [{ text: "Mitigation: ", options: { bold: true } }, { text: fill(r.mitigation) }], { x: x + 0.22, y: y + 1.48, w: w - 0.4, h: 0.7, fontSize: 13, color: PALETTE.tealDark });
  });
}

// ================================================================= 17. Next steps
{
  const sec = content.next_steps;
  const s = contentSlide("Risks and next steps", "Risks and next steps", sec);
  const colW = [0.55, 4.2, 5.68, 1.7];
  const rows = [[th("#"), th("Task"), th("Done when"), th("Status", { align: "center" })]];
  sec.items.forEach((it, i) => rows.push([td(String(i + 1), { bold: true, align: "center" }), td(it.task, { bold: true }), td(it.done_when, { color: PALETTE.ink2 }), tdStatus(it.status || "planned")]));
  s.addTable(rows, tableOpts(MX, TOP, colW, [0.42, ...sec.items.map(() => 0.5)]));
  box(s, { x: MX, y: 5.85, w: CW, h: 0.9, fill: PALETTE.goldSoft });
  iconCircle(s, "flask", MX + 0.22, 5.99, 0.62, PALETTE.ink);
  text(s, sec.decision, { x: MX + 1.05, y: 5.85, w: CW - 1.3, h: 0.9, fontSize: 15, valign: "middle", color: PALETTE.ink });
}

// ================================================================= 18. Iteration log
pres.addSection({ title: "Appendix" });
{
  const sec = content.iteration_log;
  const s = contentSlide("Appendix", "Appendix", sec);
  const colW = [0.9, 1.35, 2.2, 3.3];
  const recent = sec.entries.slice(-3).reverse(); // newest first; the full history stays in content.json
  const rows = [[th("#", { align: "center" }), th("Date"), th("Trigger"), th("What changed")]];
  recent.forEach((e) => rows.push([td(String(e.iteration), { align: "center", bold: true }), td(e.date, { fontSize: 13 }), td(e.trigger, { fontSize: 13 }), td(e.changes, { fontSize: 13, color: PALETTE.ink2 })]));
  s.addTable(rows, tableOpts(MX, TOP, colW, [0.42, ...recent.map(() => 0.62)]));
  if (sec.triggers) {
    const ty = 4.55, tw = colW.reduce((a, b) => a + b, 0);
    text(s, "Rebuild the deck when", { x: MX, y: ty, w: tw, h: 0.34, fontSize: 16, bold: true });
    sec.triggers.forEach((t, i) => {
      const cx = MX + (i % 2) * (tw / 2), cy = ty + 0.45 + Math.floor(i / 2) * 0.5;
      iconCircle(s, "check", cx, cy + 0.02, 0.32, PALETTE.teal);
      text(s, t, { x: cx + 0.45, y: cy, w: tw / 2 - 0.55, h: 0.36, fontSize: 14, valign: "middle", color: PALETTE.ink2 });
    });
  }
  const x = 8.65, w = W - MX - x;
  box(s, { x, y: TOP, w, h: 3.85, fill: PALETTE.mist });
  text(s, "How to update this deck", { x: x + 0.25, y: TOP + 0.18, w: w - 0.5, h: 0.34, fontSize: 16, bold: true });
  sec.how_to.forEach((t, i) => {
    const y = TOP + 0.72 + i * 1.0;
    numberBadge(s, i + 1, x + 0.25, y, 0.4);
    text(s, t, { x: x + 0.8, y: y - 0.02, w: w - 1.0, h: 0.9, fontSize: 14, color: PALETTE.ink2 });
  });
  const g = facts.git || {};
  const src = [
    `Facts collected ${String(facts.generated_at || "never").replace("T", " ").replace("+00:00", " UTC")}`,
    g.commit ? `at commit ${g.commit} (${g.date}, ${g.count} commits): ${g.subject}` : "",
  ].filter(Boolean).join(" ");
  text(s, src, { x: MX, y: 6.35, w: CW, h: 0.4, fontSize: 12, italic: true, color: PALETTE.slate });
}

// ---------------------------------------------------------------- write, then give the deck its theme colours
(async () => {
  await pres.writeFile({ fileName: OUT });
  await writeTheme(OUT);
  console.log(`wrote ${path.relative(process.cwd(), OUT)} (iteration ${meta.iteration}, ${pres.slides.length} slides)`);
})().catch((e) => { console.error(e); process.exit(1); });
