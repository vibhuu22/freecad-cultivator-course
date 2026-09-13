# Project: 9-Tyne Cultivator in FreeCAD — Teaching Deck

## Goal
Rebuild a 9-tyne tractor-mounted cultivator in **FreeCAD 1.1**, capturing FreeCAD UI
screenshots at **every step**, then produce detailed explanatory slide decks that teach
students of *Course: Design of Farm Machinery* how to model it themselves in FreeCAD.

Audience: undergrad farm-machinery students who are **new to FreeCAD**.
Design brief from the user: "simple and easy to understand", "explain the entire process
properly in detail", no slide-count limit, well-designed slides, end-to-end.

## Source
**Video:** https://www.youtube.com/watch?v=eZTZThWtG-k
"Design of Cultivator in solidworks | Nine tines cultivator | Solidworks hindi tutorial"
— channel *Malviya CAD Solution* (https://www.youtube.com/@MalviyaCADSolution).
Original audio is **Hindi**, which is why the supplied translation is rough in places.

`freecadtutorial.docx` → extracted to `transcript.txt` (the English translation).
The video title confirms **nine tines**, matching the 5 × Tine-01 + 4 × Tine-02 derivation below.
The decks must therefore translate SolidWorks terminology → FreeCAD equivalents explicitly,
because students may also be watching the SolidWorks source.

The transcript is machine-translated and some numbers are garbled (e.g. "hole size is 12.5"
then "hole size is 3 inches"). Use engineering judgement, state assumptions on the slides,
and keep everything dimensionally consistent.

## Prior art on this machine
`C:\Users\ASUS\Desktop\fd` holds the same workflow done previously for a **Moldboard Plough**
(8 PDF decks in `fd/decks`, ~50 screenshots in `fd/screenshots`, `build_deck.py` generator,
plus `freecad_course.html`, `plough_manual.html`). Match that structure and quality.
Reuse / adapt `fd/build_deck.py` as the deck generator.

## Environment
- FreeCAD MCP server `freecad` registered for this project in `~/.claude.json`
  (`uvx freecad-mcp`). Backup of the config: `~/.claude.json.bak-*`.
- FreeCAD addon `FreeCADMCP` installed at `~/AppData/Roaming/FreeCAD/v1-1/Mod/FreeCADMCP`,
  with `auto_start_rpc: true` → the RPC server starts when the FreeCAD GUI launches.
- **FreeCAD GUI must be running** for MCP calls and screenshots to work.
- Units: set FreeCAD to **Imperial decimal** (inches) to match the tutorial (SolidWorks IPS).

## Working rules
1. Screenshot after EVERY meaningful step — sketch created, constraints applied, each dialog
   open, each feature confirmed, tree-view state. Not just finished parts.
2. Name screenshots `NN_part_step_description.png` so deck assembly is mechanical.
3. Build each part as its own `.FCStd` in `parts/`, then a separate assembly file.
4. Prefer **parametric** construction (spreadsheet-driven where sensible) so students can
   change tyne count / spacing — a genuine FreeCAD advantage worth teaching.
5. Save often; the FreeCAD RPC connection can drop.

## Directory layout
- `transcript.txt`   — extracted English transcript (source of truth for the steps)
- `parts/`           — individual .FCStd part files
- `screenshots/`     — every captured FreeCAD UI screenshot
- `decks/`           — generated slide decks (PDF / HTML)
- `assets/`          — diagrams, exported renders

## The model (derived from the transcript)

### Overall
9 tynes = **5 × Tine-01** on the front toolbar + **4 × Tine-02** on the rear toolbar,
staggered. Tyne pitch along one bar = 19 in; effective working spacing = 9.5 in.
Frame hole pattern = 9 holes @ 9.5 in pitch (8 × 9.5 = 76 in inside an 82 in frame).

### Part 1 — Frame
- Layout rectangle (centred): 82 in × 22 in.
- Square tube structural members, wall 0.1875 in (ANSI Inch square tube in SolidWorks).
- Mounting holes: 9 @ 9.5 in pitch, 0.5 in dia; mirrored about the Front plane to the 2nd bar.
- Hitch brackets: corner rectangle 0.63 in, pair gap 1.5 in, 15 in from origin,
  pad depth 0.4 in, full-round fillet on 3 faces each side, mirrored about the Right plane.
- Bracket pin hole via Hole Wizard.

### Part 2 — Tine 01 (front rank, 5 off)
- Profile sketched on the Right plane, symmetric about the origin.
- Overall length 25 in; working height 15 in; key dims 1.5 in, 2.25 in, 2 in, 1 in.
- Thickness 1.5 in inside / 2 in outside → pad.
- Mounting pad: 5 in × 1.25 in rectangle, 11 in from origin, 22 in point-to-point.
- 2 bolt holes 0.5 in dia, 3 in apart, mirrored about the centreline. Blind 0.4 in.

### Part 3 — Tine 02 (rear rank, 4 off)
- Right plane, midpoint line 24 in; heights 2 in each side; gap 2.5 in.
- **Curve radius 16 in** both sides; 20.3 in from point to midpoint of the outer arc.
- Working height 15 in; dims 1.5 in, 1.5 in, 5 in spacing, 1 in top.
- Corner fillet R1; bottom radius R2. Thickness 1.25 in.
- Mounting pad on the bottom face: centre rectangle 5 in × 1.25 in, symmetric,
  11 in from origin, 22 in centre-to-centre. Holes 0.5 in dia, 3 in apart, mirrored.
  Blind 0.5 in.

### Part 4 — Clamp 01
- Right plane. Line 4 in, straight run 18 in, dim 7 in, angle 45°.
- Fillet R2. Offset Entities 0.5 in inward, close both ends.
- Width / thickness 3 in. Through hole 1 in dia.

### Part 5 — Clamp 02
- Right plane. Line 26.6 in, tip angle 30°, fillet, Offset Entities 0.5 in.
- Same 3 in width treatment.

### Part 6 — Blade 01 (shovel / sweep)
- Base 13 in × 4 in, thickness 0.5 in.
- Top-face sketch: centrelines, 13° angle, 1.5 in gap; mirrored about the centreline.
- Extruded cut from converted entities; full-round fillet on 3 faces each side.
- Sheet thickness 0.2 in ("normal plate").
- **Bend radius −10 in** (SolidWorks Flex → Bending).

### Part 7 — Blade 02
- Identical to Blade 01 with **bend radius −16 in** (matches Tine-02's 16 in arc).

### Assembly
- Frame fixed at the origin.
- Tine-01 mated (face + concentric holes), linear pattern: 19 in pitch, 5 instances.
- Tine-02 mated, linear pattern: 19 in pitch, 4 instances, staggered by 9.5 in.
- Blade-01 → Tine-01: tyne Right plane to blade Front plane, 3 in offset; patterned.
- Blade-02 → Tine-02 likewise, 3 in offset; patterned.
- Clamps inserted, mated frame Front plane ↔ clamp Right plane; copied to the other side.
- Hex bolts: lengths 1.5 / 2.75 / 5.5 / 5 / 4 / 1.25 in as called out; 1.25 TPI.
  Bolt linear pattern: 9.5 in pitch, 9 instances, then mirrored about the Front plane.

## SolidWorks → FreeCAD translation table (goes into the decks)

| SolidWorks | FreeCAD 1.1 |
|---|---|
| Units IPS | Preferences ▸ General ▸ Units ▸ Imperial decimal |
| Part / Feature tree | PartDesign **Body**, Model tree |
| Sketch on plane | PartDesign ▸ Create Sketch, pick XY / XZ / YZ |
| Smart Dimension | Sketcher **Dimension** constraint (K, D) |
| Fully Defined sketch | Sketcher "Fully constrained" status message |
| Convert Entities | Sketcher **External Geometry** (G, X) |
| Offset Entities | Sketcher **Offset** |
| Trim Entities | Sketcher **Trim edge** (G, T) |
| Mirror Entities (sketch) | Sketcher **Symmetry** / mirror about a construction line |
| Linear Sketch Pattern | Sketcher **Rectangular Array** |
| Boss-Extrude | PartDesign **Pad** |
| Extruded Cut | PartDesign **Pocket** |
| Blind condition | Pad / Pocket type **Dimension** |
| Mirror (feature) | PartDesign **Mirrored** |
| Linear Pattern (feature) | PartDesign **LinearPattern** |
| Hole Wizard | PartDesign **Hole** |
| Fillet / full-round fillet | PartDesign **Fillet** (Part Fillet as fallback) |
| Weldments ▸ Structural Member | No core equivalent. Teach: sketch the square-tube section and **Pad** it, or sweep with **Additive Pipe**. (Optional addon: Dodo / Flamingo.) |
| Flex ▸ Bending | No equivalent. Teach: build the blade curved *by construction* — sweep the blade section along an arc of R10 / R16 with **Additive Pipe**. Changing the arc radius reproduces the "−10 → −16" edit exactly, and is more parametric. |
| Appearance / Material | View tab ▸ **Shape Appearance**; Material task panel |
| Assembly + Mates | **Assembly** workbench (built into 1.0+), **Joints**: Fixed, Coincident, Planar, Revolute |
| Linear Component Pattern | Assembly has no direct equivalent; place instances with joints or use a transform array. Flag this limitation on the slide. |
| Toolbox hex bolts | **Fasteners** workbench (addon) or model the bolt as a simple part |

## Deck plan (adjust as the work proceeds)
1. Introduction — what a cultivator is, its agronomic role, why we model it
2. FreeCAD interface tour + SolidWorks→FreeCAD vocabulary
3. Setting up: units, workbenches, document structure
4. Sketching fundamentals and constraints (fully-defined sketches)
5. Part 1 — Frame
6. Part 2 — Tine 01
7. Part 3 — Tine 02
8. Parts 4 & 5 — Clamps
9. Parts 6 & 7 — Blades (and how to reproduce SolidWorks Flex)
10. Assembly and joints
11. Fasteners and patterns
12. Appearance, rendering, drawings (TechDraw)
13. Making it parametric — spreadsheet-driven tyne count / spacing
14. Summary + student exercises

## Status
- [x] Transcript extracted to `transcript.txt`
- [x] MCP configured for this project
- [x] FreeCAD connection verified (1.1.3; Imperial decimal needs `App.Units.setSchema(3)`,
      setting the preference parameter alone does not take effect)
- [x] Parts modelled — all 7 + assembly, in `parts/`
- [x] Screenshots captured — 101 in `screenshots/` (5 stale ones from the frame rework deleted)
- [x] Decks generated — 14 decks, 106 slides, HTML + PDF in `decks/`

### The decks (rebuilt after design review)
`tools/deck_kit.py` is the generator. Content is in `tools/decks/dNN_*.py`, one module per
deck, each exposing `build()`. The v1 content is archived in `tools/decks_v1/`.

```
python tools/build_all_decks.py           # HTML + index
python tools/build_all_decks.py --pdf     # also print each deck via headless Chrome
```

**14 decks, 106 slides, 106 PDF pages** - exactly one page per slide.

The first version was rejected: text too small, screenshots too wide and full of dead
space, writing that read as machine-generated. What changed:

- **FreeCAD window resized to 1360x1020** before capturing, so screenshots are 4:3 and the
  UI text is legible on a slide. All build scripts were re-run to recapture.
- **`tools/crop_shots.py`** trims the 3D renders to the model plus a margin, then pads back
  to 4:3, so the part fills the frame instead of floating in dark space.
- **One large screenshot per slide**, not two small ones side by side. Two-up is used only
  where a before/after comparison is the point.
- **20px body text, 46px headings**, a fixed header/rule/body grid so every slide aligns,
  16:9 slides, light theme by default.
- **Plain teaching language.** No Python console output, no solver dumps, no
  `['Touched', 'Invalid']` on a slide. Short sentences, direct address, max five bullets.

### Canva
The Canva connector can build these as real Canva presentations, but note two limits:
- `upload-asset-from-url` only accepts URLs that are **already public**. `tools/publish_shots.py`
  publishes the 55 screenshots the decks use to litterbox (72-hour expiry; Canva copies each
  image into the account at upload time, so the link only needs to live a few minutes).
  Running it needs a Bash permission the auto-mode classifier currently blocks - the user has
  to run it, or allow the rule.
- `generate-design-structured` takes at most **10 assets per design**, so a Canva deck cannot
  carry every screenshot a local deck does.
- The flow is `request-outline-review` -> user approves in the widget -> `generate-design-structured`.

### Modelling decisions — all of these need stating on the slides
1. **Frame holes are pairs.** "One hole here and another hole here" + "the hole size is
   3 inches" = two 0.5 in holes at 3 in centres per station, patterned 9× at 9.5 in pitch.
   This matches the tynes' two mounting bolts, so the machine actually bolts together.
2. **PartDesign cannot pattern a pattern, nor mirror one** (the Mirrored feature goes
   `Invalid`). The rear-bar holes therefore come from a Sketcher **Symmetry** constraint in
   the same sketch. A real limitation students will hit — worth a slide.
3. **No full-round fillet in FreeCAD.** The clevis noses get two R0.63 corner fillets
   instead. R0.63 on the 0.4 in plate edge fails outright — a good worked example.
4. **Angle constraints are ambiguous.** An angle between two *lines* let the solver flip
   Tine 01 backwards. The rake is now the **sweep angle of the bend arc** (35°), which has
   one solution; `FootReach` is a derived (result) row in the sheet. FootLength is the
   rounded 5.65 in (exact 5.6476 would make the centreline exactly 25 in).
5. **Endpoint tangency, not tangency + coincidence.** An edge-to-edge Tangent on a join that
   already has a Coincident conflicts (`solve()` = −3). Use `Tangent(g1,pos1,g2,pos2)`.
6. **Tyne lengths.** 25 in overall = 15 in straight shank + bend + foot, from the
   transcript's own 25 and 15. Rake 35° and inner bend R6 are engineering choices.
7. **Clamp 01/02 are braces.** The source never says what they attach to; modelled as
   0.5 × 3 in straps, placed as mast legs on the rear bar.
8. **Blades have no bolt holes** — the source does not dimension them. Student exercise.

### Not yet done
- Hex bolts (Fasteners addon not installed; would be Part 8 + a link array)
- Assembly **Joints** — components are placed by App::Link arrays, which is the honest
  FreeCAD answer to SolidWorks' Linear Component Pattern. The Joint *dialog* is now
  captured (`dlg_asm_joint.png`) but the assembly itself still uses link arrays.
- `assets/cultivator-field.jpg` — a real field photo the user must supply (rights).

## Repo-checklist pass (2026-09-13)
This file, `transcript.txt`, the .docx, `decks/` and `tools/` were moved to `_archive/` so the
SolidWorks vocabulary stays out of the slide-generation context (Claude Design reads the
repo). Claude Code no longer auto-loads this file; it is referenced from memory.

- Build scripts live in `_archive/tools/` now (their sys.path was updated).
- FreeCAD is on the **FreeCAD Light** theme; Model and Tasks are tabbed on the left (no
  overlay). `user.cfg.bak-before-light-theme-*` in the FreeCAD config dir is the backup.
- Everything recaptured light at 1360x1020. `fc_helpers.fit_sketch` frames sketches on
  their own geometry; `fit_tight` frames standard views on the projected bounding box, so
  `crop_shots.py` is no longer needed. `*_00_params` shots now show the sheet open.
- Sketch labels are placed from `fc_helpers.LABELS` ("<doc>/<sketch>" keyed).
- Readable driving dimensions everywhere: Tine 02 uses a construction R16 centreline arc
  (CurveRadius, WorkHeight 15); clamp legs are length + angle; blade spine is an arc-length
  constraint (FreeCAD 1.1.3 draws no label for those) and the plan edge is a 13° angle.
- 17 `dlg_*.png` captures from `dlg_helpers.py`; UI tour from `capture_ui.py`.
- `build_drawings.py` makes TechDraw pages (saved inside the part files) and
  `assets/dwg_*.png`. Picking notes: getVisibleVertexes/Edges are scaled with y DOWN;
  cosmetic geometry is created unscaled y UP; dimension label X/Y are scaled y UP.
- Run builds strictly one at a time: queued Qt timers nest inside H.pump() otherwise.
