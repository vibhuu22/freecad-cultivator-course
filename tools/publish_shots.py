# -*- coding: utf-8 -*-
"""Put the deck screenshots somewhere Canva's servers can fetch them.

Canva's "upload asset from URL" can only read a file that is already on the
public internet.  These screenshots are local, so they have to be published
before Canva can pull them in.

This uploads to **litterbox**, which deletes everything after 72 hours.  That
is deliberate: Canva copies each image into your Canva account at upload time,
so the temporary link only has to survive the next few minutes.  After three
days nothing is left on the host.

    python tools\\publish_shots.py            # only the images the decks use
    python tools\\publish_shots.py --all      # every screenshot

Writes tools/shot_urls.json, which maps screenshot name -> public URL.

BE AWARE: while the links are alive, anyone who guesses one can see the image.
These are FreeCAD screenshots of a teaching model, but read that sentence again
before running this on anything confidential.
"""
import os, sys, json, glob, subprocess, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOTS = os.path.join(ROOT, "screenshots")
OUT = os.path.join(HERE, "shot_urls.json")
ENDPOINT = "https://litterbox.catbox.moe/resources/internals/api.php"


def used_by_decks():
    """Screenshot names actually referenced by the deck modules."""
    names = set()
    pat = re.compile(r'(?:shot|strip)\(\s*"([^"]+)"')
    for path in glob.glob(os.path.join(HERE, "decks", "d??_*.py")):
        with open(path, encoding="utf-8") as f:
            src = f.read()
        names.update(pat.findall(src))
        # the (name, caption) tuples inside shots([...])
        for block in re.findall(r'shots\(\[(.*?)\]\s*[,)]', src, re.S):
            names.update(re.findall(r'\(\s*"([^"]+)"', block))
    return sorted(n for n in names
                  if os.path.exists(os.path.join(SHOTS, n + ".png")))


def upload(path, tries=4):
    """Upload one file, retrying with back-off.

    The host rate-limits a fast run of uploads and answers with an error body
    instead of a URL, so a single attempt is not enough.
    """
    last = ""
    for attempt in range(tries):
        cmd = ["curl", "-s", "--max-time", "120",
               "-F", "reqtype=fileupload",
               "-F", "time=72h",
               "-F", "fileToUpload=@" + path,
               ENDPOINT]
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = (res.stdout or "").strip()
        if out.startswith("http"):
            return out, ""
        last = out or (res.stderr or "").strip() or "empty reply"
        time.sleep(3 * (attempt + 1))
    return None, last[:110]


def main():
    names = ([os.path.basename(p)[:-4] for p in
              sorted(glob.glob(os.path.join(SHOTS, "*.png")))]
             if "--all" in sys.argv else used_by_decks())

    print("Publishing %d screenshots to litterbox (they expire in 72 hours)." % len(names))
    print("Anyone with a link can view it until then. Ctrl+C now if that is not OK.\n")

    urls = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            urls = json.load(f)

    for i, name in enumerate(names, 1):
        if name in urls:
            print("  %3d/%d  %-42s already done" % (i, len(names), name))
            continue
        path = os.path.join(SHOTS, name + ".png")
        url, err = upload(path)
        if url:
            urls[name] = url
            print("  %3d/%d  %-42s %s" % (i, len(names), name, url))
        else:
            print("  %3d/%d  %-42s FAILED  %s" % (i, len(names), name, err))
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(urls, f, indent=1, sort_keys=True)
        time.sleep(2.0)          # be gentle; the host throttles fast runs

    done = sum(1 for n in names if n in urls)
    print("\n%d of %d uploaded. Map written to %s" % (done, len(names), OUT))
    if done < len(names):
        print("Run it again - it skips what is already done and retries the rest.")


if __name__ == "__main__":
    main()
