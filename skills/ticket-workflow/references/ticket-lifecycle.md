# Ticket Lifecycle

Use this reference when executing `ticket-workflow`.

## Intake

Parse ticket IDs from the user request. If multiple tickets are independent, handle them
as separate task directories and avoid mixing artifacts.

Fetch ticket context:

```bash
plane issues fast-get TICKET-ID -f json
```

Fetch comments when the description is sparse, stale, or references discussion:

```bash
plane comments list -p PROJECT_UUID -i ISSUE_UUID -f json
```

## Task Directory

Create `tasks/<ticket-id>/req.md` with:

- Ticket ID and title.
- Type or inferred classification.
- Priority, state, assignee, labels, and links when available.
- Description.
- Relevant comments or activity.
- Assumptions and missing information.

Do not start implementation if `tasks/<ticket-id>/` already exists with unfinished work
that conflicts with the new request. Read the existing artifacts and decide whether to
resume or ask the user.

## Classification

Classify the ticket before selecting the workflow:

- `bug`: wrong behavior, regression, error, or failing user flow.
- `feature`: new user-visible capability.
- `refactor`: internal structure change without intended behavior change.
- `investigation`: answer or diagnosis only.
- `docs`: documentation-only change.
- `config`: environment, deployment, dependency, or project setup change.

If the classification is unclear, record the uncertainty in `req.md` and ask the user or
use `superpowers:brainstorming`.

## Planning

Create `findings.md` when codebase exploration is needed. Create `plan.md` when the
ticket needs multiple implementation steps, cross-area changes, or user approval.

Keep plans scoped to one ticket unless the user explicitly asks for a bundled change.

## Implementation

Use a git worktree for isolated implementation when the repository is already under git
and the ticket requires code changes. Use branch names:

- `fix/<ticket-id>` for bugs.
- `feat/<ticket-id>` for features.
- `chore/<ticket-id>` for refactor, docs, or config changes.

Update `progress.md` after meaningful checkpoints, especially after tests, validation,
or review feedback.

## Completion

Before reporting completion, run the relevant verification commands. If credentials,
services, or dependencies are missing, report exactly which validation was skipped and
why.
