# Spec Kit Integration Roadmap: Formal Verification

**Date:** 2026-01-11
**Status:** Proposed
**Priority:** High Value (Killer Feature)

---

## Executive Summary

Интеграция формальных методов верификации в Spec Kit создаст **первый в мире SDD toolkit с встроенной формальной верификацией**. Это будет killer feature, отличающая Spec Kit от всех конкурентов.

**Target:** 6-month phased rollout с immediate quick wins.

---

## Phase 1: Foundation (Month 1-2) — Quick Wins

### 1.1 New Command: `/speckit.properties`

**Purpose:** Извлечение formal properties из спецификации для property-based testing.

**Workflow:**
```
spec.md (FR-xxx, AS-xxx) → properties.md → tests/properties/test_*.py
```

**Implementation:**

```yaml
# templates/commands/speckit-properties.md
---
description: Extract formal properties for property-based testing
persona: Test Architect
model: claude-sonnet-4.5
thinking_budget: medium
handoffs:
  - /speckit.implement (auto-continue after extraction)
pre_gates: []
gates: []
---

## Task

Extract formal properties from the feature specification for property-based testing.

## Inputs

1. **spec.md** — Feature specification with FR-xxx and AS-xxx
2. **Project context** — Programming language, test framework

## Outputs

1. **properties.md** — Formal property catalog
2. **tests/properties/test_<feature>.py** — Hypothesis tests
3. **conftest.py** — CI configuration (if not exists)

## Algorithm

### Step 1: Analyze Specification

Read spec.md and identify:
- **Invariants:** Properties that always hold (e.g., balance ≥ 0)
- **Conservation laws:** Quantities that don't change (e.g., total money)
- **Reversibility:** Operations that cancel (e.g., encode → decode)
- **Idempotency:** f(f(x)) = f(x)
- **Commutativity:** f(g(x)) = g(f(x))
- **Monotonicity:** x ≤ y ⇒ f(x) ≤ f(y)

### Step 2: Generate Property Catalog

Create `properties.md`:

```markdown
# Property Catalog: [Feature Name]

## PROP-001: [Property Name]
**Type:** [Invariant/Conservation/Reversibility/...]
**FR Mapping:** FR-001
**AS Mapping:** AS-001, AS-002
**Formula:** [Mathematical or logical expression]

**Hypothesis Strategy:**
\`\`\`python
@given(st.integers(min_value=0, max_value=1000))
def test_property_001(input):
    ...
\`\`\`

**Rationale:** [Why this property matters]
**Priority:** [Critical/High/Medium]
```

### Step 3: Generate Hypothesis Tests

For each PROP-xxx, generate test in `tests/properties/test_<feature>.py`:

```python
from hypothesis import given, strategies as st, assume, example
import pytest

# PROP-001: [Property Name]
# Mapping: FR-001, AS-001
@given(st....)
@example(...)  # Known edge case from AS-xxx
def test_prop_001_<descriptive_name>(inputs):
    \"\"\"
    Property: [Description]

    Rationale: [Why this matters]

    Traceability:
    - FR-001: [requirement text]
    - AS-001: [scenario text]
    \"\"\"
    # Arrange
    ...

    # Act
    result = system_under_test(inputs)

    # Assert
    assert property_holds(result)
```

### Step 4: Configure CI Profile

If `conftest.py` doesn't exist, create:

```python
from hypothesis import settings, HealthCheck

# CI profile: longer deadlines, more examples
settings.register_profile(
    'ci',
    suppress_health_check=(HealthCheck.too_slow,),
    deadline=60000,  # 60 seconds
    max_examples=1000,  # thorough testing
    print_blob=True,  # save failing examples
)

# Local dev: faster feedback
settings.register_profile(
    'dev',
    max_examples=100,
    deadline=5000,
)

settings.load_profile('ci' if os.getenv('CI') else 'dev')
```

### Step 5: Update tasks.md

Add property testing tasks:

```markdown
## TASK-xxx: Implement property tests (TDD Wave 2)
**Type:** Test
**Priority:** P0 (before implementation)
**Acceptance:** PROP-001 to PROP-nnn all passing (red → green)
**Traceability:** FR-001, AS-001
**Properties Tested:** PROP-001, PROP-002, PROP-003
```

## Success Criteria

- [ ] properties.md created with ≥3 properties per FR
- [ ] Hypothesis tests generated for all PROP-xxx
- [ ] conftest.py configured with CI profile
- [ ] Tasks updated in tasks.md
- [ ] Tests initially FAIL (TDD red phase)

## Handoffs

After completion, automatically continue to `/speckit.implement` with:
- Property tests as part of Wave 2 (TDD Red)
- Implementation in Wave 3 makes tests pass (TDD Green)
```

**CLI Integration:**

```python
# src/specify_cli/__init__.py

@cli.command()
@click.argument('feature_name', required=False)
@click.option('--auto-implement', is_flag=True, help='Auto-continue to implementation')
def properties(feature_name, auto_implement):
    """Extract formal properties for property-based testing.

    Analyzes spec.md and generates:
    - properties.md (property catalog)
    - tests/properties/ (Hypothesis tests)
    - conftest.py (CI configuration)
    """
    # Implementation via AI agent with command template
    ...
```

**Expected Timeline:** 1 week implementation + 1 week testing

---

### 1.2 Template: Property-Based Testing Setup

**New file:** `templates/shared/pbt-setup.md`

```markdown
# Property-Based Testing Setup

## Directory Structure

\`\`\`
project/
├── tests/
│   ├── properties/
│   │   ├── __init__.py
│   │   ├── test_<feature1>.py
│   │   └── test_<feature2>.py
│   └── conftest.py
├── properties.md (property catalog)
└── .hypothesis/ (auto-generated, add to .gitignore)
\`\`\`

## Dependencies

\`\`\`toml
[project.dependencies]
hypothesis = "^6.100.0"
pytest = "^8.0.0"
pytest-timeout = "^2.2.0"
\`\`\`

## CI/CD Integration

### GitHub Actions

\`\`\`yaml
name: Property-Based Tests

on: [push, pull_request]

jobs:
  pbt:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: \${{ matrix.python-version }}

    - name: Cache Hypothesis database
      uses: actions/cache@v4
      with:
        path: .hypothesis/
        key: hypothesis-\${{ hashFiles('tests/properties/**/*.py') }}

    - name: Install dependencies
      run: pip install -e .[test]

    - name: Run property tests
      run: |
        pytest tests/properties/ \\
          --hypothesis-show-statistics \\
          -v
      timeout-minutes: 30
      env:
        HYPOTHESIS_PROFILE: ci

    - name: Upload failing examples
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: hypothesis-failures
        path: .hypothesis/
\`\`\`

## Best Practices

1. **Start Simple:** Basic properties first (non-negativity, bounds)
2. **Add Examples:** Use `@example()` for known edge cases from AS-xxx
3. **Use assume():** Filter invalid inputs instead of complex strategies
4. **Incremental:** Add properties as you discover them
5. **Document:** Link properties to FR-xxx and AS-xxx for traceability
```

**Expected Timeline:** 2 days (mostly documentation)

---

### 1.3 Update: `/speckit.implement` Integration

**Changes to:** `templates/commands/speckit-implement.md`

```yaml
# Add new wave after Wave 2 (Test Scaffolding)

## Wave 2.5: Property-Based Testing (TDD Red)

**Trigger:** After test scaffolding, if properties.md exists

**Tasks:**
- Run property tests from tests/properties/
- **Expected:** All tests should FAIL (TDD red phase)
- **Quality Gate:** Failures must be meaningful (not syntax errors)
- Verify test quality:
  - Input generation strategies are appropriate
  - Properties are correctly formalized
  - Examples from AS-xxx are included

**Deliverable:** Property tests in red state, ready for implementation

## Wave 3: Core Implementation (TDD Green)

**Changes:**
- After implementing each feature, run corresponding property tests
- **Expected:** Property tests transition from red → green
- If property test fails: Fix implementation, not test (unless spec wrong)

## Wave 3.5: Property Test Verification

**New sub-wave after implementation:**

**Tasks:**
- Run full property test suite with max_examples=10000
- Collect statistics (Hypothesis reports)
- Verify coverage:
  - All PROP-xxx have passing tests
  - Strategies generated diverse inputs
  - Edge cases from AS-xxx were tested

**Quality Gate:** 100% property test pass rate

**Deliverable:** properties-report.txt with statistics
```

**Expected Timeline:** 3 days for integration + testing

---

### 1.4 Metric: Property Coverage

**New quality metric:**

```markdown
## Property Coverage Score (PCS)

**Formula:**
PCS = (Properties Tested / Properties Defined) × 100%

**Target:** ≥ 90%

**Interpretation:**
- 100%: All extracted properties have passing tests
- 80-99%: Good, some properties skipped (document why)
- <80%: Insufficient, implement missing property tests

**Report in:** RUNNING.md, verification-plan.md
```

**Expected Timeline:** 1 day

---

## Phase 2: Core Verification (Month 3-4)

### 2.1 New Command: `/speckit.contracts`

**Purpose:** Generate Design-by-Contract annotations from specifications and code.

**Workflow:**
```
spec.md + source code → LLM analysis → icontract decorators → contract tests
```

**Implementation:**

```yaml
# templates/commands/speckit-contracts.md
---
description: Generate Design-by-Contract annotations
persona: Architect
model: claude-sonnet-4.5
thinking_budget: high
handoffs: []
pre_gates: []
gates:
  - IG-CONTRACT-001: All public APIs have contracts
  - IG-CONTRACT-002: Contracts map to FR-xxx requirements
---

## Task

Generate icontract-based Design-by-Contract annotations for implementation.

## Inputs

1. **spec.md** — Feature requirements
2. **Source code** — Classes and functions to annotate
3. **properties.md** — Formal properties (if exists)

## Outputs

1. **Source code** — Annotated with @icontract decorators
2. **contract-tests/** — Tests specifically for contract validation
3. **contracts.md** — Contract catalog for documentation

## Algorithm

### Step 1: Analyze Code

For each public function/method/class:
- Identify parameters and return types
- Analyze business logic
- Map to FR-xxx requirements

### Step 2: Extract Contracts from Spec

From FR-xxx and AS-xxx, identify:

**Preconditions:**
- Input validation (amount > 0)
- State requirements (account.is_active)
- Resource availability (connection.is_open)

**Postconditions:**
- Output guarantees (result ≥ 0)
- State changes (balance reduced by amount)
- Side effects (transaction logged)

**Class Invariants:**
- Always-true properties (balance ≥ 0)
- Consistency rules (transactions.count() == expected)

### Step 3: Generate icontract Decorators

For each function, generate:

\`\`\`python
@icontract.require(
    lambda param: condition,
    "Human-readable error message",
    enabled=icontract.DBCLevel.PRODUCTION  # or TESTING
)
@icontract.ensure(
    lambda result, OLD: postcondition,
    "Postcondition description"
)
def function(param):
    # Original implementation
    ...
\`\`\`

**Guidelines:**
- Use lambda for simple conditions
- Use functions for complex logic
- Include OLD for state comparison
- Link to FR-xxx in docstring

### Step 4: Generate Class Invariants

\`\`\`python
@icontract.invariant(
    lambda self: self.balance >= 0,
    "Balance cannot be negative"
)
@icontract.invariant(
    lambda self: len(self.transactions) <= 10000,
    "Transaction history limit"
)
class Account:
    ...
\`\`\`

### Step 5: Create Contract Tests

\`\`\`python
# contract-tests/test_<module>_contracts.py

def test_precondition_violation():
    \"\"\"Test that precondition violations raise ViolationError.\"\"\"
    account = Account(balance=10)

    with pytest.raises(icontract.ViolationError, match="Insufficient funds"):
        account.withdraw(amount=100)

def test_postcondition_holds():
    \"\"\"Test that postconditions are satisfied.\"\"\"
    account = Account(balance=100)
    initial_balance = account.balance

    account.withdraw(amount=30)

    assert account.balance == initial_balance - 30
\`\`\`

### Step 6: Document Contracts

Create `contracts.md`:

\`\`\`markdown
# Contract Catalog: [Feature]

## CONTRACT-001: Account.withdraw()

**FR Mapping:** FR-001
**AS Mapping:** AS-001

**Preconditions:**
- `amount > 0` — Amount must be positive
- `balance >= amount` — Sufficient funds

**Postconditions:**
- `balance == OLD.balance - amount` — Balance reduced correctly
- `transactions.last().amount == amount` — Transaction recorded

**Exceptions:**
- `InsufficientFundsError` if balance < amount

**Usage:**
\`\`\`python
account.withdraw(50)  # OK
account.withdraw(-10)  # Raises ViolationError (precondition)
\`\`\`
\`\`\`

### Step 7: Configure Contract Checking

Create config file:

\`\`\`python
# contract_config.py
import os
from icontract import DBCLevel

# Production: disabled or warning-only
# Testing: full checking
# CI: strict checking

if os.getenv('ENVIRONMENT') == 'production':
    icontract.SLOW = DBCLevel.DISABLED
elif os.getenv('CI'):
    icontract.SLOW = DBCLevel.STRICT
else:
    icontract.SLOW = DBCLevel.TESTING
\`\`\`

## Success Criteria

- [ ] All public APIs have preconditions
- [ ] Critical functions have postconditions
- [ ] Classes with state have invariants
- [ ] Contract tests created
- [ ] contracts.md documents all contracts
- [ ] CI configured with strict checking

## Quality Gates

**IG-CONTRACT-001:** Coverage
- All public methods: ≥1 precondition
- Critical methods: ≥1 postcondition
- Stateful classes: ≥1 invariant

**IG-CONTRACT-002:** Traceability
- Each contract links to FR-xxx
- Contract violations map to test failures
```

**Expected Timeline:** 2 weeks implementation + 1 week testing

---

### 2.2 New Command: `/speckit.verify`

**Purpose:** Orchestration command that selects and applies appropriate verification methods.

**Workflow:**
```
Analyze code + spec → Select methods (PBT, DbC, RV, Model Checking) → Generate artifacts
```

**Implementation:**

```yaml
# templates/commands/speckit-verify.md
---
description: Formal verification orchestrator
persona: Verification Engineer
model: claude-sonnet-4.5
thinking_budget: very_high
handoffs: []
pre_gates: []
gates:
  - QG-VERIFY-001: Verification plan created
  - QG-VERIFY-002: Appropriate methods selected
  - QG-VERIFY-003: Verification artifacts generated
---

## Task

Analyze the feature and select appropriate formal verification methods.

## Inputs

1. **spec.md** — Feature specification
2. **plan.md** — Implementation plan
3. **Source code** — Existing implementation (if brownfield)
4. **Project config** — Criticality level, team size, constraints

## Outputs

1. **verification-plan.md** — Selected methods and rationale
2. **Verification artifacts** (properties.md, contracts.md, monitors/, specs/)
3. **CI/CD configuration** — Automated verification pipeline
4. **verification-report.md** — Coverage and results

## Algorithm

### Step 1: Analyze Feature Characteristics

Classify along dimensions:

**Complexity:**
- Concurrent/distributed: High
- Stateful: Medium
- Stateless: Low

**Criticality:**
- Safety-critical: Extreme
- Financial/Security: High
- Customer-facing: Medium
- Internal tool: Low

**Code Type:**
- Algorithm: PBT ideal
- State machine: DbC + RV ideal
- Distributed protocol: Model Checking ideal
- Data processing: PBT + Mining ideal

### Step 2: Select Verification Methods

Decision matrix:

| Characteristic | Primary Method | Secondary Methods |
|----------------|----------------|-------------------|
| Algorithm-heavy | PBT | DbC |
| Stateful API | DbC | PBT + RV |
| Distributed | Model Checking | RV |
| Security-critical | DbC + RV | Model Checking |
| Legacy code | Spec Mining | PBT |
| Safety-critical | Theorem Proving | Model Checking + DbC |

### Step 3: Generate verification-plan.md

\`\`\`markdown
# Verification Plan: [Feature Name]

## Feature Characteristics

- **Complexity:** [Low/Medium/High]
- **Criticality:** [Low/Medium/High/Extreme]
- **Type:** [Algorithm/State Machine/Distributed/...]
- **Team Size:** [N developers]
- **Timeline:** [X weeks]

## Selected Methods

### 1. Property-Based Testing (Primary)

**Rationale:** Feature has clear mathematical properties

**Properties to Verify:**
- PROP-001: Conservation of total balance
- PROP-002: Non-negative account balances
- PROP-003: Transfer idempotency

**Timeline:** Week 1-2
**Overhead Budget:** 15%

### 2. Design by Contract (Secondary)

**Rationale:** Clear API boundaries with preconditions

**Contracts:**
- CONTRACT-001: Account.withdraw() preconditions
- CONTRACT-002: Account.deposit() postconditions

**Timeline:** Week 2-3
**Overhead Budget:** 20% (disabled in production)

### 3. Runtime Verification (Optional)

**Rationale:** Production monitoring for invariant violations

**Monitors:**
- MONITOR-001: Balance never negative (LTL: G(balance >= 0))

**Timeline:** Week 3-4
**Overhead Budget:** 10% (5% sampled in production)

## NOT Selected: Model Checking

**Rationale:** Single-node application, no concurrency

## Verification Pipeline

[GitHub Actions YAML config]

## Success Metrics

- Property Coverage: ≥90%
- Contract Coverage: 100% public APIs
- RV Violations in Staging: 0
- CI Overhead: <20%

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| PBT finds too many edge cases | Medium | Prioritize by AS-xxx mapping |
| Contract overhead | Low | Disable in production |
| RV false positives | Medium | Tune specifications in staging |
\`\`\`

### Step 4: Execute Selected Methods

For each method:
- Run `/speckit.properties` if PBT selected
- Run `/speckit.contracts` if DbC selected
- Generate RV monitors if RV selected
- Generate TLA+ specs if Model Checking selected

### Step 5: Configure CI/CD

Generate unified pipeline:

\`\`\`yaml
name: Formal Verification

jobs:
  pbt:
    if: contains(verification_plan, 'PBT')
    ...

  contracts:
    if: contains(verification_plan, 'DbC')
    ...

  rv:
    if: contains(verification_plan, 'RV')
    ...
\`\`\`

### Step 6: Generate Report

\`\`\`markdown
# Verification Report: [Feature]

## Methods Applied

- [x] Property-Based Testing (12 properties)
- [x] Design by Contract (8 contracts)
- [ ] Runtime Verification (deferred to Phase 2)

## Coverage

- Property Coverage: 95% (11/12 properties passing)
- Contract Coverage: 100% (8/8 contracts)
- Bugs Found: 3 (2 edge cases, 1 contract violation)

## Performance

- PBT Overhead: 12% (acceptable)
- DbC Overhead: 18% (disabled in prod)
- CI Time: +8 minutes (total: 25 minutes)

## Recommendations

1. Add RV monitor for balance invariant (production)
2. Increase PBT max_examples to 10,000 for nightly
3. Add model checking for future distributed features
\`\`\`

## Success Criteria

- [ ] verification-plan.md created with method selection
- [ ] All selected methods executed
- [ ] Verification artifacts generated
- [ ] CI/CD configured
- [ ] verification-report.md generated

## Quality Gates

**QG-VERIFY-001:** Plan Completeness
- Rationale documented for each method
- Risk assessment included
- Success metrics defined

**QG-VERIFY-002:** Method Appropriateness
- Methods match feature characteristics
- Overhead within budget
- Team capabilities considered

**QG-VERIFY-003:** Artifact Quality
- Generated artifacts are valid
- CI/CD pipeline runs successfully
- Report shows meaningful coverage
```

**Expected Timeline:** 3 weeks implementation + 1 week testing

---

## Phase 3: Advanced (Month 5-6)

### 3.1 Runtime Verification Infrastructure

**Deliverables:**
1. RV-Monitor Kubernetes deployment templates
2. LTL/ERE specification templates
3. Alerting integration (Slack, PagerDuty)
4. Sampling strategies for production

**Expected Timeline:** 3 weeks

---

### 3.2 Model Checking Integration

**Deliverables:**
1. TLA+ spec generation from spec.md
2. TLC integration in CI/CD
3. Counterexample → test case converter
4. Documentation: When to use TLA+

**Expected Timeline:** 4 weeks

---

### 3.3 Specification Mining

**Deliverables:**
1. `/speckit.mine-specs` command
2. Daikon integration
3. LLM-based contract extraction
4. Weekly mining CI job

**Expected Timeline:** 3 weeks

---

## Implementation Priorities

### Must-Have (Phase 1)
1. `/speckit.properties` — **Highest ROI**, immediate value
2. PBT template and CI integration
3. Update `/speckit.implement` for property testing

### Should-Have (Phase 2)
4. `/speckit.contracts` — High value, medium complexity
5. `/speckit.verify` — Orchestration glue
6. verification-plan.md template

### Nice-to-Have (Phase 3)
7. RV infrastructure
8. TLA+ integration
9. Specification mining

---

## Success Metrics

### Adoption Metrics (6 months)
- **Target:** 50% of new features use `/speckit.properties`
- **Target:** 30% of new features use `/speckit.contracts`
- **Target:** 10% of distributed features use model checking

### Quality Metrics
- **Bug Reduction:** 40-60% in features using formal methods
- **Test Coverage:** +20% property coverage vs traditional tests
- **Incident MTTR:** -30% with RV traces

### Developer Metrics
- **NPS Score:** +10 points from developers using formal methods
- **Onboarding Time:** -20% with contracts as documentation
- **Refactoring Confidence:** +40% (survey-based)

---

## Risk Mitigation

### Risk 1: Learning Curve
**Impact:** High
**Probability:** High
**Mitigation:**
- Comprehensive documentation
- Video tutorials
- Example projects
- Office hours / community support

### Risk 2: Performance Overhead
**Impact:** Medium
**Probability:** Medium
**Mitigation:**
- Clear overhead budgets in docs
- Optimization guides
- Profiling tools
- Disable-in-production patterns

### Risk 3: False Positives
**Impact:** Medium
**Probability:** Medium
**Mitigation:**
- Tuning guidelines
- Example specifications
- Community spec library
- AI-assisted spec refinement

### Risk 4: Tool Maturity
**Impact:** Low
**Probability:** Low
**Mitigation:**
- Use only mature tools (Hypothesis, icontract, TLA+)
- Avoid bleeding-edge academic tools
- Fallback to simpler methods if issues

---

## Resource Requirements

### Phase 1 (Month 1-2)
- **Engineering:** 1 senior dev, full-time
- **Documentation:** 0.5 tech writer
- **Testing:** 0.5 QA engineer
- **Total:** 2 FTE-months

### Phase 2 (Month 3-4)
- **Engineering:** 1 senior dev, full-time
- **AI/LLM:** 0.5 ML engineer (for contract generation)
- **Documentation:** 0.5 tech writer
- **Total:** 2 FTE-months

### Phase 3 (Month 5-6)
- **Engineering:** 1 senior dev, 1 junior dev
- **DevOps:** 0.5 DevOps engineer (RV infrastructure)
- **Documentation:** 0.5 tech writer
- **Total:** 2.5 FTE-months

**Total Project: 6.5 FTE-months**

---

## Go/No-Go Decision Points

### After Phase 1 (Month 2)
**Criteria:**
- [ ] `/speckit.properties` working end-to-end
- [ ] ≥3 successful pilot projects
- [ ] Developer NPS ≥ 7/10
- [ ] Bug reduction ≥ 30%

**Decision:** Proceed to Phase 2 if ≥3 criteria met

### After Phase 2 (Month 4)
**Criteria:**
- [ ] `/speckit.contracts` production-ready
- [ ] `/speckit.verify` functional
- [ ] ≥10 projects using formal methods
- [ ] Zero critical bugs from formal method overhead

**Decision:** Proceed to Phase 3 if all criteria met

---

## Next Steps (Immediate)

### Week 1-2: Design
- [ ] Review this roadmap with team
- [ ] Prototype `/speckit.properties` command template
- [ ] Design property.md schema
- [ ] Draft Hypothesis test generation algorithm

### Week 3-4: Implementation
- [ ] Implement `/speckit.properties` command
- [ ] Create PBT templates
- [ ] Write integration tests
- [ ] Update CLAUDE.md and COMMANDS_GUIDE.md

### Week 5-6: Validation
- [ ] Pilot on 3 internal features
- [ ] Collect metrics (bugs found, overhead, developer feedback)
- [ ] Iterate based on feedback
- [ ] Prepare Phase 2 detailed design

---

## Conclusion

This roadmap transforms Spec Kit from a specification tool into a **formal verification platform**. Property-based testing in Phase 1 alone will provide immediate ROI, with contracts and runtime verification adding layers of assurance in later phases.

**This is the killer feature that differentiates Spec Kit in the market.**

Let's build it.

---

**Author:** Research Team
**Reviewed by:** [Pending]
**Approved by:** [Pending]
**Last Updated:** 2026-01-11
