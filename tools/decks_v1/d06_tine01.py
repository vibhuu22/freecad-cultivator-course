# -*- coding: utf-8 -*-
"""Deck 6 - Part 2, Tine 01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "02 TINE 01"


def build():
    d = Deck("06-part2-tine01", "Part 2 — Tine 01")

    d.sheet("00", P, "OVERVIEW", "Part 2 — Tine 01", """
<p class="lede">The rigid front-rank tyne, five off. A straight shank, a smooth bend, and a
raked foot that carries the sweep. The whole shape is one sketch — and getting that sketch
fully constrained is the real lesson of this deck.</p>
""" + fig("02_tine01_final_Right", "RIGHT ELEVATION",
          "25 in overall along the shank; 15 in of it straight; 35&deg; rake below the bend")
        + specs([("Overall length", "25 in along the centreline"),
                 ("Straight shank", "15 in"),
                 ("Section", "2.25 &times; 1.5 in"),
                 ("Bend", "R6 inner, 35&deg;"),
                 ("Head", "5 &times; 2.25 &times; 1.25 in"),
                 ("Mass", "26.6 lb")]),
            eyebrow="Deck 6", kind="title")

    a = """
<h3>What the transcript gives us</h3>
""" + ticks([
        "&ldquo;Select the Right Plane&hellip; position the geometry at the centre of the "
        "origin point&rdquo;",
        "&ldquo;Length: 25 inches&rdquo;",
        "&ldquo;Dimension: 1.5 inches&rdquo; &mdash; the thickness across the machine",
        "&ldquo;Distance between the two points: 2.25 inches&rdquo; &mdash; the shank width",
        "&ldquo;The height between these two points is 15 inches&rdquo;",
        "&ldquo;Create a rectangle with a width of 5 inches and a height of 1.25 inches&rdquo;",
        "&ldquo;The hole size is 0.5 inches&hellip; the distance between the two holes will "
        "be 3 inches&hellip; mirror&rdquo;"]) + \
        note("The 3&nbsp;in bolt spacing and &oslash;0.5&nbsp;in holes are the same numbers "
             "the frame gave us. That is the confirmation that our reading of the frame "
             "was right.")

    b = """
<h3>Making the numbers consistent</h3>
<p>&ldquo;25 inches&rdquo; and &ldquo;15 inches&rdquo; are both stated. They are not in
conflict if you read 25 as the <strong>total length along the shank</strong> and 15 as the
<strong>straight part</strong> of it:</p>
""" + code("""
  straight shank            15.000 in
  bend arc, R7.125 x 35deg   4.352 in
  raked foot                 5.648 in
  ---------------------------------
  total along centreline    25.000 in
""") + warn("<strong>Assumptions:</strong> the 35&deg; rake and the R6 inner bend radius "
            "are ours &mdash; the transcript gives neither. Both are spreadsheet "
            "parameters. A rigid tyne typically rakes 25&ndash;45&deg;; steeper digs "
            "harder and pulls heavier.") + """
<h3>Where the origin goes</h3>
<p>At the centre of the <strong>mounting face</strong>, with the shank hanging into
negative Z. Placing the tyne in the assembly is then two numbers, x and y &mdash; z is
always zero.</p>
"""

    d.sheet("01", P, "READING THE SOURCE", "The shape, and the numbers", """
<p class="lede">A rigid tyne is a bent bar. The whole design is in its side profile, so
the whole modelling problem is in one sketch.</p>
""" + cols(a, b), eyebrow="25 and 15 both, not either")

    a2 = """
<h3>Eight pieces of geometry</h3>
<p>Drawn on <strong>YZ_Plane</strong> &mdash; SolidWorks' Right plane. Going round the
closed profile:</p>
""" + tbl(["#", "Geometry", "From &rarr; to"],
          [["1", "top edge", "front corner &rarr; rear corner, 2.25 in"],
           ["2", "rear edge", "straight down 15 in"],
           ["3", "<strong>outer arc</strong>", "R8.25, sweeping 35&deg;"],
           ["4", "rear of foot", "straight, 5.648 in"],
           ["5", "the point", "2.25 in, square to the foot"],
           ["6", "front of foot", "straight, back up"],
           ["7", "<strong>inner arc</strong>", "R6, concentric with #3"],
           ["8", "front edge", "straight up to the start"]]) + \
        note("Only <strong>one</strong> radius is dimensioned. The outer arc's R8.25 is not "
             "typed in anywhere &mdash; it follows from the inner arc being R6, the two "
             "being concentric, and the shank being 2.25 in wide. That is design intent "
             "expressed as geometry.")

    b2 = fig("02_tine01_02_sketch_profile", "SKETCH ON YZ",
             "8 pieces of geometry, 20 constraints, fully constrained") + \
        specs([("Geometry", "6 lines + 2 arcs"), ("DoF before", "34"),
               ("Constraints", "20"), ("DoF after", "0")])

    d.sheet("02", P, "SKETCH", "The profile", """
<p class="lede">Eight pieces of geometry, and every one of them tied down. Follow the
constraint list on the next sheet and you can reproduce it exactly.</p>
""" + cols(a2, b2), eyebrow="One sketch, the whole shape")

    a3 = """
<h3>The constraint list, in order</h3>
""" + steps([("<strong>Endpoint tangency</strong> at the four smooth joins: rear edge to "
              "outer arc, outer arc to foot, foot to inner arc, inner arc to front edge",
              "select the two endpoints, press T"),
             ("<strong>Coincident</strong> at the four sharp corners", "press C"),
             ("<strong>Horizontal</strong> on the top edge; <strong>Vertical</strong> on "
              "both the rear and front edges", ""),
             ("<strong>Coincident</strong> on the two arc <em>centres</em> &mdash; this "
              "makes them concentric", ""),
             ("<strong>Perpendicular</strong>: the point face to the rear of the foot", ""),
             ("<strong>Parallel</strong>: the two sides of the foot", ""),
             ("<strong>Symmetric</strong>: the two ends of the top edge about the origin "
              "point &mdash; centres the whole profile", ""),
             ("Dimensions: width 2.25, shank 15, inner radius 6, foot length 5.648, "
              "forward reach 3.606", "")])

    b3 = """
<h3>Two constraints that are easy to miss</h3>
""" + ticks([
        "<strong>Parallel on the foot sides.</strong> Without it the sketch sits at 1 "
        "degree of freedom: the inner arc's end angle is free, so the front of the foot "
        "can swing. Tangency alone does not pin it &mdash; tangency to a circle holds at "
        "whatever point you slide to.",
        "<strong>Symmetric about the origin <em>point</em></strong> (not an axis). "
        "Selecting the two top corners and the origin, then pressing S, centres the profile "
        "in both x and y at once &mdash; two degrees of freedom for one constraint."]) + \
        warn("<strong>Do not add a Coincident at a tangent join.</strong> Endpoint "
             "tangency already implies coincidence. Adding both gives "
             "<code>solve() = -3</code>, <em>conflicting constraints</em>, and a sketch "
             "that produces no shape at all &mdash; so the Pad then fails with a confusing "
             "message about a missing profile. See Deck 4.")

    d.sheet("03", P, "CONSTRAINTS", "Tying it down, step by step", """
<p class="lede">Twenty constraints take 34 degrees of freedom to zero. Two of them are the
ones beginners leave out.</p>
""" + cols(a3, b3), eyebrow="The full recipe")

    a4 = """
<h3>Why the rake is not an angle</h3>
<p>The obvious way to dimension the foot is an <strong>Angle</strong> constraint: 35&deg;
between the shank and the foot. It solves &mdash; to the wrong shape.</p>
""" + code("""
Angle(rear edge, foot, 35 deg)
  fully constrained,  DoF 0,  no conflicts
  tip at  (+2.872, -14.894)      <- raked BACKWARDS

DistanceX(origin, foot end) = -3.606
  fully constrained,  DoF 0,  no conflicts
  tip at  (-3.606, -24.358)      <- correct
""") + """
<p>&ldquo;These two lines are 35&deg; apart&rdquo; is true of both the forward-raked tyne
and its mirror image. The solver has no way to know which you meant, and it does not
always keep the one you drew.</p>
"""

    b4 = """
<h3>Reach is the better dimension anyway</h3>
<p>&ldquo;How far forward does the point reach?&rdquo; is a question about the machine.
&ldquo;What is the included angle at the bend?&rdquo; is a question about the drawing.</p>
""" + code("""
Params.FootReach
  = -(ShankWidth/2 + BendRadius)
    + (BendRadius + ShankWidth) * cos(Rake)
    - FootLength * sin(Rake)
  = -3.606 in
""") + note("The rake angle is still a named parameter &mdash; it just drives the reach "
            "through a formula rather than being applied directly. Change "
            "<code>Rake</code> to 30&deg; and the tyne re-rakes, unambiguously.") + \
        warn("<strong>General rule:</strong> when a constraint has more than one valid "
             "solution, find one that does not. Distances are almost always safer than "
             "angles.")

    d.sheet("04", P, "SOLVER TRAP", "The angle constraint that flipped the tyne", """
<p class="lede">This one cost real time. It is worth understanding properly because it will
happen to you on some other part.</p>
""" + cols(a4, b4), eyebrow="Two answers, one wanted")

    a5 = """
<h3>Pad the shank</h3>
""" + steps([("Select the profile sketch", ""),
             ("<strong>Part Design ▸ Pad</strong>", ""),
             ("Length <code>Params.ShankThk</code>", "1.5 in"),
             ("Tick <strong>Symmetric to plane</strong> &mdash; 0.75 in each side of YZ",
              "SolidWorks calls this Mid Plane"),
             ("OK", "84.4 in&sup3;")]) + \
        note("Symmetric matters for the assembly: the tyne is then centred on the plane you "
             "position it with, so the placement x is the tyne's centreline. Pad it one-way "
             "and every placement carries a 0.75 in correction you will eventually forget.")

    b5 = """
<h3>Pad the mounting head</h3>
""" + steps([("New sketch on <strong>XY_Plane</strong> &mdash; the mounting face", ""),
             ("Centred rectangle, 5 in along the bar &times; 2.25 in fore-aft", ""),
             ("Bind the 2.25 to <code>Params.ShankWidth</code> so the head always matches "
              "the shank", ""),
             ("<strong>Pad</strong> 1.25 in, <strong>Reversed</strong> &mdash; downward, "
              "into the shank", "")]) + \
        fig("02_tine01_04_pad_head", "PAD HEAD",
            "The head is 5 in wide so two bolts at 3 in centres fit; the shank is only "
            "1.5 in thick")

    d.sheet("05", P, "PAD", "Shank and head", """
<p class="lede">Two pads. The first makes the tyne; the second widens the top so it can be
bolted down.</p>
""" + cols(a5, b5) + plates([("02_tine01_03_pad_shank", "SHANK", "1.5 in, symmetric"),
                             ("02_tine01_04_pad_head", "HEAD ADDED",
                              "The two fuse into one solid")]),
            eyebrow="From profile to solid")

    a6 = """
<h3>Bolt holes</h3>
""" + steps([("Sketch on <strong>XY_Plane</strong> &mdash; the mounting face again", ""),
             ("&oslash;0.5 circle at <code>-BoltSpacing/2</code>", "= -1.5 in"),
             ("Second circle, <strong>Symmetric</strong> about the <strong>Y "
              "axis</strong>, plus <strong>Equal</strong>", ""),
             ("<strong>Pocket ▸ Through all</strong>", "")]) + \
        note("The transcript says &ldquo;blind, 0.4 inches&rdquo;. A blind hole cannot take "
             "a through bolt, and the frame it bolts to is drilled right through &mdash; so "
             "we make it Through all and note the change. The 0.4 is most likely a "
             "counterbore that the translation lost.")

    b6 = fig("02_tine01_05_sketch_bolt_holes", "SKETCH",
             "Two circles, one Symmetric, one Equal, one diameter &mdash; fully constrained") + \
        fig("02_tine01_06_pocket_bolt_holes", "POCKET",
            "Through the 1.25 in head, clear of the 1.5 in shank")

    d.sheet("06", P, "POCKET", "The mounting bolts", """
<p class="lede">Two holes at 3&nbsp;in centres — the same 3&nbsp;in that appears in the
frame. This is the joint that holds the machine together.</p>
""" + cols(a6, b6), eyebrow="The interface to Part 1")

    a7 = specs([("Sketches", "3"), ("Features", "3"), ("Volume", "93.7 in&sup3;"),
                ("Mass", "26.6 lb"), ("&times; 5 off", "133 lb"),
                ("Bounding box", "5 &times; 6.57 &times; 24.36 in")]) + """
<h3>Sanity checks</h3>
""" + ticks([
        "Height 24.36 in &mdash; less than the 25 in shank length, because the shank curves "
        "forward. Correct.",
        "Depth 6.57 in &mdash; the 2.25 in section plus the forward reach. Correct.",
        "Width exactly 5.00 in &mdash; the head. Correct.",
        "Five tynes weigh 133 lb, a third of the machine. Worth knowing before you specify "
        "a tractor."])

    b7 = plates([("02_tine01_final_Isometric", "ISOMETRIC", ""),
                 ("02_tine01_final_Right", "RIGHT", "the profile you drew"),
                 ("02_tine01_final_Front", "FRONT", "1.5 in shank, 5 in head"),
                 ("02_tine01_final_Top", "PLAN", "")], "grid-2")

    d.sheet("07", P, "VERIFY", "Part 2 complete", """
<p class="lede">Three sketches, three features, 27&nbsp;lb of steel. Check the bounding box
against what you expect before moving on.</p>
""" + cols(a7, b7), eyebrow="Check the numbers")

    return d
