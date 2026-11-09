---
name: talking-avatar
description: "Adds a free animated talking avatar to a web voice or chat app from one portrait: a few image edits of the same face (mouth shapes, blink, glances) pre-rendered into small cut-outs, then drawn on a canvas and driven by the AI voice volume. No lip-sync model, no video, no per-minute cost. Use for 'talking avatar', 'animate the portrait', 'make the interviewer/character talk', 'avatar for my chat/voice agent'."
argument-hint: "[portrait image path] [app repo path]"
---

# Talking Avatar

## Overview

Turns one still portrait into a face that talks while the AI voice plays: mouth eases open and
shut with the volume, changes shape, blinks, glances in pauses, sways a little. Built for an
AI buyer persona in a pitch-practice app (2026-11-09).

Why this method (from 15 rounds, each scored by a fresh AI reviewer):
- Real-time lip-sync models were slow and costly; two video loops (listening/talking) made the
  head JUMP on every switch, because each clip moves the head differently.
- Stills of ONE frame where only the mouth or eyes differ keep the head identical, so switching
  never jumps. Best cold-read score: 7/10 (timing 8, smoothness 8). The ceiling is the teeth
  detail and exact m/b/p closures; going past ~7 needs a per-frame lip-sync model. Say so.

## Steps

### 1. Check the portrait
Input: a front-facing portrait (landscape 16:9 works best), the app repo.
Note the person's gender presentation: the voice must match it (step 6).
Accept when: `scripts/face.py`'s face detector finds the face (paste.py fails loudly if not).

### 2. Make the sprites
Read [sprite prompts](references/sprite-prompts.md). Make the neutral base first, then each mouth
edit from it, then blink and two glances. Paste each with
`python3 scripts/paste.py <base> <edit> <mouth|eyes> s-<name>.jpg`.
Accept when: you have looked at face crops of all sprites and the blink is fully shut, nothing
outside the mouth or eyes changed, and the base is not smiling.

### 3. Build the atlas
`python3 scripts/finish_sprites.py <dir>` (sharpens edits to the photo's detail level), then
`python3 scripts/make_atlas.py <dir> <dir>/atlas`. It pre-renders 4 mouth shapes x 5 openings
(optical-flow in-betweens, so openings are continuous, not two images cross-faded) plus blink and
glance steps, as cut-outs with alpha, and `manifest.json`. Convert PNGs to webp for the web
(about 0.5 MB total).
Accept when: 20 mouth and 9-12 eye files exist.

### 4. Add the player
Copy `scripts/talkingAvatar.ts` into the app. Call
`startTalkingAvatar(canvas, { baseUrl, getLevel })`, where `getLevel()` returns the
AI voice RMS (Web Audio analyser on the remote stream, about 0..0.3). In React, keep `getLevel` in a
ref updated in an effect (eslint `react-hooks/refs`), and show the plain still if it throws.
Accept when: build and lint pass.

### 5. Prove it
Serve `scripts/demo.html` next to `ta.js` (esbuild bundle of the player, `--global-name=TA`),
`atlas/` and a `voice.wav`, then `node scripts/record_demo.cjs out.webm` (Playwright + system Chrome,
autoplay allowed). It records the canvas plus the voice with MediaRecorder: the real player, not a
re-creation. Convert to mp4. Then have a fresh agent with no context cold-read it
(score 1-10, defects with timestamps).
Accept when: mouth moves with speech and is still in pauses, blinks happen, no head jumps;
report the score honestly.

### 6. Match the voice to the face
Pick the voice from the portrait's gender in the same config as the atlas path (OpenAI Realtime:
male `cedar`, female `marin`).
Accept when: the call uses the matching voice.

## Demo rules
- A demo must show THIS technique: the player driven by a voice. Never a generated video where
  the model made the voice and lips together.

## Limits
- Mouth shapes are not tied to exact words in the live player (it picks shapes at syllable dips).
  An offline demo can drive shapes from word timings, but say which one you show.
- Teeth are soft and m/b/p closures are approximate; do not call it lip sync.
