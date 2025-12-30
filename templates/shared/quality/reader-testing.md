# Reader Testing Protocol

> Test artifacts with fresh reader perspective before finalization. Catches blind spots, implicit assumptions, and missing context.

## Purpose

Before finalizing any artifact, simulate how a **new team member** would read it:
- They have no context from the conversation
- They weren't in the brainstorming session
- They don't know what "obvious" things were discussed

This catches:
1. Missing definitions/acronyms
2. Implicit assumptions
3. Ambiguous statements
4. Unclear next steps
5. Jargon without explanation

---

## Reader Testing Protocol

### Step 1: Perspective Switch

```text
MENTAL_RESET:
  "Imagine a new team member reading this for the first time.
   They joined yesterday. They know nothing about this project.
   They have:
   - General technical competence in their domain
   - No knowledge of our specific codebase
   - No context from Slack discussions
   - No memory of 'that meeting where we decided...'"
```

### Step 2: Comprehension Check

Run through these questions as if you're the new reader:

```text
COMPREHENSION_QUESTIONS = [
  # Vision Clarity
  "Can I understand WHAT we're building in <30 seconds?",
  "Is the core value proposition clear in the first paragraph?",
  "Would I be able to explain this to my manager?",

  # Problem Clarity
  "Can I understand WHY we're building this?",
  "Is the problem described with specific examples?",
  "Do I understand who suffers from this problem?",

  # Actionability
  "Do I know HOW to proceed after reading?",
  "Are next steps explicit and ordered?",
  "Is ownership clear (who does what)?",

  # Context Completeness
  "Are all acronyms defined on first use?",
  "Are technical terms explained?",
  "Are there links to related docs I'd need?",

  # Assumptions
  "What assumptions does this document make?",
  "Are those assumptions stated explicitly?",
  "Would I know if an assumption doesn't apply to me?"
]
```

**Scoring:**
- Each question: YES (1), PARTIAL (0.5), NO (0)
- Threshold: 80% (12/15) to pass

### Step 3: Confidence Check

Would domain experts approve this without questions?

```text
ROLE_CONFIDENCE_CHECKS = {
  PM: [
    "Would a PM approve this spec for development?",
    "Are success criteria measurable?",
    "Is scope clearly bounded?",
    "Are out-of-scope items explicitly listed?"
  ],

  Developer: [
    "Would a developer know where to start coding?",
    "Are technical requirements specific enough?",
    "Are edge cases documented?",
    "Are integration points clear?"
  ],

  Designer: [
    "Would a designer understand the UX goals?",
    "Are user flows documented?",
    "Are interaction patterns specified?",
    "Is the visual direction clear?"
  ],

  QA: [
    "Would QA know what to test?",
    "Are acceptance criteria testable?",
    "Are error scenarios documented?",
    "Is expected behavior explicit?"
  ]
}

# Pass: All relevant roles score >= 75%
```

### Step 4: Ambiguity Scan

Find sentences that could be interpreted multiple ways:

```text
AMBIGUITY_TRIGGERS = [
  # Vague pronouns
  "it", "this", "that", "they" (without clear antecedent),

  # Undefined comparisons
  "better", "faster", "easier", "more efficient" (than what?),

  # Missing quantifiers
  "some", "many", "few", "most" (how many exactly?),

  # Unclear timeframes
  "soon", "later", "eventually", "in the future" (when?),

  # Passive voice hiding actors
  "will be implemented", "should be done" (by whom?),

  # Conditional without criteria
  "if needed", "when appropriate", "as required" (when is that?)
]

AMBIGUITY_CHECK:
  FOR EACH sentence IN artifact:
    IF contains(AMBIGUITY_TRIGGERS):
      FLAG with specific question:
        - "What does 'it' refer to in this sentence?"
        - "'Faster' than what baseline? By how much?"
        - "'If needed' — what criteria trigger this need?"
```

### Step 5: Generate Reader Test Report

```text
OUTPUT FORMAT:

## Reader Test Results

### Comprehension Score: {X}/15 ({Y}%)

| Question | Score | Issue |
|----------|-------|-------|
| Vision clarity | ✅/⚠️/❌ | [specific issue if any] |
| Problem clarity | ✅/⚠️/❌ | [specific issue if any] |
| ... | ... | ... |

### Role Confidence

| Role | Ready? | Blockers |
|------|--------|----------|
| PM | ✅/❌ | [what's missing] |
| Developer | ✅/❌ | [what's missing] |
| Designer | ✅/❌ | [what's missing] |
| QA | ✅/❌ | [what's missing] |

### Ambiguities Found

1. Line X: "[sentence]"
   - Ambiguity: [description]
   - Fix: [suggestion]

2. Line Y: "[sentence]"
   - Ambiguity: [description]
   - Fix: [suggestion]

### Missing Context

- [ ] Acronym "ABC" undefined (first appears line X)
- [ ] Technical term "xyz" unexplained
- [ ] Assumption "user has admin access" not stated

### Verdict: PASS / NEEDS_REVISION

{If NEEDS_REVISION: List top 3 fixes required}
```

---

## Integration

### Import in Self-Review

Add to `self-review/framework.md`:

```text
READER_TEST_CHECKS = [
  {
    id: "SR-READ-01",
    name: "Fresh Reader Comprehension",
    description: "Would a new team member understand this?",
    severity: HIGH,
    auto_fixable: false,
    check: COMPREHENSION_SCORE >= 80%
  },
  {
    id: "SR-READ-02",
    name: "Role Actionability",
    description: "Clear next steps for each role",
    severity: MEDIUM,
    auto_fixable: false,
    check: ALL_RELEVANT_ROLES_READY
  },
  {
    id: "SR-READ-03",
    name: "Ambiguity Detection",
    description: "No sentence interpretable 2+ ways",
    severity: HIGH,
    auto_fixable: false,
    check: AMBIGUITY_COUNT == 0
  },
  {
    id: "SR-READ-04",
    name: "Acronym Definitions",
    description: "All acronyms defined on first use",
    severity: LOW,
    auto_fixable: true,
    check: ALL_ACRONYMS_DEFINED
  },
  {
    id: "SR-READ-05",
    name: "Assumptions Stated",
    description: "Implicit assumptions made explicit",
    severity: MEDIUM,
    auto_fixable: false,
    check: ASSUMPTIONS_SECTION_EXISTS_IF_NEEDED
  }
]
```

### Artifact-Specific Application

```text
# For Concept Documents
READER_TEST_FOCUS = [Vision Clarity, Problem Clarity, PM Confidence]
PASS_THRESHOLD = 85%

# For Specifications
READER_TEST_FOCUS = [Actionability, Developer Confidence, QA Confidence]
PASS_THRESHOLD = 90%

# For Plans
READER_TEST_FOCUS = [Actionability, Developer Confidence, Assumptions]
PASS_THRESHOLD = 85%

# For Design Documents
READER_TEST_FOCUS = [Vision Clarity, Designer Confidence, Context]
PASS_THRESHOLD = 80%
```

---

## Examples

### Ambiguity: Before/After

**Before (Ambiguous):**
> The system will process requests faster. It should handle the new requirements
> when needed. Users will see improvements soon.

**After (Clear):**
> The payment processing API will respond in <200ms (currently 800ms).
> When daily transactions exceed 10,000, the queue system activates automatically.
> Performance improvements deploy January 15, 2025.

### Missing Context: Before/After

**Before (Missing Context):**
> Use the CLI tool to generate the config. Make sure RBAC is configured correctly
> before deploying to the K8s cluster.

**After (Context Added):**
> Use the `specify` CLI tool (installation: `uvx specify`) to generate the config.
>
> **Prerequisites:**
> - RBAC (Role-Based Access Control) configured in `rbac.yaml` — see [RBAC Setup Guide](./docs/rbac.md)
> - K8s (Kubernetes) cluster access with `kubectl` configured
>
> Run: `specify init my-project --ai claude`

### Assumption: Before/After

**Before (Implicit Assumption):**
> Deploy the service to production. Users will access via the main dashboard.

**After (Assumption Explicit):**
> **Assumptions:**
> - Production environment (`prod-cluster`) is operational
> - User has deployment permissions (requires `deploy-prod` role)
> - Dashboard v2.3+ is deployed (feature requires new navigation API)
>
> Deploy the service to production using `./deploy.sh prod`.
> Users access via Main Dashboard → Services → [New Service Name].

---

## When to Apply

| Artifact Type | When to Run | Focus Areas |
|---------------|-------------|-------------|
| Concept | After first draft | Vision, Problem, Why |
| Specification | Before self-review | Actionability, Completeness |
| Plan | Before approval | Assumptions, Risks |
| Tasks | After generation | Developer clarity |
| Design | Before handoff | Designer, UX clarity |

---

## Quick Checklist

Before finalizing any artifact, verify:

```text
□ Can someone understand the purpose in 30 seconds?
□ Are all acronyms defined on first use?
□ Are technical terms explained or linked?
□ Is every "it/this/that" clearly referencing something?
□ Are all comparisons specific (faster than X by Y%)?
□ Are timeframes concrete (dates, not "soon")?
□ Are actors explicit (who does what)?
□ Are assumptions stated in a dedicated section?
□ Would each relevant role know their next step?
```
