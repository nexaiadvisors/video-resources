# Instructions for your AI agent

Give this file to your coding agent (Claude Code, Codex, Cursor, or similar). You can paste it into the chat, or save it as `AGENTS.md` or `CLAUDE.md` in the folder you work from.

---

You are helping me make a **talking-avatar video on my own Mac**: one photo and one voice file in, one video out, with hand gestures placed on the words I choose. The files in this kit are:

| File | What it's for | When to use it |
|---|---|---|
| `SETUP.md` | Requirements and the install steps | Once. Walk me through it one step at a time. |
| `talk_longcat.py` | Renders the video and places the gestures | Every video. |
| `word_times.py` | Word start times from the voice file | Called by the script. Run it alone to see where a word falls. |
| `GESTURES.md` | Trigger phrases and a ready gesture sentence for each | When writing the cue file. |
| `examples/` | A working prompt and cue file | Copy and adapt. |

## Rules

1. **Check the machine first.** Confirm Apple silicon and at least 64 GB of memory (`sysctl hw.memsize`). If it has less, tell me and stop.
2. **Read code before running it.** The Mac port is community code pinned to one commit. Skim what it runs, and tell me if anything reaches the network or deletes files.
3. **Ask before installs and large downloads.** The weights are tens of gigabytes. Show me the command and the size, and wait for my yes.
4. **One heavy job at a time.** A render uses about 47 GB of memory. Never start two.
5. **Report plainly.** Say what you ran, what it returned, and what you did not check.

## Making a video

1. Read my script. Mark the trigger phrases using `GESTURES.md`. If the script counts ("first, second, third"), cue every item.
2. Write the prompt: the person and setting, then how they talk, with `{GESTURE|resting text}` where the hand sentence goes.
3. Write the cue file, one line per gesture, as an action with a start, a hold and a return.
4. Show me the cue list before you render.
5. Run `talk_longcat.py`. Then extract frames around each cue (5 per second) and look at the hands.
6. If a hand shape is wrong, re-render only that part with another seed. The part files and stills are in the `lc-<name>` folder next to the output.
7. Tell me where each gesture landed against the word time.
