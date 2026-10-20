#!/usr/bin/env python3
# Baluster Math oracle - mirrors engine.js with Fractions: balusters are added one at a time until the equal gap is no larger than the chosen gap, centres are placed by walking along the opening, packs are bought one at a time, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

OPEN = "the opening must be from 1 to 600 cm with at most one decimal place"
WIDTH = "the baluster width must be a whole number of mm from 5 to 100"
GAP = "the largest gap must be a whole number of mm from 20 to 300"
OPENINGS = "the number of openings must be a whole number from 1 to 50"
PACK = "the pack size must be a whole number from 1 to 100"
FILL = "the balusters would fill the whole opening, leaving no gap"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}(\.[0-9])?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t) * 10          # mm
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def txt(fr):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * 10).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10)
    return f"{ip}.{fp}" if fp else str(ip)
def bal(n): return f"{n} baluster" + ("" if n == 1 else "s")
def inputs(o, w, g):
    O = dec(o, OPEN, "1", "600"); W = whole(w, WIDTH, 5, 100); G = whole(g, GAP, 20, 300)
    n = 0
    while (O - n * W) / (n + 1) > G:
        n += 1
        if O - n * W <= 0: break
    if O - n * W <= 0: raise ValueError(FILL)
    return O, W, G, n

def count(o, w, g):
    O, W, G, n = inputs(o, w, g); gap = (O - n * W) / (n + 1)
    gaps = "1 gap" if n == 0 else f"{n+1} equal gaps"
    return f"In a {txt(O/10)} cm opening, balusters {W} mm wide with a gap of at most {G} mm take {bal(n)}, leaving {gaps} of {txt(gap)} mm."
def centres(o, w, g):
    O, W, G, n = inputs(o, w, g)
    if n == 0: return "With no balusters there are no centres to set out."
    gap = (O - n * W) / (n + 1)
    pos = []; x = F(0)
    for _ in range(n):
        x += gap; pos.append(x + F(W, 2)); x += W
    edge = pos[0]
    assert O - pos[-1] == edge
    if n == 1: return f"The one baluster's centre sits {txt(edge)} mm from each post."
    return f"Centres sit {txt(pos[1] - pos[0])} mm apart, with the first centre {txt(edge)} mm from one post and the last {txt(O - pos[-1])} mm from the other."
def packs(o, w, g, r, s):
    O, W, G, n = inputs(o, w, g); R = whole(r, OPENINGS, 1, 50); S = whole(s, PACK, 1, 100)
    t = n * R; k = 0
    while k * S < t: k += 1
    left = k * S - t
    return f"{R} opening{'' if R == 1 else 's'} of {bal(n)} {'needs' if R == 1 else 'need'} {bal(t)}, which is {k} pack{'' if k == 1 else 's'} of {S}, with {'none' if left == 0 else left} left over."

FNS = {"countTruth": count, "centresTruth": centres, "packsTruth": packs}
def cases():
    c = []
    opens = ["1", "8", "18.5", "180", "600"]; ws = ["5", "40", "100"]; gs = ["20", "100", "300"]
    for o in opens:
        for w in ws:
            for g in gs:
                c.append(("countTruth", [o, w, g])); c.append(("centresTruth", [o, w, g]))
    for o in ["8", "180", "600"]:
        for w in ["12", "40"]:
            for g in ["100", "300"]:
                for r in ["1", "50"]:
                    for s in ["1", "12"]:
                        c.append(("packsTruth", [o, w, g, r, s]))
    for t in [(" 180 ", " 40 ", " 100 "), ("180.0", "40", "100")]:
        c += [("countTruth", list(t)), ("centresTruth", list(t)), ("packsTruth", list(t) + [" 2 ", " 12 "])]
    bad = ["", "x", "0", "0.0", "0.5", "1.25", "-1", ".5", "5.", "1e2", "1000", "99999"]
    for v in bad:
        c += [("countTruth", [v, "40", "100"]), ("countTruth", ["180", v, "100"]), ("countTruth", ["180", "40", v]),
              ("packsTruth", ["180", "40", "100", v, "12"]), ("packsTruth", ["180", "40", "100", "2", v])]
    for t in [("600.1", "40", "100"), ("0.9", "40", "100"), ("180", "4", "100"), ("180", "101", "100"), ("180", "40", "19"), ("180", "40", "301")]:
        c.append(("countTruth", list(t)))
    for t in [("10", "100", "20"), ("10", "100", "50"), ("20", "50", "20"), ("12", "100", "20")]:
        c += [("countTruth", list(t)), ("centresTruth", list(t))]
    for t in [("180", "40", "100", "51", "12"), ("180", "40", "100", "0", "12"), ("180", "40", "100", "2", "101"), ("180", "40", "100", "2", "0")]:
        c.append(("packsTruth", list(t)))
    r = random.Random(712)
    for _ in range(6):
        o = f"{r.randint(0, 599)}.{r.randint(0, 9)}"; o = "1" if o in ("0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9") else o
        w = str(r.randint(5, 100)); g = str(r.randint(20, 300)); rr = str(r.randint(1, 50)); s = str(r.randint(1, 100))
        c += [("countTruth", [o, w, g]), ("centresTruth", [o, w, g]), ("packsTruth", [o, w, g, rr, s])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
