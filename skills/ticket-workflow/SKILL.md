---
name: ticket-workflow
description: Coordinate Codex work from one or more ticket IDs such as TAD-1816. Use when the user asks Codex to read, plan, implement, fix, investigate, or validate Plane tickets, especially when the workflow should combine plane-ticket-reader with Codex superpowers.
---

# Ticket Workflow

Use this skill as the ticket orchestration layer. It routes work through other skills
and Codex superpowers; it does not replace them.

## Required Inputs

- One or more ticket IDs, for example `TAD-1816`.
- A working repository where the ticket should be implemented or investigated.
- Plane environment variables when ticket details must be fetched live.

## Core Flow

1. Read ticket context with `plane-ticket-reader`.
2. Create `tasks/<ticket-id>/` in the implementation repository.
3. Write `tasks/<ticket-id>/req.md` with title, description, metadata, links, and relevant comments.
4. Classify the ticket as `bug`, `feature`, `refactor`, `investigation`, `docs`, or `config`.
5. Choose the next phase from `references/codex-superpowers.md`.
6. Track findings, plan, and progress when implementation work is required.
7. Before completion, verify and report according to the output contract.

For the detailed lifecycle rules, read `references/ticket-lifecycle.md`.
For Codex superpower routing, read `references/codex-superpowers.md`.

## Task Artifacts

Create these files only when they are useful for the ticket scope:

```text
tasks/<ticket-id>/
├── req.md
├── findings.md
├── plan.md
└── progress.md
```

Use `req.md` for raw ticket context. Use `findings.md` for codebase exploration and
root-cause notes. Use `plan.md` for the approved implementation plan. Use `progress.md`
for execution checkpoints.

## Output Contract

End ticket work with:

- Ticket summary: ID, title, classification, and scope.
- Files changed or created.
- Validation performed, including commands and outcomes.
- Remaining gaps or blocked items.
- Branch or worktree path when isolated implementation was used.

Stop and ask for clarification when the ticket is ambiguous, too large for one plan, or
requires access that is not available.
