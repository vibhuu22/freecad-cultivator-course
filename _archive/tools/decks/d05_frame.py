# -*- coding: utf-8 -*-
"""Deck 5 - Part 1, the frame."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("05-part1-frame", "Part 1: The Frame", "Deck 5")

    d.cover("Part 1: The Frame", split(
        shot("01_frame_final_Isometric", "82 inches long, 22 inches deep, 82 pounds"),
        stack(
            lede("The frame carries everything. It is welded from square tube, "
                 "and building it teaches most of Part Design."),
            facts([("Size", "82 &times; 22 in"),
                   ("Tube", "2 &times; 2 in"),
                   ("Wall", "3/16 in"),
                   ("Bolt holes", "36"),
                   ("Weight", "82 lb")]))))

    d.slide("What the tutorial gives us", split_even(
        stack(
            heading("What it says"),
            points([
                "&ldquo;A centre rectangle, 82 inches and a height of 22 inches&rdquo;",
                "&ldquo;Square tube, size 0.1875&rdquo;",
                "&ldquo;One hole here and another hole here&rdquo;",
                "&ldquo;The hole size is 3 inches&rdquo;",
                "&ldquo;The distance is 9.5 inches, we need 9 patterns&rdquo;"])),
        stack(
            heading("What we make of it"),
            points([
                "<strong>Each station is a pair of holes,</strong> 3 inches "
                "apart. The 3 inches is the spacing, not a diameter.",
                "The tyne, later in the same video, gets two bolts 3 inches "
                "apart. They match, so the machine bolts together.",
                "<strong>0.1875 is the wall thickness,</strong> not the tube "
                "size. We use 2 &times; 2 inch tube, which is normal for a "
                "light cultivator."]),
            warn("The brackets at each end are the tractor's lower link points. "
                 "A pair 15 inches out from the centre gives 30 inches between "
                 "them, which is the standard spacing."))),
            eyebrow="Reading the source")

    d.slide("Put the numbers in a spreadsheet first", split(
        shot("01_frame_01_params_spreadsheet",
             "Fifteen numbers. Nothing in the frame is typed anywhere else."),
        stack(
            lede("Before you draw a line, write the dimensions into a "
                 "spreadsheet and give each one a name."),
            steps([
                "Switch to the <strong>Spreadsheet</strong> workbench and "
                "create a sheet",
                ("Type the name, the value <em>with its unit</em>, and what it "
                 "means", "82 in"),
                "Click the value cell and press <strong>Alias</strong>, then "
                "type the name",
                ("Later, in any dimension box, click the small blue circle and "
                 "type the name", "Params.FrameLength")]),
            callout("Do this first and it is painless. Retro-fitting it to a "
                    "finished part is a chore."))),
            eyebrow="Parameters")

    d.slide("The outline: two rectangles", split(
        shot("01_frame_04_pad_frame",
             "Pad the ring 2 inches and all four members appear at once"),
        stack(
            lede("Seen from above, a rectangular tube frame is just two "
                 "rectangles, one inside the other."),
            steps([
                "Sketch on the <strong>XY plane</strong>",
                "Centred rectangle, 82 &times; 22 &mdash; the outside",
                "Second centred rectangle, 78 &times; 18 &mdash; the inside",
                ("<strong>Pad</strong> the ring 2 inches", "= tube size")]),
            callout("SolidWorks would use the Weldments tool here. FreeCAD has "
                    "no equivalent, and for a four-sided frame it does not need "
                    "one."))),
            eyebrow="Sketch and pad")

    d.slide("Making the tube hollow", split(
        shot("01_frame_05_pocket_tube_bore",
             "You cannot see this cut from outside, and it saves 145 pounds"),
        stack(
            lede("Right now the frame is solid bar and weighs 227 pounds. Real "
                 "tube is hollow."),
            steps([
                "New sketch on the XY plane",
                ("Set its <strong>attachment offset</strong> so it floats just "
                 "under the top wall", "z = 1.8125 in"),
                "Draw two more rectangles: the inside of the tube walls",
                ("<strong>Pocket</strong> down through the middle", "1.625 in")]),
            warn("A pocket cuts <em>from its sketch plane, downwards</em>. If "
                 "you sketch on the top face, the pocket eats the top wall. "
                 "Start it just below the wall instead and you get a proper "
                 "hollow tube."))),
            eyebrow="A cut that starts inside the metal")

    d.slide("One tyne station", split(
        shot("01_frame_06_sketch_station_holes",
             "Four circles, ten rules, nothing able to move"),
        stack(
            lede("A tyne station is two bolts, 3 inches apart. Both bars need "
                 "the same stations."),
            steps([
                ("Sketch on the XY plane, offset up to the top face", "z = 2 in"),
                "First circle, half an inch across, positioned from the origin",
                ("Second circle 3 inches along, and <strong>Equal</strong> to "
                 "the first", "3 in"),
                "Two more circles, made <strong>Symmetric</strong> about the "
                "X axis, for the rear bar",
                "<strong>Pocket, through all</strong>"]),
            callout("All four holes go in one sketch. Deck 11 explains why "
                    "&mdash; it saves a real headache further on."))),
            eyebrow="Symmetry doing the work")

    d.slide("Nine stations from one", split(
        shot("01_frame_08_linear_pattern_holes",
             "Thirty-six holes from a single pattern feature"),
        stack(
            lede("One station becomes nine, and both the count and the spacing "
                 "come from the spreadsheet."),
            steps([
                "Select the <strong>pocket</strong> in the tree",
                "<strong>Part Design &rsaquo; LinearPattern</strong>",
                "Direction: the body's <strong>X axis</strong>",
                ("Mode <strong>Extent</strong>, length 76 inches", "8 &times; 9.5"),
                ("Occurrences: <strong>9</strong>", "including the original")]),
            callout("<strong>Extent</strong> spreads the copies across a total "
                    "length. <strong>Spacing</strong> puts a fixed gap between "
                    "them. Use Extent here, so changing the count keeps the "
                    "holes on the frame."))),
            eyebrow="Linear pattern")

    d.slide("The hitch brackets", split(
        shot("01_frame_11_pad_clevis_pair",
             "Both plates, straddling the front tool bar"),
        stack(
            lede("Each lower link needs a fork: two plates with a gap between "
                 "them for the tractor's ball end."),
            steps([
                "Sketch on the <strong>YZ plane</strong>",
                ("Offset it out to where the first plate face goes", "15.75 in"),
                "Draw the plate outline: 5 inches long, 3 inches tall",
                ("<strong>Pad</strong> it", "0.4 in"),
                "Repeat on the other side of the gap, with "
                "<strong>Reversed</strong> ticked"]),
            callout("We model the 1.5 inch <em>gap</em> directly, because that "
                    "is the dimension that has to fit the tractor."))),
            eyebrow="Sketching away from the plane")

    d.slide("Pin hole, then mirror", split(
        shot("01_frame_13_mirror_clevis",
             "Both brackets, 30 inches apart, from one mirror"),
        stack(
            lede("Build one side properly, then mirror it. Half the work, and "
                 "the two sides can never drift apart."),
            steps([
                ("Sketch a 1 inch circle on the YZ plane, halfway between the "
                 "plates", "15 in"),
                "<strong>Pocket, through all</strong>, with "
                "<strong>Symmetric to plane</strong> ticked",
                "Select both pads and the pocket",
                "<strong>Part Design &rsaquo; Mirrored</strong>, about the "
                "<strong>YZ plane</strong>"]),
            callout("Symmetric plus Through all cuts both ways at once, so one "
                    "feature drills both plates."))),
            eyebrow="Mirrored")

    d.slide("A fillet that cannot exist", split(
        shot("01_frame_14_fillet_clevis_nose",
             "Both corners of every bracket nose, rounded in one feature"),
        stack(
            lede("The tutorial asks for a rounded end on the bracket. Our first "
                 "attempt failed, and it is worth understanding why."),
            points([
                "We asked for a 0.63 inch round on the two edges of the "
                "bracket nose.",
                "The nose is only <strong>0.4 inches wide</strong> &mdash; the "
                "plate thickness. There is not enough metal, so FreeCAD "
                "refused.",
                "The fix is to round the <em>corners of the outline</em> "
                "instead, where the plate is 3 inches tall."]),
            warn("SolidWorks has a full-round fillet that replaces a face with "
                 "a half-round. FreeCAD does not. Rounding both corners gets "
                 "you the same look."))),
            eyebrow="When FreeCAD says no")

    d.slide("Check it before you move on", split(
        shots([("01_frame_final_Top", "From above: nine stations"),
               ("01_frame_final_Front", "From the front: 82 inches")]),
        stack(
            lede("Always finish a part by checking the numbers, not just by "
                 "looking at it."),
            facts([("Sketches", "6"), ("Features", "8"),
                   ("Volume", "289.5 in&sup3;"), ("Weight", "82.2 lb")]),
            points([
                "Every sketch says <strong>fully constrained</strong>.",
                "No feature is marked failed.",
                "Two by two inch tube weighs about 4.3 lb per foot. Nineteen "
                "feet of it is 82 pounds. That checks out."]))),
            eyebrow="Part 1 done")

    return d
