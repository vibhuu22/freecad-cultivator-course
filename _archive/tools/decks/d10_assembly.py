# -*- coding: utf-8 -*-
"""Deck 10 - The assembly."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("10-assembly", "The Assembly", "Deck 10")

    d.cover("The Assembly", split(
        shot("08_asm_hero_Isometric", "Twenty-three components, 377 pounds"),
        stack(
            lede("Seven parts become one machine. FreeCAD gives you two ways to "
                 "do it, and they suit different jobs."),
            facts([("Components", "23"), ("Unique parts", "7"),
                   ("Working width", "76 in"), ("Weight", "377 lb")]))))

    d.slide("Two ways to assemble", split_even(
        stack(
            heading("Joints"),
            points([
                "You pick a face on one part and a face on another, and "
                "FreeCAD holds them together.",
                "This is what SolidWorks calls a mate.",
                "Good for anything that has to line up, or move."])),
        stack(
            heading("Links"),
            points([
                "You place a copy of a part at a position you give it.",
                "One link object can hold a whole list of positions.",
                "Good for repeated parts on a regular spacing."]),
            callout("Nine tynes on a regular pitch is exactly the second case. "
                    "With joints that would be eighteen separate mates to "
                    "create and keep in step."))),
            eyebrow="Pick deliberately")

    d.slide("Starting the assembly", split(
        shot("08_asm_01_frame_placed",
             "The frame goes in first, at the origin, and stays there"),
        stack(
            lede("Three things to get right before you place anything."),
            steps([
                "<strong>File &rsaquo; New</strong>, then "
                "<strong>save it immediately</strong>",
                "Open each part file you are going to use",
                "Switch to the <strong>Assembly</strong> workbench",
                "Insert the frame first and leave it at the origin"]),
            warn("<strong>Save first.</strong> A link stores the path to "
                 "another file. Until your assembly has a path of its own, "
                 "FreeCAD cannot work out a relative one, and you get "
                 "&ldquo;owner document not saved&rdquo;. Everybody hits this "
                 "once."))),
            eyebrow="Save before you link")

    d.slide("Placing nine tynes", split(
        shots([("08_asm_02_front_rank", "Five in front"),
               ("08_asm_03_rear_rank", "Four behind")]),
        stack(
            lede("Both tynes were modelled with their mounting face at zero "
                 "height, centred on their bolts. So placing one is two "
                 "numbers."),
            table(["Row", "Across the machine", "Front to back"],
                  [["Front, 5 off", "&minus;38, &minus;19, 0, 19, 38", "&minus;10 in"],
                   ["Rear, 4 off", "&minus;28.5, &minus;9.5, 9.5, 28.5", "+10 in"]]),
            callout("That is the payoff for choosing the part origin carefully "
                    "back in Deck 3. Had the origin been at some corner of the "
                    "bounding box, every placement would carry three "
                    "corrections and a rotation."))),
            eyebrow="Design parts around their interfaces")

    d.slide("The stagger", split(
        shot("08_asm_04_rank_stagger",
             "Nine points on an even 9.5 inch grid"),
        stack(
            lede("The rear row sits half a spacing across from the front row. "
                 "That is the whole trick."),
            points([
                "Both rows are at 19 inch pitch.",
                "The rear row is shifted 9.5 inches sideways.",
                "Seen from the front, the nine points are 9.5 inches apart "
                "across a 76 inch swath."]),
            callout("Check this view before you go further. If the points are "
                    "not evenly spread, the offset is wrong &mdash; and it is "
                    "much easier to see here than in an isometric view."))),
            eyebrow="Check it from above")

    d.slide("The blades and the braces", split(
        shots([("08_asm_05_blades", "A sweep under every tyne"),
               ("08_asm_06_braces", "The braces on the rear bar")]),
        stack(
            lede("Each sweep sits at its tyne's point. The tyne's tip position "
                 "comes straight out of the part model."),
            warn("These are placements, not joints. Move a tyne and its blade "
                 "does <em>not</em> follow. A <strong>Coincident</strong> joint "
                 "between the tyne's point face and the blade's top face would "
                 "keep them together properly."),
            callout("For a picture it does not matter. For a machine you intend "
                    "to keep changing, it does."))),
            eyebrow="Placements have limits")

    d.slide("Doing it with joints instead", split(
        shot("08_asm_hero_Right", "Both rows, seen from the side"),
        stack(
            lede("Worth doing once by hand, because a joint tests something a "
                 "placement never does: whether the parts actually fit."),
            steps([
                "<strong>Assembly &rsaquo; Create joint &rsaquo; "
                "Coincident</strong>",
                "Click the underside of the tool bar on the frame",
                "Click the top of the tyne's mounting head",
                "The faces snap together. The tyne can still spin.",
                "Add a second joint on a <strong>bolt hole</strong> of each to "
                "stop it"]),
            callout("Do this once and you will find out whether your bolt holes "
                    "line up. On this machine they do, because the frame's 3 "
                    "inch spacing and the tyne's 3 inch spacing came from the "
                    "same reading of the tutorial."))),
            eyebrow="Joints")

    d.slide("What the machine weighs", split(
        shots([("08_asm_hero_Front", "From the front"),
               ("08_asm_hero_Top", "From above")]),
        stack(
            lede("The weight comes out of the model, so you can check the "
                 "tractor before anyone cuts steel."),
            table(["Part", "How many", "Total"],
                  [["Frame", "1", "82 lb"],
                   ["Tine 01", "5", "133 lb"],
                   ["Tine 02", "4", "88 lb"],
                   ["Blades", "9", "22 lb"],
                   ["Clamps", "4", "52 lb"],
                   ["<strong>All of it</strong>", "<strong>23</strong>",
                    "<strong>377 lb</strong>"]]),
            callout("377 pounds is well inside what a 35 horsepower compact "
                    "tractor can lift &mdash; the right size of machine for a "
                    "76 inch swath."))),
            eyebrow="Check the numbers")

    return d
