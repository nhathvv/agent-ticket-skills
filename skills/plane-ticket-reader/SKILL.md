---
name: plane-ticket-reader
description: Read Plane.so projects, work items, comments, states, labels, members, and authenticated user details from a self-hosted Plane instance. Use when Codex needs to fetch or search ticket context such as PROJECT-123 before planning or implementing work.
---

# Plane Ticket Reader

Use the bundled `scripts/plane` CLI for read-only Plane.so access.

## Environment

Require these variables in the shell or a `.env` file in the current directory or an
ancestor directory:

```env
PLANE_API_KEY="plane_api_key_xxx"
PLANE_WORKSPACE="workspace-slug"
PLANE_BASE_URL="https://plane.example.com"
```

## Commands

Find projects:

```bash
plane projects list
plane projects get PROJECT_UUID
```

Read tickets:

```bash
plane issues list -p PROJECT_UUID
plane issues get -p PROJECT_UUID ISSUE_UUID
plane issues fast-get PROJECT-123
plane issues fast-get PROJECT-123 --expand
plane issues search PROJECT-123
```

Read comments and reference data:

```bash
plane comments list -p PROJECT_UUID -i ISSUE_UUID
plane comments list -p PROJECT_UUID -i ISSUE_UUID --all
plane members
plane me
plane states -p PROJECT_UUID
plane labels -p PROJECT_UUID
plane cycles list -p PROJECT_UUID
plane modules list -p PROJECT_UUID
```

Use `-f json` when the result will be parsed or copied into task artifacts.

This skill is intentionally read-only. Do not create, update, assign, comment on, or
delete Plane records through this workflow.
