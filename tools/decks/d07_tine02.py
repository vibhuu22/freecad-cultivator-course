# -*- coding: utf-8 -*-
"""Deck 7 - Part 3, Tine 02."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("07-part3-tine02", "Part 3: Tine 02", "Deck 7")

    d.cover("Part 3: Tine 02", split(
        shot("03_tine02_final_Right", "One continuous curve on a 16 inch radius"),
        stack(
            lede("The curved tyne for the back row. Four of them. A simpler "
                 "sketch than Tine 01, and a neater shape."),
            facts([("Radius", "16 in"), ("Working height", "15 in"),
                   ("Bar", "2.5 &times; 1.25 in"), ("Weight", "22.1 lb")]))))

    d.slide("Three numbers that check each other", split(
        shot("03_tine02_final_Right", "Radius, working height and chord all agree"),
        stack(
            lede("The tutorial gives three dimensions for the same arc. That is "
                 "a gift &mdash; you can check your reading before you draw."),
            points([
                "&ldquo;A radius of 16 inches on both sides&rdquo;",
                "&ldquo;The height from this point to this point is 15 inches&rdquo;",
                "&ldquo;From this point to the midpoint of the outer arc: 20.3 "
                "inches&rdquo;"]),
            callout("Take the radius and the height as given. The straight "
                    "distance across the arc then works out at 19.7 inches. The "
                    "tutorial says 20.3. Three per cent apart, so our reading is "
                    "right."))),
            eyebrow="Cross-check before you draw")

    d.slide("The profile", split(
        shot("03_tine02_01_sketch_profile",
             "Four lines and two arcs. Fully constrained first time."),
        stack(
            lede("Two arcs sharing a centre, joined by four straight lines."),
            points([
                "A flat top edge, 2.5 inches wide, centred on the origin.",
                "Two short straight sides before the curve begins.",
                "Two arcs sharing a centre, so the bar keeps the same width all "
                "the way down.",
                "A flat end for the point."]),
            callout("The point has to sit square across the bar. Rather than an "
                    "angle, tell FreeCAD that the arcs' shared "
                    "<strong>centre point</strong> lies on the end line. A line "
                    "through the centre of a circle is square to it by "
                    "definition."))),
            eyebrow="Simpler than Tine 01")

    d.slide("Let the spreadsheet do the arithmetic", split(
        shot("03_tine02_00_params",
             "Thirteen cells, and three of them are formulas"),
        stack(
            lede("The sweep angle of the curve is not a design decision. It "
                 "follows from the radius and the working depth."),
            table(["Cell", "Value"],
                  [["Curve radius", "16 in &mdash; your choice"],
                   ["Working height", "15 in &mdash; your choice"],
                   ["Bar width", "2.5 in &mdash; your choice"],
                   ["Sweep angle", "worked out from the first two"],
                   ["Outer radius", "radius plus half the bar width"],
                   ["Point height", "worked out from all of them"]]),
            callout("Change the working height to 12 inches and the sweep, the "
                    "outer radius and the point height all follow. The tyne "
                    "stays a proper arc."))),
            eyebrow="Derived numbers")

    d.slide("From outline to solid", split(
        shot("03_tine02_03_pad_head",
             "The shank padded 1.25 inches, with the same 5 inch head as Tine 01"),
        stack(
            lede("Three of the four steps are exactly what you did on Tine 01."),
            steps([
                ("<strong>Pad</strong> the profile, symmetric", "1.25 in"),
                ("Sketch the head on the XY plane and pad it down", "5 &times; 2.5 in"),
                ("Two half-inch holes, 3 inches apart, pocketed through", "same as Tine 01"),
                ("<strong>Fillet</strong> the two corners of the point", "R1")]),
            callout("The bolt interface is deliberately identical. Either tyne "
                    "fits any of the eighteen stations on the frame &mdash; "
                    "which is how a real cultivator works, and it costs nothing "
                    "to design in."))),
            eyebrow="Reusing the interface")

    d.slide("Rounding the point", split(
        shot("03_tine02_05_fillet_point", "Both corners rounded in one feature"),
        stack(
            lede("A 1 inch radius on a 2.5 inch bar makes the point very nearly "
                 "a half-round."),
            points([
                "A sharp corner on a wear part is where cracks start.",
                "It is also where the blade bolts on, and a rounded seat "
                "spreads the load.",
                "In soil a sharp corner wears round within an hour anyway."]),
            warn("Picking the two edges by eye is fine once. It is not "
                 "repeatable &mdash; change something upstream and the edges "
                 "get renumbered. Keep dress-up features to the end of the "
                 "tree, and few."))),
            eyebrow="Fillet")

    d.slide("The two tynes compared", split(
        shots([("02_tine01_final_Right", "Tine 01, front row"),
               ("03_tine02_final_Right", "Tine 02, back row")]),
        stack(
            lede("Two different shapes, one shared bolt pattern."),
            table(["", "Tine 01", "Tine 02"],
                  [["Row", "front, 5 off", "rear, 4 off"],
                   ["Shape", "straight, bend, foot", "one curve"],
                   ["Bar", "2.25 &times; 1.5 in", "2.5 &times; 1.25 in"],
                   ["Reaches forward", "3.6 in", "10.4 in"],
                   ["Weight each", "26.6 lb", "22.1 lb"]]),
            callout("The rear tyne reaches much further forward. Mounted 20 "
                    "inches behind the front row, that leaves about 13 inches "
                    "between the two sets of points &mdash; enough for trash to "
                    "clear."))),
            eyebrow="Part 3 done")

    return d
