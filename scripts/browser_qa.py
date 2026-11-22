#!/usr/bin/env python3
"""Responsive, MathML, SVG, JS and keyboard smoke QA for illustrated lessons.

Usage:
  python scripts/build_site.py
  python scripts/browser_qa.py --output qa/batch-16-20

Requires Playwright and a downloaded Chromium browser.
"""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
BATCH = [f"chapters/{n:02}.html" for n in range(16,21)]
PAGES = ["index.html"] + BATCH
VIEWPORTS = [(1440,900),(768,900),(390,844),(360,780)]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="qa/batch-16-20")
    args=parser.parse_args()
    out=ROOT / args.output
    out.mkdir(parents=True,exist_ok=True)
    if not (SITE/"index.html").exists():
        raise SystemExit("Build _site/ first: python scripts/build_site.py")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        raise SystemExit("Install playwright: pip install playwright") from err
    handler=partial(SimpleHTTPRequestHandler,directory=str(SITE))
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    base=f"http://127.0.0.1:{server.server_port}/"
    rows=[]
    failures=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
            for width,height in VIEWPORTS:
                context=browser.new_context(viewport={"width":width,"height":height},reduced_motion="reduce")
                page=context.new_page()
                console_errors=[]
                page.on("pageerror",lambda exc: console_errors.append(str(exc)))
                for file in PAGES:
                    before=len(console_errors)
                    response=page.goto(urljoin(base,file),wait_until="load",timeout=20000)
                    page.wait_for_timeout(75)
                    title=page.title()
                    h1=page.locator("h1").count()
                    overflow=page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                    math=page.locator("math").count()
                    bad_math=page.locator("math").evaluate_all(
                        "(els)=>els.filter(el=>{let r=el.getBoundingClientRect();return r.width===0||r.height===0}).length"
                    ) if math else 0
                    imgs=page.locator("img").count()
                    broken=page.locator("img").evaluate_all(
                        "(els)=>els.filter(img=>!img.complete || img.naturalWidth===0).length"
                    ) if imgs else 0
                    if file!="index.html":
                        if math<2:failures.append(f"{file} {width}: missing MathML")
                        if imgs<1:failures.append(f"{file} {width}: missing figure")
                    if h1!=1:failures.append(f"{file} {width}: h1={h1}")
                    if overflow:failures.append(f"{file} {width}: document overflow")
                    if bad_math:failures.append(f"{file} {width}: zero geometry MathML={bad_math}")
                    if broken:failures.append(f"{file} {width}: broken images={broken}")
                    new_errors=console_errors[before:]
                    if new_errors:failures.append(f"{file} {width}: JS errors={new_errors}")
                    lab_ok=None
                    if file!="index.html":
                        control=page.locator("[data-lab] input,[data-lab] select").first
                        if control.count():
                            output=page.locator("[data-lab] output").first
                            original=output.inner_text()
                    # Test each interactive lab using a real UI input/change event
                    if file!="index.html":
                        control=page.locator("[data-lab] input,[data-lab] select").first
                        output=page.locator("[data-lab] output").first
                        if control.count() and output.count():
                            old=output.inner_text()
                            is_select=control.evaluate("(el)=>el.tagName.toLowerCase()==='select'")
                            if is_select:
                                count=control.locator("option").count()
                                if count>1: control.select_option(index=1)
                            else:
                                control.evaluate("""el => {
                                    el.value=el.max||'1';
                                    el.dispatchEvent(new Event('input',{bubbles:true}));
                                }""")
                            now=output.inner_text()
                            lab_ok=now!=old
                            if not lab_ok:failures.append(f"{file} {width}: lab output unchanged")
                    # Print is a paper-width layout, not a phone-width layout.
                    page.set_viewport_size({"width":816,"height":1056})
                    page.emulate_media(media="print")
                    print_overflow=page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                    page.emulate_media(media="screen")
                    page.set_viewport_size({"width":width,"height":height})
                    if print_overflow: failures.append(f"{file} {width}: print overflow")
                    name=file.replace("/","-").replace(".html","")
                    shot=out/f"{name}-{width}.png"
                    page.screenshot(path=str(shot),full_page=True)
                    page.keyboard.press("Tab")
                    keyboard_focus=page.evaluate("document.activeElement && document.activeElement.tagName !== 'BODY'")
                    if not keyboard_focus: failures.append(f"{file} {width}: keyboard focus missing")
                    rows.append(dict(file=file,width=width,height=height,title=title,
                                     h1=h1,math=math,broken_images=broken,overflow=overflow,
                                     math_bad_geometry=bad_math,print_overflow=print_overflow,js_errors=new_errors,
                                     interactive=lab_ok,keyboard_focus=keyboard_focus,screenshot=str(shot.relative_to(ROOT))))
                context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    report=dict(pages=PAGES,viewports=VIEWPORTS,rows=rows,failures=failures)
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"checked":len(rows),"failed":len(failures),"failures":failures},ensure_ascii=False,indent=2))
    return 1 if failures else 0

if __name__=="__main__":sys.exit(main())
