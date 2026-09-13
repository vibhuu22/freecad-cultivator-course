# -*- coding: utf-8 -*-
"""Deck 2 - The FreeCAD window."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, shot, shots, strip, lede, points, steps, table, facts,
                      callout, warn, heading, split, split_even, stack)


def build():
    d = Deck("02-freecad-interface", "The FreeCAD Window", "Deck 2")

    d.cover("The FreeCAD Window", split(
        shot("00_ui_00_window", "FreeCAD 1.1 with the finished frame open"),
        stack(
            lede("Before you draw anything, learn where things are. "
                 "This deck is a tour of the screen."),
            points([
                "The five parts of the window",
                "What the model tree is telling you",
                "The four Part Design toolbars",
                "What SolidWorks words mean in FreeCAD"]))))

    d.slide("Five parts of the window", split(
        shot("00_ui_00_window", "Menus and toolbars on top, tree on the left, model in the middle"),
        stack(
            lede("Learn these five names and every instruction in this course "
                 "tells you exactly where to look."),
            points([
                "<strong>Menu bar.</strong> The last menu is named after "
                "whichever workbench you are in.",
                "<strong>Toolbars.</strong> The same commands as pictures. "
                "Hover for the name.",
                "<strong>Model tree,</strong> on the left. Everything in your file.",
                "<strong>3D view,</strong> in the middle. Your part.",
                "<strong>Task panel.</strong> Appears in place of the tree when "
                "a command needs your input."]))),
            eyebrow="Where things are")

    d.slide("The tree is your build history", split(
        shot("00_ui_01_model_tree", "The finished frame: six sketches and eight features, in the order they were made"),
        stack(
            lede("FreeCAD does not save your part as a shape. It saves the "
                 "recipe, and replays it whenever something changes."),
            points([
                "<strong>Body</strong> is one solid lump of metal.",
                "<strong>Origin</strong> holds the three starting planes. "
                "Select it and press <code>Space</code> to see them.",
                "<strong>Sketches and features</strong> are listed in the order "
                "you made them.",
                "A red mark on an icon means that step failed. Fix it before "
                "you carry on."]),
            callout("The task panel and the tree share the same space. The first "
                    "time you open a Pad dialog the tree seems to vanish. It has "
                    "not &mdash; click the <strong>Model</strong> tab at the "
                    "bottom."))),
            eyebrow="The most important panel")

    d.slide("Part Design has four toolbars", stack(
        lede("Learn what each group is for and you will stop hunting for icons."),
        split_even(
            stack(strip("00_ui_03_tb_pd_helper",
                        "<strong>Helper.</strong> Make a body, make a sketch, "
                        "make a datum plane."),
                  strip("00_ui_04_tb_pd_modeling",
                        "<strong>Modelling.</strong> Everything that adds or "
                        "removes metal.")),
            stack(strip("00_ui_05_tb_pd_dressup",
                        "<strong>Dress-up.</strong> Fillet, chamfer, draft, "
                        "thickness."),
                  strip("00_ui_06_tb_pd_transform",
                        "<strong>Transformation.</strong> Mirror and pattern.")))),
            eyebrow="Learn the groups, not the icons")

    d.slide("Adding metal and removing metal", split(
        stack(
            lede("Every modelling command either adds material or takes it away. "
                 "They work in pairs."),
            table(["Adds", "Removes", "Made from"],
                  [["Pad", "Pocket", "a sketch, pushed straight"],
                   ["Revolution", "Groove", "a sketch, spun about an axis"],
                   ["Additive Loft", "Subtractive Loft", "two or more sketches"],
                   ["Additive Pipe", "Subtractive Pipe", "a sketch pushed along a path"]])),
        stack(
            heading("Dress-up is different"),
            points([
                "Fillet, Chamfer and Draft do not use a sketch.",
                "They work on the faces and edges of the solid you already have.",
                "That makes them fragile. Add them last, and use as few as you can."]),
            callout("On the frame we ask for a fillet that is physically "
                    "impossible, and FreeCAD refuses. Deck 5 walks through it."))),
            eyebrow="Two halves of one toolbar")

    d.slide("Getting around the 3D view", split(
        strip("00_ui_07_tb_view", "The View toolbar: fit, draw style, standard views"),
        stack(
            lede("Six number keys and one letter will cover almost everything "
                 "you need."),
            table(["Key", "What it does"],
                  [["<code>1</code> to <code>6</code>", "Front, top, right, rear, bottom, left"],
                   ["<code>0</code>", "Isometric view"],
                   ["<code>V</code> then <code>F</code>", "Fit the model on screen"],
                   ["<code>Space</code>", "Show or hide whatever is selected"],
                   ["Scroll wheel", "Zoom"],
                   ["Middle button drag", "Pan"]]))),
            eyebrow="Navigation")

    d.slide("SolidWorks words, FreeCAD words", split_even(
        table(["SolidWorks", "FreeCAD"],
              [["Units: IPS", "Imperial decimal"],
               ["FeatureManager tree", "Model tree"],
               ["Front / Top / Right plane", "XZ / XY / <strong>YZ</strong> plane"],
               ["Smart Dimension", "Dimension constraint"],
               ["Fully Defined", "Fully constrained"],
               ["Mirror Entities", "Symmetry constraint"],
               ["Boss-Extrude", "Pad"],
               ["Extruded Cut", "Pocket"]]),
        stack(
            table(["SolidWorks", "FreeCAD"],
                  [["Blind", "Type: Dimension"],
                   ["Through All", "Type: Through all"],
                   ["Mid Plane", "Symmetric to plane"],
                   ["Linear Pattern", "LinearPattern"],
                   ["Mirror", "Mirrored"],
                   ["Hole Wizard", "Hole"],
                   ["Mates", "Joints"]]),
            warn("Careful with the planes. SolidWorks calls it the "
                 "<strong>Right</strong> plane; FreeCAD calls the same plane "
                 "<strong>YZ</strong>. Most of the tyne and clamp sketches in "
                 "this course go on it."))),
            eyebrow="If you are watching the SolidWorks video too")

    d.slide("Three things SolidWorks has that FreeCAD does not", stack(
        lede("You will meet all three in this machine. In two cases the FreeCAD "
             "way is actually better."),
        table(["SolidWorks tool", "What we do instead", "Deck"],
              [["<strong>Weldments</strong> &mdash; structural members",
                "Sketch the tube section and Pad it, or sweep it along a path "
                "with Additive Pipe",
                "5, 8"],
               ["<strong>Flex</strong> &mdash; bending a finished plate",
                "Build the blade curved from the start, by sweeping it along an "
                "arc of the radius we want",
                "9"],
               ["<strong>Linear Component Pattern</strong> in an assembly",
                "Use a link array, which is one object holding a list of "
                "positions",
                "10, 11"]]),
        callout("Because the blade is built curved, its bend radius is just a "
                "number in a spreadsheet. Blade 02 is Blade 01 with that number "
                "changed from 10 to 16.")),
            eyebrow="The real gaps")

    return d
