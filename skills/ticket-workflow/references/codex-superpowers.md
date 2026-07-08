# Codex Superpowers Routing

Use this reference after `ticket-workflow` has fetched the ticket context and classified
the work.

## Phase Map

| Situation | Required superpower |
| --- | --- |
| Requirements are unclear, design choices are open, or user approval is needed | `superpowers:brainstorming` |
| Requirements are clear and implementation needs a written plan | `superpowers:writing-plans` |
| Work should happen in an isolated branch/worktree | `superpowers:using-git-worktrees` |
| The ticket is a bug or observed behavior is unexplained | `superpowers:systematic-debugging` |
| Code behavior must change and tests are feasible | `superpowers:test-driven-development` |
| Work is ready to be called done | `superpowers:verification-before-completion` |
| Changes are substantial or ready for merge/PR | `superpowers:requesting-code-review` |

## Routing Rules

Use superpowers exactly when their trigger conditions apply in the active environment.
Do not summarize a superpower from memory when it is available; load it and follow its
current instructions.

For bug tickets, reproduce or characterize the failure before editing code. For feature
tickets, get requirement/design approval before implementation when the behavior is not
fully specified.

If a required superpower is unavailable, continue with the closest local discipline and
report the missing skill as a gap in the final output.

## Minimal Workflows

Bug:

```text
plane-ticket-reader
ticket-workflow req.md
superpowers:systematic-debugging
superpowers:test-driven-development
superpowers:verification-before-completion
```

Feature:

```text
plane-ticket-reader
ticket-workflow req.md
superpowers:brainstorming
superpowers:writing-plans
superpowers:using-git-worktrees
superpowers:test-driven-development
superpowers:verification-before-completion
```

Investigation-only:

```text
plane-ticket-reader
ticket-workflow req.md
findings.md
superpowers:verification-before-completion
```
