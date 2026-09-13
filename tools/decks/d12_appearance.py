# -*- coding: utf-8 -*-
"""Deck 12 - Appearance, materials and drawings."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("12-appearance-and-drawings", "Appearance and Drawings", "Deck 12")

    d.cover("Appearance and Drawings", split(
        shot("08_asm_hero_Isometric",
             "Frame in implement red, tynes in dark steel, sweeps in bright steel"),
        stack(
            lede("A model nobody can read is a model nobody will use. This deck "
                 "is about finishing the job."),
            points([
                "Colour, and why material is different",
                "Getting a clean picture out",
                "Turning the model into a drawing",
                "Which file format to send"]))))

    d.slide("Colour and material are not the same thing", split_even(
        stack(
            heading("Colour"),
            points([
                "Select the part, open the <strong>View</strong> tab, set "
                "<strong>Shape Appearance</strong>.",
                "For a whole assembly, set it on the <strong>link</strong> and "
                "tick override.",
                "Group by function: frame red, tynes dark, wear parts bright."])),
        stack(
            heading("Material"),
            points([
                "Select the body and open the <strong>Material</strong> panel.",
                "Choose <strong>Steel</strong>.",
                "This sets the density, so the weight FreeCAD reports means "
                "something."]),
            callout("Every weight quoted in this course came out of the model "
                    "this way. That is the difference between modelling and "
                    "drawing."))),
            eyebrow="Looks, and physics")

    d.slide("Getting a clean picture", split(
        shot("08_asm_hero_Isometric", "Sketches hidden, model fitted, fixed size"),
        stack(
            lede("Six steps, and the first one is the one students skip."),
            steps([
                "<strong>Hide the sketches</strong>, datums and origin &mdash; "
                "select them and press <code>Space</code>",
                ("Set the view", "0 for isometric"),
                ("Fit the model on screen", "V then F"),
                "<strong>Tools &rsaquo; Save image</strong>",
                "Type the pixel size in yourself, do not accept the window size",
                "Pick the background: current, white, or transparent"]),
            warn("Green sketch lines all over a finished part is the commonest "
                 "fault in student work, and it takes one keystroke to fix."))),
            eyebrow="Hide the sketches first")

    d.slide("Making a drawing", split(
        shot("01_frame_final_Front",
             "The frame from the front &mdash; one of the views a drawing needs"),
        stack(
            lede("<strong>TechDraw</strong> turns the model into a dimensioned "
                 "sheet, and the views stay linked to the model."),
            steps([
                "Switch to the <strong>TechDraw</strong> workbench",
                "<strong>Insert default page</strong>",
                "Select the body, then <strong>Insert view</strong>",
                "Or use <strong>Insert projection group</strong> for front, top "
                "and side together",
                ("Set the scale on the page", "1:8 suits the frame"),
                "Dimension it, then export as PDF"]),
            callout("Change the model and the drawing updates, dimensions "
                    "included &mdash; as long as they are attached to geometry "
                    "rather than typed in as text."))),
            eyebrow="TechDraw")

    d.slide("What each sheet should show", split(
        shots([("01_frame_final_Top", "Frame from above"),
               ("02_tine01_final_Right", "Tine 01 from the side")]),
        stack(
            lede("One sheet per part, plus a general arrangement."),
            table(["Part", "Views", "Key dimensions"],
                  [["Frame", "plan, front", "82, 22, hole pitch 9.5, bolt spacing 3"],
                   ["Tine 01", "right, front", "25 overall, 15 straight, R6"],
                   ["Tine 02", "right, front", "R16, 15 working height, R1 point"],
                   ["Blades", "plan, right", "13 span, 13&deg;, R10 and R16"]]),
            callout("Put a section through the tool bar on the frame sheet. The "
                    "3/16 wall is invisible otherwise, and it is a third of the "
                    "part's design."))),
            eyebrow="What a workshop needs")

    d.slide("Which format to send", split(
        stack(
            table(["Format", "Carries", "Send it for"],
                  [["<strong>STEP</strong>", "exact solids and colours",
                    "anything going to another CAD system"],
                   ["<strong>DXF</strong>", "flat outlines",
                    "laser and plasma cutting"],
                   ["<strong>STL</strong>", "a triangle mesh",
                    "3D printing only"],
                   ["<strong>FCStd</strong>", "everything, editable",
                    "a colleague who has to change it"]])),
        stack(
            warn("<strong>STEP throws away the history.</strong> The person "
                 "receiving it gets the solid, not your sketches or your "
                 "spreadsheet. That is usually what you want for a supplier, "
                 "and a disaster for a colleague."),
            heading("Cutting the blade blank"),
            points([
                "Because we swept the blade along an arc of known length, the "
                "flat blank is exactly 13 by 4 inches.",
                "No bend allowance to work out.",
                "Export the plan outline to DXF from a TechDraw top view."]))),
            eyebrow="Exporting")

    return d
