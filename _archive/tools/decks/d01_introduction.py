# -*- coding: utf-8 -*-
"""Deck 1 - What the machine is, and what we are going to do."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("01-introduction", "The Nine-Tyne Cultivator", "Deck 1")

    d.cover("The Nine-Tyne Cultivator", split(
        shot("08_asm_hero_Isometric", "The machine you will build"),
        stack(
            lede("A tractor-mounted cultivator with nine tynes. "
                 "You are going to build all of it in FreeCAD."),
            facts([("Tynes", "9"),
                   ("Working width", "76 in"),
                   ("Tyne spacing", "9.5 in"),
                   ("Weight", "377 lb")]))))

    d.slide("What a cultivator does", split(
        shot("08_asm_hero_Front", "Nine points, evenly spaced across 76 inches"),
        stack(
            lede("It is a secondary tillage tool. The plough has already turned "
                 "the soil. The cultivator breaks it down."),
            points([
                "<strong>Breaks clods.</strong> The tyne cracks the furrow slice "
                "the plough left behind.",
                "<strong>Kills weeds.</strong> The blade runs just under the "
                "surface and cuts weed roots.",
                "<strong>Saves moisture.</strong> Loosening the top few inches "
                "slows water evaporating from below."]))),
            eyebrow="Why this machine exists")

    d.slide("Where it fits in the field work", stack(
        lede("Every tillage tool has its place in the sequence. The cultivator "
             "is the second pass."),
        table(["Pass", "Tool", "Working depth"],
              [["First", "Mouldboard or disc plough", "8 to 12 inches"],
               ["<strong>Second</strong>",
                "<strong>Cultivator</strong> &mdash; this machine",
                "<strong>4 to 9 inches</strong>"],
               ["Third", "Disc harrow or tine harrow", "2 to 4 inches"],
               ["Last", "Roller or planker", "surface only"]]),
        callout("Nine tynes at 9.5 inch spacing cover 76 inches in one pass. "
                "That suits a 35 to 45 horsepower tractor.")),
            eyebrow="The tillage sequence")

    d.slide("Why the tynes are in two rows", split(
        shot("08_asm_hero_Top", "Five tynes in front, four behind, offset by half a spacing"),
        stack(
            lede("Look at the machine from above. The nine tynes sit on two bars, "
                 "not one."),
            points([
                "Five on the front bar, 19 inches apart.",
                "Four on the rear bar, also 19 inches apart, but shifted "
                "9.5 inches sideways.",
                "Seen from the front the nine points are evenly spread, "
                "9.5 inches apart."]),
            callout("If all nine sat in one row, straw and stubble would jam "
                    "between them. Two rows give each tyne room to clear."))),
            eyebrow="A 5 + 4 arrangement")

    d.slide("The seven parts", stack(
        lede("Seven different parts make up the machine. You will model every one."),
        table(["Part", "How many", "What it does"],
              [["<strong>1. Frame</strong>", "1",
                "The welded square-tube frame that carries everything"],
               ["<strong>2. Tine 01</strong>", "5",
                "A straight tyne with a bent foot, for the front row"],
               ["<strong>3. Tine 02</strong>", "4",
                "A curved tyne, for the back row"],
               ["<strong>4 &amp; 5. Clamps</strong>", "2 + 2",
                "Bent steel straps that brace the frame"],
               ["<strong>6 &amp; 7. Blades</strong>", "5 + 4",
                "The sweeps that do the cutting"]])),
            eyebrow="What you will build")

    d.slide("A model, not a drawing", split(
        shot("01_frame_01_params_spreadsheet",
             "The frame's dimensions live in a spreadsheet, not in the geometry"),
        stack(
            lede("Every dimension in this machine sits in a spreadsheet cell. "
                 "Change the cell and the model rebuilds itself."),
            points([
                "Want eleven tynes instead of nine? Change one number.",
                "Want the blade bent on a bigger radius? Change one number.",
                "The model works out the mass for you, so you can check the "
                "tractor can lift it."]),
            callout("This is what people mean by <strong>parametric</strong>. "
                    "It takes a little more care while you build, and it saves "
                    "hours later."))),
            eyebrow="How we work")

    d.slide("Where the design comes from", stack(
        lede("This course follows a SolidWorks tutorial by Malviya CAD Solution. "
             "The original is in Hindi, and we worked from a rough translation."),
        points([
            "Some numbers in the translation are garbled. One line calls a hole "
            "&ldquo;12.5&rdquo;, another calls it &ldquo;3 inches&rdquo;.",
            "Neither is a diameter. The 3 inches turned out to be the "
            "<em>spacing</em> between a pair of holes.",
            "So we read the tutorial, check it against what the machine has to "
            "do, and then decide."]),
        warn("Wherever we had to decide something the source did not say, the "
             "slide says so. Deck 14 lists all twelve of those decisions in one "
             "place.")),
            eyebrow="Reading the source")

    d.slide("How the course is laid out", split_even(
        stack(
            heading("Learning FreeCAD"),
            table(["", "Deck"],
                  [["2", "The FreeCAD window"],
                   ["3", "Setting up a part"],
                   ["4", "Sketching and constraints"]]),
            heading("Building the parts"),
            table(["", "Deck"],
                  [["5", "The frame"],
                   ["6", "Tine 01"],
                   ["7", "Tine 02"],
                   ["8", "The clamps"],
                   ["9", "The blades"]])),
        stack(
            heading("Putting it together"),
            table(["", "Deck"],
                  [["10", "The assembly"],
                   ["11", "Patterns and fasteners"],
                   ["12", "Appearance and drawings"],
                   ["13", "Making it parametric"],
                   ["14", "Summary and exercises"]]),
            callout("You need FreeCAD 1.1 or newer. It is free. Nothing in this "
                    "course needs a paid add-on."),
            callout("Allow about twelve hours for the whole thing."))),
            eyebrow="Fourteen decks")

    return d
