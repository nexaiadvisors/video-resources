"""Word start times of a voice file, for placing gestures (talk_longcat.py).

Run it with:
    uv run -q --with mlx-whisper python word_times.py VOICE.wav words.json
Writes {"text": ..., "words": [{"w": word, "s": start, "e": end}, ...]}.
"""
import json
import sys

import mlx_whisper

wav, out = sys.argv[1], sys.argv[2]
r = mlx_whisper.transcribe(wav, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", word_timestamps=True)
words = [{"w": w["word"].strip(), "s": float(w["start"]), "e": float(w["end"])}
         for s in r["segments"] for w in s["words"]]
json.dump({"text": r["text"].strip(), "words": words}, open(out, "w"), indent=1)
print(f"{len(words)} words")
