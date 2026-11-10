#!/usr/bin/env python3
"""How fresh is a NotebookLM notebook of YouTube videos?

  freshness.py --notebook <id> [--days 7] [--out file.json]

Reads the notebook's sources with the `nlm` CLI (notebooklm-mcp-cli), looks up each
video's upload date and channel, and prints JSON: video_count, newest_published,
fresh (any video inside --days), recent (those videos) and creators (channels by
video count). Nothing is written to the notebook.

Upload dates come from the YouTube Data API when YOUTUBE_API_KEY is set (free key,
about 1 quota unit per 50 videos), otherwise from yt-dlp (no key, slower).
"""
import argparse, datetime as dt, json, os, re, subprocess, sys, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

VID = re.compile(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})")


def via_api(ids, key):
    out = []
    for i in range(0, len(ids), 50):
        q = urllib.parse.urlencode({"part": "snippet,statistics", "id": ",".join(ids[i:i + 50]), "key": key})
        with urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/videos?{q}", timeout=60) as r:
            for it in json.load(r).get("items", []):
                s = it["snippet"]
                out.append({"id": it["id"], "title": s["title"], "channel": s["channelTitle"],
                            "published": s["publishedAt"], "views": int(it.get("statistics", {}).get("viewCount", 0))})
    return out


def via_ytdlp(ids):
    out = []
    for vid in ids:
        r = subprocess.run(["yt-dlp", "--skip-download", "--no-warnings", "--print",
                            "%(title)s\t%(channel)s\t%(upload_date)s\t%(view_count)s",
                            f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=120)
        if r.returncode or not r.stdout.strip():
            continue
        title, channel, day, views = r.stdout.strip().split("\t")
        out.append({"id": vid, "title": title, "channel": channel,
                    "published": f"{day[:4]}-{day[4:6]}-{day[6:]}T00:00:00Z",
                    "views": int(views) if views.isdigit() else 0})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--notebook", required=True)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    src = subprocess.run(["nlm", "source", "list", a.notebook, "--json"], capture_output=True, text=True, timeout=180)
    if src.returncode:
        print(json.dumps({"ok": False, "error": f"nlm source list: {src.stderr.strip()[-300:]}"}))
        return 2
    sources = json.loads(src.stdout)
    ids = sorted({m.group(1) for s in sources for m in [VID.search(s.get("url") or "")] if m})
    key = os.environ.get("YOUTUBE_API_KEY")
    videos = (via_api(ids, key) if key else via_ytdlp(ids)) if ids else []

    now = dt.datetime.now(dt.timezone.utc)
    pub = lambda v: dt.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))  # noqa: E731
    recent = sorted([v for v in videos if pub(v) >= now - dt.timedelta(days=a.days)], key=pub, reverse=True)
    newest = max(videos, key=pub) if videos else None
    by = defaultdict(list)
    for v in videos:
        by[v["channel"]].append(v)
    creators = sorted(({"channel": c, "videos": len(vs), "newest": max(pub(v) for v in vs).date().isoformat(),
                        "views_total": sum(v["views"] for v in vs)} for c, vs in by.items()),
                      key=lambda c: (-c["videos"], -c["views_total"]))
    report = {
        "ok": True, "notebook": a.notebook, "checked_at": now.isoformat(timespec="seconds"),
        "date_source": "youtube-api" if key else "yt-dlp", "window_days": a.days,
        "source_count": len(sources), "video_count": len(videos),
        "newest_published": pub(newest).isoformat() if newest else None,
        "fresh": bool(recent),
        "recent": [{"title": v["title"], "channel": v["channel"], "published": v["published"],
                    "url": f"https://www.youtube.com/watch?v={v['id']}"} for v in recent],
        "creators": creators,
    }
    text = json.dumps(report, indent=2)
    if a.out:
        Path(a.out).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
