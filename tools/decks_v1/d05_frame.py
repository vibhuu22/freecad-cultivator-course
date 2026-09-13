# -*- coding: utf-8 -*-
"""Deck 5 - Part 1, the frame."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "01 FRAME"


def build():
    d = Deck("05-part1-frame", "Part 1 — The Frame")

    d.sheet("00", P, "OVERVIEW", "Part 1 — The Frame", """
<p class="lede">The frame carries everything: both tool bars, all nine tyne stations, and
the tractor hitch. It is a welded rectangle of 2&nbsp;&times;&nbsp;2&nbsp;&times;&nbsp;0.1875&nbsp;in
square tube, and it teaches six of the eight Part Design features you will ever need.</p>
""" + fig("01_frame_final_Isometric", "ISOMETRIC",
          "82 lb of steel: two tool bars, two end members, 36 bolt holes, two hitch clevises")
        + specs([("Overall", "82 &times; 22 &times; 2 in"),
                 ("Section", "2 &times; 2 &times; 3/16 square tube"),
                 ("Stations", "9 at 9.5 in pitch"),
                 ("Holes", "36 &oslash;0.5 in"),
                 ("Hitch", "2 clevises at &plusmn;15 in"),
                 ("Mass", "82.2 lb")]),
            eyebrow="Deck 5", kind="title")

    a = """
<h3>What the transcript gives us</h3>
""" + ticks([
        "&ldquo;A centre rectangle&hellip; 82 inches and a height of 22 inches&rdquo;",
        "&ldquo;Weldments ▸ Structural Member ▸ ANSI Inch ▸ square tube&hellip; size 0.1875&rdquo;",
        "&ldquo;One hole here and another hole here&hellip; the hole size is 3 inches&rdquo;",
        "&ldquo;The distance is 9.5 inches&hellip; we need 9 patterns&rdquo;",
        "&ldquo;Mirror&hellip; select the Front Plane&rdquo;",
        "&ldquo;Two brackets&hellip; corner rectangle 0.63&hellip; distance between both "
        "rectangles 1.5&hellip; from the origin point 15 inches&hellip; depth 0.4&rdquo;"])

    b = """
<h3>What we decide</h3>
""" + phases([("The holes are pairs",
               "&ldquo;One hole here and another hole here&rdquo; plus &ldquo;3 "
               "inches&rdquo; = two &oslash;0.5 holes at 3 in centres. The tyne, later in "
               "the same video, gets two bolts at 3 in centres. They match."),
              ("0.1875 is the wall, not the size",
               "ANSI square tube is called out as size &times; wall. 0.1875 in is 3/16 "
               "wall; we take the section as 2 &times; 2, the common size for a light "
               "cultivator bar."),
              ("The brackets are lower-link clevises",
               "A pair 1.5 in apart at &plusmn;15 in from centre is a Category-II lower "
               "link spacing of 30 in. That is what it must be.")]) + \
        warn("<strong>Assumption:</strong> the clevis plate is 5&nbsp;in long and rises "
             "3&nbsp;in. The transcript never dimensions it. Both are parameters, so "
             "disagree freely.")

    d.sheet("01", P, "READING THE SOURCE", "What we are building, and why", """
<p class="lede">Before any geometry: settle what the numbers mean. The transcript is a
machine translation of spoken Hindi and some of it is garbled.</p>
""" + cols(a, b), eyebrow="Decisions first")

    a2 = fig("01_frame_01_params_spreadsheet", "SPREADSHEET",
             "15 named parameters. Every dimension in the part refers to one of these.")

    b2 = """
<h3>Build the table first</h3>
""" + steps([("Switch to the <strong>Spreadsheet</strong> workbench and create a sheet",
              "Spreadsheet ▸ Create spreadsheet"),
             ("Type a name in column A, the value in column B, its meaning in column C", ""),
             ("Click the B cell, then <strong>Alias</strong> in the toolbar, and give it a "
              "name", "B2 -> FrameLength"),
             ("Aliased cells turn yellow. That name is now usable in any expression in "
              "this document.", ""),
             ("Back in Part Design, click the small blue circle beside any dimension box "
              "to enter an expression instead of a number",
              "Params.FrameLength")], compact=True) + \
        note("Doing this <em>before</em> the geometry, rather than retro-fitting it, is "
             "what makes it painless. You type <code>Params.FrameLength</code> once, in "
             "the constraint that needs it, and never type 82 again.")

    d.sheet("02", P, "PARAMETERS", "The parameter table", """
<p class="lede">Fifteen numbers define this frame. Put them in a spreadsheet before you
draw a line, and the rest of the part builds itself around them.</p>
""" + cols(a2, b2) + tbl(["Alias", "Value", "Drives"],
                         [["<code>FrameLength</code>", "82 in", "outer rectangle, hole span"],
                          ["<code>FrameDepth</code>", "22 in", "outer rectangle, bar centres"],
                          ["<code>MemberSize</code>", "2 in", "tube across flats, pad height"],
                          ["<code>WallThk</code>", "0.1875 in", "tube bore sketch and depth"],
                          ["<code>HolePitch</code>", "9.5 in", "pattern spacing"],
                          ["<code>HoleCount</code>", "9", "pattern count, first hole position"],
                          ["<code>BoltSpacing</code>", "3 in", "the pair within one station"],
                          ["<code>HitchOffset</code>", "15 in", "clevis position"],
                          ["<code>CornerR</code>", "0.63 in", "clevis nose fillet"]]),
            eyebrow="Do this before you draw")

    a3 = """
<h3>One sketch, two rectangles</h3>
<p>SolidWorks builds this frame with Weldments: draw the four centrelines, then let the
structural-member tool place tube along them. FreeCAD has no such tool, and does not need
one here &mdash; the plan view of a rectangular tube frame <em>is</em> two concentric
rectangles.</p>
""" + steps([("Sketch on <strong>XY_Plane</strong>", ""),
             ("Centred rectangle, 82 &times; 22 &mdash; the outside of the frame", ""),
             ("Second centred rectangle, 78 &times; 18 &mdash; the inside", ""),
             ("Bind all four dimensions to the spreadsheet",
              "Params.FrameLength - 2 * Params.MemberSize"),
             ("<strong>8 lines, 22 constraints, fully constrained</strong>", "")]) + \
        note("The 2&nbsp;in member width falls out of the arithmetic rather than being "
             "dimensioned: inner = outer &minus; 2 &times; MemberSize. Change MemberSize "
             "to 2.5 and the frame re-proportions correctly.")

    b3 = fig("01_frame_03_sketch_plan_constrained", "SKETCH",
             "Two centred rectangles. The ring between them is the steel.") + \
        fig("01_frame_04_pad_frame", "PAD 2 in",
            "Pad the ring 2 in and the four tube members appear at once")

    d.sheet("03", P, "SKETCH + PAD", "The plan, and the first pad", """
<p class="lede">The whole frame outline comes from one sketch and one pad. This is the
FreeCAD replacement for SolidWorks Weldments, and for a four-member rectangle it is
simpler than the thing it replaces.</p>
""" + cols(a3, b3), eyebrow="Two rectangles become four members")

    a4 = """
<h3>The tube is hollow</h3>
<p>What we have is 800&nbsp;in&sup3; of solid bar &mdash; 227&nbsp;lb. Real 2&nbsp;&times;&nbsp;2
&times;&nbsp;3/16 tube is hollow, and the difference matters: 82&nbsp;lb against 227&nbsp;lb
changes what tractor can lift this.</p>
""" + steps([("New sketch on <strong>XY_Plane</strong>", ""),
             ("Set <strong>Attachment Offset ▸ Position ▸ z</strong> to "
              "<code>MemberSize - WallThk</code>", "= 1.8125 in"),
             ("Two more centred rectangles, 81.625 &times; 21.625 and 78.375 &times; 18.375 "
              "&mdash; the bore, 1.625 in wide, centred in the 2 in member", ""),
             ("<strong>Pocket</strong>, length <code>MemberSize - 2 * WallThk</code>",
              "= 1.625 in downward")]) + \
        warn("<strong>Why the offset?</strong> A Pocket cuts <em>from its sketch plane, in "
             "one direction</em>. Sketch on the top face at z&nbsp;=&nbsp;2 and the pocket "
             "eats the top wall. Sketch at z&nbsp;=&nbsp;1.8125 and it starts just below "
             "the top wall, leaving 3/16 in above and 3/16 in below &mdash; a real tube.")

    b4 = fig("01_frame_05_pocket_tube_bore", "POCKET",
             "Invisible from outside, and worth 145 lb") + \
        specs([("Solid bar", "800.0 in&sup3; &mdash; 227 lb"),
               ("Hollow tube", "271.9 in&sup3; &mdash; 77 lb"),
               ("Saved", "66%")]) + \
        note("You cannot see this feature in any render, which is exactly why it is worth "
             "doing. The model's mass is now something you can quote.")

    d.sheet("04", P, "POCKET", "Making the tube hollow", """
<p class="lede">A pocket that starts <em>inside</em> the material. This is the first place
where understanding what a feature actually does &mdash; rather than what its icon looks
like &mdash; changes the answer.</p>
""" + cols(a4, b4), eyebrow="An internal cavity")

    a5 = """
<h3>One station, four holes</h3>
<p>A tyne station is two bolts 3&nbsp;in apart. Both tool bars need the same stations. All
four circles go in <strong>one</strong> sketch.</p>
""" + steps([("Sketch on XY_Plane, attachment offset z = <code>MemberSize</code> "
              "(the top face)", ""),
             ("First circle: &oslash;0.5, positioned from the origin by expression",
              "-(HoleCount - 1) * HolePitch / 2 - BoltSpacing / 2"),
             ("Second circle: same y, <code>+BoltSpacing/2</code>, and "
              "<strong>Equal</strong> to the first", ""),
             ("Two more circles roughly on the rear bar", ""),
             ("<strong>Symmetric</strong> each about the <strong>X axis</strong>, plus "
              "<strong>Equal</strong>", ""),
             ("<strong>Pocket ▸ Through all</strong>", "cuts top wall, cavity, bottom wall")])

    b5 = fig("01_frame_06_sketch_station_holes", "SKETCH",
             "Four circles, ten constraints, zero degrees of freedom") + \
        fig("01_frame_07_pocket_first_station", "POCKET THROUGH ALL",
            "One station drilled through both walls of both bars")

    d.sheet("05", P, "SYMMETRY", "One tyne station", """
<p class="lede">The transcript says &ldquo;one hole here and another hole here&rdquo;, then
&ldquo;the hole size is 3 inches&rdquo;. Three inches is not a diameter &mdash; it is the
spacing. Read it that way and the machine bolts together.</p>
""" + cols(a5, b5) + warn("<strong>Why all four in one sketch?</strong> The tutorial "
                          "mirrors the finished pattern about the Front plane. PartDesign "
                          "will not do that &mdash; you cannot mirror a pattern, and you "
                          "cannot pattern a mirror. The feature goes <em>Invalid</em>. "
                          "Doing the symmetry in the sketch avoids the limitation "
                          "entirely. Deck 11 goes into it properly."),
            eyebrow="Read the numbers correctly")

    a6 = """
<h3>Pattern the pocket, not the sketch</h3>
""" + steps([("Select the <strong>Pocket</strong> in the tree", ""),
             ("<strong>Part Design ▸ Apply a pattern ▸ LinearPattern</strong>", ""),
             ("Direction: the body's <strong>X axis</strong>", ""),
             ("Mode <strong>Extent</strong>, length <code>(HoleCount - 1) * HolePitch</code>",
              "= 76 in"),
             ("Occurrences <code>HoleCount</code>", "= 9"),
             ("OK. 36 holes.", "")]) + \
        note("<strong>Extent</strong> means &ldquo;spread N copies across this total "
             "length&rdquo;, not &ldquo;space them this far apart&rdquo;. The other mode, "
             "<strong>Spacing</strong>, does the latter. Pick Extent here so that changing "
             "HoleCount keeps the holes inside the frame.")

    b6 = fig("01_frame_08_linear_pattern_holes", "PLAN",
             "Nine stations at 9.5 in pitch on both bars &mdash; one feature, one row of "
             "numbers") + \
        specs([("Occurrences", "9"), ("Pitch", "9.5 in"), ("Span", "76 in"),
               ("Holes", "36"), ("End margin", "3 in")])

    d.sheet("06", P, "LINEAR PATTERN", "Nine stations", """
<p class="lede">One station becomes nine. Both the count and the pitch come from the
spreadsheet, so a wider frame with more tynes is a two-cell edit.</p>
""" + cols(a6, b6), eyebrow="One feature, nine stations")

    a7 = """
<h3>A clevis is two plates and a gap</h3>
<p>Each lower link needs a fork for its ball end: two plates 1.5&nbsp;in apart, 0.4&nbsp;in
thick, straddling the tool bar and projecting forward.</p>
""" + steps([("Sketch on <strong>YZ_Plane</strong> &mdash; the plane across the machine",
              ""),
             ("Attachment offset z = <code>HitchOffset + HitchGap/2</code>",
              "= 15.75 in, the inner face of the outer plate"),
             ("Rectangle: 5 in fore-aft &times; 3 in tall, its rear edge on the bar's "
              "rear face", ""),
             ("<strong>Pad</strong> 0.4 in", ""),
             ("Repeat at <code>HitchOffset - HitchGap/2</code> with "
              "<strong>Reversed</strong> ticked", "= 14.25 in, padding the other way")]) + \
        note("Two sketches rather than one padded symmetrically, because the 1.5&nbsp;in "
             "<em>gap</em> is the dimension that matters &mdash; it has to clear the "
             "tractor's link ball. Modelling the gap directly means it stays right when "
             "the plate thickness changes.")

    b7 = fig("01_frame_10_sketch_clevis_plate", "SKETCH ON YZ",
             "The plate profile, located from the origin. Note the sketch is 15.75 in out "
             "along X, not on the plane itself.") + \
        fig("01_frame_11_pad_clevis_pair", "PAD &times; 2",
            "Both plates, straddling the front tool bar")

    d.sheet("07", P, "PAD ON AN OFFSET PLANE", "The hitch clevis", """
<p class="lede">The first feature that is not on an origin plane. Attachment offsets do all
the work &mdash; no datum planes required.</p>
""" + cols(a7, b7), eyebrow="Sketch attachment, properly used")

    a8 = """
<h3>The pin hole</h3>
""" + steps([("Sketch on <strong>YZ_Plane</strong>, offset z = <code>HitchOffset</code>",
              "= 15 in, midway between the plates"),
             ("&oslash;1 in circle, 1 in ahead of the frame's front face, at half the "
              "plate height", ""),
             ("<strong>Pocket ▸ Through all</strong> with <strong>Symmetric to "
              "plane</strong> ticked", "cuts both ways from the mid-plane")]) + \
        note("Symmetric + Through all cuts to infinity in <em>both</em> directions from the "
             "sketch plane, so one feature drills both plates. The hole sits forward of the "
             "tube so the pin never fouls the bar &mdash; check that in the Right view "
             "before you move on.")

    b8 = """
<h3>Then mirror the whole clevis</h3>
""" + steps([("Select the two Pads and the Pocket &mdash; all three", ""),
             ("<strong>Part Design ▸ Mirrored</strong>", ""),
             ("Mirror plane: <strong>YZ_Plane</strong> (base plane)", ""),
             ("OK &mdash; a matching clevis appears at &minus;15 in", "")]) + \
        fig("01_frame_13_mirror_clevis", "MIRRORED",
            "Both clevises, 30 in apart &mdash; Category II lower link spacing") + \
        warn("This mirror works because the three features it copies are ordinary pads and "
             "pockets. Try to mirror the <em>hole pattern</em> the same way and it fails "
             "&mdash; see Deck 11.")

    d.sheet("08", P, "POCKET + MIRRORED", "Pin hole, then mirror", """
<p class="lede">Build one side properly, then mirror. Half the modelling, and the two sides
can never drift apart.</p>
""" + cols(a8, b8), eyebrow="Build one, mirror it")

    a9 = """
<h3>The fillet that failed</h3>
<p>The transcript asks for a &ldquo;complete circular fillet&rdquo; on three faces &mdash;
SolidWorks' <em>full-round fillet</em>, which replaces a face entirely with a half round.
FreeCAD has no such option, so we round the corners instead. First attempt:</p>
""" + code("""
Selected: the 8 vertical edges at the clevis nose
Radius:   0.63 in   (Params.CornerR)

  Fillet_ClevisNose  ['Touched', 'Invalid']
  Shape is null
""") + """
<p>The nose face is only <strong>0.4&nbsp;in</strong> wide &mdash; the plate thickness. A
0.63&nbsp;in fillet on each of its two edges needs 1.26&nbsp;in of face to consume. There
is not enough material, so OpenCASCADE refuses. Correctly.</p>
"""

    b9 = """
<h3>The fix</h3>
<p>Round the <strong>profile</strong> corners instead &mdash; the edges running through the
plate thickness, at the top and bottom of the nose. The plate is 5&nbsp;in long and
3&nbsp;in tall there, so R0.63 fits easily.</p>
""" + code("""
Selected: the 8 edges parallel to X at y = -14 in
Radius:   0.63 in

  Fillet_ClevisNose  ['Up-to-date']
  289.79 -> 289.52 in3
""") + fig("01_frame_14_fillet_clevis_nose", "FILLET R0.63",
           "Both nose corners rounded, on all four plates, in one feature") + \
        note("<strong>The lesson is not the fillet.</strong> It is that FreeCAD tells you "
             "when geometry is impossible instead of quietly producing something wrong. "
             "An <em>Invalid</em> feature is information.")

    d.sheet("09", P, "FILLET", "A fillet that cannot exist", """
<p class="lede">Worth walking through in full, because it is the most common way a
beginner's model breaks and the error message does not explain itself.</p>
""" + cols(a9, b9), eyebrow="When FreeCAD says no")

    a10 = """
<h3>Check the result</h3>
""" + specs([("Bodies", "1"), ("Sketches", "6"), ("Features", "8"),
             ("Volume", "289.5 in&sup3;"), ("Mass @ 0.284 lb/in&sup3;", "82.2 lb"),
             ("Bounding box", "82 &times; 25 &times; 3 in")]) + """
<p>The 25&nbsp;in depth is the 22&nbsp;in frame plus 3&nbsp;in of clevis projecting ahead
of it. If that number had come out at 22, the clevises would not be there.</p>
""" + ticks([
        "Every sketch reports <strong>fully constrained</strong>",
        "No feature is marked Invalid or Touched",
        "Mass is plausible for 2 &times; 2 &times; 3/16 tube: about 4.3 lb/ft &times; "
        "~19 ft = 82 lb &mdash; it checks out"])

    b10 = plates([("01_frame_final_Top", "PLAN", "9 stations, 4 holes each"),
                  ("01_frame_final_Front", "FRONT", "82 in span, 2 in deep section"),
                  ("01_frame_final_Right", "RIGHT", "22 in bar centres, clevis projecting"),
                  ("01_frame_final_Isometric", "ISOMETRIC", "Part 1 complete")], "grid-2")

    d.sheet("10", P, "VERIFY", "Part 1 complete", """
<p class="lede">Always finish a part by checking it numerically, not just by looking at it.
A model that looks right and weighs three times what it should is a model with a mistake
in it.</p>
""" + cols(a10, b10), eyebrow="Check the numbers")

    return d
