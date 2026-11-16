# Changelog

## 1.110 — 2026-11-16 (release v1.1.0)

Sharper on screen, an OpenType/CFF version, and cleaner joins. The font's own version string is 1.110. Advances, metrics and coverage are unchanged.

- The `.ttf` and `.woff2` are now hinted with ttfautohint (strong stem snapping in grayscale, GDI and DirectWrite modes) and their gasp table allows grid-fitting. Before, they were unhinted, which made small sizes look soft
- New `.otf` files for both weights: the same outlines as CFF, with PostScript hints from otfautohint; alignment zones and standard stems are measured from the font's own ink
- Redrawn where strokes did not meet or crowded each other: 2 and ? (the bowl now runs straight into the diagonal or stem), 5 (upright stem, smooth shoulder, open tail so it cannot read as 6), & (rebuilt: closed loop, leg to the baseline, open bowl), @ (smaller inner a, tail joins the ring), 3 and G (strokes meet exactly), e (the bowl starts at the end of the bar), and the straight double quote; ² ³ ½ ¿ are built from those glyphs and follow them (marks further apart)
- `build.py` needs `ttfautohint-py` and `afdko` in addition to the previous packages

## 1.101 — 2026-11-15

The font's own version string is 1.101. The outlines and advances are the same as in 1.100; only the vertical metrics change.

- Line spacing goes back to the 1.000 values: hhea and typo ascent 1038, descent -329, line gap 0, with USE_TYPO_METRICS set. Lines set in AhmiPrint are as tall as in 1.000 again. Marks over capitals may rise above the ascent, as in most fonts
- usWinAscent 1152 and usWinDescent 349 cover every glyph, so Windows never clips the marks over capitals or the commas below
- `check.py` checks that the hhea and typo metrics equal the 1.000 values in both weights and that the usWin metrics cover every glyph, instead of requiring every glyph inside the line box

## 1.100 — 2026-11-15

The font's own version string is 1.100.

- 584 characters in each weight, up from 96: Latin-1 Supplement and Latin Extended-A in full, Ș ș Ț ț and ƒ, the spacing accents, Greek (monotonic), Cyrillic (U+0400 to U+045F and the Kazakh letters), general punctuation, currency signs, ™ №, arrows, maths signs and the interface shapes
- Figure, punctuation, thin, hair and narrow no-break spaces; U+00A0 is now its own empty glyph of the space's width
- Accented letters are composed from a base letter and a mark drawn once. The stroke file gains `use <code> [dx,dy] [sx,sy]` for this, hexadecimal codes (`U+00C0`), and filled shapes `E` (ellipse) and `P` (polygon)
- Superior figures and fractions are tabular among themselves, as are the figures, figure space and figure dash
- The line box grows for the marks over capitals and the commas below: ascent 1152 (was 1038), descent 349 (was 329)
- Fixed: a contour that came out of the curve conversion with only off-curve points was dropped, which filled small counters such as the two rings of % in Bold
- `check.py` checks every character of the target set in both weights, an outline on every non-space glyph, the widths of the spaces, tabular figures, and that no glyph leaves the line box

## 1.0.0 — 2026-11-15

First release. The font's own version string is 1.000.

- Regular and Bold, each as TrueType (`.ttf`) and WOFF2 (`.woff2`)
- 95 characters drawn from the stroke source: Basic Latin, U+0020 through U+007E
- U+00A0 no-break space uses the space glyph
- Tabular figures and a slashed zero
- `check.py` checks advances, closed counters, tabular figures, and that both weights share one set of vertical metrics
