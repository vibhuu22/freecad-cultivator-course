# -*- coding: utf-8 -*-
"""Deck 9 - Parts 6 and 7, the blades."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("09-parts67-blades", "Parts 6 and 7: The Blades", "Deck 9")

    d.cover("Parts 6 and 7: The Blades", split(
        shot("06_blade01_final_Isometric", "13 inches across, bent on a 10 inch radius"),
        stack(
            lede("The sweeps that do the cutting. Thin curved plates with the "
                 "cutting edges swept back."),
            facts([("Span", "13 in"), ("Length", "4 in"),
                   ("Thickness", "0.2 in"), ("Edge angle", "13&deg;")]))))

    d.slide("SolidWorks bends them. FreeCAD cannot.", split_even(
        stack(
            heading("What the tutorial does"),
            points([
                "Builds the blade flat.",
                "Runs <strong>Flex &rsaquo; Bending</strong> to warp it around "
                "a radius.",
                "Blade 02 is the same thing bent on 16 inches instead of 10."]),
            warn("FreeCAD has no Flex. Not in Part Design, not in Part, not in "
                 "any add-on. If you went looking for the button, it is not "
                 "there.")),
        stack(
            heading("What we do instead"),
            points([
                "Build the blade <strong>already curved</strong>.",
                "Draw an arc of the radius we want, and sweep the blade's "
                "cross-section along it.",
                "Then cut the plan shape out of the curved plate."]),
            callout("This is not a workaround. It is the better model. The bend "
                    "radius becomes a number you can name and change, instead "
                    "of an operation applied afterwards."))),
            eyebrow="The one real gap")

    d.slide("The arc the blade is bent on", split(
        shot("06_blade_01_sketch_spine",
             "One arc, five rules, fully constrained"),
        stack(
            lede("A single arc on the YZ plane. It starts flat at the cutting "
                 "edge and lifts towards the back."),
            steps([
                "Draw an arc roughly where the blade goes",
                "Position its start point from the origin",
                ("Dimension the <strong>radius</strong> from the spreadsheet",
                 "10 in"),
                "Force the arc's centre directly above its start, so the blade "
                "leaves the cutting edge flat",
                "Position the end point"]),
            callout("We measure the blade's 4 inch length <em>around the "
                    "curve</em>, not straight across. That is how much steel it "
                    "takes, so that is the number to fix."))),
            eyebrow="The spine")

    d.slide("Sweep the section along it", split(
        shot("06_blade_03_additive_pipe",
             "A curved plate, before the shape is cut out of it"),
        stack(
            lede("Same tool as the clamps: <strong>Additive Pipe</strong>."),
            points([
                "The section is a plain rectangle, 13 inches by 0.2 inches.",
                "It sits on the XZ plane, offset forward to the start of the "
                "arc.",
                "Sweep it, and you have a curved plate."]),
            table(["Check", "Expected", "Got"],
                  [["Across", "13 in", "13.00"],
                   ["Front to back", "under 4 in, because it curves", "3.93"],
                   ["Height", "the curvature, plus 0.2 sheet", "0.98"]]))),
            eyebrow="The sweep")

    d.slide("Cutting the duckfoot shape", split(
        shot("06_blade_04_sketch_plan_shape",
             "Two closed shapes in one sketch: the stock, and the blade outline inside it"),
        stack(
            lede("A sweep comes to a point in the middle and its edges rake "
                 "back, so soil and trash slide off."),
            points([
                "The cutting edges sweep back at <strong>13 degrees</strong>.",
                "Over a 6.5 inch half-width, 13 degrees lifts the outer corners "
                "<strong>1.5 inches</strong>.",
                "The tutorial separately quotes a 1.5 inch gap. Two numbers, "
                "same answer &mdash; so we have read it right."]),
            callout("To cut everything <em>outside</em> a shape, draw a big "
                    "rectangle and the blade outline inside it, in one sketch. "
                    "A pocket then removes the ring between them."))),
            eyebrow="The plan shape")

    d.slide("Blade 02 is one number", split(
        shots([("07_blade02_00_before_edit", "Radius 10: Blade 01"),
               ("07_blade02_01_after_edit", "Radius 16: Blade 02")]),
        stack(
            lede("Open the spreadsheet. Change the bend radius from 10 to 16. "
                 "Recompute. That is the whole of Part 7."),
            points([
                "The arc flattens, and the swept plate follows.",
                "The plan-shape pocket re-cuts the same outline out of the new "
                "surface.",
                "Same 13 inch span, same 4 inches of steel, same weight."]),
            callout("This is exactly the edit the SolidWorks tutorial makes by "
                    "re-running Flex. Here it costs one cell &mdash; which is "
                    "the whole argument for building it curved."))),
            eyebrow="The payoff")

    d.slide("What we left out", split(
        shot("06_blade01_final_Top",
             "The finished sweep, seen from above"),
        stack(
            lede("Two things a real sweep has that this model does not."),
            points([
                "<strong>Bolt holes.</strong> The tutorial never dimensions "
                "them, so we did not guess. That is exercise 4.",
                "<strong>A ground edge.</strong> A real sweep is sharpened "
                "underneath along the leading edges."]),
            facts([("Each", "2.4 lb"), ("Nine of them", "21.6 lb"),
                   ("Share of machine", "under 6%")]),
            callout("These are the only parts that wear out and get replaced, "
                    "so they are worth getting right when you take this "
                    "further."))),
            eyebrow="Parts 6 and 7 done")

    return d
