// Hilfswerkzeug: Top-Level-Einheiten (Funktionen, const/let/var) des Haupt-Skripts per AST analysieren und entfernen.
// Aufruf: node ast_tool.mjs <html> refs a,b,c      -> Verweise auf die Namen
//         node ast_tool.mjs <html> remove a,b,c    -> schreibt <html> neu ohne diese Top-Level-Einheiten (nur wenn sie als ganze Einheit existieren)
//         node ast_tool.mjs <html> orphans         -> Top-Level-Einheiten, auf die nichts (ausser sie selbst) verweist
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire('C:/Users/tknec/AppData/Local/Temp/claude/e8d0e7e0a92221a7/9d2819f3-b01d-426e-b2d9-daba34a7aa43/scratchpad/acorn/');
const acorn = require('acorn'); const walk = require('acorn-walk');
const [,, file, cmd, arg] = process.argv;
const html = fs.readFileSync(file, 'utf8');
const m = /<script(?![^>]*src)[^>]*>/.exec(html);
const sStart = m.index + m[0].length, sEnd = html.indexOf('</script>', sStart);
const js = html.slice(sStart, sEnd);
const ast = acorn.parse(js, { ecmaVersion: 2022, sourceType: 'script', allowReturnOutsideFunction: true });
const lineOf = (off) => html.slice(0, sStart + off).split('\n').length;
const units = [];   // {names, start, end, kind}
for (const node of ast.body) {
  if (node.type === 'FunctionDeclaration') units.push({ names: [node.id.name], start: node.start, end: node.end, kind: 'function', node });
  else if (node.type === 'VariableDeclaration') units.push({ names: node.declarations.map(d => d.id.name).filter(Boolean), start: node.start, end: node.end, kind: node.kind, node });
  else units.push({ names: [], start: node.start, end: node.end, kind: 'stmt:' + node.type, node });
}
// Identifier-Vorkommen je Einheit
function idents(node) {
  const s = new Map();
  walk.full(node, (n) => { if (n.type === 'Identifier') { s.set(n.name, (s.get(n.name) || 0) + 1); } });
  return s;
}
const uIdents = units.map(u => idents(u.node));
const htmlRest = html.slice(0, sStart) + html.slice(sEnd);
const inHtml = (name) => (htmlRest.match(new RegExp('(?<![A-Za-z0-9_$])' + name.replace(/\$/g, '\\$') + '(?![A-Za-z0-9_$])', 'g')) || []).length;
if (cmd === 'refs') {
  for (const name of arg.split(',')) {
    const di = units.findIndex(u => u.names.includes(name));
    const out = { name, def: di < 0 ? null : { line: lineOf(units[di].start), lines: lineOf(units[di].end) - lineOf(units[di].start) + 1, kind: units[di].kind }, htmlRefs: inHtml(name), usedBy: [] };
    units.forEach((u, i) => { if (i !== di && uIdents[i].has(name)) out.usedBy.push((u.names[0] || u.kind) + '@' + lineOf(u.start) + (u.kind === 'function' ? '' : '[' + u.kind + ']')); });
    console.log(JSON.stringify(out));
  }
} else if (cmd === 'orphans') {
  const res = [];
  units.forEach((u, i) => u.names.forEach(name => {
    if (u.kind === 'stmt') return;
    let used = inHtml(name) > 0;
    units.forEach((v, j) => { if (j !== i && uIdents[j].has(name)) used = true; });
    // Selbstverweise (Rekursion) zaehlen nicht; Verweise in Zeichenketten (onclick="x()") sind in htmlRest/JS-Strings -> zusaetzlich Textsuche in Strings
    if (!used) {
      const textHits = (js.match(new RegExp('(?<![A-Za-z0-9_$])' + name.replace(/\$/g, '\\$') + '(?![A-Za-z0-9_$])', 'g')) || []).length;
      const own = uIdents[i].get(name) || 0;
      res.push({ name, kind: u.kind, line: lineOf(u.start), lines: lineOf(u.end) - lineOf(u.start) + 1, textHits, ownIdents: own });
    }
  }));
  console.log(JSON.stringify(res));
} else if (cmd === 'remove') {
  const names = new Set(arg.split(','));
  const cuts = [];
  for (const u of units) {
    if (!u.names.length) continue;
    const hit = u.names.filter(n => names.has(n));
    if (!hit.length) continue;
    if (hit.length !== u.names.length) { console.error('Teilweise Deklaration, nicht entfernt: ' + u.names.join(',')); continue; }
    cuts.push([u.start, u.end]);
  }
  const found = new Set(units.flatMap(u => u.names));
  const missing = [...names].filter(n => !found.has(n));
  if (missing.length) console.error('Nicht gefunden: ' + missing.join(','));
  // Alle Schnitte auf dem ORIGINALTEXT berechnen (keine Wechselwirkung), danach zusammenführen und von hinten anwenden
  const rngs = [];
  for (const [a0, b0] of cuts) {
    let start = a0, end = b0;
    const NL = String.fromCharCode(10), TAB = String.fromCharCode(9);
    const lineStart = js.lastIndexOf(NL, start - 1) + 1;
    const startsLine = /^[ \t]*$/.test(js.slice(lineStart, start));
    let q = end; while (js[q] === ' ' || js[q] === TAB) q++;
    const restBlank = js[q] === NL || q >= js.length;
    if (startsLine && restBlank) {
      end = q < js.length ? q + 1 : q; start = lineStart;
      // direkt davor stehende Kommentarzeilen (aber keine Abschnitts-Banner) mitnehmen
      let ls = start;
      while (ls > 0) {
        const prevEnd = ls - 1, prevStart = js.lastIndexOf(String.fromCharCode(10), prevEnd - 1) + 1;
        const line = js.slice(prevStart, prevEnd);
        if (/^\s*\/\/(?!\s*[═─=-]{3})/.test(line)) { ls = prevStart; start = prevStart; } else break;
      }
    }
    rngs.push([start, end]);
  }
  rngs.sort((x, y) => x[0] - y[0]);
  const merged = [];
  for (const r of rngs) { const l = merged[merged.length - 1]; if (l && r[0] <= l[1]) l[1] = Math.max(l[1], r[1]); else merged.push([...r]); }
  let out = js, removedChars = 0;
  for (const [a1, b1] of merged.sort((x, y) => y[0] - x[0])) { removedChars += b1 - a1; out = out.slice(0, a1) + out.slice(b1); }
  fs.writeFileSync(file, html.slice(0, sStart) + out + html.slice(sEnd), 'utf8');
  console.log(JSON.stringify({ removedUnits: cuts.length, removedChars }));
}
