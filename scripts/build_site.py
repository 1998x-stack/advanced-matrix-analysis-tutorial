#!/usr/bin/env python3
"""Build the static GitHub Pages payload without third-party dependencies."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for name in ("index.html", "courses.json", ".nojekyll"):
    shutil.copy2(ROOT / name, OUT / name)
for n in range(1, 29):
    shutil.copy2(ROOT / f"{n:02}.html", OUT / f"{n:02}.html")
for dirname in ("chapters", "assets"):
    shutil.copytree(ROOT / dirname, OUT / dirname)
print(f"Built {OUT}; chapters: 28; legacy redirects: 28")
