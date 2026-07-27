# AI Context Files — Design Spec

**Goal:** Define a standard set of Markdown context files that any project can use to keep AI coding agents aligned — preventing them from guessing architecture, making contradicting decisions, or building the wrong thing.

**Architecture:** Eight optional Markdown files at the project root, each with a clear single responsibility. AI agents (Claude, Codex, Cursor, etc.) read these files as ground-truth context before generating code. The files act as a "project constitution" — explicit, versioned, and reviewable alongside code changes.

**Tech Stack:** Markdown (no special tooling required). A CLI scaffold command for convenience.

## File Definitions

### 1. `PRD.md` — Product Requirements Document
The "why" behind the project. Prevents AI from guessing user intent.

Required sections:
- Problem being solved
- Target users
- Core features (bullet list)
- User roles / personas
- Functional requirements (numbered, testable)
- Non-functional requirements
- Success criteria (measurable)
- Out-of-scope items

### 2. `ARCHITECTURE.md` — Technical Blueprint
Prevents the system from becoming a patchwork of conflicting patterns.

Required sections:
- System architecture overview (diagram in ASCII or Mermaid)
- App flow / data flow
- Folder structure (tree)
- Tech stack (with exact versions)
- Database design (entities, relationships)
- Auth flow (if applicable)
- API patterns (REST, GraphQL, etc.)
- Frontend/backend boundaries
- Key design decisions

### 3. `RULES.md` — Coding Constraints
Prevents the AI from "improving" the project into chaos.

Required sections:
- Required tech stack (locked versions)
- Approved / forbidden libraries
- Naming conventions (files, classes, functions, variables)
- Error handling rules
- Security guidelines
- Reusable component standards
- Files the AI must not touch (denylist)
- Limits on autonomous decisions (what requires human approval)

### 4. `PHASES.md` — Implementation Plan
Prevents building everything at once.

Required sections:
- Phase breakdown (each with scope, dependencies, "done" criteria)
- Phase 1: [name] — scope, deps, done criteria
- Phase N: ... (repeat)

### 5. `DESIGN.md` — Design System
Prevents AI-generated UIs from looking random.

Required sections:
- Colors & themes (hex/rgb values)
- Typography (font stack, sizes, weights, line heights)
- Spacing system (4px/8px grid base)
- Border radius values
- Shadow/elevation system
- Component behavior patterns (hover, active, disabled)
- Breakpoints (responsive)
- Accessibility rules (WCAG targets)

### 6. `MEMORY.md` — Project State
Helps the AI stay aligned over time across sessions.

Required sections:
- What's done
- Current phase
- Active work (what's being worked on now)
- Key decisions (with rationales)
- Known issues
- Open tasks
- Next step

### 7. `TESTING.md` (Optional) — Testing Guide
Prevents the AI from writing inconsistent or missing tests.

Required sections:
- Critical flows to test
- Edge cases to cover
- Validation rules
- Testing strategy (unit vs integration vs e2e)
- Pre-release checklist

### 8. `DECISIONS.md` (Optional) — Decision Log
Prevents future AI sessions from undoing intentional choices.

Required sections:
- Each entry: date, decision, rationale, alternatives considered
- Append-only (new entries at top)

## File Location

- All files live at project root (`./PRD.md`, `./ARCHITECTURE.md`, etc.)
- Or in `./docs/` if the project root is too cluttered
- Git-tracked and versioned alongside code

## CLI Scaffold Command (v2)

```
ai-context init           # Create all files with templates
ai-context init --prd     # Create only PRD.md
ai-context init --all     # Create all including optional files
```

## Agent Integration

- AI agents read these files at session start
- `AGENTS.md` or `CLAUDE.md` should reference them: "See PRD.md for product requirements"
- `MEMORY.md` updated by the agent at end of each session

## Non-Goals (v1)

- No watcher / hot-reload daemon
- No VSCode extension
- No validation/linting of the files (v2)
- No web UI
- No integration with external project management tools
