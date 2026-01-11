# Contributing Guidelines Template

This template generates contributing documentation from project constitution, code style, and development workflow.

## Usage

This template is used by:
- `/speckit.implement` — generates contributing guidelines from constitution principles
- `/speckit.docs build --type contributing` — regenerates contributing documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| constitution.md | Project principles, values, coding standards |
| plan.md | Tech stack, architecture, development environment |
| .github/ | PR templates, CI/CD workflows, code review process |
| code analysis | Code style, patterns, conventions |
| RUNNING.md | Development setup instructions |

## Template Structure

```markdown
# Contributing to {Project Name}

Thank you for your interest in contributing to {Project Name}! This document will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Review Process](#review-process)
- [Getting Help](#getting-help)

---

## Code of Conduct

{From constitution.md or standard CoC}

This project adheres to the principles outlined in our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

**Core Values** (from constitution):
{Extract values from constitution.md}

- **{Value 1}**: {Description}
- **{Value 2}**: {Description}
- **{Value 3}**: {Description}

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- [ ] Read this contributing guide
- [ ] Set up development environment ([Installation Guide](../installation/detailed-setup.md))
- [ ] Reviewed project architecture ([Architecture Guide](../developer-guide/architecture/overview.md))
- [ ] Joined community channels ({community-links})

### Finding Work

**For first-time contributors:**
- Look for issues labeled [`good first issue`]({issues-url}?q=label%3A%22good+first+issue%22)
- Check [`help wanted`]({issues-url}?q=label%3A%22help+wanted%22) label

**For experienced contributors:**
- Browse [open issues]({issues-url})
- Review [project roadmap]({roadmap-url})
- Propose new features via [discussions]({discussions-url})

### Claiming an Issue

1. Comment on the issue: "I'd like to work on this"
2. Wait for maintainer assignment
3. Fork the repository
4. Create a feature branch

---

## Development Workflow

### 1. Fork and Clone

```bash
# Fork repository on GitHub

# Clone your fork
git clone {repository-url}
cd {project-name}

# Add upstream remote
git remote add upstream {upstream-url}
```

### 2. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/{feature-name}
# or
git checkout -b fix/{bug-name}
```

**Branch Naming Conventions:**
- `feature/{feature-name}` — New features
- `fix/{bug-name}` — Bug fixes
- `docs/{doc-name}` — Documentation updates
- `refactor/{component}` — Code refactoring
- `test/{test-name}` — Test additions

### 3. Make Changes

{From constitution principles}

**Development Principles:**
{Extract from constitution.md}

**Before coding:**
- [ ] Understand the problem
- [ ] Review existing code
- [ ] Plan your approach
- [ ] Ask questions if unclear

### 4. Test Your Changes

```bash
# Run tests
{test command}

# Run linter
{lint command}

# Check formatting
{format command}

# Run type checker (if applicable)
{type check command}
```

**All checks must pass before submitting PR.**

### 5. Commit Changes

```bash
# Stage changes
git add {files}

# Commit with descriptive message
git commit -m "{commit message}"
```

See [Commit Guidelines](#commit-guidelines) for message format.

### 6. Push and Create PR

```bash
# Push to your fork
git push origin feature/{feature-name}

# Create Pull Request on GitHub
```

---

## Coding Standards

{From code analysis and constitution}

### General Principles

{Extract from constitution.md}

- **{Principle 1}**: {Description}
- **{Principle 2}**: {Description}

### Code Style

**We follow {style-guide-name} with modifications:**

{Language-specific style guide}

#### {Language} Style

**File naming:**
- `{pattern}` for {type}
- Example: `{example}`

**Function naming:**
- `{pattern}` for {type}
- Example: `{example}`

**Code organization:**
```{language}
// Example structure
{code example}
```

### Formatting

**Automated formatting:**
```bash
# Format code
{format command}
```

**Configuration:** See `{config-file}`

### Linting

**Linter configuration:** `{linter-config}`

```bash
# Run linter
{lint command}

# Auto-fix issues
{lint-fix command}
```

**Common lint errors:**
| Error | Fix |
|-------|-----|
| {error} | {fix} |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | {convention} | `{example}` |
| Functions | {convention} | `{example}` |
| Classes | {convention} | `{example}` |
| Constants | {convention} | `{example}` |
| Files | {convention} | `{example}` |

### Documentation

**Code comments:**
- Document **why**, not **what**
- Use docstrings for public APIs
- Keep comments up-to-date

**Example:**
```{language}
{documented code example}
```

**API documentation:**
{Documentation standard for the project}

---

## Testing Requirements

### Test Coverage

**Minimum coverage:** {coverage-threshold}% (from constitution or plan)

```bash
# Run tests with coverage
{coverage command}

# View coverage report
{coverage report command}
```

### Test Types

**Unit Tests:**
- Test individual functions/methods
- Mock external dependencies
- Fast execution (< 100ms per test)

**Integration Tests:**
- Test component interactions
- Use test database/services
- Moderate execution time

**End-to-End Tests:**
- Test complete user workflows
- Use staging environment
- Longer execution time

### Writing Tests

**Test file location:** `{test-directory-structure}`

**Test naming:**
```{language}
{test naming example}
```

**Test structure:**
```{language}
{test structure example}
```

**Best practices:**
- ✅ One assertion per test (when possible)
- ✅ Clear test names describing behavior
- ✅ Arrange-Act-Assert pattern
- ✅ Independent tests (no shared state)
- ❌ Don't test implementation details
- ❌ Don't write flaky tests

### Test Data

**Test fixtures:** `{fixture-location}`

**Test data guidelines:**
- Use realistic but anonymous data
- Don't commit sensitive data
- Use factories for complex objects

---

## Commit Guidelines

{From git history analysis or standard convention}

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(auth): add OAuth2 authentication

Implement OAuth2 authentication flow with Google and GitHub providers.
Includes token refresh mechanism and user profile sync.

Closes #123
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add user endpoints` |
| `fix` | Bug fix | `fix(auth): resolve token expiry issue` |
| `docs` | Documentation | `docs(readme): update installation steps` |
| `style` | Code style | `style(lint): fix formatting issues` |
| `refactor` | Code refactoring | `refactor(db): simplify query logic` |
| `test` | Add/update tests | `test(auth): add OAuth integration tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |

### Commit Best Practices

- ✅ Write in imperative mood ("add feature" not "added feature")
- ✅ Keep subject line under 50 characters
- ✅ Capitalize subject line
- ✅ Don't end subject with period
- ✅ Separate subject from body with blank line
- ✅ Wrap body at 72 characters
- ✅ Explain **what** and **why**, not **how**
- ✅ Reference issues: `Closes #123`, `Fixes #456`

### Atomic Commits

Make commits atomic — each commit should:
- Represent one logical change
- Be independently revertible
- Pass all tests

**Don't mix unrelated changes in one commit.**

---

## Pull Request Process

### Before Submitting

**Pre-submission checklist:**
- [ ] Tests pass locally
- [ ] Code follows style guide
- [ ] Linter passes
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow guidelines
- [ ] PR description is complete
- [ ] Branch is up-to-date with main

### PR Title

Follow commit message format:
```
<type>(<scope>): <description>
```

### PR Description

Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`):

```markdown
## Description
{What does this PR do?}

## Motivation
{Why is this change needed?}

## Changes
- {Change 1}
- {Change 2}

## Testing
{How was this tested?}

## Screenshots (if applicable)
{Visual changes}

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG updated (if user-facing)
- [ ] Breaking changes noted

## Related Issues
Closes #{issue-number}
```

### PR Size

**Keep PRs small and focused:**
- ✅ Ideal: < 400 lines changed
- ⚠️ Large: 400-1000 lines (needs justification)
- ❌ Too large: > 1000 lines (split into smaller PRs)

**If PR is large:**
- Explain why in description
- Consider breaking into smaller PRs
- Provide clear review guide

### Draft PRs

Use draft PRs for:
- Work in progress
- Early feedback
- Breaking changes discussion

Convert to ready when:
- All checks pass
- Ready for full review
- All comments addressed

---

## Review Process

### Review Timeline

**Expected response time:**
- First review: Within {X} business days
- Follow-up reviews: Within {Y} business days

**If no response:**
- Ping reviewers after {Z} days
- Escalate to maintainers if needed

### Review Checklist

Reviewers will check:
- [ ] Code quality and readability
- [ ] Tests cover new/changed code
- [ ] No security vulnerabilities
- [ ] Performance implications considered
- [ ] Documentation adequate
- [ ] Consistent with project architecture
- [ ] Breaking changes documented

### Addressing Feedback

**How to respond:**
1. Read feedback carefully
2. Ask questions if unclear
3. Make requested changes
4. Respond to each comment
5. Re-request review when ready

**Resolving discussions:**
- Mark resolved when addressed
- Explain your changes
- If disagree, discuss respectfully

### Approval Requirements

**Required approvals:** {approval-count} maintainer(s)

**Merge criteria:**
- All reviews approved
- All checks passing
- No unresolved discussions
- Up-to-date with main branch

### Merge

**Who merges:** {who-can-merge}

**Merge strategy:** {merge-strategy}
- Squash and merge (default)
- Rebase and merge
- Merge commit

---

## Architecture Decisions

### Proposing Changes

**For significant architectural changes:**
1. Open discussion issue
2. Explain problem and proposed solution
3. Gather feedback
4. Create Architecture Decision Record (ADR)
5. Implement after approval

**ADR Template:** See `docs/developer-guide/architecture/decisions/template.md`

### Technology Choices

{From constitution technology principles}

**We prefer:**
- {Technology preference 1}
- {Technology preference 2}

**When proposing new technology:**
- Justify the need
- Compare alternatives
- Consider maintenance burden
- Check license compatibility

---

## Getting Help

### Communication Channels

**For questions:**
- 💬 Discussions: {discussions-url}
- 💬 Slack/Discord: {chat-url}
- 📧 Mailing list: {mailing-list}

**For bugs:**
- 🐛 GitHub Issues: {issues-url}

**For security issues:**
- 🔒 Security email: {security-email}
- Don't post publicly

### Mentorship

**First-time contributor?** Request a mentor:
- Comment on issue: "@maintainers I'd like a mentor for this"
- Join {mentorship-program} if available

### Office Hours

{If applicable}

Join maintainer office hours:
- **When:** {schedule}
- **Where:** {location/link}

---

## Recognition

### Contributors

All contributors are recognized in:
- CONTRIBUTORS.md
- Release notes
- GitHub contributors page

### Maintainer Track

**Interested in becoming a maintainer?**
1. Consistent high-quality contributions
2. Help review PRs
3. Help other contributors
4. Demonstrate project knowledge
5. Nomination by existing maintainers

---

## License

By contributing, you agree that your contributions will be licensed under {license-name}.

See [LICENSE](../LICENSE) for details.

---

## Thank You!

Thank you for contributing to {Project Name}! Your efforts make this project better for everyone.

**Questions?** Don't hesitate to ask in {discussions/chat}.

---

*Last updated: {generation timestamp}*
*Generated from: {constitution.md path}, {code analysis}, {.github/ templates}*
```

## Generation Instructions for AI Agents

### Step 1: Extract Principles from Constitution

```python
principles = extract_principles(constitution.md)

contributing_principles = {
    "values": principles.core_values,
    "coding_standards": principles.technical_standards,
    "development_philosophy": principles.dev_philosophy
}
```

### Step 2: Analyze Code Style

```python
# Detect code style from codebase
code_style = analyze_code_style(codebase)

style_guide = {
    "naming_conventions": code_style.naming_patterns,
    "file_structure": code_style.directory_patterns,
    "formatting": code_style.formatting_rules
}
```

### Step 3: Extract Git Workflow

```python
# Analyze git history
git_history = analyze_git_history()

workflow = {
    "branch_naming": git_history.branch_patterns,
    "commit_format": git_history.commit_patterns,
    "pr_process": analyze_pr_templates(".github/")
}
```

### Step 4: Extract Testing Requirements

```python
test_config = extract_test_config()

testing_requirements = {
    "coverage_threshold": test_config.min_coverage,
    "test_types": test_config.test_suites,
    "test_location": test_config.test_directory
}
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:contributing:workflow -->
{Auto-generated workflow section}
<!-- /speckit:auto:contributing:workflow -->

<!-- MANUAL SECTION - Team-specific guidelines -->
Our team has a weekly sync meeting...
<!-- /MANUAL SECTION -->
```

## Quality Checks

- [ ] All constitution principles reflected
- [ ] Code style matches actual codebase
- [ ] Git workflow matches PR templates
- [ ] Testing requirements align with CI
- [ ] Contact information current
- [ ] Links to related docs work

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
