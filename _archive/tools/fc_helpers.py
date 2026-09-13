# -*- coding: utf-8 -*-
"""Helpers for the 9-tyne cultivator build: units, screenshots, sketch utilities.

Run inside FreeCAD (GUI must be up).  Imported by every MCP execute_code call:

    import sys; sys.path.insert(0, r"C:\\Users\\ASUS\\Desktop\\freecad\\tools")
    import fc_helpers as H; H.reload_me()
"""
import os, sys, time, importlib
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

ROOT   = r"C:\Users\ASUS\Desktop\freecad"
SHOTS  = os.path.join(ROOT, "screenshots")
PARTS  = os.path.join(ROOT, "parts")
ASSETS = os.path.join(ROOT, "assets")
for d in (SHOTS, PARTS, ASSETS):
    if not os.path.isdir(d):
        os.makedirs(d)

IN = 25.4                      # inches -> FreeCAD internal mm


def inch(v):
    return v * IN


# --------------------------------------------------------------- housekeeping
def reload_me():
    importlib.reload(sys.modules[__name__])


def set_units():
    p = App.ParamGet("User parameter:BaseApp/Preferences/Units")
    p.SetInt("UserSchema", 3)          # Imperial decimal (in, lb)
    p.SetInt("Decimals", 2)            # matches the dlg_units capture; no long floats on slides
    App.Units.setSchema(3)


def pump(ms=120):
    """Let Qt repaint before grabbing a frame."""
    Gui.updateGui()
    QtWidgets.QApplication.processEvents()
    t = time.time()
    while (time.time() - t) * 1000 < ms:
        QtWidgets.QApplication.processEvents()


# --------------------------------------------------------------- screenshots
def mw():
    return Gui.getMainWindow()


def _save(pix, name):
    path = os.path.join(SHOTS, name + ".png")
    pix.save(path, "PNG")
    return path


def _front_panel():
    """Model and Tasks are tabbed on the left: show Tasks while a dialog or
    sketch is open, the Model tree otherwise - what a student would be looking at."""
    want = "Tasks" if Gui.Control.activeDialog() else "Model"
    for d in mw().findChildren(QtWidgets.QDockWidget):
        if d.windowTitle() == want:
            d.raise_()


def shot(name):
    """Full FreeCAD application window - the teaching screenshot."""
    _front_panel()
    pump()
    mw().statusBar().clearMessage()
    pump(50)
    return _save(mw().grab(), name)


def shot_widget(widget, name):
    pump()
    return _save(widget.grab(), name)


def find_dock(title_fragment):
    frag = title_fragment.lower()
    for d in mw().findChildren(QtWidgets.QDockWidget):
        if frag in d.windowTitle().lower():
            return d
    return None


def shot_dock(title_fragment, name):
    d = find_dock(title_fragment)
    if d is None:
        return "dock not found: " + title_fragment
    return shot_widget(d, name)


def find_toolbar(name_fragment):
    frag = name_fragment.lower()
    for t in mw().findChildren(QtWidgets.QToolBar):
        if frag in (t.windowTitle() or "").lower() and t.isVisible():
            return t
    return None


def shot_toolbar(name_fragment, name):
    t = find_toolbar(name_fragment)
    if t is None:
        return "toolbar not found: " + name_fragment
    return shot_widget(t, name)


def view(orient="Isometric", fit=True):
    v = Gui.ActiveDocument.ActiveView
    if orient == "Isometric":
        v.viewIsometric()
    else:
        getattr(v, "view" + orient)()
    if fit:
        Gui.SendMsgToActiveView("ViewFit")
        fit_tight()
    pump()


def fit_tight(margin=1.12):
    """Fit All sizes the view to the model's bounding *sphere*, so a thin part
    seen side-on (a 13 in blade from the Right) is a sliver in empty space.
    Project the visible solids' box corners onto the screen axes instead."""
    try:
        from pivy import coin
        doc = App.ActiveDocument
        shapes = []
        for o in doc.Objects:
            vo = getattr(o, "ViewObject", None)
            if vo is None or not vo.Visibility:
                continue
            if o.TypeId in ("PartDesign::Body", "App::Link") or (
                    o.isDerivedFrom("Part::Feature") and o.getParentGeoFeatureGroup() is None
                    and not o.isDerivedFrom("Sketcher::SketchObject")):
                try:
                    s = Part.getShape(o)
                    if not s.isNull() and s.BoundBox.isValid():
                        shapes.append(s)
                except Exception:
                    pass
        if not shapes:
            return
        v = Gui.ActiveDocument.ActiveView
        cam = v.getCameraNode()
        if cam.getTypeId().getName() != "OrthographicCamera":
            return
        rot = cam.orientation.getValue()
        right = rot.multVec(coin.SbVec3f(1, 0, 0)).getValue()
        up = rot.multVec(coin.SbVec3f(0, 1, 0)).getValue()
        look = rot.multVec(coin.SbVec3f(0, 0, -1)).getValue()
        us, ws = [], []
        for s in shapes:
            bb = s.BoundBox
            for x in (bb.XMin, bb.XMax):
                for y in (bb.YMin, bb.YMax):
                    for z in (bb.ZMin, bb.ZMax):
                        us.append(x * right[0] + y * right[1] + z * right[2])
                        ws.append(x * up[0] + y * up[1] + z * up[2])
        uc, wc = (min(us) + max(us)) / 2.0, (min(ws) + max(ws)) / 2.0
        bw, bh = max(us) - min(us), max(ws) - min(ws)
        w_px, h_px = v.getSize()
        aspect = float(w_px) / float(h_px)
        # keep the camera's depth, move it across the screen plane to the centre
        p = cam.position.getValue().getValue()
        du = uc - (p[0] * right[0] + p[1] * right[1] + p[2] * right[2])
        dw = wc - (p[0] * up[0] + p[1] * up[1] + p[2] * up[2])
        cam.position.setValue(p[0] + du * right[0] + dw * up[0],
                              p[1] + du * right[1] + dw * up[1],
                              p[2] + du * right[2] + dw * up[2])
        cam.height.setValue(max(bh, bw / aspect, 1.0) * margin)
    except Exception as e:                      # never let framing break a build
        App.Console.PrintWarning("fit_tight: %s\n" % e)


# Dimension-label placement per sketch, so no two labels overlap on a slide.
# name -> (distance from the measured geometry, in; shift along the dimension
# line, in).  A ("rad", a) shift is an angle, used by radius/diameter labels.
# Found by trial in the Sketcher; the sign conventions are FreeCAD's own.
LABELS = {
    "Frame/Sk_FramePlan":   {"FrameLength": (-4, 0), "InnerLength": (4, 0),
                             "FrameDepth": (-7, 0), "InnerDepth": (12, 0)},
    "Frame/Sk_MountHoles":  {"HoleX1": (3, 0), "HoleX2": (-3, -9), "HoleY1": (-3, 0),
                             "HoleY2": (16, 0), "HoleDia": (11, ("rad", 0.5))},
    "Frame/Sk_ClevisOuter": {"PlateLen": (-1.5, 0), "PlateRise": (-1.5, 0),
                             "PlateY": (-4.5, 0), "PlateZ": (-2, 0)},
    "Tine01/Sk_TineProfile": {"ShankWidth": (2.5, 4), "BendRadius": (-3, ("rad", -0.3)),
                              "Rake": (7, ("rad", 0)), "FootLength": (-5, 3)},
    "Tine01/Sk_BoltHoles":   {"BoltX": (0.8, 0), "BoltY": (1.0, 0), "BoltDia": (0.6, ("rad", 0.8))},
    "Tine02/Sk_BoltHoles":   {"BoltX": (0.8, 0), "BoltY": (1.0, 0), "BoltDia": (0.6, ("rad", 0.8))},
    "Tine02/Sk_TineProfile": {"BarWidth": (2, -2), "TopStraight": (2, 0),
                              "CurveRadius": (-6, ("rad", -0.6)), "WorkHeight": (4, 0)},
    "Clamp01/Sk_Path":       {"Rise": (-2.5, 0), "ArmLength": (-2, 0), "ArmAngle": (5, 0),
                              "Return": (2, 0), "CornerR3": (1.5, ("rad", 0)),
                              "CornerR5": (2, ("rad", 3.6))},
    "Clamp01/Sk_Section":    {"StrapThk": (-0.4, 0)},
    "Clamp02/Sk_Path":       {"Rise": (-2.5, 0), "TipLength": (3, 0), "TipAngle": (4, 0),
                              "CornerR2": (3, ("rad", -0.2))},
    "Clamp02/Sk_Section":    {"StrapThk": (-0.4, 0)},
    # BladeLength is an arc-length constraint; FreeCAD 1.1.3 draws no label for
    # those (its value shows in the constraint list), so it needs no placement.
    "Blade/Sk_Spine":        {"BendRadius": (-0.8, ("rad", -1.45))},
    "Blade/Sk_Section":      {"Sheet": (-1.5, 0)},
    "Blade/Sk_PlanShape":    {"TipOffset": (2, 0), "HalfSpan": (1.5, -1), "EdgeAngle": (1.0, 0),
                              "TrailOffset": (11.5, 0), "StockL": (21.5, 0)},
}


def place_labels(sk):
    """Keyed "<document name>/<sketch name>" - sketch names repeat across parts."""
    table = LABELS.get("%s/%s" % (sk.Document.Name, sk.Name), {})
    for i, c in enumerate(sk.Constraints):
        if c.Name in table:
            d, p = table[c.Name]
            sk.setLabelDistance(i, inch(d))
            sk.setLabelPosition(i, p[1] if isinstance(p, tuple) else inch(p))


def fit_sketch(sk, margin=1.45):
    """Frame the camera on the sketch being edited, not on the whole body.

    Fit All in the Sketcher fits every visible solid and the sketch axes too,
    so a 5 in plate sketch on an 82 in frame ends up a speck with its labels
    piled up. Instead: bounding box of the sketch edges plus its origin (the
    location dimensions run to the origin), in sketch coordinates, and point
    the orthographic camera straight at it.
    """
    place_labels(sk)
    # The Sketcher animates the camera to face the sketch; with animation on,
    # the animation finishes after (and overrides) the camera set below.
    App.ParamGet("User parameter:BaseApp/Preferences/View").SetBool("UseNavigationAnimations", False)
    gpl = sk.getGlobalPlacement()
    inv = gpl.inverse()
    pts = [inv.multVec(v.Point) for v in sk.Shape.Vertexes]
    for e in sk.Shape.Edges:                       # arcs bulge past their ends
        pts += [inv.multVec(p) for p in e.discretize(12)]
    pts.append(Vector(0, 0, 0))
    xs, ys = [p.x for p in pts], [p.y for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    v = Gui.ActiveDocument.ActiveView
    w_px, h_px = v.getSize()
    aspect = float(w_px) / float(h_px)
    centre = gpl.multVec(Vector(cx, cy, 0))
    look = gpl.Rotation.multVec(Vector(0, 0, -1))  # camera looks down the sketch normal
    cam = v.getCameraNode()
    dist = 5000.0
    cam.position.setValue(centre.x - look.x * dist, centre.y - look.y * dist,
                          centre.z - look.z * dist)
    cam.focalDistance.setValue(dist)
    cam.height.setValue(max(bh, bw / aspect, 25.4) * margin)
    pump(250)


def shot3d(name, orient="Isometric", w=1400, h=1050, fit=True):
    """3D viewport only, at a fixed resolution - the plate images for decks."""
    view(orient, fit)
    path = os.path.join(SHOTS, name + ".png")
    Gui.ActiveDocument.ActiveView.saveImage(path, w, h, "Current")
    return path


def shot_set(prefix, orients=("Isometric", "Front", "Right", "Top"), w=1400, h=1050):
    return [shot3d("%s_%s" % (prefix, o), o, w, h) for o in orients]


# --------------------------------------------------------------- doc / body
def newdoc(name):
    if name in App.listDocuments():
        App.closeDocument(name)
    d = App.newDocument(name)
    App.setActiveDocument(name)
    return d


def savedoc(doc, fname=None):
    path = os.path.join(PARTS, (fname or doc.Name) + ".FCStd")
    doc.recompute()
    doc.saveAs(path)
    return path


def body(doc, name="Body"):
    b = doc.addObject("PartDesign::Body", name)
    doc.recompute()
    Gui.activeDocument().ActiveView.setActiveObject("pdbody", b)
    return b


def activate(b):
    Gui.activeDocument().ActiveView.setActiveObject("pdbody", b)


# --------------------------------------------------------------- sketch utils
import Part, Sketcher
from FreeCAD import Vector

XY, XZ, YZ = "XY_Plane", "XZ_Plane", "YZ_Plane"


def sketch(bdy, plane=XZ, name="Sketch"):
    doc = bdy.Document
    sk = doc.addObject("Sketcher::SketchObject", name)
    bdy.addObject(sk)
    sk.AttachmentSupport = [(doc.getObject(plane), "")]
    sk.MapMode = "FlatFace"
    doc.recompute()
    return sk


def poly(sk, pts, close=True, construction=False):
    """Add a polyline through pts (inches, 2-tuples). Returns the line indices."""
    idx = []
    n = len(pts)
    last = n if close else n - 1
    for i in range(last):
        a = pts[i]
        b = pts[(i + 1) % n]
        g = sk.addGeometry(Part.LineSegment(Vector(inch(a[0]), inch(a[1]), 0),
                                            Vector(inch(b[0]), inch(b[1]), 0)),
                           construction)
        idx.append(g)
    for k in range(len(idx) - 1):
        sk.addConstraint(Sketcher.Constraint("Coincident", idx[k], 2, idx[k + 1], 1))
    if close and len(idx) > 1:
        sk.addConstraint(Sketcher.Constraint("Coincident", idx[-1], 2, idx[0], 1))
    return idx


def circle(sk, c, dia, construction=False):
    return sk.addGeometry(Part.Circle(Vector(inch(c[0]), inch(c[1]), 0),
                                      Vector(0, 0, 1), inch(dia) / 2.0), construction)


def rect(sk, cx, cy, w, h, construction=False):
    """Axis-aligned rectangle centred on (cx, cy). All values in inches."""
    x0, x1 = cx - w / 2.0, cx + w / 2.0
    y0, y1 = cy - h / 2.0, cy + h / 2.0
    return poly(sk, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                construction=construction)


def status(sk):
    """Constraint state, as the Sketcher status bar reports it."""
    dof = sk.solve()
    return "geometry=%d constraints=%d solve=%d" % (
        len(sk.Geometry), len(sk.Constraints), dof)


# --------------------------------------------------------------- features
def pad(bdy, sk, length, midplane=False, reversed_=False, name="Pad"):
    doc = bdy.Document
    f = doc.addObject("PartDesign::Pad", name)
    bdy.addObject(f)
    f.Profile = sk
    f.Length = inch(length)
    f.Midplane = midplane
    f.Reversed = reversed_
    doc.recompute()
    return f


def pocket(bdy, sk, length, through=False, midplane=False, reversed_=False, name="Pocket"):
    doc = bdy.Document
    f = doc.addObject("PartDesign::Pocket", name)
    bdy.addObject(f)
    f.Profile = sk
    if through:
        f.Type = 1                 # ThroughAll
    else:
        f.Length = inch(length)
    f.Midplane = midplane
    f.Reversed = reversed_
    doc.recompute()
    return f


def fillet(bdy, base_feature, edge_names, radius, name="Fillet"):
    doc = bdy.Document
    f = doc.addObject("PartDesign::Fillet", name)
    bdy.addObject(f)
    f.Base = (base_feature, edge_names)
    f.Radius = inch(radius)
    doc.recompute()
    return f


def color(obj, rgb, transparency=0):
    try:
        obj.ViewObject.ShapeColor = rgb
        obj.ViewObject.Transparency = transparency
    except Exception:
        pass


STEEL      = (0.62, 0.65, 0.70)
STEEL_DARK = (0.38, 0.41, 0.46)
PAINT_RED  = (0.72, 0.16, 0.14)
PAINT_BLUE = (0.16, 0.32, 0.62)
SHARE      = (0.80, 0.80, 0.84)


def report(doc):
    out = []
    for o in doc.Objects:
        sh = getattr(o, "Shape", None)
        if sh is not None and not sh.isNull() and sh.Volume > 1e-6:
            out.append("%-22s %-26s vol=%9.2f in3  bbox=%.2f x %.2f x %.2f in" % (
                o.Name, o.TypeId.split("::")[-1], sh.Volume / IN ** 3,
                sh.BoundBox.XLength / IN, sh.BoundBox.YLength / IN,
                sh.BoundBox.ZLength / IN))
    return "\n".join(out)


# ------------------------------------------------- fully-constrained sketching
def _name(sk, cidx, nm):
    if nm:
        sk.renameConstraint(cidx, nm)
    return cidx


def crect_centred(sk, w, h, wname="", hname="", cx=0.0, cy=0.0):
    """Rectangle centred on the origin, FULLY constrained.

    Returns dict with the line ids and the two dimension constraint indices.
    """
    ls = rect(sk, cx, cy, w, h)
    sk.addConstraint(Sketcher.Constraint("Horizontal", ls[0]))
    sk.addConstraint(Sketcher.Constraint("Horizontal", ls[2]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ls[1]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ls[3]))
    # bottom-left and top-right symmetric about the sketch origin -> centres it
    sk.addConstraint(Sketcher.Constraint("Symmetric", ls[0], 1, ls[2], 1, -1, 1))
    cw = sk.addConstraint(Sketcher.Constraint("DistanceX", ls[0], 1, ls[0], 2, inch(w)))
    ch = sk.addConstraint(Sketcher.Constraint("DistanceY", ls[1], 1, ls[1], 2, inch(h)))
    _name(sk, cw, wname)
    _name(sk, ch, hname)
    return dict(lines=ls, w=cw, h=ch)


def ccircle(sk, cx, cy, dia, xname="", yname="", dname=""):
    """Circle located from the sketch origin, FULLY constrained."""
    g = circle(sk, (cx, cy), dia)
    cx_ = sk.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, g, 3, inch(cx)))
    cy_ = sk.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, g, 3, inch(cy)))
    cd = sk.addConstraint(Sketcher.Constraint("Diameter", g, inch(dia)))
    _name(sk, cx_, xname)
    _name(sk, cy_, yname)
    _name(sk, cd, dname)
    return dict(geo=g, x=cx_, y=cy_, d=cd)


def constrained(sk):
    sk.Document.recompute()
    return bool(getattr(sk, "FullyConstrained", False))


def dof_text(sk):
    sk.Document.recompute()
    ok = constrained(sk)
    return "%s : %d geometry, %d constraints, %s" % (
        sk.Name, len(sk.Geometry), len(sk.Constraints),
        "FULLY CONSTRAINED" if ok else "under-constrained")


# ------------------------------------------------------------------ spreadsheet
def params_sheet(doc, rows, name="Params", title="Parameters"):
    """rows = [(alias, value_string, description), ...] -> Spreadsheet object."""
    sh = doc.addObject("Spreadsheet::Sheet", name)
    sh.Label = title
    sh.set("A1", "Parameter")
    sh.set("B1", "Value")
    sh.set("C1", "Meaning")
    for i, (alias, val, desc) in enumerate(rows):
        r = i + 2
        sh.set("A%d" % r, alias)
        sh.set("B%d" % r, str(val))
        sh.set("C%d" % r, desc)
        sh.setAlias("B%d" % r, alias)
    sh.setStyle("A1:C1", "bold")
    # wide enough that every name and description reads in full on a slide
    sh.setColumnWidth("A", 150)
    sh.setColumnWidth("B", 120)
    sh.setColumnWidth("C", 420)
    doc.recompute()
    return sh


def shot_sheet(sheet, name, zoom=130):
    """The parameter table open in its own tab - what a student actually looks
    at while typing values in. (A grab of the 3D view at this point shows an
    empty viewport; the sheet is only a line in the tree.)"""
    doc = sheet.Document
    Gui.getDocument(doc.Name).setEdit(sheet)
    pump(500)
    mdi = mw().findChild(QtWidgets.QMdiArea)
    sub = mdi.activeSubWindow()
    w = sub.widget()
    s = w.findChild(QtWidgets.QSlider, "zoomSlider")
    if s is not None:
        s.setValue(zoom)
    for tv in QtWidgets.QApplication.allWidgets():
        if isinstance(tv, QtWidgets.QTableView) and tv.objectName() == "cells" and tv.isVisible():
            tv.selectionModel().setCurrentIndex(tv.model().index(0, 0),
                                                QtCore.QItemSelectionModel.ClearAndSelect)
    pump(300)
    path = shot(name)
    sub.close()
    pump(300)
    return path


def bind(obj, path, expr):
    """Attach a spreadsheet expression, e.g. bind(pad,'Length','Params.MemberSize')."""
    obj.setExpression(path, expr)
    obj.Document.recompute()


# ------------------------------------------------------- transformation features
def append_tip(bdy, f):
    """Put a new solid feature at the end of the Body's feature chain."""
    prev = bdy.Tip
    bdy.addObject(f)
    if hasattr(f, "BaseFeature") and prev is not None and f.BaseFeature is None:
        f.BaseFeature = prev
    bdy.Tip = f
    return f


def linear_pattern(bdy, features, direction, length, occurrences, name="LinearPattern",
                   reverse=False):
    doc = bdy.Document
    f = doc.addObject("PartDesign::LinearPattern", name)
    append_tip(bdy, f)
    f.TransformMode = "Features"
    f.Originals = features if isinstance(features, list) else [features]
    f.Direction = direction
    f.Mode = "Extent"
    f.Length = inch(length)
    f.Occurrences = occurrences
    f.Reversed = reverse
    doc.recompute()
    return f


def mirrored(bdy, features, plane, name="Mirrored", whole=False):
    doc = bdy.Document
    f = doc.addObject("PartDesign::Mirrored", name)
    append_tip(bdy, f)
    if whole:
        f.TransformMode = "Whole shape"
    else:
        f.TransformMode = "Features"
        f.Originals = features if isinstance(features, list) else [features]
    f.MirrorPlane = plane
    doc.recompute()
    return f


def origin_ref(bdy, which):
    """which in {X_Axis, Y_Axis, Z_Axis, XY_Plane, XZ_Plane, YZ_Plane}."""
    for o in bdy.Origin.OriginFeatures:
        if o.Name.startswith(which) or o.Name == which:
            return o
    return bdy.Document.getObject(which)


# ---------------------------------------------------------- more sketch tools
def crect_box(sk, u0, v0, u1, v1, names=("X0", "Y0", "W", "H")):
    """Rectangle by its two opposite corners, located from the sketch origin.

    Fully constrained: 2 horizontals, 2 verticals, corner position, width, height.
    """
    ls = poly(sk, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    sk.addConstraint(Sketcher.Constraint("Horizontal", ls[0]))
    sk.addConstraint(Sketcher.Constraint("Horizontal", ls[2]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ls[1]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ls[3]))
    cx = sk.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, ls[0], 1, inch(u0)))
    cy = sk.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, ls[0], 1, inch(v0)))
    cw = sk.addConstraint(Sketcher.Constraint("DistanceX", ls[0], 1, ls[0], 2, inch(u1 - u0)))
    ch = sk.addConstraint(Sketcher.Constraint("DistanceY", ls[1], 1, ls[1], 2, inch(v1 - v0)))
    for c, nm in zip((cx, cy, cw, ch), names):
        _name(sk, c, nm)
    return dict(lines=ls, x=cx, y=cy, w=cw, h=ch)


def edges_where(feature, pred):
    """Edge names ('Edge7', ...) of feature.Shape satisfying pred(edge)."""
    return ["Edge%d" % (i + 1) for i, e in enumerate(feature.Shape.Edges) if pred(e)]


def is_straight_along(e, axis, tol=1e-6):
    """True if e is a straight edge parallel to axis ('x' | 'y' | 'z')."""
    if not isinstance(e.Curve, Part.Line):
        return False
    a, b = e.Vertexes[0].Point, e.Vertexes[-1].Point
    d = b.sub(a)
    comp = {"x": (d.x, d.y, d.z), "y": (d.y, d.x, d.z), "z": (d.z, d.x, d.y)}[axis]
    return abs(comp[0]) > tol and abs(comp[1]) < tol and abs(comp[2]) < tol


def at_coord(e, axis, value, tol=1e-4):
    """True if every vertex of e sits at the given coordinate (inches)."""
    v = inch(value)
    return all(abs(getattr(p.Point, axis) - v) < tol for p in e.Vertexes)


def weld(sk, tol=1e-4):
    """Coincident-constrain every pair of geometry endpoints that already touch.

    Lets a profile be drawn as independent lines and arcs in any direction and
    still close up cleanly, without hand-tracking start/end point ids.
    """
    pts = []
    for gi, g in enumerate(sk.Geometry):
        if g.isDerivedFrom("Part::GeomCircle"):
            continue
        for pos in (1, 2):
            try:
                pts.append((gi, pos, sk.getPoint(gi, pos)))
            except Exception:
                pass
    used = constrained_points(sk)
    made = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            gi, pi, a = pts[i]
            gj, pj, b = pts[j]
            if gi == gj or (gi, pi) in used or (gj, pj) in used:
                continue
            if a.distanceToPoint(b) < tol:
                sk.addConstraint(Sketcher.Constraint("Coincident", gi, pi, gj, pj))
                used.add((gi, pi))
                used.add((gj, pj))
                made += 1
    return made


def constrained_points(sk):
    """Endpoints already tied down by a coincident or endpoint-tangent constraint."""
    out = set()
    for c in sk.Constraints:
        if c.Type in ("Coincident", "Tangent") and c.FirstPos in (1, 2) and c.SecondPos in (1, 2):
            out.add((c.First, c.FirstPos))
            out.add((c.Second, c.SecondPos))
    return out


def tangent_join(sk, ga, gb, tol=1e-4):
    """Endpoint-to-endpoint tangency between two touching curves.

    This is the constraint FreeCAD wants at a smooth join: it carries the
    coincidence with it, so adding a separate Coincident there conflicts.
    """
    best = None
    for pa in (1, 2):
        for pb in (1, 2):
            try:
                dist = sk.getPoint(ga, pa).distanceToPoint(sk.getPoint(gb, pb))
            except Exception:
                continue
            if best is None or dist < best[0]:
                best = (dist, pa, pb)
    if best is None or best[0] > tol:
        return False
    sk.addConstraint(Sketcher.Constraint("Tangent", ga, best[1], gb, best[2]))
    return True


def hide_sketches(doc):
    """Hide every sketch, datum and origin so a final render shows solids only."""
    for o in doc.Objects:
        if (o.isDerivedFrom("Sketcher::SketchObject")
                or o.isDerivedFrom("Part::Datum")
                or o.isDerivedFrom("App::Origin")
                or o.TypeId in ("App::Line", "App::Plane", "App::Placement")):
            try:
                o.ViewObject.Visibility = False
            except Exception:
                pass
    pump()
