# I Built My Own HeyGen Avatar 6 on a Mac (Free Code)

Watch: https://www.youtube.com/watch?v=<id>

**What you get:** the script that makes a talking avatar from one photo and one voice file on your own Mac, and places hand gestures on the exact words you choose. Plus the gesture list, example prompts and setup notes.

## The kit

| File | What it is |
|---|---|
| `SETUP.md` | What you need and how to install it: the model, the Mac port, the weights |
| `talk_longcat.py` | The script. Photo + voice + prompt + cue file in, one continuous video out |
| `word_times.py` | Finds when each word is spoken, so a gesture can land on it |
| `GESTURES.md` | Which gesture goes with which words, with a ready sentence for each |
| `examples/prompt.txt`, `examples/cues.txt` | The prompt and cue file from the video |
| `AGENT-INSTRUCTIONS.md` | Hand this to your coding agent and let it do the setup with you |

## The one idea

A video model does what you ask at the **start** of what it is generating. It does not wait for a word. So to make a gesture land on a word, do not ask harder. Start a new piece of video just before the word, from a single still frame, with the gesture in the prompt.

## What it costs to run

- A Mac with Apple silicon and 64 GB of memory or more. The model peaked at about 47 GB in our runs.
- About 45 seconds of compute for each second of video at 592x480.
- No per-minute fee. The voice is separate: bring any audio file.

## What does not work yet

- A placed gesture on a walking shot. Walking and talking works; the timed gesture does not land.
- Finger counts depend on the random seed. Check a frame, and re-render that one piece with another seed.
- Small text on clothing turns to scribble. Use a photo with no lettering.

## Credits

- LongCat-Video-Avatar 1.6 is by Meituan (MIT licence): https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6
- The Mac (MLX) port is by xocialize (MIT licence): https://github.com/xocialize/longcat-avatar-mlx
- Version 1.6 support with continuation is by fedeinfe, in pull request 8 on that repo.

---
More videos and resources: https://www.nexaiadvisors.com/resources
