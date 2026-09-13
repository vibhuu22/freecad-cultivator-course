# -*- coding: utf-8 -*-
"""The assembly - 9 tynes on an 82 in frame.

Layout:
  front tool bar (y = -10)  5 x Tine 01 at 19 in pitch, x = -38 .. +38
  rear  tool bar (y = +10)  4 x Tine 02 at 19 in pitch, staggered 9.5 in
  -> 9 tynes at an effective 9.5 in working spacing across a 76 in swath

SolidWorks would use a Linear Component Pattern here.  The Assembly workbench
has no direct equivalent, but FreeCAD does: an **App::Link array**.  One link
object carries a PlacementList, so five tynes cost one object in the tree and
one row of numbers - and the pitch is still a single value to edit.
"""
import sys, os, math
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Vector, Rotation, Placement

H.set_units()
SHOT = []


def snap(name, orient=None):
    if orient:
        H.view(orient)
    H.shot(name)
    SHOT.append(name)


# ------------------------------------------------------------------- geometry
PITCH   = 19.0        # tyne pitch along one bar
STAGGER = 9.5         # rear rank offset
BAR_Y   = 10.0        # tool bar centrelines at y = -10 and +10
FRONT_X = [-38.0, -19.0, 0.0, 19.0, 38.0]
REAR_X  = [-28.5, -9.5, 9.5, 28.5]

# Tine 01 point, in tyne coordinates (from build_tine01)
T1_TIP = (-4.528, -23.713)
# Tine 02 point (mid of the tip face), from build_tine02
T2_TIP = (-10.433, -17.000)

PARTS = [("01_frame",   "Frame"),
         ("02_tine01",  "Tine01"),
         ("03_tine02",  "Tine02"),
         ("04_clamp01", "Clamp01"),
         ("05_clamp02", "Clamp02"),
         ("06_blade01", "Blade"),
         ("07_blade02", "Blade")]

# --------------------------------------------------------------- open sources
srcs = {}
for fname, bodyname in PARTS:
    path = os.path.join(H.PARTS, fname + ".FCStd")
    d = App.listDocuments().get(fname) or App.openDocument(path)
    srcs[fname] = (d, d.getObject(bodyname))
    print("opened", fname, "->", d.Name, bodyname)

doc = H.newdoc("Cultivator")
# An App::Link that points into another document needs its owner saved first
doc.saveAs(os.path.join(H.PARTS, "08_cultivator_assembly.FCStd"))
Gui.activateWorkbench("AssemblyWorkbench")
H.pump(400)
snap("08_asm_00_empty_assembly")


def link(name, fname, placements, color=None):
    d, body = srcs[fname]
    lnk = doc.addObject("App::Link", name)
    lnk.LinkedObject = body
    lnk.Label = name
    if len(placements) > 1:
        # A link array's PlacementList is relative to the link's own Placement,
        # so the array itself must stay at the origin.
        lnk.ElementCount = len(placements)
        lnk.ShowElement = False
        lnk.PlacementList = placements
    else:
        lnk.Placement = placements[0]
    if color:
        try:
            lnk.ViewObject.OverrideMaterial = True
            lnk.ViewObject.ShapeMaterial.DiffuseColor = color
        except Exception:
            try:
                lnk.ViewObject.ShapeColor = color
            except Exception:
                pass
    doc.recompute()
    return lnk


def P(x, y, z, yaw=0.0):
    return Placement(Vector(H.inch(x), H.inch(y), H.inch(z)), Rotation(yaw, 0, 0))


# ------------------------------------------------------------------ the frame
l_frame = link("Frame", "01_frame", [P(0, 0, 0)], H.PAINT_RED)
doc.recompute()
snap("08_asm_01_frame_placed", "Isometric")

# ------------------------------------------------------- front rank, 5 tynes
l_t1 = link("Tine01_x5", "02_tine01", [P(x, -BAR_Y, 0) for x in FRONT_X], H.STEEL_DARK)
doc.recompute()
snap("08_asm_02_front_rank", "Isometric")

# -------------------------------------------------------- rear rank, 4 tynes
l_t2 = link("Tine02_x4", "03_tine02", [P(x, BAR_Y, 0) for x in REAR_X], H.STEEL_DARK)
doc.recompute()
snap("08_asm_03_rear_rank", "Isometric")
snap("08_asm_04_rank_stagger", "Top")

# ----------------------------------------------------------------- the blades
b1 = [P(x, -BAR_Y + T1_TIP[0] + 1.0, T1_TIP[1] - 0.1) for x in FRONT_X]
l_b1 = link("Blade01_x5", "06_blade01", b1, H.SHARE)
b2 = [P(x, BAR_Y + T2_TIP[0] + 1.0, T2_TIP[1] - 0.1) for x in REAR_X]
l_b2 = link("Blade02_x4", "07_blade02", b2, H.SHARE)
doc.recompute()
snap("08_asm_05_blades", "Isometric")

# ------------------------------------------------------------------ the mast
l_c1 = link("Clamp01_x2", "04_clamp01", [P(-10, BAR_Y, 2), P(10, BAR_Y, 2)], H.PAINT_RED)
l_c2 = link("Clamp02_x2", "05_clamp02", [P(-25, BAR_Y, 2), P(25, BAR_Y, 2)], H.PAINT_RED)
doc.recompute()
snap("08_asm_06_braces", "Isometric")

# ------------------------------------------------------------------- finish
doc.recompute()
tot = 0.0
for o in doc.Objects:
    if o.isDerivedFrom("App::Link"):
        n = max(1, o.ElementCount)
        v = o.LinkedObject.Shape.Volume / H.IN ** 3
        tot += v * n
        print("%-14s x%d  %7.2f in3 each" % (o.Label, n, v))
print("total steel %.1f in3 = %.0f lb" % (tot, tot * 0.284))

Gui.Selection.clearSelection()
H.shot_set("08_asm_hero", ("Isometric", "Front", "Right", "Top"), w=2000, h=1300)
snap("08_asm_07_complete", "Isometric")
H.savedoc(doc, "08_cultivator_assembly")
print("SHOTS:", SHOT)
