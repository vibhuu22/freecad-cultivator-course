# -*- coding: utf-8 -*-
"""Deck 3 - Setting up a part."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("03-setting-up", "Setting Up a Part", "Deck 3")

    d.cover("Setting Up a Part", split(
        shot("01_frame_02_body_created", "A new document with one empty body"),
        stack(
            lede("Five minutes of setting up saves hours of confusion later."),
            points([
                "Switch the units to inches",
                "Make a document and a body",
                "Learn which plane is which",
                "Put a sketch exactly where you want it"]))))

    d.slide("Units first, before you draw", split(
        stack(
            heading("How to change them"),
            steps([("Open <strong>Edit &rsaquo; Preferences &rsaquo; General "
                    "&rsaquo; Units</strong>", ""),
                   "Set the unit system to <strong>Imperial decimal</strong>",
                   "Set decimals to <strong>3</strong>",
                   "Click OK. Every box now reads inches."])),
        stack(
            lede("The tutorial works in inches, so we work in inches."),
            callout("FreeCAD always stores lengths in millimetres inside the "
                    "file. Changing the units only changes what you see and "
                    "type. Your geometry does not move."),
            warn("Do this <strong>before</strong> you draw anything. Changing "
                 "units halfway through will not break the model, but every "
                 "number you had in your head now reads differently."))),
            eyebrow="Step one")

    d.slide("Document, body, feature", split(
        shot("00_ui_01_model_tree", "One document, one body, and the features inside it"),
        stack(
            lede("FreeCAD has three levels. Mixing them up is the commonest "
                 "beginner mistake."),
            points([
                "A <strong>document</strong> is the file. We use one file per part.",
                "A <strong>body</strong> is one solid lump of metal. Two "
                "separate lumps need two bodies.",
                "A <strong>feature</strong> is one operation: a pad, a pocket, "
                "a fillet. Features run in order."]),
            callout("New features go into whichever body is <strong>active</strong>. "
                    "Double-click a body in the tree to make it active; its name "
                    "goes bold."))),
            eyebrow="The three levels")

    d.slide("Starting a new part", split(
        shot("01_frame_00_empty_document", "An empty document, ready to work in"),
        stack(
            lede("Four steps, every time. Get into the habit."),
            steps([
                "<strong>File &rsaquo; New</strong>",
                "Switch to the <strong>Part Design</strong> workbench",
                "<strong>Create body</strong> from the Helper toolbar",
                ("<strong>Save</strong> straight away, with a real name",
                 "Ctrl+S")]),
            callout("Name files in build order: <code>01_frame</code>, "
                    "<code>02_tine01</code>, and so on. It keeps the folder "
                    "readable."))),
            eyebrow="Do it the same way every time")

    d.slide("Which plane is which", split(
        stack(
            table(["FreeCAD name", "Faces", "SolidWorks calls it", "We use it for"],
                  [["<strong>XY plane</strong>", "up", "Top",
                    "the frame seen from above, tyne heads, bolt holes"],
                   ["<strong>XZ plane</strong>", "forward", "Front",
                    "the blade section, clamp holes"],
                   ["<strong>YZ plane</strong>", "sideways", "<strong>Right</strong>",
                    "every side view: both tynes, both clamps"]])),
        stack(
            lede("Every body starts with three planes. You draw your first "
                 "sketch on one of them."),
            warn("The names do not match SolidWorks. When the video says "
                 "&ldquo;select the Right plane&rdquo;, you want "
                 "<strong>YZ</strong>."),
            heading("Our machine directions"),
            points([
                "<strong>X</strong> runs across the machine",
                "<strong>Y</strong> runs front to back",
                "<strong>Z</strong> is up"]))),
            eyebrow="The trap that catches everyone")

    d.slide("Putting a sketch where you want it", split(
        shot("01_frame_05_pocket_tube_bore",
             "This cut starts 1.8125 in above the XY plane, so it leaves the top wall alone"),
        stack(
            lede("A sketch does not have to sit on a plane. Give it an offset "
                 "and it floats parallel to that plane."),
            steps([
                "Make the sketch on an origin plane as usual",
                "Select it and open the <strong>Data</strong> tab",
                "Find <strong>Attachment Offset &rsaquo; Position</strong>",
                ("Type the distance into <strong>z</strong>", "z = 2 in")]),
            warn("You can also sketch straight onto a face of your part. Do not. "
                 "Faces get renumbered when you change something upstream, and "
                 "your sketch then attaches to the wrong one. Every sketch in "
                 "this course sits on an origin plane."))),
            eyebrow="Offsets, not faces")

    return d
