# -*- coding: utf-8 -*-
"""Deck 14 - Summary, reference and student exercises."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "SUMMARY"


def build():
    d = Deck("14-summary-and-exercises", "Summary and Exercises")

    d.sheet("00", P, "REVIEW", "Summary and Exercises", """
<p class="lede">Seven parts, twenty sketches, twenty-four features, one assembly, and about
a dozen places where FreeCAD did something you needed to understand rather than
memorise. Here it all is in one place — plus twelve exercises.</p>
""" + fig("08_asm_hero_Isometric", "COMPLETE", "377 lb, 76 in working width")
        + specs([("Parts", "7"), ("Components", "23"), ("Sketches", "20"),
                 ("Features", "24"), ("All fully constrained", "yes"),
                 ("Exercises", "12")]),
            eyebrow="Deck 14", kind="title")

    a = tbl(["Part", "Sketches", "Features", "Mass", "Off", "Taught"],
            [["Frame", "6", "8", "82.2 lb", "1",
              "pad, pocket, offset attachment, symmetry, pattern, mirror, fillet"],
             ["Tine 01", "3", "3", "26.6 lb", "5", "arcs, tangency, solver ambiguity"],
             ["Tine 02", "3", "4", "22.1 lb", "4", "derived parameters, edge selection"],
             ["Clamp 01", "3", "2", "12.2 lb", "2", "Additive Pipe, sketch fillets"],
             ["Clamp 02", "3", "2", "13.8 lb", "2", "reusing a method"],
             ["Blade 01", "3", "2", "2.4 lb", "5", "replacing Flex, two-wire pockets"],
             ["Blade 02", "&mdash;", "&mdash;", "2.4 lb", "4", "one cell"],
             ["<strong>Assembly</strong>", "&mdash;", "&mdash;", "<strong>377 lb</strong>",
              "&mdash;", "links, arrays, joints"]])

    b = """
<h3>The ten things worth remembering</h3>
""" + ticks([
        "<strong>Fully constrain every sketch.</strong> Zero degrees of freedom, every time.",
        "<strong>Attach sketches to origin planes,</strong> not to faces. Offsets, not datums.",
        "<strong>Endpoint tangency</strong> where curves join smoothly &mdash; never "
        "tangency plus coincidence.",
        "<strong>Distances beat angles.</strong> An angle constraint has two answers.",
        "<strong>Read the solver message.</strong> Redundant means no shape, which means "
        "the next feature fails.",
        "<strong>A pocket cuts from its sketch plane onward.</strong> Put the plane where "
        "the cut starts.",
        "<strong>You cannot pattern a pattern.</strong> Do the symmetry in the sketch.",
        "<strong>Dress-up features go last</strong> and stay few.",
        "<strong>Design each part around its interface,</strong> and put the origin there.",
        "<strong>Every driving dimension in a spreadsheet,</strong> named, with units."])

    d.sheet("01", P, "REVIEW", "What we built, and what it taught", """
<p class="lede">Every part earned its place in the course by teaching something the next
part needed.</p>
""" + cols(a, b), eyebrow="The whole course on one sheet")

    a2 = """
<h3>Every assumption we made</h3>
<p>The transcript is a machine translation. Where it was silent or garbled, we decided —
and here is the complete list, so you can disagree with any of it.</p>
""" + tbl(["#", "Assumption", "Source said"],
          [["1", "Frame holes are <strong>pairs</strong> at 3 in centres",
            "&ldquo;one hole here and another&hellip; hole size is 3 inches&rdquo;"],
           ["2", "Square tube is <strong>2 &times; 2</strong>, 0.1875 is the wall",
            "&ldquo;square tube&hellip; size 0.1875&rdquo;"],
           ["3", "Clevis plate 5 in long, 3 in tall", "not dimensioned"],
           ["4", "Tine 01 rake <strong>35&deg;</strong>", "not stated"],
           ["5", "Tine 01 inner bend <strong>R6</strong>", "not stated"],
           ["6", "25 in = total along shank; 15 in = the straight part",
            "both numbers stated, no relationship given"],
           ["7", "Tyne bolt holes go <strong>through</strong>, not blind 0.4",
            "&ldquo;blind condition, depth 0.4&rdquo;"],
           ["8", "Clamps are <strong>braces</strong> forming a top-link mast",
            "&ldquo;the attachment clamp&rdquo;, never mated"],
           ["9", "Clamp 02 tip is <strong>6 in</strong> long", "angle given, length not"],
           ["10", "Blade centreline radius is R10 / R16",
            "&ldquo;bend radius &minus;10&rdquo; (Flex convention)"],
           ["11", "<strong>No blade bolt holes</strong>", "never mentioned"],
           ["12", "Full-round fillet becomes <strong>two corner fillets</strong>",
            "&ldquo;complete circular fillet on three faces&rdquo;"]])

    b2 = """
<h3>Why list them at all?</h3>
<p>Because a design document that hides its assumptions is not a design document. Anyone
reviewing this model can see in one table exactly where the source ran out and judgement
took over.</p>
""" + note("Every one of these twelve is a <strong>spreadsheet parameter</strong>. "
           "Disagreeing with any of them costs one cell edit and a recompute &mdash; which "
           "is the practical reason to build parametrically, quite apart from the "
           "principle.") + """
<h3>Things a real design review would raise</h3>
""" + ticks([
        "No top-link mast is properly defined &mdash; the machine cannot be hitched as "
        "modelled. Exercise 9.",
        "No depth-control wheel or skid, so working depth depends entirely on the tractor's "
        "draft control.",
        "The tynes are rigid: no shear-bolt or spring release. A stone will bend a shank.",
        "No stress analysis. At ~150 lbf per tyne the 2.25 &times; 1.5 in shank is "
        "comfortable, but that is arithmetic, not FEM. Exercise 12."])

    d.sheet("02", P, "ASSUMPTIONS", "Everything we assumed", """
<p class="lede">Twelve decisions the source did not make for us. All twelve are parameters,
so all twelve are yours to change.</p>
""" + cols(a2, b2), eyebrow="Nothing hidden")

    a3 = """
<h3>Exercises &mdash; get comfortable</h3>
""" + phases([("1. Change the tyne count",
               "Open the frame. Set <code>HoleCount</code> to 11 and "
               "<code>FrameLength</code> to 101 in. Recompute. Check the end margin is "
               "still sensible and report the new mass."),
              ("2. Change the working width",
               "Make a 10 ft machine. Decide the tyne spacing first, then work out the "
               "count and the frame length &mdash; do not just stretch the frame."),
              ("3. Re-rake Tine 01",
               "Set <code>Rake</code> to 25&deg;, then 45&deg;. Note what happens to the "
               "forward reach and to the overall height. Which raking would you specify "
               "for hard ground, and why?"),
              ("4. Add blade bolt holes",
               "Two &oslash;0.5 in holes on the blade centreline that line up with the "
               "tyne point. You will need to decide the spacing yourself &mdash; justify "
               "it.")])

    b3 = """
<h3>Exercises &mdash; build something</h3>
""" + phases([("5. Model a bolt",
               "&frac12; in &times; 4 in hex head bolt: hexagon sketch, pad, circle, pad, "
               "chamfer. Then place eighteen of them with a link array."),
              ("6. Draw the frame",
               "A TechDraw sheet: plan, front, isometric, plus a section through a tool bar "
               "showing the 3/16 wall. Fully dimensioned, with a title block."),
              ("7. A third tyne",
               "Design a spring-tine (S-tine) alternative that uses the same 5 in head and "
               "3 in bolt centres. It must drop into any existing station."),
              ("8. Make the blade sharp",
               "Add a ground edge to the underside of the blade's two cutting edges. "
               "Chamfer, taper, or a subtractive pipe &mdash; try more than one and say "
               "which models it best.")])

    d.sheet("03", P, "EXERCISES", "Exercises 1 to 8", """
<p class="lede">The first four are parameter edits — thirty minutes each. The next four are
modelling jobs.</p>
""" + cols(a3, b3), eyebrow="Start here")

    a4 = """
<h3>Exercises &mdash; harder</h3>
""" + phases([("9. Build a proper hitch",
               "The machine as modelled cannot be hitched: there is no top-link point. "
               "Design an A-frame mast that ties into the existing clevises and the rear "
               "bar, using Clamp 01 and Clamp 02 or replacing them. Justify the geometry "
               "against a Category II three-point linkage."),
              ("10. One master parameter table",
               "Move <code>BoltSpacing</code>, <code>BoltDia</code> and "
               "<code>HeadLength</code> into a single master document and have the frame "
               "and both tynes reference it. Then change the bolt to &frac58; in and "
               "confirm all three parts follow."),
              ("11. Assemble it with joints",
               "Rebuild the assembly using Assembly-workbench Joints instead of "
               "placements. Ground the frame; use Coincident joints on the actual mounting "
               "faces and bolt holes. Report any place where the parts did <em>not</em> "
               "fit &mdash; that is the real test of the model.")])

    b4 = """
<h3>Exercise &mdash; the big one</h3>
""" + phases([("12. Analyse a tyne",
               "Take Tine 01 into the <strong>FEM</strong> workbench. Fix the mounting "
               "head, apply a horizontal 150 lbf at the point, mesh it, and solve for von "
               "Mises stress. Compare the peak with the yield strength of your chosen "
               "steel. Then answer: is the 2.25 &times; 1.5 in section right, over-designed, "
               "or marginal? What would you change and why?")]) + \
        note("Exercise 12 is where the modelling stops being drawing and starts being "
             "engineering. A model built the way this course built it &mdash; correct "
             "material, correct geometry, correct mass &mdash; is ready for it. A model "
             "pushed around until it looked right is not.") + """
<h3>How these are marked</h3>
""" + ticks([
        "Every sketch <strong>fully constrained</strong>. This is not negotiable.",
        "Every driving dimension in a spreadsheet, <strong>named</strong>, with units.",
        "Assumptions <strong>stated</strong>, with a reason.",
        "The model <strong>recomputes cleanly</strong> &mdash; no Invalid or Touched "
        "features anywhere in the tree.",
        "Mass and envelope quoted, and <strong>checked</strong> against a rough "
        "hand calculation."])

    d.sheet("04", P, "EXERCISES", "Exercises 9 to 12", """
<p class="lede">These take longer and have no single right answer. Exercise 12 is the one
that turns a CAD exercise into a design exercise.</p>
""" + cols(a4, b4), eyebrow="Where it gets real")

    a5 = """
<h3>The files</h3>
""" + tbl(["Path", "What"],
          [["<code>parts/01_frame.FCStd</code> &hellip; <code>07_blade02.FCStd</code>",
            "the seven parts, each with its Params sheet"],
           ["<code>parts/08_cultivator_assembly.FCStd</code>", "the assembly"],
           ["<code>tools/fc_helpers.py</code>",
            "the shared library: inch units, screenshots, constrained sketch primitives, "
            "spreadsheet binding, pattern wrappers"],
           ["<code>tools/build_frame.py</code> &hellip; <code>build_assembly.py</code>",
            "one runnable script per part &mdash; re-run any to rebuild it from nothing"],
           ["<code>tools/deck_kit.py</code>, <code>tools/decks/</code>",
            "this course, as code"],
           ["<code>screenshots/</code>", "101 captures, every one taken by script"],
           ["<code>transcript.txt</code>", "the translated source narration"]])

    b5 = """
<h3>Rebuilding a part from scratch</h3>
""" + code("""
# in FreeCAD's Python console
exec(open(r"C:\\...\\freecad\\tools\\build_frame.py",
          encoding="utf-8").read())
""") + """
<p>Each script closes any existing document of that name, rebuilds the part step by step,
takes its screenshots, prints a constraint report and a volume, and saves. Running them is
the fastest way to see what every feature in this course actually does.</p>
""" + note("<strong>Read one.</strong> <code>build_tine01.py</code> is about 200 lines and "
           "contains every constraint on the tyne profile, in order, with comments. It is a "
           "better reference than any slide.") + """
<h3>Where to go next</h3>
""" + ticks([
        "<strong>FreeCAD documentation</strong> &mdash; <code>wiki.freecad.org</code>, "
        "genuinely good on Part Design and Sketcher.",
        "<strong>The FEM workbench</strong> &mdash; for exercise 12.",
        "<strong>The Fasteners addon</strong> &mdash; for exercise 5, if you would rather "
        "not model a bolt.",
        "<strong>The source video</strong> &mdash; Malviya CAD Solution, &ldquo;Design of "
        "Cultivator in SolidWorks | Nine tines cultivator&rdquo;. Watch it now that you "
        "know what the numbers mean."])

    d.sheet("05", P, "REFERENCE", "The files, and what to do next", """
<p class="lede">Everything in this course is on disk and re-runnable. Nothing here is a
screenshot of something you cannot reproduce.</p>
""" + cols(a5, b5), eyebrow="It all rebuilds")

    return d
