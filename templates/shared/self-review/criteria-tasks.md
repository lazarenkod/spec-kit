# Self-Review Criteria: Tasks (SR-TASK)

> Validation criteria for `/speckit.tasks` output. Import in self-review phase.

## Purpose

Ensure task artifacts meet quality standards for:
1. Clarity - no placeholders or generic terms
2. Executability - immediately actionable by weak LLMs
3. Specificity - concrete file paths, method names, test scenarios
4. Completeness - all API/service/component details specified
5. Traceability - proper linkage to spec requirements

---

## Criteria Table

| ID | Name | Description | Severity | Auto-Fix |
|----|------|-------------|----------|----------|
| SR-TASK-11 | No Placeholder Brackets | Zero placeholders: `[Entity]`, `[Service]`, `[Component]`, etc. | HIGH | ✅ |
| SR-TASK-12 | Concrete File Paths | All file paths specific: `src/models/user.py` not `[entity].py` | HIGH | ✅ |
| SR-TASK-13 | Specific Method Names | Service tasks specify methods: `register()`, `authenticate()` | HIGH | ❌ |
| SR-TASK-14 | API HTTP Details | API tasks have HTTP method + path + handler + I/O | HIGH | ❌ |
| SR-TASK-15 | Test Scenario Specificity | Test tasks reference AS-xxx and have concrete test values | HIGH | ❌ |

---

## Detailed Criteria

### SR-TASK-11: No Placeholder Brackets

```text
SR-TASK-11:
  severity: HIGH
  auto_fixable: true

  check_fn(tasks_md):
    placeholder_pattern = '\[(Entity\d*|Service|Component|scenario|test|method|function|field|endpoint)\]'
    matches = GREP(tasks_md, pattern=placeholder_pattern)

    IF matches.count > 0:
      violations = []
      FOR match IN matches:
        task_line = EXTRACT_LINE(tasks_md, match.line_number)
        task_id = EXTRACT_TASK_ID(task_line)

        # Attempt auto-fix by extracting from spec.md/plan.md
        fix_suggestion = EXTRACT_CONCRETE_DETAIL(
          placeholder=match.text,
          spec_path="spec.md",
          plan_path="plan.md"
        )

        IF fix_suggestion != null:
          violations.append({
            task_id: task_id,
            line: match.line_number,
            placeholder: match.text,
            fix: fix_suggestion,
            auto_fixable: true
          })
        ELSE:
          violations.append({
            task_id: task_id,
            line: match.line_number,
            placeholder: match.text,
            fix: null,
            auto_fixable: false
          })

      RETURN {
        status: FAIL,
        violations: violations,
        message: "{matches.count} placeholder(s) detected",
        remediation: "Extract concrete details from spec.md/plan.md or run /speckit.clarify"
      }

    RETURN {status: PASS}
```

**Examples**:

```markdown
❌ FAIL:
- [ ] T012 Create [Entity1] model in src/models/[entity1].py

✅ PASS:
- [ ] T012 Create User model in src/models/user.py with fields: id (UUID), email (unique), password_hash, created_at
```

---

### SR-TASK-12: Concrete File Paths

```text
SR-TASK-12:
  severity: HIGH
  auto_fixable: true

  check_fn(tasks_md):
    path_placeholder_pattern = 'src/[a-z]+/\[.*?\]\.(py|ts|tsx|js|jsx|java|go|rs)'
    matches = GREP(tasks_md, pattern=path_placeholder_pattern)

    IF matches.count > 0:
      violations = []
      FOR match IN matches:
        task_line = EXTRACT_LINE(tasks_md, match.line_number)
        task_id = EXTRACT_TASK_ID(task_line)

        # Attempt to derive concrete path from context
        concrete_path = DERIVE_PATH(
          placeholder_path=match.text,
          context=task_line,
          spec_path="spec.md",
          plan_path="plan.md"
        )

        violations.append({
          task_id: task_id,
          line: match.line_number,
          placeholder_path: match.text,
          concrete_path: concrete_path,
          auto_fixable: concrete_path != null
        })

      RETURN {
        status: FAIL,
        violations: violations,
        message: "{matches.count} placeholder path(s) detected",
        remediation: "Replace with concrete file names derived from entity/service names"
      }

    RETURN {status: PASS}
```

**Examples**:

```markdown
❌ FAIL:
- [ ] T014 Implement UserService in src/services/[service].py

✅ PASS:
- [ ] T014 Implement UserService in src/services/user_service.py with methods: register(email, password), authenticate(email, password)
```

---

### SR-TASK-13: Specific Method Names

```text
SR-TASK-13:
  severity: HIGH
  auto_fixable: false

  check_fn(tasks_md):
    # Find all service/class implementation tasks
    service_pattern = '(Implement|Create).*?(Service|Repository|Controller|Manager)'
    service_tasks = GREP(tasks_md, pattern=service_pattern)

    violations = []
    FOR task IN service_tasks:
      task_line = EXTRACT_LINE(tasks_md, task.line_number)
      task_id = EXTRACT_TASK_ID(task_line)

      # Check if task specifies methods
      has_methods = CONTAINS(task_line, patterns=[
        'with methods:',
        'methods:',
        'implementing:',
        '\w+\(\s*\w*\s*[,)]'  # method signature pattern
      ])

      IF NOT has_methods:
        violations.append({
          task_id: task_id,
          line: task.line_number,
          task_text: task_line,
          missing: "method specifications",
          suggestion: "Add 'with methods: methodName1(), methodName2()' or extract from plan.md Architecture"
        })

    IF violations.length > 0:
      RETURN {
        status: FAIL,
        violations: violations,
        message: "{violations.length} service task(s) without method specifications",
        remediation: "Specify methods from plan.md Architecture or spec.md Functional Requirements"
      }

    RETURN {status: PASS}
```

**Examples**:

```markdown
❌ FAIL:
- [ ] T014 Implement UserService in src/services/user_service.py

✅ PASS:
- [ ] T014 Implement UserService in src/services/user_service.py with methods: register(email, password) returns userId, authenticate(email, password) returns token
```

---

### SR-TASK-14: API HTTP Details

```text
SR-TASK-14:
  severity: HIGH
  auto_fixable: false

  check_fn(tasks_md):
    # Find all API endpoint tasks
    api_pattern = '(Implement|Create).*(endpoint|API|route)'
    api_tasks = GREP(tasks_md, pattern=api_pattern)

    violations = []
    FOR task IN api_tasks:
      task_line = EXTRACT_LINE(tasks_md, task.line_number)
      task_id = EXTRACT_TASK_ID(task_line)

      # Check for required API components
      has_http_method = CONTAINS(task_line, patterns=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
      has_path = CONTAINS(task_line, patterns=['/api/', '/v\d+/'])
      has_handler = CONTAINS(task_line, patterns=['handler', '\w+\(\)'])
      has_io_spec = CONTAINS(task_line, patterns=['expects:', 'returns:', 'request:', 'response:'])

      missing_components = []
      IF NOT has_http_method: missing_components.append("HTTP method (GET/POST/PUT/DELETE)")
      IF NOT has_path: missing_components.append("endpoint path (/api/v1/...)")
      IF NOT has_handler: missing_components.append("handler function name")
      IF NOT has_io_spec: missing_components.append("I/O specification (expects/returns)")

      IF missing_components.length > 0:
        violations.append({
          task_id: task_id,
          line: task.line_number,
          task_text: task_line,
          missing: missing_components,
          suggestion: "Extract from spec.md API Requirements or Contracts section"
        })

    IF violations.length > 0:
      RETURN {
        status: FAIL,
        violations: violations,
        message: "{violations.length} API task(s) with incomplete HTTP details",
        remediation: "Specify: HTTP method + path + handler + (expects/returns)"
      }

    RETURN {status: PASS}
```

**Examples**:

```markdown
❌ FAIL:
- [ ] T018 Implement user registration endpoint

❌ FAIL:
- [ ] T018 Implement POST /api/v1/auth/register endpoint

✅ PASS:
- [ ] T018 Implement POST /api/v1/auth/register endpoint in src/api/auth.py with register_user() handler (expects: email, password; returns: userId, token; status: 201)
```

---

### SR-TASK-15: Test Scenario Specificity

```text
SR-TASK-15:
  severity: HIGH
  auto_fixable: false

  check_fn(tasks_md):
    # Find all test tasks
    test_pattern = '\[TEST:'
    test_tasks = GREP(tasks_md, pattern=test_pattern)

    violations = []
    FOR task IN test_tasks:
      task_line = EXTRACT_LINE(tasks_md, task.line_number)
      task_id = EXTRACT_TASK_ID(task_line)

      # Check for AS reference
      has_as_reference = CONTAINS(task_line, patterns=['AS-\d+[A-Z]?', '\[TEST:AS-'])

      # Check for concrete test values (emails, numbers, strings)
      has_concrete_values = CONTAINS(task_line, patterns=[
        '\w+@\w+\.\w+',  # email pattern
        '"\w+"',          # quoted strings
        '\d{3}',          # HTTP status codes
        'test\w*',        # test data identifiers
      ])

      # Check for expectations
      has_expectations = CONTAINS(task_line, patterns=['expects', 'should', 'returns', 'status'])

      missing_components = []
      IF NOT has_as_reference: missing_components.append("AS-xxx reference")
      IF NOT has_concrete_values: missing_components.append("concrete test values (email, password, etc.)")
      IF NOT has_expectations: missing_components.append("expected outcome (expects/returns)")

      IF missing_components.length > 0:
        violations.append({
          task_id: task_id,
          line: task.line_number,
          task_text: task_line,
          missing: missing_components,
          suggestion: "Extract from spec.md Acceptance Scenarios (AS-xxx section)"
        })

    IF violations.length > 0:
      RETURN {
        status: FAIL,
        violations: violations,
        message: "{violations.length} test task(s) with vague scenarios",
        remediation: "Specify: AS-xxx reference + concrete test values + expected outcomes"
      }

    RETURN {status: PASS}
```

**Examples**:

```markdown
❌ FAIL:
- [ ] T023 [TEST] Test user registration

❌ FAIL:
- [ ] T023 [TEST:AS-001] Test user registration with valid email

✅ PASS:
- [ ] T023 [TEST:AS-001] Test user registration with valid email (test@example.com, SecurePass123!) expects 201 status, userId in response, and confirmation email sent
```

---

## Integration with Quality Gates

These criteria work with:
- **IG-TASK-005**: Inline gate enforcing no placeholders (pre-emptive check)
- **SR-TASK-11 to SR-TASK-15**: Self-review validation (post-generation check)

**Workflow**:
1. `/speckit.tasks` generates tasks with extraction algorithms
2. **IG-TASK-005** runs immediately (HIGH severity, blocks if violations)
3. Agent performs self-review using **SR-TASK-11 to SR-TASK-15**
4. If any criteria fail → regenerate with enhanced context

**Pass Threshold**: 5/5 criteria must pass for tasks.md handoff

---

## Remediation Actions

| Criteria | Remediation |
|----------|-------------|
| SR-TASK-11 | Run extraction algorithms from spec.md/plan.md; if insufficient → /speckit.clarify |
| SR-TASK-12 | Derive file paths from entity/service names using naming conventions |
| SR-TASK-13 | Extract methods from plan.md Architecture or spec.md FR descriptions |
| SR-TASK-14 | Extract endpoint details from spec.md API Requirements/Contracts |
| SR-TASK-15 | Extract test scenarios from spec.md AS-xxx tables (Given/When/Then) |

---

## Auto-Fix Capability

| Criteria | Auto-Fixable | Method |
|----------|--------------|--------|
| SR-TASK-11 | ✅ Partial | Extract from spec.md Domain Model → replace `[Entity1]` with actual entity name |
| SR-TASK-12 | ✅ Partial | Derive path from entity/service name → `[entity].py` → `user.py` |
| SR-TASK-13 | ❌ Manual | Requires semantic understanding of service responsibilities |
| SR-TASK-14 | ❌ Manual | Requires parsing spec.md Contracts for complete endpoint spec |
| SR-TASK-15 | ❌ Manual | Requires extracting GIVEN/WHEN/THEN and mapping to test values |

---

*Version: v0.1.4*
*Related: IG-TASK-005, Task Clarity Requirements*
