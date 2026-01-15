# Formal Verification Methods: Quick Reference Guide

**Last Updated:** 2026-01-11

---

## Decision Matrix: Which Method to Use?

### By Project Type

| Project Type | Primary Method | Secondary Methods | Avoid |
|--------------|----------------|-------------------|-------|
| **Web API / REST** | PBT + DbC | RV (production) | Theorem Proving |
| **Distributed System** | TLA+ (design) | PBT + RV | - |
| **Embedded / IoT** | DbC + Model Checking | RV (lightweight) | Heavy PBT |
| **Financial / Trading** | DbC (mandatory) | PBT + RV + TLA+ | - |
| **ML / Data Science** | PBT (properties) | Spec Mining | Model Checking |
| **Legacy System** | Spec Mining → PBT | DbC (gradual) | Full rewrite |
| **Safety-Critical** | Theorem Proving | Model Checking + DbC | Shortcuts |

### By Team Size

| Team Size | Recommended Stack | Max Learning Investment | Expected ROI |
|-----------|-------------------|-------------------------|--------------|
| **1-5 devs** | PBT + Spec Mining | 1 week | 5-10x |
| **6-20 devs** | PBT + DbC + RV | 1 month | 8-15x |
| **20-50 devs** | Full Stack (no Theorem Proving) | 2 months | 10-30x |
| **50+ devs** | All methods, dedicated FM team | 3-6 months | 20-100x |

### By Criticality

| Criticality Level | Required Methods | Optional Methods | Overhead Budget |
|-------------------|------------------|------------------|-----------------|
| **Low (internal tools)** | PBT | Spec Mining | <10% |
| **Medium (customer-facing)** | PBT + DbC | RV | <20% |
| **High (financial, healthcare)** | PBT + DbC + RV | TLA+ | <30% |
| **Critical (safety, security)** | All methods | Theorem Proving | <50% |

---

## Method Comparison Matrix

| Aspect | PBT (Hypothesis) | DbC (icontract) | RV (RV-Monitor) | Model Checking (TLA+) | Theorem Proving (Coq) |
|--------|------------------|-----------------|-----------------|----------------------|----------------------|
| **Phase** | Testing | Implementation | Runtime | Design | Implementation |
| **Automation** | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ High | ⭐⭐⭐ Medium | ⭐⭐ Low |
| **Overhead** | 10-20% | 15-25% (disable in prod) | 10-20% (1-3% sampled) | N/A (design-time) | N/A (compile-time) |
| **Learning Curve** | 2-3 days | 1-2 weeks | 2-4 weeks | 3-6 months | 6-12 months |
| **False Positives** | Low | Low | Low | Medium | Very Low |
| **ROI** | 10x | 5x | 8x | 50x+ | 100x+ |
| **Payback** | 1-2 months | 3-4 months | 3-6 months | 6-12 months | 1-2 years |
| **CI/CD Ready** | ✅ Excellent | ✅ Good | ✅ Excellent | 🟡 Moderate | 🟡 Complex |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes (AWS) | 🟡 Partial |
| **Maintenance** | Low | Low | Medium | Medium | High |
| **Tool Maturity** | Mature | Mature | Mature | Mature | Academic → Industry |

---

## When to Use Each Method

### ✅ Property-Based Testing (PBT)

**Use When:**
- Testing parsers, serializers, encoders
- Validating mathematical properties (commutative, associative, idempotent)
- API contract testing
- Algorithm correctness
- Data structure invariants
- Round-trip properties (encode → decode = identity)

**Real Examples:**
- Email parser: `@given(st.emails())`
- JSON roundtrip: `parse(serialize(x)) == x`
- Password validation: `valid(password) => meets_criteria(password)`
- ML fairness: `similar_users → similar_recommendations`

**Don't Use For:**
- UI interactions (too non-deterministic)
- Performance benchmarks (use dedicated tools)
- External API behavior (mock instead)

### ✅ Design by Contract (DbC)

**Use When:**
- Defining API boundaries (public methods)
- Core business logic with clear invariants
- Financial transactions (mandatory audit trail)
- State machines with invariants
- Refactoring legacy code (contracts = safety net)

**Real Examples:**
- Bank account: `@require(balance >= amount)`
- User registration: `@ensure(user.is_persisted)`
- Access control: `@require(current_user.has_permission(...))`
- Resource cleanup: `@ensure(connection.is_closed)`

**Don't Use For:**
- Performance-critical hot paths (overhead)
- Private helper methods (overkill)
- Trivial getters/setters

### ✅ Runtime Verification (RV)

**Use When:**
- Security properties (authentication flow)
- Business invariants (account balance ≥ 0)
- Protocol compliance (state machine transitions)
- Distributed system properties (causality, ordering)
- Regulatory compliance (GDPR, HIPAA)

**Real Examples:**
- Payment: `G(process_payment -> O log_transaction)`
- File handling: `G(open -> F close)`
- Authentication: `G(access_resource -> O authenticate)`
- Order flow: `order → payment → shipment → delivery`

**Don't Use For:**
- Performance metrics (use APM tools)
- High-frequency events (>1M/sec without sampling)
- Non-deterministic behavior (hard to specify)

### ✅ Model Checking (TLA+)

**Use When:**
- Designing distributed algorithms (consensus, replication)
- Concurrent protocols (lock-free data structures)
- Security protocols (authentication, key exchange)
- Cloud infrastructure (schedulers, load balancers)
- Before implementation (catch design bugs early)

**Real Examples:**
- DynamoDB replication (AWS)
- S3 lock manager (AWS)
- Raft consensus
- Two-phase commit
- Byzantine fault tolerance

**Don't Use For:**
- Single-threaded applications
- CRUD applications
- UI logic
- After implementation (too late, model drift)

### ✅ Theorem Proving (Coq/Lean)

**Use When:**
- Safety-critical systems (aerospace, medical, nuclear)
- Security kernels (seL4)
- Compilers (CompCert)
- Cryptographic primitives
- Regulatory requirements demand formal proof

**Real Examples:**
- CompCert C compiler (Coq)
- seL4 microkernel (Isabelle/HOL)
- Airbus A380 flight control software
- Medical device firmware
- Nuclear reactor control systems

**Don't Use For:**
- Web applications
- Mobile apps
- Internal tools
- Anything without life/safety/security criticality

### ✅ Specification Mining

**Use When:**
- Understanding legacy code (no documentation)
- Reverse-engineering API contracts
- Generating documentation automatically
- Detecting regression (mined specs = oracles)
- Refactoring (preserve mined properties)

**Real Examples:**
- Daikon on Java codebase → invariants
- Caruca on CLI tools → state machines
- LLM on Python code → icontract decorators
- Process mining on event logs → LTL specs

**Don't Use For:**
- Security properties (false negatives dangerous)
- Novel/greenfield code (no traces = no specs)
- Performance-critical paths (tracing overhead)

---

## Quick Start Checklist

### Week 1: Property-Based Testing
- [ ] Install: `pip install hypothesis pytest`
- [ ] Write 3 property tests for existing code
- [ ] Add to CI: `.github/workflows/pbt.yml`
- [ ] Training: Read [Hypothesis docs](https://hypothesis.readthedocs.io/) (2 hours)

**Expected Result:** Find 2-5 edge case bugs

### Week 2-3: Contract-Based Design
- [ ] Install: `pip install icontract`
- [ ] Add contracts to 5 core functions
- [ ] Setup CrossHair: `pip install crosshair-tool`
- [ ] Training: Read [icontract guide](https://icontract.readthedocs.io/) (4 hours)

**Expected Result:** Prevent 1-3 contract violations in tests

### Week 4-6: Runtime Verification
- [ ] Choose properties (security, invariants)
- [ ] Write 3 LTL specifications
- [ ] Setup RV-Monitor (Docker or K8s)
- [ ] Training: [RV-Monitor docs](https://runtimeverification.com/monitor) (8 hours)

**Expected Result:** Continuous monitoring in staging

### Month 3-4: Model Checking (Optional)
- [ ] Identify critical distributed component
- [ ] Learn TLA+ basics: [Learn TLA+](https://learntla.com/) (20 hours)
- [ ] Model 1 protocol in TLA+
- [ ] Run TLC model checker

**Expected Result:** Find 1 design-level bug

---

## Common Pitfalls & Solutions

### Pitfall 1: "Too much overhead"
**Solution:**
- PBT: Use `max_examples=100` for fast tests, `max_examples=10000` for nightly
- DbC: Disable runtime checks in production (`ICONTRACT_SLOW=0`)
- RV: Use sampling (10-30%) for high-throughput systems

### Pitfall 2: "Learning curve too steep"
**Solution:**
- Start with PBT (easiest)
- Gradual adoption: 1 feature → prove value → expand
- Invest in training (71.5% cite lack of knowledge as barrier)

### Pitfall 3: "False positives"
**Solution:**
- PBT: Use `assume()` to filter invalid inputs
- DbC: Weaken overly strict contracts
- RV: Tune specifications based on production traces

### Pitfall 4: "Not integrated into workflow"
**Solution:**
- CI/CD from day 1 (not bolted-on later)
- Code review includes verification artifacts
- Design docs include formal specs

### Pitfall 5: "Tools not production-ready"
**Solution:**
- Stick to mature tools: Hypothesis, icontract, RV-Monitor, TLA+
- Avoid bleeding-edge academic tools
- AWS/Microsoft use these tools in production (proof of maturity)

---

## ROI Quick Calculator

**Input your numbers:**
```
Annual development cost: $_________ (e.g., $1M for 10 devs)
Average incident cost: $_________ (downtime + engineering + customer)
Expected incidents/year: _________ (e.g., 10)
Bug prevention rate: _________% (conservative: 50%, optimistic: 85%)

Initial investment:
- PBT setup: 2 dev-weeks = $10k
- DbC setup: 4 dev-weeks = $20k
- RV setup: 6 dev-weeks = $30k
- Training: 1 week all-hands = $50k
Total: $110k

Expected savings:
Incidents prevented = Expected incidents × Bug prevention rate
Savings = Incidents prevented × Average incident cost

ROI = (Savings - Investment) / Investment × 100%
```

**Example:**
- Incidents: 10/year × $50k = $500k impact
- Prevention: 50% = 5 incidents prevented = $250k saved
- Investment: $110k
- **ROI: 127%** (payback in 6 months)

---

## Tool Ecosystem

### Python
- **PBT:** `hypothesis` ⭐⭐⭐⭐⭐
- **DbC:** `icontract` ⭐⭐⭐⭐⭐, `deal` ⭐⭐⭐⭐
- **Static Check:** `crosshair-tool` ⭐⭐⭐
- **Mining:** `daikon` (Java, Python support) ⭐⭐⭐

### JavaScript/TypeScript
- **PBT:** `fast-check` ⭐⭐⭐⭐
- **DbC:** `ts-runtime-checker` ⭐⭐⭐
- **RV:** Limited options

### Java
- **PBT:** `JUnit QuickCheck` ⭐⭐⭐⭐
- **DbC:** `Cofoja` ⭐⭐⭐
- **RV:** `JavaPathExplorer` ⭐⭐⭐⭐
- **Mining:** `Daikon` ⭐⭐⭐⭐⭐ (native)

### Go
- **PBT:** `gopter` ⭐⭐⭐
- **DbC:** Limited (use comments + static analysis)
- **RV:** Custom solutions

### Rust
- **PBT:** `proptest` ⭐⭐⭐⭐⭐
- **DbC:** Type system (compile-time contracts) ⭐⭐⭐⭐⭐
- **Formal:** `kani` (verification tool) ⭐⭐⭐

### Language-Agnostic
- **Model Checking:** TLA+ ⭐⭐⭐⭐⭐, SPIN ⭐⭐⭐⭐
- **Theorem Proving:** Coq/Rocq ⭐⭐⭐⭐⭐, Lean 4 ⭐⭐⭐⭐, Isabelle/HOL ⭐⭐⭐⭐
- **RV:** RV-Monitor ⭐⭐⭐⭐⭐, Linux Kernel RV ⭐⭐⭐⭐

---

## Further Reading

### Beginner (0-3 months experience)
1. [Property-Based Testing with Hypothesis](https://hypothesis.readthedocs.io/) — Start here!
2. [icontract Introduction](https://icontract.readthedocs.io/en/latest/introduction.html) — Contracts 101
3. [A Beginner's Guide to Hypothesis](https://betterstack.com/community/guides/testing/hypothesis-unit-testing/)

### Intermediate (3-6 months)
4. [Learn TLA+](https://learntla.com/) — Practical TLA+ course
5. [Runtime Verification Tutorial](https://runtimeverification.com/monitor) — RV-Monitor guide
6. [Design by Contract in Python](https://medium.com/@m.nusret.ozates/good-design-practices-with-python-design-by-contract-a2a2d07b37d0)

### Advanced (6+ months)
7. [AWS Formal Methods](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — How AWS uses TLA+
8. [CompCert C Compiler](https://compcert.org/) — Verified compiler case study
9. [seL4 Microkernel](https://sel4.systems/) — Verified OS kernel

### Academic (deep dive)
10. [The Daikon System](https://plse.cs.washington.edu/daikon/) — Invariant detection
11. [Runtime Verification Book](https://link.springer.com/book/10.1007/978-3-319-75632-5)
12. [Formal Methods in Industry](https://dl.acm.org/doi/full/10.1145/3689374) — 2024 survey

---

## Glossary

- **LTL:** Linear Temporal Logic — язык для спецификации temporal properties
- **ERE:** Extended Regular Expressions — паттерны для последовательностей событий
- **TDD:** Test-Driven Development — tests before implementation
- **DbC:** Design by Contract — preconditions + postconditions + invariants
- **PBT:** Property-Based Testing — генерация тестовых входов на основе свойств
- **RV:** Runtime Verification — мониторинг executions против formal specs
- **Model Checking:** Exhaustive state space exploration для verification
- **Theorem Proving:** Mathematical proof of correctness
- **Spec Mining:** Автоматическое извлечение спецификаций из кода/traces

---

**Last Updated:** 2026-01-11
**Maintained by:** Spec Kit Research Team
**Full Report:** `formal-verification-methods-research-2026-01-11.md`
