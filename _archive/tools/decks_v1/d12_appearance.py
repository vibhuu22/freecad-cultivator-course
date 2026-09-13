# -*- coding: utf-8 -*-
"""Deck 12 - Appearance, materials, rendering and TechDraw."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "PRESENTATION"


def build():
    d = Deck("12-appearance-and-drawings", "Appearance, Materials and Drawings")

    d.sheet("00", P, "OVERVIEW", "Appearance, Materials and Drawings", """
<p class="lede">A model nobody can read is a model nobody will use. This deck covers making
it look right on screen, giving it a real material so the mass means something, and turning
it into a dimensioned drawing somebody can work from.</p>
""" + fig("08_asm_hero_Isometric", "PRESENTATION",
          "Frame in implement red, tynes in dark steel, sweeps in bright steel")
        + specs([("Colour", "View tab ▸ Shape appearance"),
                 ("Material", "Model tab ▸ Material"),
                 ("Screenshots", "Tools ▸ Save image"),
                 ("Drawings", "TechDraw workbench"),
                 ("Export", "STEP, IGES, STL, DXF")]),
            eyebrow="Deck 12", kind="title")

    a = """
<h3>Colour, per object</h3>
""" + steps([("Select the body (or a single face) in the tree or the 3D view", ""),
             ("In the property panel, switch to the <strong>View</strong> tab", ""),
             ("<strong>Shape Appearance</strong> ▸ Diffuse Color", ""),
             ("For a whole assembly, set the colour on the <strong>Link</strong> and tick "
              "<strong>Override Material</strong>", "")], compact=True) + \
        tbl(["Component", "Colour", "Why"],
            [["Frame, clamps", "implement red", "painted structure"],
             ["Tynes", "dark grey-blue", "forged, oiled steel"],
             ["Blades", "light grey", "polished by soil within an hour of work"]]) + \
        note("Colour is not decoration in an assembly &mdash; it is how a reader tells "
             "twenty-three components apart at a glance. Group by function, not by "
             "preference.")

    b = """
<h3>Material, and why it is different</h3>
<p><strong>Shape appearance</strong> changes how a part looks. <strong>Material</strong>
changes what it <em>is</em> &mdash; density, yield strength, Young's modulus &mdash; and
that is what mass and any later FEM depend on.</p>
""" + steps([("Select the body", ""),
             ("<strong>View ▸ Panels ▸ Material</strong>, or right-click the body", ""),
             ("Choose <strong>Steel</strong>, or a specific grade", ""),
             ("The appearance usually follows the material automatically", "")],
            compact=True) + code("""
Mild steel        0.284 lb/in3   7850 kg/m3

  frame           289.5 in3  ->   82.2 lb
  9 tynes         856.5 in3  ->  221.4 lb
  9 blades         76.1 in3  ->   21.6 lb
  4 clamps        182.7 in3  ->   51.9 lb
  ------------------------------------------
  total          1327.7 in3  ->  377.1 lb
""") + note("Every mass figure quoted in this course came out of the model this way. That "
            "is the point of modelling rather than drawing.")

    d.sheet("01", P, "APPEARANCE", "Colour and material", """
<p class="lede">Two different things that beginners conflate. One is how it looks; the other
is what it weighs.</p>
""" + cols(a, b), eyebrow="Looks and physics")

    a2 = """
<h3>Getting a usable image out</h3>
""" + steps([("Set the view: <strong>0</strong>&ndash;<strong>6</strong> for standard "
              "views, <strong>0</strong> for isometric", ""),
             ("<strong>View ▸ Fit all</strong>", "V, F"),
             ("Hide the sketches, datums and origin &mdash; select them and press "
              "<strong>Space</strong>", ""),
             ("<strong>Tools ▸ Save image</strong>", ""),
             ("Set the pixel size explicitly &mdash; do not accept the window size", ""),
             ("Choose the background: Current, White, or Transparent", "")]) + \
        warn("<strong>Hide your sketches first.</strong> Green construction lines all over "
             "a finished part is the commonest fault in student submissions, and it takes "
             "one keystroke to fix. Every render in this course was taken after a "
             "<em>hide everything that is not a solid</em> pass.")

    b2 = """
<h3>Draw styles</h3>
""" + tbl(["Style", "Shows", "Good for"],
          [["<strong>Shaded</strong>", "surfaces only", "clean marketing-style renders"],
           ["<strong>Flat lines</strong>", "surfaces + edges", "the default; best for teaching"],
           ["<strong>Wireframe</strong>", "edges only", "seeing internal features"],
           ["<strong>Hidden line</strong>", "edges, hidden ones dashed", "drawing-like views"],
           ["<strong>Points</strong>", "vertices", "rarely"]]) + """
<h3>Scripting it</h3>
""" + code("""
view = Gui.ActiveDocument.ActiveView
view.viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
view.saveImage(r"C:\\...\\hero.png", 2000, 1300, "Current")
""") + note("All 101 screenshots in this course were taken by a script, which is why they "
            "are consistent in size, framing and lighting. If you need more than a handful "
            "of images, script them.")

    d.sheet("02", P, "IMAGES", "Renders and screenshots", """
<p class="lede">Six clicks for one image; five lines of Python for a hundred consistent
ones.</p>
""" + cols(a2, b2), eyebrow="Hide the sketches first")

    a3 = """
<h3>TechDraw: a first sheet</h3>
""" + steps([("Switch to the <strong>TechDraw</strong> workbench", ""),
             ("<strong>Insert default page</strong> &mdash; an A3 sheet with a title block",
              ""),
             ("Select the body in the tree", ""),
             ("<strong>Insert view</strong> &mdash; places a projection on the sheet", ""),
             ("With the view selected, <strong>Insert projection group</strong> adds front, "
              "top, side and isometric together", ""),
             ("Set the <strong>Scale</strong> on the page or per view", "1:8 suits the frame"),
             ("Dimension with the tools on the <strong>Dimensions</strong> toolbar", ""),
             ("<strong>Export page as PDF</strong> or DXF", "")]) + \
        note("TechDraw views are <em>live</em>. Change the model and the drawing updates "
             "&mdash; dimensions included, as long as they are attached to geometry rather "
             "than typed in as text.")

    b3 = """
<h3>What each part's sheet should carry</h3>
""" + tbl(["Part", "Views", "Key dimensions"],
          [["Frame", "plan, front, iso", "82, 22, 2; hole pitch 9.5; bolt spacing 3; "
            "&oslash;0.5; clevis at &plusmn;15"],
           ["Tine 01", "right, front", "25 overall, 15 straight, R6, 2.25 &times; 1.5, "
            "head 5 &times; 1.25"],
           ["Tine 02", "right, front", "R16, 15 working height, 2.5 &times; 1.25, R1 point"],
           ["Clamps", "right, front", "18 / 7 / 4 and 26.6 / 6, R2, 3 &times; 0.5, &oslash;1"],
           ["Blades", "plan, right", "13 span, 4 long, 0.2 thick, 13&deg;, R10 / R16"],
           ["Assembly", "plan, front, iso", "overall envelope, working width, "
            "hitch spacing, mass"]]) + \
        ticks([
            "One sheet per part, plus a general arrangement.",
            "Section the frame's tool bar to show the 3/16 wall &mdash; it is invisible "
            "otherwise, and it is a third of the part's design.",
            "Put the parameter table on the GA sheet. It is the design, in one box."])

    d.sheet("03", P, "TECHDRAW", "Turning the model into drawings", """
<p class="lede">The output nobody can build from a 3D file alone. TechDraw is FreeCAD's
drawing workbench, and the views it makes stay attached to the model.</p>
""" + cols(a3, b3), eyebrow="Live views, live dimensions")

    a4 = """
<h3>Exporting</h3>
""" + tbl(["Format", "Carries", "Use for"],
          [["<strong>STEP</strong> (.step)", "exact solids, assembly structure, colours",
            "<strong>the default</strong> &mdash; opens in every CAD system"],
           ["IGES", "surfaces", "legacy; prefer STEP"],
           ["<strong>STL</strong>", "a triangle mesh, no units",
            "3D printing, rendering. Not for CAD exchange."],
           ["<strong>DXF</strong>", "2D curves", "laser and plasma cutting, from a "
            "TechDraw page"],
           ["OBJ / glTF", "mesh + appearance", "visualisation, web"],
           ["FCStd", "everything, parametric", "sharing with another FreeCAD user"]]) + \
        warn("<strong>STEP loses the history.</strong> The recipient gets the solid, not "
             "your sketches, features or spreadsheet. That is usually what you want when "
             "sending to a supplier &mdash; and it is a disaster if you send it to a "
             "colleague who has to modify it. Send the FCStd for that.")

    b4 = """
<h3>Flat patterns for the blade</h3>
<p>The blade is a bent 0.2&nbsp;in plate. To cut the blank you need its
<strong>developed</strong> shape, and here our modelling choice pays off again: because we
swept along an arc of known length, the developed length <em>is</em>
<code>BladeLength</code> = 4&nbsp;in exactly.</p>
""" + code("""
blank:   13.0 in span
          4.0 in developed length
          0.2 in thick

then form on R10 (Blade 01) or R16 (Blade 02)
""") + ticks([
        "No bend allowance calculation needed &mdash; the arc-length parameterisation gave "
        "it to us.",
        "For the plan shape, project the plan outline to DXF from a TechDraw top view.",
        "The 13&deg; swept-back edges nest well: alternate them and a 13 &times; 4 in "
        "blank yields with very little waste."])

    d.sheet("04", P, "EXPORT", "Getting it out of FreeCAD", """
<p class="lede">Different jobs need different formats, and choosing wrong is how a supplier
ends up quoting from a triangle mesh.</p>
""" + cols(a4, b4), eyebrow="STEP for solids, DXF for cutting")

    a5 = """
<h3>A presentation checklist</h3>
""" + steps([("Hide every sketch, datum and origin", "select, Space"),
             ("Set a sensible colour per component group", ""),
             ("Assign the material &mdash; and quote the mass it gives you", ""),
             ("Take four views at the same size: iso, front, right, plan", ""),
             ("One TechDraw sheet per part, one general arrangement", ""),
             ("Export STEP for the record, PDF for the drawings", ""),
             ("Put the parameter table somewhere visible", "")])

    b5 = plates([("08_asm_hero_Isometric", "ISOMETRIC", "the general arrangement"),
                 ("08_asm_hero_Top", "PLAN", "working width and spacing"),
                 ("08_asm_hero_Front", "FRONT", "the swath"),
                 ("08_asm_hero_Right", "RIGHT", "both ranks")], "grid-2")

    d.sheet("05", P, "CHECKLIST", "Presenting the machine", """
<p class="lede">The last 10% of the work, and the part your marker actually sees.</p>
""" + cols(a5, b5), eyebrow="Finish the job")

    return d
