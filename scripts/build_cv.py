#!/usr/bin/env python3
"""Compile both CV PDFs from `_data/*.yml` via Typst.

Reads the `cv/cv.typ` template (which in turn loads the YAML files
under `_data/`) and writes:

  assets/cv_en.pdf
  assets/cv_ko.pdf

Requires the `typst` Python package (installed from
`scripts/requirements.txt`). The package bundles the Typst compiler
as a Python extension, so no separate Typst CLI install is needed.

Run from the repo root, after `scripts/build.py`:

  python scripts/build_cv.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CV_TYP = ROOT / "cv" / "cv.typ"
FONT_DIR = ROOT / "cv" / "fonts"
ASSETS = ROOT / "assets"

OUTPUTS = (
    ("en", ASSETS / "cv_en.pdf"),
    ("ko", ASSETS / "cv_ko.pdf"),
)


def main() -> int:
    try:
        import typst  # type: ignore[import-not-found]
    except ImportError:
        print(
            "ERROR: the `typst` Python package is not installed.\n"
            "       run: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        return 1

    if not CV_TYP.is_file():
        print(f"ERROR: template not found: {CV_TYP}", file=sys.stderr)
        return 1
    if not FONT_DIR.is_dir():
        print(f"ERROR: font directory not found: {FONT_DIR}", file=sys.stderr)
        return 1

    ASSETS.mkdir(exist_ok=True)

    for lang, out_path in OUTPUTS:
        try:
            typst.compile(
                str(CV_TYP),
                output=str(out_path),
                root=str(ROOT),
                font_paths=[str(FONT_DIR)],
                sys_inputs={"lang": lang},
            )
        except typst.TypstError as e:
            print(f"ERROR compiling {lang} CV: {e}", file=sys.stderr)
            return 1
        size_kb = out_path.stat().st_size / 1024
        print(f"wrote {out_path.relative_to(ROOT)} ({size_kb:.1f} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
