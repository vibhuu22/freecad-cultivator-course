# -*- coding: utf-8 -*-
"""Deck 13 - Making it parametric."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("13-making-it-parametric", "Making It Parametric", "Deck 13")

    d.cover("Making It Parametric", split(
        shot("01_frame_01_params_spreadsheet",
             "Fifteen numbers. Nothing in the frame is typed anywhere else."),
        stack(
            lede("This is what everything so far has been building towards. The "
                 "model is not one cultivator. It is a family of them."),
            facts([("Frame", "15 numbers"), ("Tine 01", "11"),
                   ("Tine 02", "13"), ("Typed twice", "none")]))))

    d.slide("Why bother", split(
        shot("01_frame_final_Isometric", "Change one cell, and this rebuilds"),
        stack(
            lede("It costs about twenty seconds a dimension. Here is what you "
                 "get back."),
            points([
                "<strong>You change, instead of rebuilding.</strong> Nine tynes "
                "become eleven in one cell.",
                "<strong>Your reasoning is written down.</strong> &ldquo;Inner "
                "rectangle = outer minus two member widths&rdquo; says "
                "something. The number 78 does not.",
                "<strong>Mistakes show up.</strong> Ask for fifteen tynes and "
                "the holes run off the end, on screen, not in the workshop.",
                "<strong>Someone else can check it.</strong> Fifteen named "
                "cells can be reviewed. Forty numbers hidden in a feature tree "
                "cannot."]))),
            eyebrow="The case for it")

    d.slide("Keep it in three layers", split(
        shot("03_tine02_00_params",
             "Tine 02: three of these cells are formulas"),
        stack(
            lede("Separate the numbers you chose from the numbers that follow "
                 "from them."),
            table(["Layer", "Holds", "Example"],
                  [["<strong>1. Choices</strong>", "numbers a designer picked",
                    "curve radius 16 in"],
                   ["<strong>2. Worked out</strong>",
                    "formulas built from layer 1", "sweep angle"],
                   ["<strong>3. The shapes</strong>",
                    "dimensions pointing at layer 1 or 2", "the arc radius"]]),
            callout("Never put arithmetic in a dimension box. If a dimension "
                    "needs 82 minus twice 2, that belongs in a named cell where "
                    "it can be seen and checked."))),
            eyebrow="Three layers")

    d.slide("How to actually do it", split(
        shot("01_frame_01_params_spreadsheet",
             "Aliased cells go yellow. That name works anywhere in the file."),
        stack(
            lede("Three steps. Most people stop after the second."),
            steps([
                ("Type the name, the value <em>with its unit</em>, and what it "
                 "means", "82 in"),
                "Select the value cell and click <strong>Alias</strong>, then "
                "type a name",
                ("In any dimension box, click the small blue circle and type "
                 "the name", "Params.FrameLength")]),
            warn("Always include the unit. A cell holding <code>82</code> is "
                 "just a number; a cell holding <code>82 in</code> is a length. "
                 "Attach a plain number to a length and FreeCAD will either "
                 "refuse or quietly treat it as millimetres."))),
            eyebrow="Cells, aliases, expressions")

    d.slide("Watch a change cascade", split(
        shot("01_frame_final_Top",
             "Nine stations now. Two cells make it eleven."),
        stack(
            lede("Change the tyne count to eleven and the frame length to 101 "
                 "inches. Then recompute and watch."),
            points([
                "The outer rectangle widens, and the inner one follows because "
                "it is defined as the outer minus two member widths.",
                "The tube bore widens with it.",
                "The first hole moves to the new starting position.",
                "The pattern spreads eleven stations across the new span.",
                "The hitch brackets stay put, because their spacing is set by "
                "the tractor, not the frame."]),
            callout("Five changes from two cells, and not one of them needed a "
                    "decision."))),
            eyebrow="A worked change")

    d.slide("Where a parametric model breaks", split(
        shot("01_frame_14_fillet_clevis_nose",
             "The bracket fillet: the first thing to fail if you push it"),
        stack(
            lede("A model that has only ever been tried at one set of numbers "
                 "only works at one set of numbers."),
            table(["If you", "What breaks", "Why"],
                  [["make a fillet much bigger", "the fillet", "no metal left to round"],
                   ["make the tube wall too thick", "the bore pocket", "the bore turns inside out"],
                   ["make a bend radius tiny", "the sweep", "it runs into itself"],
                   ["ask for too many holes", "<strong>nothing</strong>",
                    "they run off the end silently"]]),
            callout("That last one is the dangerous case. Add a check cell that "
                    "compares the hole span against the frame length and shows "
                    "true or false. Cheapest design review there is."))),
            eyebrow="Test the extremes")

    return d
