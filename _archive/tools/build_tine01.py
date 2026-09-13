# -*- coding: utf-8 -*-
"""Part 2 - Tine 01, the rigid front-rank tyne (5 off).

Side profile on the Right plane (FreeCAD YZ_Plane), origin at the centre of the
mounting face so the part drops straight onto the tool bar in the assembly.

  25 in   overall tyne length, measured along the shank centreline
  15 in   straight vertical shank
  2.25 in shank width, fore and aft
  1.5 in  shank thickness, across the machine
  35 deg  forward rake of the foot          (assumption - see the deck)
  6 in    inner bend radius                 (assumption - see the deck)
  5 x 1.25 in mounting head, two 0.5 in bolts at 3 in centres
"""
import sys, math
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\_archive\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H

import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher
from FreeCAD import Vector

H.set_units()
SHOT = []


def snap(name, orient=None):
    if orient:
        H.view(orient)
    H.shot(name)
    SHOT.append(name)


def edit_snap(sk, name):
    Gui.ActiveDocument.setEdit(sk)
    H.pump(300)
    H.fit_sketch(sk)
    H.pump(200)
    snap(name)
    Gui.ActiveDocument.resetEdit()
    H.pump(200)


# ------------------------------------------------------------------ dimensions
W      = 2.25      # shank width, fore and aft
THK    = 1.5       # shank thickness, across the machine
HSTR   = 15.0      # straight vertical shank
RI     = 6.0       # inner bend radius
RAKE   = 35.0      # forward rake of the foot, degrees
LTOT   = 25.0      # overall tyne length along the centreline
HEADL  = 5.0       # mounting head length, along the tool bar
HEADT  = 1.25      # mounting head thickness
BOLTS  = 3.0       # bolt centres
BDIA   = 0.5       # bolt hole diameter

RO   = RI + W                                   # outer bend radius, 8.25
RC   = RI + W / 2.0                             # centreline bend radius, 7.125
A    = math.radians(RAKE)
# Straight foot below the bend. The exact value that makes the centreline 25 in
# long is LTOT - HSTR - RC*A = 5.6476 in; the sketch is driven by the rounded
# 5.65 in (0.002 in longer) so every label on the slide is a readable number.
LLEG = 5.65
CY   = -HSTR                                    # bend centre
CX   = -W / 2.0 - RI                            # bend centre, -7.125
TANG = (math.sin(-A), -math.cos(-A))            # foot direction, down and forward


def arc_pt(r, ang):
    return (CX + r * math.cos(ang), CY + r * math.sin(ang))


def along(p, d, s):
    return (p[0] + d[0] * s, p[1] + d[1] * s)


p_top_f = (-W / 2.0, 0.0)
p_top_r = (W / 2.0, 0.0)
p_bend_r = arc_pt(RO, 0.0)                      # (1.125, -15)
p_bend_f = arc_pt(RI, 0.0)                      # (-1.125, -15)
p_arc_r = arc_pt(RO, -A)
p_arc_f = arc_pt(RI, -A)
p_tip_r = along(p_arc_r, TANG, LLEG)
p_tip_f = along(p_arc_f, TANG, LLEG)

# ------------------------------------------------------------------- document
doc = H.newdoc("Tine01")
Gui.activateWorkbench("PartDesignWorkbench")
H.pump(300)

PAR = [
    ("ShankWidth",   "2.25 in", "Shank width, fore and aft"),
    ("ShankThk",     "1.5 in",  "Shank thickness, across the machine"),
    ("StraightHt",   "15 in",   "Straight vertical part of the shank"),
    ("BendRadius",   "6 in",    "Inner radius of the forward bend"),
    ("Rake",         "35 deg",  "Forward rake of the foot"),
    ("FootLength",   "5.65 in", "Straight foot below the bend (tyne is 25 in long)"),
    ("FootReach",    "=(ShankWidth / 2 + BendRadius) - (BendRadius + ShankWidth) "
                     "* cos(Rake) + FootLength * sin(Rake)",
                     "Result: how far forward the point reaches"),
    ("HeadLength",   "5 in",    "Mounting head length along the tool bar"),
    ("HeadThk",      "1.25 in", "Mounting head thickness"),
    ("BoltSpacing",  "3 in",    "Bolt centres"),
    ("BoltDia",      "0.5 in",  "Bolt hole diameter"),
]
sheet = H.params_sheet(doc, PAR, title="Tine 01 parameters")
H.shot_sheet(sheet, "02_tine01_00_params")

bd = H.body(doc, "Tine01")
H.activate(bd)
snap("02_tine01_01_body", "Isometric")

# --------------------------------------------------------------- side profile
sk = H.sketch(bd, H.YZ, "Sk_TineProfile")
g_top = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_top_f[0]), H.inch(p_top_f[1]), 0),
                                        Vector(H.inch(p_top_r[0]), H.inch(p_top_r[1]), 0)))
g_rear = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_top_r[0]), H.inch(p_top_r[1]), 0),
                                         Vector(H.inch(p_bend_r[0]), H.inch(p_bend_r[1]), 0)))
c_out = Part.Circle(Vector(H.inch(CX), H.inch(CY), 0), Vector(0, 0, 1), H.inch(RO))
g_aout = sk.addGeometry(Part.ArcOfCircle(c_out, -A, 0.0))
g_leg_r = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_arc_r[0]), H.inch(p_arc_r[1]), 0),
                                          Vector(H.inch(p_tip_r[0]), H.inch(p_tip_r[1]), 0)))
g_tip = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_tip_r[0]), H.inch(p_tip_r[1]), 0),
                                        Vector(H.inch(p_tip_f[0]), H.inch(p_tip_f[1]), 0)))
g_leg_f = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_tip_f[0]), H.inch(p_tip_f[1]), 0),
                                          Vector(H.inch(p_arc_f[0]), H.inch(p_arc_f[1]), 0)))
c_in = Part.Circle(Vector(H.inch(CX), H.inch(CY), 0), Vector(0, 0, 1), H.inch(RI))
g_ain = sk.addGeometry(Part.ArcOfCircle(c_in, -A, 0.0))
g_front = sk.addGeometry(Part.LineSegment(Vector(H.inch(p_bend_f[0]), H.inch(p_bend_f[1]), 0),
                                          Vector(H.inch(p_top_f[0]), H.inch(p_top_f[1]), 0)))
# The four smooth joins get endpoint-to-endpoint tangency, which carries the
# coincidence with it; the four sharp corners get plain coincidence.
for a, b in ((g_rear, g_aout), (g_aout, g_leg_r), (g_leg_f, g_ain), (g_ain, g_front)):
    H.tangent_join(sk, a, b)
H.weld(sk)

sk.addConstraint(Sketcher.Constraint("Horizontal", g_top))
sk.addConstraint(Sketcher.Constraint("Vertical", g_rear))
sk.addConstraint(Sketcher.Constraint("Vertical", g_front))
sk.addConstraint(Sketcher.Constraint("Coincident", g_aout, 3, g_ain, 3))   # concentric
sk.addConstraint(Sketcher.Constraint("Perpendicular", g_tip, g_leg_r))
sk.addConstraint(Sketcher.Constraint("Parallel", g_leg_f, g_leg_r))
sk.addConstraint(Sketcher.Constraint("Symmetric", g_top, 1, g_top, 2, -1, 1))
cw = sk.addConstraint(Sketcher.Constraint("DistanceX", g_top, 1, g_top, 2, H.inch(W)))
ch = sk.addConstraint(Sketcher.Constraint("Distance", g_rear, H.inch(HSTR)))
cr = sk.addConstraint(Sketcher.Constraint("Radius", g_ain, H.inch(RI)))
cl = sk.addConstraint(Sketcher.Constraint("Distance", g_leg_r, H.inch(LLEG)))
# The rake is the sweep angle of the bend arc. An angle between two *lines* has
# two valid solutions and the solver can flip the tyne backwards; an arc's own
# sweep angle has only one, and it reads as a plain "35 deg" on the slide.
ca = sk.addConstraint(Sketcher.Constraint("Angle", g_aout, A))
for c, nm in ((cw, "ShankWidth"), (ch, "StraightHt"), (cr, "BendRadius"),
              (cl, "FootLength"), (ca, "Rake")):
    sk.renameConstraint(c, nm)
doc.recompute()
print(H.dof_text(sk))
print("tip at", [round(v / H.IN, 3) for v in sk.Geometry[g_tip].StartPoint])
for nm, expr in (("ShankWidth", u"Params.ShankWidth"), ("StraightHt", u"Params.StraightHt"),
                 ("BendRadius", u"Params.BendRadius"), ("FootLength", u"Params.FootLength"),
                 ("Rake", u"Params.Rake")):
    sk.setExpression("Constraints.%s" % nm, expr)
doc.recompute()
# label placement comes from H.LABELS, applied when the sketch is captured
edit_snap(sk, "02_tine01_02_sketch_profile")

pad1 = H.pad(bd, sk, THK, midplane=True, name="Pad_Shank")
H.bind(pad1, "Length", u"Params.ShankThk")
H.color(pad1, H.STEEL_DARK)
doc.recompute()
snap("02_tine01_03_pad_shank", "Isometric")

# ------------------------------------------------------------- mounting head
sk2 = H.sketch(bd, H.XY, "Sk_Head")
H.crect_centred(sk2, HEADL, W, "HeadLength", "HeadWidth")
sk2.setExpression("Constraints.HeadLength", u"Params.HeadLength")
sk2.setExpression("Constraints.HeadWidth", u"Params.ShankWidth")
doc.recompute()
print(H.dof_text(sk2))
pad2 = H.pad(bd, sk2, HEADT, reversed_=True, name="Pad_Head")
H.bind(pad2, "Length", u"Params.HeadThk")
doc.recompute()
snap("02_tine01_04_pad_head", "Isometric")

# ----------------------------------------------------------------- bolt holes
sk3 = H.sketch(bd, H.XY, "Sk_BoltHoles")
b1 = H.ccircle(sk3, -BOLTS / 2.0, 0.0, BDIA, "BoltX", "BoltY", "BoltDia")
b2 = H.circle(sk3, (BOLTS / 2.0, 0.0), BDIA)
sk3.addConstraint(Sketcher.Constraint("Symmetric", b1["geo"], 3, b2, 3, -2))
sk3.addConstraint(Sketcher.Constraint("Equal", b1["geo"], b2))
sk3.setExpression("Constraints.BoltX", u"-Params.BoltSpacing / 2")
sk3.setExpression("Constraints.BoltY", u"0 mm")
sk3.setExpression("Constraints.BoltDia", u"Params.BoltDia")
doc.recompute()
print(H.dof_text(sk3))
edit_snap(sk3, "02_tine01_05_sketch_bolt_holes")

poc = H.pocket(bd, sk3, 0, through=True, name="Pocket_BoltHoles")
doc.recompute()
snap("02_tine01_06_pocket_bolt_holes", "Isometric")

# ------------------------------------------------------------------- finish
H.color(bd, H.STEEL_DARK)
doc.recompute()
print(H.report(doc))
H.shot_set("02_tine01_final", ("Isometric", "Right", "Front", "Top"))
snap("02_tine01_07_complete", "Isometric")
H.savedoc(doc, "02_tine01")
print("SHOTS:", SHOT)
