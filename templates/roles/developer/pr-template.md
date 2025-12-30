# Pull Request Template

## Purpose

Standardized PR template to ensure clear communication, proper context, and efficient reviews.

---

## PR Template (GitHub)

Create this file at `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary

<!-- Brief description of what this PR does (1-2 sentences) -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactoring (no functional changes)
- [ ] Documentation update
- [ ] Configuration change
- [ ] Test update

## Related Issues

<!-- Link to related issues/tickets -->

Closes #

## Changes Made

<!-- List the main changes in this PR -->

-
-
-

## Testing

<!-- Describe how you tested these changes -->

### Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

### Testing Steps

1.
2.
3.

## Screenshots (if applicable)

<!-- Add screenshots for UI changes -->

| Before | After |
|--------|-------|
|        |       |

## Checklist

<!-- Ensure all items are complete before requesting review -->

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Notes

<!-- Any additional context, decisions made, or things reviewers should know -->

```

---

## Detailed PR Templates by Type

### Feature PR Template

```markdown
## Feature: [Feature Name]

### Summary
<!-- What does this feature do? Why is it needed? -->

### User Story
<!-- As a [user], I want [goal] so that [benefit] -->

### Implementation Details

#### New Components/Modules
-

#### Modified Components/Modules
-

#### API Changes
-

### Testing

#### Happy Path
1.
2.

#### Edge Cases Tested
-

### Screenshots/Demo
<!-- Add screenshots, GIFs, or video for UI changes -->

### Rollback Plan
<!-- How to rollback if something goes wrong -->

### Feature Flag (if applicable)
<!-- Flag name and how to enable/disable -->

Flag: `FEATURE_{{NAME}}`

### Monitoring
<!-- What metrics/logs to watch after deploy -->

-
```

### Bug Fix PR Template

```markdown
## Bug Fix: [Issue Title]

### Problem
<!-- What was happening? Include error messages if applicable -->

### Root Cause
<!-- What caused this issue? -->

### Solution
<!-- How did you fix it? -->

### Reproduction Steps (Before Fix)
1.
2.
3.
Expected:
Actual:

### Verification (After Fix)
1.
2.
3.
Result: Working as expected

### Related Issues
Fixes #

### Tests Added
- [ ] Regression test to prevent recurrence
- [ ] Unit tests for fixed code path

### Impact Assessment
- [ ] Low risk - isolated change
- [ ] Medium risk - touches shared code
- [ ] High risk - affects critical path

### Rollback Plan
<!-- If this fix causes issues -->
```

### Refactoring PR Template

```markdown
## Refactoring: [What's Being Refactored]

### Motivation
<!-- Why is this refactoring needed? -->

- [ ] Code quality improvement
- [ ] Performance optimization
- [ ] Technical debt reduction
- [ ] Preparation for upcoming feature
- [ ] Other:

### Changes

#### Before
<!-- Brief description or code snippet of old approach -->

#### After
<!-- Brief description or code snippet of new approach -->

### What's NOT Changing
<!-- Explicitly state what behavior remains the same -->

### Migration Steps (if applicable)
<!-- For changes that require migration -->

### Testing Strategy
<!-- How did you verify behavior is unchanged? -->

- [ ] All existing tests pass
- [ ] Added tests for edge cases
- [ ] Manual testing of affected flows
- [ ] Performance benchmarks (if applicable)

### Risk Assessment
- [ ] No functional changes expected
- [ ] Tested in staging environment
- [ ] Rollback plan documented
```

### Hotfix PR Template

```markdown
## 🚨 HOTFIX: [Issue]

### Severity
<!-- How severe is this issue? -->

- [ ] P0 - Critical (Production down)
- [ ] P1 - High (Major functionality broken)
- [ ] P2 - Medium (Degraded experience)

### Incident Link
<!-- Link to incident/alert -->

### Problem
<!-- What's happening in production? -->

### Impact
<!-- Who/what is affected? -->

### Fix
<!-- What does this change? -->

### Testing
<!-- How was this tested? Time is critical but don't skip testing -->

- [ ] Locally tested
- [ ] Staging tested (if time permits)
- [ ] Smoke test plan for production

### Deployment Plan
<!-- How will this be deployed? -->

- Target environment: Production
- Deployment method:
- Rollback trigger:

### Post-Deployment Verification
1.
2.

### Follow-up
<!-- What follow-up work is needed? -->

- [ ] Proper fix scheduled: #
- [ ] Post-mortem scheduled
- [ ] Monitoring improved
```

---

## PR Description Best Practices

### Good PR Description

```markdown
## Summary

Add rate limiting to the /api/users endpoint to prevent abuse.
Currently, this endpoint has no rate limiting which could allow
a malicious user to enumerate all users.

## Changes Made

- Added rate limiting middleware using Redis
- Set limit to 100 requests/minute per IP
- Added 429 response with Retry-After header
- Added rate limit metrics to monitoring

## Testing

Tested locally with:
```bash
for i in {1..150}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/users; done
```
Confirmed 429 responses after 100 requests.

## Related

- Security audit finding #123
- Rate limiting RFC: docs/rfcs/rate-limiting.md
```

### Poor PR Description

```markdown
## Summary

Fixed stuff

## Changes

- Updated code
```

---

## Commit Message Convention

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

```yaml
types:
  feat: "New feature"
  fix: "Bug fix"
  docs: "Documentation only"
  style: "Formatting, missing semicolons, etc."
  refactor: "Code change that neither fixes a bug nor adds a feature"
  perf: "Performance improvement"
  test: "Adding or fixing tests"
  build: "Build system or external dependencies"
  ci: "CI configuration"
  chore: "Other changes that don't modify src or test files"
  revert: "Reverts a previous commit"
```

### Examples

```
feat(auth): add OAuth2 login with Google

- Implement Google OAuth2 flow
- Add user profile sync
- Store refresh tokens securely

Closes #123
```

```
fix(api): handle null response from external service

The external service sometimes returns null instead of an empty array.
This caused a TypeError when we tried to iterate over the response.

Fixes #456
```

---

## PR Workflow

```yaml
pr_workflow:
  1_create:
    - Create branch from main
    - Make changes with atomic commits
    - Push and create PR
    - Fill out template completely

  2_draft:
    - Mark as draft if not ready
    - Use for early feedback
    - Run CI checks

  3_review:
    - Request reviewers
    - Address feedback
    - Re-request when ready

  4_approve:
    - Get required approvals
    - Ensure CI passes
    - Resolve all threads

  5_merge:
    - Squash and merge (preferred)
    - Delete branch after merge
    - Verify in staging/production
```

---

## Branch Naming Convention

```yaml
branch_naming:
  format: "<type>/<ticket-id>-<short-description>"

  examples:
    feature: "feat/PROJ-123-add-user-auth"
    bugfix: "fix/PROJ-456-login-error"
    hotfix: "hotfix/PROJ-789-critical-crash"
    refactor: "refactor/PROJ-101-cleanup-api"
    docs: "docs/PROJ-102-update-readme"

  rules:
    - Use lowercase
    - Use hyphens (not underscores)
    - Keep description short (3-5 words)
    - Include ticket number when available
```
