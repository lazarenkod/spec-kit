# Spec Kit Quick Start

Welcome! This project is set up for **Spec-Driven Development (SDD)** — a methodology where you describe *what* you want to build, and AI agents help you plan and implement it.

## Available Commands

### Core Workflow

| Command | Description |
|---------|-------------|
| `/speckit.constitution` | Define project principles and constraints |
| `/speckit.specify` | Create a feature specification (what & why) |
| `/speckit.clarify` | Resolve ambiguities in the specification |
| `/speckit.plan` | Create technical implementation plan |
| `/speckit.tasks` | Generate actionable task breakdown |
| `/speckit.implement` | Execute the implementation |

### Large Projects & UI Features

| Command | Description |
|---------|-------------|
| `/speckit.concept` | Capture complete service concept before specification (for 50+ requirements) |
| `/speckit.design` | Create visual specifications and design system for UI-heavy features |
| `/speckit.baseline` | Capture current system state for brownfield specifications |

### Validation & Analysis

| Command | Description |
|---------|-------------|
| `/speckit.analyze` | Cross-artifact consistency check |
| `/speckit.checklist` | Validate specification completeness |

### Feature Management

| Command | Description |
|---------|-------------|
| `/speckit.list` | List all specifications in the project |
| `/speckit.switch` | Switch to a different specification |
| `/speckit.extend` | Extend a merged feature with new capabilities |
| `/speckit.merge` | Finalize feature and update system specs after PR merge |

### Integration

| Command | Description |
|---------|-------------|
| `/speckit.taskstoissues` | Convert tasks into GitHub issues with dependencies |

## Recommended Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. CONSTITUTION   →   Define project rules & principles    │
│         ↓                                                   │
│  2. SPECIFY        →   Describe what you want (not how)     │
│         ↓                                                   │
│  3. CLARIFY        →   Resolve any ambiguities              │
│         ↓                                                   │
│  4. PLAN           →   Define tech stack & architecture     │
│         ↓                                                   │
│  5. TASKS          →   Break down into actionable items     │
│         ↓                                                   │
│  6. IMPLEMENT      →   Let the AI build it                  │
└─────────────────────────────────────────────────────────────┘
```

## Quick Example

### Step 1: Set up constitution (once per project)
```
/speckit.constitution This project uses TypeScript strictly. We prefer functional patterns. All code must have tests.
```

### Step 2: Describe your feature
```
/speckit.specify Build a todo app with categories, due dates, and priority levels. Users can filter and sort tasks.
```

### Step 3: Clarify requirements
```
/speckit.clarify What happens when a due date passes? How are priorities displayed?
```

### Step 4: Plan implementation
```
/speckit.plan Use React with Zustand for state. Store data in localStorage. Use Tailwind for styling.
```

### Step 5: Generate tasks
```
/speckit.tasks
```

### Step 6: Implement
```
/speckit.implement
```

## Project Structure

```
.specify/
├── memory/
│   └── constitution.md    # Project principles
├── scripts/               # Helper scripts
└── templates/             # Specification templates

specs/                     # Your specifications (created as you work)
├── 001-feature-name/
│   ├── spec.md           # Feature specification
│   ├── plan.md           # Technical plan
│   └── tasks.md          # Task breakdown
```

## Tips

- **Focus on WHAT, not HOW** during `/speckit.specify` — save tech decisions for `/speckit.plan`
- **Use `/speckit.clarify`** whenever requirements are ambiguous
- **Run `/speckit.analyze`** before implementation to catch inconsistencies
- **Branch per feature**: Commands auto-detect the active spec from your git branch

## Learn More

- [Full Documentation](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/docs/spec-driven.md)
