# -*- coding: utf-8 -*-
"""Part 3 - Tine 02, the curved rear-rank tyne (4 off).

Same bolt interface as Tine 01 (5 in head, two 0.5 in bolts at 3 in centres) so
either tyne fits any station on either tool bar.  Below the head the shank is a
single circular sweep instead of a straight-bend-straight shank.

  16 in    centreline radius of the curve   ("radius of 16 inches on both sides")
  15 in    working height, top of curve to the point
  2.5 in   bar width           ("the gap between the two sides is 2.5 inches")
  2 in     straight length before the curve starts
  1.25 in  bar thickness, across the machine

The sweep angle follows from the radius and the working height, so the chord
from the start of the outer arc to the point comes out at ~19.7 in, which is
the transcript's "20.3 inches from the point to the midpoint of the outer arc".
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
W     = 2.5        # bar width in the profile
THK   = 1.25       # bar thickness, across the machine
TOPS  = 2.0        # straight length before the curve
RC    = 16.0       # centreline radius of the curve
WORK  = 15.0       # working height, start of curve down to the point
HEADL = 5.0        # mounting head length along the tool bar
HEADT = 1.25       # mounting head thickness
BOLTS = 3.0
BDIA  = 0.5
TIPR  = 1.0        # corner radius at the point

RO = RC + W / 2.0                       # 17.25, rear (outer) edge
RI = RC - W / 2.0                       # 14.75, front (inner) edge
SW = math.asin(WORK / RC)               # sweep angle, 69.64 deg
CX, CY = -RC, -TOPS                     # curve centre


def arc_pt(r, ang):
    return (CX + r * math.cos(ang), CY + r * math.sin(ang))


p_top_f = (-W / 2.0, 0.0)
p_top_r = (W / 2.0, 0.0)
p_str_r = arc_pt(RO, 0.0)               # (1.25, -2)
p_str_f = arc_pt(RI, 0.0)               # (-1.25, -2)
p_tip_r = arc_pt(RO, -SW)
p_tip_f = arc_pt(RI, -SW)
print("chord outer arc start -> point: %.2f in" %
      math.hypot(p_tip_r[0] - p_str_r[0], p_tip_r[1] - p_str_r[1]))

# ------------------------------------------------------------------- document
doc = H.newdoc("Tine02")
Gui.activateWorkbench("PartDesignWorkbench")
H.pump(300)

PAR = [
    ("BarWidth",    "2.5 in",  "Bar width in the side profile"),
    ("BarThk",      "1.25 in", "Bar thickness, across the machine"),
    ("TopStraight", "2 in",    "Straight length before the curve starts"),
    ("CurveRadius", "16 in",   "Centreline radius of the curve"),
    ("WorkHeight",  "15 in",   "Top of the curve down to the point"),
    ("Sweep",       "=asin(WorkHeight / CurveRadius)", "Result: how far the curve turns"),
    ("HeadLength",  "5 in",    "Mounting head length along the tool bar"),
    ("HeadThk",     "1.25 in", "Mounting head thickness"),
    ("BoltSpacing", "3 in",    "Bolt centres"),
    ("BoltDia",     "0.5 in",  "Bolt hole diameter"),
    ("TipRadius",   "1 in",    "Corner radius at the point"),
]
sheet = H.params_sheet(doc, PAR, title="Tine 02 parameters")
H.shot_sheet(sheet, "03_tine02_00_params")

bd = H.body(doc, "Tine02")
H.activate(bd)

# --------------------------------------------------------------- side profile
sk = H.sketch(bd, H.YZ, "Sk_TineProfile")


def line(a, b):
    return sk.addGeometry(Part.LineSegment(Vector(H.inch(a[0]), H.inch(a[1]), 0),
                                           Vector(H.inch(b[0]), H.inch(b[1]), 0)))


g_top = line(p_top_f, p_top_r)
g_rear = line(p_top_r, p_str_r)
g_aout = sk.addGeometry(Part.ArcOfCircle(
    Part.Circle(Vector(H.inch(CX), H.inch(CY), 0), Vector(0, 0, 1), H.inch(RO)), -SW, 0.0))
g_tip = line(p_tip_r, p_tip_f)
g_ain = sk.addGeometry(Part.ArcOfCircle(
    Part.Circle(Vector(H.inch(CX), H.inch(CY), 0), Vector(0, 0, 1), H.inch(RI)), -SW, 0.0))
g_front = line(p_str_f, p_top_f)

for a, b in ((g_rear, g_aout), (g_ain, g_front)):
    H.tangent_join(sk, a, b)
H.weld(sk)

sk.addConstraint(Sketcher.Constraint("Horizontal", g_top))
sk.addConstraint(Sketcher.Constraint("Vertical", g_rear))
sk.addConstraint(Sketcher.Constraint("Vertical", g_front))
sk.addConstraint(Sketcher.Constraint("Coincident", g_aout, 3, g_ain, 3))    # concentric
sk.addConstraint(Sketcher.Constraint("PointOnObject", g_aout, 3, g_tip))    # tip face is radial
sk.addConstraint(Sketcher.Constraint("Symmetric", g_top, 1, g_top, 2, -1, 1))
cw = sk.addConstraint(Sketcher.Constraint("DistanceX", g_top, 1, g_top, 2, H.inch(W)))
ct = sk.addConstraint(Sketcher.Constraint("Distance", g_rear, H.inch(TOPS)))
# A construction centreline arc carries the two design numbers from the source:
# a 16 in curve radius and a 15 in working height. Dimensioning the edges instead
# would put derived values (R17.25, an 18.17 in drop) on the slide.
g_ac = sk.addGeometry(Part.ArcOfCircle(
    Part.Circle(Vector(H.inch(CX), H.inch(CY), 0), Vector(0, 0, 1), H.inch(RC)), -SW, 0.0), True)
sk.addConstraint(Sketcher.Constraint("Coincident", g_ac, 3, g_aout, 3))     # same centre
sk.addConstraint(Sketcher.Constraint("PointOnObject", g_ac, 2, -2))         # top end on the bar centreline
sk.addConstraint(Sketcher.Constraint("Horizontal", g_ac, 3, g_ac, 2))       # ...level with the centre
sk.addConstraint(Sketcher.Constraint("PointOnObject", g_ac, 1, g_tip))      # far end on the tip face
cr = sk.addConstraint(Sketcher.Constraint("Radius", g_ac, H.inch(RC)))
cd = sk.addConstraint(Sketcher.Constraint("DistanceY", g_ac, 1, g_ac, 2, H.inch(WORK)))
for c, nm in ((cw, "BarWidth"), (ct, "TopStraight"), (cr, "CurveRadius"), (cd, "WorkHeight")):
    sk.renameConstraint(c, nm)
doc.recompute()
print(H.dof_text(sk), "| DoF", sk.DoF, "| conflict", sk.ConflictingConstraints,
      "| redundant", sk.RedundantConstraints)
for nm in ("BarWidth", "TopStraight", "CurveRadius", "WorkHeight"):
    sk.setExpression("Constraints.%s" % nm, u"Params.%s" % nm)
doc.recompute()
edit_snap(sk, "03_tine02_01_sketch_profile")

pad1 = H.pad(bd, sk, THK, midplane=True, name="Pad_Shank")
H.bind(pad1, "Length", u"Params.BarThk")
H.color(pad1, H.STEEL_DARK)
doc.recompute()
snap("03_tine02_02_pad_shank", "Isometric")

# ------------------------------------------------------------- mounting head
sk2 = H.sketch(bd, H.XY, "Sk_Head")
H.crect_centred(sk2, HEADL, W, "HeadLength", "HeadWidth")
sk2.setExpression("Constraints.HeadLength", u"Params.HeadLength")
sk2.setExpression("Constraints.HeadWidth", u"Params.BarWidth")
doc.recompute()
print(H.dof_text(sk2))
pad2 = H.pad(bd, sk2, HEADT, reversed_=True, name="Pad_Head")
H.bind(pad2, "Length", u"Params.HeadThk")
doc.recompute()
snap("03_tine02_03_pad_head", "Isometric")

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
poc = H.pocket(bd, sk3, 0, through=True, name="Pocket_BoltHoles")
doc.recompute()
snap("03_tine02_04_pocket_bolt_holes", "Isometric")

# ---------------------------------------------------------------- point radii
tip_edges = H.edges_where(
    poc, lambda e: H.is_straight_along(e, "x") and
    any(H.at_coord(e, "y", p[0]) and H.at_coord(e, "z", p[1])
        for p in (p_tip_r, p_tip_f)))
print("tip edges:", tip_edges)
if tip_edges:
    fil = H.fillet(bd, poc, tip_edges, TIPR, name="Fillet_Point")
    H.bind(fil, "Radius", u"Params.TipRadius")
    doc.recompute()
    print("fillet state:", fil.State)
snap("03_tine02_05_fillet_point", "Isometric")

# ------------------------------------------------------------------- finish
H.color(bd, H.STEEL_DARK)
doc.recompute()
print(H.report(doc))
H.shot_set("03_tine02_final", ("Isometric", "Right", "Front", "Top"))
snap("03_tine02_06_complete", "Isometric")
H.savedoc(doc, "03_tine02")
print("SHOTS:", SHOT)
