# -*- coding: utf-8 -*-
"""Deck 1 - Introduction: the machine, and why we model it."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck_kit import (Deck, fig, plates, wide, specs, tbl, steps, phases,
                      ticks, note, warn, code, cols)


def build():
    d = Deck("01-introduction", "The Nine-Tyne Cultivator",
             "What the machine does, and what we are going to build")

    d.sheet("00", "GENERAL ARRANGEMENT", "—", "The Nine-Tyne Cultivator", """
<p class="lede">A tractor-mounted, rigid-tyne cultivator — nine tynes on an
82&nbsp;inch frame, cutting a 76&nbsp;inch swath at 9.5&nbsp;inch spacing. Over the next
fourteen decks you will build every part of it in FreeCAD, from an empty document to a
complete parametric assembly.</p>
%s
%s
""" % (fig("08_asm_hero_Isometric", "ISOMETRIC",
           "The finished assembly: 16 solid bodies, 377 lb of steel"),
       specs([("Tynes", "9 (5 front + 4 rear)"),
              ("Working width", "76 in / 6 ft 4 in"),
              ("Tyne spacing", "9.5 in effective"),
              ("Frame", "82 × 22 in square tube"),
              ("Mass", "377 lb / 171 kg"),
              ("Software", "FreeCAD 1.1.3, free and open source")])),
            eyebrow="Design of Farm Machinery", kind="title")

    d.sheet("01", "AGRONOMY", "CONTEXT", "What a cultivator is for", """
<p class="lede">A cultivator is a <strong>secondary tillage</strong> implement. The plough
has already turned the soil; the cultivator's job is to break the clods down, kill weeds,
and leave a seedbed that a drill can work in.</p>
%s
""" % cols("""
<h3>The three jobs</h3>
%s
<h3>Working depth</h3>
<p>A rigid-tyne cultivator like this one works at roughly <strong>4 to 9 inches</strong>.
Depth is set by the tractor's three-point linkage and by how far the tyne is pulled up
through its mounting — which is why each tool bar in our design carries nine bolt
stations, not one welded position.</p>
""" % phases([("Clod reduction",
               "The tyne fractures the furrow slice the plough left behind. Soil "
               "shatters along its own failure planes, which is far less energy per "
               "cubic foot than cutting."),
              ("Weed control",
               "The sweep runs just below the surface and severs weed roots. No "
               "chemistry, and it works on weeds that have already emerged."),
              ("Moisture conservation",
               "Breaking the capillary channels in the top few inches slows evaporation "
               "from below — the classic dust-mulch effect.")]), """
<h3>Where it sits in the sequence</h3>
%s
%s
""" % (tbl(["Pass", "Implement", "Depth"],
           [["Primary", "Mouldboard or disc plough", "8–12 in"],
            ["<strong>Secondary</strong>", "<strong>Cultivator</strong> — this machine", "<strong>4–9 in</strong>"],
            ["Secondary", "Disc harrow / tine harrow", "2–4 in"],
            ["Finishing", "Roller, planker", "surface"]]),
       note("<strong>Why nine tynes?</strong> Nine tynes at 9.5&nbsp;in spacing give a "
            "76&nbsp;in swath. Behind a 35–45&nbsp;hp tractor that is about the right "
            "draught: roughly 100–150&nbsp;lbf per tyne in medium soil, so 900–1350&nbsp;lbf "
            "total — comfortably inside what a compact tractor can pull at 3–4&nbsp;mph."))),
            eyebrow="Why this machine exists")

    d.sheet("02", "LAYOUT", "PRINCIPLE", "Why the tynes are staggered", """
<p class="lede">The nine tynes are not in one row. Five sit on the front tool bar at
19&nbsp;inch pitch; four sit on the rear bar, also at 19&nbsp;inch pitch, but offset by
half a pitch. Seen from above, the points fall at an even 9.5&nbsp;inch spacing.</p>
%s
%s
""" % (plates([("08_asm_hero_Top", "PLAN",
                "Two ranks at 19 in pitch, offset 9.5 in — nine evenly spaced cutting lines"),
               ("08_asm_hero_Front", "FRONT ELEVATION",
                "All nine points work at the same depth")]),
       cols("""
<h3>Why not one row of nine?</h3>
%s
""" % ticks([
    "<strong>Trash flow.</strong> Nine shanks 9.5 in apart in a single row will bridge "
    "with stubble and straw and drag a plug of trash. Two ranks 20 in apart give each "
    "shank room to shed.",
    "<strong>Soil break-out.</strong> A tyne fractures soil in a wedge either side. "
    "Staggering lets the front rank loosen the ground the rear rank then works.",
    "<strong>Frame loading.</strong> Splitting the draught across two bars halves the "
    "torsion on each."]), """
<h3>The arithmetic</h3>
%s
%s
""" % (specs([("Bar pitch", "19 in"), ("Stagger", "9.5 in"),
              ("Effective spacing", "9.5 in"), ("Swath", "8 × 9.5 = 76 in"),
              ("Frame length", "82 in"), ("End margin", "3 in each side")]),
       note("Both bars are drilled with all nine stations at 9.5&nbsp;in pitch, so a "
            "student can move tynes around, or fit nine on one bar for a different job. "
            "That flexibility is the reason the holes are patterned rather than placed.")))),
            eyebrow="The 5 + 4 arrangement")

    d.sheet("03", "PARTS", "BREAKDOWN", "The seven parts", """
<p class="lede">Seven distinct parts make the whole machine. Every one of them is built
in this course, from its first sketch line to its final fillet.</p>
%s
%s
""" % (tbl(["#", "Part", "Off", "What it does", "Deck"],
           [["1", "<strong>Frame</strong>", "1",
             "82 × 22 in welded square-tube frame carrying both tool bars and the hitch", "5"],
            ["2", "<strong>Tine 01</strong>", "5",
             "Rigid tyne — straight shank, forward-raked foot. Front rank.", "6"],
            ["3", "<strong>Tine 02</strong>", "4",
             "Curved C-tyne on a 16 in radius. Rear rank.", "7"],
            ["4", "<strong>Clamp 01</strong>", "2",
             "Bent 3 × 0.5 in strap brace", "8"],
            ["5", "<strong>Clamp 02</strong>", "2",
             "Taller strap brace, 30° tip", "8"],
            ["6", "<strong>Blade 01</strong>", "5",
             "13 in sweep, bent on a 10 in radius", "9"],
            ["7", "<strong>Blade 02</strong>", "4",
             "The same sweep bent on 16 in — one parameter apart from Blade 01", "9"]]),
       plates([("01_frame_final_Isometric", "PART 1 — FRAME", "82 lb"),
               ("02_tine01_final_Right", "PART 2 — TINE 01", "27 lb each"),
               ("03_tine02_final_Right", "PART 3 — TINE 02", "22 lb each"),
               ("06_blade01_final_Isometric", "PART 6 — BLADE 01", "2.4 lb each")],
              "grid-4")),
            eyebrow="What you will build")

    d.sheet("04", "METHOD", "APPROACH", "Modelled, not drawn", """
<p class="lede">Every dimension in this machine lives in a spreadsheet. Change
<code>HolePitch</code> from 9.5 to 12 and the frame re-drills itself. That is what
<strong>parametric</strong> means, and it is the single most important habit to build.</p>
%s
""" % cols("""
<h3>Three rules we hold to throughout</h3>
%s
""" % phases([("Every sketch fully constrained",
               "FreeCAD tells you when a sketch has zero degrees of freedom. If it does "
               "not say so, the geometry can still move — and it will, at the worst "
               "possible moment. We never move on from an under-constrained sketch."),
              ("Every driving dimension in a spreadsheet",
               "Not typed into a constraint. A named cell, referenced by expression. "
               "The model then documents its own design intent."),
              ("Every part in its own file",
               "One body, one file, one job. The assembly links to them. Change a part, "
               "the assembly updates.")]), """
<h3>What that buys you</h3>
%s
%s
""" % (ticks([
    "A 9-tyne machine becomes an 11-tyne machine by editing one cell.",
    "The blade bent on R10 becomes the blade bent on R16 by editing one cell — which is "
    "exactly what the source tutorial does by hand in SolidWorks.",
    "Mass comes out of the model, so you can check the tractor can lift it before you "
    "cut any steel.",
    "Mistakes are cheap. A wrong number is a wrong number, not a wrong shape."]),
       note("<strong>The discipline is the lesson.</strong> Anyone can push geometry "
            "around until it looks right. An engineer builds a model that stays right "
            "when the requirements change."))),
            eyebrow="How we work")

    d.sheet("05", "SOURCE", "PROVENANCE", "Where the design comes from", """
<p class="lede">This course follows a SolidWorks tutorial by <em>Malviya CAD Solution</em>,
&ldquo;Design of Cultivator in SolidWorks | Nine tines cultivator&rdquo;. The original
narration is in Hindi; we worked from a machine translation.</p>
%s
""" % cols("""
<h3>The translation problem</h3>
<p>Machine translation of spoken technical Hindi garbles numbers. The transcript says the
frame's <em>&ldquo;hole size is 12.5&rdquo;</em> in one sentence and
<em>&ldquo;the hole size is 3 inches&rdquo;</em> two sentences later. Neither is a hole
diameter — the first is a mistranscription, the second is the <strong>spacing</strong>
between a pair of holes.</p>
<p>So this is not a transcription exercise. At each step we read what the tutorial is
doing, check it against what the machine has to do mechanically, and then commit to a
number — stating the assumption on the slide.</p>
%s
""" % warn("<strong>Every assumption is flagged.</strong> Where a slide says "
           "<em>assumption</em>, the number is our engineering judgement, not the "
           "source's. You are free to disagree — and because the model is parametric, "
           "disagreeing costs one cell edit."), """
<h3>Worked example: the frame holes</h3>
<p>The transcript says: <em>&ldquo;There is one hole here and another hole here&rdquo;</em>,
then <em>&ldquo;the hole size is 3 inches&rdquo;</em>, then <em>&ldquo;the distance is
9.5 inches, we need 9 patterns&rdquo;</em>.</p>
%s
<p>The tyne, five minutes later in the same video, gets <em>&ldquo;two holes 0.5 inches,
3 inches apart&rdquo;</em>. The two readings lock together: the frame's hole pairs are
what the tyne's bolts pass through. Read either one alone and you would get it wrong.</p>
""" % steps([("Two holes, not one — so each tyne station is a <strong>pair</strong>", ""),
             ("&ldquo;3 inches&rdquo; is the spacing between that pair, not a diameter", ""),
             ("The pair is patterned nine times at 9.5 in", ""),
             ("The whole lot is mirrored to the rear bar", "")], compact=True)),
            eyebrow="Reading a rough translation")

    d.sheet("06", "COURSE", "MAP", "The fourteen decks", """
<p class="lede">Decks 2 to 4 teach you FreeCAD. Decks 5 to 9 build the parts.
Decks 10 to 14 put the machine together and make it work for you.</p>
%s
""" % cols(tbl(["#", "Deck", "What you learn"],
               [["2", "The FreeCAD interface", "The window, the tree, the workbenches, the vocabulary"],
                ["3", "Setting up", "Units, documents, the Body, the origin planes"],
                ["4", "Sketching &amp; constraints", "Geometric vs dimensional; what <em>fully constrained</em> means"],
                ["5", "Part 1 — Frame", "Pad, pocket, linear pattern, mirror, fillet, spreadsheet"],
                ["6", "Part 2 — Tine 01", "Arcs, tangency, and why angle constraints bite"],
                ["7", "Part 3 — Tine 02", "One clean sweep; deriving a sweep angle"]]),
           tbl(["#", "Deck", "What you learn"],
               [["8", "Parts 4–5 — Clamps", "Additive Pipe: FreeCAD's answer to Weldments"],
                ["9", "Parts 6–7 — Blades", "Replacing SolidWorks Flex with real geometry"],
                ["10", "Assembly", "Links, placement, joints"],
                ["11", "Patterns &amp; fasteners", "Link arrays, and what PartDesign will not do"],
                ["12", "Appearance &amp; drawings", "Materials, rendering, TechDraw"],
                ["13", "Making it parametric", "Driving the whole machine from one table"],
                ["14", "Summary &amp; exercises", "Twelve exercises, from easy to hard"]])),
            eyebrow="Where this goes")

    d.sheet("07", "SETUP", "CHECKLIST", "Before you start", """
<p class="lede">You need FreeCAD 1.1 or later. It is free, it runs on Windows, macOS and
Linux, and nothing in this course needs a paid add-on.</p>
%s
""" % cols("""
<h3>Install and check</h3>
%s
""" % steps([("Download FreeCAD 1.1 from <code>freecad.org</code> and install it", ""),
             ("Open it. You should land on the Start page", ""),
             ("Check the version under <strong>Help ▸ About FreeCAD</strong> — this "
              "course was written against <strong>1.1.3</strong>", ""),
             ("Set the units to imperial decimal (Deck 3 shows you where)", ""),
             ("Make a folder for the job — one file per part", "")]), """
<h3>What you should already know</h3>
%s
<h3>How long it takes</h3>
%s
""" % (ticks([
    "Basic engineering drawing — plan, elevation, section",
    "What a tyne, a sweep and a three-point linkage are",
    "No CAD experience is assumed. None at all."]),
       specs([("Decks 2–4", "≈ 2 hours"), ("Parts 1–3", "≈ 4 hours"),
              ("Parts 4–7", "≈ 3 hours"), ("Assembly &amp; rest", "≈ 3 hours"),
              ("Total", "≈ 12 hours")]))),
            eyebrow="Getting ready")

    return d
