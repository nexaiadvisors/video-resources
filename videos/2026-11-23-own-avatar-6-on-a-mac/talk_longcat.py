#!/usr/bin/env python3
"""Talking-avatar video from one photo and one voice file, with hand gestures placed on chosen words.

Uses LongCat-Video-Avatar 1.6 through the community MLX port (see SETUP.md). Apple silicon, 64 GB of memory or more.

    python3 talk_longcat.py LOOK.jpg VOICE.wav PROMPT.txt OUT.mp4 [--cues CUES.txt] [--seed 42] [--lead 0.2] [--size HxW]

PROMPT.txt: describe the person and setting, then how they talk. Mark where the hand sentence goes with
{GESTURE|resting text}:
    ... calm, confident way. {GESTURE|His hands rest loosely on his lap.} Natural head movements ...
  Normal segments use the resting text. A gesture segment uses the cue's gesture sentence in that place.
CUES.txt: one cue per line, `phrase | gesture sentence`. The phrase is matched in the spoken words, in order.
  `@7.4 | gesture sentence` gives a time in seconds instead of a phrase.
  Add `| seed=7` to a line to render that one gesture with its own seed (hand shapes depend on the seed).

Why it works this way: a video model performs a prompted action at the START of a generation. A gesture prompt on a
segment that continues earlier frames is ignored. A segment started fresh from one still frame obeys it, and the
gesture lands about 0.5 s after that frame. So each gesture segment starts fresh from the frame just before the
word; everything else continues from the previous 13 frames.

Set LONGCAT_CODE (the port's folder) and LONGCAT_WEIGHTS (the converted weights folder) if yours differ from the
defaults below.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

FPS, SEG, COND = 25, 93, 13          # LongCat: 25 fps, 93-frame segments, continues from the last 13 frames
MIN_GAP = 25                          # frames of normal talking required before the first gesture and after the last
MIN_GESTURE = 63                      # a gesture segment keeps at least this many frames (2.5 s) before the next cue
HOME = pathlib.Path.home()
CODE = pathlib.Path(os.environ.get("LONGCAT_CODE", HOME / "longcat-avatar-mlx"))
WEIGHTS = pathlib.Path(os.environ.get("LONGCAT_WEIGHTS",
                                      HOME / "models/LongCat-Video-Avatar-1.6-bf16"))
HERE = pathlib.Path(__file__).resolve().parent
os.environ["PATH"] = f"/opt/homebrew/bin:{HOME}/.local/bin:" + os.environ.get("PATH", "")


def run(cmd, log=None, **kw):
    out = open(log, "w") if log else None
    r = subprocess.run([str(c) for c in cmd], stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT if out else None, **kw)
    if r.returncode != 0:
        sys.exit(f"FAILED rc={r.returncode}: {' '.join(str(c) for c in cmd[:6])} ... (log: {log})")


def probe(path, entries, stream=True):
    cmd = ["ffprobe", "-v", "error"] + (["-select_streams", "v:0", "-count_frames"] if stream else []) + \
          ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


def norm(word):
    return re.sub(r"[^a-z0-9']", "", word.lower())


def cue_frames(cues, words, lead, total):
    """Each cue -> the frame where its gesture segment starts (phrase start minus `lead` seconds)."""
    toks, out, i0 = [norm(w["w"]) for w in words], [], 0
    for phrase, gesture, seed in cues:
        if phrase.startswith("@"):
            t = float(phrase[1:])
        else:
            want = [norm(p) for p in phrase.split() if norm(p)]
            hit = next((i for i in range(i0, len(toks) - len(want) + 1) if toks[i:i + len(want)] == want), None)
            if hit is None:
                sys.exit(f'cue phrase "{phrase}" not found in the voice after word {i0}. Spoken: '
                         + " ".join(w["w"] for w in words))
            t, i0 = words[hit]["s"] - lead, hit + len(want)
        out.append((max(0, round(t * FPS)), phrase, gesture, seed))
    prev = None
    for nb, phrase, *_ in out:
        if prev is None and nb < MIN_GAP:
            sys.exit(f'cue "{phrase}" at {nb / FPS:.2f}s is too close to the start (needs {MIN_GAP / FPS:.1f}s of talking first)')
        if prev is not None and nb - prev < MIN_GESTURE:
            sys.exit(f'cue "{phrase}" at {nb / FPS:.2f}s is less than {MIN_GESTURE / FPS:.1f}s after the previous cue '
                     f"at {prev / FPS:.2f}s")
        if nb >= total - MIN_GAP:
            sys.exit(f'cue "{phrase}" at {nb / FPS:.2f}s is too close to the end ({total / FPS:.2f}s)')
        prev = nb
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("look"); ap.add_argument("voice"); ap.add_argument("prompt"); ap.add_argument("out")
    ap.add_argument("--cues"); ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--lead", type=float, default=0.2, help="seconds before the phrase that the gesture segment starts")
    ap.add_argument("--resolution", choices=["480p", "720p"], default="480p")
    ap.add_argument("--size", help="explicit HxW in multiples of 32, e.g. 480x864 for widescreen (default: fitted to the look)")
    a = ap.parse_args()
    look, voice, out = (pathlib.Path(p).expanduser().resolve() for p in (a.look, a.voice, a.out))
    W = out.parent / f"lc-{out.stem}"; W.mkdir(parents=True, exist_ok=True)
    status = W / "status.txt"; status.write_text("")

    def note(msg):
        print(msg, flush=True)
        with open(status, "a") as f:
            f.write(msg + "\n")

    run(["ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-c:a", "pcm_s16le", W / "voice.wav"])
    total = round(float(probe(W / "voice.wav", "format=duration", stream=False)) * FPS)
    text = pathlib.Path(a.prompt).read_text().strip()
    slot = re.compile(r"\{GESTURE(?:\|([^}]*))?\}")
    rest_prompt = re.sub(r"\s+", " ", slot.sub(lambda m: m.group(1) or "", text)).strip()

    def gesture_prompt(g):
        return re.sub(r"\s+", " ", slot.sub(lambda m: g, text) if slot.search(text) else f"{text} {g}").strip()

    cues = []
    if a.cues:
        lines = [l.strip() for l in pathlib.Path(a.cues).read_text().splitlines() if l.strip() and not l.startswith("#")]
        for l in lines:
            parts = [x.strip() for x in l.split("|")]
            seed = next((int(x[5:]) for x in parts[2:] if x.startswith("seed=")), None)
            cues.append((parts[0], parts[1], seed))
    words = []
    if any(not c[0].startswith("@") for c in cues):
        env = dict(os.environ)
        run(["uv", "run", "-q", "--with", "mlx-whisper", "python", HERE / "word_times.py", voice, W / "words.json"],
            log=W / "words.log", env=env)
        words = json.loads((W / "words.json").read_text())["words"]
    placed = cue_frames(cues, words, a.lead, total)
    for nb, phrase, *_ in placed:
        note(f'cue "{phrase}": gesture segment starts at {nb / FPS:.2f}s (frame {nb})')

    # Plan: (kind, first frame, frames to render, frames to keep, prompt). A part that is followed by a gesture renders
    # one extra frame: that frame is the still the gesture segment starts from. A gesture segment is cut short when
    # the next cue comes before its 93 frames end; the next gesture then starts from its frame at that cue.
    plan, c = [], 0
    for j, (nb, _, g, cseed) in enumerate(placed):
        if nb > c or not plan:
            plan.append(("talk", c, nb - c + 1, nb - c, rest_prompt, None))
        nxt = placed[j + 1][0] if j + 1 < len(placed) else None
        n = min(SEG, total - nb)
        if nxt is not None and nxt - nb < SEG:
            plan.append(("gesture", nb, nxt - nb + 1, nxt - nb, gesture_prompt(g), cseed))
            c = nxt
        else:
            plan.append(("gesture", nb, n, n, gesture_prompt(g), cseed))
            c = nb + n
    if c < total:
        plan.append(("talk", c, total - c, total - c, rest_prompt, None))

    size, prev, parts = a.size, None, []
    for i, (kind, first, n, keep, prompt, pseed) in enumerate(plan):
        p = W / f"p{i}-{kind}.mp4"
        (W / f"p{i}.txt").write_text(prompt)
        aud = W / f"p{i}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{first / FPS:.3f}", "-i", W / "voice.wav", "-c:a", "pcm_s16le", aud])
        cmd = [CODE / ".venv/bin/python", "scripts/generate.py", "--weights", WEIGHTS, "--audio", aud, "--prompt", W / f"p{i}.txt",
               "--duration", f"{n / FPS:.3f}", "--seed", a.seed if pseed is None else pseed, "--resolution", a.resolution, "--out", p]
        if size:
            cmd += ["--size", size]
        if kind == "gesture":             # fresh start from the single frame at the cue
            still = W / f"p{i}-still.png"
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", prev[0], "-vf", f"select=eq(n\\,{prev[1] - 1})", "-frames:v", "1", still])
            cmd += ["--image", still]
        elif prev:                        # continue from the last 13 frames of the previous part
            cmd += ["--image", look, "--start-video", prev[0], "--start-at", f"{(prev[1] - COND) / FPS:.3f}"]
        else:
            cmd += ["--image", look]
        run(cmd, log=W / f"p{i}.log", cwd=CODE)
        got = int(probe(p, "stream=nb_read_frames"))
        if got != n:
            sys.exit(f"part {i} has {got} frames, expected {n}")
        if not size:
            w, h = probe(p, "stream=width,height").split("\n")[0].split(",")[:2]
            size = f"{h}x{w}"
        note(f"part {i} {kind} {first / FPS:.2f}-{(first + keep) / FPS:.2f}s ok")
        parts.append((p, keep))
        prev = (p, n)

    ins, chain = [], ""
    for i, (p, keep) in enumerate(parts):
        ins += ["-i", p]
        chain += f"[{i}:v]trim=end_frame={keep},setpts=PTS-STARTPTS[v{i}];"
    chain += "".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v]"
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", voice, "-filter_complex", chain, "-map", "[v]",
         "-map", f"{len(parts)}:a", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    got = int(probe(out, "stream=nb_read_frames"))
    note(f"done {out} frames={got} expected={total} size={size}")
    if abs(got - total) > 1:
        sys.exit("frame count mismatch")


if __name__ == "__main__":
    main()
