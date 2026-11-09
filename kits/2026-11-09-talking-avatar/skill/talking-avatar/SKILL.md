---
name: talking-avatar
description: "Adds a free animated talking avatar to a web voice or chat app from one portrait: two looping clips (listening, talking) of the same person, swapped in the browser while the AI voice plays. No real-time lip sync, no per-minute cost. Use for 'talking avatar', 'animate the portrait', 'make my AI character talk on screen', 'avatar for my voice/chat agent'."
argument-hint: "[portrait image path] [app repo path]"
---

# Talking Avatar

## Overview

Turns one still portrait into a character that looks like it talks whenever
the AI voice is playing.

The trick: do not sync lips to words. Make a **listening** loop and a
**talking** loop of the same person once, and cross-fade between them on the
AI audio level. Real-time lip sync is slow, costs money every minute and often
looks off. This costs nothing per call, adds no delay, and reads as "talking".

---

## Steps

### 1. Check the portrait

Input: one portrait (landscape 16:9 works best, face in the middle third) and
the app repo. Note the person's gender presentation; the voice must match it
(step 5).
Accept when: the portrait is the image the app should show.

### 2. Generate two clips of the same person

Use any image-to-video model that takes the portrait as a reference. The
author uses Google Vids (Omni model, included with a Google AI plan): add the
portrait as an image ingredient and generate two 8-second clips:

- Listening: "Image1 exactly: the same person, same clothes, same background,
  same framing. Locked-off static camera, no zoom, no cuts. They are on a video
  call, LISTENING silently: mouth closed with a slight friendly smile, natural
  blinks, small attentive nods. No speech, no hand gestures, nothing else moves."
- Talking: the same, but "TALKING to the viewer in a calm, friendly tone: mouth
  moving naturally as they speak, natural blinks, small head movements."

Then run `scripts/make-loops.sh <listening.mp4> <talking.mp4> <out-dir>`. It
plays each clip forward then backward (so the loop has no jump), makes 720p
H.264 with no audio (about 1.5 MB each), a poster frame, and a contact sheet
per clip.

Accept when: you have looked at both contact sheets: same face as the
portrait, same clothes and background, the camera did not move, mouth closed
in every listening frame and visibly moving in the talking frames, no extra
hands or text. Regenerate a clip that fails.

### 3. Add the assets to the app

Copy `avatar-idle.mp4`, `avatar-talk.mp4`, `avatar-poster.jpg` and the original
still into the app's static folder. Keep the avatar paths and the voice name
in ONE config file, so swapping the portrait later changes them together.
Accept when: the files load at the paths the config names.

### 4. Switch on the AI voice

Read [browser player](references/browser-player.md). Wire the app's "AI is
speaking" signal (or the level meter in that file) to the player: both videos
autoplay muted and loop; the talking one is visible while the level is above
about 0.01, held 400 ms through gaps; a clip error falls back to the still.
Accept when: the build passes.

### 5. Match the voice to the face

Pick the TTS or realtime voice from the portrait's gender in the same config
(OpenAI Realtime: male `cedar`, female `marin`) and send it on every call. A
male face with a female voice is the first thing users notice.
Accept when: the call uses the matching voice.

### 6. Prove it in a real call

Start a real call. If you cannot click the mic prompt in an automated test,
replace `navigator.mediaDevices.getUserMedia` in the page with a quiet
oscillator stream (test only). Sample every 500 ms which `<video>` is visible.
Accept when: the talking clip shows while the AI speaks and the listening clip
after it stops, and nothing falls back to the still.

---

## Limits

- The mouth moves like speech but does not match the exact words. Do not call it lip sync.
- Generated clips may carry the provider's AI-content marks; follow your provider's terms.
