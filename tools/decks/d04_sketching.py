# -*- coding: utf-8 -*-
"""Deck 4 - Sketching and constraints."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("04-sketching-and-constraints", "Sketching and Constraints", "Deck 4")

    d.cover("Sketching and Constraints", split(
        shot("01_frame_03_sketch_plan_constrained",
             "The frame outline: eight lines, held in place by twenty-two rules"),
        stack(
            lede("Everything in this machine starts as a 2D sketch. A sketch is "
                 "not a drawing. It is shapes plus rules."),
            points([
                "What &ldquo;fully constrained&rdquo; means",
                "The two kinds of constraint",
                "A rectangle, done properly",
                "Two traps that will catch you"]))))

    d.slide("What fully constrained means", split(
        shot("01_frame_03_sketch_plan_constrained",
             "When nothing can move, FreeCAD turns the sketch green and says so"),
        stack(
            lede("A shape can move until you pin it down. Every rule you add "
                 "takes away one way it could move."),
            points([
                "A line can move four ways: each end can go left, right, up or down.",
                "A circle can move three: its centre, and its size.",
                "Add rules until nothing is left. FreeCAD then says "
                "<strong>fully constrained</strong>."]),
            callout("The frame outline has eight lines. That is thirty-two ways "
                    "it could move, and thirty-two rules to hold it still."))),
            eyebrow="The most important idea in this deck")

    d.slide("Why it matters", split(
        shot("02_tine01_02_sketch_profile",
             "The tyne profile. Twenty rules, and nothing can shift."),
        stack(
            lede("An unfinished sketch will move on you. Usually at the worst "
                 "possible moment."),
            points([
                "<strong>The model stops surprising you.</strong> Change one "
                "dimension and only the thing you meant to change moves.",
                "<strong>Your intention is written down.</strong> The sketch "
                "says &ldquo;this rectangle is centred and 82 inches "
                "wide&rdquo;, not &ldquo;these lines happen to be here&rdquo;.",
                "<strong>It is the whole point.</strong> If the shape is not "
                "locked to the numbers, changing a number does nothing "
                "reliable."]),
            callout("All twenty sketches in this machine are fully constrained. "
                    "It is a habit, and it takes seconds."))),
            eyebrow="Do not leave it for later")

    d.slide("The two kinds of constraint", split_even(
        stack(
            heading("Rules about relationships"),
            table(["Rule", "Key", "It says"],
                  [["Coincident", "<code>C</code>", "these two points are the same point"],
                   ["Horizontal", "<code>H</code>", "this line is level"],
                   ["Vertical", "<code>V</code>", "this line is upright"],
                   ["Parallel", "<code>P</code>", "these two lines run the same way"],
                   ["Tangent", "<code>T</code>", "the curve meets the line smoothly"],
                   ["Equal", "<code>E</code>", "same length, or same radius"],
                   ["Symmetric", "<code>S</code>", "these mirror about that line"]])),
        stack(
            heading("Rules with numbers"),
            table(["Rule", "Key", "It says"],
                  [["Distance", "<code>K</code>&nbsp;<code>D</code>", "this is 15 inches long"],
                   ["Horizontal distance", "<code>L</code>", "these are 3 inches apart sideways"],
                   ["Vertical distance", "<code>I</code>", "these are 2 inches apart up and down"],
                   ["Radius", "<code>K</code>&nbsp;<code>R</code>", "this arc is R6"],
                   ["Diameter", "<code>K</code>&nbsp;<code>O</code>", "this hole is half an inch"]]),
            callout("Prefer the first kind. Two lines told to be "
                    "<strong>equal</strong> stay equal forever. Two lines each "
                    "measured 5 inches stay equal only until somebody edits "
                    "one."))),
            eyebrow="Relationships and numbers")

    d.slide("A centred rectangle, step by step", split(
        shot("01_frame_03_sketch_plan_constrained",
             "The same six steps done twice: the outside of the frame, and the inside"),
        stack(
            lede("The commonest shape in the whole machine. Watch the count on "
                 "the right go down to nothing."),
            steps([
                ("Draw four lines corner to corner. FreeCAD adds the corner "
                 "joins for you.", "8 left"),
                ("<strong>Horizontal</strong> on the top and bottom lines", "6 left"),
                ("<strong>Vertical</strong> on the left and right lines", "4 left"),
                ("<strong>Symmetric</strong>: two opposite corners about the "
                 "origin. This centres it.", "2 left"),
                ("<strong>Horizontal distance</strong> on the bottom line: 82 in", "1 left"),
                ("<strong>Vertical distance</strong> on the side: 22 in", "done")]))),
            eyebrow="Worked example")

    d.slide("Symmetry beats copying", split(
        shot("01_frame_06_sketch_station_holes",
             "Four holes. Two are dimensioned; the other two are mirrored by a rule."),
        stack(
            lede("The frame needs matching bolt holes on both bars. Do not draw "
                 "them twice."),
            steps([
                "Draw and dimension the two holes on the front bar",
                "Draw two more circles roughly where the back pair goes",
                ("Select a front centre, a back centre, then the "
                 "<strong>X axis</strong>, and press S", "Symmetric"),
                "Add <strong>Equal</strong> so the sizes follow as well"]),
            callout("This is what SolidWorks calls Mirror Entities. It is not a "
                    "copy. Move the front hole and the back one follows, "
                    "always."))),
            eyebrow="One of the most useful rules there is")

    d.slide("Trap one: joining a line to a curve", split(
        shot("02_tine01_02_sketch_profile",
             "Four smooth joins on this profile. Each one is a single tangent rule."),
        stack(
            lede("Where a straight line runs smoothly into an arc, you need "
                 "<strong>endpoint tangency</strong>."),
            points([
                "Click the <em>end of the line</em> and the <em>end of the "
                "arc</em>, then press <code>T</code>.",
                "That one rule joins them <em>and</em> makes the join smooth.",
                "Do not also add a coincident rule at the same corner."]),
            warn("If you add both, the two rules fight each other. FreeCAD says "
                 "<strong>conflicting constraints</strong>, the sketch produces "
                 "no shape at all, and the Pad that follows fails with a "
                 "confusing message about a missing profile."))),
            eyebrow="Tangency")

    d.slide("Trap two: angles have two answers", split(
        shots([("02_tine01_final_Right", "What we wanted"),
               ("02_tine01_final_Isometric", "The tyne, raked forward")]),
        stack(
            lede("&ldquo;These two lines are 35 degrees apart&rdquo; describes "
                 "two different shapes. One leans forward, one leans back."),
            points([
                "The solver picks whichever it finds first. It is not always "
                "the one you drew.",
                "On the Tine 01 profile it flipped the whole foot backwards.",
                "The fix: say <em>how far forward the point reaches</em> "
                "instead. That has only one answer."]),
            callout("It is also the better dimension. &ldquo;How far forward "
                    "does the point go?&rdquo; is a question about the machine. "
                    "&ldquo;What is the angle at the bend?&rdquo; is a question "
                    "about the drawing."))),
            eyebrow="Prefer distances to angles")

    d.slide("Sketching in the right order", split(
        stack(
            heading("Work this way"),
            steps([
                "<strong>Draw roughly.</strong> Do not chase exact positions "
                "with the mouse. Get the shape right.",
                "<strong>Add the relationship rules.</strong> Horizontal, "
                "vertical, tangent, equal, symmetric.",
                "<strong>Then add the numbers,</strong> watching the count go down.",
                "<strong>Stop at zero.</strong> Do not add one more for luck &mdash; "
                "that is the one that causes trouble."])),
        stack(
            heading("Two habits worth forming"),
            points([
                "<strong>Name your dimensions.</strong> Double-click the "
                "constraint and call it <code>FrameLength</code>, not "
                "<code>Constraint7</code>. You need the name to drive it from a "
                "spreadsheet later.",
                "<strong>Close your shapes.</strong> An open outline cannot be "
                "padded. If a Pad complains, look for a gap at a corner."]),
            callout("If a Pad or Pocket fails and the sketch looks perfectly "
                    "fine, read the small message in the Sketcher panel first. "
                    "It is usually telling you exactly what is wrong."))),
            eyebrow="A routine that works")

    return d
