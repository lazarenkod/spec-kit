# Product Management Anti-Patterns Database

## Overview

This database catalogs common Product Management anti-patterns observed in product development organizations. Each anti-pattern includes detection signals, root causes, consequences, and remediation strategies.

**Usage**: Reference during PRD reviews, retrospectives, and product process audits.

---

## PRD-001: Solution Bias

### Description
Jumping to "User wants feature X" without understanding the underlying job-to-be-done. The PM starts with a solution rather than a problem.

### Detection Signals
- PRD starts with feature description, not user problem
- No user research or customer quotes cited
- "Requirements" are actually implementation details
- Stakeholder says "I want X" and it goes directly into spec
- No alternative solutions considered

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| HiPPO pressure | Highest Paid Person's Opinion becomes requirement |
| Feature parity obsession | "Competitor has it, so we need it" |
| Time pressure | "No time for research, just build it" |
| PM inexperience | Confusion between problem and solution |
| Sales-driven roadmap | Deal-specific features without validation |

### Consequences
- Build wrong thing entirely
- Feature unused after launch
- Technical debt from poorly-scoped work
- Team frustration ("why did we build this?")
- Opportunity cost of not building right thing

### Remediation

**Immediate Actions**:
1. Add mandatory "Problem Statement" section to PRD template
2. Require 3+ user research data points before feature approval
3. Apply "5 Whys" to every feature request

**JTBD Reframe**:
```text
BEFORE (Solution Bias):
"User wants dark mode"

AFTER (JTBD):
"When working late at night on documents,
I want to reduce eye strain from bright screens,
So I can work comfortably for longer periods."

→ Leads to solutions: dark mode, blue light filter,
  scheduled brightness, reading mode, etc.
```

**Process Fix**:
- PRD gate: "Can you articulate the job without mentioning the solution?"
- Require "Jobs Stories" format for all requirements
- Stakeholder training on problem/solution separation

### Prevention Checklist
- [ ] Problem statement doesn't mention solution
- [ ] User research supports problem existence
- [ ] Multiple solution alternatives explored
- [ ] JTBD format used: "When... I want to... So I can..."

---

## PRD-002: Feature Without Success Metrics

### Description
Shipping features without defining how success will be measured. No leading or lagging indicators, no experiment design, no success criteria.

### Detection Signals
- PRD has no "Success Metrics" section
- Success defined as "feature launches"
- Metrics are vanity metrics (pageviews, signups) not behavior change
- No baseline measurement before launch
- Post-launch: no one checks if feature worked

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Ship-it culture | Velocity over outcomes |
| Metrics illiteracy | PM doesn't know which metrics matter |
| Analytics gaps | Can't measure what matters |
| Fear of accountability | Undefined success = no failure |
| Output over outcome | OKRs measure features shipped, not impact |

### Consequences
- Can't prove feature value
- No learning from launch
- Feature bloat (keep building, never pruning)
- Wasted resources on ineffective features
- Death by 1000 features

### Remediation

**Metric Framework**:
```text
For each feature, define:

1. LEADING INDICATOR (short-term, predictive)
   "Within 2 weeks: 30% of users try feature"

2. LAGGING INDICATOR (long-term, outcome)
   "Within 3 months: 15% improvement in retention"

3. GUARDRAIL METRIC (what shouldn't get worse)
   "Page load time stays under 2 seconds"

4. SUCCESS THRESHOLD
   "Ship if: leading indicator > X AND guardrail holds"
```

**Metric Types Hierarchy**:
| Level | Type | Example |
|-------|------|---------|
| 1 | North Star | Weekly active users |
| 2 | Product Health | Retention, engagement |
| 3 | Feature Success | Feature adoption, task completion |
| 4 | Process Health | Time to value, error rates |

**Process Fix**:
- PRD gate: "What's the success metric and target?"
- Launch checklist requires baseline measurement
- 30-day post-launch review mandatory
- Feature flags for easy rollback

### Prevention Checklist
- [ ] Success metric defined before development starts
- [ ] Baseline measurement in place
- [ ] Target threshold documented
- [ ] Guardrail metrics identified
- [ ] Post-launch review scheduled

---

## PRD-003: Requirements Without Personas

### Description
Generic requirements that apply to "users" without specifying which user segment. Results in features that serve no one well.

### Detection Signals
- PRD uses "users" or "customers" generically
- No persona references in user stories
- Same priority for all user needs
- "Everyone wants this" justification
- Edge cases not considered

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| No personas exist | Never created or outdated |
| Persona proliferation | Too many, lose meaning |
| One-size-fits-all thinking | "We serve everyone" |
| B2B complexity | End user vs buyer confusion |
| Research avoidance | Personas feel like overhead |

### Consequences
- Feature serves no one well
- Conflicting requirements from different segments
- Prioritization paralysis
- Marketing can't position product
- Support overwhelmed by diverse needs

### Remediation

**Persona Prioritization Matrix**:
```text
High Value, Underserved
       ▲
       │   "Pro Editors"      "Enterprise Admins"
       │   (Focus here)        (Strategic)
       │
       ├────────────────────────────────────────►
       │                                    Effort to Serve
       │   "Casual Users"      "Legacy Users"
       │   (Serve generically) (Maintain)
       ▼
Low Value, Well-Served
```

**Persona Linking Template**:
```markdown
## User Story: [Feature Name]

### Primary Persona: [Persona Name]
**As a** Power User (Sarah, 35, uses product daily for work)
**I want** keyboard shortcuts for common actions
**So that** I can complete tasks faster without touching the mouse

### Also Benefits:
- Accessibility users (motor impairments)
- Developer persona (efficiency-focused)

### Not For:
- Casual users (added complexity, no benefit)
- Mobile users (no keyboard)
```

**Process Fix**:
- Each PRD must tag primary persona
- User stories start with persona name, not role
- Prioritization weights by persona value
- Quarterly persona validation

### Prevention Checklist
- [ ] Primary persona explicitly named
- [ ] Persona's goals aligned with feature
- [ ] Trade-offs for non-primary personas documented
- [ ] Persona is validated (not hypothetical)

---

## PRD-004: Infinite Backlog

### Description
Never-ending backlog that grows faster than items are completed. Teams feel overwhelmed, important items get lost, and prioritization becomes impossible.

### Detection Signals
- Backlog has 500+ items
- Items at bottom are years old
- No regular grooming/pruning
- Every stakeholder request gets added
- "We'll get to it eventually"

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| FOMO culture | Fear of losing good ideas |
| Stakeholder appeasement | "Added to backlog" vs "no" |
| No deletion authority | PM can't remove items |
| Sunk cost fallacy | "We already discussed this" |
| Backlog as graveyard | Where ideas go to die |

### Consequences
- Important items lost in noise
- Team demoralization ("we'll never finish")
- Stakeholders don't trust system
- Meetings spent on zombie items
- New priorities can't get attention

### Remediation

**Backlog Health Metrics**:
| Metric | Healthy | Unhealthy |
|--------|---------|-----------|
| Total items | <100 | >300 |
| Age of oldest item | <6 months | >1 year |
| Items touched this month | >20% | <5% |
| Items with owner | 100% | <50% |

**Ruthless Prioritization Framework**:
```text
Weekly: Stack rank top 10 items only
Monthly: Archive anything not touched in 3 months
Quarterly: Delete anything archived for 2 quarters

The "Maybe Someday" Archive:
├── Never referenced = Delete at 6 months
├── Referenced once = Keep 3 more months
└── Actively discussed = Promote to backlog
```

**RICE-Based Pruning**:
```text
Calculate RICE score for all items:
- RICE < 100: Archive immediately
- RICE 100-500: Review monthly
- RICE 500-1000: Keep on backlog
- RICE > 1000: Prioritize this sprint
```

**Process Fix**:
- Backlog limit: max 100 items
- "One in, one out" rule
- Quarterly backlog bankruptcy
- Stakeholder-facing "won't do" list

### Prevention Checklist
- [ ] Backlog has explicit size limit
- [ ] Monthly grooming scheduled
- [ ] Archiving criteria defined
- [ ] "No" is an acceptable answer

---

## PRD-005: Output Over Outcome

### Description
Measuring success by features shipped rather than behavior changed. Team celebrates launch day, ignores whether anyone uses the feature.

### Detection Signals
- OKRs measure features delivered
- "We shipped 15 features this quarter!"
- Launch is the finish line
- No post-launch measurement
- Roadmap is a list of features, not goals

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Velocity culture | Speed = success |
| Easier to measure | Counting is simple |
| Quarterly pressure | Features fit quarters, outcomes don't |
| Stakeholder expectations | "What did you ship?" |
| Outcome fear | "What if feature doesn't work?" |

### Consequences
- Feature graveyard (unused features)
- No learning culture
- Technical debt accumulation
- User experience degradation
- Misaligned incentives

### Remediation

**Output vs Outcome Framework**:
```text
OUTPUT (What we build):
"Ship dark mode feature"
↓
OUTCOME (Behavior change):
"Users spend 20% more time in app during evening hours"
↓
IMPACT (Business result):
"Evening session revenue increases 15%"

Always tie OUTPUT → OUTCOME → IMPACT
```

**OKR Reframe**:
```text
❌ OUTPUT-FOCUSED OKR:
Objective: Improve user experience
KR1: Ship dark mode
KR2: Launch 5 new themes
KR3: Redesign settings page

✅ OUTCOME-FOCUSED OKR:
Objective: Users love using our app
KR1: NPS increases from 42 to 55
KR2: Evening session duration up 20%
KR3: Theme-related support tickets down 50%
```

**Process Fix**:
- Ban feature-based OKRs
- Post-launch reviews mandatory at 30/60/90 days
- Celebrate outcomes, not launches
- Feature flags to measure incrementally

### Prevention Checklist
- [ ] Success defined as behavior change, not launch
- [ ] OKRs are outcome-based
- [ ] Post-launch measurement scheduled
- [ ] Features have sunset criteria

---

## PRD-006: Premature Scaling

### Description
Building for scale before achieving product-market fit. Over-engineering solutions for millions of users when you have hundreds.

### Detection Signals
- "This needs to scale to 10 million users"
- Enterprise architecture for MVP
- 6-month timeline for validation feature
- Microservices for team of 5
- "We can't do that because it won't scale"

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Engineering pride | Build it "right" |
| Anticipated success | "When we go viral..." |
| Enterprise habits | Team from big company |
| Scale as excuse | Avoids hard product decisions |
| Fear of rework | "Let's do it once" |

### Consequences
- Slow time-to-market
- Learning delayed
- Resources wasted on unused capacity
- Technical complexity for no benefit
- Product decisions constrained by architecture

### Remediation

**Right-Sizing Framework**:
```text
Stage 1: Problem-Solution Fit (0-100 users)
├── Fake doors, Wizard of Oz
├── Manual processes OK
└── Spreadsheet as backend OK

Stage 2: Product-Market Fit (100-1000 users)
├── MVP architecture
├── Monolith is fine
└── "Things that don't scale" OK

Stage 3: Scaling (1000+ users)
├── Optimize bottlenecks
├── Infrastructure investment
└── Scale architecture
```

**Do Things That Don't Scale**:
| Instead of... | Do this first... |
|---------------|------------------|
| Automated onboarding | Personally onboard first 50 users |
| Self-serve support | Direct Slack channel with users |
| Recommendation engine | Manually curate content |
| Payment processing | Invoice manually |

**Process Fix**:
- Architecture decisions require user count justification
- "Good enough for N users" sizing
- Technical debt budget for iteration
- Explicit scaling milestones

### Prevention Checklist
- [ ] Solution sized for current stage
- [ ] Scaling plan tied to user milestones
- [ ] Manual processes allowed for early stage
- [ ] Technical debt accepted as investment

---

## PRD-007: Stakeholder-Driven Roadmap

### Description
Roadmap driven by loudest stakeholders rather than user needs and strategic priorities. Sales dictates features, executives override priorities.

### Detection Signals
- "Customer X needs this to sign"
- Roadmap changes every board meeting
- Different story to each stakeholder
- No visible prioritization criteria
- PM is order-taker, not strategist

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Revenue pressure | Sales has CEO's ear |
| Weak PM authority | PM can't say no |
| No framework | Prioritization is political |
| Customer success anxiety | Fear of churn |
| Short-term thinking | Quarter-by-quarter survival |

### Consequences
- Fragmented product
- Engineering thrash
- Strategic initiatives never completed
- Team cynicism
- Competitor gains ground

### Remediation

**Stakeholder Prioritization Framework**:
```text
Request → Filter → Prioritize → Communicate

Filter Questions:
1. Does this support our strategy?
2. How many customers need this?
3. What's the revenue impact?
4. What are we NOT doing instead?

Prioritization Formula:
Score = (Strategic Fit × Revenue Impact × User Count) / Effort
```

**Stakeholder Communication Template**:
```markdown
## Request: [Feature Name]
From: [Stakeholder]
Date: [Date]

### Assessment
- Strategic alignment: High/Medium/Low
- User research support: Yes/No
- RICE Score: X

### Decision
☐ Accepted → Roadmap Q[X]
☐ Deferred → Backlog (revisit [date])
☐ Declined → Reason: [X]

### Rationale
[Clear explanation of decision]
```

**Process Fix**:
- Published prioritization criteria
- Stakeholder request intake form
- Monthly roadmap review (not ad-hoc changes)
- Transparent priority stack

### Prevention Checklist
- [ ] Prioritization criteria published
- [ ] All requests through same process
- [ ] Roadmap changes require governance
- [ ] Regular stakeholder communication

---

## PRD-008: Scope Creep Tolerance

### Description
Allowing continuous scope expansion during development without pushback. "Just one more thing" accumulates until projects are months late.

### Detection Signals
- "While we're at it..."
- Projects consistently late
- Original scope forgotten
- No change control process
- PM can't quote current scope

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| People-pleasing | PM wants to say yes |
| Discovery gaps | Didn't know scope upfront |
| Stakeholder pressure | "It's just small" |
| No process | Informal scope management |
| Fear of conflict | Avoids difficult conversations |

### Consequences
- Projects chronically late
- Team burnout
- Quality degradation
- Stakeholder distrust (ironic)
- Original value proposition diluted

### Remediation

**Scope Control Framework**:
```text
Original Scope (locked at kickoff)
         ↓
New Request Arrives
         ↓
┌─────────────────────────────────────┐
│ Trade-off Analysis:                 │
│ • Add this → Remove what?           │
│ • Add this → Extend timeline by?    │
│ • Add this → Increase team by?      │
└─────────────────────────────────────┘
         ↓
Stakeholder Decision (documented)
```

**"Yes, and..." Framework**:
```text
❌ "No, we can't add that"
❌ "Yes, we'll add that"

✅ "Yes, and here's the trade-off:
    - Add X → slip 2 weeks
    - Add X → cut Y
    - Add X → need 1 more engineer
    Which would you prefer?"
```

**Process Fix**:
- Scope frozen after kickoff
- Change request requires written trade-off
- Weekly scope check-ins
- Public scope tracker

### Prevention Checklist
- [ ] Scope documented and approved at kickoff
- [ ] Change requests formal process
- [ ] Trade-offs explicit for every addition
- [ ] Scope visible to all stakeholders

---

## PRD-009: Specification Without Validation

### Description
Writing detailed specifications without validating core assumptions first. Building elaborate plans on unproven foundations.

### Detection Signals
- 50-page PRD for unproven concept
- No prototype or mockup testing
- "We know users want this" (no evidence)
- Months of planning before user contact
- Launch reveals users don't want it

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Waterfall habits | Document first, build later |
| Risk aversion | "Let's plan everything" |
| Stakeholder pressure | "Need detailed spec for approval" |
| PM comfort zone | Writing specs vs talking to users |
| Misunderstood Agile | Specs ≠ user stories alone |

### Consequences
- Wasted planning effort
- Late discovery of fatal flaws
- Sunk cost pressure to continue
- Team distrust of PM
- Slow learning cycles

### Remediation

**Validation-First Framework**:
```text
Level 0: Riskiest Assumption Test (RAT)
├── What's the one thing that must be true?
├── How can we test it in 1 week?
└── Make/kill decision

Level 1: Problem Validation (before solution design)
├── Do users have this problem?
├── Is it painful enough to solve?
└── Will they pay/change behavior?

Level 2: Solution Validation (before full spec)
├── Does this solution resonate?
├── Can users use it?
└── Does it solve the problem?

Level 3: Detailed Specification (after validation)
├── Full PRD
├── Technical design
└── Implementation plan
```

**Validation Methods by Confidence**:
| Method | Confidence | Time |
|--------|------------|------|
| User interviews | Medium | Days |
| Prototype testing | High | Weeks |
| Fake door test | High | Days |
| Concierge MVP | Very High | Weeks |
| Pilot launch | Highest | Months |

**Process Fix**:
- Spec depth proportional to validation level
- "Riskiest Assumption" identified first
- Validation checkpoint before detailed design
- Learn budget before build budget

### Prevention Checklist
- [ ] Riskiest assumption identified
- [ ] Validation plan before detailed spec
- [ ] User research data informs spec
- [ ] Spec depth matches confidence level

---

## PRD-010: Missing Edge Cases

### Description
Specifications that only cover the happy path, ignoring error states, edge cases, and failure modes. Results in poor user experience when things go wrong.

### Detection Signals
- No error state designs
- "Let's handle that later"
- QA finds obvious gaps
- Users encounter unhandled scenarios
- Support tickets reveal unknown states

### Root Causes
| Cause | Why It Happens |
|-------|----------------|
| Optimism bias | "That won't happen" |
| Time pressure | Happy path faster to spec |
| Complexity avoidance | Edge cases are hard |
| Designer gaps | Not trained for failure states |
| User research gaps | Testing happy path only |

### Consequences
- Poor error UX
- User frustration and churn
- Support burden
- Security vulnerabilities
- Data integrity issues

### Remediation

**Edge Case Framework**:
```text
For each feature, document:

1. EMPTY STATES
   - First time user (no data)
   - Deleted content
   - No search results

2. ERROR STATES
   - Network failure
   - Permission denied
   - Invalid input
   - Server error

3. BOUNDARY CONDITIONS
   - Maximum input length
   - Minimum required
   - Rate limits
   - Timeouts

4. CONCURRENT ACCESS
   - Multiple editors
   - Race conditions
   - Stale data

5. ABUSE CASES
   - Malicious input
   - Gaming the system
   - Bot attacks
```

**Edge Case Checklist Template**:
```markdown
## Feature: [Name]

### Happy Path ✅
- User does X → Result Y

### Edge Cases
| Scenario | Frequency | Severity | Handler |
|----------|-----------|----------|---------|
| Empty state | Common | Low | Show empty state UI |
| Network fail | Occasional | Medium | Retry with message |
| Invalid input | Common | Low | Inline validation |
| Concurrent edit | Rare | High | Conflict resolution |
| Rate limit | Rare | Medium | Throttle + message |
```

**Process Fix**:
- Edge case section required in all PRDs
- QA review before development
- Pre-mortem exercise: "What could go wrong?"
- Design review includes error states

### Prevention Checklist
- [ ] Empty states designed
- [ ] Error states for each action
- [ ] Boundary conditions documented
- [ ] Abuse cases considered
- [ ] QA reviewed edge cases before dev

---

## Quick Reference: Anti-Pattern Detection Matrix

| Anti-Pattern | Quick Detection | Immediate Action |
|--------------|-----------------|------------------|
| PRD-001: Solution Bias | PRD leads with feature | Rewrite in JTBD format |
| PRD-002: No Metrics | No success criteria | Add metric section |
| PRD-003: No Personas | "Users" is generic | Name specific persona |
| PRD-004: Infinite Backlog | 500+ items | Backlog bankruptcy |
| PRD-005: Output Focus | OKRs are features | Reframe as outcomes |
| PRD-006: Premature Scaling | "Scale to millions" | Size for current stage |
| PRD-007: Stakeholder-Driven | Roadmap volatility | Publish criteria |
| PRD-008: Scope Creep | Projects always late | Freeze scope at kickoff |
| PRD-009: No Validation | Big spec, no research | Validate assumptions first |
| PRD-010: Missing Edge Cases | Only happy path | Add edge case section |

## Resources

- **Books**: "Inspired" (Marty Cagan), "Escaping the Build Trap" (Melissa Perri)
- **Articles**: "Shape Up" (Basecamp), "JTBD Playbook" (Intercom)
- **Tools**: ProductPlan, Aha!, Productboard
