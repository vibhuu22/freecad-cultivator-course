# -*- coding: utf-8 -*-
"""Capture FreeCAD command dialogs (checklist section 2) without changing the models.

Every capture opens a task panel on an existing feature, screenshots the whole
window, then cancels. Run inside FreeCAD:

    import sys; sys.path.insert(0, r"C:\\Users\\ASUS\\Desktop\\freecad\\_archive\\tools")
    import dlg_helpers as D; D.reload_me()
"""
import sys, importlib
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import fc_helpers as H


def reload_me():
    importlib.reload(H)
    importlib.reload(sys.modules[__name__])


def mw():
    return Gui.getMainWindow()


def dock(title):
    for d in mw().findChildren(QtWidgets.QDockWidget):
        if d.windowTitle() == title:
            return d


def layout():
    """1360x1020 window, Model and Tasks tabbed on the left, nothing floating."""
    w = mw()
    if w.isMaximized():
        w.showNormal()
    w.resize(1360, 1020)
    m, t = dock("Model"), dock("Tasks")
    if w.dockWidgetArea(t) != QtCore.Qt.LeftDockWidgetArea:
        w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, t)
        w.tabifyDockWidget(m, t)
    w.resizeDocks([m], [330], QtCore.Qt.Horizontal)
    H.pump(200)


def use_doc(name):
    """Make `name` the active document and bring its 3D view tab to the front."""
    App.setActiveDocument(name)
    gdoc = Gui.getDocument(name)
    mdi = mw().findChild(QtWidgets.QMdiArea)
    for sw in mdi.subWindowList():
        if sw.widget() is not None and gdoc.ActiveView is not None:
            if sw.windowTitle().split(" : ")[0] == App.getDocument(name).Label:
                mdi.setActiveSubWindow(sw)
                break
    H.pump(200)
    return App.getDocument(name)


def tasks_front():
    dock("Tasks").raise_()
    H.pump(150)


def model_front():
    dock("Model").raise_()
    H.pump(150)


def fit(orient=None):
    v = Gui.ActiveDocument.ActiveView
    if orient == "Isometric":
        v.viewIsometric()
    elif orient:
        getattr(v, "view" + orient)()
    Gui.SendMsgToActiveView("ViewFit")
    H.pump(250)


def task_widget():
    return dock("Tasks").widget()


def task_button(text):
    for b in dock("Tasks").findChildren(QtWidgets.QAbstractButton):
        if b.isVisible() and b.text().replace("&", "") == text:
            return b


def close_task(cancel=True):
    """Cancel (or OK) whatever task dialog is open; fall back to resetEdit."""
    b = task_button("Cancel" if cancel else "OK")
    if b is not None:
        b.click()
        H.pump(250)
    if Gui.Control.activeDialog():
        try:
            Gui.ActiveDocument.resetEdit()
        except Exception:
            pass
        Gui.Control.closeDialog()
    H.pump(200)
    model_front()


def edit(obj, orient="Isometric"):
    """Open the task panel of an existing feature, fit the view."""
    Gui.ActiveDocument.setEdit(obj, 0)
    H.pump(400)
    tasks_front()
    fit(orient)


def set_quantity(label_fragment, value, parent=None):
    """Type into the task-panel quantity field whose label contains label_fragment."""
    root = parent or dock("Tasks")
    for lab in root.findChildren(QtWidgets.QLabel):
        if label_fragment.lower() in lab.text().lower() and lab.isVisible():
            buddy = lab.buddy()
            if buddy is not None:
                buddy.setText(value)
                return buddy
    return None


def gizmos(on):
    """The 1.1 drag gizmos float in empty space on a still image - off while capturing."""
    App.ParamGet("User parameter:BaseApp/Preferences/Gui/Gizmos").SetBool("EnableGizmos", on)


def shot(name):
    H.pump(250)
    mw().statusBar().clearMessage()
    H.pump(50)
    return H.shot(name)


def shot_with_popups(name, popups):
    """Main window plus separate top-level popups (combo lists, dialogs) painted
    at their on-screen positions - mw.grab() alone never includes them."""
    from PySide import QtGui
    H.pump(250)
    w = mw()
    w.statusBar().clearMessage()
    pix = w.grab()
    painter = QtGui.QPainter(pix)
    origin = w.mapToGlobal(QtCore.QPoint(0, 0))
    for p in popups:
        pos = p.mapToGlobal(QtCore.QPoint(0, 0)) - origin
        painter.drawPixmap(pos, p.grab())
    painter.end()
    return H._save(pix, name)
