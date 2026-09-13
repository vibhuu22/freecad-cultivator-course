# -*- coding: utf-8 -*-
"""Build every deck, then an index page.

    python tools\\build_all_decks.py           # HTML only
    python tools\\build_all_decks.py --pdf     # also print each deck to PDF
"""
import sys, os, glob, importlib, io, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "decks"))
import deck_kit

CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]


def modules():
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "decks", "d??_*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        out.append(importlib.import_module(name))
    return out


def to_pdf(html_path):
    exe = next((c for c in CHROME if os.path.exists(c)), None)
    if not exe:
        print("  no Chrome/Edge found - skipping PDF")
        return None
    pdf = os.path.splitext(html_path)[0] + ".pdf"
    cmd = [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           "--print-to-pdf-no-header", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=20000",
           "--print-to-pdf=" + pdf, "file:///" + html_path.replace("\\", "/")]
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pdf if os.path.exists(pdf) else None


def index(decks):
    rows = []
    for d, path in decks:
        pdf = os.path.splitext(os.path.basename(path))[0] + ".pdf"
        has_pdf = os.path.exists(os.path.join(deck_kit.DECKS, pdf))
        # the PDF link is a sibling of the card, never nested inside it:
        # an anchor inside an anchor is invalid and browsers unnest it
        rows.append(
            '<li><a class="card" href="%s"><span class="n">%s</span>'
            '<span class="t">%s</span><span class="m">%d sheets</span></a>%s</li>'
            % (os.path.basename(path), d.slug.split("-")[0], html.escape(d.title),
               len(d.sheets),
               '<a class="pdf" href="%s">PDF</a>' % pdf if has_pdf else '<span class="pdf"></span>'))
    page = INDEX.replace("__ROWS__", "".join(rows)).replace("__N__", str(len(decks)))
    out = os.path.join(deck_kit.DECKS, "index.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("  index.html")
    return out


INDEX = u"""<title>Design of Farm Machinery - Cultivator in FreeCAD</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{--paper:#E8EAE6;--sheet:#F6F7F4;--ink:#161814;--ink2:#575C52;--ink3:#7C8177;
  --rule:#C7CCC2;--rule2:#DEE2D9;--accent:#A8321E;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#131512;--sheet:#1A1D19;--ink:#DEE2D9;--ink2:#969C90;--ink3:#6F756A;
  --rule:#2D322A;--rule2:#232821;--accent:#E0603D;}}
:root[data-theme="dark"]{--paper:#131512;--sheet:#1A1D19;--ink:#DEE2D9;--ink2:#969C90;
  --ink3:#6F756A;--rule:#2D322A;--rule2:#232821;--accent:#E0603D;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Newsreader",Georgia,serif;font-size:17px;line-height:1.6}
.wrap{max-width:1100px;margin:0 auto;padding:clamp(28px,6vw,80px) clamp(20px,4vw,40px)}
h1{font-family:"Archivo",sans-serif;font-size:clamp(32px,5.5vw,60px);font-weight:800;
  letter-spacing:-.03em;margin:0 0 6px;line-height:1.04}
.sub{font-size:clamp(17px,1.6vw,21px);color:var(--ink2);max-width:60ch;margin:0 0 8px}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.19em;
  text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 10px}
hr{border:0;border-top:1px solid var(--rule);margin:clamp(26px,4vw,44px) 0}
ul{list-style:none;padding:0;margin:0;display:grid;gap:1px;background:var(--rule);
  border:1px solid var(--rule)}
li{display:grid;grid-template-columns:1fr auto;background:var(--sheet)}
a.card{display:grid;grid-template-columns:56px 1fr auto;gap:16px;align-items:baseline;
  padding:16px 20px;text-decoration:none;color:inherit;transition:background .15s;min-width:0}
a.card:hover{background:var(--paper)}
.pdf{display:flex;align-items:center;padding:0 20px;font-family:"IBM Plex Mono",monospace;
  font-size:11px;letter-spacing:.1em;color:var(--ink3);text-decoration:none;
  border-left:1px solid var(--rule);transition:color .15s,background .15s}
a.pdf:hover{color:var(--accent);background:var(--paper)}
.n{font-family:"IBM Plex Mono",monospace;font-size:13px;font-weight:600;color:var(--accent)}
.t{font-family:"Archivo",sans-serif;font-size:19px;font-weight:600;letter-spacing:-.01em}
.m{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink3);white-space:nowrap}
.m a{color:var(--accent)}
.foot{margin-top:clamp(26px,4vw,44px);font-size:14px;color:var(--ink3);max-width:70ch}
</style>
<div class="wrap">
<p class="eyebrow">Design of Farm Machinery</p>
<h1>Nine-Tyne Cultivator in FreeCAD</h1>
<p class="sub">A complete, screenshot-by-screenshot build of a tractor-mounted rigid-tyne
cultivator in FreeCAD 1.1 &mdash; from an empty document to a parametric assembly.
__N__ decks.</p>
<hr>
<ul>__ROWS__</ul>
<p class="foot">Each deck is a single self-contained HTML file: the screenshots are
embedded, so it works offline. Arrow keys page through it. Source design after
&ldquo;Design of Cultivator in SolidWorks | Nine tines cultivator&rdquo; by Malviya CAD
Solution; all FreeCAD modelling, dimensions and assumptions are documented on the slides.</p>
</div>
"""


def main():
    want_pdf = "--pdf" in sys.argv
    print("building decks ->", deck_kit.DECKS)
    built = []
    for m in modules():
        deck = m.build()
        built.append((deck, deck.write()))
    if want_pdf:
        print("printing PDFs...")
        for deck, path in built:
            p = to_pdf(path)
            if p:
                print("  %-34s %5.2f MB" % (os.path.basename(p),
                                            os.path.getsize(p) / 1048576.0))
    index(built)
    print("done: %d decks, %d sheets, %d unique images"
          % (len(built), sum(len(d.sheets) for d, _ in built), len(deck_kit._cache)))


if __name__ == "__main__":
    main()
