# -*- coding: utf-8 -*-
"""Deck 11 - Patterns, mirrors, link arrays and fasteners."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "PATTERNS"


def build():
    d = Deck("11-patterns-and-fasteners", "Patterns, Mirrors and Fasteners")

    d.sheet("00", P, "REFERENCE", "Patterns, Mirrors and Fasteners", """
<p class="lede">Repetition is most of mechanical design. This deck collects everything this
machine taught us about repeating things — including the one limitation of PartDesign that
you will certainly hit, and the two clean ways round it.</p>
""" + fig("01_frame_08_linear_pattern_holes", "36 HOLES, ONE FEATURE",
          "Nine stations at 9.5 in pitch, both bars, from a single LinearPattern")
        + specs([("Sketch-level", "Symmetry, Rectangular array"),
                 ("Feature-level", "Mirrored, LinearPattern, PolarPattern"),
                 ("Assembly-level", "App::Link array"),
                 ("Cannot", "nest one inside another")]),
            eyebrow="Deck 11", kind="title")

    a = """
<h3>Three levels of repetition</h3>
""" + phases([("In the sketch",
               "<strong>Symmetry</strong> and <strong>Rectangular array</strong>. Cheapest, "
               "most robust, and it composes with everything downstream. Use it when you "
               "can."),
              ("In the feature tree",
               "<strong>Mirrored</strong>, <strong>LinearPattern</strong>, "
               "<strong>PolarPattern</strong>. Repeats a whole feature &mdash; a pocket, "
               "a pad, a group of them."),
              ("In the assembly",
               "<strong>Link arrays</strong>. Repeats a whole component. One tree object "
               "for any number of instances.")]) + \
        note("Push repetition <em>down</em> the levels wherever you can. Symmetry in a "
             "sketch always works; a feature Mirror sometimes does not; and the two "
             "cannot always be combined.")

    b = """
<h3>Where each one is used in this machine</h3>
""" + tbl(["Level", "Tool", "Used for"],
          [["sketch", "Symmetry", "frame rear-bar holes; both tynes' second bolt hole; "
            "the blade's plan outline"],
           ["sketch", "Symmetry about a point", "centring every rectangle on the origin"],
           ["feature", "LinearPattern", "the nine tyne stations"],
           ["feature", "Mirrored", "the second hitch clevis"],
           ["feature", "Fillet on a pattern", "all eight clevis nose corners at once"],
           ["assembly", "Link array", "5 tynes, 4 tynes, 5 blades, 4 blades, 2+2 clamps"]])

    d.sheet("01", P, "LEVELS", "Three places to repeat something", """
<p class="lede">FreeCAD lets you repeat geometry at three different levels. Choosing the
right one is mostly about which limitations you can live with.</p>
""" + cols(a, b), eyebrow="Push it down a level")

    a2 = """
<h3>LinearPattern</h3>
""" + steps([("Select the feature to repeat &mdash; a Pocket, a Pad, or several", ""),
             ("<strong>Part Design ▸ Apply a pattern ▸ LinearPattern</strong>", ""),
             ("<strong>Direction</strong>: an origin axis, a sketch axis, or an edge", ""),
             ("<strong>Mode</strong>: Extent or Spacing", ""),
             ("<strong>Occurrences</strong>: the total, including the original", ""),
             ("<strong>Reverse</strong> if it went the wrong way", "")]) + \
        tbl(["Mode", "Length means", "Change Occurrences and&hellip;"],
            [["<strong>Extent</strong>", "the total span from first to last",
              "they get closer together; the span stays"],
             ["<strong>Spacing</strong>", "the gap between neighbours",
              "the pattern gets longer"]]) + \
        note("For the frame we used <strong>Extent</strong> with length "
             "<code>(HoleCount-1) * HolePitch</code> and occurrences "
             "<code>HoleCount</code> &mdash; so both the span and the pitch stay correct "
             "when the count changes. That is the combination you usually want.")

    b2 = """
<h3>Mirrored</h3>
""" + steps([("Select the feature or features", ""),
             ("<strong>Part Design ▸ Apply a pattern ▸ Mirrored</strong>", ""),
             ("<strong>Mirror plane</strong>: an origin plane, a datum plane, or a "
              "sketch's axis", "")], compact=True) + """
<p>Its other mode is <strong>Whole shape</strong>: instead of repeating named features it
mirrors the entire solid so far and fuses the result.</p>
""" + warn("<strong>Whole shape is a trap with subtractive features.</strong> Mirror a "
           "shape that has holes in the front bar and fuse it with the original, and each "
           "copy fills the other's holes &mdash; you get a frame with no holes at all. "
           "Whole-shape mirroring is only safe for purely additive geometry.")

    d.sheet("02", P, "FEATURES", "LinearPattern and Mirrored", """
<p class="lede">The two feature-level tools, and the settings that actually matter.</p>
""" + cols(a2, b2), eyebrow="Extent, not spacing")

    a3 = """
<h3>The limitation</h3>
<p>PartDesign's transformation features <strong>cannot take another transformation feature
as input</strong>. Not a pattern of a pattern, not a mirror of a pattern, not a pattern of
a mirror.</p>
""" + code("""
What the tutorial does in SolidWorks:

  1. two holes on the front bar
  2. LinearPattern them, 9 at 9.5 in
  3. Mirror the pattern about the Front plane -> rear bar

What FreeCAD does with step 3:

  Mirror_HolesToRearBar  ['Touched', 'Invalid']
  Shape is null
  ...and every feature after it is stuck 'Touched'
""") + """
<p>There is no error dialog. The feature simply goes Invalid, and if you do not notice, you
carry on building on top of a broken tree.</p>
"""

    b3 = """
<h3>Two ways round it</h3>
""" + phases([("Do the symmetry in the sketch",
               "Put all four circles &mdash; both bars &mdash; in one sketch, tied together "
               "with Symmetry and Equal constraints. Then one Pocket, then one "
               "LinearPattern. This is what we did."),
              ("Pattern a group of features",
               "A single LinearPattern can take <em>several</em> originals at once. So "
               "make two separate pockets (front bar, rear bar) and pattern both in one "
               "feature. Also valid, one more feature in the tree.")]) + \
        fig("01_frame_06_sketch_station_holes", "THE FIX",
            "All four holes in one sketch: two dimensioned, two mirrored by constraint") + \
        note("The sketch route is better. The rear holes are now tied to the front ones by "
             "a live constraint, so they cannot drift apart &mdash; which is more than the "
             "SolidWorks version guarantees.")

    d.sheet("03", P, "LIMITATION", "You cannot pattern a pattern", """
<p class="lede">This is the one PartDesign limitation everybody hits, and it fails silently.
Worth understanding properly.</p>
""" + cols(a3, b3), eyebrow="And it fails silently")

    a4 = """
<h3>Link arrays</h3>
<p>SolidWorks has a <em>Linear Component Pattern</em> in assemblies. FreeCAD's Assembly
workbench does not. What it has instead is arguably better.</p>
""" + code("""
lnk = doc.addObject('App::Link', 'Tine01_x5')
lnk.LinkedObject  = tine01_body
lnk.ElementCount  = 5
lnk.ShowElement   = False
lnk.PlacementList = [ Placement(x, -10, 0) for x in
                      (-38, -19, 0, 19, 38) ]
""") + ticks([
        "<strong>One object</strong> in the tree, whatever the count.",
        "<strong>One copy</strong> of the geometry in memory &mdash; nine tynes cost what "
        "one costs.",
        "<strong>Arbitrary placements.</strong> Not just a grid: any list. Staggered ranks, "
        "a curved rank, a random scatter.",
        "<strong>Generated from a formula.</strong> The list is code, so the pitch can come "
        "from a spreadsheet."])

    b4 = """
<h3>Doing it in the GUI</h3>
""" + steps([("Select the component in the tree", ""),
             ("In the <strong>Data</strong> tab, set <strong>Element Count</strong>", ""),
             ("Set <strong>Show Element</strong> to false so the array uses the "
              "placement list rather than exposing each child", ""),
             ("Expand <strong>Placement List</strong> and enter each placement", ""),
             ("Leave the link's own <strong>Placement</strong> at identity", "")]) + \
        warn("<strong>The compounding trap again.</strong> <code>PlacementList</code> "
             "entries are relative to the link's own <code>Placement</code>. Set both and "
             "your whole array shifts by the first element's offset. Symptom: the parts "
             "look right relative to each other but the entire rank is displaced from the "
             "frame.")

    d.sheet("04", P, "LINK ARRAYS", "Repeating components", """
<p class="lede">The assembly-level answer, and the one FreeCAD feature in this course with
no SolidWorks equivalent at all.</p>
""" + cols(a4, b4), eyebrow="Better than a component pattern")

    a5 = """
<h3>Fasteners</h3>
<p>The transcript calls for hex bolts &mdash; &ldquo;lengths 1.5 / 2.75 / 5.5 / 5 / 4 /
1.25 in, 1.25 TPI&rdquo; &mdash; patterned at 9.5&nbsp;in pitch and mirrored. SolidWorks
pulls these from its Toolbox. FreeCAD core has no bolt library.</p>
""" + tbl(["Option", "How", "Verdict"],
          [["<strong>Fasteners workbench</strong>",
            "Addon Manager ▸ Fasteners. ISO/DIN/ANSI screws, nuts, washers, placed on a "
            "hole with one click.",
            "the right answer for real work"],
           ["<strong>Model one bolt</strong>",
            "Hexagon sketch + Pad for the head, circle + Pad for the shank. Ten minutes.",
            "fine, and it is a good sketching exercise"],
           ["<strong>Leave them out</strong>",
            "Holes are modelled; bolts are not.",
            "what this course does &mdash; and states"]]) + \
        note("<strong>Install the addon:</strong> Tools ▸ Addon Manager ▸ Fasteners ▸ "
             "Install, then restart. It adds a workbench that will place a bolt "
             "concentric to any selected hole.")

    b5 = """
<h3>What the bolts would be</h3>
<p>Reading the transcript's list against the machine we have built:</p>
""" + tbl(["Length", "Joint", "Grip"],
          [["1.25 in", "blade to tyne point", "0.2 + 1.5 sheet + nut"],
           ["<strong>4 in</strong>", "<strong>tyne head to tool bar</strong>",
            "1.25 head + 2 tube + nut &mdash; <strong>18 off</strong>"],
           ["5 in", "clamp foot to bar", "3 strap + 2 tube"],
           ["5.5 in", "clamp to clamp", "two straps plus spacer"],
           ["2.75 in", "clevis pin retention", ""],
           ["1.5 in", "miscellaneous", ""]]) + \
        code("""
Bolt count, tyne mountings only:
   9 tynes x 2 bolts             = 18 off, 1/2 in x 4 in

Full set including clamps and blades: about 40 bolts.
""") + note("Modelling all forty is not a good use of your time unless you need a bill of "
            "materials. If you do, the Fasteners workbench plus a link array gets you "
            "there in about fifteen minutes.")

    d.sheet("05", P, "FASTENERS", "The bolts we did not model", """
<p class="lede">Deliberately left out — and here is exactly what it would take to put them
in, plus what they would be.</p>
""" + cols(a5, b5), eyebrow="Stated, not hidden")

    a6 = """
<h3>Quick reference</h3>
""" + tbl(["Want to&hellip;", "Use", "Level"],
          [["mirror geometry inside one sketch", "Symmetry constraint", "sketch"],
           ["repeat geometry inside one sketch", "Rectangular array", "sketch"],
           ["repeat a pocket along a line", "LinearPattern", "feature"],
           ["repeat around an axis", "PolarPattern", "feature"],
           ["mirror a pad or pocket", "Mirrored", "feature"],
           ["mirror the whole solid (additive only)", "Mirrored, Whole shape", "feature"],
           ["combine a pattern and a mirror", "MultiTransform", "feature"],
           ["repeat a component", "App::Link array", "assembly"],
           ["pattern a pattern", "<strong>not possible</strong> &mdash; restructure",
            "&mdash;"]])

    b6 = """
<h3>Rules of thumb</h3>
""" + ticks([
        "<strong>Pattern the smallest thing that works.</strong> Patterning one pocket is "
        "robust; patterning a group of six features is fragile.",
        "<strong>Bind occurrences and spacing to the spreadsheet.</strong> A pattern with "
        "hard-typed numbers is a pattern you will edit by hand forever.",
        "<strong>Check the count after every pattern.</strong> Occurrences includes the "
        "original &mdash; 9 occurrences means 9 total, not 9 extra.",
        "<strong>Dress up after patterning, not before.</strong> One Fillet across all "
        "eight clevis nose edges is one feature; filleting first and then mirroring is "
        "a feature that will not build.",
        "<strong>If a transformation goes Invalid, look for nesting first.</strong> Nine "
        "times out of ten that is what it is."])

    d.sheet("06", P, "SUMMARY", "Which tool, when", """
<p class="lede">One table to keep. Everything this machine taught about repeating things.</p>
""" + cols(a6, b6), eyebrow="Keep this one")

    return d
