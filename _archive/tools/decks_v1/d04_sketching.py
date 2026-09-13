# -*- coding: utf-8 -*-
"""Deck 4 - Sketching and constraints."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)


def build():
    d = Deck("04-sketching-and-constraints", "Sketching and Constraints")

    d.sheet("00", "SKETCHER", "FUNDAMENTALS", "Sketching and Constraints", """
<p class="lede">Everything in this machine starts as a 2D sketch. A sketch is not a
drawing — it is a set of geometry plus a set of <strong>rules</strong>, solved
simultaneously. Learn to think in rules and the rest of CAD follows.</p>
""" + fig("01_frame_03_sketch_plan_constrained", "SKETCHER",
          "The frame plan sketch in edit mode: 8 lines, 22 constraints, fully constrained")
        + specs([("Geometry types", "line, arc, circle, B-spline, point"),
                 ("Constraint types", "geometric and dimensional"),
                 ("Target", "0 degrees of freedom"),
                 ("Status", 'shown in the Sketcher task panel')]),
            eyebrow="Deck 4", kind="title")

    a = """
<h3>Degrees of freedom</h3>
<p>Every piece of geometry can move. A line segment has <strong>4</strong> degrees of
freedom — two coordinates at each end. A circle has 3: centre x, centre y, radius. An arc
has 5.</p>
<p>Each constraint removes one or more. When the total removed equals the total available,
the sketch has <strong>zero degrees of freedom</strong> and nothing in it can move. FreeCAD
then says <em>Fully constrained</em> and turns the geometry green.</p>
""" + code("""
Frame plan sketch
  8 lines  x 4 DoF                 = 32
  constraints removed              = 32
  ------------------------------------
  remaining                        =  0     -> fully constrained
""")

    b = """
<h3>Why it matters</h3>
""" + ticks([
        "<strong>The model stops surprising you.</strong> An under-constrained sketch will "
        "quietly move when an upstream dimension changes, and you will not notice until "
        "something two features later fails.",
        "<strong>Intent becomes readable.</strong> A constrained sketch says <em>this "
        "rectangle is centred on the origin and 82 inches wide</em>, not <em>these four "
        "lines happen to be here</em>.",
        "<strong>It is the whole point of parametric CAD.</strong> If the geometry is not "
        "locked to the dimensions, changing a dimension does not reliably change the "
        "geometry."]) + \
        warn("<strong>Never leave a sketch under-constrained &ldquo;for now&rdquo;.</strong> "
             "Every one of the 20 sketches in this cultivator reports "
             "<strong>fully constrained</strong>. It is a habit, not a chore &mdash; and "
             "the Sketcher tells you the moment you get there.")

    d.sheet("01", "CONSTRAINTS", "PRINCIPLE", "What &ldquo;fully constrained&rdquo; means", """
<p class="lede">A sketch is fully constrained when there is exactly one shape that
satisfies all its rules. Not &ldquo;looks right&rdquo; — <em>provably</em> one shape.</p>
""" + cols(a, b), eyebrow="The single most important idea")

    a2 = """
<h3>Geometric constraints — relationships</h3>
<p>No numbers. They say how pieces of geometry relate to each other.</p>
""" + tbl(["Constraint", "Key", "Says"],
          [["Coincident", "<code>C</code>", "these two points are the same point"],
           ["Horizontal", "<code>H</code>", "this line is horizontal"],
           ["Vertical", "<code>V</code>", "this line is vertical"],
           ["Parallel", "<code>P</code>", "these two lines run the same way"],
           ["Perpendicular", "<code>N</code>", "these two lines meet at 90&deg;"],
           ["Tangent", "<code>T</code>", "curve and line meet smoothly"],
           ["Equal", "<code>E</code>", "same length, or same radius"],
           ["Symmetric", "<code>S</code>", "these two points mirror about that line"],
           ["Point on object", "<code>O</code>", "this point lies on that curve"],
           ["Block", "<code>K,B</code>", "freeze this geometry (a last resort)"]])

    b2 = """
<h3>Dimensional constraints — numbers</h3>
""" + tbl(["Constraint", "Key", "Says"],
          [["Distance", "<code>K,D</code>", "this length is 15 in"],
           ["Horizontal distance", "<code>L</code>", "&Delta;x between two points"],
           ["Vertical distance", "<code>I</code>", "&Delta;y between two points"],
           ["Radius", "<code>K,R</code>", "this arc is R6"],
           ["Diameter", "<code>K,O</code>", "this circle is &oslash;0.5"],
           ["Angle", "<code>K,A</code>", "these two lines are 35&deg; apart"]]) + \
        note("<strong>Prefer geometric constraints.</strong> Two lines constrained "
             "<em>Equal</em> stay equal forever; two lines each dimensioned 5&nbsp;in are "
             "only equal until someone edits one of them. Use dimensions for the values a "
             "designer actually chose, and geometry for the relationships that must hold.")

    d.sheet("02", "CONSTRAINTS", "THE TWO KINDS", "Geometric and dimensional", """
<p class="lede">There are two families of constraint, and good sketches use far more of the
first than the second.</p>
""" + cols(a2, b2), eyebrow="Relationships and numbers")

    a3 = """
<h3>A rectangle, fully constrained, in six constraints</h3>
""" + steps([("Draw four lines corner to corner. FreeCAD adds the four "
              "<strong>Coincident</strong> constraints automatically as you snap.",
              "16 DoF - 8 = 8 left"),
             ("<strong>Horizontal</strong> on the top and bottom lines", "8 - 2 = 6"),
             ("<strong>Vertical</strong> on the left and right lines", "6 - 2 = 4"),
             ("<strong>Symmetric</strong>: bottom-left and top-right corners about the "
              "origin point. This centres the rectangle.", "4 - 2 = 2"),
             ("<strong>Horizontal distance</strong> on the bottom line = 82 in", "2 - 1 = 1"),
             ("<strong>Vertical distance</strong> on the right line = 22 in",
              "1 - 1 = 0  fully constrained")])

    b3 = fig("01_frame_03_sketch_plan_constrained", "RESULT",
             "Two centred rectangles, 22 constraints, fully constrained &mdash; the "
             "frame plan") + """
<p>That is the frame's plan sketch: the same six-constraint recipe applied twice, once for
the 82 &times; 22 outside and once for the 78 &times; 18 inside. The ring between them is
the square tube.</p>
""" + note("Notice what centring the rectangle on the origin bought us: the frame is now "
           "symmetric about both origin planes <em>by construction</em>. Later we mirror "
           "the hitch clevis about YZ and it lands exactly right, with no arithmetic.")

    d.sheet("03", "WORKED", "RECTANGLE", "Worked example: a centred rectangle", """
<p class="lede">The most common shape in the whole machine, done properly. Follow the
degrees-of-freedom count down the right-hand column.</p>
""" + cols(a3, b3), eyebrow="Count the degrees of freedom")

    a4 = """
<h3>Symmetry instead of copying</h3>
<p>The frame needs bolt holes on <em>both</em> tool bars. You could draw four circles and
dimension all four. Instead:</p>
""" + steps([("Draw and fully constrain the two holes on the front bar", ""),
             ("Draw two more circles roughly where the rear pair goes", ""),
             ("Select front hole centre, rear hole centre, then the "
              "<strong>X axis</strong>, and press <code>S</code>", ""),
             ("Add <strong>Equal</strong> so the diameters follow too", ""),
             ("Repeat for the second pair. Fully constrained.", "")], compact=True) + \
        note("This is FreeCAD's answer to SolidWorks <em>Mirror Entities</em>. It is not a "
             "copy — it is a live relationship. Move the front hole and the rear one "
             "follows, forever.")

    b4 = fig("01_frame_06_sketch_station_holes", "SYMMETRY",
             "One tyne station: two holes at 3 in centres, mirrored about the X axis to "
             "the rear bar. Four circles, ten constraints, zero DoF.") + \
        warn("<strong>Why not a feature Mirror?</strong> Because we are about to "
             "<em>pattern</em> this pocket nine times, and PartDesign cannot pattern a "
             "mirror or mirror a pattern &mdash; the feature goes <em>Invalid</em>. "
             "Doing the symmetry inside the sketch sidesteps the whole problem. "
             "Deck 11 has the full story.")

    d.sheet("04", "WORKED", "SYMMETRY", "Worked example: symmetry", """
<p class="lede">Symmetry is the constraint students under-use most, and it is the one that
makes a model hold together when dimensions change.</p>
""" + cols(a4, b4), eyebrow="Relationships beat copies")

    a5 = """
<h3>Tangency: use the endpoint form</h3>
<p>When an arc joins a line smoothly, you need <strong>endpoint-to-endpoint</strong>
tangency &mdash; select the line's endpoint and the arc's endpoint, then press
<code>T</code>. That single constraint carries the coincidence with it.</p>
""" + warn("Selecting the <em>line</em> and the <em>arc</em> (rather than their endpoints) "
           "gives you edge-to-edge tangency. If the two are already joined by a Coincident "
           "constraint, the two rules fight, and the solver reports "
           "<strong>conflicting constraints</strong>. The sketch then produces no shape at "
           "all and every feature downstream fails.") + code("""
Tine 01 profile, first attempt
  Coincident(rear line end, arc end)     <- from snapping
  Tangent(rear line, arc)                <- edge to edge
  ...
  solve() = -3        conflicting: [3, 4, 7, 8, 13, 14, 15, 16]
  Shape has 0 edges   ->  Pad fails with no profile

Fix: drop the Coincident, use Tangent(line, pos2, arc, pos1)
  solve() = 0         fully constrained
""")

    b5 = """
<h3>Angle constraints have two answers</h3>
<p>&ldquo;These two lines are 35&deg; apart&rdquo; describes two different shapes &mdash;
one raked forward, one raked back. The solver picks whichever it reaches first, and it is
not always the one you drew.</p>
""" + fig("02_tine01_02_sketch_profile", "TINE 01 PROFILE",
          "The rake is dimensioned as a horizontal distance, not an angle") + \
        note("On the Tine 01 profile an Angle constraint flipped the tyne backwards. "
             "Replacing it with a <strong>horizontal distance</strong> to the point &mdash; "
             "how far forward the tyne reaches &mdash; is unambiguous, and it is arguably "
             "the better design dimension anyway. The rake angle is still a spreadsheet "
             "parameter; the reach is computed from it.")

    d.sheet("05", "TRAPS", "SOLVER", "Two traps that will bite you", """
<p class="lede">Both of these cost real time on this model. Both have a one-line fix once
you know what you are looking at.</p>
""" + cols(a5, b5), eyebrow="Learn these now, not later")

    a6 = """
<h3>Reading the solver's verdict</h3>
""" + tbl(["Message", "Means", "Do"],
          [["<strong>Fully constrained</strong>", "0 DoF, one solution", "move on"],
           ["<em>n</em> degrees of freedom", "geometry can still move",
            "add constraints until n = 0"],
           ["<strong>Redundant constraints</strong>",
            "you said the same thing twice",
            "delete one &mdash; FreeCAD names which"],
           ["<strong>Partially redundant</strong>", "over-specified in one direction",
            "usually safe, but tidy it"],
           ["<strong>Conflicting constraints</strong>",
            "two rules cannot both be true", "delete one; the sketch makes no shape until "
            "you do"],
           ["<strong>Malformed constraints</strong>", "constraint refers to deleted geometry",
            "delete it"]])

    b6 = """
<h3>Redundancy is not harmless</h3>
<p>A redundant constraint does not just clutter the list. FreeCAD refuses to produce a
<strong>shape</strong> from a sketch it could not cleanly solve &mdash; the sketch has
zero wires, and any Pad or Pocket using it fails with an unhelpful message about a missing
profile.</p>
""" + code("""
Blade plan-shape sketch, first attempt
  ... Symmetric(side lines about V axis)
  ... Symmetric(trailing edge about V axis)   <- says it again

  solve() = -2   redundant: [18, 19]
  sk.Shape.Wires -> 0
  Pocket -> Invalid

Fix: delete the second Symmetric. 25 constraints, 0 DoF, 2 wires.
""") + note("So when a Pad or Pocket fails and the sketch <em>looks</em> fine, check the "
            "solver message first. Nine times out of ten the sketch is telling you.")

    d.sheet("06", "DIAGNOSIS", "MESSAGES", "What the solver is telling you", """
<p class="lede">The Sketcher tells you exactly what is wrong, in a small line of text most
beginners never read. Read it.</p>
""" + cols(a6, b6), eyebrow="Read the message")

    a7 = """
<h3>A workflow that works</h3>
""" + phases([("Draw roughly, at roughly the right size",
               "Do not chase exact coordinates with the mouse. Get the shape and the "
               "topology right; the constraints will move it."),
              ("Add geometric constraints first",
               "Horizontal, vertical, tangent, symmetric, equal. These express what must "
               "always be true and they cost nothing to change later."),
              ("Then add dimensions, watching the DoF count",
               "Each one should take the count down by exactly one. If a dimension takes "
               "it down by zero, it is redundant &mdash; undo it."),
              ("Stop at zero",
               "Do not add 'just one more to be safe'. That one is the redundant one.")])

    b7 = """
<h3>Habits worth forming</h3>
""" + ticks([
        "<strong>Name your dimensional constraints.</strong> Double-click the constraint in "
        "the Elements list and give it a name &mdash; <code>FrameLength</code>, not "
        "<code>Constraint7</code>. You need the name to drive it from a spreadsheet, and "
        "it turns the constraint list into documentation.",
        "<strong>Sketch small, feature often.</strong> One sketch that makes one feature. "
        "A 60-line sketch that makes one enormous pad is impossible to edit.",
        "<strong>Use construction geometry.</strong> Toggle a line to construction "
        "(<code>G, N</code>) and it constrains real geometry without becoming part of the "
        "profile. Centrelines, symmetry axes, bolt-circle diameters.",
        "<strong>Close your profiles.</strong> An open wire cannot be padded. If a Pad "
        "complains, check for a gap at a corner &mdash; usually a missing Coincident."])

    d.sheet("07", "METHOD", "WORKFLOW", "How to sketch, in order", """
<p class="lede">Do it in this order and sketches come out constrained the first time,
instead of being wrestled into shape.</p>
""" + cols(a7, b7) + note("Every dimensional constraint in this cultivator is named, and "
                          "every one is bound to a spreadsheet cell. That takes about "
                          "twenty extra seconds per sketch and it is what makes Deck 13 "
                          "possible."),
            eyebrow="Rough, then relate, then dimension")

    return d
