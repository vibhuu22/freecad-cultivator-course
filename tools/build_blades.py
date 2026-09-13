# -*- coding: utf-8 -*-
"""Parts 6 and 7 - Blade 01 and Blade 02, the sweeps that do the cutting.

SolidWorks builds these flat and then bends them with Flex > Bending, radius
-10 in for Blade 01 and -16 in for Blade 02.  FreeCAD has no Flex.  Instead we
build the blade curved by construction: sweep the 13 x 0.2 in section along an
arc of the wanted radius with an Additive Pipe, then cut the plan shape.

That is not a workaround, it is the better model.  The bend radius is a
spreadsheet parameter, so Blade 02 is Blade 01 with one cell changed from 10 to
16 - which is precisely the edit the tutorial makes in SolidWorks.

  13 in    blade span
  4 in     blade length, fore and aft (developed along the arc)
  0.2 in   sheet thickness
  13 deg   sweep-back of the cutting edge, giving the 1.5 in rise at each end
  R10/R16  bend radius
"""
import sys, math
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H

import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher
from FreeCAD import Vector

H.set_units()
SHOT = []

SPAN  = 13.0      # blade span, across the machine
LEN   = 4.0       # blade length fore and aft, measured along the arc
SHEET = 0.2       # sheet thickness
EDGE  = 13.0      # cutting edge sweep-back, degrees
RISE  = SPAN / 2.0 * math.tan(math.radians(EDGE))    # 1.50 in
TRAIL = LEN / 2.0


def snap(name, orient=None):
    if orient:
        H.view(orient)
    H.shot(name)
    SHOT.append(name)


def edit_snap(sk, name):
    Gui.ActiveDocument.setEdit(sk)
    H.pump(300)
    Gui.SendMsgToActiveView("ViewFit")
    H.pump(200)
    snap(name)
    Gui.ActiveDocument.resetEdit()
    H.pump(200)


def arc_points(R):
    """Spine arc: starts at the cutting edge, horizontal, and lifts to the rear."""
    th = LEN / R
    cy, cz = -TRAIL, R
    p0 = (-TRAIL, 0.0)
    p1 = (cy + R * math.sin(th), cz - R * math.cos(th))
    return (cy, cz), p0, p1, th


# =============================================================== the document
doc = H.newdoc("Blade")
Gui.activateWorkbench("PartDesignWorkbench")
H.pump(200)

R0 = 10.0
PAR = [
    ("Span",        "13 in",   "Blade span, across the machine"),
    ("BladeLength", "4 in",    "Blade length fore and aft, along the arc"),
    ("Sheet",       "0.2 in",  "Sheet thickness"),
    ("EdgeAngle",   "13 deg",  "Sweep-back of the cutting edge"),
    ("EdgeRise",    "=Span / 2 * tan(EdgeAngle)", "Rise of the cutting edge (derived)"),
    ("BendRadius",  "10 in",   "Bend radius - 10 for Blade 01, 16 for Blade 02"),
]
H.params_sheet(doc, PAR, title="Blade parameters")
snap("06_blade_00_params")

bd = H.body(doc, "Blade")
H.activate(bd)

# ------------------------------------------------------------------ the spine
(CY, CZ), P0, P1, TH = arc_points(R0)
sk_spine = H.sketch(bd, H.YZ, "Sk_Spine")
g_arc = sk_spine.addGeometry(Part.ArcOfCircle(
    Part.Circle(Vector(H.inch(CY), H.inch(CZ), 0), Vector(0, 0, 1), H.inch(R0)),
    -math.pi / 2.0, -math.pi / 2.0 + TH))
sk_spine.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g_arc, 1, H.inch(P0[0])))
sk_spine.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, g_arc, 1, H.inch(P0[1])))
c_r = sk_spine.addConstraint(Sketcher.Constraint("Radius", g_arc, H.inch(R0)))
sk_spine.renameConstraint(c_r, "BendRadius")
c_cx = sk_spine.addConstraint(Sketcher.Constraint("DistanceX", g_arc, 1, g_arc, 3, 0.0))
sk_spine.renameConstraint(c_cx, "TangentAtEdge")     # centre directly above the edge
c_e = sk_spine.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g_arc, 2, H.inch(P1[0])))
sk_spine.renameConstraint(c_e, "SpineEnd")
sk_spine.setExpression("Constraints.BendRadius", u"Params.BendRadius")
sk_spine.setExpression("Constraints.SpineEnd",
                       u"-Params.BladeLength / 2 + Params.BendRadius "
                       u"* sin(Params.BladeLength / Params.BendRadius * 1rad)")
doc.recompute()
print("spine:", H.dof_text(sk_spine), "DoF", sk_spine.DoF,
      "conflict", sk_spine.ConflictingConstraints)
edit_snap(sk_spine, "06_blade_01_sketch_spine")

# ---------------------------------------------------------------- the section
sk_sec = H.sketch(bd, H.XZ, "Sk_Section")
sk_sec.AttachmentOffset = App.Placement(Vector(0, 0, H.inch(TRAIL)), App.Rotation())
H.crect_centred(sk_sec, SPAN, SHEET, "Span", "Sheet")
sk_sec.setExpression("Constraints.Span", u"Params.Span")
sk_sec.setExpression("Constraints.Sheet", u"Params.Sheet")
sk_sec.setExpression(".AttachmentOffset.Base.z", u"Params.BladeLength / 2")
doc.recompute()
print("section:", H.dof_text(sk_sec))
edit_snap(sk_sec, "06_blade_02_sketch_section")

pipe = doc.addObject("PartDesign::AdditivePipe", "Pipe_Blade")
H.append_tip(bd, pipe)
pipe.Profile = sk_sec
pipe.Spine = (sk_spine, ["Edge1"])
pipe.Mode = "Standard"
doc.recompute()
print("pipe:", pipe.State, "bbox y/z:",
      round(pipe.Shape.BoundBox.YMin / H.IN, 2), round(pipe.Shape.BoundBox.YMax / H.IN, 2),
      "|", round(pipe.Shape.BoundBox.ZMin / H.IN, 2), round(pipe.Shape.BoundBox.ZMax / H.IN, 2))
H.color(pipe, H.SHARE)
snap("06_blade_03_additive_pipe", "Isometric")

# ------------------------------------------------------------- the plan shape
sk_plan = H.sketch(bd, H.XY, "Sk_PlanShape")
H.crect_centred(sk_plan, SPAN + 6, LEN + 6, "StockW", "StockL")   # material to remove
l0 = H.poly(sk_plan, [(0.0, -TRAIL), (SPAN / 2.0, -TRAIL + RISE), (SPAN / 2.0, TRAIL),
                      (-SPAN / 2.0, TRAIL), (-SPAN / 2.0, -TRAIL + RISE)], close=True)
sk_plan.addConstraint(Sketcher.Constraint("Vertical", l0[1]))
sk_plan.addConstraint(Sketcher.Constraint("Vertical", l0[3]))
sk_plan.addConstraint(Sketcher.Constraint("Horizontal", l0[2]))
sk_plan.addConstraint(Sketcher.Constraint("Symmetric", l0[1], 1, l0[3], 2, -2))
sk_plan.addConstraint(Sketcher.Constraint("PointOnObject", l0[0], 1, -2))
cd = [sk_plan.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, l0[0], 1, H.inch(-TRAIL))),
      sk_plan.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, l0[1], 1, H.inch(SPAN / 2.0))),
      sk_plan.addConstraint(Sketcher.Constraint("DistanceY", l0[0], 1, l0[0], 2, H.inch(RISE))),
      sk_plan.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, l0[2], 1, H.inch(TRAIL)))]
for c, nm in zip(cd, ("TipOffset", "HalfSpan", "EdgeRise", "TrailOffset")):
    sk_plan.renameConstraint(c, nm)
sk_plan.setExpression("Constraints.TipOffset", u"-Params.BladeLength / 2")
sk_plan.setExpression("Constraints.HalfSpan", u"Params.Span / 2")
sk_plan.setExpression("Constraints.EdgeRise", u"Params.EdgeRise")
sk_plan.setExpression("Constraints.TrailOffset", u"Params.BladeLength / 2")
doc.recompute()
print("plan:", H.dof_text(sk_plan), "DoF", sk_plan.DoF,
      "conflict", sk_plan.ConflictingConstraints)
edit_snap(sk_plan, "06_blade_04_sketch_plan_shape")

poc = H.pocket(bd, sk_plan, 0, through=True, midplane=True, name="Pocket_PlanShape")
doc.recompute()
print("pocket:", poc.State)
snap("06_blade_05_pocket_plan_shape", "Isometric")

# ------------------------------------------------------------ Blade 01 saved
H.hide_sketches(doc)
doc.recompute()
print(H.report(doc))
H.shot_set("06_blade01_final", ("Isometric", "Front", "Right", "Top"))
snap("06_blade01_06_complete", "Isometric")
H.savedoc(doc, "06_blade01")

# ------------------------------------------------------------------ Blade 02
# The whole point of building it parametrically: one cell, 10 -> 16.
snap("07_blade02_00_before_edit", "Right")
doc.Params.set("BendRadius", "16 in")
doc.recompute()
print("after radius change:", H.report(doc))
H.shot_set("07_blade02_final", ("Isometric", "Front", "Right", "Top"))
snap("07_blade02_01_after_edit", "Right")
H.savedoc(doc, "07_blade02")
print("SHOTS:", SHOT)
