# pstack for Claude Code

A port of six skills from [pstack](https://github.com/cursor/plugins/tree/main/pstack), a Cursor plugin by Lauren Tan, to a Claude Code plugin. Upstream is a git submodule that is never edited. A script moves it to the latest upstream commit and rebuilds the plugin from it.

| Skill | What it does |
| --- | --- |
| `/pstack:correct` | Turns a mistake agents keep repeating into a check that fails, trying architecture, then types, then a lint, then a test, and docs last. |
| `/pstack:automate-me` | Mines past chats for how you work and writes a personal mode skill. |
| `/pstack:blast-radius` | Finds what a change breaks outside the diff and proves the one fact it is safe because of by running code. |
| `/pstack:create-verification-skill` | Writes a repo-local skill that launches the app, drives a feature like a user, and saves evidence. |
| `/pstack:recall` | Rebuilds where you left off from chat history and live git and PR state. |
| `/pstack:in-your-own-words` | Restates your goal before any work starts. |

`blast-radius` and `recall` can also be called by the model on its own. The other four run only when you type the slash command. `MODEL_INVOCABLE` in `port.py` sets which skills are which.

## Layout

```
~/repos/pstack-claude
  upstream/                     submodule of cursor/plugins, pinned to the synced commit. Never edit it.
  port.py                       builds plugin/ from the submodule
  adapter.md                    note added to each SKILL.md mapping Cursor terms to Claude Code
  sync.sh                       update the submodule, rebuild, validate
  plugin/                       generated plugin, committed so each sync shows upstream changes as a diff
~/.claude/skills/pstack         symlink to plugin/, loaded as pstack@skills-dir
```

## Update

```bash
~/repos/pstack-claude/sync.sh
git -C ~/repos/pstack-claude diff -- plugin    # read what upstream changed
git -C ~/repos/pstack-claude commit -am "Sync pstack <version>"   # also records the new upstream commit
```

Changes load in the next Claude Code session.

The sync stops with an error if upstream removes or renames a ported skill. It also lists any `.cursor/` path in the ported text that has no rewrite rule. Add a rule to `REWRITES` in `port.py` when the path has an exact Claude Code equivalent. Otherwise cover it in `adapter.md`.

## Add another skill

Add its folder name to `SKILLS` in `port.py` and run `sync.sh`. Then check its text for Cursor terms that `adapter.md` doesn't cover yet, such as the `Task` tool, model slugs, or Bugbot.

## Set up on a new machine

```bash
git clone --recurse-submodules https://github.com/christophercuongkim/pstack-claude.git ~/repos/pstack-claude
ln -s ~/repos/pstack-claude/plugin ~/.claude/skills/pstack
```

The plugin works without the submodule, since `plugin/` is committed. Skip `--recurse-submodules` if you only want to use the skills, not sync them.

The port scripts are MIT licensed, see `LICENSE`. pstack is MIT licensed too, and its license ships in `plugin/LICENSE`.
