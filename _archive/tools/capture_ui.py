# -*- coding: utf-8 -*-
"""Interface-tour screenshots (00_ui_*) and the finished-part window shots
(*_ui_complete). Run after the build scripts, with their documents still open.
"""
import sys
sys.path.insert(0, r"C:\Users\ASUS\Desktop\freecad\_archive\tools")
import fc_helpers as H
H.reload_me()
import fc_helpers as H
import dlg_helpers as D
D.reload_me()
import dlg_helpers as D

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets

H.set_units()
D.layout()
Gui.activateWorkbench("PartDesignWorkbench")
H.pump(300)


def tree():
    for t in H.mw().findChildren(QtWidgets.QTreeWidget):
        if t.isVisible() and t.topLevelItemCount():
            return t


def focus_tree(doc):
    """Collapse every other document; open this one down to its features."""
    t = tree()
    for i in range(t.topLevelItemCount()):
        top = t.topLevelItem(i)
        mine = top.text(0) == doc.Label
        top.setExpanded(mine)
        if mine:
            for j in range(top.childCount()):
                top.child(j).setExpanded(True)
    H.pump(200)


def finished(docname, shotname):
    doc = D.use_doc(docname)
    Gui.Selection.clearSelection()
    D.model_front()
    focus_tree(doc)
    H.view("Isometric")
    return H.shot(shotname)


out = []
out.append(finished("Frame", "00_ui_00_window"))
out.append(H.shot_dock("Model", "00_ui_01_model_tree"))
for frag, name in (("Structure", "00_ui_02_tb_structure"),
                   ("Helper", "00_ui_03_tb_pd_helper"),
                   ("Modeling", "00_ui_04_tb_pd_modeling"),
                   ("Dress-Up", "00_ui_05_tb_pd_dressup"),
                   ("Transformation", "00_ui_06_tb_pd_transform"),
                   ("View", "00_ui_07_tb_view")):
    out.append(H.shot_toolbar(frag, name))
out.append(finished("Frame", "01_frame_ui_complete"))
out.append(finished("Tine01", "02_tine01_ui_complete"))
out.append(finished("Tine02", "03_tine02_ui_complete"))
print("\n".join(str(o) for o in out))
