# -*- coding: utf-8 -*-
"""Deck 8 - Parts 4 and 5, the clamps."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "04/05 CLAMPS"


def build():
    d = Deck("08-parts45-clamps", "Parts 4 & 5 — The Clamps")

    d.sheet("00", P, "OVERVIEW", "Parts 4 &amp; 5 — The Clamps", """
<p class="lede">Two bent straps, 3&nbsp;inches wide and half an inch thick. The tutorial
draws a centreline, rounds the corners, then uses <em>Offset Entities</em> to thicken it
into a strap. FreeCAD gets there a different way — and the way it gets there is the same
tool the blades need.</p>
""" + plates([("04_clamp01_final_Isometric", "CLAMP 01",
               "18 in rise, 7 in at 45&deg;, 4 in return &mdash; 12.2 lb"),
              ("05_clamp02_final_Isometric", "CLAMP 02",
               "26.6 in rise, 6 in at 30&deg; &mdash; 13.8 lb")])
        + specs([("Section", "3 &times; 0.5 in"), ("Corner radius", "R2"),
                 ("Hole", "&oslash;1 in through"), ("Off", "2 of each"),
                 ("Method", "Additive Pipe")]),
            eyebrow="Deck 8", kind="title")

    a = """
<h3>The SolidWorks route</h3>
""" + steps([("Draw the bent centreline: 4 in, 18 in straight, 7 in, 45&deg;", ""),
             ("<strong>Sketch Fillet</strong>, R2, on the corners", ""),
             ("<strong>Offset Entities</strong>, 0.5 in, toward the inside", ""),
             ("Close the sketch at both ends &mdash; it is now a closed 0.5 in ribbon", ""),
             ("<strong>Boss-Extrude</strong> 3 in", "")], compact=True) + \
        warn("<strong>FreeCAD has Sketcher Offset</strong> &mdash; it is on the Sketcher "
             "tools menu and it works. What it does not have is a <em>scriptable</em> "
             "offset, and more importantly the offset result is dumb geometry: it does not "
             "stay attached to the centreline you offset it from.")

    b = """
<h3>The FreeCAD route: sweep it</h3>
""" + steps([("Sketch the bent <strong>path</strong> on YZ &mdash; three lines, "
              "fully constrained", ""),
             ("<strong>Sketcher fillet</strong> the two corners, R2", ""),
             ("Sketch the <strong>section</strong> on XY at the start of the path: a "
              "3 &times; 0.5 in rectangle", ""),
             ("<strong>Part Design ▸ Additive pipe</strong>: profile = the section, "
              "spine = the path", "")], compact=True) + """
<p>Same solid, and now the model knows the strap's <em>section</em> and its
<em>path</em> as separate, named things. Change the section to 4&nbsp;&times;&nbsp;0.375
and the strap re-sweeps along the same path.</p>
""" + note("This is FreeCAD's stand-in for <strong>Weldments ▸ Structural Member</strong> "
           "too. Sweep a section along a path is exactly what a structural member is. What "
           "you lose is the automatic cut list and mitred joints.")

    d.sheet("01", P, "METHOD", "Offset Entities, or a sweep?", """
<p class="lede">Two ways to turn a line into a strap. One of them keeps the design intent;
the other throws it away.</p>
""" + cols(a, b), eyebrow="Additive Pipe replaces two SolidWorks tools")

    a2 = """
<h3>The path, fully constrained</h3>
<p>Three lines from the origin. Because each segment is dimensioned by its
<strong>&Delta;x and &Delta;y</strong> rather than by a length and an angle, there is no
ambiguity for the solver to get wrong.</p>
""" + code("""
Clamp 01 path
  (0, 0)  -> (0, 18)                  vertical, 18 in
          -> (-4.95, 22.95)           7 in at 45 deg
          -> (-8.95, 22.95)           horizontal, 4 in

  3 lines, 9 constraints, fully constrained
""") + steps([("Draw three connected lines", ""),
              ("<strong>Coincident</strong> the first point to the origin", ""),
              ("<strong>Vertical</strong> on the first, <strong>Horizontal</strong> on "
               "the last", ""),
              ("Dimension each segment's run and rise", "")], compact=True)

    b2 = fig("04_clamp01_01_sketch_path", "PATH SKETCH",
             "Three lines and two R2 fillets. The construction points at the virtual "
             "corners keep the 18 / 7 / 4 dimensions meaningful.") + \
        warn("<strong>Fillet with 'create corner' ticked.</strong> A sketch fillet trims "
             "the two lines back, so the 18&nbsp;in dimension would suddenly measure the "
             "<em>trimmed</em> line. Ticking <em>create corner</em> leaves a construction "
             "point at the original intersection and re-attaches the dimensions to it. "
             "Without it, your stated dimensions quietly stop meaning what they say.")

    d.sheet("02", P, "PATH", "Sketching the bend", """
<p class="lede">Nine constraints for three lines. Then two fillets — and one checkbox that
decides whether your dimensions still mean anything afterwards.</p>
""" + cols(a2, b2), eyebrow="Create corner, always")

    a3 = """
<h3>The fillet leaves a loose end</h3>
<p><code>sk.fillet()</code> creates the arc and constrains it tangent to both lines &mdash;
but it does <strong>not</strong> dimension its radius. The sketch drops from fully
constrained to one degree of freedom per fillet.</p>
""" + code("""
  path before fillets: 3 geometry, 9 constraints, FULLY CONSTRAINED
  path after fillets:  7 geometry, 15 constraints, DoF 2        <-

  add Radius on each new arc, bound to Params.CornerR

  path after fillets:  7 geometry, 17 constraints, FULLY CONSTRAINED
""") + note("The GUI behaves the same way. After filleting, look at the Sketcher's "
            "degrees-of-freedom message and dimension the new arcs. It is the single most "
            "commonly forgotten step in the whole of Sketcher.")

    b3 = """
<h3>The section, and where it sits</h3>
<p>An Additive Pipe needs the profile positioned <strong>at the start of the spine and
square to it</strong>. Our path starts at the origin heading straight up, so the section
goes on <strong>XY_Plane</strong>, centred on the origin. No offset, no datum.</p>
""" + fig("04_clamp01_02_sketch_section", "SECTION SKETCH",
          "3 in across the machine, 0.5 in in the plane of the bend") + \
        ticks([
            "Choosing a path that starts at the origin, along an axis, is not laziness "
            "&mdash; it is what makes the section sketch trivial.",
            "If the path had started at an angle you would need a datum plane normal to "
            "it, and every edit would become fiddly.",
            "Design the path around the convenience of the section. It costs nothing."])

    d.sheet("03", P, "SECTION", "Dimension the fillets, place the section", """
<p class="lede">Two small things that both cause trouble: the radius a fillet does not
constrain, and getting the sweep section square to the path.</p>
""" + cols(a3, b3), eyebrow="The forgotten radius")

    a4 = """
<h3>Running the sweep</h3>
""" + steps([("Select the <strong>section</strong> sketch", ""),
             ("<strong>Part Design ▸ Additive pipe</strong>", ""),
             ("In the dialog, click <strong>Object</strong> under Path and pick the "
              "<strong>path</strong> sketch", ""),
             ("Mode: <strong>Standard</strong> &mdash; the section keeps its orientation "
              "relative to the path", ""),
             ("OK", "43.24 in&sup3;")]) + \
        tbl(["Mode", "Does"],
            [["<strong>Standard</strong>", "section rotates with the path. What you want "
              "almost always."],
             ["Fixed", "section keeps its world orientation &mdash; the strap would twist "
              "flat at the bends."],
             ["Frenet", "uses the curve's natural frame. Matters for 3D paths; ours is "
              "planar, so it makes no difference."]])

    b4 = plates([("04_clamp01_03_additive_pipe", "CLAMP 01 SWEPT",
                  "One feature: 3 &times; 0.5 in strap along the whole bent path"),
                 ("04_clamp01_04_pocket_hole", "&oslash;1 HOLE",
                  "Sketched on XZ, Through all, Symmetric &mdash; drilled across the strap")]) + \
        note("The R2 corners come out as proper swept bends with no separate fillet "
             "feature. Bends made <em>by construction</em> rather than added afterwards is "
             "the theme that carries straight into the blades.")

    d.sheet("04", P, "ADDITIVE PIPE", "Sweeping the strap", """
<p class="lede">One feature turns a line and a rectangle into a bent strap with rounded
corners.</p>
""" + cols(a4, b4), eyebrow="Section along path")

    a5 = """
<h3>Clamp 02 is the same recipe</h3>
""" + code("""
Clamp 01     (0,0) -> (0, 18.0)   -> 7 in at 45 deg -> 4 in horizontal
Clamp 02     (0,0) -> (0, 26.6)   -> 6 in at 30 deg

same section    3 x 0.5 in
same fillet     R2
same hole       dia 1 in, 4 in up from the foot
""") + """
<p>Two lines of difference in the path sketch. Everything else &mdash; the section, the
sweep, the hole, the parameter names &mdash; is identical, which is why one build script
produces both.</p>
""" + plates([("05_clamp02_01_sketch_path", "CLAMP 02 PATH", "Two lines, one R2 fillet"),
              ("05_clamp02_final_Right", "CLAMP 02", "26.6 in tall, 30&deg; tip")])

    b5 = """
<h3>What these parts actually do</h3>
""" + warn("<strong>Assumption &mdash; and a significant one.</strong> The transcript calls "
           "these &ldquo;the attachment clamp&rdquo; but never says what they attach to, "
           "and never mates them in the assembly. We model the dimensions it gives and "
           "place them as <strong>braces on the rear tool bar</strong>, forming a mast for "
           "the tractor's top link.") + """
<p>That reading is supported by the &oslash;1&nbsp;in hole &mdash; the same diameter as the
hitch clevis pin &mdash; and by the fact that a three-point mounted implement needs a top
link anchor somewhere.</p>
""" + ticks([
        "If you disagree, the parts are still right; only their placement in Deck 10 "
        "changes.",
        "A cleaner design would join the two braces into a proper A-frame mast. That is "
        "exercise 9 in Deck 14.",
        "This is a good illustration of a real engineering situation: the source is "
        "incomplete, so you state what you assumed and move on rather than stalling."])

    d.sheet("05", P, "CLAMP 02", "The second strap, and what they are for", """
<p class="lede">Clamp&nbsp;02 is Clamp&nbsp;01 with a different path. The interesting part
of this sheet is the honest bit: we are not certain what these parts do.</p>
""" + cols(a5, b5), eyebrow="Same method, stated assumption")

    a6 = specs([("Clamp 01", "42.9 in&sup3; &mdash; 12.2 lb"),
                ("Clamp 02", "48.5 in&sup3; &mdash; 13.8 lb"),
                ("Both, &times;2 each", "52 lb"),
                ("Sketches each", "3"), ("Features each", "2")])

    b6 = plates([("04_clamp01_final_Right", "CLAMP 01 — RIGHT", ""),
                 ("04_clamp01_final_Front", "CLAMP 01 — FRONT", "3 in wide strap"),
                 ("05_clamp02_final_Right", "CLAMP 02 — RIGHT", ""),
                 ("05_clamp02_final_Front", "CLAMP 02 — FRONT", "")], "grid-2")

    d.sheet("06", P, "VERIFY", "Parts 4 and 5 complete", """
<p class="lede">Two features each — a sweep and a hole. The simplest parts in the machine,
and they taught the tool the blades depend on.</p>
""" + cols(a6, b6), eyebrow="Check the numbers")

    return d
