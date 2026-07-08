# Agent Ticket Skills

Current Codex plugin version: `0.1.2`.

Reusable agent skills for ticket-driven development.

This repo is intentionally runtime-neutral at the source layer. The canonical skills
live in `skills/`; runtime adapters live in folders such as `codex/`. The first adapter
targets Codex and routes ticket work through Codex superpowers.

## What This Provides

- `plane-ticket-reader`: read-only Plane.so access for projects, work items, comments,
  states, labels, members, cycles, and modules.
- `ba`: creates and validates ticket-scoped feature specs in `tasks/<ticket-id>/spec.md`.
- `lead`: reviews specs, approves development, creates ADRs, and flags tech debt.
- `ticket-workflow`: a ticket orchestration skill that fetches ticket context, creates
  task artifacts, classifies the work, and routes the next phase through superpowers.
- `codex/agent-ticket-skills`: a plugin-ready Codex adapter that exposes the neutral
  skills without duplicating source files.

## Repository Layout

```text
agent-ticket-skills/
├── README.md
├── skills/
│   ├── ba/
│   │   └── SKILL.md
│   ├── lead/
│   │   └── SKILL.md
│   ├── plane-ticket-reader/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── plane
│   └── ticket-workflow/
│       ├── SKILL.md
│       └── references/
│           ├── codex-superpowers.md
│           └── ticket-lifecycle.md
├── codex/
│   └── agent-ticket-skills/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── ba -> ../../../skills/ba
│       │   ├── lead -> ../../../skills/lead
│       │   ├── plane-ticket-reader -> ../../../skills/plane-ticket-reader
│       │   └── ticket-workflow -> ../../../skills/ticket-workflow
│       └── scripts/
│           └── validate.sh
└── tests/
    └── test_plane_cli.py
```

`skills/` is the source of truth. Adapter folders should point to those skills instead
of copying them.

## Requirements

- Codex with superpowers installed for the full ticket workflow.
- Python 3.8+ for the bundled `plane` CLI.
- Access to a self-hosted Plane instance.
- A target git repo when using the workflow to implement tickets.

Plane environment variables:

```bash
export PLANE_API_KEY="plane_api_key_xxx"
export PLANE_WORKSPACE="workspace-slug"
export PLANE_BASE_URL="https://plane.example.com"
```

You can also put those values in a `.env` file in the target repo. The `plane` CLI
searches from the current directory upward and loads the first `.env` it finds.

## Validate This Repo

From this repo:

```bash
cd /path/to/agent-ticket-skills
codex/agent-ticket-skills/scripts/validate.sh
```

This checks:

- `plane` CLI help commands.
- read-only CLI command exposure.
- skill frontmatter.
- Codex plugin metadata.
- Codex adapter symlinks.

Validate the Codex plugin manifest directly:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  "$(pwd)/codex/agent-ticket-skills"
```

`validate.sh` runs this schema validator automatically when it is available. Set
`CODEX_PLUGIN_VALIDATOR=/path/to/validate_plugin.py` to use a non-default validator path.

## Install In Personal Codex Marketplace

For local Codex marketplace use, point the personal marketplace plugin source at the Codex
adapter:

```bash
cd /path/to/agent-ticket-skills
mkdir -p "$HOME/.agents/plugins/plugins"
ln -s "$(pwd)/codex/agent-ticket-skills" \
  "$HOME/.agents/plugins/plugins/agent-ticket-skills"
```

The marketplace entry should use this local source:

```json
{
  "name": "agent-ticket-skills",
  "source": {
    "source": "local",
    "path": "./plugins/agent-ticket-skills"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

The plugin exposes the Codex skills. The bundled Plane CLI is still an executable script inside
the repo, so make it available in shells where the workflow will fetch live Plane tickets:

```bash
export PATH="/path/to/agent-ticket-skills/skills/plane-ticket-reader/scripts:$PATH"
```

## Use In A Target Repo

Go to the repo where you want Codex to work:

```bash
cd /path/to/target-repo
git status
```

Expose the skills at project level:

```bash
AGENT_TICKET_SKILLS_ROOT=/path/to/agent-ticket-skills
mkdir -p .codex/skills
ln -s "$AGENT_TICKET_SKILLS_ROOT/skills/plane-ticket-reader" .codex/skills/plane-ticket-reader
ln -s "$AGENT_TICKET_SKILLS_ROOT/skills/ticket-workflow" .codex/skills/ticket-workflow
ln -s "$AGENT_TICKET_SKILLS_ROOT/skills/ba" .codex/skills/ba
ln -s "$AGENT_TICKET_SKILLS_ROOT/skills/lead" .codex/skills/lead
```

Add the Plane CLI to `PATH` for the current shell:

```bash
export PATH="/path/to/agent-ticket-skills/skills/plane-ticket-reader/scripts:$PATH"
```

Smoke test:

```bash
plane --help
plane issues --help
plane comments --help
```

Live Plane test:

```bash
plane issues fast-get TAD-1816 -f json
```

Replace `TAD-1816` with a real ticket ID from your Plane workspace.

## Codex Usage Examples

Read a ticket only:

```text
Use ticket-workflow to read TAD-1816, save raw ticket context, and ask BA to create the spec only. Do not implement.
```

Plan without implementation:

```text
Use ticket-workflow for TAD-1816. Fetch the ticket, explore this repo, and produce a plan only. Do not edit implementation files.
```

Implement with superpowers:

```text
Use ticket-workflow to implement TAD-1816 with superpowers.
```

Investigate a bug:

```text
Use ticket-workflow to investigate bug ticket TAD-1816. Reproduce or characterize the issue before editing code.
```

## Workflow Summary

`ticket-workflow` coordinates the lifecycle:

1. Fetch ticket context with `plane-ticket-reader`.
2. Save raw context to `tasks/<ticket-id>/ticket-context.json`.
3. Ask BA to create or audit `tasks/<ticket-id>/spec.md`.
4. Ask Lead to review the spec, create an ADR if needed, and approve or block development.
5. Classify the ticket as bug, feature, refactor, investigation, docs, or config.
6. Route to the right superpower phase:
   - `superpowers:brainstorming`
   - `superpowers:writing-plans`
   - `superpowers:using-git-worktrees`
   - `superpowers:systematic-debugging`
   - `superpowers:test-driven-development`
   - `superpowers:verification-before-completion`
   - `superpowers:requesting-code-review`
7. Save plans at `tasks/<ticket-id>/plan.md` and ADRs at `tasks/<ticket-id>/adr.md`.
8. Track findings and progress under `tasks/<ticket-id>/` when needed.
9. Report ticket summary, spec status, Lead decision, plan path, changed files,
   validation, gaps, and branch/worktree details.

Ticket artifacts are kept together:

```text
tasks/<ticket-id>/
├── ticket-context.json
├── spec.md
├── plan.md
├── adr.md
├── findings.md
└── progress.md
```

## Plane CLI Commands

The bundled CLI is read-only by design:

```bash
plane me
plane members
plane projects list
plane projects get PROJECT_UUID
plane issues list -p PROJECT_UUID
plane issues get -p PROJECT_UUID ISSUE_UUID
plane issues fast-get TICKET-ID
plane issues search QUERY
plane comments list -p PROJECT_UUID -i ISSUE_UUID
plane states -p PROJECT_UUID
plane labels -p PROJECT_UUID
plane cycles list -p PROJECT_UUID
plane cycles get -p PROJECT_UUID CYCLE_UUID
plane modules list -p PROJECT_UUID
plane modules get -p PROJECT_UUID MODULE_UUID
```

Use `-f json` when Codex needs to parse or save the response.

## Notes

- This repo currently supports Codex first.
- Claude and Antigravity adapters can be added later without moving `skills/`.
- The Codex adapter is plugin-ready, but project-level symlinks are the fastest way to
  test in a target repo.
- Do not use this workflow to write back to Plane. The current Plane integration is
  intentionally read-only.
