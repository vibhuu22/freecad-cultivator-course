# -*- coding: utf-8 -*-
"""Part 1 - Cultivator main frame.

82 x 22 in rectangular frame welded from 2 x 2 x 0.1875 in square tube,
9 tyne-mounting holes at 9.5 in pitch on each tool bar, and a pair of
lower-link hitch clevises at +/-15 in from the centreline.

Every dimension is driven by the Params spreadsheet, so students can retune
the machine (tyne count, pitch, working width) from one table.
"""
import sys
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H

import FreeCAD as App
import FreeCADGui as Gui
import Sketcher
from FreeCAD import Vector

H.set_units()
SHOT = []


def snap(name, orient=None):
    if orient:
        H.view(orient)
    H.SHOTS_LAST = H.shot(name)
    SHOT.append(name)
    return H.SHOTS_LAST


def edit_snap(sk, name):
    """Open the sketch in the Sketcher and grab the real editing UI."""
    Gui.ActiveDocument.setEdit(sk)
    H.pump(300)
    Gui.SendMsgToActiveView("ViewFit")
    H.pump(200)
    snap(name)
    Gui.ActiveDocument.resetEdit()
    H.pump(200)


# =============================================================== 0  document
doc = H.newdoc("Frame")
Gui.activateWorkbench("PartDesignWorkbench")
H.pump(300)
snap("01_frame_00_empty_document")

# =============================================================== 1  parameters
PAR = [
    ("FrameLength", "82 in",    "Overall width of the tool frame"),
    ("FrameDepth",  "22 in",    "Front bar to rear bar, outside to outside"),
    ("MemberSize",  "2 in",     "Square tube across flats"),
    ("WallThk",     "0.1875 in", "Square tube wall thickness (3/16 in)"),
    ("HolePitch",   "9.5 in",   "Tyne mounting hole pitch"),
    ("HoleDia",     "0.5 in",   "Tyne mounting bolt hole diameter"),
    ("BoltSpacing", "3 in",     "Bolt centres across one tyne station"),
    ("HoleCount",   "9",        "Mounting holes per tool bar"),
    ("HitchOffset", "15 in",    "Lower link clevis, half spacing from centreline"),
    ("HitchGap",    "1.5 in",   "Clear gap between the two clevis plates"),
    ("HitchPlate",  "0.4 in",   "Clevis plate thickness"),
    ("HitchRise",   "3 in",     "Clevis plate height above the frame underside"),
    ("HitchReach",  "5 in",     "Clevis plate length, fore and aft"),
    ("PinDia",      "1 in",     "Lower link pin hole diameter"),
    ("CornerR",     "0.63 in",  "Clevis nose corner radius"),
]
sheet = H.params_sheet(doc, PAR, name="Params", title="Cultivator parameters")
doc.recompute()
Gui.Selection.clearSelection()
snap("01_frame_01_params_spreadsheet")

# =============================================================== 2  body
bd = H.body(doc, "Frame")
H.activate(bd)
doc.recompute()
snap("01_frame_02_body_created", "Isometric")

# =============================================================== 3  plan sketch
L, D, M = 82.0, 22.0, 2.0
sk1 = H.sketch(bd, H.XY, "Sk_FramePlan")
outer = H.crect_centred(sk1, L, D, "FrameLength", "FrameDepth")
inner = H.crect_centred(sk1, L - 2 * M, D - 2 * M, "InnerLength", "InnerDepth")
sk1.setExpression("Constraints.FrameLength", u"Params.FrameLength")
sk1.setExpression("Constraints.FrameDepth",  u"Params.FrameDepth")
sk1.setExpression("Constraints.InnerLength", u"Params.FrameLength - 2 * Params.MemberSize")
sk1.setExpression("Constraints.InnerDepth",  u"Params.FrameDepth  - 2 * Params.MemberSize")
doc.recompute()
print(H.dof_text(sk1))
edit_snap(sk1, "01_frame_03_sketch_plan_constrained")

# =============================================================== 4  pad
pad1 = H.pad(bd, sk1, M, name="Pad_Frame")
H.bind(pad1, "Length", u"Params.MemberSize")
doc.recompute()
H.color(pad1, H.PAINT_RED)
snap("01_frame_04_pad_frame", "Isometric")

# =============================================================== 5  tube bore
t = 0.1875
sk2 = H.sketch(bd, H.XY, "Sk_TubeBore")
sk2.AttachmentOffset = App.Placement(Vector(0, 0, H.inch(M - t)), App.Rotation())
bo = H.crect_centred(sk2, L - 2 * t, D - 2 * t, "BoreOuterL", "BoreOuterD")
bi = H.crect_centred(sk2, L - 2 * M + 2 * t, D - 2 * M + 2 * t, "BoreInnerL", "BoreInnerD")
sk2.setExpression("Constraints.BoreOuterL", u"Params.FrameLength - 2 * Params.WallThk")
sk2.setExpression("Constraints.BoreOuterD", u"Params.FrameDepth  - 2 * Params.WallThk")
sk2.setExpression("Constraints.BoreInnerL",
                  u"Params.FrameLength - 2 * Params.MemberSize + 2 * Params.WallThk")
sk2.setExpression("Constraints.BoreInnerD",
                  u"Params.FrameDepth  - 2 * Params.MemberSize + 2 * Params.WallThk")
sk2.setExpression(".AttachmentOffset.Base.z", u"Params.MemberSize - Params.WallThk")
doc.recompute()
print(H.dof_text(sk2))
poc1 = H.pocket(bd, sk2, M - 2 * t, name="Pocket_TubeBore")
H.bind(poc1, "Length", u"Params.MemberSize - 2 * Params.WallThk")
doc.recompute()
snap("01_frame_05_pocket_tube_bore", "Isometric")

# =============================================================== 6  first station
# One tyne station = two bolt holes 3 in apart along the bar.  The rear-bar pair
# is a Symmetry constraint away from the front-bar pair: Sketcher Symmetry is
# FreeCAD's "Mirror Entities".  All four go in ONE sketch, because PartDesign
# cannot pattern a pattern (or mirror one) - see the deck note on that limit.
x0 = -0.5 * (9 - 1) * 9.5          # -38 in : first station centre
BS = 3.0                           # bolt spacing along the bar
ybar = -0.5 * (D - M)              # -10 in : front bar centreline
sk3 = H.sketch(bd, H.XY, "Sk_MountHoles")
sk3.AttachmentOffset = App.Placement(Vector(0, 0, H.inch(M)), App.Rotation())
c1 = H.ccircle(sk3, x0 - BS / 2, ybar, 0.5, "HoleX1", "HoleY1", "HoleDia")
c2 = H.ccircle(sk3, x0 + BS / 2, ybar, 0.5, "HoleX2", "HoleY2", "")
sk3.addConstraint(Sketcher.Constraint("Equal", c1["geo"], c2["geo"]))
sk3.delConstraint(c2["d"])         # diameter comes from the Equal constraint
c3 = H.circle(sk3, (x0 - BS / 2, -ybar), 0.5)
c4 = H.circle(sk3, (x0 + BS / 2, -ybar), 0.5)
for src, dst in ((c1["geo"], c3), (c2["geo"], c4)):
    sk3.addConstraint(Sketcher.Constraint("Symmetric", src, 3, dst, 3, -1))
    sk3.addConstraint(Sketcher.Constraint("Equal", src, dst))
E_STATION = u"-(Params.HoleCount - 1) * Params.HolePitch / 2"
E_BARY = u"-(Params.FrameDepth - Params.MemberSize) / 2"
sk3.setExpression("Constraints.HoleX1", E_STATION + u" - Params.BoltSpacing / 2")
sk3.setExpression("Constraints.HoleX2", E_STATION + u" + Params.BoltSpacing / 2")
sk3.setExpression("Constraints.HoleY1", E_BARY)
sk3.setExpression("Constraints.HoleY2", E_BARY)
sk3.setExpression("Constraints.HoleDia", u"Params.HoleDia")
sk3.setExpression(".AttachmentOffset.Base.z", u"Params.MemberSize")
doc.recompute()
print(H.dof_text(sk3))
edit_snap(sk3, "01_frame_06_sketch_station_holes")

poc2 = H.pocket(bd, sk3, 0, through=True, name="Pocket_MountHoles")
doc.recompute()
snap("01_frame_07_pocket_first_station", "Isometric")

# =============================================================== 7  hole pattern
xaxis = H.origin_ref(bd, "X_Axis")
lp = H.linear_pattern(bd, poc2, (xaxis, [""]), (9 - 1) * 9.5, 9, name="Pattern_Holes")
lp.setExpression("Length", u"(Params.HoleCount - 1) * Params.HolePitch")
lp.setExpression("Occurrences", u"Params.HoleCount")
doc.recompute()
snap("01_frame_08_linear_pattern_holes", "Top")

# =============================================================== 8  hitch clevis
HO, HG, HT = 15.0, 1.5, 0.4          # offset from centreline, clear gap, plate thk
HR, HH = 5.0, 3.0                    # reach (fore-aft), rise (above frame underside)
y_rear = -(D / 2 - M)                # -9  : rear face of the front tool bar
y_nose = y_rear - HR                 # -14 : nose of the clevis plate

E_X0 = u"-(Params.FrameDepth / 2 - Params.MemberSize + Params.HitchReach)"
E_W  = u"Params.HitchReach"
E_H  = u"Params.HitchRise"


def clevis_plate(nm, x_face, reverse):
    """One clevis plate: sketch on the YZ plane, offset out to its own face."""
    sk = H.sketch(bd, H.YZ, "Sk_" + nm)
    sk.AttachmentOffset = App.Placement(Vector(0, 0, H.inch(x_face)), App.Rotation())
    H.crect_box(sk, y_nose, 0.0, y_rear, HH, names=("PlateY", "PlateZ", "PlateLen", "PlateRise"))
    sk.setExpression("Constraints.PlateY", E_X0)
    sk.setExpression("Constraints.PlateZ", u"0 mm")
    sk.setExpression("Constraints.PlateLen", E_W)
    sk.setExpression("Constraints.PlateRise", E_H)
    sk.setExpression(".AttachmentOffset.Base.z",
                     u"Params.HitchOffset %s Params.HitchGap / 2" % ("+" if not reverse else "-"))
    doc.recompute()
    pd = H.pad(bd, sk, HT, reversed_=reverse, name="Pad_" + nm)
    H.bind(pd, "Length", u"Params.HitchPlate")
    doc.recompute()
    return sk, pd


sk_a, pad_a = clevis_plate("ClevisInner", HO - HG / 2, True)
sk_b, pad_b = clevis_plate("ClevisOuter", HO + HG / 2, False)
print(H.dof_text(sk_a), "|", H.dof_text(sk_b))
edit_snap(sk_b, "01_frame_10_sketch_clevis_plate")
snap("01_frame_11_pad_clevis_pair", "Isometric")

# ---- lower-link pin hole, through both plates
sk_pin = H.sketch(bd, H.YZ, "Sk_HitchPin")
sk_pin.AttachmentOffset = App.Placement(Vector(0, 0, H.inch(HO)), App.Rotation())
H.ccircle(sk_pin, -(D / 2 + 1.0), HH / 2, 1.0, "PinY", "PinZ", "PinDia")
sk_pin.setExpression("Constraints.PinY", u"-(Params.FrameDepth / 2 + 1 in)")
sk_pin.setExpression("Constraints.PinZ", u"Params.HitchRise / 2")
sk_pin.setExpression("Constraints.PinDia", u"Params.PinDia")
sk_pin.setExpression(".AttachmentOffset.Base.z", u"Params.HitchOffset")
doc.recompute()
print(H.dof_text(sk_pin))
poc_pin = H.pocket(bd, sk_pin, 0, through=True, midplane=True, name="Pocket_HitchPin")
doc.recompute()
snap("01_frame_12_pocket_hitch_pin", "Isometric")

# ---- mirror the whole clevis to the other side of the machine
yz = H.origin_ref(bd, "YZ_Plane")
mir2 = H.mirrored(bd, [pad_a, pad_b, poc_pin], yz, name="Mirror_ClevisToLeft")
doc.recompute()
snap("01_frame_13_mirror_clevis", "Isometric")

# ---- round the clevis noses (all four plates at once)
# SolidWorks would use a full-round fillet across three faces; FreeCAD has no
# such option, so we round the two profile corners of each nose instead.
nose = H.edges_where(mir2, lambda e: H.is_straight_along(e, "x") and H.at_coord(e, "y", y_nose))
print("nose edges:", nose)
fil = H.fillet(bd, mir2, nose, 0.63, name="Fillet_ClevisNose")
H.bind(fil, "Radius", u"Params.CornerR")
doc.recompute()
H.color(fil, H.PAINT_RED)
snap("01_frame_14_fillet_clevis_nose", "Isometric")

# =============================================================== 9  finish
doc.recompute()
print(H.report(doc))
H.shot_set("01_frame_final", ("Isometric", "Front", "Top", "Right"))
snap("01_frame_15_complete_tree", "Isometric")
H.savedoc(doc, "01_frame")
print("SHOTS:", SHOT)
