# Code Review Checklist

## Purpose

Comprehensive checklist for conducting effective code reviews. Ensures consistency, catches issues early, and promotes knowledge sharing.

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    Code Review Priorities                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CORRECTNESS    Does it work? Does it do what it should?     │
│  2. SECURITY       Are there vulnerabilities?                    │
│  3. DESIGN         Is the approach sound?                        │
│  4. READABILITY    Can others understand it?                     │
│  5. PERFORMANCE    Are there obvious issues?                     │
│  6. TESTING        Is it adequately tested?                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pre-Review Checklist

Before starting the review:

```yaml
pre_review:
  - [ ] PR has clear title and description
  - [ ] PR is appropriately sized (< 400 lines ideal)
  - [ ] CI/CD checks are passing
  - [ ] PR is linked to issue/ticket
  - [ ] Self-review completed by author
```

---

## Review Categories

### 1. Correctness

```yaml
correctness:
  logic:
    - [ ] Code does what the PR description says
    - [ ] Edge cases are handled
    - [ ] Error conditions are handled gracefully
    - [ ] No obvious bugs or logic errors

  behavior:
    - [ ] Existing functionality not broken
    - [ ] New functionality works as expected
    - [ ] State management is correct
    - [ ] Async operations handled properly

  data:
    - [ ] Data validation is present
    - [ ] Null/undefined checks where needed
    - [ ] Type conversions are safe
    - [ ] Database operations are correct
```

### 2. Security

```yaml
security:
  input_validation:
    - [ ] User input is sanitized
    - [ ] SQL injection prevented (parameterized queries)
    - [ ] XSS prevention (output encoding)
    - [ ] Command injection prevented

  authentication:
    - [ ] Auth checks present where needed
    - [ ] No hardcoded credentials
    - [ ] Secrets not exposed in logs
    - [ ] Session management secure

  authorization:
    - [ ] Proper permission checks
    - [ ] No privilege escalation
    - [ ] Data access properly scoped

  data_protection:
    - [ ] Sensitive data encrypted
    - [ ] PII handled correctly
    - [ ] Secure communication (HTTPS)
```

### 3. Design & Architecture

```yaml
design:
  patterns:
    - [ ] Follows existing codebase patterns
    - [ ] Single Responsibility Principle
    - [ ] Appropriate abstraction level
    - [ ] No unnecessary complexity

  modularity:
    - [ ] Functions/classes have clear purpose
    - [ ] Dependencies are explicit
    - [ ] Coupling is minimized
    - [ ] Changes are localized

  api_design:
    - [ ] API is intuitive and consistent
    - [ ] Error responses are helpful
    - [ ] Backwards compatible (if applicable)
    - [ ] Well documented
```

### 4. Readability & Maintainability

```yaml
readability:
  naming:
    - [ ] Variables/functions have clear names
    - [ ] Names match conventions
    - [ ] No cryptic abbreviations
    - [ ] Boolean names are predicates

  code_structure:
    - [ ] Functions are reasonably short
    - [ ] Nesting is not too deep
    - [ ] Flow is easy to follow
    - [ ] No dead code

  documentation:
    - [ ] Complex logic is commented
    - [ ] Public APIs are documented
    - [ ] TODOs have tickets
    - [ ] README updated if needed

  formatting:
    - [ ] Consistent with codebase style
    - [ ] Linter rules followed
    - [ ] No unnecessary whitespace changes
```

### 5. Performance

```yaml
performance:
  efficiency:
    - [ ] No N+1 queries
    - [ ] Appropriate data structures used
    - [ ] No obvious memory leaks
    - [ ] Large operations are paginated

  scalability:
    - [ ] Handles expected load
    - [ ] Caching considered where appropriate
    - [ ] Database indexes exist
    - [ ] No blocking operations in hot paths

  resources:
    - [ ] Connections properly closed
    - [ ] Files/streams properly closed
    - [ ] No unnecessary API calls
```

### 6. Testing

```yaml
testing:
  coverage:
    - [ ] New code has tests
    - [ ] Edge cases are tested
    - [ ] Error paths are tested
    - [ ] Critical paths have integration tests

  quality:
    - [ ] Tests are readable
    - [ ] Tests are deterministic
    - [ ] Tests are independent
    - [ ] Mocks are appropriate

  types:
    - [ ] Unit tests for logic
    - [ ] Integration tests for workflows
    - [ ] E2E tests for critical paths (if applicable)
```

---

## Review Comments Guide

### Comment Types

```yaml
comment_types:
  blocking:
    prefix: "🔴 BLOCKING:"
    use: "Must be fixed before merge"
    example: "🔴 BLOCKING: SQL injection vulnerability here"

  suggestion:
    prefix: "🟡 SUGGESTION:"
    use: "Should consider changing"
    example: "🟡 SUGGESTION: This could use a more descriptive name"

  nitpick:
    prefix: "🟢 NIT:"
    use: "Minor, optional change"
    example: "🟢 NIT: Extra blank line"

  question:
    prefix: "❓ QUESTION:"
    use: "Need clarification"
    example: "❓ QUESTION: Why did we choose this approach?"

  praise:
    prefix: "✨"
    use: "Highlight good work"
    example: "✨ Nice refactor, this is much cleaner!"
```

### Effective Comments

```yaml
good_comments:
  - specific: "Point to exact line/issue"
  - actionable: "Explain what to change"
  - respectful: "Focus on code, not person"
  - educational: "Explain why, share knowledge"

  examples:
    good: |
      🟡 SUGGESTION: Consider using `Promise.all()` here instead of
      sequential awaits. This would reduce latency from ~600ms to ~200ms
      since these operations are independent.

    bad: |
      This is wrong.

    good: |
      ❓ QUESTION: I see we're catching all errors here. Was this intentional?
      Some errors (like auth failures) might need different handling.

    bad: |
      Why are you doing this?
```

---

## Review Process

### As a Reviewer

```yaml
reviewer_process:
  1_understand:
    - Read PR description and linked issue
    - Understand the goal and context
    - Check if approach makes sense

  2_review:
    - Start with tests (understand intent)
    - Review file by file
    - Use checklist categories
    - Take notes on patterns

  3_comment:
    - Be specific and actionable
    - Prioritize important issues
    - Acknowledge good work
    - Ask questions if unclear

  4_approve:
    - Approve if no blocking issues
    - Request changes if needed
    - Follow up on your comments
```

### As an Author

```yaml
author_process:
  before_review:
    - Self-review your own code
    - Write clear description
    - Keep PR focused and small
    - Ensure CI passes

  during_review:
    - Respond to all comments
    - Explain decisions if asked
    - Be open to feedback
    - Don't take it personally

  after_review:
    - Address all blocking issues
    - Consider suggestions
    - Re-request review when ready
    - Thank reviewers
```

---

## PR Size Guidelines

```yaml
pr_size:
  ideal:
    lines: "< 200"
    files: "< 10"
    description: "Single focused change"

  acceptable:
    lines: "200-400"
    files: "10-20"
    description: "Related changes, clear scope"

  large:
    lines: "400-800"
    files: "20-40"
    description: "Consider splitting"
    action: "Add detailed description"

  too_large:
    lines: "> 800"
    description: "Difficult to review effectively"
    action: "Split into smaller PRs"
```

---

## Language-Specific Checks

### JavaScript/TypeScript

```yaml
javascript_typescript:
  - [ ] Proper async/await usage (no floating promises)
  - [ ] TypeScript types are accurate (not `any`)
  - [ ] No unused imports/variables
  - [ ] Proper error handling (try/catch)
  - [ ] Environment variables typed
  - [ ] Dependencies are production vs dev correct
```

### Python

```yaml
python:
  - [ ] Type hints present
  - [ ] Docstrings for public functions
  - [ ] Context managers used for resources
  - [ ] No bare except clauses
  - [ ] Requirements properly versioned
```

### React

```yaml
react:
  - [ ] Hooks rules followed
  - [ ] useEffect dependencies correct
  - [ ] Keys in lists are stable
  - [ ] No prop drilling (consider context)
  - [ ] Proper memoization where needed
  - [ ] Accessibility (aria labels, semantic HTML)
```

### SQL

```yaml
sql:
  - [ ] Parameterized queries (no string concat)
  - [ ] Indexes exist for WHERE clauses
  - [ ] No SELECT * in production code
  - [ ] Transactions used appropriately
  - [ ] Migrations are reversible
```

---

## Anti-Patterns to Watch

```yaml
anti_patterns:
  code_smells:
    - "God objects/functions"
    - "Deep nesting (> 3 levels)"
    - "Magic numbers/strings"
    - "Copy-paste code"
    - "Dead code"
    - "Commented out code"

  security_issues:
    - "Hardcoded secrets"
    - "SQL concatenation"
    - "Unvalidated input"
    - "Missing auth checks"
    - "Exposed stack traces"

  performance_issues:
    - "N+1 queries"
    - "Missing indexes"
    - "Unbounded queries"
    - "Synchronous blocking"
    - "Missing pagination"
```

---

## Review Automation

```yaml
automation:
  linting:
    tool: "ESLint/Prettier/Black"
    when: "Pre-commit and CI"
    catches: "Style, simple bugs"

  static_analysis:
    tool: "SonarQube/CodeClimate"
    when: "PR checks"
    catches: "Complexity, duplication"

  security_scanning:
    tool: "Snyk/Dependabot"
    when: "PR checks"
    catches: "Vulnerable dependencies"

  type_checking:
    tool: "TypeScript/mypy"
    when: "Pre-commit and CI"
    catches: "Type errors"

  # Focus human review on:
  # - Logic and correctness
  # - Design decisions
  # - Security implications
  # - Knowledge sharing
```
