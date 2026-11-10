# Ask the experts: NotebookLM for business strategy and cold outreach

**What you get:** the method I use to turn YouTube experts into a research desk, a no-code version you can run in NotebookLM today, and the Claude Code skill (`ask-expert`) that runs it for me.

## The method

1. **One notebook per topic.** In [NotebookLM](https://notebooklm.google.com), make a notebook named `YT: <Topic>` (for example `YT: Cold Outreach to Local Businesses`). Add 15-50 YouTube videos from the creators who actually do the thing. NotebookLM reads each video's transcript.
2. **Ask for the patterns, not a draft.** Ask what the experts agree on, with each point tied to the video it came from. NotebookLM cites its sources, so you can check every claim.
3. **Draft from the rules.** Hand those rules plus real facts about the recipient to your AI agent and have it draft the message.
4. **Review against the experts, then iterate.** Paste the draft back into the notebook and ask what the experts would cut. Revise 2-3 times until it reads like you wrote it to one person. You read and send every message yourself.
5. **Keep it fresh.** Before you rely on an answer, check that the notebook has videos from the last week on that subject. Advice on cold DMs from a year ago can be wrong today.

## No-code version (NotebookLM only)

Make the notebook as in step 1, then paste these prompts into its chat, one at a time.

**Prompt 1: the rules**

```
I'm writing a cold [email / Instagram DM / follow-up] to [who: e.g. owners of small pet brands].
What do these experts agree makes a message like this get a reply? Cover length, structure, the
first line, the ask, and follow-up timing. Name the video and creator for each point, and say
plainly what the sources do not cover.
```

**Prompt 2: the review**

```
Here is my draft:

[paste draft]

Review it against the experts. What would they cut, change or add? Quote the specific rule and
the video it comes from. Then give me a revised version under [N] words.
```

Run Prompt 2 again on each revision until it stops finding real problems.

## Claude Code version (the `ask-expert` skill)

The skill picks the right `YT:` notebook for your question, checks it has recent videos on that subject, adds new ones if not, asks it, and answers with linked sources.

Setup (about 10 minutes):

1. Install the NotebookLM CLI: `uv tool install notebooklm-mcp-cli` (or `pipx install notebooklm-mcp-cli`).
2. Sign in: `nlm login`. It opens a browser for your Google account.
3. Create at least one notebook named `YT: <Topic>` and add videos (in NotebookLM, or `nlm source add <notebook-id> --youtube <url>`).
4. Copy the [`skill/ask-expert`](skill/ask-expert/) folder into `~/.claude/skills/` (or your agent's skills folder).
5. Optional: set `YOUTUBE_API_KEY` (a free YouTube Data API key) so the freshness check is fast. Without it the script uses `yt-dlp`.
6. Ask: `/ask-expert what makes a cold follow-up email to contractors get a reply?`

Files:
- [`SKILL.md`](skill/ask-expert/SKILL.md): the five steps, each with a check, plus the outreach loop
- [`scripts/freshness.py`](skill/ask-expert/scripts/freshness.py): lists a notebook's videos by upload date and creator; reads only, never changes the notebook

Honest limits: NotebookLM only knows what you put in the notebook, so pick creators who have done the work. It summarizes; it can still miss nuance, so open the cited video when a point matters. `nlm` uses NotebookLM's web session, not an official API, so it can break when Google changes things.

---
More videos and resources: https://www.nexaiadvisors.com/resources
