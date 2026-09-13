# -*- coding: utf-8 -*-
"""Deck 10 - The assembly."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "08 ASSEMBLY"


def build():
    d = Deck("10-assembly", "The Assembly")

    d.sheet("00", P, "OVERVIEW", "The Assembly", """
<p class="lede">Sixteen components, nine tynes, one machine. FreeCAD 1.0 gained a proper
Assembly workbench with real joints and a solver — and it also has something SolidWorks
does not: the <strong>Link</strong>, which makes patterning components almost free.</p>
""" + fig("08_asm_hero_Isometric", "ISOMETRIC", "The complete cultivator, 377 lb")
        + specs([("Components", "16"), ("Unique parts", "7"),
                 ("Working width", "76 in"), ("Overall", "82 &times; 25 &times; 35 in"),
                 ("Mass", "377 lb / 171 kg"), ("Tree objects", "7 links")]),
            eyebrow="Deck 10", kind="title")

    a = """
<h3>Two ways to assemble in FreeCAD</h3>
""" + tbl(["", "Assembly workbench", "Links + placement"],
          [["What it is", "Joints solved by a constraint solver", "Components positioned by a transform"],
           ["Like SolidWorks", "Mates", "no direct equivalent"],
           ["Captures intent", "yes &mdash; &ldquo;these faces are flush&rdquo;", "no &mdash; just numbers"],
           ["Can pattern", "no", "<strong>yes</strong> &mdash; a link array"],
           ["Survives part edits", "usually", "always"],
           ["Good for", "mechanisms, anything that moves", "repeated parts on a grid"]]) + \
        note("They are not exclusive. A real project uses joints for the parts whose "
             "relationship matters and link arrays for the nine identical tynes. This deck "
             "shows both.")

    b = """
<h3>Why this machine uses links</h3>
<p>Nine tynes. Five of one part, four of another, on a regular pitch. With joints that is
eighteen mates to create and maintain; if the pitch changes, you edit all of them.</p>
""" + code("""
App::Link  "Tine01_x5"
   LinkedObject  = Tine01 (in 02_tine01.FCStd)
   ElementCount  = 5
   PlacementList = [ (-38, -10, 0),
                     (-19, -10, 0),
                     (  0, -10, 0),
                     ( 19, -10, 0),
                     ( 38, -10, 0) ]
""") + ticks([
        "<strong>One object in the tree</strong> for five tynes.",
        "One copy of the geometry in memory, however many instances.",
        "Change the source part and all five update.",
        "The pitch is a list of numbers you can generate from a formula."])

    d.sheet("01", P, "APPROACH", "Joints, or links?", """
<p class="lede">FreeCAD gives you two genuinely different ways to build an assembly. Pick
deliberately — they suit different problems.</p>
""" + cols(a, b), eyebrow="Pick the right tool")

    a2 = """
<h3>Setting up</h3>
""" + steps([("<strong>File ▸ New</strong>, then <strong>save it immediately</strong>",
              "an unsaved document cannot hold external links"),
             ("Switch to the <strong>Assembly</strong> workbench", ""),
             ("Open each part file you need &mdash; the source documents must be open for "
              "links to resolve", ""),
             ("<strong>Assembly ▸ Insert component</strong>, or drag the body from one "
              "document's tree into the assembly", ""),
             ("Position it: select the component and edit its <strong>Placement</strong>, "
              "or add a joint", "")]) + \
        warn("<strong>&ldquo;Owner document not saved&rdquo;</strong> is the first error "
             "everybody hits. A link stores a path to another file; until your assembly "
             "has a path of its own, FreeCAD cannot work out the relative one. Save first, "
             "always.")

    b2 = fig("08_asm_01_frame_placed", "FRAME AT THE ORIGIN",
             "The first component goes in unmoved &mdash; it defines the machine's "
             "coordinate system") + """
<h3>The first component is special</h3>
<p>Whatever you place first, place it at the origin and leave it there. Everything else is
positioned relative to it, so it may as well be the part with the most interfaces &mdash;
here, the frame.</p>
""" + note("In the Assembly workbench you would additionally add a <strong>Fixed</strong> "
           "joint (or tick <em>grounded</em>) so the solver knows this component does not "
           "move. Without a grounded component the solver has nothing to solve against.")

    d.sheet("02", P, "SETUP", "Starting the assembly", """
<p class="lede">Three things to get right at the start: save the document, open the sources,
and ground the first component.</p>
""" + cols(a2, b2), eyebrow="Save before you link")

    a3 = """
<h3>Placing the front rank</h3>
<p>Both tynes were modelled with their mounting face at <strong>z = 0</strong>, centred on
their bolt pattern. The frame's underside is also at z = 0. So placing a tyne is two
numbers:</p>
""" + code("""
front bar centreline    y = -10 in
tyne stations            x = -38, -19, 0, +19, +38     (19 in pitch)

Placement = (x, -10, 0)   no rotation
""") + """
<p>That is the payoff for choosing the part origin carefully in Deck 3. Had the tyne's
origin been at a bounding-box corner, every placement would carry three correction terms
and a rotation.</p>
""" + note("<strong>Design parts around their interfaces.</strong> It costs nothing while "
           "modelling and it saves the whole assembly.")

    b3 = plates([("08_asm_02_front_rank", "FRONT RANK",
                  "5 &times; Tine 01 at 19 in pitch"),
                 ("08_asm_03_rear_rank", "REAR RANK",
                  "4 &times; Tine 02, offset 9.5 in")]) + \
        code("""
rear bar centreline     y = +10 in
tyne stations            x = -28.5, -9.5, +9.5, +28.5

  = front stations + 9.5 in   -> the stagger
""")

    d.sheet("03", P, "TYNES", "Nine tynes, two link arrays", """
<p class="lede">Two objects in the tree carry all nine tynes. The stagger is a single
9.5&nbsp;inch offset applied to the rear list.</p>
""" + cols(a3, b3) + fig("08_asm_04_rank_stagger", "PLAN",
                         "The nine points fall on an even 9.5 in grid &mdash; five from the "
                         "front bar, four from the rear"),
            eyebrow="One object, five instances")

    a4 = """
<h3>The trap in link arrays</h3>
<p>A link array's <code>PlacementList</code> holds placements <strong>relative to the
link's own Placement</strong>. Set both and the offsets compound.</p>
""" + code("""
WRONG
  lnk.PlacementList = [(-38,-10,0), (-19,-10,0), ...]
  lnk.Placement     = (-38,-10,0)        <- also set

  -> instances land at -76, -57, -38, -19, 0
     the whole rank is 38 in off, and nothing lines up

RIGHT
  lnk.PlacementList = [(-38,-10,0), (-19,-10,0), ...]
  lnk.Placement     = identity           <- leave it alone
""") + fig("08_asm_05_blades", "BLADES PLACED",
           "Nine sweeps, one under each tyne point")

    b4 = """
<h3>Placing the blades</h3>
<p>Each sweep sits at its tyne's point. The tyne's tip coordinate comes straight out of the
part model, so the blade placement is the tyne placement plus a known offset.</p>
""" + code("""
Tine 01 point (part coords)   (-4.53, -23.71)
Tine 02 point (part coords)  (-10.43, -17.00)

blade placement = tyne placement + point + small seat offset
""") + warn("<strong>These are placements, not joints.</strong> Move the tyne and the blade "
            "does <em>not</em> follow &mdash; you would edit both. A "
            "<strong>Coincident</strong> joint between the tyne's point face and the "
            "blade's top face would maintain that relationship properly. For a static "
            "render it does not matter; for a machine you intend to modify, it does.")

    d.sheet("04", P, "PLACEMENT", "Blades, and one trap", """
<p class="lede">The blades go on next. And here is the mistake that cost an hour: link
arrays offset twice if you let them.</p>
""" + cols(a4, b4), eyebrow="PlacementList is relative")

    a5 = """
<h3>How joints work</h3>
<p>The Assembly workbench's joints are FreeCAD's answer to SolidWorks mates. You pick a
feature on each of two components and the solver keeps the relationship true.</p>
""" + tbl(["Joint", "Degrees left", "SolidWorks equivalent"],
          [["<strong>Fixed</strong>", "0", "Fix / ground"],
           ["<strong>Coincident</strong>", "1 rotation", "Concentric + coincident"],
           ["<strong>Revolute</strong>", "1 rotation", "Hinge"],
           ["<strong>Cylindrical</strong>", "1 rot + 1 slide", "Concentric"],
           ["<strong>Slider</strong>", "1 slide", "Slot"],
           ["<strong>Planar</strong>", "2 slide + 1 rot", "Coincident (faces)"],
           ["<strong>Distance</strong>", "varies", "Distance mate"]])

    b5 = """
<h3>Bolting a tyne to the bar, properly</h3>
""" + steps([("<strong>Assembly ▸ Create joint ▸ Coincident</strong>", ""),
             ("Pick the <strong>underside of the tool bar</strong> on the frame", ""),
             ("Pick the <strong>top of the tyne's mounting head</strong>", ""),
             ("The two faces snap flush. One rotation is still free.", ""),
             ("Add a second Coincident on a <strong>bolt hole</strong> of each &mdash; "
              "that removes the rotation and the sideways slide", ""),
             ("The tyne is now fully located by its real interfaces", "")]) + \
        note("Do this once, by hand, even though this course places the tynes numerically. "
             "The joint dialog is where you find out that your bolt holes actually line up "
             "&mdash; and on this machine they do, because the frame's 3&nbsp;in spacing "
             "and the tyne's 3&nbsp;in spacing came from the same reading of the "
             "transcript.")

    d.sheet("05", P, "JOINTS", "Doing it with joints instead", """
<p class="lede">Worth doing at least once by hand, because a joint tests something a
placement never does: whether the parts actually fit each other.</p>
""" + cols(a5, b5), eyebrow="Mates, FreeCAD style")

    a6 = tbl(["Component", "Off", "Each", "Total"],
             [["Frame", "1", "289.5 in&sup3;", "82.2 lb"],
              ["Tine 01", "5", "93.7 in&sup3;", "133.1 lb"],
              ["Tine 02", "4", "77.7 in&sup3;", "88.3 lb"],
              ["Blade 01", "5", "8.45 in&sup3;", "12.0 lb"],
              ["Blade 02", "4", "8.45 in&sup3;", "9.6 lb"],
              ["Clamp 01", "2", "42.9 in&sup3;", "24.3 lb"],
              ["Clamp 02", "2", "48.5 in&sup3;", "27.5 lb"],
              ["<strong>Total</strong>", "<strong>23</strong>", "1327.7 in&sup3;",
               "<strong>377 lb</strong>"]]) + \
        note("At 0.284&nbsp;lb/in&sup3; for mild steel. 377&nbsp;lb / 171&nbsp;kg is "
             "comfortably within the lift capacity of a 35&nbsp;hp compact tractor, which "
             "is the right size of machine for a 76&nbsp;in swath.")

    b6 = plates([("08_asm_hero_Front", "FRONT", "76 in working width"),
                 ("08_asm_hero_Right", "RIGHT", "both ranks, both tyne types"),
                 ("08_asm_hero_Top", "PLAN", "the 9.5 in point spacing"),
                 ("08_asm_hero_Isometric", "ISOMETRIC", "complete")], "grid-2")

    d.sheet("06", P, "VERIFY", "The machine, complete", """
<p class="lede">Sixteen components. The mass comes out of the model, so you can check the
tractor can lift it before anyone cuts steel.</p>
""" + cols(a6, b6), eyebrow="Check the numbers")

    return d
