# -*- coding: utf-8 -*-
"""Deck 11 - Patterns, mirrors and fasteners."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("11-patterns-and-fasteners", "Patterns and Fasteners", "Deck 11")

    d.cover("Patterns and Fasteners", split(
        shot("01_frame_08_linear_pattern_holes",
             "Thirty-six holes, from one pattern"),
        stack(
            lede("Repetition is most of mechanical design. Here is everything "
                 "this machine taught us about it."),
            points([
                "Three places you can repeat something",
                "The one thing PartDesign will not do",
                "How to repeat a whole component",
                "The bolts we left out, and how to add them"]))))

    d.slide("Three places to repeat something", split(
        shot("01_frame_06_sketch_station_holes",
             "Repetition inside a sketch: the cheapest kind"),
        stack(
            lede("Do it as early as you can. Repetition inside a sketch always "
                 "works. Repetition in the tree sometimes does not."),
            table(["Where", "Tool", "Used for"],
                  [["<strong>In the sketch</strong>", "Symmetry, Rectangular array",
                    "the rear bar holes, the second bolt hole on both tynes"],
                   ["<strong>In the tree</strong>", "LinearPattern, Mirrored",
                    "the nine tyne stations, the second hitch bracket"],
                   ["<strong>In the assembly</strong>", "Link array",
                    "five tynes, four tynes, nine blades, four braces"]]))),
            eyebrow="Push it down a level")

    d.slide("Linear pattern: the setting that matters", split(
        shot("01_frame_08_linear_pattern_holes",
             "Nine stations at 9.5 inch pitch, both bars"),
        stack(
            lede("Two modes, and picking the wrong one bites you later."),
            table(["Mode", "The length means", "Change the count and&hellip;"],
                  [["<strong>Extent</strong>", "the total span, first to last",
                    "they get closer together, span stays"],
                   ["<strong>Spacing</strong>", "the gap between neighbours",
                    "the pattern gets longer"]]),
            callout("On the frame we use <strong>Extent</strong>, with the "
                    "length and the count both coming from the spreadsheet. "
                    "Change the number of tynes and the holes stay on the "
                    "frame."),
            warn("Occurrences <em>includes</em> the original. Nine means nine "
                 "in total, not nine extra."))),
            eyebrow="Extent, not spacing")

    d.slide("You cannot pattern a pattern", split(
        shot("01_frame_06_sketch_station_holes",
             "So all four holes go in one sketch instead"),
        stack(
            lede("The tutorial patterns the holes nine times, then mirrors the "
                 "pattern to the other bar. FreeCAD will not do the second "
                 "step."),
            points([
                "PartDesign cannot mirror a pattern, or pattern a mirror.",
                "There is no error dialogue. The feature just goes grey and "
                "everything after it stops working.",
                "The fix: do the symmetry <em>inside the sketch</em>, then "
                "pattern once."]),
            callout("The sketch route is arguably better anyway. The rear holes "
                    "are tied to the front ones by a live rule, so they cannot "
                    "drift apart."))),
            eyebrow="The limitation everybody hits")

    d.slide("Repeating a whole component", split(
        shot("08_asm_02_front_rank", "Five tynes, one object in the tree"),
        stack(
            lede("SolidWorks has a Linear Component Pattern. FreeCAD's Assembly "
                 "does not &mdash; but links do it better."),
            steps([
                "Select the component in the tree",
                "In the <strong>Data</strong> tab set "
                "<strong>Element Count</strong>",
                "Set <strong>Show Element</strong> to false",
                "Fill in the <strong>Placement List</strong>, one position per "
                "copy"]),
            warn("Leave the link's own <strong>Placement</strong> alone. The "
                 "list is measured <em>from</em> it, so if you set both, the "
                 "whole row shifts. The parts look right next to each other but "
                 "the rank is displaced from the frame."))),
            eyebrow="Link arrays")

    d.slide("The bolts we did not model", split(
        shot("01_frame_final_Top", "Thirty-six holes, and no bolts in them"),
        stack(
            lede("The tutorial calls for hex bolts from the SolidWorks Toolbox. "
                 "FreeCAD has no bolt library built in."),
            table(["Option", "Verdict"],
                  [["<strong>Fasteners add-on</strong> &mdash; Tools, Addon "
                    "Manager, install, restart",
                    "the right answer for real work"],
                   ["<strong>Model one bolt yourself</strong> &mdash; hexagon, "
                    "pad, circle, pad",
                    "ten minutes, and good sketching practice"],
                   ["<strong>Leave them out</strong>", "what we did, and said so"]]),
            callout("If you do add them: eighteen half-inch bolts, four inches "
                    "long, hold the nine tynes on. That is the joint that "
                    "matters."))),
            eyebrow="Fasteners")

    d.slide("Which tool, when", split(
        stack(
            table(["You want to", "Use", "Where"],
                  [["mirror shapes inside a sketch", "Symmetry", "sketch"],
                   ["repeat shapes inside a sketch", "Rectangular array", "sketch"],
                   ["repeat a pocket along a line", "LinearPattern", "tree"],
                   ["repeat around an axis", "PolarPattern", "tree"],
                   ["mirror a pad or pocket", "Mirrored", "tree"],
                   ["repeat a whole part", "Link array", "assembly"],
                   ["pattern a pattern", "<strong>not possible</strong>", "&mdash;"]])),
        stack(
            heading("Rules of thumb"),
            points([
                "Pattern the smallest thing that works. One pocket is robust; "
                "a group of six features is fragile.",
                "Take the count and the spacing from the spreadsheet, never "
                "typed in.",
                "Add fillets and chamfers <em>after</em> patterning, not before.",
                "If a pattern or mirror goes grey, look for nesting first. Nine "
                "times out of ten that is what it is."]))),
            eyebrow="One table to keep")

    return d
