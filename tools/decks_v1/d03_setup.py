# -*- coding: utf-8 -*-
"""Deck 3 - Setting up: units, documents, bodies, origin planes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)


def build():
    d = Deck("03-setting-up", "Setting Up")

    d.sheet("00", "DOCUMENT", "SETUP", "Setting Up", """
<p class="lede">Five minutes of setup saves five hours of confusion. Units, a document,
a body, and an understanding of which plane is which — that is everything you need before
the first sketch line.</p>
""" + fig("01_frame_00_empty_document", "EMPTY DOCUMENT",
          "A new document with one Body and its Origin — the starting state for every part")
        + specs([("Units", "Imperial decimal (in)"),
                 ("Decimals", "3"),
                 ("Workbench", "Part Design"),
                 ("One file per", "part"),
                 ("Bodies per file", "1")]),
            eyebrow="Deck 3", kind="title")

    a = """
<h3>Set the schema</h3>
""" + steps([("<strong>Edit ▸ Preferences ▸ General ▸ Units</strong>", ""),
             ("Unit system: <strong>Imperial decimal (in, lb)</strong>", ""),
             ("Number of decimals: <strong>3</strong>", ""),
             ("OK. Every dimension box now reads and writes inches.", "")]) + """
<p>The source tutorial uses SolidWorks' <strong>IPS</strong> (inch-pound-second). Imperial
decimal is the same thing: lengths in decimal inches, not feet-and-fractions.</p>
""" + warn("<strong>Do this before you draw anything.</strong> Changing the schema later "
           "does not change your geometry — internally it never moved — but every "
           "dimension you had memorised now reads differently, and that is how mistakes "
           "get made.")

    b = """
<h3>What the schema does and does not do</h3>
<p>FreeCAD stores <strong>every</strong> length internally in millimetres. Always. The unit
schema is a display and input convention layered on top.</p>
""" + code("""
>>> App.Units.Quantity("25.4 mm").UserString
'1.00 in'
>>> Pad.Length          # the stored value, in mm
2082.8
>>> Pad.Length.UserString
'82.00 in'
""") + note("If you script FreeCAD, remember this: <code>Pad.Length = 2</code> is two "
            "<em>millimetres</em>, not two inches, whatever the schema says. Every build "
            "script in this course defines <code>IN = 25.4</code> and multiplies.") + """
<h3>Other schemas you may meet</h3>
""" + tbl(["Schema", "Use"],
          [["Standard (mm/kg/s)", "The default. Most FreeCAD tutorials online."],
           ["<strong>Imperial decimal</strong>", "<strong>This course.</strong> Inches, decimal."],
           ["US customary (in/lb)", "Feet and fractional inches — good for joinery, bad here."],
           ["Building US (ft-in)", "Architectural."]])

    d.sheet("01", "UNITS", "PREFERENCES", "Units first, always", """
<p class="lede">The tutorial works in inches, so we work in inches. Every dimension in
this course — 82, 22, 9.5, 0.5, 1.25 — is an inch value.</p>
""" + cols(a, b), eyebrow="Step one")

    a2 = """
<h3>Document, Body, Feature</h3>
""" + phases([("Document (<code>.FCStd</code>)",
               "The file. It can hold several bodies, a spreadsheet, drawings — anything. "
               "One document per part is our rule."),
              ("Body",
               "One <em>continuous</em> solid, with its own origin and its own feature "
               "history. If your part is two separate lumps of steel that never touch, it "
               "needs two bodies — or, better, two parts."),
              ("Feature",
               "One operation: Pad, Pocket, Fillet, Pattern. Features chain: each takes "
               "the previous result and modifies it. The last one is the Tip.")]) + \
        note("A <strong>Part</strong> (Structure toolbar) is different again — a container "
             "that groups bodies. We do not need one; our assembly uses Links instead.")

    b2 = """
<h3>Making one</h3>
""" + steps([("<strong>File ▸ New</strong>, or the Parametric Body card on the Start page", ""),
             ("Switch to the <strong>Part Design</strong> workbench in the workbench "
              "dropdown", ""),
             ("<strong>Part Design ▸ Create body</strong>", "shortcut: none by default"),
             ("The body appears in the tree, highlighted — it is now the "
              "<strong>active</strong> body, and new features go into it", ""),
             ("<strong>File ▸ Save As</strong> straight away, with a real name", "")],
            ) + warn("<strong>Active body matters.</strong> If no body is active, "
                     "Create Sketch will ask you where to put the sketch, and a Pad will "
                     "refuse to run. Double-click a body in the tree to activate it; its "
                     "label turns bold.")

    d.sheet("02", "STRUCTURE", "CONCEPTS", "Document, Body, Feature", """
<p class="lede">FreeCAD's structure has three levels, and mixing them up is the single
most common beginner error. Get them straight now.</p>
""" + cols(a2, b2) + plates([("01_frame_02_body_created", "BODY CREATED",
                              "A new Body: Origin, and nothing else yet"),
                             ("01_frame_15_complete_tree", "THE SAME BODY, FINISHED",
                              "6 sketches, 8 features, one solid")]),
            eyebrow="Getting the hierarchy right")

    a3 = """
<h3>The three origin planes</h3>
<p>Every body starts with three planes and three axes. They are hidden; select
<strong>Origin</strong> in the tree and press <strong>Space</strong> to see them.</p>
""" + tbl(["FreeCAD", "Normal to", "SolidWorks calls it", "In this machine"],
          [["<strong>XY_Plane</strong>", "Z (up)", "Top", "Frame plan, tyne head, bolt holes"],
           ["<strong>XZ_Plane</strong>", "Y (fore-aft)", "Front", "Blade section, clamp holes"],
           ["<strong>YZ_Plane</strong>", "X (across)", "<strong>Right</strong>",
            "All the side profiles: both tynes, both clamps"]]) + \
        warn("<strong>The names do not correspond.</strong> SolidWorks' <em>Front</em> "
             "plane is FreeCAD's <strong>XZ</strong>; SolidWorks' <em>Right</em> is "
             "FreeCAD's <strong>YZ</strong>. When the video says &ldquo;select the Right "
             "plane&rdquo;, you want <strong>YZ_Plane</strong>. Nearly every tyne and "
             "clamp sketch in this course is on YZ.")

    b3 = """
<h3>Our machine coordinate system</h3>
""" + specs([("+X", "across the machine, to the right"),
             ("+Y", "rearward (the tractor is at &minus;Y)"),
             ("+Z", "up"),
             ("Origin", "centre of the frame, at its underside")]) + """
<p>Choosing this deliberately, once, at the start, is what makes the assembly fall
together later. Both tynes are modelled with their <strong>mounting face at
z&nbsp;=&nbsp;0</strong> and their shank hanging into negative Z, so placing one is a
matter of x and y only.</p>
""" + note("<strong>Design the part around its interface.</strong> The tyne's origin is "
           "not at some corner of its bounding box — it is at the centre of the face that "
           "bolts to the tool bar. That is the surface the rest of the machine cares about.")

    d.sheet("03", "PLANES", "ORIENTATION", "Which plane is which", """
<p class="lede">Three planes, three axes, and one naming trap that catches everybody who
comes from SolidWorks.</p>
""" + cols(a3, b3), eyebrow="The trap that catches everyone")

    a4 = """
<h3>The AttachmentOffset trick</h3>
<p>A sketch does not have to sit <em>on</em> a plane. Attach it to a plane and give it an
offset, and it floats parallel to that plane at any distance you like.</p>
""" + steps([("Create the sketch on, say, XY_Plane", ""),
             ("Select it, and in the <strong>Data</strong> tab open "
              "<strong>Attachment ▸ Attachment Offset ▸ Position</strong>", ""),
             ("Set <strong>z</strong> to the offset you want", "z = 2 in"),
             ("The sketch moves; everything drawn in it moves with it", "")]) + \
        note("Used four times in the frame alone: the tube bore sketch sits 1.8125&nbsp;in "
             "up, the bolt-hole sketch sits on the top face at 2&nbsp;in, and each clevis "
             "plate sketch sits out at its own x. No datum planes needed.")

    b4 = """
<h3>Why not just use the face?</h3>
<p>You can sketch directly on a face of the solid — click the face, then Create Sketch.
It is quick, and it is <strong>fragile</strong>.</p>
""" + ticks([
        "Faces are numbered by the geometry kernel, not by you. Add a feature upstream and "
        "<code>Face7</code> may become <code>Face11</code>.",
        "Your sketch then attaches to the wrong face, or to nothing, and the model breaks "
        "in a way that is genuinely hard to debug. This is <em>topological naming</em>, "
        "and it is FreeCAD's oldest weakness.",
        "An origin plane never renumbers. Neither does a datum plane built from origin "
        "geometry."]) + \
        warn("<strong>Rule of thumb:</strong> attach to origin planes wherever you can. "
             "Every sketch in this cultivator is attached to an origin plane, most with an "
             "offset. Not one is attached to a face — which is why re-running the build "
             "scripts always works.")

    d.sheet("04", "SKETCH PLACEMENT", "TECHNIQUE", "Putting a sketch where you want it", """
<p class="lede">You will constantly need a sketch that is parallel to an origin plane but
not on it. There are two ways; only one of them is robust.</p>
""" + cols(a4, b4), eyebrow="Attachment, not faces")

    a5 = """
<h3>Save early, save often</h3>
""" + steps([("One folder for the job", "Cultivator\\parts\\"),
             ("One file per part, numbered in build order",
              "01_frame.FCStd  02_tine01.FCStd  ..."),
             ("Save before every risky operation — fillets especially", "Ctrl+S"),
             ("FreeCAD keeps one backup, <code>.FCBak</code>, beside the file", "")],
            compact=True)

    b5 = """
<h3>Recompute and the little markers</h3>
""" + ticks([
        "A <strong>blue check</strong> or nothing: up to date.",
        "A <strong>touched</strong> marker: the object needs recomputing. "
        "<strong>Refresh</strong> (the circular arrows, or <code>Ctrl+R</code>) rebuilds it.",
        "A <strong>red exclamation</strong>: the feature <em>failed</em>. Everything after "
        "it in the tree is now meaningless. Fix it before you go on.",
        "Right-click the document ▸ <strong>Mark to recompute</strong> forces a full "
        "rebuild — the first thing to try when a model looks wrong but reports no error."])

    d.sheet("05", "HOUSEKEEPING", "HABITS", "Files, saving, recompute", """
<p class="lede">Boring, and it is what separates a model you can hand to someone else from
a model you have to rebuild.</p>
""" + cols(a5, b5) + note("Every part in this course was built by a script, and every "
                          "script ends with a save. You can re-run any of them and get "
                          "byte-for-byte the same part — which is the real test of whether "
                          "a model is properly built."),
            eyebrow="Boring but essential")

    return d
