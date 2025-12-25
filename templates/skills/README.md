# Spec Kit Skills

Skills are **instruction sets** that Spec Kit commands reference. They are NOT standalone slash commands.

**How skills work**:
1. A command (e.g., `/speckit.design`) has a `skills:` section in frontmatter
2. When the command runs, the agent reads referenced skill files
3. The agent follows skill instructions at appropriate points

## Available Skills

### Product Management Skills

| Skill | Purpose | Used By |
|-------|---------|---------|
| **market-research** | Competitor analysis, market trends, user pain points | `/speckit.concept` |
| **competitive-analysis** | Deep competitive landscape analysis | `/speckit.concept` |
| **prioritization** | ICE/RICE feature prioritization | `/speckit.plan` |

### UX Quality Skills

| Skill | Purpose | Used By |
|-------|---------|---------|
| **ux-audit** | Validate spec against UXQ domain principles | `/speckit.specify`, `/speckit.design` |

### UX Design Skills

| Skill | Purpose | Used By |
|-------|---------|---------|
| **interaction-design** | Component states, transitions, behaviors | `/speckit.design` |
| **wireframe-spec** | ASCII wireframes with annotations | `/speckit.design` |
| **accessibility-audit** | WCAG compliance validation | `/speckit.design` |

### QA & Testing Skills

| Skill | Purpose | Used By |
|-------|---------|---------|
| **test-strategy** | Generate test plan from specification | `/speckit.analyze` |
| **security-audit** | OWASP and constitution security check | `/speckit.analyze` |

### Codebase Skills

| Skill | Purpose | Used By |
|-------|---------|---------|
| **code-explore** | Document existing codebase behaviors | `/speckit.baseline`, `/speckit.specify` |

## Skill Integration with Commands

### `/speckit.concept`
- Uses `market-research` during Phase 0b (Market & User Research)
- Uses `competitive-analysis` for positioning decisions
- Uses `ux-audit` to validate concept for UX quality

### `/speckit.specify`
- Uses `ux-audit` before finalizing spec when UXQ domain is active
- Uses `code-explore` in brownfield mode to understand existing code

### `/speckit.baseline`
- Uses `code-explore` for comprehensive codebase analysis

### `/speckit.plan`
- Uses `prioritization` to sequence implementation

### `/speckit.design`
- Uses `interaction-design` for component behavior specs
- Uses `wireframe-spec` for layout specifications
- Uses `accessibility-audit` for WCAG compliance
- Uses `ux-audit` for UXQ domain validation

### `/speckit.analyze`
- Uses `test-strategy` for test coverage analysis
- Uses `security-audit` in QA mode for security verification

## Skill-to-Persona Mapping

| Persona | Primary Skills |
|---------|---------------|
| **Product Agent** | market-research, competitive-analysis, prioritization, ux-audit |
| **UX Designer Agent** | interaction-design, wireframe-spec, accessibility-audit, ux-audit |
| **QA Agent** | test-strategy, security-audit, code-explore, ux-audit |
| **Architect Agent** | code-explore, security-audit |
| **Developer Agent** | code-explore, test-strategy |

## Using Claude Code Built-in Agents

Skills leverage Claude Code's Task tool with built-in agents:

```text
Task(subagent_type="Explore", prompt="...")  → Fast codebase exploration
Task(subagent_type="Plan", prompt="...")     → Architecture planning
```

Skills also use Claude Code tools directly:
- `WebSearch` → Market research, competitor analysis
- `Read/Grep/Glob` → Codebase analysis
- `Write` → Report generation

## Creating New Skills

1. Create `.md` file in `templates/skills/`
2. Add frontmatter with `description`
3. Define execution steps
4. Reference in relevant commands' `skills:` section
5. Update relevant persona with skill reference

Example structure:

```yaml
---
description: Brief description of skill purpose
---

## User Input
$ARGUMENTS

## Purpose
Why this skill exists and what problem it solves.

## When to Use
- Trigger condition 1
- Trigger condition 2

## Execution Steps
### 1. Step Name
Detailed instructions...

## Output
What the skill produces.

## Integration with Spec Kit
How it connects to other commands/skills.
```

## Quick Reference

| Skill | Description | Primary Command |
|-------|-------------|-----------------|
| market-research | Market landscape research | `/speckit.concept` |
| competitive-analysis | Deep competitor analysis | `/speckit.concept` |
| prioritization | ICE/RICE scoring | `/speckit.plan` |
| ux-audit | UXQ domain compliance | `/speckit.specify` |
| interaction-design | Component states & behaviors | `/speckit.design` |
| wireframe-spec | ASCII wireframes | `/speckit.design` |
| accessibility-audit | WCAG compliance | `/speckit.design` |
| test-strategy | Test plan generation | `/speckit.analyze` |
| security-audit | OWASP security check | `/speckit.analyze` |
| code-explore | Brownfield code analysis | `/speckit.baseline` |
