# -*- coding: utf-8 -*-
"""Tighten the 3D viewport renders.

FreeCAD's ViewFit leaves the model floating in a lot of empty background, which
on a slide means a small part and a large dark rectangle.  This trims each
render down to the model plus a margin, then pads it back out to 4:3 so every
plate on a slide is the same shape.

Only touches the viewport renders (_Isometric / _Right / _Front / _Top); the
full-window UI grabs are left alone.

    python tools\\crop_shots.py
"""
import os, glob, sys
from PIL import Image, ImageChops

SHOTS = r"C:\Users\ASUS\Desktop\freecad\screenshots"
VIEWS = ("_Isometric", "_Right", "_Front", "_Top", "_Left", "_Rear", "_Bottom")
ASPECT = 4.0 / 3.0
MARGIN = 0.05          # of the trimmed size, added all round
TOL = 18               # per-channel difference that counts as "not background"


def content_box(im, tol=TOL):
    """Bounding box of everything that is not the background colour."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda v: 255 if v > tol else 0)
    return diff.getbbox()


def fit_aspect(box, size, aspect=ASPECT):
    """Grow box to the target aspect, centred, clamped to the image."""
    x0, y0, x1, y1 = box
    W, H = size
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    if w / float(h) < aspect:
        w = h * aspect
    else:
        h = w / aspect
    # do not ask for more than the image has
    if w > W:
        w, h = W, W / aspect
    if h > H:
        h, w = H, H * aspect
    x0, x1 = cx - w / 2.0, cx + w / 2.0
    y0, y1 = cy - h / 2.0, cy + h / 2.0
    if x0 < 0:
        x0, x1 = 0, w
    if x1 > W:
        x0, x1 = W - w, W
    if y0 < 0:
        y0, y1 = 0, h
    if y1 > H:
        y0, y1 = H - h, H
    return tuple(int(round(v)) for v in (x0, y0, x1, y1))


def tighten(path):
    im = Image.open(path)
    box = content_box(im)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    mx = int((x1 - x0) * MARGIN)
    my = int((y1 - y0) * MARGIN)
    box = (max(0, x0 - mx), max(0, y0 - my),
           min(im.size[0], x1 + mx), min(im.size[1], y1 + my))
    box = fit_aspect(box, im.size)
    if box[2] - box[0] >= im.size[0] - 4 and box[3] - box[1] >= im.size[1] - 4:
        return None                      # already full-frame, nothing to gain
    im.crop(box).save(path)
    return box


def main():
    targets = [p for p in sorted(glob.glob(os.path.join(SHOTS, "*.png")))
               if any(os.path.basename(p)[:-4].endswith(v) for v in VIEWS)]
    done = 0
    for p in targets:
        im = Image.open(p)
        before = im.size
        box = tighten(p)
        if box:
            after = Image.open(p).size
            done += 1
            print("  %-34s %sx%s -> %sx%s" % (os.path.basename(p),
                                              before[0], before[1], after[0], after[1]))
    print("tightened %d of %d viewport renders" % (done, len(targets)))


if __name__ == "__main__":
    main()
