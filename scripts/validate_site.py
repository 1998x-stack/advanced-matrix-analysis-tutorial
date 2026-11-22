#!/usr/bin/env python3
"""Fail fast on missing assets, broken local routes and incomplete illustrated lessons."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import json, re, sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references=[]; self.ids=set(); self.h1=0; self.h2=0; self.math=0; self.figures=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='h2': self.h2+=1
        if tag=='math': self.math+=1
        if tag=='figure': self.figures+=1
        field='href' if tag in ('a','link') else 'src' if tag in ('script','img') else None
        if field and a.get(field): self.references.append(a[field])

def inspect(path,deep=False):
    parser=Inspect()
    source=path.read_text(encoding='utf-8')
    try: parser.feed(source)
    except Exception as err: ERRORS.append(f'{path}: parse error {err}'); return
    if deep:
        if parser.h1!=1: ERRORS.append(f'{path}: expected 1 h1, got {parser.h1}')
        if parser.h2<5: ERRORS.append(f'{path}: expected at least 5 h2, got {parser.h2}')
        if parser.math<2: ERRORS.append(f'{path}: expected at least 2 MathML formulas, got {parser.math}')
        if parser.figures<1: ERRORS.append(f'{path}: missing figure')
        if any(s in source for s in ('cdn.jsdelivr.net','MathJax','>上一章我们','>本讲介绍')):
            ERRORS.append(f'{path}: legacy dependency or lecture wrapper')
    for ref in parser.references:
        if ref.startswith(('http:', 'https:', 'mailto:', 'tel:', 'data:', '//')): continue
        target, _, frag=ref.partition('#')
        dest=(path.parent/unquote(target.split('?')[0])) if target else path
        if target and not dest.is_file(): ERRORS.append(f'{path}: missing local file {ref}')
        if deep and not target and frag and frag not in parser.ids:
            ERRORS.append(f'{path}: missing in-page anchor {ref}')

catalog=json.loads((ROOT/'courses.json').read_text(encoding='utf-8'))
if len(catalog['chapters'])!=28: ERRORS.append('catalog must have 28 lessons')
inspect(ROOT/'index.html')
for n in range(1,29):
    p=ROOT/'chapters'/f'{n:02}.html'
    if not p.is_file(): ERRORS.append(f'missing chapter {n:02}'); continue
    inspect(p,deep=n<=16)
    if not (ROOT/f'{n:02}.html').is_file(): ERRORS.append(f'missing legacy redirect {n:02}')
    c=catalog['chapters'][n-1]
    if c['file']!=f'chapters/{n:02}.html': ERRORS.append(f'wrong chapter file {n}')
    if c['status']!=('illustrated' if n<=16 else 'legacy'): ERRORS.append(f'wrong chapter status {n}')
for file in (ROOT/'assets/figures').glob('*.svg'):
    try:
        root=ET.fromstring(file.read_text(encoding='utf-8'))
        if not root.tag.endswith('svg') or 'viewBox' not in root.attrib:
            ERRORS.append(f'{file}: missing svg viewBox')
        tags={e.tag.split('}')[-1] for e in root.iter()}
        if not {'title','desc'}.issubset(tags): ERRORS.append(f'{file}: missing title/desc')
    except Exception as err: ERRORS.append(f'{file}: invalid SVG XML: {err}')
if ERRORS:
    print('\n'.join('ERROR '+e for e in ERRORS))
    sys.exit(1)
print('OK: 28 lessons, 16 illustrated, legacy routes, MathML, SVG XML, local links')
