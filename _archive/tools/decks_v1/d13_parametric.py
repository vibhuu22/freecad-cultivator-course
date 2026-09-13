# -*- coding: utf-8 -*-
"""Deck 13 - Making it parametric."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)

P = "PARAMETRIC"


def build():
    d = Deck("13-making-it-parametric", "Making It Parametric")

    d.sheet("00", P, "OVERVIEW", "Making It Parametric", """
<p class="lede">Everything so far has been building toward this. Every dimension in this
machine lives in a spreadsheet cell, which means the model is not a nine-tyne cultivator —
it is a <strong>family</strong> of cultivators, and you pick one by editing a table.</p>
""" + fig("01_frame_01_params_spreadsheet", "THE FRAME'S PARAMETERS",
          "15 cells. Nothing in the frame is typed anywhere else.")
        + specs([("Frame", "15 parameters"), ("Tine 01", "11"), ("Tine 02", "13"),
                 ("Clamps", "8 each"), ("Blades", "6"),
                 ("Typed twice anywhere", "none")]),
            eyebrow="Deck 13", kind="title")

    a = """
<h3>What parametric actually buys you</h3>
""" + phases([("Change, not rebuild",
               "A 9-tyne machine becomes an 11-tyne machine in one cell. Without "
               "parameters it is a re-model."),
              ("Design intent is recorded",
               "<code>InnerLength = FrameLength - 2 * MemberSize</code> says the inner "
               "rectangle is inset by one member width. The number 78 says nothing."),
              ("Errors surface immediately",
               "Set HoleCount to 15 and the end holes run off the frame. The model shows "
               "you, instead of you finding out on the shop floor."),
              ("It is reviewable",
               "Someone else can read fifteen named cells. Nobody can review 40 numbers "
               "scattered through a feature tree.")])

    b = """
<h3>The three-layer rule</h3>
""" + code("""
layer 1   INPUTS      numbers a designer chose
          FrameLength 82 in   HolePitch 9.5 in   BendRadius 16 in

layer 2   DERIVED     formulas of layer 1
          Sweep    = asin(WorkHeight / CurveRadius)
          OuterR   = CurveRadius + BarWidth / 2
          FootReach = -(ShankWidth/2 + BendRadius)
                    + (BendRadius + ShankWidth) * cos(Rake)
                    - FootLength * sin(Rake)

layer 3   GEOMETRY    constraints bound to layer 1 or 2
          Constraints.FrameLength = Params.FrameLength
""") + note("Never let layer 3 contain arithmetic. If a constraint needs "
            "<code>82 - 2*2</code>, that belongs in a named derived cell, where it is "
            "visible and can be checked.")

    d.sheet("01", P, "PRINCIPLE", "Why bother", """
<p class="lede">The discipline costs about twenty seconds per dimension. Here is what it
returns.</p>
""" + cols(a, b), eyebrow="Inputs, derived, geometry")

    a2 = """
<h3>Building the table</h3>
""" + steps([("<strong>Spreadsheet</strong> workbench ▸ <strong>Create spreadsheet</strong>",
              ""),
             ("Column A: the name. Column B: the value <em>with its unit</em>. Column C: "
              "what it means.", "82 in    not    82"),
             ("Select the B cell, click <strong>Alias</strong>, type the name", ""),
             ("Aliased cells shade yellow", ""),
             ("For a derived cell, start with <code>=</code> and use the aliases",
              "=Span / 2 * tan(EdgeAngle)")]) + \
        warn("<strong>Always include the unit.</strong> A cell holding <code>82</code> is a "
             "dimensionless number; a cell holding <code>82 in</code> is a length. Bind a "
             "dimensionless cell to a length constraint and FreeCAD will either refuse or "
             "silently treat it as millimetres.")

    b2 = """
<h3>Binding a constraint to a cell</h3>
""" + steps([("Open the sketch and double-click the dimension you want to drive", ""),
             ("Click the small blue <strong>f(x)</strong> circle in the value box", ""),
             ("Type the reference", "Params.FrameLength"),
             ("The box turns orange and shows the resolved value", ""),
             ("Name the constraint too &mdash; it makes the constraint list readable", "")],
            compact=True) + code("""
# the same thing from Python
sk.setExpression("Constraints.FrameLength",
                 u"Params.FrameLength")

sk.setExpression("Constraints.InnerLength",
                 u"Params.FrameLength - 2 * Params.MemberSize")

pad.setExpression("Length", u"Params.MemberSize")

sk.setExpression(".AttachmentOffset.Base.z",
                 u"Params.MemberSize - Params.WallThk")
""") + note("That last one is worth noticing: <strong>attachment offsets can be driven by "
            "expressions too</strong>, not just dimensions. The frame's tube-bore sketch "
            "floats at <code>MemberSize - WallThk</code>, so it follows the tube wall "
            "automatically.")

    d.sheet("02", P, "MECHANICS", "Cells, aliases, expressions", """
<p class="lede">Three steps: make the cell, alias it, reference it. The third step is where
most people stop too early.</p>
""" + cols(a2, b2), eyebrow="Alias, then reference")

    a3 = """
<h3>Worked change: 9 tynes to 11</h3>
""" + code("""
01_frame.FCStd  ▸  Params

  HoleCount    9   ->  11
  FrameLength  82  ->  101      (10 x 9.5 + 6 in margin)

recompute
""") + """
<p>What happens, in order:</p>
""" + steps([("The frame plan sketch widens to 101 in; the inner rectangle follows because "
              "it is <code>FrameLength - 2*MemberSize</code>", ""),
             ("The tube-bore sketch widens with it", ""),
             ("The first hole's x moves to <code>-(11-1) * 9.5 / 2</code> = &minus;47.5", ""),
             ("The LinearPattern spans <code>(11-1) * 9.5</code> = 95 in with 11 "
              "occurrences", ""),
             ("The clevises stay at &plusmn;15 in &mdash; hitch spacing is set by the "
              "tractor, not by the frame", "")]) + \
        note("Five cascading changes from two cells, and none of them needed a decision. "
             "That is what &ldquo;the model captures design intent&rdquo; means in "
             "practice.")

    b3 = """
<h3>Worked change: R10 to R16</h3>
""" + code("""
06_blade01.FCStd  ▸  Params

  BendRadius   10 in  ->  16 in
""") + plates([("07_blade02_00_before_edit", "R10", "0.98 in tall"),
               ("07_blade02_01_after_edit", "R16", "0.69 in tall")]) + """
<p>The spine arc flattens; the swept plate follows; the plan-shape pocket re-cuts the same
duckfoot outline out of the new surface. Same 13&nbsp;in span, same 4&nbsp;in of steel,
same 8.45&nbsp;in&sup3;.</p>
""" + note("This <em>is</em> Blade 02. The two parts in <code>parts/</code> are the same "
           "model saved at two values of one cell.")

    d.sheet("03", P, "WORKED", "Two changes, end to end", """
<p class="lede">Follow the cascade. Neither of these edits needed any judgement — the model
already knew what depended on what.</p>
""" + cols(a3, b3), eyebrow="Watch it cascade")

    a4 = """
<h3>Driving several files from one table</h3>
<p>Each part currently has its own <code>Params</code> sheet, and some numbers appear in
more than one &mdash; the &oslash;0.5 bolt hole and the 3&nbsp;in bolt spacing are in the
frame <em>and</em> in both tynes. That is a duplication waiting to go wrong.</p>
""" + phases([("A master document",
               "One file holding nothing but the machine's parameters. Each part links to "
               "it with an App::Link and references <code>Master.Params.BoltSpacing</code>."),
              ("A VarSet",
               "FreeCAD 1.0's Structure toolbar has <strong>Create variable set</strong> "
               "&mdash; a lightweight parameter holder that lives in the document and can "
               "be referenced across links."),
              ("External expressions",
               "<code>&lt;&lt;Master&gt;&gt;.Params.BoltSpacing</code> references another "
               "open document directly. Simple, but the file must be open.")]) + \
        warn("Whichever route, the rule is the same: <strong>a number that appears in two "
             "parts should be defined once</strong>. The bolt spacing is a property of the "
             "machine, not of the tyne.")

    b4 = """
<h3>What should be shared</h3>
""" + tbl(["Parameter", "Appears in", "Owner"],
          [["<code>BoltSpacing</code> 3 in", "frame, tine 01, tine 02", "the machine"],
           ["<code>BoltDia</code> 0.5 in", "frame, tine 01, tine 02", "the machine"],
           ["<code>HeadLength</code> 5 in", "tine 01, tine 02", "the machine"],
           ["<code>HolePitch</code> 9.5 in", "frame, assembly", "the machine"],
           ["<code>MemberSize</code> 2 in", "frame", "the frame"],
           ["<code>BendRadius</code>", "blades", "each blade"],
           ["<code>Rake</code> 35&deg;", "tine 01", "tine 01"]]) + \
        note("Notice how the shared ones are all <strong>interface</strong> dimensions "
             "&mdash; the numbers where two parts meet. That is exactly the set that must "
             "never drift apart, and exactly the set a master table should own.")

    d.sheet("04", P, "NEXT LEVEL", "One table for the whole machine", """
<p class="lede">The obvious improvement to this model, and the one you should make if you
take it further.</p>
""" + cols(a4, b4), eyebrow="Interfaces belong to the machine")

    a5 = """
<h3>Rules that keep it working</h3>
""" + ticks([
        "<strong>Every driving dimension named.</strong> <code>Constraint12</code> cannot "
        "be referenced usefully and cannot be reviewed.",
        "<strong>No arithmetic in constraints.</strong> Put it in a derived cell where it "
        "is visible.",
        "<strong>Units in every cell.</strong> <code>82 in</code>, not <code>82</code>.",
        "<strong>Angles as angles.</strong> <code>35 deg</code>, so <code>cos()</code> and "
        "<code>sin()</code> behave.",
        "<strong>Comment every cell</strong> in column C. Six months later that column is "
        "the only documentation you will have.",
        "<strong>Test the extremes.</strong> Set every parameter to its plausible minimum "
        "and maximum and recompute. Models break at the edges, not in the middle."])

    b5 = """
<h3>Where a parametric model breaks</h3>
""" + tbl(["Change", "What breaks", "Why"],
          [["Big increase in a fillet radius", "the Fillet feature",
            "no material left &mdash; exactly the clevis nose in Deck 5"],
           ["Wall thicker than half the member", "the tube bore pocket",
            "the bore inverts"],
           ["Bend radius toward zero", "the Additive Pipe", "the sweep self-intersects"],
           ["Hole pitch &times; count &gt; frame length", "nothing &mdash; and that is worse",
            "holes run off the end silently; add a check cell"],
           ["Renaming an alias", "every expression using it",
            "FreeCAD does not rename references for you"]]) + \
        note("<strong>Add check cells.</strong> A cell reading "
             "<code>=(HoleCount-1)*HolePitch &lt; FrameLength - 2*MemberSize</code> gives "
             "you a visible true/false. It is the cheapest design review there is.")

    d.sheet("05", P, "DISCIPLINE", "Keeping it honest", """
<p class="lede">A parametric model that has never been tested at its limits is a parametric
model that only works at one set of values.</p>
""" + cols(a5, b5), eyebrow="Test the extremes")

    return d
