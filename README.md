# Baluster Math

Baluster spacing arithmetic. In a 180 cm opening, balusters 40 mm wide with a gap of at most 100 mm take 13 balusters, leaving 14 equal gaps of 91.4 mm.

## What it computes

- **The count truth** - balusters between two posts (opening 1 to 600 cm) for the largest gap you choose (20 to 300 mm) and a baluster width (5 to 100 mm), spaced evenly, with the equal gap that results.
- **The centres truth** - the centre to centre distance and the distance from each post to the nearest centre.
- **The packs truth** - the balusters and whole packs (1 to 100 per pack) for 1 to 50 identical openings.

## Boundary

Arithmetic only. The opening, width, largest gap and pack size are the owner's own entries. It has not seen any stair, deck or balcony and does not know any code, height, load or fixing, and it gives no verdict that a layout is compliant, adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on mm, half-up rounding to 0.1 mm).
- `oracle.py` - the Python mirror (Fractions, balusters added one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/balustermath/
Repo: https://github.com/iLanis-agent/balustermath
