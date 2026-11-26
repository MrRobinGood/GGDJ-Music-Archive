"""Save the track list of every playlist in the archive to docs/tracks.json.

It reads the playlist ids from docs/index.html and asks Spotify's public
embed page for each one. No Spotify account or key is needed.
"""
import json, re, sys, time, urllib.request

html = open("docs/index.html", encoding="utf-8").read()
data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1))

out = {}
for p in data:
    pid = p["id"]
    req = urllib.request.Request(
        f"https://open.spotify.com/embed/playlist/{pid}",
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"},
    )
    try:
        page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
        nd = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S).group(1))
        ent = nd["props"]["pageProps"]["state"]["data"]["entity"]
        out[pid] = {
            "title": p["title"],
            "tracks": [
                {"title": t["title"], "artists": t["subtitle"], "seconds": round(t["duration"] / 1000), "id": t["uri"].split(":")[-1]}
                for t in ent["trackList"]
            ],
        }
        print(pid, len(out[pid]["tracks"]))
    except Exception as e:
        print(pid, "FAILED", e, file=sys.stderr)
    time.sleep(1)

if len(out) < len(data) * 0.9:
    sys.exit(f"Only {len(out)} of {len(data)} playlists answered. Keeping the old file.")

json.dump(out, open("docs/tracks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(out), "playlists,", sum(len(v["tracks"]) for v in out.values()), "tracks")
