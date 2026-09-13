# -*- coding: utf-8 -*-
"""Deck 6 - Part 2, Tine 01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("06-part2-tine01", "Part 2: Tine 01", "Deck 6")

    d.cover("Part 2: Tine 01", split(
        shot("02_tine01_final_Right", "Straight down 15 inches, then a smooth bend forward"),
        stack(
            lede("The rigid tyne for the front row. Five of them. The whole "
                 "shape comes from one sketch."),
            facts([("Length", "25 in"), ("Straight part", "15 in"),
                   ("Bar", "2.25 &times; 1.5 in"), ("Weight", "26.6 lb")]))))

    d.slide("Making the numbers agree", split_even(
        stack(
            heading("What the tutorial says"),
            points([
                "&ldquo;Length: 25 inches&rdquo;",
                "&ldquo;The height between these two points is 15 inches&rdquo;",
                "&ldquo;Distance between the two points: 2.25 inches&rdquo;",
                "&ldquo;Dimension: 1.5 inches&rdquo;",
                "&ldquo;Two holes 0.5 inches, 3 inches apart&rdquo;"])),
        stack(
            lede("Twenty-five inches and fifteen inches are both stated. They "
                 "only make sense together."),
            points([
                "<strong>25 inches</strong> is the whole tyne, measured along "
                "the bar.",
                "<strong>15 inches</strong> is the straight part at the top.",
                "The bend and the foot make up the remaining 10 inches."]),
            warn("The rake angle and the bend radius are <strong>our "
                 "choice</strong> &mdash; the tutorial gives neither. We use "
                 "35 degrees and a 6 inch inner radius. Both are spreadsheet "
                 "numbers, so change them if you disagree."))),
            eyebrow="Reading the source")

    d.slide("The profile", split(
        shot("02_tine01_02_sketch_profile",
             "Six lines and two arcs, held by twenty rules"),
        stack(
            lede("Drawn on the <strong>YZ plane</strong> &mdash; the one "
                 "SolidWorks calls Right."),
            points([
                "A flat top edge, 2.25 inches wide, centred on the origin.",
                "Two straight sides going down 15 inches.",
                "Two arcs that share the same centre, so the bar keeps the same "
                "width all the way round the bend.",
                "Two straight sides for the foot, and a flat end for the point."]),
            callout("Only <strong>one</strong> radius is dimensioned. The outer "
                    "arc follows automatically, because the two arcs share a "
                    "centre and the bar is 2.25 inches wide."))),
            eyebrow="One sketch, the whole shape")

    d.slide("Two rules people forget", split(
        shot("02_tine01_02_sketch_profile",
             "Zero degrees of freedom. Nothing in here can move."),
        stack(
            lede("Twenty rules pin this sketch down. These are the two that "
                 "are easy to miss."),
            points([
                "<strong>Parallel on the two sides of the foot.</strong> "
                "Without it the sketch still moves. Tangency alone does not "
                "hold an arc's end in place.",
                "<strong>Symmetric about the origin point.</strong> Select the "
                "two top corners and the origin, press <code>S</code>, and the "
                "whole profile centres itself in one go."]),
            warn("At the four smooth joins use endpoint tangency <em>only</em>. "
                 "Adding a coincident rule as well makes the two fight, and the "
                 "sketch then produces no shape at all."))),
            eyebrow="Constraints")

    d.slide("Dimension the reach, not the angle", split(
        shots([("02_tine01_final_Right", "Dimensioned by reach: correct"),
               ("02_tine01_final_Isometric", "The finished tyne")]),
        stack(
            lede("We first tried an angle constraint for the rake. The solver "
                 "flipped the foot backwards."),
            points([
                "&ldquo;35 degrees between these lines&rdquo; is true of the "
                "tyne <em>and</em> its mirror image.",
                "The sketch reported fully constrained and no errors. It was "
                "just the wrong shape.",
                "Saying <em>the point reaches 3.6 inches forward</em> has only "
                "one answer."]),
            callout("The rake angle is still a named parameter. It drives the "
                    "reach through a formula in the spreadsheet, so you can "
                    "still type 30 degrees and get a 30 degree tyne."))),
            eyebrow="The trap from Deck 4, in practice")

    d.slide("From outline to solid", split(
        shot("02_tine01_04_pad_head",
             "The shank padded 1.5 inches, with the mounting head added on top"),
        stack(
            lede("Two pads. The first makes the tyne, the second widens the top "
                 "so it can be bolted down."),
            steps([
                ("<strong>Pad</strong> the profile, with <strong>Symmetric to "
                 "plane</strong> ticked", "1.5 in"),
                "New sketch on the <strong>XY plane</strong>",
                ("Centred rectangle, 5 inches along the bar", "5 &times; 2.25 in"),
                ("<strong>Pad</strong> it downwards, with "
                 "<strong>Reversed</strong> ticked", "1.25 in")]),
            callout("Pad symmetrically so the tyne sits centred on whatever you "
                    "position it with. Pad it one way and every placement in "
                    "the assembly carries a correction you will forget."))),
            eyebrow="Pads")

    d.slide("The mounting bolts", split(
        shot("02_tine01_05_sketch_bolt_holes",
             "Two circles, held together by one symmetric rule and one equal rule"),
        stack(
            lede("Two half-inch holes, 3 inches apart. The same 3 inches that "
                 "is drilled in the frame."),
            steps([
                "Sketch on the <strong>XY plane</strong>",
                ("Circle at half the bolt spacing from the centre", "1.5 in"),
                "Second circle made <strong>Symmetric</strong> about the Y "
                "axis, and <strong>Equal</strong>",
                "<strong>Pocket, through all</strong>"]),
            callout("This is the joint that holds the machine together. It is "
                    "worth checking against the frame before you go on &mdash; "
                    "same diameter, same spacing."))),
            eyebrow="The interface to Part 1")

    d.slide("Check it before you move on", split(
        shots([("02_tine01_final_Front", "From the front: 1.5 in bar, 5 in head"),
               ("02_tine01_final_Isometric", "Part 2 finished")]),
        stack(
            lede("The bounding box is the quickest check that the shape came "
                 "out as intended."),
            facts([("Height", "24.4 in"), ("Depth", "6.6 in"),
                   ("Width", "5.0 in"), ("Weight", "26.6 lb")]),
            points([
                "Height is under 25 inches because the shank curves forward. "
                "Correct.",
                "Width is exactly 5 inches, which is the head. Correct.",
                "Five tynes weigh 133 pounds &mdash; a third of the whole "
                "machine."]))),
            eyebrow="Part 2 done")

    return d
