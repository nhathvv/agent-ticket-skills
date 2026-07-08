---
name: ticket-workflow
description: Coordinate Codex work from one or more ticket IDs such as TAD-1816. Use when the user asks Codex to read, specify, plan, implement, fix, investigate, or validate Plane tickets through plane-ticket-reader, BA specs, Lead architecture review, and Codex superpowers.
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
3. Save raw ticket context to `tasks/<ticket-id>/ticket-context.json`.
4. Use `ba` to create or audit `specs/FEAT-XXX-<slug>.md`.
5. Use `lead` to review the spec, create ADRs when needed, and approve or block development.
6. Choose the implementation phase from `references/codex-superpowers.md`.
7. Track progress when implementation work is required.
8. Before completion, verify and report according to the output contract.

For the detailed lifecycle rules, read `references/ticket-lifecycle.md`.
For Codex superpower routing, read `references/codex-superpowers.md`.

## Task Artifacts

Create these files only when they are useful for the ticket scope:

```text
tasks/<ticket-id>/
├── ticket-context.json
├── findings.md
└── progress.md

specs/
└── FEAT-XXX-<slug>.md

docs/adr/
└── NNNN-<slug>.md
```

Use `ticket-context.json` for raw Plane output. Use `specs/FEAT-XXX-<slug>.md` for the
BA requirements artifact. Use `docs/adr/NNNN-<slug>.md` only when Lead determines an ADR
is required. Use `findings.md` for codebase exploration and root-cause notes. Use
`progress.md` for execution checkpoints.

## Output Contract

End ticket work with:

- Ticket summary: ID, title, classification, and scope.
- Spec path and status.
- Lead decision: approved, blocked, or no implementation needed.
- ADR path when one was created.
- Files changed or created.
- Validation performed, including commands and outcomes.
- Remaining gaps or blocked items.
- Branch or worktree path when isolated implementation was used.

Stop and ask for clarification when the ticket is ambiguous, too large for one plan, or
requires access that is not available.
