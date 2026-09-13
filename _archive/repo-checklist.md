# What the repo needs before you paste the prompt

Four sections, roughly in the order you should do them. Section 1 is fifteen minutes and
is the only part that is genuinely blocking. Sections 2 and 3 are what decide whether the
slides look real or improvised. Section 4 is optional.

---

## 1 — Quarantine the contaminated files (15 min, blocking)

These files all name SolidWorks. If Claude Design can see them, the vocabulary leaks back
into the slides no matter what the prompt says:

```
CLAUDE.md
transcript.txt
decks/          (all 14 HTML + all 14 PDF)
tools/          (build scripts, deck_kit, decks/, decks_v1/)
```

`design/` and `screenshots/` are clean — I checked every file. Nothing to do there.

The prompt tells Design not to read the contaminated paths, but an instruction is weaker
than absence. Move them out of the way:

```bash
git mv CLAUDE.md transcript.txt decks tools _archive/
git commit -m "Archive authoring notes and v1 decks"
git push
```

`screenshots/` does not move, so every raw URL in the prompt keeps working.

Nothing is deleted. `_archive/` keeps your build scripts and the v1 decks if you want them
later.

**One file to actually delete:**

```
screenshots/01_frame_01_params_spreadsheet.png
```

It shows an empty 3D viewport. The spreadsheet exists only in the tree. Any slide built on
it would be illustrating nothing.

---

## 2 — Capture the command dialogs (2–3 hours, high impact)

This is the fix that matters most. Right now **no screenshot in the repo shows a command
dialog open.** Every capture is the state after a feature was created, with the Tasks
panel sitting on its default list. A student cannot learn which box to type into from a
picture taken after the box closed.

None of this needs a model rebuilt. Open the existing `.FCStd`, start the command,
screenshot the dialog, press Escape.

### Before you start

- Switch FreeCAD to the **light theme** (Preferences ▸ General ▸ Theme). Dark UI projects
  badly and prints worse.
- Resize the window to **1360 × 1020**. The frame captures already use this and they are
  the most legible ones you have.
- Press **View ▸ Fit All** before every single capture.
- Save into `screenshots/` using the `dlg_` prefix below, so the prompt picks them up
  automatically.

### The list — 17 captures

| Filename | What must be visible |
|---|---|
| `dlg_units.png` | Preferences ▸ General ▸ Units, set to Imperial decimal |
| `dlg_workbench.png` | The workbench dropdown open, Part Design highlighted |
| `dlg_spreadsheet.png` | The Spreadsheet tab with all named parameters and values filled in |
| `dlg_alias.png` | A cell selected with the Alias field being typed into |
| `dlg_expression.png` | The expression editor open, showing a parameter name typed into a dimension |
| `dlg_dimension.png` | The Insert length dialog in Sketcher, with a value typed |
| `dlg_pad.png` | Pad task panel, Length **2 in** |
| `dlg_pocket_through.png` | Pocket task panel, type set to Through all |
| `dlg_pocket_offset.png` | Pocket with a reversed attachment offset, for the hollow tube |
| `dlg_hole.png` | Hole task panel with diameter and depth set |
| `dlg_fillet.png` | Fillet task panel with a radius set |
| `dlg_linearpattern.png` | LinearPattern: direction, length **19 in**, occurrences **9** |
| `dlg_mirrored.png` | Mirrored task panel with a plane selected |
| `dlg_pipe.png` | Additive Pipe with spine and section both selected |
| `dlg_asm_insert.png` | Assembly ▸ Insert Component |
| `dlg_asm_joint.png` | Assembly ▸ Create Joint, mid-selection |
| `dlg_error.png` | A deliberate failure: an over-constrained sketch, or an Invalid feature red-flagged in the tree |

That last one is worth the trouble. The watch-out slides are the ones students remember,
and a real red warning is far more convincing than a drawing of one.

**If you skip this section entirely**, the prompt still works — Design will draw clean
mockups of each dialog and caption them as diagrams. It looks tidy but students will find
the real dialog looks different, which costs you in the lab.

---

## 3 — Re-capture parts 2 to 8 (2 hours, high impact)

The frame was recaptured at 1360 × 1020, but parts 2 through 8 are still **1920 × 1009** —
a 1.9:1 frame with a large empty panel on the left and UI text too small to read from the
back of a room. That is the "too wide, too much dead space" problem you already noticed.

Two sketch captures also have a specific problem worth fixing while you are in there:

- `02_tine01_02_sketch_profile.png` — the dimension labels overlap each other, "ShankWidth"
  collides with the origin marker, and one label reads `FootReach = -3.60693 in`. A raw
  negative float with five decimal places on a teaching slide is not useful.
- `01_frame_03_sketch_plan_constrained.png` — the rectangle runs off the right edge behind
  the Tasks panel. Not zoomed to fit.

**In the Sketcher, before capturing:** drag the dimension labels apart so none overlap,
and give the driving dimensions readable values. Overwrite the existing files with the
same names so the prompt's image list keeps working.

There is also a gap in the sequence — there is no `01_frame_09_*`. Either capture whatever
step is missing there, or renumber so the frame runs unbroken.

---

## 4 — New assets you need to supply (optional but visible)

Put these in a new `assets/` folder. The prompt already references these exact filenames.

| File | What it is | Why |
|---|---|---|
| `cultivator-field.jpg` | A real tractor-mounted cultivator working in a field | Module 1 opens on it. Use your own photo or something you hold rights to — I shouldn't source one for you. |
| `dwg_frame.png` | Dimensioned 2D views of the frame | Farm machinery students are trained to model *from a drawing*. Right now they'd be modelling from bullet points. |
| `dwg_tine01.png` | Dimensioned profile of Tine 01 | Same. Module 5 has a slide reserved for it. |
| `dwg_tine02.png` | Dimensioned profile of Tine 02, R16 called out | Same, Module 6. |
| `dwg_blade.png` | Dimensioned blade, plan and section | Same, Module 9. |
| `asm_exploded.png` | Exploded view of the assembly | Module 12. |

The four drawings are TechDraw sheets — it is noted as not yet done in your own status
list. If TechDraw is more work than you want right now, clean hand-annotated exports of
the existing `*_final_Front` and `*_final_Right` renders will do the same job.

---

## 5 — Verify before you paste

```bash
# every screenshot resolves publicly
for f in screenshots/*.png; do
  n=$(basename "$f")
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://raw.githubusercontent.com/vibhuu22/freecad-cultivator-course/main/screenshots/$n")
  [ "$code" = "200" ] || echo "MISSING: $n ($code)"
done

# nothing outside _archive mentions the other CAD package
grep -ril -E "solidworks|solid works|weldment" . --exclude-dir=_archive --exclude-dir=.git
```

Both should print nothing. Then paste Part A of the prompt into a fresh Claude Design
canvas, followed by Module 1.

---

## Order I'd do it in

Section 1 today — it's fifteen minutes and unblocks everything. Then Module 1 through 4 in
Design, because Module 4 is already drafted in `design/` and building it will tell you fast
whether the visual system holds up at scale. Only then decide how much of Sections 2 and 3
you want to invest, with a real deck in front of you to judge against.
