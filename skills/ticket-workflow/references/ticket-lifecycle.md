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

## Ticket Context

Create the ticket workspace:

```text
tasks/<ticket-id>/
├── ticket-context.json
├── spec.md
├── plan.md
├── adr.md
├── findings.md
└── progress.md
```

Create `tasks/<ticket-id>/ticket-context.json` with the raw ticket JSON and relevant
comments or activity. Preserve the source data so BA and Lead artifacts can be reviewed
without refetching Plane.

Create `tasks/<ticket-id>/progress.md` when work will continue beyond intake. Use it
as the resumable state log for done, in-progress, next steps, validation, and blockers.
Create `tasks/<ticket-id>/findings.md` when codebase exploration, debugging notes,
observations, or root-cause analysis are useful.

Do not start implementation if `tasks/<ticket-id>/` already exists with unfinished work
that conflicts with the new request. Read the existing artifacts and decide whether to
resume or ask the user.

## BA Specification

After ticket context is available, use the `ba` skill to create or audit a feature spec:

```text
tasks/<ticket-id>/spec.md
```

BA owns requirements only. The spec must include Context, User Story, Acceptance
Criteria, Out of Scope, Open Questions, and Dependencies. BA must run its quality gates
before marking the spec `ready`.

## Classification

Classify the ticket before selecting the workflow:

- `bug`: wrong behavior, regression, error, or failing user flow.
- `feature`: new user-visible capability.
- `refactor`: internal structure change without intended behavior change.
- `investigation`: answer or diagnosis only.
- `docs`: documentation-only change.
- `config`: environment, deployment, dependency, or project setup change.

If the classification is unclear, record the uncertainty in the BA spec and ask the user
or use `superpowers:brainstorming`.

## Planning

After BA marks the spec `ready`, use the `lead` skill before Dev starts.

Lead must read the spec, run the architecture/code review checklist as applicable, and
decide whether an ADR is required. If an ADR is required, Lead creates:

```text
tasks/<ticket-id>/adr.md
```

If Lead approves the feature, Lead sets spec status to `in-dev`. If Lead blocks the
feature, stop before implementation and report the blocking issues.

Use `superpowers:writing-plans` for detailed implementation plans after Lead approval.
Save the resulting plan under:

```text
tasks/<ticket-id>/plan.md
```

Keep plans scoped to one ticket unless the user explicitly asks for a bundled change.

## Implementation

Use a git worktree for isolated implementation when the repository is already under git
and the ticket requires code changes. Use branch names:

- `fix/<ticket-id>` for bugs.
- `feat/<ticket-id>` for features.
- `chore/<ticket-id>` for refactor, docs, or config changes.

Update `tasks/<ticket-id>/progress.md` after meaningful checkpoints, especially after
tests, validation, or review feedback.

## Completion

Before reporting completion, run the relevant verification commands. If credentials,
services, or dependencies are missing, report exactly which validation was skipped and
why.
