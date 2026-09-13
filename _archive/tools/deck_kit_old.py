# -*- coding: utf-8 -*-
"""Slide-deck generator for the 9-tyne cultivator course.

Each deck is one self-contained HTML file: screenshots are base64-embedded, so a
deck can be emailed, put on a USB stick, or opened offline in a lab with no
network.  Arrow keys page through it; it prints to PDF cleanly.

Adapted from the moldboard-plough generator in ..\\..\\fd\\build_deck.py.
"""
import base64, os, html, io

ROOT   = r"C:\Users\ASUS\Desktop\freecad"
SHOTS  = os.path.join(ROOT, "screenshots")
DECKS  = os.path.join(ROOT, "decks")
if not os.path.isdir(DECKS):
    os.makedirs(DECKS)

_cache = {}


def uri(name):
    if name not in _cache:
        path = os.path.join(SHOTS, name + ".png")
        if not os.path.exists(path):
            raise IOError("missing screenshot: " + path)
        with open(path, "rb") as f:
            _cache[name] = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return _cache[name]


# ------------------------------------------------------------------ fragments
def fig(name, proj, cap=""):
    c = '<figcaption>%s</figcaption>' % cap if cap else ''
    return ('<figure class="plate"><span class="proj">%s</span>'
            '<img src="%s" alt="%s" loading="lazy">%s</figure>'
            % (html.escape(proj), uri(name), html.escape(cap or proj), c))


def plates(items, cls="grid-2"):
    return '<div class="plates %s">%s</div>' % (cls, "".join(fig(*i) for i in items))


def wide(name, proj, cap=""):
    return '<div class="plates grid-1">%s</div>' % fig(name, proj, cap)


def specs(rows):
    return ('<dl class="specs">' +
            "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in rows) +
            '</dl>')


def tbl(headers, rows, cls="tbl"):
    head = "".join("<th>%s</th>" % h for h in headers)
    body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ('<table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
            % (cls, head, body))


def steps(items, compact=False):
    li = "".join("<li><span>%s</span>%s</li>"
                 % (t, ('<code class="cmd">%s</code>' % html.escape(c)) if c else "")
                 for t, c in items)
    return '<ol class="steps%s">%s</ol>' % (" compact" if compact else "", li)


def phases(items):
    return ('<ol class="phases">' +
            "".join("<li><b>%s</b><span>%s</span></li>" % (a, b) for a, b in items) +
            '</ol>')


def ticks(items, minus=False):
    return ('<ul class="tick%s">' % (" minus" if minus else "") +
            "".join("<li>%s</li>" % i for i in items) + '</ul>')


def note(text, kind="note"):
    return '<p class="%s">%s</p>' % (kind, text)


def warn(text):
    return note(text, "warn")


def code(text, lang=""):
    return ('<div class="code"><pre><code>%s</code></pre></div>'
            % html.escape(text.strip("\n")))


def cols(a, b, wide_right=False):
    return ('<div class="cols%s"><div>%s</div><div>%s</div></div>'
            % (" cols-wide" if wide_right else "", a, b))


def kv(label, value):
    return '<span class="kv"><i>%s</i>%s</span>' % (label, value)


# ---------------------------------------------------------------------- deck
class Deck(object):
    def __init__(self, slug, title, subtitle=""):
        self.slug = slug
        self.title = title
        self.subtitle = subtitle
        self.sheets = []

    def sheet(self, num, part, op, title, body, eyebrow=None, kind="std"):
        self.sheets.append(dict(num=num, part=part, op=op, title=title,
                                body=body, eyebrow=eyebrow, kind=kind))
        return self

    def _render(self, s, i):
        eyebrow = '<p class="eyebrow">%s</p>' % s["eyebrow"] if s["eyebrow"] else ''
        return """
<section class="sheet %s" id="s%d" aria-label="Sheet %s - %s">
  <div class="sheet-inner">
    <header class="sheet-head">%s<h2>%s</h2></header>
    <div class="sheet-body">%s</div>
    <div class="titleblock">
      <div><span>SHEET</span><b>%s</b></div>
      <div><span>PART</span><b>%s</b></div>
      <div><span>OPERATION</span><b>%s</b></div>
      <div><span>UNITS</span><b>inch (imperial decimal)</b></div>
    </div>
  </div>
</section>""" % (s["kind"], i, s["num"], html.escape(s["title"]),
                 eyebrow, s["title"], s["body"], s["num"], s["part"], s["op"])

    def write(self):
        nav = "".join('<a href="#s%d" data-i="%d"><span>%s</span></a>' % (i, i, s["num"])
                      for i, s in enumerate(self.sheets))
        body = "".join(self._render(s, i) for i, s in enumerate(self.sheets))
        page = (SHELL.replace("__TITLE__", html.escape(self.title))
                     .replace("__NAV__", nav)
                     .replace("__BODY__", body)
                     .replace("__COUNT__", str(len(self.sheets))))
        out = os.path.join(DECKS, self.slug + ".html")
        with io.open(out, "w", encoding="utf-8") as f:
            f.write(page)
        mb = os.path.getsize(out) / 1024.0 / 1024.0
        print("  %-34s %2d sheets  %5.2f MB" % (self.slug + ".html", len(self.sheets), mb))
        return out


SHELL = u"""<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --paper:#E8EAE6; --sheet:#F6F7F4; --plate:#23262A;
  --ink:#161814; --ink2:#575C52; --ink3:#7C8177;
  --rule:#C7CCC2; --rule2:#DEE2D9;
  --accent:#A8321E; --soil:#7A5A32; --steel:#5C6874; --crop:#4A6B34;
  --shadow:0 1px 2px rgba(20,24,18,.06),0 8px 24px -12px rgba(20,24,18,.18);
  --plate-filter:none;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#131512; --sheet:#1A1D19; --plate:#23262A;
    --ink:#DEE2D9; --ink2:#969C90; --ink3:#6F756A;
    --rule:#2D322A; --rule2:#232821;
    --accent:#E0603D; --soil:#BE9159; --steel:#8DA0AE; --crop:#8FB56A;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -14px rgba(0,0,0,.7);
    --plate-filter:none;
  }
}
:root[data-theme="dark"]{
  --paper:#131512; --sheet:#1A1D19; --plate:#23262A;
  --ink:#DEE2D9; --ink2:#969C90; --ink3:#6F756A;
  --rule:#2D322A; --rule2:#232821;
  --accent:#E0603D; --soil:#BE9159; --steel:#8DA0AE; --crop:#8FB56A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -14px rgba(0,0,0,.7);
  --plate-filter:none;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Newsreader",Georgia,"Times New Roman",serif;
  font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased;}
h1,h2,h3{font-family:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;
  text-wrap:balance;margin:0;letter-spacing:-.018em;}
code,.mono,.proj,.eyebrow,.titleblock,.specs dt,.tag,.cmd,th,.kv i{
  font-family:"IBM Plex Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;}

#deck{height:100vh;overflow-y:auto;scroll-snap-type:y proximity;scroll-behavior:smooth;}
@media (prefers-reduced-motion:reduce){#deck{scroll-behavior:auto}}
.sheet{scroll-snap-align:start;min-height:100vh;display:flex;padding:clamp(14px,2.2vw,34px);}
.sheet-inner{position:relative;flex:1;display:flex;flex-direction:column;
  background:var(--sheet);border:1px solid var(--rule);box-shadow:var(--shadow);
  padding:clamp(22px,3.4vw,54px) clamp(20px,3.4vw,58px) 76px;
  background-image:linear-gradient(var(--rule2) 1px,transparent 1px),
    linear-gradient(90deg,var(--rule2) 1px,transparent 1px);
  background-size:52px 52px;background-position:-1px -1px;}
.sheet-body{flex:1;max-width:1500px;width:100%;margin:0 auto;}
.sheet-head{max-width:1500px;width:100%;margin:0 auto clamp(16px,2vw,26px);}
.eyebrow{margin:0 0 8px;font-size:11px;letter-spacing:.19em;text-transform:uppercase;
  color:var(--accent);font-weight:600;}
.sheet-head h2{font-size:clamp(28px,4.1vw,54px);font-weight:800;line-height:1.03;}
.sheet-head h2::after{content:"";display:block;width:56px;height:3px;
  background:var(--accent);margin-top:16px;}

.sheet.title .sheet-head h2{font-size:clamp(40px,7.4vw,96px);letter-spacing:-.035em;}
.sheet.title .lede{font-size:clamp(18px,1.9vw,25px);max-width:36ch;}
.sheet.title .sheet-body{display:grid;gap:clamp(20px,3vw,44px);
  grid-template-columns:minmax(280px,.85fr) minmax(320px,1.35fr);align-items:center;}
.sheet.title .plate{margin:0}
.sheet.title .specs{margin-top:26px}
@media(max-width:900px){.sheet.title .sheet-body{grid-template-columns:1fr}}

.lede{font-size:clamp(17px,1.4vw,20.5px);line-height:1.55;color:var(--ink);
  max-width:78ch;margin:0 0 clamp(16px,2vw,26px);}
p{margin:0 0 .85em;max-width:72ch}
h3{font-size:13px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink2);margin:1.7em 0 .7em;padding-bottom:7px;border-bottom:1px solid var(--rule);}
h3:first-child{margin-top:0}
em{font-style:italic}
strong{font-weight:600;color:var(--ink)}
var{font-family:"IBM Plex Mono",monospace;font-style:normal;color:var(--accent);font-size:.94em}
.note{font-size:15px;color:var(--ink2);border-left:2px solid var(--soil);
  padding-left:14px;margin-top:1.1em;max-width:74ch}
.note strong{color:var(--soil)}
.warn{font-size:15px;color:var(--ink2);border-left:2px solid var(--accent);
  padding-left:14px;margin-top:1.1em;max-width:74ch}
.warn strong{color:var(--accent)}
.kv{display:inline-block;margin:0 18px 6px 0}
.kv i{font-style:normal;font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink3);display:block}

.cols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(22px,3.2vw,52px);align-items:start;}
.cols-wide{grid-template-columns:1fr 1.15fr}
@media(max-width:960px){.cols{grid-template-columns:1fr;gap:26px}}

.plates{display:grid;gap:clamp(12px,1.5vw,20px);margin-top:clamp(16px,2vw,26px)}
.grid-1{grid-template-columns:1fr}
.grid-2{grid-template-columns:repeat(2,1fr)}
.grid-3{grid-template-columns:repeat(3,1fr)}
.grid-4{grid-template-columns:repeat(4,1fr)}
@media(max-width:1100px){.grid-4{grid-template-columns:repeat(2,1fr)}
  .grid-3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.grid-2,.grid-3,.grid-4{grid-template-columns:1fr}}
.plate{margin:0;border:1px solid var(--rule);background:var(--plate);
  position:relative;overflow:hidden;display:flex;flex-direction:column;}
.plate img{display:block;width:100%;aspect-ratio:16/10;object-fit:contain;
  background:var(--plate);filter:var(--plate-filter);}
.grid-1 .plate img{aspect-ratio:16/9}
.proj{position:absolute;top:0;left:0;z-index:2;font-size:9.5px;letter-spacing:.15em;
  font-weight:600;background:var(--ink);color:var(--sheet);padding:4px 9px;}
.plate figcaption{font-size:13.5px;line-height:1.42;color:var(--ink2);
  padding:9px 12px 11px;border-top:1px solid var(--rule2);background:var(--sheet);}

.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:0;margin:1.2em 0 0;border-top:1px solid var(--rule);}
.specs>div{border-bottom:1px solid var(--rule2);padding:9px 12px 9px 0;}
.specs dt{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);margin-bottom:3px;}
.specs dd{margin:0;font-size:16px;font-weight:600;font-variant-numeric:tabular-nums;
  font-family:"Archivo",sans-serif;}

.tbl{width:100%;border-collapse:collapse;font-size:14.5px;margin:.6em 0 1em;
  display:block;overflow-x:auto;}
.tbl thead th{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);
  text-align:left;font-weight:600;border-bottom:1px solid var(--rule);padding:0 14px 7px 0;white-space:nowrap;}
.tbl td{padding:8px 14px 8px 0;border-bottom:1px solid var(--rule2);vertical-align:top;line-height:1.42;}
.tbl.sw td:first-child{color:var(--ink3);white-space:nowrap}
.tbl.sw td:nth-child(2){font-weight:600}

ul.tick{list-style:none;padding:0;margin:.5em 0 1em}
ul.tick li{position:relative;padding-left:20px;margin-bottom:.6em;max-width:68ch}
ul.tick li::before{content:"";position:absolute;left:0;top:.62em;width:9px;height:1px;background:var(--accent)}
ul.tick.minus li::before{background:var(--ink3)}
ol.phases{list-style:none;padding:0;margin:.5em 0 1em;counter-reset:p}
ol.phases li{counter-increment:p;position:relative;padding-left:40px;margin-bottom:1.05em;max-width:66ch}
ol.phases li::before{content:counter(p,decimal-leading-zero);position:absolute;left:0;top:.15em;
  font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:600;color:var(--accent);
  border:1px solid var(--rule);padding:2px 6px;}
ol.phases b{font-family:"Archivo",sans-serif;font-size:16px;display:block;margin-bottom:1px}
ol.phases span{color:var(--ink2);font-size:15.5px}
ol.steps{list-style:none;padding:0;margin:.5em 0 1em;counter-reset:s}
ol.steps li{counter-increment:s;position:relative;padding-left:36px;margin-bottom:.85em}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:.1em;width:22px;height:22px;
  display:grid;place-items:center;font-family:"IBM Plex Mono",monospace;font-size:11px;
  font-weight:600;color:var(--sheet);background:var(--ink);}
ol.steps span{display:block;font-size:15.5px;line-height:1.45;max-width:68ch}
ol.steps.compact li{margin-bottom:.6em}
.cmd{display:block;margin-top:5px;font-size:12.5px;color:var(--accent);background:var(--paper);
  border:1px solid var(--rule2);padding:5px 9px;overflow-x:auto;white-space:pre;}

.code{background:var(--paper);border:1px solid var(--rule);margin:.7em 0 1em;overflow-x:auto;}
.code pre{margin:0;padding:14px 16px}
.code code{font-size:12.6px;line-height:1.62;color:var(--ink);white-space:pre;}
p code,td code,li code,span code{font-size:.86em;background:var(--paper);
  border:1px solid var(--rule2);padding:1px 5px;color:var(--accent);}

.titleblock{position:absolute;left:clamp(20px,3.4vw,58px);right:clamp(20px,3.4vw,58px);
  bottom:22px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  border:1px solid var(--rule);background:var(--sheet);}
.titleblock>div{padding:6px 12px;border-right:1px solid var(--rule);min-width:0}
.titleblock>div:last-child{border-right:0}
.titleblock span{display:block;font-size:8.5px;letter-spacing:.16em;color:var(--ink3);}
.titleblock b{font-size:12px;font-weight:600;color:var(--ink2);white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;display:block;}
@media(max-width:700px){.titleblock{grid-template-columns:repeat(2,1fr)}
  .titleblock>div:nth-child(2n){border-right:0}}

#rail{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:40;
  display:flex;flex-direction:column;gap:1px;padding:6px 0 6px 6px;}
#rail a{font-family:"IBM Plex Mono",monospace;font-size:9.5px;font-weight:600;color:var(--ink3);
  text-decoration:none;padding:2px 6px;line-height:1.5;border-left:2px solid transparent;
  transition:color .18s,border-color .18s;}
#rail a:hover{color:var(--ink)}
#rail a[aria-current="true"]{color:var(--accent);border-left-color:var(--accent)}
#rail a:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media(max-width:900px){#rail{display:none}}
#hint{position:fixed;right:14px;bottom:12px;z-index:40;font-family:"IBM Plex Mono",monospace;
  font-size:10px;letter-spacing:.1em;color:var(--ink3);background:var(--sheet);
  border:1px solid var(--rule);padding:4px 9px;}

@media print{
  @page{size:1900px 1188px;margin:0}
  html,body{background:#fff}
  body{font-size:13px;line-height:1.46}
  #deck{height:auto;overflow:visible}
  #rail,#hint{display:none}
  /* never clip: a sheet that runs long spills to a second page rather than
     silently losing its last paragraph */
  .sheet{min-height:1188px;height:auto;page-break-after:always;break-after:page;padding:0;}
  .sheet-inner{border:0;box-shadow:none;background:#fff;background-image:none;
    padding:30px 40px 56px;}
  .sheet-head{margin-bottom:14px}
  .sheet-head h2{font-size:31px}
  .sheet.title .sheet-head h2{font-size:64px}
  .lede{font-size:15px;margin-bottom:12px}
  h3{margin:1.1em 0 .5em}
  .plates{gap:10px;margin-top:12px}
  .plate img{max-height:272px;aspect-ratio:auto;height:auto;filter:none}
  .grid-1 .plate img{max-height:380px}
  .sheet.title .plate img{max-height:520px}
  .plate figcaption{font-size:11.5px;padding:6px 9px 7px}
  .specs dd{font-size:14px}
  .tbl{font-size:11.8px;display:table}
  .tbl td{padding:5px 12px 5px 0}
  .code code{font-size:10.4px;line-height:1.46}
  .code pre{padding:10px 12px}
  ol.steps span,ol.phases span{font-size:12.6px}
  ol.steps li,ol.phases li{margin-bottom:.5em}
  ul.tick li{margin-bottom:.4em}
  .note,.warn{font-size:12.2px;margin-top:.7em}
  .titleblock{bottom:16px}
}
</style>
<nav id="rail" aria-label="Sheets">__NAV__</nav>
<div id="deck">__BODY__</div>
<div id="hint"><span id="cnt">01</span> / __COUNT__ &nbsp;&middot;&nbsp; &uarr; &darr; to page</div>
<script>
(function(){
  var deck=document.getElementById('deck');
  var sheets=[].slice.call(deck.querySelectorAll('.sheet'));
  var links=[].slice.call(document.querySelectorAll('#rail a'));
  var cnt=document.getElementById('cnt');
  var cur=-1;
  function mark(i){
    if(i===cur)return; cur=i;
    links.forEach(function(a,k){a.setAttribute('aria-current',k===i?'true':'false');});
    cnt.textContent=String(i+1).padStart(2,'0');
  }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting) mark(sheets.indexOf(e.target)); });
    },{root:deck,threshold:.5});
    sheets.forEach(function(s){io.observe(s);});
  }
  function go(i){
    i=Math.max(0,Math.min(sheets.length-1,i));
    sheets[i].scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
    mark(i);
  }
  document.addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    var t=e.target.tagName;
    if(t==='INPUT'||t==='TEXTAREA')return;
    if(e.key==='ArrowDown'||e.key==='PageDown'||e.key===' '){e.preventDefault();go(cur+1);}
    else if(e.key==='ArrowUp'||e.key==='PageUp'){e.preventDefault();go(cur-1);}
    else if(e.key==='Home'){e.preventDefault();go(0);}
    else if(e.key==='End'){e.preventDefault();go(sheets.length-1);}
  });
  links.forEach(function(a,k){a.addEventListener('click',function(e){e.preventDefault();go(k);});});
  mark(0);
})();
</script>
"""
