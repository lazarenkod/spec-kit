# QA Anti-Patterns Database

## Overview

This database catalogs common QA and testing anti-patterns that undermine software quality. Each anti-pattern includes detection methods, consequences, root causes, and remediation strategies.

**Usage**: Reference during test planning, test strategy reviews, and QA process audits.

---

## QA-001: Chasing 100% Code Coverage

### Description
Obsessing over code coverage metrics as the primary quality indicator, leading to meaningless tests that provide false confidence.

### Detection Signals
- Coverage gates block releases (e.g., "must be 80%+")
- Tests exist solely to satisfy coverage
- Tests verify implementation, not behavior
- High coverage but bugs still escape
- "Coverage went down" is a blocker

### Coverage Illusion
```text
100% Coverage ≠ Bug-Free Code

Example:
function divide(a, b) {
    return a / b;  // 100% coverage possible
}

test('divide works') {
    expect(divide(10, 2)).toBe(5); // ✓ Covered
}

// But misses: divide(1, 0) → Infinity ← BUG
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Metric fixation | "We need a number" |
| Management pressure | "What % are we at?" |
| Tool default | Coverage tools prominent |
| False equivalence | Coverage = Quality belief |
| Box checking | Compliance over effectiveness |

### Consequences
| Impact | Description |
|--------|-------------|
| Meaningless tests | Tests written for coverage, not value |
| Maintenance burden | More tests = more maintenance |
| False confidence | "We're covered" but bugs escape |
| Slow builds | Excessive test execution |
| Developer resentment | "These tests add nothing" |

### Remediation

**Risk-Based Coverage Strategy**:
```text
INSTEAD OF: 80% coverage everywhere

USE:
┌─────────────────────────────────────────────┐
│ Risk Level        Coverage Target           │
├─────────────────────────────────────────────┤
│ Critical paths    95%+ (payment, auth)      │
│ Core business     80%+ (main features)      │
│ Utilities         60%+ (helpers, utils)     │
│ Generated code    0% (auto-generated)       │
│ UI layouts        Manual review preferred   │
└─────────────────────────────────────────────┘
```

**Mutation Testing Supplement**:
```text
Coverage: "Was this line executed?"
Mutation: "Would a bug here be caught?"

Example:
if (age >= 18) { allow(); }  // Covered

Mutations:
- if (age > 18) { allow(); }   // Caught?
- if (age >= 17) { allow(); }  // Caught?
- if (age <= 18) { allow(); }  // Caught?

Mutation Score = Killed Mutants / Total Mutants
Better indicator than coverage alone.
```

### Prevention Checklist
- [ ] Coverage targets risk-adjusted
- [ ] Mutation testing supplements coverage
- [ ] Test quality reviews (not just quantity)
- [ ] Critical paths have higher bar

---

## QA-002: Only Happy Path Testing

### Description
Testing only successful scenarios while ignoring error cases, edge conditions, and failure modes. The "works on my machine" of testing.

### Detection Signals
- All tests pass but users report errors
- No error state tests
- No boundary condition tests
- No concurrent access tests
- "We didn't test that scenario"

### Test Gap Analysis
```text
HAPPY PATH (typically tested):
User enters valid data → System accepts → Success

MISSING:
├── Invalid input (empty, too long, wrong format)
├── Boundary conditions (min-1, max+1)
├── Error states (network fail, timeout)
├── Concurrent access (race conditions)
├── Permission edge cases (expired, revoked)
├── State transitions (valid → invalid)
└── Resource exhaustion (memory, disk, rate limits)
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Time pressure | "Test the main flow first" |
| Optimism bias | "That won't happen in prod" |
| Incomplete specs | Specs don't cover errors |
| Developer mindset | "Why would user do that?" |
| Manual testing gaps | Hard to simulate errors |

### Remediation

**Test Quadrant Approach**:
```text
┌─────────────────────┬─────────────────────┐
│ Business-Facing     │ Business-Facing     │
│ Supporting Dev      │ Critique Product    │
│                     │                     │
│ Functional Tests    │ Exploratory Testing │
│ Story Tests         │ Usability Testing   │
│ Simulations         │ UAT                 │
├─────────────────────┼─────────────────────┤
│ Technology-Facing   │ Technology-Facing   │
│ Supporting Dev      │ Critique Product    │
│                     │                     │
│ Unit Tests          │ Performance Tests   │
│ Component Tests     │ Security Tests      │
│ Integration Tests   │ "-ility" Tests      │
└─────────────────────┴─────────────────────┘
```

**Edge Case Checklist per Feature**:
```text
INPUT VALIDATION:
☐ Empty input
☐ Maximum length input
☐ Minimum length input
☐ Special characters
☐ SQL injection attempts
☐ XSS payloads
☐ Unicode characters
☐ Null/undefined

BOUNDARY CONDITIONS:
☐ Zero values
☐ Negative values
☐ Maximum integer
☐ Boundary ± 1
☐ Empty collections
☐ Single item collections
☐ Maximum collection size

ERROR STATES:
☐ Network timeout
☐ Network failure
☐ Server error (500)
☐ Not found (404)
☐ Permission denied (403)
☐ Rate limited (429)
☐ Concurrent modification

STATE TRANSITIONS:
☐ Valid to valid
☐ Valid to invalid
☐ Invalid to valid
☐ Interrupted transitions
```

### Prevention Checklist
- [ ] Error cases in acceptance criteria
- [ ] Edge case coverage in test plans
- [ ] Negative test cases required
- [ ] Exploratory testing time budgeted

---

## QA-003: Flaky Test Tolerance

### Description
Accepting intermittent test failures as normal. "Just run it again" culture that erodes test suite reliability and developer trust.

### Detection Signals
- CI passes "on retry"
- Tests marked @flaky or @skip
- "That test always fails first time"
- Developers don't trust test results
- Same test fails differently each run

### Flakiness Sources
```text
TIMING ISSUES:
├── Race conditions in async code
├── Hardcoded waits (sleep(1000))
├── Clock-dependent tests
└── Order-dependent tests

ENVIRONMENT ISSUES:
├── Shared test state
├── External service dependencies
├── Database pollution
└── Port conflicts

RESOURCE ISSUES:
├── Memory pressure
├── Slow CI machines
├── Network variability
└── File system timing
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Time pressure | "Fix it later, ship now" |
| Normalization | "That test is just flaky" |
| Difficulty | "Hard to reproduce" |
| No ownership | "Not my test" |
| Wrong solution | Mark skip vs fix |

### Consequences
| Impact | Description |
|--------|-------------|
| CI distrust | Developers ignore failures |
| Increased cycle time | Re-runs, manual verification |
| Hidden real failures | Flakiness masks real bugs |
| Test suite rot | Accumulating @skip tags |
| Developer frustration | "Tests are waste of time" |

### Remediation

**Flakiness Elimination Protocol**:
```text
DETECTION:
- Track test consistency over time
- Flag tests with >1% failure rate
- Dashboard for flaky test visibility

QUARANTINE:
- Move flaky tests to quarantine suite
- Run separately from main CI
- Clear ownership for fixing

ANALYSIS:
- Reproduce locally
- Add logging/diagnostics
- Identify root cause

FIX:
- Make test deterministic
- Remove timing dependencies
- Isolate from shared state

PREVENTION:
- Review for timing issues in PR
- No new flaky tests policy
- Delete tests that can't be fixed
```

**Common Fixes**:
| Problem | Fix |
|---------|-----|
| Race condition | Proper async/await, wait for condition |
| Shared state | Isolated test fixtures, fresh DB per test |
| Time dependency | Mock time, use relative durations |
| External service | Mock external calls, contract tests |
| Order dependency | Independent test setup/teardown |

### Prevention Checklist
- [ ] Zero tolerance for new flaky tests
- [ ] Flaky tests tracked and owned
- [ ] Quarantine process established
- [ ] Root cause analysis required

---

## QA-004: Ice Cream Cone Test Pyramid

### Description
Inverted test pyramid with most tests at the UI/E2E level and few unit tests. Slow, brittle, expensive test suite.

### Detection Signals
- E2E tests run 30+ minutes
- Test failures cascade (one break, many failures)
- Hard to identify what broke
- Flakiness epidemic
- "We test through the UI"

### Test Pyramid vs Ice Cream Cone
```text
CORRECT (Pyramid):          ANTI-PATTERN (Ice Cream):
                            ┌─────────────────────┐
       ▲                    │      Manual         │
      /E2E\                 │      Testing        │
     /─────\                ├─────────────────────┤
    / Integ \               │                     │
   /─────────\              │        E2E          │
  /   Unit    \             │    (Selenium, etc)  │
 /─────────────\            │                     │
                            ├─────────────────────┤
Fast, isolated,             │    Integration      │
cheap, stable               ├─────────────────────┤
                            │    Unit (few)       │
                            └─────────────────────┘

                            Slow, brittle,
                            expensive, flaky
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| QA-driven testing | Testers test through UI |
| Late testing | Testing after code, not TDD |
| Legacy code | Can't unit test without refactoring |
| Tool familiarity | Know Selenium, not unit testing |
| "Real" testing | "UI tests are closer to user" |

### Consequences
| Impact | Description |
|--------|-------------|
| Slow feedback | Minutes to hours vs seconds |
| Flakiness | UI tests inherently flaky |
| Debugging difficulty | Many layers to diagnose |
| Maintenance cost | UI changes break many tests |
| Parallel limits | E2E tests harder to parallelize |

### Remediation

**Right Pyramid Distribution**:
```text
Recommended Ratio:
Unit:Integration:E2E = 70:20:10

Example for 1000 tests:
├── Unit Tests: 700 (fast, isolated, specific)
├── Integration: 200 (component interactions)
└── E2E: 100 (critical user journeys only)

Total execution time target:
├── Unit: < 5 minutes
├── Integration: < 10 minutes
└── E2E: < 15 minutes
```

**Test Level Selection Guide**:
| What to Test | Test Level |
|--------------|------------|
| Business logic | Unit |
| Data transformations | Unit |
| API contracts | Integration |
| Database queries | Integration |
| Critical user journeys | E2E |
| UI component rendering | Component (snapshot) |

**Migration Strategy**:
```text
Phase 1: Stop adding E2E tests
         └── New tests at lowest possible level

Phase 2: Extract unit tests from E2E
         └── Identify logic tested via E2E
         └── Write unit tests for that logic

Phase 3: Reduce E2E to smoke tests
         └── Keep only critical path E2E
         └── Delete redundant E2E

Phase 4: Establish CI time budget
         └── Total test time < 20 minutes
```

### Prevention Checklist
- [ ] Test pyramid ratios in DoD
- [ ] CI time budget enforced
- [ ] New features start with unit tests
- [ ] E2E only for critical journeys

---

## QA-005: Testing After Development

### Description
Testing as a phase after development rather than integrated throughout. QA as gate-keeper, not quality partner.

### Detection Signals
- "Throw it over the wall to QA"
- Bug rate spikes at end of sprint
- QA backlog builds up
- Developers don't write tests
- "We'll test it in staging"

### Cost of Late Testing
```text
Bug Found At:         Relative Fix Cost:
─────────────────────────────────────────
Requirements          1x
Design               5x
Development          10x
Testing              20x
Production           100x+

Late testing = expensive testing
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Organizational silos | Dev and QA separate teams |
| Waterfall legacy | Phases die hard |
| Skill separation | "Devs don't test" |
| Time pressure | "Ship first, test later" |
| Tooling gaps | Testing is hard |

### Remediation

**Shift-Left Testing Strategy**:
```text
WATERFALL:
Design → Develop → [Test] → Deploy
                      ↑
            Testing at the end

SHIFT-LEFT:
[Test] → Design → [Test] → Develop → [Test] → Deploy
   ↑                ↑                    ↑
Requirements    Design review       Continuous testing
validation      Testing criteria    TDD, CI/CD
```

**Testing by Phase**:
| Phase | Testing Activity |
|-------|------------------|
| Requirements | Testability review, test criteria |
| Design | API contract tests, test plan |
| Development | TDD, unit tests, component tests |
| Code Review | Test review, coverage check |
| Integration | Integration tests, contract tests |
| Deployment | Smoke tests, canary verification |
| Production | Monitoring, synthetic tests |

**TDD Flow**:
```text
1. Write failing test (RED)
   └── Define expected behavior

2. Write minimal code (GREEN)
   └── Make test pass, nothing more

3. Refactor (REFACTOR)
   └── Improve code, tests still pass

Repeat for each behavior.
Tests exist before code.
```

### Prevention Checklist
- [ ] Tests required in PR
- [ ] TDD encouraged/required
- [ ] QA involved in requirements
- [ ] Shift-left practices in DoD

---

## QA-006: No Test Isolation

### Description
Tests that depend on shared state, external services, or execution order. One test's side effects affect another test's results.

### Detection Signals
- Tests pass individually, fail together
- Test order matters
- "Run tests in this order"
- Database populated with test data
- Tests modify shared resources

### Isolation Failures
```text
SHARED STATE PROBLEM:
Test A: Creates user "john@test.com"
Test B: Expects no users exist → FAILS

ORDER DEPENDENCY:
Test 1: Creates order
Test 2: Assumes order exists → FAILS if run alone

EXTERNAL DEPENDENCY:
Test A: Calls real payment API
Test B: Rate limited → FAILS intermittently
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Convenience | "Just use existing data" |
| Setup complexity | "Hard to create isolated state" |
| External services | "Easier than mocking" |
| Database testing | "Need real database" |
| Test evolution | "Originally worked alone" |

### Remediation

**Test Isolation Patterns**:
```text
1. FRESH DATABASE PER TEST
   - Create schema
   - Seed minimal data
   - Run test
   - Rollback/destroy

2. TRANSACTION ROLLBACK
   - Begin transaction
   - Run test
   - Rollback (never commit)

3. UNIQUE DATA PER TEST
   - Generate unique identifiers
   - No collisions between tests
   - Clean up after each test

4. MOCK EXTERNAL SERVICES
   - In-memory doubles
   - Recorded responses (VCR)
   - Contract tests separate
```

**Isolation Verification**:
```text
Tests must pass in any order:
- Run: test1, test2, test3 ✓
- Run: test3, test1, test2 ✓
- Run: test2 (alone) ✓

Shuffle test order in CI:
- Jest: --randomize
- pytest: pytest-random-order
- JUnit: @Order not used
```

**External Service Isolation**:
| Dependency | Isolation Strategy |
|------------|---------------------|
| Database | Transaction rollback, in-memory |
| HTTP APIs | Mock server, recorded responses |
| Message queues | In-memory stub |
| File system | Temp directories |
| Time/clock | Mock time library |
| Random | Seeded generator |

### Prevention Checklist
- [ ] Tests run in random order
- [ ] Each test creates own data
- [ ] External services mocked
- [ ] No shared mutable state

---

## QA-007: Ignoring Exploratory Testing

### Description
Over-reliance on automated tests while neglecting exploratory testing. Missing bugs that automated tests can't catch.

### Detection Signals
- 100% automated, 0% exploratory
- No test charters or sessions
- "Automated tests cover everything"
- UX issues found by users
- Edge cases discovered in production

### What Automation Misses
```text
AUTOMATED TESTS VERIFY:
├── Expected behavior (defined upfront)
├── Regression (known paths)
└── Specific scenarios (scripted)

EXPLORATORY TESTING FINDS:
├── Unexpected behavior
├── Usability issues
├── Edge case combinations
├── State corruption
├── Visual/layout issues
├── Performance under strange conditions
└── "I wonder what happens if..."
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Automation focus | "Automate everything" |
| Undervalued skill | "Anyone can click around" |
| Time pressure | "No time for exploration" |
| Metrics obsession | "Can't measure exploratory" |
| Talent gap | Exploration is a skill |

### Remediation

**Exploratory Testing Charters**:
```text
CHARTER TEMPLATE:
Explore [target]
With [resources/constraints]
To discover [information sought]

EXAMPLE:
Explore: checkout flow
With: slow network simulation, multiple concurrent tabs
To discover: race conditions and error handling gaps

TIME BOX: 45 minutes
```

**Session-Based Test Management**:
```text
SESSION STRUCTURE:
├── Charter (5 min): Define focus
├── Exploration (45 min): Test and document
├── Debrief (10 min): Report findings

OUTPUT:
├── Bugs found
├── Questions raised
├── Coverage notes
├── Charter suggestions
```

**Exploration Techniques**:
| Technique | Description |
|-----------|-------------|
| Tours | Navigation, feature, scenario tours |
| SFDPOT | Structure, Function, Data, Platform, Operations, Time |
| Boundaries | Min, max, empty, special values |
| Disruption | Network fail, back button, refresh |
| Personae | Novice, expert, malicious, impatient |
| Combinations | Unlikely feature combinations |

### Prevention Checklist
- [ ] Exploratory testing in sprint planning
- [ ] Charter-based sessions scheduled
- [ ] Findings documented and tracked
- [ ] Mix of automated and exploratory

---

## QA-008: Production-Only Testing

### Description
First real testing happens in production. No staging, no pre-production validation, no safe environment to verify changes.

### Detection Signals
- "Deploy to prod and see"
- No staging environment
- Staging differs from production
- No smoke tests post-deploy
- Users discover bugs

### Testing Environment Gap
```text
MISSING:
Local → [?] → Production

NEEDED:
Local → CI → Staging → [Canary →] Production
         ↓        ↓            ↓
    Automated  Manual      Real traffic
    tests      testing     subset
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Cost | "Environments are expensive" |
| Complexity | "Too hard to replicate prod" |
| Speed | "Just push to prod" |
| Small scale | "We're small, it's fine" |
| Data issues | "Can't copy prod data" |

### Remediation

**Environment Strategy**:
```text
ENVIRONMENT PIPELINE:
1. LOCAL
   └── Developer testing, unit tests

2. CI/CD
   └── Automated tests, linting, security

3. STAGING
   └── Integration tests, manual testing
   └── Mirror production config

4. CANARY (optional)
   └── 1% production traffic
   └── Automatic rollback on errors

5. PRODUCTION
   └── Full rollout
   └── Monitoring and alerting
```

**Staging Parity Checklist**:
```text
Staging should match production in:
☐ Infrastructure (containers, serverless, etc.)
☐ Configuration (same env vars structure)
☐ Dependencies (same versions)
☐ Database schema (migration tested)
☐ External service connections (mocked or sandbox)
☐ Network topology (load balancer, etc.)

Acceptable differences:
☐ Scale (smaller instances OK)
☐ Data volume (subset OK)
☐ Third-party integrations (sandbox OK)
```

**Progressive Rollout**:
```text
Stage 1: Deploy to staging
         └── Smoke tests pass

Stage 2: Deploy to canary (1% traffic)
         └── Monitor error rates
         └── Auto-rollback if errors spike

Stage 3: Gradual rollout (10% → 50% → 100%)
         └── Monitor at each stage
         └── Manual approval or automatic
```

### Prevention Checklist
- [ ] Staging environment exists
- [ ] Staging mirrors production config
- [ ] Smoke tests post-deploy
- [ ] Rollback capability tested

---

## QA-009: Untested Error Paths

### Description
Testing only successful paths while error handling code remains untested. Errors in production reveal untested recovery code.

### Detection Signals
- Error handling code never executed in tests
- "Catch blocks" without test coverage
- Error messages discovered in production
- Recovery mechanisms untested
- Fallback behaviors unknown

### Error Path Debt
```text
CODE:
try {
    result = callExternalService();  // Tested ✓
} catch (TimeoutError) {
    showRetryDialog();               // Untested ✗
    logError();                      // Untested ✗
    notifyOps();                     // Untested ✗
} catch (AuthError) {
    redirectToLogin();               // Untested ✗
}

Error paths often contain:
- Incorrect error messages
- Missing logging
- Broken recovery logic
- State corruption
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Happy path focus | Optimism in testing |
| Difficulty | Hard to trigger errors |
| Code structure | Errors buried in callbacks |
| Coverage metrics | Focus on line coverage |
| Time pressure | "Main flow first" |

### Remediation

**Error Injection Testing**:
```text
TECHNIQUES:
1. Mock to throw exceptions
2. Chaos engineering (kill services)
3. Network failure simulation
4. Timeout injection
5. Resource exhaustion

EXAMPLE:
test('handles API timeout gracefully') {
    mockApi.rejectWith(new TimeoutError());

    renderComponent();

    expect(screen.getByText('Request timed out')).toBeVisible();
    expect(screen.getByRole('button', {name: 'Retry'})).toBeVisible();
    expect(logSpy).toHaveBeenCalledWith('API_TIMEOUT');
}
```

**Error Scenario Coverage**:
| Scenario | Test Approach |
|----------|---------------|
| Network failure | Mock network layer |
| Timeout | Mock with delay + timeout |
| Auth expired | Return 401 in mock |
| Rate limited | Return 429 in mock |
| Invalid data | Return malformed response |
| Partial failure | Mock some calls succeed, some fail |
| Recovery | Verify retry logic works |

**Chaos Testing Framework**:
```text
1. FAILURE INJECTION
   ├── Random service termination
   ├── Latency injection
   └── Error response injection

2. VERIFICATION
   ├── System degrades gracefully
   ├── Error messages correct
   ├── Logging captures context
   └── Recovery works

3. AUTOMATION
   ├── Run in CI/CD
   └── Regular chaos runs
```

### Prevention Checklist
- [ ] Error paths explicitly tested
- [ ] Chaos testing implemented
- [ ] Error messages verified
- [ ] Recovery mechanisms tested

---

## QA-010: Manual Regression Forever

### Description
Performing full regression testing manually every release instead of automating stable functionality. Time wasted on repetitive checking.

### Detection Signals
- "We need 2 weeks for regression"
- Manual test scripts hundreds of pages
- Same tests run every release
- QA team is bottleneck
- Regression found late in cycle

### Manual Regression Cost
```text
EVERY RELEASE:
├── 100 test cases × 30 min each = 50 hours
├── 2 testers = 25 hours each
├── Opportunity cost of automation
└── Delayed feedback (days not minutes)

AUTOMATION:
├── Initial investment: 200 hours
├── Each run: 30 minutes (automated)
├── Payback: 4 releases
└── Continuous execution possible
```

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Lack of skill | "We don't know automation" |
| Legacy UI | Hard to automate |
| Time pressure | "No time to automate" |
| Process inertia | "This is how we do it" |
| Short-term thinking | Immediate cost vs long-term gain |

### Remediation

**Automation Prioritization Matrix**:
```text
                  High Frequency
                       │
    AUTOMATE           │        AUTOMATE
    FIRST              │        FIRST
    (Smoke tests,      │        (Critical paths,
    login flows)       │        checkout)
                       │
───────────────────────┼───────────────────────
                       │
    MANUAL OK          │        AUTOMATE
    (One-time          │        LATER
    scenarios)         │        (Edge cases)
                       │
                  Low Frequency

Prioritize by: Frequency × Risk × Manual Effort
```

**Automation Strategy**:
```text
PHASE 1: Critical Path Automation
├── Login/logout
├── Core user journey
├── Payment flows
└── Data creation/deletion

PHASE 2: Regression Automation
├── Stable features (low change rate)
├── High-frequency scenarios
└── Time-consuming manual tests

PHASE 3: Edge Case Automation
├── Boundary conditions
├── Error scenarios
└── Complex state transitions

PHASE 4: Continuous Improvement
├── Reduce manual regression to exploratory
└── Run automation continuously
```

**Automation ROI Calculation**:
```text
ROI = (Manual Cost Saved - Automation Cost) / Automation Cost

Manual Cost per Release = Hours × Runs × Hourly Rate
Automation Cost = Development + Maintenance

EXAMPLE:
Manual: 40 hours × 12 releases × $50 = $24,000/year
Automation: 100 hours dev × $75 + 20 hours/year maintenance = $8,250

ROI = ($24,000 - $8,250) / $8,250 = 191%
```

### Prevention Checklist
- [ ] Automation backlog maintained
- [ ] New features include automation
- [ ] Manual regression minimized
- [ ] Automation runs in CI/CD

---

## Quick Reference: Anti-Pattern Detection Matrix

| Anti-Pattern | Quick Detection | Immediate Action |
|--------------|-----------------|------------------|
| QA-001: 100% Coverage | Coverage-only gates | Risk-based coverage targets |
| QA-002: Happy Path Only | Bugs in error states | Edge case checklist |
| QA-003: Flaky Tolerance | "Just rerun it" | Quarantine and fix |
| QA-004: Ice Cream Cone | E2E >> Unit tests | Invert the pyramid |
| QA-005: Test After Dev | QA bottleneck | Shift-left testing |
| QA-006: No Isolation | Tests fail together | Isolate all tests |
| QA-007: No Exploratory | Only automation | Add charter sessions |
| QA-008: Prod-Only Testing | Users find bugs | Add staging |
| QA-009: Untested Errors | Error bugs in prod | Error injection tests |
| QA-010: Manual Regression | 2-week regression | Automate stable paths |

## Test Strategy Review Questions

1. "What's our test pyramid ratio?" → Reveals QA-004
2. "How do we handle flaky tests?" → Reveals QA-003
3. "When do tests run in the process?" → Reveals QA-005
4. "What happens when tests fail together?" → Reveals QA-006
5. "How much manual regression do we do?" → Reveals QA-010
6. "How do we test error scenarios?" → Reveals QA-002, QA-009
7. "Do we do exploratory testing?" → Reveals QA-007
8. "What environments do we test in?" → Reveals QA-008
9. "What's our coverage target?" → Reveals QA-001
10. "Can any test run alone successfully?" → Reveals QA-006

## Resources

- **Books**: "Agile Testing" (Crispin & Gregory), "Explore It!" (Hendrickson)
- **Frameworks**: Test Pyramid (Fowler), Testing Quadrants (Marick)
- **Tools**: Jest, pytest, Selenium, Playwright, Cypress
