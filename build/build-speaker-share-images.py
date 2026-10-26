#!/usr/bin/env python3
"""Render the share images of the Main Speaker pages (og:image, 1200x630):
    assets/speakers/<slug>-en.png and <slug>-ar.png

Speaker name, role and photo come from SPEAKERS in build-speaker-pages.py.
Re-run after a speaker photo changes:
    python3 build/build-speaker-share-images.py
It needs a headless Chromium: Playwright's chrome-headless-shell in
~/.cache/ms-playwright is used by default (set CHROME to another binary).
On this server the shell also needs the libraries Chromium depends on
(libnss3, libnspr4, libatk...): put them in a folder and set
LD_LIBRARY_PATH to it. Without a working browser the script writes the
HTML cards to build/share-images/ and prints the command to run.
"""
import glob
import html
import importlib.util
import os
import pathlib
import subprocess

from common import ROOT

spec = importlib.util.spec_from_file_location("speaker_pages", ROOT / "build" / "build-speaker-pages.py")
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

WORK = ROOT / "build" / "share-images"
OUT = ROOT / "assets" / "speakers"

TEXT = {
    "en": ("ECommerce Day 2026", "Main Speaker", "5 November 2026 · Stage 1"),
    "ar": ("يوم التجارة الإلكترونية 2026", "متحدث رئيسي", "5 نوفمبر 2026، المسرح 1"),
}


def card(sp, lang):
    ar = lang == "ar"
    event, pill, meta = TEXT[lang]
    name = sp[lang]["name"]
    role = sp["en"]["role"]
    font = '"IBM Plex Sans Arabic", Manrope, sans-serif' if ar else "Manrope, sans-serif"
    e = html.escape
    # The photo already carries the event logo (top corner), so the text side has none.
    return f"""<!doctype html><html lang="{lang}" dir="{'rtl' if ar else 'ltr'}"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@500;700&family=Manrope:wght@600;800&family=JetBrains+Mono:wght@600&display=block" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1200px;height:630px;overflow:hidden;background:#fff}}
body{{display:grid;grid-template-columns:1fr 520px;font-family:{font};color:#101010}}
.t{{padding:64px 64px 56px;display:flex;flex-direction:column}}
.ev{{margin-bottom:auto;font:600 {'20px "IBM Plex Sans Arabic"' if ar else '16px "JetBrains Mono"'};letter-spacing:{0 if ar else '.14em'};text-transform:uppercase;color:#6b747e}}
.pill{{align-self:flex-start;background:#101010;color:#05ef62;border-radius:999px;padding:9px 18px;font:600 {'18px "IBM Plex Sans Arabic"' if ar else '15px "JetBrains Mono"'};letter-spacing:{0 if ar else '.12em'};text-transform:uppercase;margin-bottom:22px}}
h1{{font-size:{64 if ar else 58}px;line-height:{1.25 if ar else 1.05};font-weight:{700 if ar else 800};letter-spacing:{0 if ar else '-.02em'};margin-bottom:14px}}
.r{{font:600 24px Manrope,sans-serif;color:#4a5563;margin-bottom:26px;direction:ltr;text-align:{'right' if ar else 'left'}}}
.m{{font-size:24px;font-weight:700;color:#04c44e}}
.p{{background:#f4f6f8 url({sp['photo']}) center 18%/cover no-repeat}}</style></head>
<body><div class="t"><div class="ev">{e(event)}</div><span class="pill">{e(pill)}</span><h1>{e(name)}</h1><div class="r">{e(role)}</div><div class="m">{e(meta)}</div></div><div class="p"></div></body></html>"""


def chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    found = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")))
    return found[-1] if found else None


def main():
    WORK.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    browser = chrome()
    for sp in pages.SPEAKERS:
        for lang in ("en", "ar"):
            name = f"{sp['slug']}-{lang}"
            src = WORK / f"{name}.html"
            src.write_text(card(sp, lang), encoding="utf-8")
            cmd = [browser or "chrome-headless-shell", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                   "--window-size=1200,630", "--virtual-time-budget=10000",
                   f"--screenshot={OUT / (name + '.png')}", src.as_uri()]
            if not browser:
                print("no headless Chromium found; run:", " ".join(cmd))
                continue
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            ok = (OUT / f"{name}.png").exists() and r.returncode == 0
            print(("wrote " if ok else "FAILED ") + str(OUT / f"{name}.png"), "" if ok else r.stderr[-300:])


if __name__ == "__main__":
    main()
