# -*- coding: utf-8 -*-
"""Deck 9 - Parts 6 and 7, the blades, and replacing SolidWorks Flex."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "06/07 BLADES"


def build():
    d = Deck("09-parts67-blades", "Parts 6 & 7 — The Blades")

    d.sheet("00", P, "OVERVIEW", "Parts 6 &amp; 7 — The Blades", """
<p class="lede">The sweeps that do the actual work: 13&nbsp;inch wide plates, 0.2&nbsp;inch
thick, swept back 13&deg; and curved. SolidWorks bends them with <strong>Flex</strong>.
FreeCAD has no Flex — and building them curved from the start turns out to be the better
model.</p>
""" + fig("06_blade01_final_Isometric", "BLADE 01",
          "13 in span, 4 in fore-and-aft, bent on a 10 in radius")
        + specs([("Span", "13 in"), ("Length", "4 in along the arc"),
                 ("Sheet", "0.2 in"), ("Edge sweep-back", "13&deg;"),
                 ("Blade 01 bend", "R10"), ("Blade 02 bend", "R16")]),
            eyebrow="Deck 9", kind="title")

    a = """
<h3>What Flex does</h3>
<p>SolidWorks' <strong>Flex ▸ Bending</strong> takes a finished flat solid and deforms it
about a trim plane. You give it an angle or a radius; it warps the body.</p>
""" + ticks([
        "It is a <em>direct modelling</em> operation, applied after the fact.",
        "The feature tree records &ldquo;bend this by &minus;10 in&rdquo;, not &ldquo;this "
        "plate has a 10 in radius&rdquo;.",
        "Change anything upstream and the bend re-applies to whatever it now finds."]) + \
        warn("<strong>FreeCAD has no equivalent.</strong> Not in Part Design, not in Part, "
             "not in Surface. There is no add-on that reproduces it faithfully. If you came "
             "looking for the Flex button, it is not there and it is not coming.")

    b = """
<h3>What we do instead</h3>
<p>Sweep the blade's <strong>section</strong> along an <strong>arc of the wanted
radius</strong>, then cut the plan shape out of the curved plate.</p>
""" + phases([("Spine",
               "An arc in the side view, radius R, starting horizontal at the cutting edge "
               "and lifting toward the back. Its arc length is the blade's 4 in."),
              ("Section",
               "A 13 &times; 0.2 in rectangle, square to the spine at its start."),
              ("Additive Pipe",
               "Sweeps one along the other. Result: a curved plate, 13 wide, 4 long, 0.2 "
               "thick."),
              ("Pocket",
               "Cuts the swept-back plan shape out of it, from a sketch looking straight "
               "down.")]) + \
        note("The bend radius is now a <strong>parameter of the geometry</strong>, not a "
             "deformation applied to it. That is the whole difference, and it pays off on "
             "the very next part.")

    d.sheet("01", P, "METHOD", "Replacing Flex ▸ Bending", """
<p class="lede">The one place where FreeCAD's missing feature forces a genuinely different
approach — and where the different approach is an improvement.</p>
""" + cols(a, b), eyebrow="Curved by construction")

    a2 = """
<h3>The spine</h3>
<p>One arc on <strong>YZ_Plane</strong>, and it needs four constraints to be fully
defined.</p>
""" + steps([("Draw an arc roughly where the blade goes", ""),
             ("<strong>Horizontal / vertical distance</strong> from the origin to its "
              "start point &mdash; puts the cutting edge at &minus;2 in", ""),
             ("<strong>Radius</strong>, bound to <code>Params.BendRadius</code>", "10 in"),
             ("<strong>Horizontal distance</strong> from the arc's start to its "
              "<em>centre</em> = 0 &mdash; this forces the centre directly above the "
              "start, so the arc leaves the cutting edge horizontally", ""),
             ("<strong>Horizontal distance</strong> to the end point, by expression", "")]) + \
        code("""
Params.SpineEnd
  = -BladeLength/2
    + BendRadius * sin(BladeLength / BendRadius * 1rad)
""")

    b2 = fig("06_blade_01_sketch_spine", "SPINE",
             "One arc, five constraints, fully constrained") + """
<h3>Why that expression</h3>
<p>We want the blade to be 4&nbsp;inches long <strong>measured along the curve</strong>,
not as a straight chord — because 4&nbsp;inches is how much steel it takes. Arc length
<var>s</var> = <var>R&theta;</var>, so <var>&theta;</var> = 4/<var>R</var>, and the end
point falls where that angle puts it.</p>
""" + note("Change <code>BendRadius</code> and the arc gets flatter but stays 4&nbsp;in "
           "long. The blade uses the same blank either way &mdash; which is exactly what "
           "would happen in a press shop.")

    d.sheet("02", P, "SPINE", "The arc the blade is bent on", """
<p class="lede">The curvature lives in one arc, and one spreadsheet cell drives it. That
cell is the whole reason Blade&nbsp;02 is free.</p>
""" + cols(a2, b2), eyebrow="Arc length, not chord")

    a3 = """
<h3>The section</h3>
<p>A 13&nbsp;&times;&nbsp;0.2&nbsp;in rectangle, on <strong>XZ_Plane</strong>, offset
2&nbsp;inches forward so it sits exactly on the spine's start point.</p>
""" + code("""
Sk_Section
  attach:  XZ_Plane
  offset:  z = Params.BladeLength / 2   (= 2 in, along the plane normal)
  rect:    13.0 x 0.2 in, centred
""") + note("XZ_Plane's normal points along &minus;Y, so an attachment offset of +2 puts "
            "the sketch at y = &minus;2 &mdash; the leading edge. Sign conventions on "
            "attachment offsets are worth checking once by looking at the resulting "
            "bounding box, rather than reasoning about them.")

    b3 = fig("06_blade_03_additive_pipe", "SWEPT",
             "A curved plate, before the plan shape is cut") + \
        specs([("Bounding box", "13 &times; 3.93 &times; 0.98 in"),
               ("Volume", "10.40 in&sup3;"),
               ("Rise at the back", "0.88 in")]) + \
        ticks([
            "3.93&nbsp;in fore-aft, not 4.00 &mdash; the 4&nbsp;in is measured round the "
            "curve, so the flat projection is slightly shorter. Correct.",
            "0.98&nbsp;in tall for a 0.2&nbsp;in sheet &mdash; the rest is the curvature. "
            "Correct."])

    d.sheet("03", P, "SWEEP", "Section along spine", """
<p class="lede">Sweep the rectangle along the arc and you have a curved plate. Check the
bounding box against what the arithmetic says before you go further.</p>
""" + cols(a3, b3), eyebrow="Check the bounding box")

    a4 = """
<h3>The plan shape</h3>
<p>A sweep is a duckfoot: it comes to a point in the middle and its cutting edges rake
back so soil and trash slide off rather than piling up.</p>
""" + code("""
13 deg sweep-back over a 6.5 in half-span

  rise = 6.5 x tan(13 deg) = 1.50 in

  the transcript's "1.5 inch gap"   <- confirmed
""") + """
<p>So the plan outline is five points: the centre tip 2&nbsp;in ahead, two leading corners
1.5&nbsp;in back from it at &plusmn;6.5&nbsp;in, and two trailing corners.</p>
""" + note("Two independently-stated numbers &mdash; 13&deg; and 1.5&nbsp;in &mdash; that "
           "agree to two decimal places. When that happens, you have read the source "
           "correctly.")

    b4 = """
<h3>Cutting it the other way round</h3>
<p>You cannot pocket &ldquo;everything outside this shape&rdquo; directly. The trick is two
wires in one sketch:</p>
""" + steps([("Sketch on <strong>XY_Plane</strong>", ""),
             ("Draw a large rectangle &mdash; bigger than the blade. This is the material "
              "to remove.", "19 x 10 in"),
             ("Draw the blade's plan outline <em>inside</em> it", ""),
             ("<strong>Pocket ▸ Through all</strong>, <strong>Symmetric to plane</strong>",
              "cuts up and down from the sketch")]) + \
        note("A pocket from two nested closed wires removes the ring between them, leaving "
             "the inner shape standing. Exactly the same trick made the frame's four "
             "members out of two rectangles in Deck 5.")

    d.sheet("04", P, "PLAN SHAPE", "The duckfoot", """
<p class="lede">13 degrees of sweep-back over a 6.5 inch half-span gives 1.5 inches of
rise — which is the number the transcript quotes. Confirmation that the reading is right.</p>
""" + cols(a4, b4) + plates([("06_blade_04_sketch_plan_shape", "SKETCH",
                              "Two wires: the stock rectangle and the blade outline. "
                              "9 lines, 25 constraints, fully constrained."),
                             ("06_blade_05_pocket_plan_shape", "POCKET",
                              "The corners fall away and the sweep appears")]),
            eyebrow="Two wires, one pocket")

    a5 = """
<h3>A redundant constraint that produced no shape</h3>
<p>First attempt at the plan sketch had both side lines constrained
<strong>Symmetric</strong> about the vertical axis <em>and</em> the trailing edge
constrained symmetric as well. The second one says nothing new.</p>
""" + code("""
  solve()  = -2
  redundant: [18, 19]
  sk.Shape.Wires -> 0          <- no wires at all
  Pocket_PlanShape ['Touched', 'Invalid']
""") + """
<p>Note what happened: the sketch <em>looked</em> perfectly correct on screen, and reported
<strong>DoF 0</strong>. But FreeCAD will not build a shape from a sketch it could not
cleanly solve, so the sketch had zero wires and the Pocket had nothing to cut with.</p>
""" + warn("<strong>When a Pad or Pocket fails and the sketch looks fine, read the solver "
           "message.</strong> &ldquo;Redundant constraints&rdquo; is not a warning you can "
           "ignore &mdash; downstream features stop working.")

    b5 = """
<h3>Blade 02: one cell</h3>
<p>Blade&nbsp;02 is Blade&nbsp;01 bent on 16&nbsp;inches instead of 10 &mdash; matching the
16&nbsp;in radius of the Tine&nbsp;02 it bolts to. In SolidWorks that means editing the
Flex feature. Here:</p>
""" + code("""
  Params.BendRadius:  10 in  ->  16 in
  recompute
""") + plates([("07_blade02_00_before_edit", "R10", "Blade 01"),
               ("07_blade02_01_after_edit", "R16", "Blade 02, same model")]) + \
        note("Same volume, same 13&nbsp;in span, same 4&nbsp;in of steel &mdash; just a "
             "flatter curve. The rise at the back drops from 0.88&nbsp;in to 0.59&nbsp;in.")

    d.sheet("05", P, "PAYOFF", "The failure, and the payoff", """
<p class="lede">One bug worth understanding, and then the moment the parametric approach
earns its keep.</p>
""" + cols(a5, b5), eyebrow="Why we built it curved")

    a6 = specs([("Span", "13 in"), ("Volume each", "8.45 in&sup3;"),
                ("Mass each", "2.4 lb"), ("9 blades", "21.6 lb"),
                ("Blade 01 height", "0.98 in"), ("Blade 02 height", "0.69 in")]) + """
<h3>What we did not model</h3>
""" + ticks([
        "<strong>Bolt holes.</strong> The transcript never dimensions them. Two &oslash;0.5 "
        "holes on the centreline would be the obvious addition &mdash; exercise 4 in "
        "Deck 14.",
        "<strong>The ground edge.</strong> A real sweep is sharpened on the underside of "
        "the leading edges. Modelling it needs a chamfer or a thin taper.",
        "<strong>Hardfacing.</strong> Wear parts are usually hardfaced along the leading "
        "edge; that is a material property, not geometry."])

    b6 = plates([("06_blade01_final_Isometric", "BLADE 01 — ISO", "R10"),
                 ("06_blade01_final_Right", "BLADE 01 — RIGHT", "the curve"),
                 ("07_blade02_final_Right", "BLADE 02 — RIGHT", "R16, flatter"),
                 ("06_blade01_final_Top", "PLAN", "13&deg; swept-back cutting edges")],
                "grid-2")

    d.sheet("06", P, "VERIFY", "Parts 6 and 7 complete", """
<p class="lede">Nine blades weigh 21.6&nbsp;lb between them — under 6% of the machine, and
the only parts that will ever need replacing.</p>
""" + cols(a6, b6), eyebrow="Check the numbers")

    return d
