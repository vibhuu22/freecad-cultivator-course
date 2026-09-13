# -*- coding: utf-8 -*-
"""Deck 14 - Summary and exercises."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("14-summary-and-exercises", "Summary and Exercises", "Deck 14")

    d.cover("Summary and Exercises", split(
        shot("08_asm_hero_Isometric", "Seven parts, twenty-three components, 377 lb"),
        stack(
            lede("What you built, what we assumed along the way, and twelve "
                 "things to try next."),
            facts([("Parts", "7"), ("Sketches", "20"),
                   ("Features", "24"), ("Exercises", "12")]))))

    d.slide("What you built", split(
        shots([("01_frame_final_Isometric", "The frame"),
               ("08_asm_hero_Isometric", "The machine")]),
        stack(
            lede("Every part earned its place by teaching something the next "
                 "part needed."),
            table(["Part", "Weight", "Off", "Taught you"],
                  [["Frame", "82 lb", "1", "pad, pocket, pattern, mirror, fillet"],
                   ["Tine 01", "27 lb", "5", "arcs, tangency, ambiguous angles"],
                   ["Tine 02", "22 lb", "4", "formulas that work out dimensions"],
                   ["Clamps", "13 lb", "4", "sweeping a section along a path"],
                   ["Blades", "2.4 lb", "9", "building a bend into the shape"]]))),
            eyebrow="Seven parts")

    d.slide("Ten things worth remembering", split(
        stack(
            points([
                "<strong>Fully constrain every sketch.</strong> No exceptions.",
                "<strong>Put sketches on origin planes,</strong> with offsets. "
                "Not on faces.",
                "<strong>Use endpoint tangency</strong> where a line meets a "
                "curve, and nothing else at that corner.",
                "<strong>Prefer distances to angles.</strong> An angle has two "
                "answers.",
                "<strong>Read the message in the Sketcher panel.</strong> It "
                "tells you what is wrong."])),
        stack(
            points([
                "<strong>A pocket cuts from its sketch plane onward.</strong> "
                "Put the plane where the cut starts.",
                "<strong>You cannot pattern a pattern.</strong> Do the symmetry "
                "in the sketch.",
                "<strong>Fillets and chamfers go last,</strong> and keep them "
                "few.",
                "<strong>Put each part's origin on the face that matters</strong> "
                "&mdash; the one that bolts to something else.",
                "<strong>Every dimension in a spreadsheet,</strong> named, with "
                "its unit."]))),
            eyebrow="The whole course, condensed")

    d.slide("Everything we assumed", split(
        stack(
            table(["", "We decided", "Because the source"],
                  [["1", "Frame holes are pairs, 3 in apart", "said &ldquo;one hole and another&rdquo;"],
                   ["2", "Tube is 2 by 2 in, 3/16 wall", "gave only the wall"],
                   ["3", "Bracket is 5 in long, 3 in tall", "never dimensioned it"],
                   ["4", "Tine 01 rakes 35 degrees", "did not say"],
                   ["5", "Tine 01 bends on R6", "did not say"],
                   ["6", "25 in is total, 15 in is the straight part", "gave both, unrelated"]])),
        stack(
            table(["", "We decided", "Because the source"],
                  [["7", "Tyne bolt holes go through", "said blind 0.4 in"],
                   ["8", "Clamps are braces for a mast", "never mated them"],
                   ["9", "Clamp 02 tip is 6 in long", "gave the angle only"],
                   ["10", "Blade radius is on the centreline", "used Flex conventions"],
                   ["11", "Blades have no bolt holes", "never mentioned them"],
                   ["12", "Two corner fillets, not a full round", "asked for a full round"]]),
            callout("All twelve are spreadsheet numbers. Disagreeing with any "
                    "of them costs one cell edit."))),
            eyebrow="Nothing hidden")

    d.slide("Exercises: get comfortable", split_even(
        stack(
            heading("Parameter changes"),
            steps([
                "<strong>Eleven tynes.</strong> Set the count to 11 and the "
                "frame to 101 inches. Report the new weight.",
                "<strong>A ten-foot machine.</strong> Decide the spacing first, "
                "then work out the count and the length.",
                "<strong>Re-rake Tine 01</strong> to 25 and then 45 degrees. "
                "Which would you specify for hard ground, and why?",
                "<strong>Add blade bolt holes.</strong> You decide the spacing "
                "&mdash; and justify it."])),
        stack(
            heading("Modelling jobs"),
            steps([
                "<strong>Model a bolt:</strong> half inch by four inches, hex "
                "head. Then place eighteen of them.",
                "<strong>Draw the frame</strong> on a TechDraw sheet, with a "
                "section through a tool bar.",
                "<strong>Design a third tyne</strong> &mdash; a spring tine "
                "that uses the same 5 inch head and 3 inch bolts.",
                "<strong>Sharpen the blade.</strong> Add a ground edge "
                "underneath the two cutting edges."]))),
            eyebrow="Exercises 1 to 8")

    d.slide("Exercises: harder", split(
        stack(
            heading("Take it further"),
            steps([
                "<strong>Build a proper hitch.</strong> The machine as modelled "
                "has no top link point. Design an A-frame mast that ties into "
                "the brackets and the rear bar.",
                "<strong>One master parameter table.</strong> Move the bolt "
                "size and spacing into a single file that the frame and both "
                "tynes read from. Then change the bolt to 5/8 inch.",
                "<strong>Assemble it with joints</strong> instead of "
                "placements. Report anywhere the parts did <em>not</em> fit."])),
        stack(
            heading("The big one"),
            steps([
                "<strong>Analyse a tyne.</strong> Take Tine 01 into the "
                "<strong>FEM</strong> workbench. Fix the head, push 150 pounds "
                "sideways at the point, and solve for stress. Is the section "
                "right, over-built, or marginal?"]),
            callout("Exercise 12 is where this stops being drawing and starts "
                    "being engineering. A model built the way this course built "
                    "it &mdash; right material, right geometry, right weight "
                    "&mdash; is ready for it."))),
            eyebrow="Exercises 9 to 12")

    d.slide("How your work is judged", split(
        shot("02_tine01_02_sketch_profile",
             "Fully constrained. This is the first thing anyone will check."),
        stack(
            lede("Five things, and the first one is not negotiable."),
            points([
                "Every sketch says <strong>fully constrained</strong>.",
                "Every dimension is in a spreadsheet, named, with its unit.",
                "Assumptions are <strong>stated</strong>, with a reason.",
                "The model rebuilds cleanly &mdash; nothing grey or failed "
                "anywhere in the tree.",
                "Weight and overall size quoted, and checked against a rough "
                "hand calculation."]))),
            eyebrow="Marking")

    return d
