#!/usr/bin/env python3
"""Minimal offline structural and local-link checks."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.headings, self.math, self.images = [], [], 0, 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in {"a", "link", "script", "img"}:
            field = "href" if tag in {"a", "link"} else "src"
            if a.get(field):
                self.links.append(a[field])
        if tag == "h1": self.headings.append(tag)
        if tag == "math": self.math += 1
        if tag == "img": self.images += 1

def check_html(path, deep=False):
    p = Inspector()
    try: p.feed(path.read_text(encoding="utf-8"))
    except Exception as e: ERRORS.append(f"{path}: cannot parse: {e}"); return
    if deep:
        if len(p.headings) != 1: ERRORS.append(f"{path}: expected one H1; got {len(p.headings)}")
        if not p.math: ERRORS.append(f"{path}: missing native MathML")
        if not p.images: ERRORS.append(f"{path}: missing conceptual figure")
    for ref in p.links:
        if ref.startswith(("http:", "https:", "mailto:", "tel:", "data:", "//", "#")): continue
        rel = ref.split("#",1)[0].split("?",1)[0]
        if rel and not (path.parent / rel).exists(): ERRORS.append(f"{path}: broken link {ref}")

catalog=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
if len(catalog["chapters"]) != 28: ERRORS.append("catalog must have 28 chapters")
if not (ROOT/"index.html").exists(): ERRORS.append("index.html missing")
else: check_html(ROOT/"index.html", True if False else False)
for n in range(1,29):
    p=ROOT/"chapters"/f"{n:02}.html"
    if not p.exists(): ERRORS.append(f"missing chapter {n:02}"); continue
    check_html(p, n <= 5)
    if not (ROOT/f"{n:02}.html").exists(): ERRORS.append(f"missing legacy redirect {n:02}")
for p in (ROOT/"assets/figures").glob("*.svg"):
    data=p.read_text(encoding="utf-8")
    for required in ('<svg', 'viewBox=', '<title', '<desc'):
        if required not in data: ERRORS.append(f"{p}: missing {required}")
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(data)
    except Exception as e: ERRORS.append(f"{p}: invalid SVG XML {e}")
if ERRORS:
    print("\n".join("ERROR "+e for e in ERRORS))
    sys.exit(1)
print("OK: 28 chapters, legacy routes, first 5 MathML + figures, local links, SVG XML")
