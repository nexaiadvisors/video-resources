#!/usr/bin/env bash
# Turn two clips (listening + talking) of the same person into seamless web loops,
# a poster frame and contact sheets for review.
# Usage: make-loops.sh <listening.mp4> <talking.mp4> <out-dir>
# Needs: ffmpeg.
set -euo pipefail
IDLE="${1:?listening clip}"; TALK="${2:?talking clip}"; OUT="${3:?output dir}"
mkdir -p "$OUT"
for pair in "idle:$IDLE" "talk:$TALK"; do
  k="${pair%%:*}"; src="${pair#*:}"
  # Forward then reverse: the last frame equals the first, so the loop has no visible jump.
  ffmpeg -loglevel error -y -i "$src" -filter_complex \
    "[0:v]scale=1280:-2,fps=30,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,format=yuv420p" \
    -an -c:v libx264 -crf 26 -preset slow -movflags +faststart "$OUT/avatar-$k.mp4"
  ffmpeg -loglevel error -y -i "$src" -vf "fps=1,scale=480:-1,tile=4x2" -frames:v 1 "$OUT/$k-sheet.jpg"
done
ffmpeg -loglevel error -y -i "$OUT/avatar-idle.mp4" -frames:v 1 -q:v 3 "$OUT/avatar-poster.jpg"
ls -la "$OUT"
