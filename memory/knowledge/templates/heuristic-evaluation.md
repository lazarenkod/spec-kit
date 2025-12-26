# Heuristic Evaluation Report Template

> **Purpose**: Systematic expert review of UI against established usability principles.
> **When to Use**: Early design review, competitive analysis, or when usability testing isn't feasible.
> **Methodology**: Based on Nielsen's 10 Usability Heuristics with severity rating.

---

## Evaluation Metadata

| Field | Value |
|-------|-------|
| **Product/Feature** | [Name] |
| **Evaluator(s)** | [Name(s)] |
| **Evaluation Date** | [YYYY-MM-DD] |
| **Version/Build** | [Version evaluated] |
| **Scope** | [Screens/flows covered] |
| **Device/Platform** | [Desktop/Mobile/Both] |

---

## Executive Summary

### Overall Usability Score

| Heuristic | Score (1-5) | Issues Found |
|-----------|-------------|--------------|
| H1: Visibility of System Status | [X] | [N] |
| H2: Match Real World | [X] | [N] |
| H3: User Control & Freedom | [X] | [N] |
| H4: Consistency & Standards | [X] | [N] |
| H5: Error Prevention | [X] | [N] |
| H6: Recognition over Recall | [X] | [N] |
| H7: Flexibility & Efficiency | [X] | [N] |
| H8: Aesthetic & Minimalist | [X] | [N] |
| H9: Error Recovery | [X] | [N] |
| H10: Help & Documentation | [X] | [N] |
| **Overall** | **[X.X]** | **[Total]** |

**Score Scale**: 1 = Poor, 2 = Below Average, 3 = Average, 4 = Good, 5 = Excellent

### Issues by Severity

| Severity | Count | % of Total |
|----------|-------|------------|
| 🔴 Critical (4) | [N] | [X%] |
| 🟠 Major (3) | [N] | [X%] |
| 🟡 Minor (2) | [N] | [X%] |
| 🟢 Cosmetic (1) | [N] | [X%] |
| **Total** | **[N]** | **100%** |

### Top 3 Priority Issues

| # | Issue | Heuristic | Severity | Quick Fix |
|---|-------|-----------|----------|-----------|
| 1 | [Issue description] | H[X] | Critical | [Recommendation] |
| 2 | [Issue description] | H[X] | Major | [Recommendation] |
| 3 | [Issue description] | H[X] | Major | [Recommendation] |

---

## Severity Rating Scale

| Rating | Label | Description | User Impact |
|--------|-------|-------------|-------------|
| 0 | Not a problem | Disagree this is a usability issue | None |
| 1 | Cosmetic | Fix if time permits | Minor annoyance |
| 2 | Minor | Low priority fix | Slows users down |
| 3 | Major | Important to fix | Causes errors/frustration |
| 4 | Critical | Must fix before release | Prevents task completion |

**Severity Formula**: `Severity = (Frequency × Impact × Persistence) / 3`

- **Frequency**: How often does it occur? (1=rare, 4=always)
- **Impact**: How serious when it occurs? (1=trivial, 4=catastrophic)
- **Persistence**: Can users overcome it? (1=easily, 4=never)

---

## Heuristic Analysis

### H1: Visibility of System Status

> *"The system should always keep users informed about what is going on, through appropriate feedback within reasonable time."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H1-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H1-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Loading states are clearly indicated
- [ ] Progress indicators for long operations
- [ ] Current location in navigation is highlighted
- [ ] Form field validation shows immediately
- [ ] Action confirmations are provided
- [ ] System response time < 1 second (or feedback shown)

#### Good Examples Found
- ✅ [Positive observation]

---

### H2: Match Between System and Real World

> *"The system should speak the users' language, with words, phrases and concepts familiar to the user."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H2-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H2-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Language uses user's vocabulary, not system jargon
- [ ] Icons match real-world conventions
- [ ] Information appears in logical, natural order
- [ ] Metaphors are appropriate for audience
- [ ] Date/time/number formats match user locale
- [ ] Terminology is consistent with industry standards

#### Good Examples Found
- ✅ [Positive observation]

---

### H3: User Control and Freedom

> *"Users often choose system functions by mistake and need a clearly marked 'emergency exit' to leave the unwanted state."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H3-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H3-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Undo is available for destructive actions
- [ ] Cancel buttons on all dialogs/forms
- [ ] Easy to navigate back to previous state
- [ ] Exit points clearly visible
- [ ] Users can abandon tasks without penalty
- [ ] Confirmations before irreversible actions

#### Good Examples Found
- ✅ [Positive observation]

---

### H4: Consistency and Standards

> *"Users should not have to wonder whether different words, situations, or actions mean the same thing."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H4-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H4-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Same actions have same labels everywhere
- [ ] Visual design consistent across screens
- [ ] Platform conventions followed (iOS/Android/Web)
- [ ] Navigation patterns consistent
- [ ] Error handling consistent
- [ ] Keyboard shortcuts follow conventions

#### Good Examples Found
- ✅ [Positive observation]

---

### H5: Error Prevention

> *"Even better than good error messages is a careful design which prevents problems from occurring in the first place."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H5-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H5-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Dangerous actions require confirmation
- [ ] Constraints prevent invalid input (e.g., date pickers)
- [ ] Default values reduce errors
- [ ] Clear instructions before complex actions
- [ ] Disabled states prevent invalid actions
- [ ] Inline validation before submission

#### Good Examples Found
- ✅ [Positive observation]

---

### H6: Recognition Rather Than Recall

> *"Minimize the user's memory load by making objects, actions, and options visible."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H6-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H6-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Actions visible, not hidden in menus
- [ ] Recent items/history available
- [ ] Autocomplete/suggestions provided
- [ ] Context maintained across sessions
- [ ] Help text visible when needed
- [ ] Users don't need to remember from page to page

#### Good Examples Found
- ✅ [Positive observation]

---

### H7: Flexibility and Efficiency of Use

> *"Accelerators — unseen by the novice user — may speed up interaction for expert users."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H7-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H7-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Keyboard shortcuts for frequent actions
- [ ] Expert modes/power user features
- [ ] Customization options available
- [ ] Batch operations supported
- [ ] Shortcuts discoverable but not required
- [ ] Touch targets appropriately sized (44px minimum)

#### Good Examples Found
- ✅ [Positive observation]

---

### H8: Aesthetic and Minimalist Design

> *"Dialogues should not contain irrelevant or rarely needed information."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H8-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H8-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Only essential information displayed
- [ ] Visual hierarchy guides attention
- [ ] White space used effectively
- [ ] No decorative elements that distract
- [ ] Progressive disclosure for complexity
- [ ] Content is scannable

#### Good Examples Found
- ✅ [Positive observation]

---

### H9: Help Users Recognize, Diagnose, Recover from Errors

> *"Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H9-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H9-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Error messages in plain language (no codes)
- [ ] Errors indicate what went wrong
- [ ] Errors suggest how to fix
- [ ] Errors don't blame users
- [ ] Error styling is clear but not alarming
- [ ] Recovery path is obvious

#### Error Message Evaluation

| Error Found | Current Message | Issues | Improved Version |
|-------------|-----------------|--------|------------------|
| [Context] | "[Current text]" | [Problem] | "[Better text]" |

#### Good Examples Found
- ✅ [Positive observation]

---

### H10: Help and Documentation

> *"Even though it is better if the system can be used without documentation, it may be necessary to provide help."*

**Score**: [1-5]

#### Findings

| ID | Location | Issue | Severity | Recommendation |
|----|----------|-------|----------|----------------|
| H10-01 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |
| H10-02 | [Screen/Component] | [Description of issue] | [1-4] | [How to fix] |

#### Checklist

- [ ] Help is easy to find
- [ ] Help is context-sensitive
- [ ] Documentation is searchable
- [ ] Onboarding/tutorials for new users
- [ ] Tooltips for complex features
- [ ] FAQ addresses common issues

#### Good Examples Found
- ✅ [Positive observation]

---

## Issues Summary

### All Issues by Location

| Screen/Flow | Critical | Major | Minor | Cosmetic | Total |
|-------------|----------|-------|-------|----------|-------|
| [Screen 1] | [N] | [N] | [N] | [N] | [N] |
| [Screen 2] | [N] | [N] | [N] | [N] | [N] |
| [Screen 3] | [N] | [N] | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

### All Issues by Heuristic

```
Issues Distribution:

H1  ████████░░░░░░░░░░░░ 8
H2  ██░░░░░░░░░░░░░░░░░░ 2
H3  ██████░░░░░░░░░░░░░░ 6
H4  ████████████░░░░░░░░ 12
H5  ████░░░░░░░░░░░░░░░░ 4
H6  ██████░░░░░░░░░░░░░░ 6
H7  ██░░░░░░░░░░░░░░░░░░ 2
H8  ████░░░░░░░░░░░░░░░░ 4
H9  ████████░░░░░░░░░░░░ 8
H10 ████░░░░░░░░░░░░░░░░ 4
```

---

## Recommendations

### Immediate Actions (Critical Issues)

| Priority | Issue ID | Fix Description | Effort |
|----------|----------|-----------------|--------|
| 1 | [H#-##] | [Specific fix] | [Low/Med/High] |
| 2 | [H#-##] | [Specific fix] | [Low/Med/High] |
| 3 | [H#-##] | [Specific fix] | [Low/Med/High] |

### Short-Term Actions (Major Issues)

| Priority | Issue ID | Fix Description | Effort |
|----------|----------|-----------------|--------|
| 4 | [H#-##] | [Specific fix] | [Low/Med/High] |
| 5 | [H#-##] | [Specific fix] | [Low/Med/High] |

### Long-Term Improvements

| Priority | Issue ID | Fix Description | Effort |
|----------|----------|-----------------|--------|
| 6 | [H#-##] | [Specific fix] | [Low/Med/High] |

---

## Comparison (Optional)

### Before/After (If Re-evaluation)

| Heuristic | Previous Score | Current Score | Change |
|-----------|----------------|---------------|--------|
| H1 | [X] | [X] | [+/-X] |
| H2 | [X] | [X] | [+/-X] |
| ... | ... | ... | ... |
| **Overall** | **[X.X]** | **[X.X]** | **[+/-X.X]** |

### Competitive Benchmark (If Comparative)

| Heuristic | Our Product | Competitor A | Competitor B |
|-----------|-------------|--------------|--------------|
| H1 | [X] | [X] | [X] |
| H2 | [X] | [X] | [X] |
| ... | ... | ... | ... |
| **Overall** | **[X.X]** | **[X.X]** | **[X.X]** |

---

## Appendix

### A. Screens Evaluated
[List of all screens/pages included in evaluation with screenshots]

### B. Evaluator Notes
[Additional observations, patterns noticed, questions for follow-up]

### C. Methodology Notes
- Evaluation conducted by [N] evaluators independently/together
- Total evaluation time: [X] hours
- Tools used: [Browser, screen recording, etc.]

---

# Heuristic Evaluation Quality Checklist

## Completeness
- [ ] All 10 heuristics evaluated
- [ ] All key screens/flows covered
- [ ] Each finding has severity rating
- [ ] Each finding has recommendation

## Objectivity
- [ ] Findings describe what, not opinions
- [ ] Severity ratings justified
- [ ] Both positives and negatives noted
- [ ] Multiple evaluators compared notes (if applicable)

## Actionability
- [ ] Recommendations are specific
- [ ] Priority order is clear
- [ ] Effort estimates included
- [ ] Quick wins identified

## Documentation
- [ ] Screenshots/examples provided
- [ ] Issue IDs for tracking
- [ ] Evaluator methodology noted
