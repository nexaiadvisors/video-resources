# Give your AI agent a talking face, for free

**What you get:** a Claude Code skill that turns one portrait into a talking avatar for your voice or chat app, plus a demo.

[Watch the demo](talking-avatar-demo.mp4) (sound on): the real browser player, driven by an AI voice. Nothing in it is a generated video.

## How it works

1. Start with one portrait of your character.
2. With an image editor (Nano Banana works), make a few versions of that same photo where only the mouth changes (closed, slightly open, "ah", "oo", "ee"), plus a blink and two side glances. A script keeps only the mouth or eye area from each edit, so the head never changes.
3. Another script pre-renders the in-between openings as small cut-outs (about 0.5 MB in total).
4. In the browser, a canvas draws the still and layers the right mouth and eye cut-outs every frame, based on how loud the AI's voice is. It also blinks, glances away in pauses, and sways and breathes a little.

No lip-sync model, no video, no per-minute cost, no delay. Honest limits: the mouth follows the voice, not the exact words, and the teeth are soft up close. In blind reviews by AI reviewers it scored about 6-7 out of 10 for realism.

## The skill

Copy the [`skill/talking-avatar`](skill/talking-avatar/) folder into `~/.claude/skills/` (or your agent's skills folder), then ask your agent: "add a talking avatar to my app using this portrait".

- [`SKILL.md`](skill/talking-avatar/SKILL.md): the steps, each with a check
- [`references/sprite-prompts.md`](skill/talking-avatar/references/sprite-prompts.md): the exact image-edit prompts
- [`scripts/`](skill/talking-avatar/scripts/): `paste.py`, `finish_sprites.py`, `make_atlas.py` (Python + OpenCV), `talkingAvatar.ts` (the browser player), and `demo.html` + `record_demo.cjs` to record your own demo

---
More videos and resources: https://www.nexaiadvisors.com/resources
