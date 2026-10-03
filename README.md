# Machine Learning for Biology

A book in seven chapters by Qasim Hussain, written from the daily series Machine Learning for Biology (24 July to
1 October 2026). Each chapter asks one biological question with one model, from logistic regression to k-means, and
fixes its rules before running anything. The code for each chapter stays in its own repository; `companions.yml` lists
them and pins each to the commit the chapter describes.

Read it at https://qasim-hussain-code.github.io/machine-learning-for-biology/, where the PDF and EPUB editions can also
be downloaded. This is a beta edition. The book will be revised, corrected and extended continuously for some time yet, and
suggestions for its improvement are most welcome, as an issue on this repository or a message on LinkedIn.

## Layout

| Path | What it holds |
| --- | --- |
| `chapters/` | The text: preface, chapters 1 to 7 and epilogue, in Markdown with front matter |
| `sources/` | The posts each piece was rewritten from, the only admissible source of facts and numbers |
| `figures/svg/` | The book's drawn figures, which follow the reader's light or dark theme |
| `STYLE.md` | The editorial guide every piece follows |
| `tools/lint_chapter.py` | Checks a piece against `STYLE.md` and its sources |
| `tools/build_book.py` | Builds the web edition into `docs/` |
| `tools/print_book.py`, `tools/print_pdf.mjs` | Build the print edition, `docs/machine-learning-for-biology.pdf` |
| `tools/epub_book.py` | Builds the EPUB edition, `docs/machine-learning-for-biology.epub` |
| `docs/` | The built book, ready for GitHub Pages |

## Building

The web edition needs Python 3 with `markdown` and `PyYAML`:

    python tools/build_book.py

The print edition also needs `pypdf`, Node 22 or later and an installed Chrome. Nothing else is installed or
downloaded; Chrome prints the book's own print stylesheet twice, so that the contents carry page numbers:

    python tools/print_book.py
    python tools/epub_book.py
    python tools/build_book.py      # again, so the title page links to the PDF and the EPUB
