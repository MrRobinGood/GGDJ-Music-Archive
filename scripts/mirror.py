"""Copy robingood.com/music into docs/ and keep a full-size copy of every cover.

Runs on GitHub every week. robingood.com is the main site. This repository is
the safe twin: if robingood.com ever disappears, docs/ still has the whole
archive, with its own covers, published by GitHub Pages.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image

SITE = "https://robingood.com/music/"
DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
UA = {"User-Agent": "GGDJ-Music-Archive-mirror/1.0"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / "covers").mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)

    html = get(SITE + "index.html").decode("utf-8")
    sources = json.loads(get(SITE + "cover-sources.json"))
    (DOCS / "cover-sources.json").write_text(json.dumps(sources, indent=0))
    (DOCS / "assets" / "wordmark.svg").write_bytes(get(SITE + "assets/wordmark.svg"))

    ok, failed = 0, []
    for pid, urls in sources.items():
        out = DOCS / "covers" / f"{pid}.jpg"
        try:
            if len(urls) == 1:
                img = Image.open(io.BytesIO(get(urls[0]))).convert("RGB")
                img = img.resize((640, 640)) if img.size != (640, 640) else img
            else:
                img = Image.new("RGB", (600, 600))
                for i, u in enumerate(urls[:4]):
                    tile = Image.open(io.BytesIO(get(u))).convert("RGB").resize((300, 300))
                    img.paste(tile, ((i % 2) * 300, (i // 2) * 300))
            img.save(out, quality=86)
            ok += 1
        except Exception as e:  # keep the old cover if Spotify fails
            failed.append(pid)
            if not out.exists():
                try:
                    out.write_bytes(get(SITE + f"covers/{pid}.jpg"))
                except Exception:
                    pass
            print("cover problem", pid, e, file=sys.stderr)

    # In this copy the covers come from our own folder, never from Spotify.
    html = html.replace(
        "esc(p.big || ('covers/' + p.id + '.jpg'))",
        "esc('covers/' + p.id + '.jpg')",
    )
    note = '<!-- Copy of https://robingood.com/music/ kept on GitHub by Robin Good. -->\n'
    (DOCS / "index.html").write_text(note + html, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")
    print(f"covers saved: {ok}, problems: {len(failed)}")


if __name__ == "__main__":
    main()
