#!/usr/bin/env python3
"""Build a Claude Code plugin in ./plugin from an upstream pstack checkout.

Usage: port.py [path/to/cursor-plugins/pstack]  (default: ./upstream/pstack)
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPSTREAM = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "upstream/pstack"
OUT = HERE / "plugin"
ADAPTER = (HERE / "adapter.md").read_text()

# The pstack skills to port. Add a folder name here to pull in another one.
SKILLS = [
    "automate-me",
    "blast-radius",
    "correct",
    "create-verification-skill",
    "in-your-own-words",
    "recall",
]

# Upstream marks every skill disable-model-invocation, which hides it from the model.
# These ones the model may also call on its own (chris-mode runs them unprompted).
MODEL_INVOCABLE = {"blast-radius", "recall"}

# Exact one-to-one equivalents. adapter.md covers the terms that need judgment.
REWRITES = [(".cursor/skills/", ".claude/skills/")]
REGEX_REWRITES = [(re.compile(r"\bAskQuestion\b"), "AskUserQuestion")]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def port_markdown(text: str, skill_name: str | None) -> str:
    for old, new in REWRITES:
        text = text.replace(old, new)
    for pattern, new in REGEX_REWRITES:
        text = pattern.sub(new, text)

    front, body = "", text
    if m := FRONTMATTER.match(text):
        meta = m.group(1)
        if skill_name:
            # Claude Code needs the kebab-case folder name, not a display name.
            meta = re.sub(r"(?m)^name:.*$", f"name: {skill_name}", meta)
            if skill_name in MODEL_INVOCABLE:
                meta = re.sub(r"(?m)^disable-model-invocation:.*\n?", "", meta).rstrip("\n")
        front, body = f"---\n{meta}\n---\n", text[m.end():]

    if skill_name:
        # Every skill entry point carries the note. Files it loads later share that context.
        body = f"\n{ADAPTER}\n{body.lstrip(chr(10))}"
    return front + body


def main() -> None:
    if not (UPSTREAM / "skills").is_dir():
        sys.exit(f"no pstack checkout at {UPSTREAM}")
    if OUT.exists():
        shutil.rmtree(OUT)

    for name in SKILLS:
        skill_dir = UPSTREAM / "skills" / name
        if not skill_dir.is_dir():
            sys.exit(f"upstream no longer has a {name} skill; update SKILLS in port.py")
        for src in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
            dst = OUT / src.relative_to(UPSTREAM)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.suffix != ".md":
                shutil.copy2(src, dst)
                continue
            ported = port_markdown(src.read_text(), name if src.name == "SKILL.md" else None)
            dst.write_text(ported)

    upstream_meta = json.loads((UPSTREAM / "plugin.json").read_text())
    keep = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
    meta = {k: upstream_meta[k] for k in keep if k in upstream_meta}
    (OUT / ".claude-plugin").mkdir()
    (OUT / ".claude-plugin/plugin.json").write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(UPSTREAM / "LICENSE", OUT / "LICENSE")

    print(f"pstack {meta['version']}: {len(SKILLS)} skills")

    # Paths still pointing into .cursor/ have no rewrite rule yet. Surface them on each sync.
    leftovers = sorted(
        {m for f in OUT.rglob("*.md")
         for m in re.findall(r"~?/?\.cursor/[\w./<>*-]*", f.read_text().replace(ADAPTER, ""))}
    )
    if leftovers:
        print("unmapped .cursor paths (the adapter note covers them; add a rewrite if one has an exact equivalent):")
        for path in leftovers:
            print(f"  {path}")


if __name__ == "__main__":
    main()
