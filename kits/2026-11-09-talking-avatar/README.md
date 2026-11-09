# Give your AI agent a talking face, for free

**What you get:** a Claude Code skill that turns one portrait into a talking avatar for your voice or chat app, plus a demo.

![demo](talking-avatar-demo.mp4)

[Watch the demo](talking-avatar-demo.mp4): Morgan, an AI buyer in a pitch-practice app, switching between listening and talking.

## How it works

1. Start with one portrait of your character.
2. Generate two short clips of that same person from the portrait: one listening (blinking, nodding), one talking. Google Vids (Omni) works well and is included with a Google AI plan.
3. Loop both in the browser and fade to the talking clip whenever the AI's voice is playing.

No real-time lip sync, so no per-minute cost and no delay. The mouth moves like speech but is not synced to the exact words.

## The skill

Copy the [`skill/talking-avatar`](skill/talking-avatar/) folder into `~/.claude/skills/` (or your agent's skills folder), then ask your agent: "add a talking avatar to my app using this portrait".

- [`SKILL.md`](skill/talking-avatar/SKILL.md): the six steps, each with a check
- [`references/browser-player.md`](skill/talking-avatar/references/browser-player.md): level meter, React component, plain-JS version
- [`scripts/make-loops.sh`](skill/talking-avatar/scripts/make-loops.sh): turns your two clips into seamless web loops (needs ffmpeg)

---
More videos and resources: https://www.nexaiadvisors.com/resources
