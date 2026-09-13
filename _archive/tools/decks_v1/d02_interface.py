# -*- coding: utf-8 -*-
"""Deck 2 - The FreeCAD interface, and the SolidWorks vocabulary."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)


def build():
    d = Deck("02-freecad-interface", "The FreeCAD Interface")

    d.sheet("00", "SOFTWARE", "TOUR", "The FreeCAD Interface", """
<p class="lede">FreeCAD is not one program. It is a shell that hosts task-specific
<strong>workbenches</strong> — you switch workbench the way a machinist walks to a
different bench. The toolbars, the menus and the available object types all change; the
document stays the same.</p>
%s
%s
""" % (fig("00_ui_00_startup_window", "STARTUP",
           "FreeCAD 1.1.3 on first launch, Part Design workbench active"),
       specs([("Version", "1.1.3"), ("Licence", "LGPL — free"),
              ("Kernel", "OpenCASCADE"), ("Scripting", "Python, everywhere"),
              ("Workbenches used here", "Part Design, Sketcher, Assembly, Spreadsheet")])),
            eyebrow="Deck 2", kind="title")

    d.sheet("01", "WINDOW", "ANATOMY", "Five regions of the window", """
<p class="lede">Once you can name these five regions, every instruction in this course
tells you exactly where to look.</p>
%s
""" % cols(fig("00_ui_00_startup_window", "THE WINDOW", "The whole application"), """
%s
%s
""" % (phases([("Menu bar",
                "File, Edit, View, Tools, Macro, then a menu named after the current "
                "workbench — here <strong>Sketch</strong> and <strong>Part Design</strong>. "
                "That workbench menu is the complete list of what the workbench can do."),
               ("Toolbars",
                "The same commands as icons. Which toolbars appear depends on the "
                "workbench. Hover any icon for its name and shortcut."),
               ("Model tree (left)",
                "Every object in the document, in the order it was created. This is the "
                "feature history — SolidWorks calls it the FeatureManager."),
               ("3D view (centre)",
                "The model. Also the Start page, until you open a document."),
               ("Task panel (left, replaces the tree)",
                "When you run a command that needs input — a Pad, a constraint, a "
                "Sketch — its dialog appears here, not in a floating window.")]),
       note("<strong>The tree and the task panel share a dock.</strong> New users lose "
            "the tree the first time they open a Pad dialog and think it has vanished. "
            "It has not: click the <strong>Model</strong> tab at the bottom of that panel."))),
            eyebrow="Where things are")

    d.sheet("02", "TREE", "MODEL", "The model tree is the build history", """
<p class="lede">FreeCAD does not store your part as a shape. It stores the
<em>recipe</em> — sketch, pad, sketch, pocket, pattern, fillet — and replays it every
time something changes. The tree is that recipe, in order.</p>
%s
""" % cols("""
%s
""" % fig("01_frame_ui_complete", "TREE — FRAME",
          "The finished frame: 6 sketches and 8 features, in build order"), """
<h3>Reading it</h3>
%s
<h3>The Tip</h3>
<p>One feature in the tree is the <strong>Tip</strong> — the current end of the recipe,
and the shape you actually see. You can move the Tip backwards to insert a feature in
the middle of the history, exactly like SolidWorks' rollback bar.</p>
%s
""" % (ticks([
    "<strong>Document</strong> — the file. Can hold several bodies.",
    "<strong>Body</strong> — one continuous solid. A part with two separate lumps of "
    "steel needs two bodies.",
    "<strong>Origin</strong> — the three planes (XY, XZ, YZ) and three axes every body "
    "starts with. Hidden by default; press <strong>Space</strong> on it to show them.",
    "<strong>Sketches and features</strong> — in creation order. A sketch that has been "
    "consumed by a Pad is nested underneath it.",
    "<strong>Spreadsheet</strong> — sits outside the body. Our parameter table."]),
       note("A small red or grey marker on a tree icon means that feature failed or is "
            "out of date. Never ignore one: everything after it in the tree is built on "
            "sand."))),
            eyebrow="The most important panel")

    d.sheet("03", "TOOLBARS", "PART DESIGN", "The four Part Design toolbars", """
<p class="lede">Part Design splits its commands across four toolbars. Learn what each
group is <em>for</em> and you will stop hunting for icons.</p>
%s
""" % (plates([("00_ui_03_tb_pd_helper", "HELPER",
                "Create Body, Create Sketch, attach a sketch, datum plane/line/point, "
                "shape binder"),
               ("00_ui_04_tb_pd_modeling", "MODELLING",
                "Additive: Pad, Revolution, Additive Loft, Additive Pipe, primitives. "
                "Subtractive: Pocket, Groove, Subtractive Loft, Subtractive Pipe, Hole"),
               ("00_ui_05_tb_pd_dressup", "DRESS-UP",
                "Fillet, Chamfer, Draft, Thickness — applied to faces and edges of an "
                "existing solid"),
               ("00_ui_06_tb_pd_transform", "TRANSFORMATION",
                "Mirrored, LinearPattern, PolarPattern, MultiTransform, Scaled")],
              "grid-2") +
       cols("""
<h3>Additive and subtractive</h3>
<p>Every Part Design feature either <strong>adds</strong> material or
<strong>removes</strong> it. Pad adds; Pocket removes. They take the same inputs — a
sketch and a length — and differ only in sign. Once you see that, half the toolbar
explains itself:</p>
%s
""" % tbl(["Adds", "Removes", "From a…"],
          [["Pad", "Pocket", "sketch, straight"],
           ["Revolution", "Groove", "sketch, about an axis"],
           ["Additive Loft", "Subtractive Loft", "two or more sketches"],
           ["Additive Pipe", "Subtractive Pipe", "sketch swept along a path"],
           ["Additive primitive", "Subtractive primitive", "box, cylinder, cone…"]]), """
<h3>Dress-up is different</h3>
<p>Fillet, Chamfer, Draft and Thickness do not take a sketch. They take
<strong>faces and edges of the solid you already have</strong>. That makes them fragile:
if an upstream change renumbers the edges, the fillet can attach to the wrong one. Add
dress-up features late, and keep them few.</p>
%s
""" % note("We hit exactly this on the frame. A 0.63&nbsp;in fillet on a 0.4&nbsp;in "
           "thick plate edge is geometrically impossible, and FreeCAD marks the feature "
           "<em>Invalid</em> rather than guessing. Deck 5 walks through the failure."))),
            eyebrow="Learn the groups, not the icons")

    d.sheet("04", "TOOLBARS", "STRUCTURE &amp; VIEW", "Structure and View", """
%s
""" % cols("""
<h3>Structure</h3>
%s
<p>Four commands, and you will use two of them constantly:</p>
%s
""" % (fig("00_ui_02_tb_structure", "STRUCTURE", "Part, Group, Variable set, Link"),
       ticks([
           "<strong>Create part</strong> — a container that groups bodies and gives "
           "them a shared placement. Not the same as a Body.",
           "<strong>Create group</strong> — a folder. Organisational only, no geometry "
           "meaning.",
           "<strong>Make link</strong> — a reference to an object, possibly in another "
           "document. This is how our assembly is built, and it is one of FreeCAD's "
           "genuinely strong features."])), """
<h3>View</h3>
%s
%s
""" % (fig("00_ui_07_tb_view", "VIEW", "Fit, draw style, standard views, axonometric"),
       tbl(["Key", "Does"],
           [["<code>0</code>–<code>6</code>", "Front, Top, Right, Rear, Bottom, Left"],
            ["<code>0</code>", "Axonometric (isometric)"],
            ["<code>V</code> then <code>F</code>", "Fit all"],
            ["<code>Space</code>", "Show / hide the selected object"],
            ["Middle-drag", "Pan"],
            ["Middle + right drag", "Rotate (in CAD navigation)"],
            ["Scroll", "Zoom"]]))),
            eyebrow="Getting around")

    d.sheet("05", "VOCABULARY", "TRANSLATION", "SolidWorks → FreeCAD, part 1", """
<p class="lede">If you are also watching the SolidWorks source video, this table is the
one to keep open. The concepts are the same; almost every name is different.</p>
%s
""" % cols(tbl(["SolidWorks", "FreeCAD 1.1", "Note"],
               [["Units: IPS", "Preferences ▸ General ▸ Units ▸ <strong>Imperial decimal</strong>",
                 "Deck 3"],
                ["Part document", "A <code>.FCStd</code> file with one <strong>Body</strong>", ""],
                ["FeatureManager tree", "<strong>Model</strong> tree", "Same idea"],
                ["Front / Top / Right plane", "<strong>XZ / XY / YZ</strong> plane",
                 "Careful — the names do not line up"],
                ["Sketch on a plane", "Part Design ▸ <strong>Create sketch</strong>", ""],
                ["Smart Dimension", "<strong>Dimension</strong> constraint", "<code>K</code>, <code>D</code>"],
                ["Fully Defined", "<strong>Fully constrained</strong>", "Message in the Sketcher panel"],
                ["Convert Entities", "<strong>External geometry</strong>", "<code>G</code>, <code>X</code>"],
                ["Offset Entities", "Sketcher <strong>Offset</strong>", ""],
                ["Trim Entities", "<strong>Trim edge</strong>", "<code>G</code>, <code>T</code>"],
                ["Mirror Entities", "<strong>Symmetry</strong> constraint", "Deck 5 uses this"],
                ["Linear Sketch Pattern", "<strong>Rectangular array</strong>", ""]]),
           tbl(["SolidWorks", "FreeCAD 1.1", "Note"],
               [["Boss-Extrude", "<strong>Pad</strong>", ""],
                ["Extruded Cut", "<strong>Pocket</strong>", ""],
                ["Blind", "Type = <strong>Dimension</strong>", ""],
                ["Through All", "Type = <strong>Through all</strong>", ""],
                ["Mid Plane", "<strong>Symmetric to plane</strong>", ""],
                ["Mirror (feature)", "<strong>Mirrored</strong>", ""],
                ["Linear Pattern", "<strong>LinearPattern</strong>", ""],
                ["Hole Wizard", "<strong>Hole</strong>", "Less capable; a Pocket often beats it"],
                ["Fillet", "<strong>Fillet</strong>", ""],
                ["Full-round fillet", "<em>no equivalent</em>",
                 "Round the two corners instead — Deck 5"],
                ["Appearance", "View tab ▸ <strong>Shape appearance</strong>", ""],
                ["Mates", "Assembly ▸ <strong>Joints</strong>", "Deck 10"]])),
            eyebrow="Keep this open")

    d.sheet("06", "VOCABULARY", "GAPS", "SolidWorks → FreeCAD, part 2: the gaps", """
<p class="lede">Three SolidWorks features have <strong>no FreeCAD equivalent at all</strong>.
Each one appears in this cultivator, and each is worth understanding — because in two of
the three cases the FreeCAD route is the better model.</p>
%s
""" % cols("""
%s
""" % tbl(["SolidWorks", "FreeCAD", "What we do instead"],
          [["<strong>Weldments ▸ Structural Member</strong>",
            "none in core",
            "Sketch the tube section and <strong>Pad</strong> it, or sweep it with "
            "<strong>Additive Pipe</strong>. Add-ons (Dodo, Flamingo) exist but are not needed."],
           ["<strong>Flex ▸ Bending</strong>",
            "none",
            "Build the part <em>curved by construction</em>: sweep the section along an "
            "arc of the wanted radius. The bend radius becomes a parameter."],
           ["<strong>Linear Component Pattern</strong> (assembly)",
            "none in Assembly",
            "Use an <strong>App::Link array</strong> — one link object with a list of "
            "placements. Deck 11."]]), """
<h3>Why two of these are upgrades</h3>
<p>SolidWorks' <em>Flex ▸ Bending</em> takes a finished flat plate and deforms it. The
result is a shape; the bend is an operation applied after the fact, and the plate's flat
pattern is what the model really knows.</p>
<p>Sweeping a section along an R10 arc produces the <em>same solid</em>, but the model now
knows the radius as a number you can name, dimension and drive from a spreadsheet.</p>
%s
%s
""" % (note("This is why Blade 02 costs us nothing. It is Blade 01 with "
            "<code>BendRadius</code> changed from 10 to 16 — the exact edit the source "
            "video makes by re-running Flex, but here it is one cell."),
       warn("<strong>The one real loss is Weldments.</strong> SolidWorks can generate a "
            "cut list and mitre joints automatically. FreeCAD cannot. For a nine-tyne "
            "cultivator that costs you nothing; for a 40-member trailer chassis it would "
            "matter."))),
            eyebrow="What FreeCAD cannot do")

    d.sheet("07", "PYTHON", "UNDER THE HOOD", "Everything is Python", """
<p class="lede">Every click in FreeCAD is a Python call, and the console echoes the code
for whatever you just did. This is not a side feature — it is how the whole of this
cultivator was built, and it is how you check what a command really did.</p>
%s
""" % cols("""
<h3>Turn the console on</h3>
%s
<p>Then draw something. Every action prints its code. Copy a line, change a number, paste
it back — the model updates.</p>
%s
""" % (steps([("<strong>View ▸ Panels ▸ Python console</strong>", ""),
              ("<strong>View ▸ Panels ▸ Report view</strong> — errors and warnings land here", ""),
              ("Optionally <strong>Edit ▸ Preferences ▸ General ▸ Macro</strong> and tick "
               "<em>Show script commands in python console</em>", "")], compact=True),
       code("""
>>> App.ActiveDocument.addObject('PartDesign::Pad', 'Pad')
>>> App.ActiveDocument.Pad.Profile = App.ActiveDocument.Sketch
>>> App.ActiveDocument.Pad.Length = 50.8
>>> App.ActiveDocument.recompute()
""")), """
<h3>Two things it tells you that the GUI does not</h3>
%s
%s
""" % (ticks([
    "<strong>Internal units are millimetres, always.</strong> Setting the schema to "
    "imperial changes the display only. <code>Pad.Length = 50.8</code> is 2 inches. "
    "Every script in this course multiplies inches by 25.4.",
    "<strong>Property names.</strong> Select an object and type "
    "<code>obj.PropertiesList</code> to see everything you can set — including "
    "properties with no GUI at all."]),
       note("You do not need to write Python to follow this course. Every part is built "
            "click by click on the slides. But the build scripts in "
            "<code>tools/</code> are provided, and reading one is the fastest way to "
            "understand what a feature actually stores."))),
            eyebrow="The console is your friend")

    return d
