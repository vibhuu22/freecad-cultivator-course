# -*- coding: utf-8 -*-
"""Deck 7 - Part 3, Tine 02."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "03 TINE 02"


def build():
    d = Deck("07-part3-tine02", "Part 3 — Tine 02")

    d.sheet("00", P, "OVERVIEW", "Part 3 — Tine 02", """
<p class="lede">The curved C-tyne, four off, for the rear rank. Where Tine&nbsp;01 is
straight-bend-straight, this one is a single continuous sweep on a 16&nbsp;inch radius. It
is a simpler sketch, and it introduces deriving a dimension from other dimensions.</p>
""" + fig("03_tine02_final_Right", "RIGHT ELEVATION",
          "One arc, 16 in centreline radius, sweeping 69.6&deg; to a rounded point")
        + specs([("Curve radius", "16 in on the centreline"),
                 ("Working height", "15 in"),
                 ("Sweep", "69.6&deg; (derived)"),
                 ("Section", "2.5 &times; 1.25 in"),
                 ("Point radius", "R1"),
                 ("Mass", "22.1 lb")]),
            eyebrow="Deck 7", kind="title")

    a = """
<h3>What the transcript gives us</h3>
""" + ticks([
        "&ldquo;Select the Right Plane and create a line&hellip; a midpoint line&rdquo;",
        "&ldquo;The height from this point to this point is 2 inches, and the height on the "
        "other side is also 2 inches&rdquo;",
        "&ldquo;The gap between the two sides is 2.5 inches&rdquo;",
        "&ldquo;We will use a radius of 16 inches on both sides&rdquo;",
        "&ldquo;From this point to the midpoint of the outer arc: 20.3 inches&rdquo;",
        "&ldquo;The height from this point to this point is 15 inches&rdquo;",
        "&ldquo;Apply a 1-inch radius to this corner&rdquo;",
        "&ldquo;The thickness will be 1.25 inches&rdquo;"])

    b = """
<h3>Do the numbers agree?</h3>
<p>Three of these over-specify the same arc: a 16&nbsp;in radius, a 15&nbsp;in working
height, and a 20.3&nbsp;in chord. Check them against each other before drawing anything.</p>
""" + code("""
Take R = 16 and working height = 15:

  sweep  = asin(15 / 16)          = 69.64 deg
  outer radius = 16 + 2.5/2       = 17.25 in
  chord across the outer arc
         = 2 x 17.25 x sin(69.64/2) = 19.70 in

  transcript says                  20.3 in
  difference                        0.6 in  (3%)
""") + note("Three independently-quoted numbers agreeing to 3% is a strong signal that the "
            "reading is right. We drive the model from radius and working height &mdash; "
            "the two clean numbers &mdash; and treat 20.3 as the check, not the input.")

    d.sheet("01", P, "READING THE SOURCE", "Three numbers, one arc", """
<p class="lede">This part is over-dimensioned in the source. That is a gift: it lets you
verify your interpretation before you commit to it.</p>
""" + cols(a, b), eyebrow="Cross-check before you draw")

    a2 = """
<h3>Six pieces of geometry</h3>
""" + tbl(["#", "Geometry", "Note"],
          [["1", "top edge", "2.5 in, centred on the origin"],
           ["2", "rear edge", "vertical, 2 in &mdash; the straight bit before the curve"],
           ["3", "<strong>outer arc</strong>", "R17.25, sweeping 69.6&deg;"],
           ["4", "the point", "2.5 in, <strong>radial</strong> to the arcs"],
           ["5", "<strong>inner arc</strong>", "R14.75, concentric"],
           ["6", "front edge", "vertical, back up to the top"]]) + """
<h3>The one unusual constraint</h3>
<p>The point face has to be <strong>radial</strong> &mdash; square across the bar, not at
some arbitrary angle. Rather than an angle constraint, use
<strong>Point&nbsp;on&nbsp;object</strong>: the arcs' shared <em>centre point</em> must lie
on the point-face line. A line through the centre of a circle is radial by definition.</p>
"""

    b2 = fig("03_tine02_01_sketch_profile", "SKETCH ON YZ",
             "6 pieces of geometry, 16 constraints, fully constrained on the first attempt") + \
        specs([("Geometry", "4 lines + 2 arcs"), ("Constraints", "16"), ("DoF", "0")]) + \
        note("Compare with Tine 01: eight pieces and twenty constraints for a shape that "
             "is arguably less elegant. A single arc is both easier to model and easier to "
             "forge.")

    d.sheet("02", P, "SKETCH", "One arc does the whole job", """
<p class="lede">Two concentric arcs and four lines. The bar keeps a constant 2.5&nbsp;inch
width all the way round because the arcs share a centre.</p>
""" + cols(a2, b2), eyebrow="Simpler than Tine 01")

    a3 = """
<h3>Derived parameters</h3>
<p>Three of this part's cells are formulas, not numbers. They are computed from the
designer's real choices &mdash; radius, working height, bar width.</p>
""" + code("""
CurveRadius   16 in            <- design choice
WorkHeight    15 in            <- design choice
BarWidth      2.5 in           <- design choice

Sweep       = asin(WorkHeight / CurveRadius)
OuterR      = CurveRadius + BarWidth / 2
TipDrop     = -(TopStraight + OuterR * sin(Sweep))
""") + """
<p>The sketch then dimensions the outer arc with <code>Params.OuterR</code> and the point's
height with <code>Params.TipDrop</code>. No number in the sketch was worked out by hand.</p>
"""

    b3 = fig("03_tine02_00_params", "SPREADSHEET",
             "Thirteen cells; three of them formulas") + """
<h3>Why bother?</h3>
""" + ticks([
        "Change <code>WorkHeight</code> to 12 in and the sweep, the outer radius and the "
        "point height all recompute. The tyne stays a proper arc.",
        "Change <code>BarWidth</code> and the two arc radii move apart correctly &mdash; "
        "you cannot accidentally end up with a bar that changes width along its length.",
        "The formulas <em>are</em> the design rationale. Anyone opening the file can see "
        "that the sweep is a consequence of depth and radius, not an arbitrary 69.6&deg;."]) + \
        warn("FreeCAD's expression engine handles units. <code>asin(15 in / 16 in)</code> "
             "gives an angle, and <code>sin()</code> of that angle gives a plain number. "
             "Mixing them up is one of the few ways to get an error here &mdash; the "
             "message names the offending cell.")

    d.sheet("03", P, "EXPRESSIONS", "Deriving the sweep angle", """
<p class="lede">The sweep angle is not a design decision. It follows from the radius and
the working depth, so the spreadsheet should compute it — not you.</p>
""" + cols(a3, b3), eyebrow="Let the model do the arithmetic")

    a4 = """
<h3>Pad, head, holes</h3>
""" + steps([("<strong>Pad</strong> the profile 1.25 in, <strong>Symmetric to plane</strong>",
              "Params.BarThk"),
             ("Sketch the head on <strong>XY_Plane</strong>: 5 in &times; 2.5 in, centred",
              "width bound to Params.BarWidth"),
             ("<strong>Pad</strong> 1.25 in <strong>Reversed</strong>", ""),
             ("Sketch two &oslash;0.5 circles at 3 in centres, Symmetric about the Y axis",
              "identical to Tine 01"),
             ("<strong>Pocket ▸ Through all</strong>", "")]) + \
        note("<strong>The interface is deliberately identical to Tine 01.</strong> Same "
             "5 in head, same 3 in bolt centres, same &oslash;0.5. Either tyne fits any of "
             "the eighteen stations on the frame &mdash; which is how a real cultivator "
             "works, and it costs nothing to design in.")

    b4 = plates([("03_tine02_02_pad_shank", "PAD SHANK", "1.25 in, symmetric"),
                 ("03_tine02_03_pad_head", "PAD HEAD", "5 in wide mounting head"),
                 ("03_tine02_04_pocket_bolt_holes", "POCKET", "two &oslash;0.5 at 3 in centres"),
                 ("03_tine02_05_fillet_point", "FILLET R1", "the point, rounded")], "grid-2")

    d.sheet("04", P, "FEATURES", "From profile to part", """
<p class="lede">Four features, and three of them are exactly what you did on Tine&nbsp;01.
Reusing an interface is a design decision worth making deliberately.</p>
""" + cols(a4, b4), eyebrow="Same interface, different shank")

    a5 = """
<h3>Rounding the point</h3>
<p>The transcript asks for a 1&nbsp;in radius on the corner. On a 2.5&nbsp;in wide bar, R1
on both corners of the point face very nearly makes it a semicircle &mdash; which is what
a worn or forged tyne point actually looks like.</p>
""" + steps([("Select the two edges running through the bar thickness at the point", ""),
             ("<strong>Part Design ▸ Fillet</strong>", ""),
             ("Radius <code>Params.TipRadius</code>", "1 in"),
             ("OK", "78.25 -> 77.71 in&sup3;")]) + \
        warn("<strong>Picking edges by eye is fine once.</strong> It is not repeatable, "
             "and a change upstream can renumber them. If you script this, select edges by "
             "<em>where they are</em> &mdash; the build script finds edges parallel to X "
             "whose vertices sit at the point &mdash; not by their index.")

    b5 = fig("03_tine02_05_fillet_point", "R1 AT THE POINT",
             "Both corners rounded in one feature") + """
<h3>Why round it at all?</h3>
""" + ticks([
        "A sharp corner on a wear part is a stress raiser and a crack starter.",
        "It is where the sweep bolts on; a rounded seat spreads the load.",
        "In soil, a sharp corner wears to a round one within an hour anyway. Model what "
        "the part becomes, not what leaves the forge."])

    d.sheet("05", P, "FILLET", "The point", """
<p class="lede">One dress-up feature, applied last — and a note on why picking edges by
index is a habit worth breaking.</p>
""" + cols(a5, b5), eyebrow="Dress-up goes last")

    a6 = specs([("Sketches", "3"), ("Features", "4"), ("Volume", "77.7 in&sup3;"),
                ("Mass", "22.1 lb"), ("&times; 4 off", "88 lb"),
                ("Bounding box", "5 &times; 11.84 &times; 17.86 in")]) + """
<h3>Tine 01 against Tine 02</h3>
""" + tbl(["", "Tine 01", "Tine 02"],
          [["Rank", "front, 5 off", "rear, 4 off"],
           ["Shape", "straight + bend + foot", "one continuous arc"],
           ["Section", "2.25 &times; 1.5 in", "2.5 &times; 1.25 in"],
           ["Height", "24.4 in", "17.9 in"],
           ["Forward reach", "3.6 in", "10.4 in"],
           ["Mass each", "26.6 lb", "22.1 lb"],
           ["Sketch geometry", "8 pieces", "6 pieces"]])

    b6 = plates([("03_tine02_final_Isometric", "ISOMETRIC", ""),
                 ("03_tine02_final_Right", "RIGHT", "the arc, as drawn"),
                 ("03_tine02_final_Front", "FRONT", "1.25 in bar, 5 in head"),
                 ("03_tine02_final_Top", "PLAN", "10.4 in of forward reach")], "grid-2") + \
        note("The rear tyne reaches 10.4&nbsp;in forward against the front tyne's 3.6&nbsp;in. "
             "Mounted 20&nbsp;in apart on the two bars, that puts the two ranks of points "
             "about 13&nbsp;in apart fore-and-aft &mdash; enough for trash to clear between "
             "them.")

    d.sheet("06", P, "VERIFY", "Part 3 complete", """
<p class="lede">Two tynes, two different philosophies, one shared bolt interface.
Nine tynes now weigh 221&nbsp;lb between them.</p>
""" + cols(a6, b6), eyebrow="Check the numbers")

    return d
