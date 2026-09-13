# -*- coding: utf-8 -*-
"""Parts 4 and 5 - Clamp 01 and Clamp 02, the frame braces.

The tutorial draws a bent centreline, rounds the corners, then uses Offset
Entities 0.5 in to turn that line into a 0.5 in thick strap and extrudes it
3 in wide.  FreeCAD has no scriptable Offset, and it does not need one: the
same strap comes out of an **Additive Pipe** - sweep a 3 x 0.5 in section
along the bent path.  That is the same tool we use for the Weldments frame
members and for the curved blades, so it is worth learning once.

  Clamp 01 : 18 in rise, 7 in at 45 deg, 4 in return, R2 corners
  Clamp 02 : 26.6 in rise, 6 in at 30 deg, R2 corner
  both     : 3 in wide x 0.5 in thick strap, one 1 in through hole
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

WIDE = 3.0        # strap width, across the machine
THK  = 0.5        # strap thickness, in the plane of the bend
FILR = 2.0        # corner radius
HOLE = 1.0        # attachment hole diameter


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


def path_sketch(bd, segments, name="Sk_Path"):
    """Bent centreline from (0,0), fully constrained, corners rounded.

    segments = [(dy, dz, label), ...] each an offset from the previous corner.
    """
    doc = bd.Document
    sk = H.sketch(bd, H.YZ, name)
    pts = [(0.0, 0.0)]
    for dy, dz, _ in segments:
        pts.append((pts[-1][0] + dy, pts[-1][1] + dz))
    gs = H.poly(sk, pts, close=False)
    sk.addConstraint(Sketcher.Constraint("Coincident", gs[0], 1, -1, 1))
    for g, (dy, dz, label) in zip(gs, segments):
        if abs(dy) < 1e-9:
            sk.addConstraint(Sketcher.Constraint("Vertical", g))
            c = sk.addConstraint(Sketcher.Constraint("DistanceY", g, 1, g, 2, H.inch(dz)))
            sk.renameConstraint(c, label)
        elif abs(dz) < 1e-9:
            sk.addConstraint(Sketcher.Constraint("Horizontal", g))
            c = sk.addConstraint(Sketcher.Constraint("DistanceX", g, 1, g, 2, H.inch(dy)))
            sk.renameConstraint(c, label)
        else:
            cy = sk.addConstraint(Sketcher.Constraint("DistanceX", g, 1, g, 2, H.inch(dy)))
            cz = sk.addConstraint(Sketcher.Constraint("DistanceY", g, 1, g, 2, H.inch(dz)))
            sk.renameConstraint(cy, label + "Run")
            sk.renameConstraint(cz, label + "Rise")
    doc.recompute()
    print("  path before fillets:", H.dof_text(sk))
    # fillet at the shared endpoint: trim the lines back, but keep a construction
    # corner point so the 18 in / 7 in / 4 in dimensions still mean what they say
    for k in range(len(gs) - 1):
        sk.fillet(gs[k], 2, H.inch(FILR), True, True)
    doc.recompute()
    # sk.fillet() creates the arc but leaves its radius free - dimension it
    for gi, g in enumerate(sk.Geometry):
        if g.TypeId == "Part::GeomArcOfCircle" and not sk.getConstruction(gi):
            c = sk.addConstraint(Sketcher.Constraint("Radius", gi, H.inch(FILR)))
            sk.renameConstraint(c, "CornerR%d" % gi)
            sk.setExpression("Constraints.CornerR%d" % gi, u"Params.CornerR")
    doc.recompute()
    print("  path after fillets:", H.dof_text(sk), "DoF", sk.DoF,
          "conflict", sk.ConflictingConstraints, "redundant", sk.RedundantConstraints)
    return sk


def section_sketch(bd, name="Sk_Section"):
    """3 x 0.5 in strap section, sitting on the start of the path."""
    sk = H.sketch(bd, H.XY, name)
    H.crect_centred(sk, WIDE, THK, "StrapWidth", "StrapThk")
    sk.setExpression("Constraints.StrapWidth", u"Params.StrapWidth")
    sk.setExpression("Constraints.StrapThk", u"Params.StrapThk")
    bd.Document.recompute()
    print("  section:", H.dof_text(sk))
    return sk


def sweep(bd, profile, spine, name="Pipe"):
    doc = bd.Document
    f = doc.addObject("PartDesign::AdditivePipe", name)
    H.append_tip(bd, f)
    f.Profile = profile
    f.Spine = (spine, [e for e in ["Edge%d" % (i + 1) for i in range(len(spine.Shape.Edges))]])
    f.Mode = "Standard"
    f.Transition = "Transformed"
    doc.recompute()
    return f


def build_clamp(docname, fname, prefix, segments, hole_z, title, params):
    doc = H.newdoc(docname)
    Gui.activateWorkbench("PartDesignWorkbench")
    H.pump(200)
    H.params_sheet(doc, params, title=title)
    snap(prefix + "_00_params")

    bd = H.body(doc, docname)
    H.activate(bd)

    skp = path_sketch(bd, segments)
    edit_snap(skp, prefix + "_01_sketch_path")
    sks = section_sketch(bd)
    edit_snap(sks, prefix + "_02_sketch_section")

    pipe = sweep(bd, sks, skp, name="Pipe_Strap")
    H.color(pipe, H.PAINT_BLUE)
    doc.recompute()
    print("  pipe:", pipe.State)
    snap(prefix + "_03_additive_pipe", "Isometric")

    skh = H.sketch(bd, H.XZ, "Sk_Hole")
    H.ccircle(skh, 0.0, hole_z, HOLE, "HoleX", "HoleZ", "HoleDia")
    skh.setExpression("Constraints.HoleX", u"0 mm")
    skh.setExpression("Constraints.HoleZ", u"Params.HoleHeight")
    skh.setExpression("Constraints.HoleDia", u"Params.HoleDia")
    doc.recompute()
    print("  hole sketch:", H.dof_text(skh))
    poc = H.pocket(bd, skh, 0, through=True, midplane=True, name="Pocket_Hole")
    doc.recompute()
    snap(prefix + "_04_pocket_hole", "Isometric")

    H.hide_sketches(doc)
    doc.recompute()
    print(H.report(doc))
    H.shot_set(prefix + "_final", ("Isometric", "Right", "Front"))
    snap(prefix + "_05_complete", "Isometric")
    H.savedoc(doc, fname)
    return doc


COMMON = [("StrapWidth", "3 in",   "Strap width, across the machine"),
          ("StrapThk",   "0.5 in", "Strap thickness, in the plane of the bend"),
          ("CornerR",    "2 in",   "Corner radius"),
          ("HoleDia",    "1 in",   "Attachment hole diameter")]

# ------------------------------------------------------------------- Clamp 01
A45 = math.radians(45.0)
build_clamp(
    "Clamp01", "04_clamp01", "04_clamp01",
    [(0.0, 18.0, "Rise"),
     (-7.0 * math.cos(A45), 7.0 * math.sin(A45), "Arm"),
     (-4.0, 0.0, "Return")],
    hole_z=4.0,
    title="Clamp 01 parameters",
    params=COMMON + [("Rise", "18 in", "Straight rise off the tool bar"),
                     ("ArmLength", "7 in", "Angled arm"),
                     ("ArmAngle", "45 deg", "Arm angle from vertical"),
                     ("Return", "4 in", "Horizontal return at the top"),
                     ("HoleHeight", "4 in", "Attachment hole, up from the foot")])

# ------------------------------------------------------------------- Clamp 02
A30 = math.radians(30.0)
build_clamp(
    "Clamp02", "05_clamp02", "05_clamp02",
    [(0.0, 26.6, "Rise"),
     (-6.0 * math.sin(A30), 6.0 * math.cos(A30), "Tip")],
    hole_z=4.0,
    title="Clamp 02 parameters",
    params=COMMON + [("Rise", "26.6 in", "Straight rise off the tool bar"),
                     ("TipLength", "6 in", "Angled tip"),
                     ("TipAngle", "30 deg", "Tip angle from vertical"),
                     ("HoleHeight", "4 in", "Attachment hole, up from the foot")])

print("SHOTS:", SHOT)
