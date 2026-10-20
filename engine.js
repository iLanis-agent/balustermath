// Baluster Math engine: how many balusters an opening takes for a gap you choose, where their centres sit, and how many packs a run of openings needs. Exact integers (mm), results rounded half up to 0.1 mm.
function _d(t, err, lo, hi) { // cm text with at most one decimal -> whole mm
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,3})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _w(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _OPEN = "the opening must be from 1 to 600 cm with at most one decimal place";
var _WIDTH = "the baluster width must be a whole number of mm from 5 to 100";
var _GAP = "the largest gap must be a whole number of mm from 20 to 300";
var _OPENINGS = "the number of openings must be a whole number from 1 to 50";
var _PACK = "the pack size must be a whole number from 1 to 100";
var _FILL = "the balusters would fill the whole opening, leaving no gap";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _mm(v) { // tenths of a mm -> text
  var s = String(Math.floor(v / 10)), f = v % 10;
  return f ? s + "." + f : s;
}
function _bal(n) { return n + (n === 1 ? " baluster" : " balusters"); }
function _in(open, width, gap) {
  var o = _d(open, _OPEN, 10, 6000), w = _w(width, _WIDTH, 5, 100), g = _w(gap, _GAP, 20, 300);
  var n = o <= g ? 0 : Math.ceil((o - g) / (w + g));
  if (o - n * w <= 0) throw new Error(_FILL);
  return { o: o, w: w, g: g, n: n };
}

function countTruth(open, width, gap) {
  var p = _in(open, width, gap), k = p.n + 1;
  return "In a " + _mm(p.o) + " cm opening, balusters " + p.w + " mm wide with a gap of at most " + p.g + " mm take " + _bal(p.n) + ", leaving " + (k === 1 ? "1 gap" : k + " equal gaps") + " of " + _mm(_hu(10 * (p.o - p.n * p.w), k)) + " mm.";
}
function centresTruth(open, width, gap) {
  var p = _in(open, width, gap), k = p.n + 1;
  if (p.n === 0) return "With no balusters there are no centres to set out.";
  var edge = _mm(_hu(10 * (2 * p.o - (p.n - 1) * p.w), 2 * k));
  if (p.n === 1) return "The one baluster's centre sits " + edge + " mm from each post.";
  return "Centres sit " + _mm(_hu(10 * (p.o + p.w), k)) + " mm apart, with the first centre " + edge + " mm from one post and the last " + edge + " mm from the other.";
}
function packsTruth(open, width, gap, openings, pack) {
  var p = _in(open, width, gap), r = _w(openings, _OPENINGS, 1, 50), s = _w(pack, _PACK, 1, 100);
  var t = p.n * r, k = Math.floor((t + s - 1) / s), left = k * s - t;
  return r + (r === 1 ? " opening" : " openings") + " of " + _bal(p.n) + (r === 1 ? " needs " : " need ") + _bal(t) + ", which is " + k + (k === 1 ? " pack" : " packs") + " of " + s + ", with " + (left === 0 ? "none" : left) + " left over.";
}
