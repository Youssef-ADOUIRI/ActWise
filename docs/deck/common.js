// Shared style and drawing helpers for the ActWise decks (review deck and pipeline deck).
// Restyle every deck in one place: PALETTE and FONTS. Units are inches on a 16:9 wide slide.
"use strict";

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;

const PALETTE = {
  ink: "13203A", ink2: "2B3A55", slate: "5B6B82", line: "D5DBE5",
  mist: "EEF1F6", white: "FFFFFF", kicker: "9A6A0B",
  gold: "E3A21A", goldSoft: "FBEFD3",
  teal: "14917F", tealDark: "0F7A6B", tealSoft: "DDF1EE",
  coral: "D6573B", coralSoft: "F9E3DD",
  gray: "D9DEE6", graySoft: "F1F3F7",
  blue: "4F6D99", blueSoft: "E4EAF3",
  navy2: "1F2E4D", navyLine: "3A4B6B", onDark: "CBD3E1", onDark2: "AEB9CC",
  series: ["13203A", "4F6D99", "B7861A"],
};
const FONTS = { head: "Cambria", body: "Calibri", mono: "Courier New" };
const THEME = {
  name: "ActWise",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: PALETTE.ink, lt2: PALETTE.mist,
    accent1: PALETTE.ink, accent2: PALETTE.gold, accent3: PALETTE.teal, accent4: PALETTE.coral,
    accent5: PALETTE.blue, accent6: PALETTE.slate, hlink: "1F5FA8", folHlink: "6B4E9B",
  },
};

const W = 13.333, MX = 0.6, CW = W - 2 * MX; // slide width, side margin, content width
const TOP = 2.1; // content starts below kicker, title and takeaway

// Status vocabulary -> chip colours and labels.
const STATUS = {
  done: ["teal", "Done"], met: ["teal", "Met"], fixed: ["teal", "Fixed"], built: ["teal", "Built"],
  supported: ["teal", "Supported"], mitigated: ["teal", "Mitigated"],
  in_progress: ["gold", "In progress"], partial: ["gold", "Partial"], watch: ["gold", "Watch"],
  planned: ["gray", "Planned"], not_measured: ["gray", "Not measured"], untested: ["gray", "Untested"],
  open: ["gray", "Open"],
  not_met: ["coral", "Not met"], rejected: ["coral", "Rejected"], blocked: ["coral", "Blocked"],
};
const CHIP = {
  teal: { fill: PALETTE.teal, text: PALETTE.white, soft: PALETTE.tealSoft },
  gold: { fill: PALETTE.gold, text: PALETTE.ink, soft: PALETTE.goldSoft },
  gray: { fill: PALETTE.gray, text: PALETTE.ink2, soft: PALETTE.graySoft },
  coral: { fill: PALETTE.coral, text: PALETTE.white, soft: PALETTE.coralSoft },
};
const status = (s) => {
  const [tone, label] = STATUS[s] || ["gray", String(s || "Planned")];
  return { tone, label, ...CHIP[tone] };
};
const isBuilt = (s) => ["done", "built", "met", "fixed"].includes(s);

const readJson = (name, fallback = {}) => {
  const file = path.join(HERE, name);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : fallback;
};

// A presentation with the two shared layouts: TITLE_DARK and CONTENT.
function createDeck({ title, subject, author, footer }) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.theme = { headFontFace: FONTS.head, bodyFontFace: FONTS.body };
  pres.author = author;
  pres.title = title;
  pres.subject = subject;

  pres.defineSlideMaster({
    title: "TITLE_DARK",
    background: { color: PALETTE.ink },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 7.6, h: 1.3, fontFace: FONTS.head, fontSize: 60, bold: true, color: PALETTE.white, align: "left", valign: "bottom", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "subtitle", type: "body", x: 0.8, y: 3.45, w: 7.4, h: 1.0, fontSize: 24, color: PALETTE.onDark, align: "left", valign: "top", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "meta", type: "body", x: 0.8, y: 5.55, w: 7.4, h: 1.0, fontSize: 14, color: PALETTE.onDark2, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
  });

  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: PALETTE.white },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.42, w: 8.5, h: 0.3, fontSize: 12, bold: true, color: PALETTE.kicker, align: "left", valign: "top", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.72, w: CW, h: 0.68, fontFace: FONTS.head, fontSize: 34, bold: true, color: PALETTE.ink, align: "left", valign: "top", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "takeaway", type: "body", x: MX, y: 1.42, w: CW, h: 0.45, fontSize: 16, color: PALETTE.slate, align: "left", valign: "top", margin: 0 }, text: "" } },
      { text: { text: footer, options: { x: MX, y: 7.02, w: 9, h: 0.3, fontSize: 10, color: PALETTE.slate, margin: 0, valign: "middle" } } },
    ],
    slideNumber: { x: 12.13, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: PALETTE.slate, align: "right" },
  });
  return pres;
}

// Drawing helpers bound to one presentation. `fill` post-processes every string (tokens, dashes).
function helpers(pres, fill = (s) => String(s == null ? "" : s)) {
  let objCount = 0;
  const oid = (p) => `${p}-${++objCount}`;

  function text(slide, t, o) {
    slide.addText(typeof t === "string" ? fill(t) : t, { isTextBox: true, margin: 0, valign: "top", color: PALETTE.ink, fontSize: 14, objectName: oid("text"), ...o });
  }
  function box(slide, o) {
    const { x, y, w, h, fill: f = PALETTE.mist, line, radius = 0.08, dash, lineWidth = 1 } = o;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h, rectRadius: radius, fill: { color: f },
      line: line ? { color: line, width: lineWidth, dashType: dash || "solid" } : { type: "none" },
      objectName: oid("box"),
    });
  }
  function chip(slide, label, x, y, w, tone, o = {}) {
    const c = CHIP[tone] || CHIP.gray;
    slide.addText(fill(label), {
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x, y, w, h: o.h || 0.3,
      fill: { color: c.fill }, color: c.text, fontSize: o.fontSize || 11, bold: true,
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: oid("chip"),
    });
  }
  function statusChip(slide, s, x, y, w, o) {
    const st = status(s);
    chip(slide, st.label, x, y, w, st.tone, o);
  }
  function iconCircle(slide, name, x, y, d, fillColor, variant = "white") {
    slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fillColor }, line: { type: "none" }, objectName: oid("icon-bg") });
    const file = path.join(HERE, "assets", "icons", `${name}-${variant}.png`);
    if (fs.existsSync(file)) {
      const pad = d * 0.24;
      slide.addImage({ path: file, x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, altText: `${name} icon`, objectName: oid("icon") });
    }
  }
  function numberBadge(slide, n, x, y, d, o = {}) {
    slide.addText(String(n), {
      shape: pres.shapes.OVAL, x, y, w: d, h: d, fill: { color: o.fill || PALETTE.gold }, color: o.color || PALETTE.ink,
      fontFace: FONTS.head, fontSize: o.fontSize || Math.round(d * 34), bold: true, align: "center", valign: "middle",
      margin: 0, isTextBox: true, objectName: oid("badge"),
    });
  }
  function line(slide, x, y, w, h, color = PALETTE.line, width = 1.25, o = {}) {
    slide.addShape(pres.shapes.LINE, { x, y, w, h, line: { color, width, dashType: o.dash || "solid" }, objectName: oid("line") });
  }
  // Straight connector from (x1, y1) to (x2, y2) with an arrowhead at the end.
  function arrow(slide, x1, y1, x2, y2, o = {}) {
    slide.addShape(pres.shapes.LINE, {
      x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
      flipH: x2 < x1, flipV: y2 < y1,
      line: { color: o.color || PALETTE.slate, width: o.width || 1.5, dashType: o.dash || "solid", endArrowType: o.head === false ? undefined : "triangle", beginArrowType: o.both ? "triangle" : undefined },
      objectName: oid("arrow"),
    });
  }
  // Elbow connector: horizontal then vertical (or vertical then horizontal with o.vFirst).
  function elbow(slide, x1, y1, x2, y2, o = {}) {
    if (o.vFirst) {
      arrow(slide, x1, y1, x1, y2, { ...o, head: false });
      arrow(slide, x1, y2, x2, y2, o);
    } else {
      arrow(slide, x1, y1, x2, y1, { ...o, head: false });
      arrow(slide, x2, y1, x2, y2, o);
    }
  }
  function contentSlide(section, kicker, sec) {
    const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
    slide.addText(fill(kicker).toUpperCase(), { placeholder: "kicker" });
    slide.addText(fill(sec.title), { placeholder: "title" });
    slide.addText(fill(sec.takeaway || ""), { placeholder: "takeaway" });
    if (sec.notes) slide.addNotes(fill(sec.notes));
    return slide;
  }
  // Table helpers: header row in ink, body rows with light rules.
  const th = (t, o = {}) => ({ text: fill(t), options: { bold: true, color: PALETTE.white, fill: { color: PALETTE.ink }, fontSize: 13, valign: "middle", ...o } });
  const td = (t, o = {}) => ({ text: fill(t), options: { color: PALETTE.ink, fontSize: 14, valign: "middle", ...o } });
  const tdStatus = (s) => {
    const st = status(s);
    return td(st.label, { bold: true, color: st.tone === "teal" || st.tone === "coral" ? (st.tone === "teal" ? PALETTE.tealDark : PALETTE.coral) : PALETTE.ink2, fill: { color: st.soft }, align: "center", fontSize: 13 });
  };
  const pending = () => td("pending", { color: "9AA5B5", italic: true, fontSize: 13, align: "center" });
  const tableOpts = (x, y, colW, rowH) => ({
    x, y, w: colW.reduce((a, b) => a + b, 0), colW, rowH,
    border: { type: "solid", color: PALETTE.line, pt: 0.75 }, margin: [0.04, 0.1, 0.04, 0.1],
    fontFace: FONTS.body, objectName: oid("table"),
  });

  return { oid, text, box, chip, statusChip, iconCircle, numberBadge, line, arrow, elbow, contentSlide, th, td, tdStatus, pending, tableOpts };
}

// pptxgenjs writes Office's stock palette into the theme; replace it with ours after writeFile().
async function writeTheme(file, theme = THEME) {
  const JSZip = require(require.resolve("jszip", { paths: [path.dirname(require.resolve("pptxgenjs"))] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const part = "ppt/theme/theme1.xml";
  const slots = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];
  const scheme = `<a:clrScheme name="${theme.name}">` + slots.map((k) => `<a:${k}><a:srgbClr val="${theme.colors[k]}"/></a:${k}>`).join("") + "</a:clrScheme>";
  const xml = (await zip.file(part).async("string"))
    .replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => scheme)
    .replace(/(<a:(?:theme|fontScheme)\b[^>]*?\bname=")[^"]*"/g, (_, head) => `${head}${theme.name}"`);
  zip.file(part, xml);
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

module.exports = { PALETTE, FONTS, THEME, W, MX, CW, TOP, STATUS, CHIP, status, isBuilt, readJson, createDeck, helpers, writeTheme, HERE };
