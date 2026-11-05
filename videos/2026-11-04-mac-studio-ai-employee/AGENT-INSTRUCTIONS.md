# Instructions for your AI agent

Give this file to your coding agent (Claude Code, Codex, Cursor, or similar). You can paste it into the chat, or save it as `AGENTS.md` or `CLAUDE.md` in the folder you work from.

---

You are helping me set up and run an **always-on Mac**. It's a computer that stays on all day and runs my jobs, while I work from a different computer (my laptop). The files in this kit are:

| File | What it's for | When to use it |
|---|---|---|
| `SETUP.md` | The four setup steps (Tailscale, Screen Sharing, Remote Login, connect by name) and the two settings that keep the machine online | Once, when I set up the machine. Walk me through it one step at a time. |
| `FIRST-PROMPT.md` | My first prompt and my three rules | Read it first. The rules apply to everything you do on that machine. |
| `health-check.sh` | A read-only check: scheduled jobs and their last runs, sleep and update settings, disk space | Run it before you change anything, and whenever I ask "is everything OK?" |
| `watcher.plist` | A launchd template that runs a script every 15 minutes | When I want a new recurring job. Fill in the label and paths, and show me the file before you load it. |

## How to work on the always-on machine

1. **Connect by its name with your own key** (`ssh -i ~/.ssh/agent_key <user>@<machine-name>`). If you don't have a key yet, show me the `ssh-keygen` and `ssh-copy-id` commands from `SETUP.md` and let me run them.
2. **Check that you reached the right machine** before you do anything: run `hostname`, and compare it to the name I gave you.
3. **Read before you change.** Run `health-check.sh` and read the logs that matter to the task first. Tell me what you found.
4. **Ask before any change** on that machine: a setting, a file outside your working folder, a job, an install, a restart. Show me the exact command or file, and wait for my yes.
5. **Never type or ask for my passwords.** If a step needs `sudo` or a password, give me the exact command and let me run it myself.
6. **Prefer small, reversible steps.** Before you replace a file, copy the old one to `<name>.bak`.
7. **Report plainly.** Say what you ran, what it returned, and what is still unknown.

## Adding a recurring job

1. Write the script and test it once by hand. Show me the output.
2. Copy `watcher.plist`, and set `Label`, the script path and the log paths. Pick the interval: `900` for 15 min, `300` for 5 min, `43200` for 12 h, or `StartCalendarInterval` for a fixed time.
3. Show me the finished file. On my yes, save it in `~/Library/LaunchAgents/` and run `launchctl load <file>`.
4. Run `health-check.sh` afterwards and confirm the job is listed with exit status 0 after its first run.
