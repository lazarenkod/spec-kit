# Debugging Guide

## Purpose

Systematic approach to debugging issues in production and development environments. Covers common debugging techniques, tools, and best practices.

---

## Debugging Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    Debugging Process                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. REPRODUCE ─────▶ Can you reliably trigger the bug?          │
│         │                                                        │
│         ▼                                                        │
│  2. ISOLATE ───────▶ What's the smallest failing case?          │
│         │                                                        │
│         ▼                                                        │
│  3. IDENTIFY ──────▶ What's the root cause?                     │
│         │                                                        │
│         ▼                                                        │
│  4. FIX ───────────▶ What's the correct solution?               │
│         │                                                        │
│         ▼                                                        │
│  5. VERIFY ────────▶ Is the bug actually fixed?                 │
│         │                                                        │
│         ▼                                                        │
│  6. PREVENT ───────▶ How do we prevent recurrence?              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Reproduce the Bug

### Questions to Answer

```yaml
reproduction:
  what:
    - "What is the expected behavior?"
    - "What is the actual behavior?"
    - "What error messages appear?"

  when:
    - "When did this start happening?"
    - "Does it happen every time or intermittently?"
    - "What time of day? Under what load?"

  where:
    - "Which environment? (prod/staging/local)"
    - "Which browser/device/OS?"
    - "Which user account or data?"

  how:
    - "What are the exact steps to reproduce?"
    - "What data/state is required?"
    - "Are there any preconditions?"
```

### Reproduction Checklist

```yaml
reproduction_checklist:
  - [ ] Exact steps documented
  - [ ] Environment identified
  - [ ] Data/state requirements noted
  - [ ] Reproduction rate known (100%? 10%?)
  - [ ] Screenshots/videos captured
  - [ ] Error messages/stack traces saved
```

---

## Step 2: Isolate the Problem

### Isolation Techniques

```yaml
isolation_techniques:
  binary_search:
    description: "Divide and conquer to find the breaking change"
    use_when: "Bug appeared after a change"
    method: |
      1. Identify working and broken versions
      2. Test the midpoint
      3. Narrow down until you find the breaking commit
    tool: "git bisect"

  elimination:
    description: "Remove components until bug disappears"
    use_when: "Complex system with many parts"
    method: |
      1. List all components involved
      2. Remove/disable one at a time
      3. Note when bug disappears
      4. Focus on that component

  substitution:
    description: "Replace components with known-good versions"
    use_when: "Suspecting a specific component"
    method: |
      1. Replace suspected component with mock
      2. If bug disappears, problem is in that component
      3. If bug persists, look elsewhere

  simplification:
    description: "Create minimal reproduction case"
    use_when: "Complex scenario"
    method: |
      1. Start with full failing case
      2. Remove unnecessary parts
      3. Keep only essential elements
      4. Share minimal case for collaboration
```

### Git Bisect

```bash
# Find the commit that introduced a bug
git bisect start
git bisect bad                 # Current version is broken
git bisect good v1.0.0         # This version was working

# Git checks out middle commit, test it
# If broken:
git bisect bad
# If working:
git bisect good

# Repeat until git identifies the breaking commit
# When done:
git bisect reset
```

---

## Step 3: Identify Root Cause

### Debugging Tools

```yaml
debugging_tools:
  logging:
    purpose: "Trace execution flow"
    levels:
      - ERROR: "Failures that need attention"
      - WARN: "Potential problems"
      - INFO: "Normal operations"
      - DEBUG: "Detailed diagnostic info"
    tips:
      - "Add context (request ID, user ID)"
      - "Log before and after operations"
      - "Include relevant data (sanitized)"

  debugger:
    purpose: "Step through code execution"
    tools:
      - "VS Code debugger"
      - "Chrome DevTools"
      - "pdb (Python)"
      - "node --inspect"
    tips:
      - "Set breakpoints strategically"
      - "Watch key variables"
      - "Use conditional breakpoints"

  profiler:
    purpose: "Find performance issues"
    tools:
      - "Chrome DevTools Performance"
      - "Node.js --prof"
      - "Python cProfile"
    tips:
      - "Profile in realistic conditions"
      - "Look for hot paths"
      - "Check memory usage"

  network_tools:
    purpose: "Debug API/network issues"
    tools:
      - "Chrome Network tab"
      - "curl/httpie"
      - "Postman"
      - "tcpdump/Wireshark"

  database_tools:
    purpose: "Debug data issues"
    tools:
      - "Query EXPLAIN"
      - "Slow query log"
      - "pg_stat_statements"
```

### Strategic Logging

```typescript
// Bad: Uninformative logging
console.log('here');
console.log(data);

// Good: Contextual logging
logger.info('Processing order', {
  orderId: order.id,
  userId: order.userId,
  amount: order.total,
  step: 'validation'
});

logger.error('Payment failed', {
  orderId: order.id,
  error: error.message,
  errorCode: error.code,
  paymentProvider: 'stripe'
});
```

### Common Root Causes

```yaml
common_causes:
  data_issues:
    - "Null/undefined values"
    - "Incorrect data types"
    - "Stale/cached data"
    - "Missing required fields"
    - "Data migration issues"

  timing_issues:
    - "Race conditions"
    - "Deadlocks"
    - "Timeout handling"
    - "Async operation ordering"
    - "Clock skew"

  environment_issues:
    - "Missing environment variables"
    - "Wrong environment config"
    - "Dependency version mismatch"
    - "Resource limits (memory, CPU)"
    - "Network configuration"

  integration_issues:
    - "API contract changes"
    - "Authentication/authorization"
    - "Rate limiting"
    - "Network connectivity"
    - "Service unavailability"

  code_issues:
    - "Logic errors"
    - "Off-by-one errors"
    - "Type coercion bugs"
    - "Memory leaks"
    - "Unhandled exceptions"
```

---

## Step 4: Fix the Bug

### Fix Quality Checklist

```yaml
fix_quality:
  correctness:
    - [ ] Fix addresses root cause (not symptom)
    - [ ] Fix doesn't break other functionality
    - [ ] Edge cases considered

  safety:
    - [ ] Change is minimal and focused
    - [ ] Rollback plan exists
    - [ ] No security implications

  testing:
    - [ ] Regression test added
    - [ ] Existing tests still pass
    - [ ] Manual verification completed
```

### Common Fix Patterns

```yaml
fix_patterns:
  null_check:
    problem: "TypeError: Cannot read property of undefined"
    fix: "Add null check or optional chaining"
    example: "user?.profile?.name"

  error_handling:
    problem: "Unhandled promise rejection"
    fix: "Add try/catch or .catch()"
    example: "try { await operation() } catch (e) { handleError(e) }"

  validation:
    problem: "Invalid input causes crash"
    fix: "Validate input at boundaries"
    example: "if (!isValid(input)) return error"

  timeout:
    problem: "Operation hangs indefinitely"
    fix: "Add timeout with fallback"
    example: "Promise.race([operation(), timeout(5000)])"

  retry:
    problem: "Transient failures"
    fix: "Add retry with backoff"
    example: "retry(operation, { maxAttempts: 3, backoff: 'exponential' })"
```

---

## Step 5: Verify the Fix

### Verification Checklist

```yaml
verification:
  local:
    - [ ] Bug no longer reproduces with original steps
    - [ ] Unit tests pass
    - [ ] Integration tests pass
    - [ ] Manual testing completed

  staging:
    - [ ] Deploy to staging
    - [ ] Verify fix in staging environment
    - [ ] Check for side effects

  production:
    - [ ] Deploy with monitoring
    - [ ] Watch error rates
    - [ ] Verify with original reporter
```

---

## Step 6: Prevent Recurrence

### Prevention Strategies

```yaml
prevention:
  testing:
    - "Add regression test for this specific bug"
    - "Add tests for similar edge cases"
    - "Improve test coverage in affected area"

  code_quality:
    - "Add type checking"
    - "Add validation"
    - "Improve error handling"
    - "Add defensive coding"

  monitoring:
    - "Add alerts for this failure mode"
    - "Improve logging around affected area"
    - "Add metrics for visibility"

  process:
    - "Update code review checklist"
    - "Document gotchas for team"
    - "Consider architectural changes"
```

---

## Production Debugging

### Safe Production Debugging

```yaml
production_debugging:
  DO:
    - "Use read-only operations"
    - "Check logs and metrics first"
    - "Use feature flags to isolate"
    - "Test in staging first"
    - "Have rollback ready"

  DO_NOT:
    - "Debug directly on production DB"
    - "Add console.log to production"
    - "Make untested changes"
    - "Disable security controls"
    - "Share production credentials"

  tools:
    - "Centralized logging (DataDog, Splunk)"
    - "Error tracking (Sentry)"
    - "APM (New Relic, DataDog)"
    - "Feature flags (LaunchDarkly)"
```

### Production Incident Response

```yaml
incident_response:
  1_assess:
    - "What is the impact?"
    - "How many users affected?"
    - "Is it getting worse?"

  2_communicate:
    - "Alert the team"
    - "Update status page"
    - "Notify stakeholders"

  3_mitigate:
    - "Can we rollback?"
    - "Can we disable the feature?"
    - "Can we redirect traffic?"

  4_fix:
    - "Root cause analysis"
    - "Develop fix"
    - "Test fix"
    - "Deploy fix"

  5_follow_up:
    - "Post-mortem"
    - "Preventive measures"
    - "Documentation update"
```

---

## Debugging Checklist by Error Type

### JavaScript/TypeScript Errors

```yaml
js_errors:
  TypeError:
    likely_causes:
      - "Accessing property on null/undefined"
      - "Calling non-function as function"
      - "Wrong argument type"
    debug_steps:
      - "Check variable values at crash point"
      - "Add null checks"
      - "Verify API response shape"

  ReferenceError:
    likely_causes:
      - "Variable not defined"
      - "Typo in variable name"
      - "Scope issues"
    debug_steps:
      - "Check spelling"
      - "Verify import statements"
      - "Check variable scope"

  NetworkError:
    likely_causes:
      - "CORS issues"
      - "Server down"
      - "Wrong URL"
    debug_steps:
      - "Check Network tab"
      - "Verify URL"
      - "Check CORS headers"
```

### API Errors

```yaml
api_errors:
  400_Bad_Request:
    likely_causes:
      - "Invalid request body"
      - "Missing required fields"
      - "Wrong data types"
    debug_steps:
      - "Log request body"
      - "Check validation rules"
      - "Compare with API docs"

  401_Unauthorized:
    likely_causes:
      - "Missing auth token"
      - "Expired token"
      - "Invalid credentials"
    debug_steps:
      - "Check auth header"
      - "Verify token validity"
      - "Check token refresh logic"

  500_Server_Error:
    likely_causes:
      - "Unhandled exception"
      - "Database error"
      - "External service failure"
    debug_steps:
      - "Check server logs"
      - "Check error tracking"
      - "Trace request ID"
```

### Database Errors

```yaml
database_errors:
  connection_error:
    likely_causes:
      - "Wrong credentials"
      - "Network issue"
      - "Connection pool exhausted"
    debug_steps:
      - "Verify connection string"
      - "Check network connectivity"
      - "Monitor connection pool"

  timeout:
    likely_causes:
      - "Slow query"
      - "Deadlock"
      - "Resource contention"
    debug_steps:
      - "Run EXPLAIN on query"
      - "Check for missing indexes"
      - "Monitor active connections"

  constraint_violation:
    likely_causes:
      - "Duplicate key"
      - "Foreign key missing"
      - "NULL in NOT NULL column"
    debug_steps:
      - "Check constraint definition"
      - "Verify data integrity"
      - "Check related records"
```

---

## Debugging Mindset

```yaml
debugging_mindset:
  principles:
    - "The bug is in your code (usually)"
    - "Read the error message carefully"
    - "Trust nothing, verify everything"
    - "Recent changes are prime suspects"
    - "If you're stuck, take a break"
    - "Rubber duck debugging works"
    - "Ask for help sooner rather than later"

  questions_to_ask:
    - "What changed recently?"
    - "What am I assuming that might be wrong?"
    - "What haven't I checked yet?"
    - "Is this the same bug or a different one?"
    - "Would explaining this to someone help?"
```
