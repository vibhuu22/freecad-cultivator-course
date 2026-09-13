# -*- coding: utf-8 -*-
"""Slide-deck generator for the 9-tyne cultivator course.

Design rules, so every slide lines up with every other slide:

  * one idea per slide, and never more than five bullets
  * body text is 20px, headings are large, nothing is small
  * a fixed grid - eyebrow, title, rule, then the body starts at the same
    height on every slide
  * pictures are big, always 4:3, always the same size in a given layout
  * 16:9 slides, so they fill a projector

Each deck is one self-contained HTML file with the screenshots embedded, so it
works offline. Arrow keys page through it; it prints one PDF page per slide.
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


# ---------------------------------------------------------------- pictures
def shot(name, caption=""):
    """One picture, filling its column."""
    cap = '<figcaption>%s</figcaption>' % caption if caption else ''
    return ('<figure class="shot"><img src="%s" alt="%s">%s</figure>'
            % (uri(name), html.escape(caption or name), cap))


def strip(name, caption=""):
    """A wide, short picture such as a toolbar - not forced to 4:3."""
    cap = '<figcaption>%s</figcaption>' % caption if caption else ''
    return ('<figure class="shot strip"><img src="%s" alt="%s">%s</figure>'
            % (uri(name), html.escape(caption or name), cap))


def shots(items, cls="two"):
    """Two or three pictures side by side, all the same size."""
    return '<div class="shots %s">%s</div>' % (cls, "".join(shot(*i) for i in items))


# ------------------------------------------------------------------- text
def lede(text):
    return '<p class="lede">%s</p>' % text


def points(items):
    return '<ul class="points">%s</ul>' % "".join("<li>%s</li>" % i for i in items)


def steps(items):
    """Numbered instructions. Each item is a string, or (text, keystroke)."""
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append('<li>%s<b>%s</b></li>' % (it[0], html.escape(it[1])))
        else:
            out.append('<li>%s</li>' % it)
    return '<ol class="steps">%s</ol>' % "".join(out)


def table(headers, rows):
    head = "".join("<th>%s</th>" % h for h in headers)
    body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (head, body)


def facts(rows):
    """The strip of key numbers used on cover and summary slides."""
    return ('<dl class="facts">' +
            "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in rows) +
            '</dl>')


def callout(text, kind="note"):
    return '<p class="%s">%s</p>' % (kind, text)


def warn(text):
    return callout(text, "warn")


def heading(text):
    return '<h3>%s</h3>' % text


# ---------------------------------------------------------------- layouts
def split(left, right):
    """Picture on the left, words on the right."""
    return '<div class="split"><div>%s</div><div>%s</div></div>' % (left, right)


def split_even(left, right):
    return '<div class="split even"><div>%s</div><div>%s</div></div>' % (left, right)


def stack(*blocks):
    return "".join(b for b in blocks if b)


# ------------------------------------------------------------------- deck
class Deck(object):
    def __init__(self, slug, title, part=""):
        self.slug = slug
        self.title = title
        self.part = part
        self.sheets = []

    def slide(self, title, body, eyebrow="", kind="std"):
        self.sheets.append(dict(title=title, body=body, eyebrow=eyebrow, kind=kind))
        return self

    def cover(self, title, body):
        return self.slide(title, body, eyebrow=self.part, kind="cover")

    def _render(self, s, i, n):
        eyebrow = ('<p class="eyebrow">%s</p>' % s["eyebrow"]) if s["eyebrow"] else ''
        return """
<section class="sheet %s" id="s%d" aria-label="Slide %d">
  <div class="inner">
    <header>%s<h2>%s</h2></header>
    <div class="body">%s</div>
    <footer><span>%s</span><span>%02d / %02d</span></footer>
  </div>
</section>""" % (s["kind"], i, i + 1, eyebrow, s["title"], s["body"],
                 html.escape(self.title), i + 1, n)

    def write(self):
        n = len(self.sheets)
        nav = "".join('<a href="#s%d">%02d</a>' % (i, i + 1) for i in range(n))
        body = "".join(self._render(s, i, n) for i, s in enumerate(self.sheets))
        page = (SHELL.replace("__TITLE__", html.escape(self.title))
                     .replace("__NAV__", nav)
                     .replace("__BODY__", body))
        out = os.path.join(DECKS, self.slug + ".html")
        with io.open(out, "w", encoding="utf-8") as f:
            f.write(page)
        mb = os.path.getsize(out) / 1024.0 / 1024.0
        print("  %-36s %2d slides  %5.2f MB" % (self.slug + ".html", n, mb))
        return out


SHELL = u"""<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
:root{
  --paper:#FFFFFF; --edge:#DCDFDA; --edge2:#F0F2EE;
  --ink:#1A1D18; --ink2:#565C51; --ink3:#868C80;
  --accent:#A8321E; --plate:#22262A;
  --pad:clamp(30px,3.6vw,62px);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#161814; --edge:#31352D; --edge2:#22251E;
  --ink:#E7EAE3; --ink2:#A2A89C; --ink3:#787E72;
  --accent:#E4714E;}}
:root[data-theme="dark"]{
  --paper:#161814; --edge:#31352D; --edge2:#22251E;
  --ink:#E7EAE3; --ink2:#A2A89C; --ink3:#787E72;
  --accent:#E4714E;}

*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:20px;line-height:1.55;-webkit-font-smoothing:antialiased;}
h2,h3{margin:0;font-weight:700;letter-spacing:-.012em;text-wrap:balance}
code,.eyebrow,footer,.steps li b,th,.facts dt{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}

#deck{height:100vh;overflow-y:auto;scroll-snap-type:y mandatory;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){#deck{scroll-behavior:auto}}
.sheet{scroll-snap-align:start;min-height:100vh;display:flex}
.inner{flex:1;display:grid;grid-template-rows:auto 1fr auto;
  padding:var(--pad) var(--pad) 0;max-width:1760px;margin:0 auto;width:100%}

header{padding-bottom:26px;border-bottom:2px solid var(--ink);margin-bottom:34px}
.eyebrow{margin:0 0 10px;font-size:13px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--accent);font-weight:500}
h2{font-size:clamp(30px,3.5vw,46px);line-height:1.08}

.body{align-self:start;min-width:0}
.lede{font-size:clamp(21px,1.55vw,27px);line-height:1.45;color:var(--ink);
  max-width:44ch;margin:0 0 24px;font-weight:400}
.split .lede{max-width:34ch}
p{margin:0 0 .8em;max-width:52ch}
h3{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);
  margin:0 0 14px;font-weight:600}
strong{font-weight:700}
code{font-size:.88em;background:var(--edge2);border:1px solid var(--edge);
  padding:1px 6px;border-radius:3px;color:var(--accent)}

.split{display:grid;grid-template-columns:1.22fr 1fr;gap:clamp(28px,3.2vw,60px);
  align-items:start}
.split.even{grid-template-columns:1fr 1fr}
@media(max-width:1000px){.split{grid-template-columns:1fr;gap:26px}}

.shot{margin:0;display:flex;flex-direction:column}
.shot img{display:block;width:100%;aspect-ratio:4/3;object-fit:contain;
  background:var(--plate);border:1px solid var(--edge)}
.shot figcaption{font-size:15px;line-height:1.4;color:var(--ink2);padding-top:10px}
.shot.strip img{aspect-ratio:auto;height:auto;padding:8px 10px;object-fit:contain}
.shots{display:grid;gap:clamp(14px,1.5vw,24px)}
.shots.two{grid-template-columns:1fr 1fr}
.shots.three{grid-template-columns:repeat(3,1fr)}
@media(max-width:900px){.shots.two,.shots.three{grid-template-columns:1fr}}

.points{list-style:none;padding:0;margin:0 0 20px}
.points li{position:relative;padding-left:26px;margin-bottom:15px;max-width:50ch}
.points li:last-child{margin-bottom:0}
.points li::before{content:"";position:absolute;left:0;top:.62em;width:13px;height:2px;
  background:var(--accent)}
.steps{list-style:none;padding:0;margin:0 0 20px;counter-reset:s}
.steps li{counter-increment:s;position:relative;padding-left:44px;margin-bottom:16px;
  max-width:50ch}
.steps li:last-child{margin-bottom:0}
.steps li::before{content:counter(s);position:absolute;left:0;top:1px;
  width:28px;height:28px;display:grid;place-items:center;border-radius:50%;
  background:var(--ink);color:var(--paper);
  font-family:"IBM Plex Mono",monospace;font-size:14px;font-weight:500}
.steps li b{display:inline-block;margin-left:8px;font-weight:500;font-size:15px;
  color:var(--accent);background:var(--edge2);border:1px solid var(--edge);
  padding:1px 7px;border-radius:3px;white-space:nowrap}

table{width:100%;border-collapse:collapse;font-size:17px;margin:0 0 18px}
th{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);
  text-align:left;font-weight:500;border-bottom:2px solid var(--ink);
  padding:0 18px 9px 0;white-space:nowrap}
td{padding:11px 18px 11px 0;border-bottom:1px solid var(--edge);vertical-align:top;
  line-height:1.4}
tr:last-child td{border-bottom:0}

.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  gap:0;margin:26px 0 0;border-top:2px solid var(--ink)}
.facts>div{border-bottom:1px solid var(--edge);padding:12px 16px 12px 0}
.facts dt{font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);
  margin-bottom:4px}
.facts dd{margin:0;font-size:21px;font-weight:700;font-variant-numeric:tabular-nums}

.note,.warn{font-size:18px;line-height:1.45;color:var(--ink2);margin:20px 0 0;
  padding:14px 18px;border-left:3px solid var(--ink3);background:var(--edge2);
  max-width:54ch}
.warn{border-left-color:var(--accent)}
.note strong,.warn strong{color:var(--ink)}

.sheet.cover header{border-bottom-width:3px}
.sheet.cover h2{font-size:clamp(42px,6.2vw,86px);line-height:1.02;letter-spacing:-.03em}
.sheet.cover .lede{font-size:clamp(22px,1.8vw,30px);max-width:30ch}

footer{display:flex;justify-content:space-between;align-items:center;
  padding:18px 0 20px;margin-top:26px;border-top:1px solid var(--edge);
  font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3)}

#rail{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:40;
  display:flex;flex-direction:column;gap:2px;padding:8px 0 8px 8px}
#rail a{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink3);
  text-decoration:none;padding:2px 7px;border-left:2px solid transparent}
#rail a:hover{color:var(--ink)}
#rail a[aria-current="true"]{color:var(--accent);border-left-color:var(--accent)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media(max-width:1100px){#rail{display:none}}

@media print{
  @page{size:1600px 900px;margin:0}
  :root{--paper:#fff;--ink:#1A1D18;--ink2:#565C51;--ink3:#868C80;
        --edge:#DCDFDA;--edge2:#F0F2EE;--pad:44px}
  html,body{background:#fff;color:#1A1D18}
  body{font-size:17px}
  #deck{height:auto;overflow:visible}
  #rail{display:none}
  .sheet{min-height:900px;height:900px;overflow:hidden;
    page-break-after:always;break-after:page}
  .inner{padding:44px 52px 0}
  header{padding-bottom:18px;margin-bottom:24px}
  h2{font-size:34px}
  .sheet.cover h2{font-size:58px}
  .lede{font-size:20px;margin-bottom:18px}
  .sheet.cover .lede{font-size:22px}
  .points li,.steps li{margin-bottom:11px}
  table{font-size:14.5px}
  td{padding:8px 16px 8px 0}
  .facts dd{font-size:18px}
  .note,.warn{font-size:15px;padding:11px 15px;margin-top:16px}
  .shot figcaption{font-size:13px;padding-top:7px}
  footer{padding:12px 0 14px;margin-top:18px}
}
</style>
<nav id="rail" aria-label="Slides">__NAV__</nav>
<div id="deck">__BODY__</div>
<script>
(function(){
  var deck=document.getElementById('deck');
  var sheets=[].slice.call(deck.querySelectorAll('.sheet'));
  var links=[].slice.call(document.querySelectorAll('#rail a'));
  var cur=-1;
  function mark(i){ if(i===cur)return; cur=i;
    links.forEach(function(a,k){a.setAttribute('aria-current',k===i?'true':'false');}); }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting) mark(sheets.indexOf(e.target)); });
    },{root:deck,threshold:.5});
    sheets.forEach(function(s){io.observe(s);});
  }
  function go(i){ i=Math.max(0,Math.min(sheets.length-1,i));
    sheets[i].scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
    mark(i); }
  document.addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    var t=e.target.tagName; if(t==='INPUT'||t==='TEXTAREA')return;
    if(e.key==='ArrowDown'||e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();go(cur+1);}
    else if(e.key==='ArrowUp'||e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(cur-1);}
    else if(e.key==='Home'){e.preventDefault();go(0);}
    else if(e.key==='End'){e.preventDefault();go(sheets.length-1);}
  });
  links.forEach(function(a,k){a.addEventListener('click',function(e){e.preventDefault();go(k);});});
  mark(0);
})();
</script>
"""
