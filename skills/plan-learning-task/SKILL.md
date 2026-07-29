---
name: plan-learning-task
description: Turn a learning goal or small repository change into a dependency-aware, verifiable execution plan. Use when asked to plan a tutorial, study exercise, incremental feature, or practice task; when a request needs to be split between a parent agent and subagents; or when success criteria and validation steps are unclear.
---

# Plan Learning Task

Convert a goal into a short plan that a learner or agent can execute and verify.

## Workflow

1. Read the repository instructions, relevant implementation, tests, and learner goal.
2. State current behavior using only evidence from files or command output.
3. Separate requirements from assumptions. Ask only when an unresolved choice would materially change the plan.
4. Define one observable outcome and the constraints that must remain true.
5. Create 3–7 ordered steps and name likely files or symbols when known.
6. Attach a verification method to every implementation step.
7. Identify steps independent enough for subagents. Keep integration and final validation with the parent.
8. Check the draft against `references/quality-checklist.md`.

## Plan format

```markdown
## Outcome
[One observable result]

## Constraints
- [Behavior or boundary to preserve]

## Steps
1. [Action]
   - Files: [...]
   - Verify: [...]

## Delegation
- Parent: [...]
- Optional subagent: [bounded task, inputs, prohibited actions, output]

## Risks and open questions
- [...]

## Done
- [Tests, review, and learner explanation required]
```

## Delegation rules

- Delegate only a concrete, bounded task that can progress independently.
- Include objective, allowed inputs, prohibited actions, and return format.
- Avoid concurrent edits to the same files.
- Require evidence rather than conclusions alone.
- Have the parent reconcile conflicts and run final verification.
- Do not invent subagent availability; use the same boundaries as sequential roles when none are available.

