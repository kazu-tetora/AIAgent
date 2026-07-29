# Repository instructions

## Purpose and scope

This repository is a Japanese learning lab for agent instructions, skills, and bounded subagent delegation. These rules apply to the whole repository; a deeper `AGENTS.md` may refine its subtree.

## Working rules

- Read `README.md`, relevant code, and tests before editing.
- Use Python 3.10+ and the standard library only.
- Keep user-facing documentation in Japanese and Python identifiers in English.
- Make the smallest change that satisfies the task.
- Do not silently break JSON fields `id`, `title`, or `done`.
- Treat `subagents/roles/*.md` as prompt examples, not automatically active agents.
- Keep `SKILL.md` concise; put detailed criteria in `references/`.

## Verification

After changing Python:

```bash
python3 -m unittest discover -s tests -v
```

After changing the sample Skill:

```bash
python3 /Users/terakadokazuya/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/plan-learning-task
```

If that validator is unavailable elsewhere, check that the folder matches `name`, the frontmatter contains only `name` and `description`, and `agents/openai.yaml` remains consistent.

## Done means

- Relevant tests pass.
- CLI errors go to stderr with a non-zero exit code.
- Documentation matches actual commands.
- The final report lists changes, verification, and remaining uncertainty.
