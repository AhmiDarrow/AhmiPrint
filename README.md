# AhmiPrint

AhmiPrint is a typewriter and newspaper slab serif in Regular and Bold.
It is drawn as strokes with round, ink-spread terminals and slab serifs, like a typewriter. Its proportional widths, tabular figures and large x-height come from newspaper text faces, so it stays readable at small sizes.

Version 1.000. The public release is [v1.0.0](https://github.com/AhmiDarrow/AhmiPrint/releases/tag/v1.0.0).

![AhmiPrint specimen](specimen.png)

## What's here

| Path | What it is |
|---|---|
| `fonts/` | Ready-to-use files: `AhmiPrint-Regular` and `AhmiPrint-Bold`, each as `.ttf` and `.woff2` |
| `source/ahmi-print.strokes` | The source. Every character drawn as strokes on a 24-unit grid |
| `build.py` | Turns the stroke file into the font files |
| `check.py` | Checks advances, holes, tabular figures, and that both weights share one set of metrics |
| `specimen.html` | Open in a browser to see every character |
| `LICENSE` | SIL Open Font License 1.1 |
| `CHANGELOG.md` | Release history |

## Using it on a web page

```css
@font-face {
  font-family: "AhmiPrint";
  src: url("fonts/AhmiPrint-Regular.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "AhmiPrint";
  src: url("fonts/AhmiPrint-Bold.woff2") format("woff2");
  font-weight: 700;
}
h1 { font: 700 48px/1.2 "AhmiPrint", serif; }
p  { font: 400 16px/1.45 "AhmiPrint", serif; }
```

The caps and descenders are tall for the size, so give body text a line height of about 1.4.

## Using it on the desktop

Install `AhmiPrint-Regular.ttf` and `AhmiPrint-Bold.ttf`. On Windows, select both files, right-click, and choose Install. On macOS, open them in Font Book and choose Install. The family name is AhmiPrint. Bold is the bold style of that family.

The zip on the [release](https://github.com/AhmiDarrow/AhmiPrint/releases/tag/v1.0.0) has those files, the web fonts, this readme, and the specimen.

## Characters

Basic Latin, U+0020 through U+007E: the English uppercase and lowercase alphabets, digits, and the standard keyboard punctuation. 95 characters, each drawn in the stroke file. U+00A0 no-break space uses the same empty glyph as the space, so a line will not break there. No accented letters.

The drawing grid is 24 units tall: baseline 0, x-height 14, cap height 20, ascender 21, descender -6. Regular is stroke weight 2.6 and Bold is 3.8, both with round caps and round joins. Slab serifs are strokes of the same weight as the stems. The zero is slashed, and every figure has the same width so columns of numbers line up.

## Changing a letter

1. Edit its strokes in `source/ahmi-print.strokes`. The comments at the top of that file explain the commands.
2. Rebuild:

```bash
pip install fonttools brotli skia-pathops
python build.py
python check.py
```

`build.py` expands every stroke to a filled outline, removes the overlaps, and writes the `.ttf` and `.woff2` files. Advance widths come from the stroke file and are the same in both weights.

## About

AhmiPrint was made for the newspapers and typed reports in Springfield MO, a Project Zomboid map. It is built the same way as Remedy Sans.

Hope this helps
- Ahmi

## License

AhmiPrint is licensed under the [SIL Open Font License, Version 1.1](LICENSE). You can use it freely in personal and commercial projects, embed it in apps, games and websites, and modify or redistribute it under the same license. The font itself may not be sold on its own. There is no Reserved Font Name.
