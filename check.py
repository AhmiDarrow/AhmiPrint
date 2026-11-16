#!/usr/bin/env python3
"""
Check the built AhmiPrint files against source/ahmi-print.strokes.

    python check.py

A missing font is a failure. Build first with build.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

import build

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
STYLES = ("Regular", "Bold")

# These counters are closed circles in the stroke source, so each weight
# keeps a hole. The number is the contour count (outer plus holes).
HOLES = {
    "O": 2,
    "o": 2,
    "zero": 3,  # the slashed zero splits its counter in two
    "Q": 2,
    "eight": 3,
    "degree": 2,
    "ring": 2,
}

# Composed letters whose mark keeps its own hole: (letter, base, extra contours).
MARK_HOLES = [
    ("aring", "a", 2),  # a separate ring: its outline and its hole
    ("uring", "u", 2),
    ("Aring", "A", 1),  # the ring sits on the apex, so only its hole is new
    ("Uring", "U", 2),
]

# Spaces: empty glyphs with these advances (design units).
SPACES = {
    0x0020: 6.5,
    0x00A0: 6.5,
    0x2007: 17.0,  # figure space: one figure
    0x2008: 5.2,   # punctuation space: one period
    0x2009: 4.8,   # thin space: a fifth of an em
    0x200A: 2.4,   # hair space: a tenth of an em
    0x202F: 4.8,   # narrow no-break space
}

# Each group shares one advance, so numbers line up in columns.
TABULAR = {
    "figures": [0x30 + i for i in range(10)] + [0x2007, 0x2012],
    "superior figures": [0xB9, 0xB2, 0xB3],
    "fractions": [0xBC, 0xBD, 0xBE],
}


def target_set() -> set[int]:
    """Every character FreeSpeak needs from each weight (fonts/TARGET.md)."""
    s: set[int] = set()
    s |= set(range(0x20, 0x7F))                      # Basic Latin
    s |= set(range(0xA0, 0x100))                     # Latin-1 Supplement
    s |= set(range(0x100, 0x180))                    # Latin Extended-A
    s |= {0x192, 0x218, 0x219, 0x21A, 0x21B}         # f hook, Romanian comma below
    s |= {0x2C6, 0x2C7} | set(range(0x2D8, 0x2DE))   # spacing modifiers
    s |= {0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015, 0x2018, 0x2019, 0x201A,
          0x201C, 0x201D, 0x201E, 0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2032,
          0x2033, 0x2039, 0x203A, 0x203C, 0x2044}
    s |= set(SPACES)
    s |= {0x20AC, 0x20B9, 0x20BD, 0x20BA, 0x20A9, 0x20AA, 0x20AB, 0x20B1, 0x20B4,
          0x20B8, 0x20BF}                            # currency
    s |= {0x2122, 0x2116}                            # letterlike
    s |= set(range(0x2190, 0x2196)) | {0x21E7}       # arrows
    s |= {0x2212, 0x221E, 0x221A, 0x2248, 0x2260, 0x2264, 0x2265}
    s |= {0x25FB, 0x25B2, 0x25BC, 0x25BA, 0x25C4, 0x2713, 0x2717, 0x25CF, 0x25CB}
    s |= set(range(0x23F4, 0x23F8))
    s |= {0x386, 0x38C} | set(range(0x388, 0x38B)) | set(range(0x38E, 0x3A2))
    s |= set(range(0x3A3, 0x3CF))                    # Greek
    s |= set(range(0x400, 0x460))                    # Cyrillic
    s |= {0x490, 0x491, 0x492, 0x493, 0x49A, 0x49B, 0x4A2, 0x4A3, 0x4AE, 0x4AF,
          0x4B0, 0x4B1, 0x4BA, 0x4BB, 0x4D8, 0x4D9, 0x4E8, 0x4E9}
    return s


class AreaPen(BasePen):
    def __init__(self):
        super().__init__(None)
        self.areas: list[float] = []
        self._pts: list[tuple[float, float]] = []

    def _moveTo(self, pt):
        self._pts = [(pt[0], pt[1])]

    def _lineTo(self, pt):
        self._pts.append((pt[0], pt[1]))

    def _curveToOne(self, _c1, _c2, pt):
        self._pts.append((pt[0], pt[1]))

    def _qCurveToOne(self, _control, pt):
        self._pts.append((pt[0], pt[1]))

    def _closePath(self):
        area = 0.0
        pts = self._pts
        for i, (x1, y1) in enumerate(pts):
            x2, y2 = pts[(i + 1) % len(pts)]
            area += x1 * y2 - x2 * y1
        self.areas.append(area / 2.0)

    def _endPath(self):
        self._closePath()


def fail(message: str) -> None:
    print(f"fail: {message}", file=sys.stderr)
    raise SystemExit(1)


def zero_length_segments(font, glyph_name: str) -> bool:
    """True when two consecutive on-curve points are the same point."""
    glyph = font["glyf"][glyph_name]
    if glyph.numberOfContours <= 0:
        return False
    coords, ends, flags = glyph.getCoordinates(None)
    start = 0
    for end in ends:
        on = []
        for i in range(start, end + 1):
            if flags[i] & 1:
                on.append((int(coords[i][0]), int(coords[i][1])))
        for i, point in enumerate(on):
            if point == on[(i + 1) % len(on)]:
                return True
        start = end + 1
    return False


def check_font(font, style: str, strokes) -> None:
    cmap = font.getBestCmap()
    missing = sorted(target_set() - set(cmap))
    if missing:
        fail(f"{style} is missing {len(missing)} target characters: "
             + " ".join(f"U+{cp:04X}" for cp in missing[:12]))
    if set(cmap) != {cp for cp, _, _ in strokes}:
        fail(f"{style} cmap does not match the stroke source")
    if len(font.getGlyphOrder()) != len(strokes) + 1:
        fail(f"{style} has {len(font.getGlyphOrder())} glyphs, expected {len(strokes) + 1}")

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    ascent = font["hhea"].ascent
    descent = font["hhea"].descent
    for cp, advance, commands in strokes:
        name = cmap[cp]
        width, lsb = hmtx[name]
        if width != build.fu(advance):
            fail(f"{style} {name} advance {width} != {build.fu(advance)}")
        glyph = glyf[name]
        if cp in SPACES:
            if commands or glyph.numberOfContours != 0:
                fail(f"{style} space U+{cp:04X} is not empty")
            if width != build.fu(SPACES[cp]) or lsb != 0:
                fail(f"{style} space U+{cp:04X} metrics {width}, {lsb}")
            continue
        if not commands or glyph.numberOfContours <= 0:
            fail(f"{style} {name} (U+{cp:04X}) has no outline")
        if lsb != int(glyph.xMin):
            fail(f"{style} {name} lsb {lsb} != xMin {glyph.xMin}")
        # Marks included: nothing may reach past the line box and be clipped.
        if glyph.yMax > ascent or glyph.yMin < descent:
            fail(f"{style} {name} ({glyph.yMin}..{glyph.yMax}) leaves the line box")

    for name, contours in HOLES.items():
        count = glyf[name].numberOfContours
        if count != contours:
            fail(f"{style} {name} has {count} contours, expected {contours}")
        pen = AreaPen()
        glyf[name].draw(pen, glyf)
        signs = {1 if area > 0 else -1 for area in pen.areas if abs(area) > 1}
        if signs != {1, -1}:
            fail(f"{style} {name} contours do not wind as a hole ({pen.areas})")

    for name, base, extra in MARK_HOLES:
        want = glyf[base].numberOfContours + extra
        if glyf[name].numberOfContours != want:
            fail(f"{style} {name} has {glyf[name].numberOfContours} contours, expected {want}")

    for name in font.getGlyphOrder():
        if zero_length_segments(font, name):
            fail(f"{style} {name} has a zero-length segment")

    name_ids = {
        rec.nameID: rec.toUnicode()
        for rec in font["name"].names
        if rec.platformID == 3
    }
    if {1, 2, 4, 6} - set(name_ids):
        fail(f"{style} name table is missing an id")
    if name_ids[1] != "AhmiPrint":
        fail(f"{style} family name is {name_ids[1]!r}")
    if name_ids[2] != style:
        fail(f"{style} style name is {name_ids[2]!r}")
    if any(rec.platformID == 1 for rec in font["name"].names):
        fail(f"{style} still has Mac name records")

    os2 = font["OS/2"]
    if os2.fsType != 0:
        fail(f"{style} fsType is {os2.fsType}, expected 0")
    expect_weight = 700 if style == "Bold" else 400
    if os2.usWeightClass != expect_weight:
        fail(f"{style} weight class {os2.usWeightClass}")
    if font["head"].unitsPerEm != build.UPM:
        fail(f"{style} unitsPerEm {font['head'].unitsPerEm}")
    if b"\xb8\x01\xff\x85\xb0\x04\x8d" not in font["prep"].program.getBytecode():
        fail(f"{style} prep table is missing smart dropout control")

    # Round-trip through fontTools.
    from io import BytesIO

    buf = BytesIO()
    font.save(buf)
    again = TTFont(buf)
    if again.getGlyphOrder() != font.getGlyphOrder():
        fail(f"{style} did not round-trip")


def main() -> int:
    strokes = build.parse()

    loaded = {}
    for style in STYLES:
        for ext in (".ttf", ".woff2"):
            path = FONTS / f"AhmiPrint-{style}{ext}"
            if not path.is_file():
                fail(f"missing {path.name}")
            font = TTFont(path)
            if ext == ".ttf":
                loaded[style] = font
            else:
                if font.getGlyphOrder() != loaded[style].getGlyphOrder():
                    fail(f"{style} woff2 glyph order differs from the ttf")
        check_font(loaded[style], style, strokes)

    regular = loaded["Regular"]
    bold = loaded["Bold"]
    for table, attr in (("hhea", "ascent"), ("hhea", "descent"), ("hhea", "lineGap")):
        if getattr(regular[table], attr) != getattr(bold[table], attr):
            fail(f"family {table}.{attr} differs")
    for attr in ("sTypoAscender", "sTypoDescender", "sTypoLineGap", "usWinAscent", "usWinDescent"):
        if getattr(regular["OS/2"], attr) != getattr(bold["OS/2"], attr):
            fail(f"family OS/2.{attr} differs")
    if regular["post"].underlineThickness != bold["post"].underlineThickness:
        fail("underline thickness differs between weights")

    # Figures share one advance, taken from the stroke file, in both weights.
    digit_width = build.fu(next(adv for cp, adv, _ in strokes if cp == 48))
    for group, codes in TABULAR.items():
        for style, font in loaded.items():
            cmap = font.getBestCmap()
            widths = {font["hmtx"][cmap[cp]][0] for cp in codes}
            if len(widths) != 1:
                fail(f"{style} {group} are not tabular ({sorted(widths)})")
            if group == "figures" and widths != {digit_width}:
                fail(f"{style} figures are {widths}, the stroke file says {digit_width}")

    print(
        f"ok: {len(strokes)} characters in Regular and Bold, all {len(target_set())} "
        f"target characters, every non-space glyph drawn, figures tabular; "
        f"unitsPerEm {regular['head'].unitsPerEm}, ascent {regular['hhea'].ascent}, "
        f"descent {regular['hhea'].descent}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
