# Port pstack skills to Claude Code

- [x] Track cursor/plugins as the `upstream` submodule, never edited
- [x] Port script with an allowlist of six skills, path rewrites, and an adapter note per SKILL.md
- [x] Rename skills to their folder names so Claude Code accepts them
- [x] Sync script: pull, rebuild, `claude plugin validate`
- [x] Symlink plugin/ to ~/.claude/skills/pstack

## Review

- `claude plugin validate` passes. `claude plugin details pstack@skills-dir` shows six skills loaded, about 562 tokens always on.
- A headless `claude -p "/pstack:in-your-own-words ..."` session ran the ported skill and restated the goal correctly.
- Left out: every other pstack skill, the agents, docs and automations. Skills that call missing pstack skills (how, why, arena) do that step directly or skip it, per adapter.md.
