# Reference photos for a weapon, from Wikimedia Commons (free-licence pictures), saved small enough to look at.
#   python tools/ref_photos.py "<search words>" <how many> <out folder> [--min-width 600]
# Writes the pictures plus SOURCES.tsv (file page, author line, licence) so every picture can be credited.
# Tefa, 2026-11-02: "really dig into weapon images online to have a knowledge of little things like screws, cavities,
# scratches, how the stocks look, where the hammers sit". Pictures stay on the PC / MEGA, never in git.
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ashes-2063-weapons reference fetch (github.com/TefMeister)"}
WIDTH = 900


def fetch(url):
    """Polite download: a pause before each request, and on 429 wait as told (or longer each time) and retry."""
    for attempt in range(6):
        time.sleep(1.5)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(float(e.headers.get("Retry-After") or 0) or 5 * (attempt + 1))


def get(params):
    return json.loads(fetch(API + "?" + urllib.parse.urlencode(dict(params, format="json"))))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    query, count, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    min_w = int(sys.argv[sys.argv.index("--min-width") + 1]) if "--min-width" in sys.argv else 600
    os.makedirs(out, exist_ok=True)
    hits = get({"action": "query", "list": "search", "srnamespace": 6, "srsearch": query, "srlimit": 50})
    titles = [h["title"] for h in hits["query"]["search"] if re.search(r"\.(jpe?g|png)$", h["title"], re.I)]
    rows, n = [], 0
    for i in range(0, len(titles), 20):
        info = get({"action": "query", "titles": "|".join(titles[i:i + 20]), "prop": "imageinfo",
                    "iiprop": "url|size|extmetadata", "iiurlwidth": WIDTH})
        for page in info["query"]["pages"].values():
            if n >= count or "imageinfo" not in page:
                continue
            ii = page["imageinfo"][0]
            if ii.get("width", 0) < min_w:
                continue
            meta = ii.get("extmetadata", {})
            artist = re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
            lic = meta.get("LicenseShortName", {}).get("value", "")
            name = re.sub(r"[^\w.-]+", "_", page["title"][5:])[:80]
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                name += ".jpg"
            path = os.path.join(out, name)
            if not os.path.exists(path):
                open(path, "wb").write(fetch(ii["thumburl"]))
            rows.append((name, ii["descriptionurl"], artist, lic))
            n += 1
    with open(os.path.join(out, "SOURCES.tsv"), "a", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")
    for r in rows:
        print(r[0], "|", r[3], "|", r[2][:40])


if __name__ == "__main__":
    main()
