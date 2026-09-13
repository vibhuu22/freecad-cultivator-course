# -*- coding: utf-8 -*-
"""Write the frame tutorial artboards (.dc.html) and canvas.json from one spec.

A straight stepwise tutorial: cover, orientation, nine numbered steps, finish.
One generator so every slide shares the same grid, type scale and rhythm.
Edit SLIDES, re-run, re-seed.
"""
import json, os, io

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900
DECK = "The Cultivator Frame"
NSTEPS = 9

PAPER   = "#F6F3ED"
INK     = "#191712"
INK2    = "#55503F"
INK3    = "#8C8674"
RULE    = "#DED7C8"
FAINT   = "#E7E0D1"
ACCENT  = "#B03A1B"
STEEL   = "#23272B"

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&amp;'
         'family=Public+Sans:wght@400;600&amp;'
         'family=DM+Mono:wght@500&amp;display=swap">')

STYLE = """
    * { box-sizing: border-box; }
    body { margin: 0; background: %(paper)s; }
    .slide {
      width: %(w)spx; height: %(h)spx; background: %(paper)s; color: %(ink)s;
      padding: 60px 80px 0; display: flex; flex-direction: column;
      font-family: "Public Sans", system-ui, sans-serif;
      font-size: 22px; line-height: 1.48;
    }
    .top {
      display: flex; justify-content: space-between; align-items: baseline;
      font-family: "DM Mono", ui-monospace, monospace; font-size: 15px;
      letter-spacing: .2em; text-transform: uppercase; color: %(ink3)s;
    }
    .top .where { color: %(accent)s; }
    .head { display: flex; align-items: baseline; gap: 30px; margin-top: 26px; }
    .numeral {
      font-family: "Bricolage Grotesque", Georgia, serif; font-weight: 800;
      font-size: 128px; line-height: .74; color: %(faint)s;
      letter-spacing: -.04em; flex: none;
    }
    h1 {
      font-family: "Bricolage Grotesque", Georgia, serif; font-weight: 800;
      font-size: 62px; line-height: 1.02; letter-spacing: -.028em; margin: 0;
      text-wrap: balance;
    }
    .rule { height: 3px; background: %(ink)s; margin-top: 26px; }
    .body { display: flex; gap: 64px; margin-top: 42px; flex: 1; min-height: 0; }
    .col-txt { flex: 1; display: flex; flex-direction: column; gap: 26px; min-width: 0; }
    .col-img { flex: 1.06; display: flex; flex-direction: column; gap: 14px; min-width: 0; }
    .card {
      background: %(steel)s; border-radius: 4px; padding: 10px;
      box-shadow: 0 20px 44px -26px rgba(25, 23, 18, .55);
    }
    .card img { width: 100%%; display: block; border-radius: 2px; }
    .caption { font-size: 17px; color: %(ink3)s; margin: 0; }
    .lede { font-size: 27px; line-height: 1.36; margin: 0; }
    .steps { display: flex; flex-direction: column; gap: 20px; margin: 0; }
    .step { display: flex; gap: 18px; align-items: flex-start; }
    .num {
      flex: none; width: 34px; height: 34px; border-radius: 50%%;
      background: %(ink)s; color: %(paper)s; display: flex;
      align-items: center; justify-content: center;
      font-family: "DM Mono", monospace; font-size: 16px; margin-top: 2px;
    }
    .step p { margin: 0; }
    .points { display: flex; flex-direction: column; gap: 18px; margin: 0; }
    .point { display: flex; gap: 17px; align-items: flex-start; }
    .dash { flex: none; width: 17px; height: 3px; background: %(accent)s; margin-top: 15px; }
    .point p { margin: 0; }
    .see {
      border-left: 4px solid %(accent)s; padding: 6px 0 6px 22px;
      background: linear-gradient(90deg, rgba(176, 58, 27, .05), rgba(176, 58, 27, 0) 60%%);
    }
    .see .tag {
      font-family: "DM Mono", monospace; font-size: 14px; letter-spacing: .17em;
      text-transform: uppercase; color: %(accent)s; margin: 0 0 8px;
    }
    .see p { margin: 0; color: %(ink2)s; font-size: 21px; }
    .facts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0; border-top: 3px solid %(ink)s; }
    .fact { padding: 17px 20px 17px 0; border-bottom: 1px solid %(rule)s; }
    .fact .k {
      font-family: "DM Mono", monospace; font-size: 14px; letter-spacing: .15em;
      text-transform: uppercase; color: %(ink3)s; margin: 0 0 5px;
    }
    .fact .v { font-family: "Bricolage Grotesque", serif; font-weight: 800;
      font-size: 30px; margin: 0; letter-spacing: -.015em; }
    strong { font-weight: 600; }
    a { color: %(accent)s; } a:hover { color: %(ink)s; }
    footer {
      margin-top: auto; padding: 20px 0 24px; display: flex;
      align-items: center; gap: 14px;
    }
    .dots { display: flex; gap: 9px; }
    .dot { width: 11px; height: 11px; border-radius: 50%%; background: %(faint)s; }
    .dot.on { background: %(accent)s; }
    .dot.done { background: %(ink3)s; }
    .foot-note {
      font-family: "DM Mono", monospace; font-size: 14px; letter-spacing: .15em;
      text-transform: uppercase; color: %(ink3)s; margin-left: auto;
    }
""" % dict(paper=PAPER, ink=INK, ink2=INK2, ink3=INK3, rule=RULE, faint=FAINT,
           accent=ACCENT, steel=STEEL, w=W, h=H)


def steps_html(items):
    rows = "".join(
        '<div class="step"><div class="num">%d</div><p>%s</p></div>' % (i + 1, t)
        for i, t in enumerate(items))
    return '<div class="steps">%s</div>' % rows


def points_html(items):
    return '<div class="points">%s</div>' % "".join(
        '<div class="point"><div class="dash"></div><p>%s</p></div>' % t
        for t in items)


def see_html(text, tag="You should see"):
    return '<div class="see"><p class="tag">%s</p><p>%s</p></div>' % (tag, text)


def facts_html(rows):
    return '<div class="facts">%s</div>' % "".join(
        '<div class="fact"><p class="k">%s</p><p class="v">%s</p></div>' % (k, v)
        for k, v in rows)


def dots_html(step):
    out = []
    for i in range(1, NSTEPS + 1):
        cls = "dot on" if i == step else ("dot done" if i < step else "dot")
        out.append('<div class="%s"></div>' % cls)
    return '<div class="dots">%s</div>' % "".join(out)


def artboard(s):
    step = s.get("step")
    numeral = ('<div class="numeral">%02d</div>' % step) if step else ""
    where = s.get("where", "")
    img = ""
    if s.get("image"):
        img = ('<div class="col-img"><div class="card">'
               '<img src="%s" alt="%s"></div><p class="caption">%s</p></div>'
               % (s["image"], s.get("alt", s["title"]), s.get("caption", "")))
    txt = '<div class="col-txt">%s</div>' % "".join(s["blocks"])
    body = ('<div class="body">%s%s</div>' % (txt, img) if img else
            '<div class="body"><div style="flex:1">%s</div></div>' % "".join(s["blocks"]))
    foot = ('%s<span class="foot-note">%s</span>'
            % (dots_html(step), "Step %d of %d" % (step, NSTEPS))) if step else \
           ('<span class="foot-note" style="margin-left:0">%s</span>' % DECK)
    return """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  %(fonts)s
  <style>%(style)s</style>
</helmet>
<div class="slide">
  <div class="top"><span>%(deck)s</span><span class="where">%(where)s</span></div>
  <div class="head">%(numeral)s<h1>%(title)s</h1></div>
  <div class="rule"></div>
  %(body)s
  <footer>%(foot)s</footer>
</div>
</x-dc>
</body>
</html>
""" % dict(fonts=FONTS, style=STYLE, deck=DECK, where=where, numeral=numeral,
           title=s["title"], body=body, foot=foot)


# --------------------------------------------------------------------- slides
SLIDES = [
 dict(file="Main", where="Part 1 of 7", title="The Cultivator Frame",
      image="01_frame_final_Isometric.jpg",
      caption="What you will have at the end of these nine steps",
      blocks=[
        '<p class="lede">A welded rectangle of square tube, drilled for nine '
        'tynes and fitted with a pair of brackets for the tractor hitch. '
        'Nine steps, start to finish.</p>',
        facts_html([("Overall", "82 &times; 22 in"), ("Tube", "2 in square"),
                    ("Wall", "3/16 in"), ("Bolt holes", "36"),
                    ("Brackets", "2"), ("Weight", "82 lb")]),
      ]),

 dict(file="WhatYouAreMaking", where="Orientation",
      title="What you are making",
      image="01_frame_final_Top.jpg",
      caption="Looking straight down on the finished frame",
      blocks=[
        points_html([
          "The two <strong>long bars</strong> run across the machine. Every "
          "tyne bolts to one of these.",
          "The two <strong>short bars</strong> close the ends and stop the "
          "frame twisting.",
          "<strong>Nine bolt stations</strong> along each long bar, 9.5 inches "
          "apart, so a tyne can go anywhere.",
          "A pair of <strong>brackets</strong> at the front, where the "
          "tractor's lower links pin on."]),
        see_html("Two inch square tube with a 3/16 inch wall is ordinary stock. "
                 "Any workshop can cut and weld it.", "Why these sizes"),
      ]),

 dict(file="SetUp", step=1, where="Getting started",
      title="Set up and start the file",
      image="01_frame_00_empty_document.jpg",
      caption="A new part, ready to draw in",
      blocks=[
        steps_html([
          "Open <strong>Edit &rsaquo; Preferences &rsaquo; General &rsaquo; "
          "Units</strong> and set the unit system to <strong>Imperial "
          "decimal</strong>.",
          "<strong>File &rsaquo; New</strong>.",
          "Change the workbench dropdown along the top to <strong>Part "
          "Design</strong>.",
          "Click <strong>Create body</strong>.",
          "Save the file and give it a name you will recognise later."]),
        see_html("The body listed on the left, its name in <strong>bold</strong>. "
                 "Everything you draw next goes inside it."),
      ]),

 dict(file="DrawOutline", step=2, where="The outline",
      title="Draw the outline",
      image="01_frame_03_sketch_plan_constrained.jpg",
      caption="Two rectangles. The gap between them is the steel.",
      blocks=[
        '<p class="lede">Seen from above, a tube frame is two rectangles, one '
        'inside the other.</p>',
        steps_html([
          "Click <strong>Create sketch</strong> and pick the <strong>XY "
          "plane</strong>.",
          "Draw a rectangle, roughly the right shape.",
          "Dimension it <strong>82 wide</strong> and <strong>22 deep</strong>.",
          "Draw a second rectangle inside it, <strong>78 by 18</strong>.",
          "Close the sketch."]),
        see_html("The lines turn <strong>green</strong>, and the panel reads "
                 "<em>fully constrained</em>."),
      ]),

 dict(file="GiveItHeight", step=3, where="First solid",
      title="Give it height",
      image="01_frame_04_pad_frame.jpg",
      caption="One command turns the outline into four bars",
      blocks=[
        steps_html([
          "Select the sketch.",
          "Click <strong>Pad</strong>.",
          "Enter <strong>2 inches</strong>.",
          "Click OK."]),
        see_html("All four bars, at once. You drew the two-inch gap between two "
                 "rectangles, and raising that gap made the frame."),
        '<p style="margin:0;color:%s">Draw the shape of the metal, then raise '
        'it. Nearly every part in this course is made this way.</p>' % INK2,
      ]),

 dict(file="HollowTube", step=4, where="The bore",
      title="Hollow out the tube",
      image="01_frame_05_pocket_tube_bore.jpg",
      caption="Invisible from outside, and worth 145 pounds",
      blocks=[
        '<p class="lede">Solid bar weighs 227 pounds. Real tube is hollow.</p>',
        steps_html([
          "Start a new sketch on the <strong>XY plane</strong>.",
          "In its properties, set the <strong>attachment offset</strong> so the "
          "sketch sits just below the top face.",
          "Draw two rectangles marking the inside of the tube walls.",
          "Click <strong>Pocket</strong> and cut down, stopping just above the "
          "bottom face."]),
        see_html("No change on screen. Check the weight instead &mdash; it "
                 "drops from 227 pounds to 82."),
      ]),

 dict(file="OneStation", step=5, where="Bolt holes",
      title="Drill one tyne station",
      image="01_frame_06_sketch_station_holes.jpg",
      caption="Four holes: one station on each bar",
      blocks=[
        '<p class="lede">Each tyne is held by two bolts, three inches apart.</p>',
        steps_html([
          "New sketch on the <strong>top face</strong> of the frame.",
          "Draw a circle <strong>half an inch</strong> across, near the "
          "left-hand end of the front bar.",
          "Draw a second circle <strong>three inches</strong> along, select "
          "both, and click <strong>Equal</strong>.",
          "Draw two more circles over the back bar. Select a front circle, its "
          "partner behind, and the horizontal axis, then click "
          "<strong>Symmetry</strong>.",
          "Click <strong>Pocket</strong> and cut <strong>through "
          "everything</strong>."]),
        see_html("Four holes. Symmetry keeps the back pair tied to the front "
                 "pair, so they stay in line."),
      ]),

 dict(file="NineStations", step=6, where="Bolt holes",
      title="Repeat it nine times",
      image="01_frame_08_linear_pattern_holes.jpg",
      caption="Thirty-six holes, from one command",
      blocks=[
        steps_html([
          "Select the <strong>pocket</strong> you just made.",
          "Click <strong>LinearPattern</strong>.",
          "Set the direction to run <strong>along the long bars</strong>.",
          "Set the mode to <strong>Extent</strong>, the length to "
          "<strong>76 inches</strong>, and the number to <strong>9</strong>.",
          "Click OK."]),
        see_html("Nine evenly spaced stations on both bars. The number includes "
                 "the one you already drew, so nine means nine in total."),
      ]),

 dict(file="HitchBrackets", step=7, where="The hitch",
      title="Add the hitch brackets",
      image="01_frame_11_pad_clevis_pair.jpg",
      caption="Two plates, straddling the front bar",
      blocks=[
        '<p class="lede">The tractor\'s lower links pin into a fork: two plates '
        'with a gap between them.</p>',
        steps_html([
          "New sketch on the <strong>YZ plane</strong>.",
          "Set its <strong>offset</strong> so it sits where the first plate "
          "face goes.",
          "Draw the plate outline, <strong>5 inches long, 3 inches tall</strong>.",
          "<strong>Pad</strong> it <strong>0.4 inches</strong>.",
          "Repeat on the far side of the gap, ticking <strong>Reversed</strong>."]),
        see_html("Two parallel plates with a <strong>1.5 inch gap</strong>, "
                 "sitting astride the front bar."),
      ]),

 dict(file="MirrorBrackets", step=8, where="The hitch",
      title="Pin hole, then mirror",
      image="01_frame_13_mirror_clevis.jpg",
      caption="Both brackets, 30 inches apart",
      blocks=[
        steps_html([
          "Sketch a <strong>1 inch</strong> circle midway between the two "
          "plates.",
          "<strong>Pocket</strong> it through everything, ticking "
          "<strong>Symmetric to plane</strong>.",
          "Select both pads and the pocket together.",
          "Click <strong>Mirrored</strong>, and pick the plane down the middle "
          "of the machine."]),
        see_html("A matching bracket on the other side. The two are now "
                 "<strong>30 inches</strong> apart, which is what the tractor "
                 "expects."),
      ]),

 dict(file="RoundNoses", step=9, where="Finishing",
      title="Round off the bracket noses",
      image="01_frame_14_fillet_clevis_nose.jpg",
      caption="Both corners of every bracket, rounded in one go",
      blocks=[
        steps_html([
          "Rotate the view so you can see the front of a bracket.",
          "Select the <strong>top and bottom corner edges</strong> of the nose "
          "&mdash; the ones running through the plate thickness.",
          "Do the same on the other three plates, holding "
          "<strong>Ctrl</strong> to add to the selection.",
          "Click <strong>Fillet</strong> and enter <strong>0.63 inches</strong>.",
          "Click OK."]),
        see_html("Eight rounded corners. Sharp corners on a hitch bracket are "
                 "where cracks start, so this is worth doing."),
      ]),

 dict(file="Finished", where="Done",
      title="The finished frame",
      image="01_frame_final_Isometric.jpg",
      caption="Part 1 complete, ready for the tynes",
      blocks=[
        '<p class="lede">Nine steps, six sketches, eight features. Confirm '
        'yours matches these numbers before you start the next part.</p>',
        facts_html([("Length", "82 in"), ("Depth", "22 in"),
                    ("With brackets", "25 in"), ("Bolt holes", "36"),
                    ("Bracket spacing", "30 in"), ("Weight", "82 lb")]),
        see_html("Nine tynes come next, then the blades and the braces. "
                 "Everything from here bolts onto what you have just built.",
                 "Coming next"),
      ]),
]

# --------------------------------------------------------------------- write
names = []
for s in SLIDES:
    fn = "%s.dc.html" % s["file"]
    with io.open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
        f.write(artboard(s))
    names.append(fn)
    print("wrote", fn)

COLS, GAP_X, GAP_Y = 4, 130, 150
boards = [dict(file=fn, x=(i % COLS) * (W + GAP_X), y=(i // COLS) * (H + GAP_Y),
               w=W, h=H) for i, fn in enumerate(names)]
with io.open(os.path.join(HERE, "canvas.json"), "w", encoding="utf-8") as f:
    json.dump(dict(artboards=boards, launch={"view": "canvas"}), f, indent=1)
print("wrote canvas.json  (%d artboards)" % len(boards))
