# pstack for Claude Code

A port of six skills from [pstack](https://github.com/cursor/plugins/tree/main/pstack), a Cursor plugin by Lauren Tan, to a Claude Code plugin. The upstream checkout stays untouched, so it updates with `git pull`. A script rebuilds the plugin from it.

| Skill | What it does |
| --- | --- |
| `/pstack:correct` | Turns a mistake agents keep repeating into a check that fails, trying architecture, then types, then a lint, then a test, and docs last. |
| `/pstack:automate-me` | Mines past chats for how you work and writes a personal mode skill. |
| `/pstack:blast-radius` | Finds what a change breaks outside the diff and proves the one fact it is safe because of by running code. |
| `/pstack:create-verification-skill` | Writes a repo-local skill that launches the app, drives a feature like a user, and saves evidence. |
| `/pstack:recall` | Rebuilds where you left off from chat history and live git and PR state. |
| `/pstack:in-your-own-words` | Restates your goal before any work starts. |

All six run only when you type the slash command.

## Layout

```
~/repos/pstack                  sparse clone of cursor/plugins, pstack/ only. Never edit it.
~/repos/pstack-claude
  port.py                       builds plugin/ from the clone
  adapter.md                    note added to each SKILL.md mapping Cursor terms to Claude Code
  sync.sh                       pull, rebuild, validate
  plugin/                       generated plugin, committed so each sync shows upstream changes as a diff
~/.claude/skills/pstack         symlink to plugin/, loaded as pstack@skills-dir
```

## Update

```bash
~/repos/pstack-claude/sync.sh
git -C ~/repos/pstack-claude diff -- plugin    # read what upstream changed
git -C ~/repos/pstack-claude commit -am "Sync pstack <version>"
```

Changes load in the next Claude Code session.

The sync stops with an error if upstream removes or renames a ported skill. It also lists any `.cursor/` path in the ported text that has no rewrite rule. Add a rule to `REWRITES` in `port.py` when the path has an exact Claude Code equivalent. Otherwise cover it in `adapter.md`.

## Add another skill

Add its folder name to `SKILLS` in `port.py` and run `sync.sh`. Then check its text for Cursor terms that `adapter.md` doesn't cover yet, such as the `Task` tool, model slugs, or Bugbot.

## Set up on a new machine

```bash
git clone --filter=blob:none --sparse https://github.com/cursor/plugins.git ~/repos/pstack
git -C ~/repos/pstack sparse-checkout set pstack
ln -s ~/repos/pstack-claude/plugin ~/.claude/skills/pstack
```

pstack is MIT licensed. Its license ships in `plugin/LICENSE`.
