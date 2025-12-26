# Nielsen's 10 Usability Heuristics Guide

## Overview

Jakob Nielsen's 10 Usability Heuristics are general principles for interaction design. Published in 1994 and updated over time, they remain the most widely used heuristics for usability evaluation.

**Purpose**: Identify usability problems in a user interface through expert evaluation.

## The 10 Heuristics

### H1: Visibility of System Status

**Principle**: The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.

**Implementation**:
| Element | Good Example | Bad Example |
|---------|--------------|-------------|
| Loading | Progress bar with percentage | Blank screen |
| Form submission | "Saving..." then "Saved ✓" | No feedback |
| Navigation | Highlighted current page | No indication of location |
| Upload | Progress indicator, file name | "Please wait..." |

**Feedback Timing**:
| Response Time | User Perception | Design Implication |
|---------------|-----------------|---------------------|
| 0.1 seconds | Instantaneous | No indicator needed |
| 1 second | Noticeable delay | Simple indicator |
| 10+ seconds | Long wait | Progress bar, cancel option |

**Checklist**:
- [ ] Every action has visible feedback
- [ ] Loading states are clearly indicated
- [ ] Progress is shown for long operations
- [ ] Current state/location is always visible

---

### H2: Match Between System and Real World

**Principle**: The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions.

**Implementation**:
| Context | Good | Bad |
|---------|------|-----|
| E-commerce | "Shopping Cart" | "Order Accumulator" |
| Email | "Inbox", "Sent" | "Received Container", "Transmitted Items" |
| Finance | "Balance", "Transfer" | "Account State", "Fund Relocation" |
| Calendar | "Today", "Tomorrow" | "Current Date Instance" |

**Metaphors That Work**:
- Desktop (files, folders, trash)
- Shopping cart
- Bookmarks
- Dashboard

**Checklist**:
- [ ] Labels use user's vocabulary, not system's
- [ ] Icons match real-world metaphors
- [ ] Information flows in logical order
- [ ] Units and formats match user expectations

---

### H3: User Control and Freedom

**Principle**: Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process.

**Implementation**:
| Feature | Implementation |
|---------|----------------|
| Undo | Ctrl+Z, "Undo" button, undo toast |
| Cancel | Clear cancel button in dialogs |
| Back | Browser back works, breadcrumbs |
| Escape | ESC closes modals, cancels actions |
| Reset | Clear form, restore defaults |

**Undo Patterns**:
```text
Simple Undo:
[Action] ──► "Done. Undo?" ──► [Undo clicked] ──► [Restored]

Time-limited Undo:
[Delete] ──► "Deleted. Undo (5s)" ──► [Timer expires] ──► [Permanent]

Multi-level Undo:
[Action 1] ──► [Action 2] ──► [Action 3]
                    ◄── Undo ◄── Undo
```

**Checklist**:
- [ ] Undo is available for destructive actions
- [ ] Cancel is clearly visible in all flows
- [ ] Users can exit any state easily
- [ ] Multi-step processes allow going back

---

### H4: Consistency and Standards

**Principle**: Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

**Types of Consistency**:
| Type | Description | Example |
|------|-------------|---------|
| **Internal** | Consistent within your product | Same button style everywhere |
| **External** | Consistent with platform/industry | iOS design patterns on iOS |
| **Visual** | Same look for same function | Primary buttons always blue |
| **Functional** | Same action, same result | "Save" always saves |
| **Linguistic** | Same terminology | "Delete" vs "Remove" — pick one |

**Common Standards**:
- Logo links to home
- Underlined blue text is a link
- X closes modals
- Search icon is a magnifying glass
- Settings is a gear icon

**Checklist**:
- [ ] Same patterns used throughout product
- [ ] Platform conventions followed
- [ ] Terminology is consistent
- [ ] Visual hierarchy is consistent

---

### H5: Error Prevention

**Principle**: Good error messages are important, but the best designs carefully prevent problems from occurring in the first place.

**Error Types and Prevention**:
| Error Type | Prevention Strategy |
|------------|---------------------|
| Slips (unconscious) | Constraints, defaults, confirmations |
| Mistakes (conscious) | Clear options, good defaults, guidance |

**Prevention Techniques**:
| Technique | Example |
|-----------|---------|
| Constraints | Date picker instead of text field |
| Defaults | Pre-fill likely values |
| Confirmations | "Delete this? This cannot be undone" |
| Inline validation | Check email format as user types |
| Suggestions | Autocomplete, "Did you mean...?" |
| Warnings | "You have unsaved changes" |

**Confirmation Dialog Best Practices**:
```text
❌ Bad:
"Are you sure?"
[OK] [Cancel]

✅ Good:
"Delete 'Project Alpha'? This will permanently remove all files."
[Cancel] [Delete Project]
```

**Checklist**:
- [ ] Dangerous actions require confirmation
- [ ] Input constraints prevent invalid data
- [ ] Defaults reduce decision burden
- [ ] Inline validation catches errors early

---

### H6: Recognition Rather Than Recall

**Principle**: Minimize the user's memory load by making elements, actions, and options visible. Users should not have to remember information from one part of the interface to another.

**Memory Load Reduction**:
| Pattern | Implementation |
|---------|----------------|
| Show, don't hide | Visible navigation vs. hamburger menu |
| Recent items | "Recently viewed", "Recent searches" |
| Autocomplete | Suggest as user types |
| Preview | Show effect before committing |
| Labels on icons | Text + icon, not icon alone |

**Recognition vs. Recall**:
```text
Recall (harder):
"Type the product code to continue"

Recognition (easier):
[Product A] [Product B] [Product C] ← Choose one
```

**Checklist**:
- [ ] Options are visible, not hidden
- [ ] Icons have labels
- [ ] Help is contextual, not separate
- [ ] Recently used items are easily accessible

---

### H7: Flexibility and Efficiency of Use

**Principle**: Accelerators — unseen by the novice user — may speed up interaction for the expert user. Allow users to tailor frequent actions.

**Accelerator Types**:
| Type | Example |
|------|---------|
| Keyboard shortcuts | Ctrl+S to save |
| Touch gestures | Swipe to delete |
| Command palette | Cmd+K to search/command |
| Macros | Record and replay actions |
| Customization | Toolbar customization |
| Templates | Pre-built starting points |

**Novice-Expert Spectrum**:
```text
Novice ◄────────────────────────────────► Expert
  │                                          │
  ▼                                          ▼
Menu navigation                     Keyboard shortcuts
Step-by-step                        Quick actions
Tooltips needed                     Power user features
Visible options                     Customized workflow
```

**Checklist**:
- [ ] Keyboard shortcuts for common actions
- [ ] Shortcuts are discoverable (shown in menus)
- [ ] Power users can customize
- [ ] Both mouse and keyboard work

---

### H8: Aesthetic and Minimalist Design

**Principle**: Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information in an interface competes with relevant units of information.

**Signal-to-Noise Ratio**:
```text
High S/N (Good):
┌──────────────────────────────────┐
│ Order #12345       Status: Shipped│
│ Arriving: Tomorrow               │
│                    [Track Order] │
└──────────────────────────────────┘

Low S/N (Bad):
┌──────────────────────────────────────────────────┐
│ ORDER CONFIRMATION #12345-ABC-789                │
│ Thank you for your order! We appreciate your...  │
│ Order placed: 2024-01-15T14:32:00Z               │
│ Payment method: ****1234 (Visa)                  │
│ Billing address: 123 Main St, Apt 4B, ...       │
│ Shipping method: Standard Ground                 │
│ Carrier: UPS Ground                              │
│ Tracking: 1Z999AA10123456784                     │
│ Status: In Transit                               │
│ Estimated: 2024-01-17                            │
│ [Track] [Contact] [Return] [Reorder] [Share]    │
└──────────────────────────────────────────────────┘
```

**Minimalism Techniques**:
- Progressive disclosure (show more on demand)
- Prioritize content hierarchy
- Remove redundant labels
- Use whitespace effectively
- One primary action per screen

**Checklist**:
- [ ] Only essential information shown
- [ ] Visual hierarchy guides attention
- [ ] Secondary info is accessible but not prominent
- [ ] Design is clean, not cluttered

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Principle**: Error messages should be expressed in plain language (not error codes), precisely indicate the problem, and constructively suggest a solution.

**Error Message Formula**:
```text
[What happened] + [Why it happened] + [How to fix it]

Bad: "Error 403"
Good: "You don't have permission to view this file. Ask the owner to share it with you."
```

**Error Message Examples**:
| Situation | Bad | Good |
|-----------|-----|------|
| Wrong password | "Authentication failed" | "Incorrect password. Try again or reset it." |
| Network error | "Error -1009" | "No internet connection. Check your network." |
| Form validation | "Invalid input" | "Email must include @ symbol" |
| Server error | "500 Internal Server Error" | "Something went wrong. We're looking into it." |

**Error Message Checklist**:
- [ ] Written in plain language
- [ ] Explains what went wrong
- [ ] Suggests how to fix it
- [ ] Provides an action (retry, contact support, etc.)
- [ ] Doesn't blame the user

---

### H10: Help and Documentation

**Principle**: It's best if the system can be used without documentation, but it may be necessary to provide help and documentation. Help should be easy to search, focused on the user's task, list concrete steps, and not be too large.

**Help Types**:
| Type | Description | Example |
|------|-------------|---------|
| Inline hints | Contextual tips | Placeholder text, tooltips |
| Onboarding | First-time guidance | Tours, coachmarks |
| In-app help | Task-focused help | Help sidebar, tooltips |
| Documentation | Comprehensive reference | Help center, docs |
| Search | Find answers quickly | Search in help center |

**Help Content Principles**:
1. **Task-focused**: Organized by what users want to do
2. **Searchable**: Easy to find specific topics
3. **Concise**: Minimal reading, maximum doing
4. **Actionable**: Clear steps, not theory
5. **Visual**: Screenshots, videos where helpful

**Checklist**:
- [ ] Help is searchable
- [ ] Content is task-oriented
- [ ] Steps are clear and numbered
- [ ] Help is contextual when possible

---

## Heuristic Evaluation Process

### Step 1: Prepare

1. Define scope (which screens/flows)
2. Gather 3-5 evaluators
3. Create evaluation template

### Step 2: Evaluate Individually

Each evaluator reviews independently:
1. Go through the interface twice
2. First pass: Get familiar with flow
3. Second pass: Apply heuristics, note issues

### Step 3: Rate Severity

| Rating | Severity | Priority |
|--------|----------|----------|
| 0 | Not a usability problem | - |
| 1 | Cosmetic only | Fix if time permits |
| 2 | Minor usability problem | Low priority |
| 3 | Major usability problem | High priority |
| 4 | Usability catastrophe | Must fix |

### Step 4: Aggregate Findings

Compile all evaluators' findings, remove duplicates, prioritize by severity.

## Evaluation Template

```markdown
# Heuristic Evaluation: [Product/Feature]

**Evaluator**: [Name]
**Date**: [Date]
**Scope**: [Screens evaluated]

## Findings

### Issue #1
- **Heuristic**: H[X] - [Heuristic Name]
- **Location**: [Screen/Element]
- **Severity**: [0-4]
- **Description**: [What's the problem]
- **Recommendation**: [How to fix]
- **Screenshot**: [If applicable]

### Issue #2
...

## Summary

| Heuristic | Issues Found | Avg Severity |
|-----------|--------------|--------------|
| H1 | X | X.X |
| H2 | X | X.X |
...

**Total Issues**: X
**Critical (Sev 4)**: X
**Major (Sev 3)**: X
```

## Resources

- **Original Paper**: Nielsen, J. (1994). "Enhancing the Explanatory Power of Usability Heuristics"
- **NN/g Website**: [nngroup.com](https://www.nngroup.com/articles/ten-usability-heuristics/)
- **Related Methods**: Cognitive walkthrough, usability testing, accessibility audit
