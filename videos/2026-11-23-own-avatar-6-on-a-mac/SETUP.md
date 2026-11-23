# Setup

## What you need

- A Mac with Apple silicon and at least 64 GB of memory.
- About 80 GB of free disk for the model files.
- `ffmpeg`, `git` and `uv` (`brew install ffmpeg uv`).
- One photo of the person (whole head in frame, no text on clothing) and one voice file (`.wav`).

## 1. Get the Mac port

Version 1.6 support lives in a pull request that was still open when this was written (2026-11-23). We used this exact commit:

```bash
git clone https://github.com/fedeinfe/longcat-avatar-mlx ~/longcat-avatar-mlx
cd ~/longcat-avatar-mlx
git fetch origin feat/avatar-1.6-continuation-lora
git checkout 2ab5b417473aea7fb9fbbb7323fdb94831132de0
uv venv --python 3.12 .venv
uv pip install -e ".[parity]" librosa pyloudnorm pillow ftfy imageio imageio-ffmpeg
```

Read code before you run it. If the pull request has been merged into https://github.com/xocialize/longcat-avatar-mlx by the time you read this, use that repo instead.

## 2. Get the weights

Download the official model from https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6 and follow the port's README to convert it for MLX. The port's `recipes/convert_dit` turns the official `base_model` into the MLX format, and the two LoRA files (`loraA`, `loraB`) go in a `lora/` folder next to it. The port's README is the authority for the folder layout.

**Do not run 1.6 weights with code for version 1.5.** It runs without an error, ignores your photo and gives cartoon colours.

## 3. Point the script at them

```bash
export LONGCAT_CODE=~/longcat-avatar-mlx
export LONGCAT_WEIGHTS=~/models/LongCat-Video-Avatar-1.6-bf16
```

## 4. Make a video

```bash
python3 talk_longcat.py me.jpg voice.wav examples/prompt.txt out.mp4 --cues examples/cues.txt
```

Add `--size 480x864` for a widescreen clip. The script prints each cue's time and each part as it finishes. Part files stay in a folder next to the output, so you can re-render one gesture without redoing the rest.

## 5. Upscale (optional)

The model's output is small. We used the RelayVSR upscaler at 4x to reach 2560x1440. Any video upscaler works.

## Times we measured

- 592x480: about 45 seconds of compute per second of video, about 47 GB peak memory.
- A 23 second clip with one gesture: about 18 minutes.
- Rendering HD directly (1280x720) failed twice on our machine after the first segment. Render small and upscale.
