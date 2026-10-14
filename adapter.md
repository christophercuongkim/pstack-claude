> **Running in Claude Code.** pstack was written for Cursor. Read its Cursor terms as these Claude Code equivalents:
>
> - The agent instruction file is `CLAUDE.md`. Read a repo's `AGENTS.md` as well when it has one.
> - Cursor's `create-skill` skill is the `skill-creator` skill.
> - Chat transcripts live at `~/.claude/projects/<slug>/<uuid>.jsonl`, with subagent chats at `<slug>/<uuid>/subagents/*.jsonl`. The slug is the working directory with every character that is not a letter or digit replaced by `-`, so `/home/me/my_repo` becomes `-home-me-my-repo`.
> - Only some pstack skills are installed. When a step sends you to one that isn't in your skill list, such as `how`, `why`, `arena`, `poteto-mode` or `maintain-verification-skill`, do that step directly from its description or skip it and say so.
