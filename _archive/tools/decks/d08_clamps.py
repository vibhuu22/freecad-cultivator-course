# -*- coding: utf-8 -*-
"""Deck 8 - Parts 4 and 5, the clamps."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("08-parts45-clamps", "Parts 4 and 5: The Clamps", "Deck 8")

    d.cover("Parts 4 and 5: The Clamps", split(
        shots([("04_clamp01_final_Isometric", "Clamp 01"),
               ("05_clamp02_final_Isometric", "Clamp 02")]),
        stack(
            lede("Two bent steel straps, 3 inches wide and half an inch thick. "
                 "They brace the frame."),
            facts([("Strap", "3 &times; 0.5 in"), ("Corners", "R2"),
                   ("Hole", "1 in"), ("Weight", "12 and 14 lb")]))))

    d.slide("Two ways to make a bent strap", split_even(
        stack(
            heading("How the tutorial does it"),
            steps([
                "Draw the bent centre line",
                "Round the corners",
                ("Use <strong>Offset Entities</strong> to push a copy inward",
                 "0.5 in"),
                "Close the two ends to make a closed shape",
                ("Extrude it", "3 in")])),
        stack(
            heading("How we do it"),
            steps([
                "Draw the bent centre line",
                "Round the corners",
                "Draw the strap's cross-section on a separate sketch",
                "<strong>Additive Pipe</strong>: push the section along the line"]),
            callout("Same solid either way. But now the model knows the "
                    "<em>section</em> and the <em>path</em> as two separate "
                    "things you can edit. Change the section to 4 by 3/8 and "
                    "the strap re-sweeps along the same path."))),
            eyebrow="Offset, or sweep?")

    d.slide("Additive Pipe replaces two SolidWorks tools", split(
        shot("04_clamp01_03_additive_pipe",
             "One feature: the whole strap, bends included"),
        stack(
            lede("Push a shape along a path. That is all a sweep is, and it "
                 "covers a lot of ground."),
            points([
                "It replaces <strong>Offset Entities</strong> for making a "
                "strap out of a line.",
                "It replaces <strong>Weldments</strong> for making a beam out "
                "of a path &mdash; a structural member is a section swept along "
                "a line.",
                "It is how we build the curved blades in the next deck."]),
            callout("The rounded corners come out of the sweep itself. There is "
                    "no separate fillet feature to add or to break."))),
            eyebrow="The tool worth learning here")

    d.slide("The path", split(
        shot("04_clamp01_01_sketch_path",
             "Three lines and two rounded corners, fully constrained"),
        stack(
            lede("Three straight runs from the origin. Dimension each one by "
                 "how far it goes across and how far up."),
            steps([
                "Draw three connected lines starting at the origin",
                "Make the first <strong>vertical</strong> and the last "
                "<strong>horizontal</strong>",
                "Dimension each run and rise, rather than a length and an angle",
                ("Round the two corners", "R2")]),
            warn("When you round a corner, tick <strong>create corner</strong>. "
                 "The fillet trims the lines back, so without it your "
                 "18&nbsp;inch dimension quietly starts measuring the trimmed "
                 "line instead of the real one."))),
            eyebrow="Sketching the bend")

    d.slide("The radius the fillet forgets", split(
        shot("04_clamp01_01_sketch_path",
             "Two rounded corners, each with its radius dimensioned"),
        stack(
            lede("Rounding a corner in a sketch creates the arc but does not "
                 "dimension it."),
            points([
                "Before the fillets the sketch was fully constrained.",
                "After two fillets it can move again &mdash; one loose end per "
                "corner.",
                "Add a <strong>Radius</strong> dimension to each new arc and it "
                "is solid again."]),
            callout("This is the single most commonly forgotten step in the "
                    "whole Sketcher. Look at the message in the Sketcher panel "
                    "after every fillet."))),
            eyebrow="Check after you fillet")

    d.slide("The section, and where it sits", split(
        shot("04_clamp01_02_sketch_section",
             "3 inches across the machine, half an inch in the plane of the bend"),
        stack(
            lede("A sweep needs its section sitting on the start of the path, "
                 "square to it."),
            points([
                "Our path starts at the origin heading straight up.",
                "So the section goes on the <strong>XY plane</strong>, centred "
                "on the origin. No offsets, no datum planes.",
                "Then run <strong>Additive Pipe</strong>: pick the section, "
                "then pick the path."]),
            callout("Choosing a path that starts at the origin along an axis is "
                    "not laziness. It is what makes the section sketch trivial. "
                    "Design the path around that."))),
            eyebrow="Making the sweep easy")

    d.slide("Clamp 02 is the same recipe", split(
        shot("05_clamp02_01_sketch_path",
             "Clamp 02: two lines and one rounded corner, and nothing else changes"),
        stack(
            lede("Two lines of difference. Everything else is identical, which "
                 "is why one script builds both."),
            table(["", "Clamp 01", "Clamp 02"],
                  [["Rise", "18 in", "26.6 in"],
                   ["Then", "7 in at 45&deg;", "6 in at 30&deg;"],
                   ["Then", "4 in across", "&mdash;"],
                   ["Section", "3 &times; 0.5 in", "3 &times; 0.5 in"],
                   ["Hole", "1 in", "1 in"]]))),
            eyebrow="Reuse the method")

    d.slide("What these parts are for", split(
        shot("08_asm_hero_Isometric",
             "The braces, standing up from the rear bar"),
        stack(
            lede("Honest answer: the tutorial never says."),
            points([
                "It calls them &ldquo;the attachment clamp&rdquo; and gives "
                "dimensions, but never mates them to anything.",
                "The 1 inch hole is the same size as the hitch pin, and a "
                "three-point mounted implement needs a top link anchor.",
                "So we model the dimensions given and stand them on the rear "
                "bar as a mast."]),
            warn("If you disagree, the parts are still right. Only where they "
                 "sit in Deck 10 changes. Joining the two braces into a proper "
                 "A-frame is exercise 9."))),
            eyebrow="A stated assumption")

    return d
