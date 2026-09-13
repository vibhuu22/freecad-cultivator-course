# -*- coding: utf-8 -*-
"""Section 4 - dimensioned TechDraw sheets for the frame, both tynes and the blade.

Each sheet is a TechDraw page saved inside the part's own .FCStd (so students
can open it next to the model), then exported to assets/dwg_*.png through SVG.

Every dimension references real view geometry: a model-space point is projected
into the view and the nearest visible vertex/edge is used. The script prints how
far each pick landed from the point asked for, so a wrong pick is obvious.

Run inside FreeCAD after the build scripts (their documents open).
"""
import sys, os, math, time
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\_archive\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H

import FreeCAD as App
import FreeCADGui as Gui
import TechDrawGui
from FreeCAD import Vector
from PySide import QtGui

IN = 25.4
TEMPLATE = os.path.join(App.getResourceDir(), "Mod", "TechDraw", "Templates", "ASME",
                        "ANSIB_Landscape.svg")
TMP = os.environ.get("TEMP", H.ASSETS)
LOG = []


def log(*a):
    LOG.append(" ".join(str(x) for x in a))


# --------------------------------------------------------------------- sheet
class Sheet:
    def __init__(self, doc, name, title, subtitle, scale_text, number):
        old = doc.getObject(name)
        if old is not None:                      # rebuilding: start clean
            # names first: removing a view also removes its dimensions
            names = [o.Name for o in old.Views]
            names += [old.Template.Name] if old.Template is not None else []
            names.append(old.Name)
            for n in names:
                if doc.getObject(n) is not None:
                    doc.removeObject(n)
            doc.recompute()
        self.doc = doc
        self.page = doc.addObject("TechDraw::DrawPage", name)
        tpl = doc.addObject("TechDraw::DrawSVGTemplate", name + "_Template")
        tpl.Template = TEMPLATE
        self.page.Template = tpl
        texts = tpl.EditableTexts
        texts.update({
            "CompanyName": "Design of Farm Machinery",
            "CompanyAddress": "9-tyne cultivator - FreeCAD 1.1 course",
            "DrawingTitle1": title, "DrawingTitle2": subtitle, "DrawingTitle3": "",
            "DrawnBy": "", "CheckedBy": "", "Approved1": "", "Approved2": "",
            "Code": "", "Weight": "", "drawing_number": number, "revision_index": "A",
            "scale": scale_text, "Sheet": "1 / 1"})
        tpl.EditableTexts = texts
        self.views = {}

    def view(self, key, body, direction, xdir, x, y, scale):
        v = self.doc.addObject("TechDraw::DrawViewPart", self.page.Name + "_" + key)
        self.page.addView(v)
        v.Source = [body]
        v.Direction = direction
        v.XDirection = xdir
        v.ScaleType = "Custom"
        v.Scale = scale
        v.X, v.Y = x, y
        self.doc.recompute()
        wait(v)
        pv = PView(v, body, direction, xdir, scale)
        self.views[key] = pv
        return pv

    def note(self, text_lines, x, y, size=5.0):
        a = self.doc.addObject("TechDraw::DrawViewAnnotation", self.page.Name + "_Note")
        self.page.addView(a)
        a.Text = text_lines
        a.TextSize = size
        a.X, a.Y = x, y
        return a

    def export(self, png, width=2400):
        self.doc.recompute()
        H.pump(500)
        # the page needs an open GUI view to export; double-click opens it with
        # its template (setEdit alone exported the views without the sheet)
        self.page.ViewObject.doubleClicked()
        H.pump(2000)
        svg = os.path.join(TMP, self.page.Name + ".svg")
        TechDrawGui.exportPageAsSvg(self.page, svg)
        from PySide import QtSvg
        r = QtSvg.QSvgRenderer(svg)
        h = int(width * 279.4 / 431.8)
        img = QtGui.QImage(width, h, QtGui.QImage.Format_RGB32)
        img.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(img)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setRenderHint(QtGui.QPainter.TextAntialiasing)
        r.render(p)
        p.end()
        img.save(png)
        mdi = H.mw().findChild(QtGui.QMdiArea) if hasattr(QtGui, "QMdiArea") else None
        from PySide import QtWidgets
        sub = H.mw().findChild(QtWidgets.QMdiArea).activeSubWindow()
        if sub is not None and self.page.Label in sub.windowTitle():
            sub.close()
        H.pump(300)
        log("exported", png)
        return png


def wait(v, timeout=60):
    t0 = time.time()
    while time.time() - t0 < timeout:
        H.pump(150)
        if v.getVisibleEdges():
            return
    raise RuntimeError("no geometry for view " + v.Name)


# ---------------------------------------------------------------------- view
class PView:
    """A projected view plus model -> view coordinate mapping (scaled, y up)."""

    def __init__(self, v, body, direction, xdir, scale):
        self.v, self.s = v, scale
        self.d = Vector(direction).normalize()
        self.xd = Vector(xdir).normalize()
        self.yd = self.d.cross(self.xd).normalize()
        pts = []
        sh = body.Shape
        for e in sh.Edges:
            pts += e.discretize(24)
        us = [p.dot(self.xd) for p in pts]
        ws = [p.dot(self.yd) for p in pts]
        self.cu = (min(us) + max(us)) / 2.0
        self.cw = (min(ws) + max(ws)) / 2.0

    def P(self, x, y, z):
        """model point (inches) -> view point (page mm, relative to view centre,
        y up). This is the system dimension label positions use."""
        p = Vector(x * IN, y * IN, z * IN)
        return Vector((p.dot(self.xd) - self.cu) * self.s, (p.dot(self.yd) - self.cw) * self.s, 0)

    def G(self, x, y, z):
        """Same point in the view's *geometry* system - getVisibleVertexes()
        and getVisibleEdges() have y pointing down."""
        p = self.P(x, y, z)
        return Vector(p.x, -p.y, 0)

    def U(self, x, y, z):
        """Same point for *creating* cosmetic geometry: unscaled, y up.
        TechDraw scales and flips it on display (checked: a vertex stored at
        (-63.5, 52.92) shows at (-10.58, -8.82) in a 1:6 view)."""
        p = self.P(x, y, z)
        return Vector(p.x / self.s, p.y / self.s, 0)

    def vertex(self, x, y, z, tol=1.5):
        target = self.G(x, y, z)
        vs = self.v.getVisibleVertexes()
        i, d = min(((i, (p - target).Length) for i, p in enumerate(vs)), key=lambda t: t[1])
        log("   vertex near (%g,%g,%g) -> Vertex%d  off %.2f mm%s" % (x, y, z, i, d, "  <-- CHECK" if d > tol else ""))
        return "Vertex%d" % i

    def edge(self, kind, x, y, z, radius=None, tol=2.0):
        """kind 'circle' (x,y,z = centre) or 'line' (x,y,z = a point on it)"""
        target = self.G(x, y, z)
        best = None
        for i, e in enumerate(self.v.getVisibleEdges()):
            t = e.Curve.TypeId
            if kind == "circle" and t == "Part::GeomCircle":
                d = (e.Curve.Center - target).Length
                if radius is not None:
                    d += abs(e.Curve.Radius - radius * IN * self.s) * 4
            elif kind == "line" and t == "Part::GeomLine":
                d = e.distToShape(__import__("Part").Vertex(target))[0]
            else:
                continue
            if best is None or d < best[1]:
                best = (i, d)
        log("   %s near (%g,%g,%g) -> Edge%d  off %.2f mm%s" % (kind, x, y, z, best[0], best[1], "  <-- CHECK" if best[1] > tol else ""))
        return "Edge%d" % best[0]


def dim(sheet, pv, typ, refs, lx, ly, lz, fmt=None):
    """Dimension on references, label placed at model point (lx, ly, lz)."""
    d = sheet.doc.addObject("TechDraw::DrawViewDimension", sheet.page.Name + "_Dim")
    d.Type = typ
    d.MeasureType = "Projected"
    d.References2D = [(pv.v, refs)]
    sheet.page.addView(d)
    if fmt:
        d.FormatSpec = fmt
    p = pv.P(lx, ly, lz)
    d.X, d.Y = p.x, p.y
    try:
        d.ViewObject.Fontsize = 5.0
        d.ViewObject.Arrowsize = 3.5
    except Exception:
        pass
    sheet.doc.recompute()
    try:
        val = d.getRawValue()
        log("  %-9s %-28s = %s" % (typ, ",".join(refs), ("%.3f in" % (val / IN)) if not typ.startswith("Angle") else ("%.2f deg" % val)))
    except Exception as e:
        log("  %-9s %s  (value? %s)" % (typ, refs, e))
    return d


TOP, FRONT, RIGHT = Vector(0, 0, 1), Vector(0, -1, 0), Vector(1, 0, 0)
XX, YY = Vector(1, 0, 0), Vector(0, 1, 0)


# ===================================================================== FRAME
def frame():
    doc = App.getDocument("Frame")
    body = doc.getObject("Frame")
    sh = Sheet(doc, "Drawing", "Main frame", "2 x 2 x 3/16 in square tube", "1:7 (side view 1:4)", "CULT-01")
    top = sh.view("Top", body, TOP, XX, 205, 188, 1 / 7.0)
    log("frame / top")
    dim(sh, top, "DistanceX", [top.vertex(-41, 11, 2), top.vertex(41, 11, 2)], 0, 15.5, 0)
    dim(sh, top, "DistanceY", [top.vertex(-41, -11, 2), top.vertex(-41, 11, 2)], -46, 0, 0)
    dim(sh, top, "DistanceY", [top.vertex(41, 11, 2), top.vertex(39, 9, 2)], 45, 10, 0)
    dim(sh, top, "DistanceX", [top.vertex(-39.5, 10, 2), top.vertex(-30, 10, 2)], -34.75, 13.5, 0)
    dim(sh, top, "DistanceX", [top.vertex(-39.5, -10, 2), top.vertex(-36.5, -10, 2)], -38, -14, 0)
    dim(sh, top, "Diameter", [top.edge("circle", 39.5, 10, 2, radius=0.25)], 44, 15, 0)
    # hitch spacing between the two clevis centre lines, on cosmetic vertices
    for x in (-15.0, 15.0):
        top.v.makeCosmeticVertex(top.U(x, -14, 3))
    doc.recompute()
    H.pump(300)
    dim(sh, top, "DistanceX", [top.vertex(-15, -14, 3, tol=0.01), top.vertex(15, -14, 3, tol=0.01)], 0, -16.6, 0)

    front = sh.view("Front", body, FRONT, XX, 205, 128, 1 / 7.0)
    log("frame / front")
    dim(sh, front, "DistanceY", [front.vertex(-41, -11, 0), front.vertex(-41, -11, 2)], -46, -11, 1)
    dim(sh, front, "DistanceY", [front.vertex(41, -11, 0), front.vertex(15.75, -14, 3)], 46, -11, 1.5)

    side = sh.view("Right", body, RIGHT, YY, 125, 66, 1 / 4.0)
    log("frame / right")
    dim(sh, side, "Diameter", [side.edge("circle", 15, -12, 1.5, radius=0.5)], 15, -9, 5.5)
    # the nose has R0.63 corners, so take the upper tangent point, and the plate's top-rear corner
    dim(sh, side, "DistanceX", [side.vertex(15, -14, 3 - 0.63), side.vertex(15, -9, 3)], 15, -11.5, 5.2)
    sh.note(["All dimensions in inches.",
             "Holes: 2 per tyne station, 9 stations",
             "per bar, same pattern on both bars."], 332, 104, 4.5)
    return sh.export(os.path.join(H.ASSETS, "dwg_frame.png"))


# ==================================================================== TINE 01
def tine01():
    doc = App.getDocument("Tine01")
    body = doc.getObject("Tine01")
    sh = Sheet(doc, "Drawing", "Tine 01 - front rank (5 off)", "Rigid tyne, 1.5 in bar",
               "1:4 (top view 1:3)", "CULT-02")
    rv = sh.view("Right", body, RIGHT, YY, 110, 152, 1 / 4.0)
    log("tine01 / right")
    A = math.radians(35.0)
    # key points of the side profile (model y = fore-aft, z = up)
    arc_c = (-7.125, -15.0)
    ro, ri = 8.25, 6.0
    p_arc_r = (arc_c[0] + ro * math.cos(-A), arc_c[1] + ro * math.sin(-A))
    tang = (math.sin(-A), -math.cos(-A))
    p_tip_r = (p_arc_r[0] + tang[0] * 5.65, p_arc_r[1] + tang[1] * 5.65)
    dim(sh, rv, "DistanceX", [rv.vertex(0, -1.125, 0), rv.vertex(0, 1.125, 0)], 0, 0, 2.5)
    dim(sh, rv, "DistanceY", [rv.vertex(0, 1.125, 0), rv.vertex(0, 1.125, -15)], 0, 3.2, -7.5)
    dim(sh, rv, "Radius", [rv.edge("circle", 0, arc_c[0], arc_c[1], radius=ri)], 0, -4.5, -19)
    dim(sh, rv, "Distance", [rv.edge("line", 0, (p_arc_r[0] + p_tip_r[0]) / 2, (p_arc_r[1] + p_tip_r[1]) / 2)],
        0, p_tip_r[0] + 3.2, (p_arc_r[1] + p_tip_r[1]) / 2)
    # The rake: the rear edge and the foot never meet (the bend is between
    # them), so extend both to a cosmetic apex and use a three-point angle.
    t_int = (1.125 - p_arc_r[0]) / tang[0]
    apex = (1.125, p_arc_r[1] + t_int * tang[1])
    below = (1.125, apex[1] - 6.0)
    for yy, zz in (apex, below):
        rv.v.makeCosmeticVertex(rv.U(0, yy, zz))
    doc.recompute()
    H.pump(300)
    dim(sh, rv, "Angle3Pt", [rv.vertex(0, below[0], below[1], tol=0.01), rv.vertex(0, apex[0], apex[1], tol=0.01),
                             rv.vertex(0, p_tip_r[0], p_tip_r[1])],
        0, 3.8, apex[1] - 3.5)
    dim(sh, rv, "DistanceY", [rv.vertex(0, -1.125, 0), rv.vertex(0, p_tip_r[0], p_tip_r[1])], 0, -7.5, -12)

    fv = sh.view("Front", body, FRONT, XX, 215, 152, 1 / 4.0)
    log("tine01 / front")
    dim(sh, fv, "DistanceX", [fv.vertex(-2.5, 0, 0), fv.vertex(2.5, 0, 0)], 0, 0, 2.5)
    dim(sh, fv, "DistanceX", [fv.vertex(-0.75, 0, -15), fv.vertex(0.75, 0, -15)], 0, 0, -17)
    dim(sh, fv, "DistanceY", [fv.vertex(2.5, 0, 0), fv.vertex(2.5, 0, -1.25)], 4.5, 0, -0.6)

    tv = sh.view("Top", body, TOP, XX, 330, 205, 1 / 3.0)
    log("tine01 / top")
    dim(sh, tv, "DistanceX", [tv.vertex(-1.5, 0, 0), tv.vertex(1.5, 0, 0)], 0, 2.6, 0)
    dim(sh, tv, "Diameter", [tv.edge("circle", 1.5, 0, 0, radius=0.25)], 3.4, -2.6, 0)
    dim(sh, tv, "DistanceY", [tv.vertex(-2.5, -1.125, 0), tv.vertex(-2.5, 1.125, 0)], -3.6, 0, 0)
    sh.note(["All dimensions in inches.",
             "Tyne length along the centreline: 25 in",
             "(15 straight + R7.125 bend + 5.65 foot).",
             "Bolt holes 0.5 through, 3 in centres."], 335, 128, 4.2)
    return sh.export(os.path.join(H.ASSETS, "dwg_tine01.png"))


# ==================================================================== TINE 02
def tine02():
    doc = App.getDocument("Tine02")
    body = doc.getObject("Tine02")
    sh = Sheet(doc, "Drawing", "Tine 02 - rear rank (4 off)", "Curved tyne, R16 centreline",
               "1:3 (top view 1:4)", "CULT-03")
    rv = sh.view("Right", body, RIGHT, YY, 125, 150, 1 / 3.0)
    log("tine02 / right")
    RC, W, TOPS = 16.0, 2.5, 2.0
    SW = math.asin(15.0 / RC)
    c = (-RC, -TOPS)
    # the R16 centreline is not an edge of the solid: draw it as a cosmetic arc
    rv.v.makeCosmeticCircleArc(rv.U(0, c[0], c[1]), RC * IN, -math.degrees(SW), 0.0)
    tip_mid = (c[0] + RC * math.cos(-SW), c[1] + RC * math.sin(-SW))
    for (yy, zz) in ((0.0, -TOPS), tip_mid):
        rv.v.makeCosmeticVertex(rv.U(0, yy, zz))
    doc.recompute()
    H.pump(400)
    dim(sh, rv, "DistanceX", [rv.vertex(0, -1.25, 0), rv.vertex(0, 1.25, 0)], 0, 0, 2.5)
    dim(sh, rv, "DistanceY", [rv.vertex(0, 1.25, 0), rv.vertex(0, 1.25, -2)], 0, 3.6, -1)
    dim(sh, rv, "Radius", [rv.edge("circle", 0, c[0], c[1], radius=RC)], 0, -9.5, -8.5)
    dim(sh, rv, "DistanceY", [rv.vertex(0, 0, -TOPS, tol=0.01), rv.vertex(0, tip_mid[0], tip_mid[1], tol=0.01)],
        0, 4.5, -9.5)
    dim(sh, rv, "Radius", [rv.edge("circle", 0, -10.4, -17.0, radius=1.0, tol=12)], 0, -13.5, -19.5)

    fv = sh.view("Front", body, FRONT, XX, 245, 150, 1 / 3.0)
    log("tine02 / front")
    dim(sh, fv, "DistanceX", [fv.vertex(-2.5, 0, 0), fv.vertex(2.5, 0, 0)], 0, 0, 2.5)
    dim(sh, fv, "DistanceX", [fv.vertex(-0.625, 0, -6), fv.vertex(0.625, 0, -6)], 0, 0, -8)
    dim(sh, fv, "DistanceY", [fv.vertex(2.5, 0, 0), fv.vertex(2.5, 0, -1.25)], 4.5, 0, -0.6)

    tv = sh.view("Top", body, TOP, XX, 350, 200, 1 / 4.0)
    log("tine02 / top")
    dim(sh, tv, "DistanceX", [tv.vertex(-1.5, 0, 0), tv.vertex(1.5, 0, 0)], 0, 2.8, 0)
    dim(sh, tv, "Diameter", [tv.edge("circle", 1.5, 0, 0, radius=0.25)], 3.4, -2.8, 0)
    sh.note(["All dimensions in inches.",
             "Dashed arc: R16 centreline of the bar,",
             "15 in working height below the straight.",
             "Bolt holes 0.5 through, 3 in centres."], 330, 100, 4.2)
    return sh.export(os.path.join(H.ASSETS, "dwg_tine02.png"))


# ===================================================================== BLADE
def blade():
    path = os.path.join(H.PARTS, "06_blade01.FCStd")
    doc = None
    for d in App.listDocuments().values():
        if os.path.normcase(d.FileName) == os.path.normcase(path):
            doc = d
    if doc is None:
        doc = App.openDocument(path)
    App.setActiveDocument(doc.Name)
    body = doc.getObject("Blade")
    sh = Sheet(doc, "Drawing", "Blade 01 - sweep share", "0.2 in plate, bent R10", "4:5 (side view 1:1)", "CULT-06")
    tv = sh.view("Top", body, TOP, XX, 210, 190, 0.8)
    log("blade / top")
    ys = [v.Point.y / IN for v in body.Shape.Vertexes]
    y_trail = max(ys)
    dim(sh, tv, "DistanceX", [tv.vertex(-6.5, y_trail, 1), tv.vertex(6.5, y_trail, 1)], 0, y_trail + 0.9, 0)
    tv.v.makeCosmeticVertex(tv.U(6.5, -2, 0))
    doc.recompute()
    H.pump(300)
    dim(sh, tv, "Angle3Pt", [tv.vertex(6.5, -0.5, 0.2, tol=3), tv.vertex(0, -2, 0), tv.vertex(6.5, -2, 0, tol=0.01)],
        4.5, -1.6, 0)
    dim(sh, tv, "DistanceY", [tv.vertex(0, -2, 0), tv.vertex(-6.5, y_trail, 1)], -8.2, 0, 0)

    rv = sh.view("Right", body, RIGHT, YY, 120, 78, 1.0)
    log("blade / right")
    # the plate faces are R9.9 and R10.1; the R10 is the bend of the plate's
    # centre line, so draw that as a dashed cosmetic arc and dimension it
    th = math.degrees(4.0 / 10.0)
    rv.v.makeCosmeticCircleArc(rv.U(0, -2, 10), 10 * IN, -90.0, -90.0 + th)
    doc.recompute()
    H.pump(400)
    # (a TechDraw radius dimension draws its line all the way to the centre,
    #  10 in above the part, straight across the sheet - so a callout instead)
    lab = rv.P(0, 1.6, 1.4)
    sh.note(["R10 bend", "(dashed: plate centre line)"], rv.v.X.Value + lab.x, rv.v.Y.Value + lab.y, 4.5)
    dim(sh, rv, "DistanceY", [rv.vertex(0, -2, -0.1), rv.vertex(0, -2, 0.1)], 0, -2.9, 0)
    sh.note(["All dimensions in inches.",
             "Cutting edge swept back 13 deg each side.",
             "Blade 02 is identical except bent to R16",
             "(matching the Tine 02 curve)."], 330, 118, 4.5)
    return sh.export(os.path.join(H.ASSETS, "dwg_blade.png"))


H.set_units()
out = []
for fn in (frame, tine01, tine02, blade):
    try:
        out.append(fn())
    except Exception as e:
        import traceback
        log("FAILED", fn.__name__, traceback.format_exc())
for d in ("Frame", "Tine01", "Tine02"):
    App.getDocument(d).save()
for d in App.listDocuments().values():
    if d.FileName.endswith("06_blade01.FCStd"):
        d.save()
print("\n".join(LOG))
