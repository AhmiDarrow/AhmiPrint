# Changelog

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
