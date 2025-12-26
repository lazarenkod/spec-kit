# UX Anti-Patterns Database

## Overview

This database catalogs common UX anti-patterns that degrade user experience. Each anti-pattern includes detection methods, psychological root causes, real-world examples, and remediation strategies.

**Usage**: Reference during design reviews, usability audits, and heuristic evaluations.

---

## UX-001: Modal Overload

### Description
Excessive use of modal dialogs that interrupt user flow, create cognitive dissonance, and prevent task completion.

### Detection Signals
- Multiple modals per screen
- Modals appearing immediately on page load
- Nested modals (modal opens another modal)
- Non-dismissable modals (no X or ESC)
- Modal for every confirmation
- "Are you sure you want to close this modal?" pattern

### Psychological Impact
| Impact | Why It Hurts |
|--------|--------------|
| Cognitive interruption | Flow state destroyed |
| Learned helplessness | Users stop reading modals |
| Attention blindness | Important modals ignored |
| Exit intent | Users leave rather than deal with modals |
| Frustration buildup | Each modal adds friction |

### Nielsen Heuristic Violations
- **H3 (User Control & Freedom)**: Forced interruption
- **H8 (Aesthetic & Minimalist Design)**: Information noise

### Remediation

**Modal Alternatives**:
```text
Instead of Modal → Use:

Confirmation → Undo toast
Settings → Slide-over panel
Additional info → Tooltip or expand-in-place
Warnings → Inline banner
Form → Dedicated page or inline expansion
Onboarding → Coach marks or inline tips
```

**Modal Usage Guidelines**:
```text
✅ USE MODAL WHEN:
- Action is truly destructive and irreversible
- External context required (e.g., payment)
- Legal requirement (e.g., consent)
- Short, focused task (1-2 actions)

❌ AVOID MODAL WHEN:
- Information can display inline
- User initiated action (no confirmation needed)
- Content requires scrolling
- User needs to reference page content
```

**Modal Design Checklist**:
- [ ] Dismissable via X, ESC, and backdrop click
- [ ] Clear title stating purpose
- [ ] Primary action clearly highlighted
- [ ] Secondary action is "Cancel" not "No"
- [ ] Maximum 2 modals deep (prefer 1)
- [ ] Mobile: full-screen or bottom sheet

### Prevention Pattern
Use **progressive disclosure** instead:
```text
[See Details] → Expand section in-place
[Edit] → Inline editing mode
[Confirm] → Undo toast with 5-second window
```

---

## UX-002: Hidden Navigation

### Description
Critical navigation and features hidden behind hamburger menus, gestures, or obscure icons, forcing users to discover functionality.

### Detection Signals
- Desktop site using hamburger menu
- Key actions only in hamburger menu
- No visible navigation bar
- Reliance on swipe gestures without hints
- "Long press for options" without indicator
- Icon-only navigation without labels

### Discovery Problems
| Issue | Impact |
|-------|--------|
| Menu blindness | Users don't know hamburger has content |
| Feature ignorance | Users never find key functionality |
| Task abandonment | Can't find how to complete goal |
| Support burden | "How do I...?" tickets |
| Competitive disadvantage | Competitor's visible feature wins |

### Nielsen Heuristic Violations
- **H6 (Recognition over Recall)**: Forces memorization
- **H7 (Flexibility & Efficiency)**: Hidden accelerators

### Remediation

**Navigation Visibility Matrix**:
```text
                     High Frequency
                          │
    ALWAYS VISIBLE        │        VISIBLE + SHORTCUT
    (Primary nav,         │        (Search, actions)
    Core features)        │
                          │
──────────────────────────┼──────────────────────────
                          │
    DISCOVERABLE          │        HIDDEN OK
    (Secondary nav,       │        (Rare settings,
    power features)       │        edge cases)
                          │
                     Low Frequency
```

**Desktop vs Mobile**:
| Viewport | Recommendation |
|----------|----------------|
| Desktop (>1024px) | Full navigation visible |
| Tablet (768-1024px) | Condensed nav, hamburger for secondary |
| Mobile (<768px) | Bottom nav for primary, hamburger for secondary |

**Bottom Navigation Pattern**:
```text
Mobile: Use bottom navigation for top 4-5 actions

┌────────────────────────────────────────┐
│           App Content                  │
│                                        │
├────────────────────────────────────────┤
│  🏠      🔍      ➕      💬      👤    │
│ Home   Search  Create  Chat   Profile  │
└────────────────────────────────────────┘
```

### Prevention Checklist
- [ ] Primary navigation visible at all times
- [ ] Icons have text labels (not icon-only)
- [ ] Hamburger only for secondary navigation
- [ ] Gestures have visual hints
- [ ] First-time user can find all core features

---

## UX-003: Form Abandonment Design

### Description
Form design that maximizes abandonment through long forms, poor validation, unclear requirements, and confusing layouts.

### Detection Signals
- 20+ fields on single page
- No progress indicator on multi-step forms
- Validation only on submit
- Generic error messages ("Invalid input")
- Required fields not marked
- Placeholder text as labels (disappears on focus)
- No autocomplete attributes

### Abandonment Causes
| Issue | Abandonment Rate Impact |
|-------|-------------------------|
| 1 extra field | +10% abandonment |
| No progress indicator | +28% abandonment |
| Submit-only validation | +40% abandonment |
| Account required first | +35% abandonment |

### Nielsen Heuristic Violations
- **H5 (Error Prevention)**: Late validation
- **H9 (Error Recovery)**: Unclear error messages
- **H10 (Help & Documentation)**: No guidance

### Remediation

**Progressive Form Pattern**:
```text
Step 1: Minimum Viable Information
├── Email only (1 field)
└── "Continue" button

Step 2: Essential Details
├── Name, Password
└── Progress: ●●○○ (2 of 4)

Step 3: Profile Enhancement (optional)
├── Avatar, preferences
└── "Skip for now" option

Step 4: Confirmation
└── Summary + "Complete"
```

**Inline Validation Rules**:
```text
Validate WHEN:
- Field loses focus (blur)
- User pauses typing (debounce 800ms)
- Form submit (catch stragglers)

Show Error AS:
- Inline, below field
- Red border + icon
- Specific: "Password needs 8+ characters" not "Invalid"

Show Success AS:
- Green checkmark
- "Email available" for unique fields
```

**Form Field Optimization**:
```text
❌ REMOVE OR DEFER:
- Gender (unless legally required)
- Phone (unless 2FA)
- Address (until checkout)
- Birthday (unless age-gated)

✅ USE SMART DEFAULTS:
- Country from IP
- State from ZIP
- City from ZIP
- Format from locale
```

### Prevention Checklist
- [ ] Form has minimum viable fields
- [ ] Progress indicator for multi-step
- [ ] Inline validation on blur
- [ ] Error messages are specific and actionable
- [ ] Required fields clearly marked
- [ ] Autocomplete attributes set
- [ ] Mobile-friendly input types

---

## UX-004: Invisible System Status

### Description
Failing to communicate system status — loading, processing, success, or failure — leaving users uncertain if their actions worked.

### Detection Signals
- Button click with no visual feedback
- Long operations with no progress indicator
- No success confirmation after action
- Errors fail silently
- "Did it work?" uncertainty
- Users clicking multiple times

### User Uncertainty Timeline
| Time | User Experience |
|------|-----------------|
| 0-100ms | Instant feedback expected |
| 100ms-1s | "Something is happening" needed |
| 1-10s | Progress indicator needed |
| 10s+ | Time estimate + cancel option needed |

### Nielsen Heuristic Violations
- **H1 (Visibility of System Status)**: Primary violation

### Remediation

**Feedback Framework**:
```text
USER ACTION → IMMEDIATE FEEDBACK → PROCESS → RESULT

Click button:
  [Button Press] → [Visual press state] →
  [Loading spinner] → [Success toast / Error banner]

Form submit:
  [Submit] → [Button: "Saving..."] →
  [Disable form] → [Success: "Saved ✓" / Error with retry]

File upload:
  [Select file] → [Preview + progress bar] →
  [xx% uploaded] → [Complete with checkmark]
```

**Feedback Types by Duration**:
| Duration | Feedback Pattern |
|----------|-----------------|
| <100ms | Button state change |
| 100ms-1s | Spinner on button |
| 1-5s | Full-screen spinner or progress |
| 5-30s | Progress bar with percentage |
| 30s+ | Background task with notification |

**Success/Failure Patterns**:
```text
SUCCESS:
✓ "Project created successfully" [View Project]
├── Green color
├── Checkmark icon
├── Auto-dismiss in 5s
└── Action button for next step

FAILURE:
✗ "Couldn't save changes. Check your connection." [Retry]
├── Red/amber color
├── X or warning icon
├── Persistent until dismissed
└── Retry button or troubleshooting link
```

### Prevention Checklist
- [ ] Every button has hover/active/loading states
- [ ] Operations >1s have progress indicator
- [ ] Success confirmations for all mutations
- [ ] Errors surface with recovery actions
- [ ] Optimistic UI for perceived speed

---

## UX-005: Cognitive Overload

### Description
Overwhelming users with too many options, information, or decisions at once, leading to decision paralysis and task failure.

### Detection Signals
- 15+ menu items in single menu
- Dashboard with 20+ widgets
- Form asking 10 questions at once
- Settings page with 50+ options
- No visual hierarchy (everything looks equal)
- "I don't know where to start"

### Psychological Limits
| Limit | Research Finding |
|-------|------------------|
| Working memory | 7±2 items (Miller's Law) |
| Decision fatigue | Quality degrades after ~10 decisions |
| Choice paradox | More options → less satisfaction |
| Attention span | 8 seconds average |

### Nielsen Heuristic Violations
- **H8 (Aesthetic & Minimalist Design)**: Information overload
- **H6 (Recognition over Recall)**: Too much to remember

### Remediation

**Information Hierarchy Framework**:
```text
LEVEL 1: Primary (always visible)
├── Core task elements
├── 1 primary action
└── Max 5-7 items

LEVEL 2: Secondary (visible on demand)
├── Supporting information
├── Secondary actions
└── Expand/collapse sections

LEVEL 3: Tertiary (discoverable)
├── Advanced settings
├── Edge case options
└── Expert features
```

**Progressive Disclosure Pattern**:
```text
Initial View:
┌─────────────────────────────────────┐
│ Basic Settings                      │
│ ┌─────────────────────────────────┐ │
│ │ Name: [___________]             │ │
│ │ Email: [___________]            │ │
│ └─────────────────────────────────┘ │
│ [▶ Advanced Settings]               │
└─────────────────────────────────────┘

Expanded:
┌─────────────────────────────────────┐
│ Basic Settings                      │
│ ┌─────────────────────────────────┐ │
│ │ Name: [___________]             │ │
│ │ Email: [___________]            │ │
│ └─────────────────────────────────┘ │
│ [▼ Advanced Settings]               │
│ ┌─────────────────────────────────┐ │
│ │ Timezone: [___________]         │ │
│ │ Language: [___________]         │ │
│ │ Notifications: [▼]              │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Choice Reduction Strategies**:
| Strategy | Example |
|----------|---------|
| Smart defaults | Pre-select most common option |
| Recommendations | "Most users choose..." |
| Categorization | Group related options |
| Progressive disclosure | Show more on demand |
| Wizard pattern | One question per step |

### Prevention Checklist
- [ ] Maximum 7 items at each level
- [ ] Clear visual hierarchy
- [ ] Progressive disclosure for complexity
- [ ] Smart defaults reduce decisions
- [ ] White space aids scanning

---

## UX-006: Destructive Action Without Confirmation

### Description
Allowing irreversible actions without adequate warning, undo capability, or confirmation — violating user trust when data is lost.

### Detection Signals
- Delete with single click
- No undo for destructive actions
- Confirmation is generic "Are you sure?"
- Confirmation button same as action button
- Archive/delete same visual weight
- Permanent actions look like temporary ones

### Destruction Spectrum
| Action Level | Protection Needed |
|--------------|-------------------|
| Low (mark read) | None |
| Medium (archive) | Undo toast |
| High (delete) | Confirmation dialog |
| Critical (delete account) | Friction + confirmation |

### Nielsen Heuristic Violations
- **H3 (User Control & Freedom)**: No emergency exit
- **H5 (Error Prevention)**: Allows harmful slips

### Remediation

**Confirmation Dialog Best Practices**:
```text
❌ BAD DIALOG:
"Are you sure?"
[OK] [Cancel]

✅ GOOD DIALOG:
"Delete project 'Alpha Launch'?"
This will permanently delete all 47 files and 12 tasks.
This cannot be undone.

[Cancel]  [Delete Project]
            ↑ Red/destructive styling
```

**Protection Levels**:
```text
Level 1: Undo Toast (soft delete)
┌──────────────────────────────────────────┐
│ ✓ Item archived  [UNDO] ────────── 5s ── │
└──────────────────────────────────────────┘

Level 2: Confirmation Dialog (hard delete)
┌──────────────────────────────────────────┐
│ Delete "Project Alpha"?                  │
│                                          │
│ 47 files and 12 tasks will be deleted.   │
│ This cannot be undone.                   │
│                                          │
│ [Cancel]                [Delete Project] │
└──────────────────────────────────────────┘

Level 3: Friction + Confirmation (critical)
┌──────────────────────────────────────────┐
│ Delete your account?                     │
│                                          │
│ Type "DELETE" to confirm:                │
│ [_______________]                        │
│                                          │
│ [Cancel]         [Delete My Account]     │
└──────────────────────────────────────────┘
```

**Undo vs Confirm Matrix**:
| Frequency | Reversibility | Pattern |
|-----------|---------------|---------|
| Common | Reversible | Undo toast |
| Common | Irreversible | Confirmation |
| Rare | Reversible | No protection |
| Rare | Irreversible | Friction + confirm |

### Prevention Checklist
- [ ] Destructive actions have distinct styling (red)
- [ ] Confirmation describes what will be lost
- [ ] Primary button is safe action (Cancel)
- [ ] Undo available for reversible actions
- [ ] Critical actions require typed confirmation

---

## UX-007: Mobile Neglect

### Description
Designing desktop-first (or only) and treating mobile as an afterthought, resulting in unusable mobile experiences.

### Detection Signals
- Desktop site served to mobile
- Horizontal scroll on mobile
- Tap targets too small
- Forms impossible to complete on mobile
- "View Desktop Site" as primary option
- Text requires pinch-zoom to read

### Mobile Reality
| Stat | Implication |
|------|-------------|
| 55%+ web traffic is mobile | Mobile-first, not mobile-maybe |
| Average mobile session: 72 seconds | Optimize for speed |
| 53% abandon if load >3s | Performance critical |
| Touch accuracy: 7mm target min | 44px minimum touch target |

### Nielsen Heuristic Violations
- **H4 (Consistency & Standards)**: Violates mobile conventions
- **H7 (Flexibility & Efficiency)**: Touch inefficient

### Remediation

**Mobile-First Design Principles**:
```text
1. Content Priority
   Desktop: 3 columns
   Tablet: 2 columns
   Mobile: 1 column (stacked)

2. Touch Targets
   Minimum: 44×44 pixels
   Comfortable: 48×48 pixels
   Spacing: 8px between targets

3. Navigation
   Desktop: Top nav bar
   Tablet: Condensed top nav
   Mobile: Bottom nav (thumb zone)

4. Forms
   Full-width inputs
   Native keyboards (type="email", "tel")
   Minimal fields
```

**Thumb Zone Design**:
```text
┌──────────────────────────────────────┐
│                                      │
│          Hard to reach               │
│       (Secondary actions)            │
│                                      │
│                                      │
│          OK to reach                 │
│       (Content viewing)              │
│                                      │
│                                      │
│          Easy to reach               │
│       (Primary actions, nav)         │
│                                      │
│ ─────────────────────────────────────│
│  🏠   🔍    ➕    💬    👤           │  ← Thumb zone
└──────────────────────────────────────┘
```

**Mobile Form Optimization**:
| Input Type | Mobile Optimization |
|------------|---------------------|
| Email | type="email" (@ keyboard) |
| Phone | type="tel" (number pad) |
| Number | inputmode="numeric" |
| Date | Native date picker |
| Select | Native OS picker |

### Prevention Checklist
- [ ] Responsive breakpoints tested
- [ ] Touch targets ≥44px
- [ ] No horizontal scroll
- [ ] Forms use correct input types
- [ ] Primary actions in thumb zone
- [ ] Performance budget enforced

---

## UX-008: Accessibility Afterthought

### Description
Treating accessibility as a post-launch checkbox rather than a design requirement, excluding users with disabilities.

### Detection Signals
- No keyboard navigation
- Images without alt text
- Low color contrast
- No focus indicators
- Video without captions
- Screen reader incompatible
- "We'll add accessibility later"

### User Impact
| Disability Type | Affected Users | Common Barriers |
|-----------------|----------------|-----------------|
| Visual | 285M worldwide | No alt text, low contrast |
| Motor | 75M+ | No keyboard nav, small targets |
| Hearing | 466M | No captions, audio-only |
| Cognitive | 10-15% | Complex language, no structure |

### WCAG 2.1 AA Core Failures
| Criterion | Common Failure |
|-----------|----------------|
| 1.1.1 Non-text Content | Missing alt text |
| 1.4.3 Contrast | Text below 4.5:1 ratio |
| 2.1.1 Keyboard | Not all functions keyboard accessible |
| 2.4.7 Focus Visible | Focus indicator hidden |
| 4.1.2 Name, Role, Value | Custom controls not labelled |

### Remediation

**Accessibility Baseline Checklist**:
```text
PERCEIVABLE
☐ All images have alt text
☐ Color contrast ≥4.5:1 (text) ≥3:1 (large text)
☐ Video has captions
☐ Content scales to 200% zoom

OPERABLE
☐ All functions keyboard accessible
☐ Focus order is logical
☐ Focus indicator visible
☐ No keyboard traps
☐ Skip to content link

UNDERSTANDABLE
☐ Page language declared
☐ Error messages identify the error
☐ Labels associated with inputs
☐ Consistent navigation

ROBUST
☐ Valid HTML
☐ ARIA used correctly
☐ Works with assistive tech
```

**Component Accessibility Pattern**:
```html
<!-- Accessible Button -->
<button
  type="button"
  aria-label="Close dialog"
  aria-pressed="false"
  class="btn-close"
>
  <span aria-hidden="true">×</span>
</button>

<!-- Accessible Form Field -->
<div class="form-field">
  <label for="email" id="email-label">Email Address</label>
  <input
    type="email"
    id="email"
    aria-describedby="email-help email-error"
    aria-invalid="false"
  />
  <span id="email-help" class="help-text">We'll never share your email</span>
  <span id="email-error" class="error" role="alert"></span>
</div>
```

**Testing Tools**:
| Tool | Purpose |
|------|---------|
| axe DevTools | Automated testing |
| WAVE | Visual accessibility checker |
| VoiceOver/NVDA | Screen reader testing |
| Keyboard only | Navigation testing |
| Color contrast analyzer | Ratio checking |

### Prevention Checklist
- [ ] Accessibility requirements in design specs
- [ ] Component library accessibility audited
- [ ] Automated testing in CI/CD
- [ ] Manual keyboard testing each sprint
- [ ] Screen reader testing quarterly

---

## UX-009: Inconsistent Patterns

### Description
Using different patterns for similar functions throughout the product, increasing cognitive load and destroying user expectations.

### Detection Signals
- Multiple button styles for same action
- Different confirmation patterns per feature
- Navigation changes between sections
- Different form layouts per page
- Icons mean different things in different places
- "Edit" vs "Modify" vs "Change" (same action)

### Consistency Breakdown
| Type | Description | Example Violation |
|------|-------------|-------------------|
| **Visual** | Same look for same function | Primary button: Blue here, green there |
| **Behavioral** | Same action, same result | Save: dialog here, toast there |
| **Linguistic** | Same terminology | Delete/Remove/Trash interchangeably |
| **Platform** | Match OS conventions | iOS: swipe-to-delete absent |

### Nielsen Heuristic Violations
- **H4 (Consistency & Standards)**: Primary violation

### Remediation

**Design System Enforcement**:
```text
Component Usage Rules:

1. PRIMARY ACTION (one per screen)
   - Always blue (#0066CC)
   - Always 40px height on desktop
   - Always labeled with verb (Save, Submit, Create)

2. SECONDARY ACTION
   - Always ghost/outline style
   - Same height as primary
   - Less prominent than primary

3. DESTRUCTIVE ACTION
   - Always red (#DC2626)
   - Always confirmation required
   - Never primary position
```

**Terminology Glossary**:
| Concept | Standard Term | Never Use |
|---------|---------------|-----------|
| Remove from list | Remove | Delete (implies permanent) |
| Permanently destroy | Delete | Remove, Trash |
| Temporary hide | Archive | Delete |
| Stop service | Cancel | Terminate, End |
| Navigate away | Back | Return, Go Back |

**Consistency Audit Template**:
```markdown
## Pattern: [Action/Element]

### Current Usage
| Screen | Variation | Pattern |
|--------|-----------|---------|
| Dashboard | Blue button | A |
| Settings | Green button | B |
| Profile | Link style | C |

### Standard Pattern: A (Blue button)

### Migration Plan
1. Update Settings → Pattern A
2. Update Profile → Pattern A
3. Update design system documentation
```

### Prevention Checklist
- [ ] Design system documented and enforced
- [ ] Component library is single source
- [ ] Pattern library for common interactions
- [ ] Terminology glossary maintained
- [ ] Regular consistency audits

---

## UX-010: Error State Neglect

### Description
Designing only the happy path while ignoring error states, empty states, and edge cases — leaving users stranded when things go wrong.

### Detection Signals
- No empty state designs
- Error messages are "Something went wrong"
- Loading states inconsistent or missing
- Edge cases discovered in production
- "What happens when...?" answer is "I don't know"

### State Coverage Gap
| State Type | Design Coverage Needed |
|------------|------------------------|
| Empty | First use, no data, no results |
| Loading | Initial, skeleton, partial |
| Error | Network, permission, validation, server |
| Partial | Some data missing, degraded mode |
| Edge | Maximum data, minimum data, special chars |

### Nielsen Heuristic Violations
- **H9 (Error Recovery)**: No helpful error messages
- **H5 (Error Prevention)**: Edge cases not considered

### Remediation

**State Design Framework**:
```text
For each component/screen, design:

1. IDEAL STATE (happy path)
   └── Full data, working correctly

2. EMPTY STATES
   ├── First time (no content yet)
   │   └── Onboarding, call-to-action
   ├── No results (search/filter)
   │   └── Clear filters, suggestions
   └── Cleared (user deleted all)
       └── Confirmation, next action

3. LOADING STATES
   ├── Initial load (skeleton)
   ├── Refresh (pull-to-refresh indicator)
   ├── Pagination (loading more)
   └── Background (non-blocking indicator)

4. ERROR STATES
   ├── Network error (offline/timeout)
   │   └── Retry button, cache fallback
   ├── Permission denied (403)
   │   └── Request access, explanation
   ├── Not found (404)
   │   └── Navigation options, search
   └── Server error (500)
       └── Apology, try later, support

5. PARTIAL STATES
   └── Some data available, some failed
       └── Show available, indicate missing
```

**Error Message Formula**:
```text
[What happened] + [Why it might have happened] + [What to do]

❌ BAD: "Error"
❌ BAD: "Something went wrong"
❌ BAD: "Error 500: Internal Server Error"

✅ GOOD: "Couldn't load your projects.
          Check your internet connection and try again."
          [Try Again] [Work Offline]

✅ GOOD: "You don't have access to this file.
          The owner may have changed permissions."
          [Request Access] [Go to My Files]
```

**Empty State Design Patterns**:
```text
FIRST-TIME EMPTY:
┌─────────────────────────────────────────┐
│                                         │
│         📄                              │
│                                         │
│    No projects yet                      │
│                                         │
│    Create your first project to         │
│    start collaborating with your team   │
│                                         │
│        [Create Project]                 │
│                                         │
└─────────────────────────────────────────┘

NO SEARCH RESULTS:
┌─────────────────────────────────────────┐
│                                         │
│         🔍                              │
│                                         │
│    No results for "xyz"                 │
│                                         │
│    Try different keywords or            │
│    [Clear filters]                      │
│                                         │
│    Suggestions: "project", "design"     │
│                                         │
└─────────────────────────────────────────┘
```

### Prevention Checklist
- [ ] All screens have empty state designs
- [ ] Loading states defined (skeleton preferred)
- [ ] Error messages are specific and actionable
- [ ] Error states include recovery actions
- [ ] Edge cases documented in specs

---

## Quick Reference: Anti-Pattern Detection Matrix

| Anti-Pattern | Quick Detection | Immediate Action |
|--------------|-----------------|------------------|
| UX-001: Modal Overload | Count modals per session | Replace with inline/toast |
| UX-002: Hidden Navigation | Core features need menu open | Make primary nav visible |
| UX-003: Form Abandonment | High form dropout rate | Reduce fields, add validation |
| UX-004: Invisible Status | Users clicking repeatedly | Add feedback for every action |
| UX-005: Cognitive Overload | Too many options visible | Progressive disclosure |
| UX-006: No Confirmation | "Oops" moments | Add undo or confirm |
| UX-007: Mobile Neglect | Pinch-zoom required | Responsive redesign |
| UX-008: Accessibility Gap | Keyboard doesn't work | Audit and fix basics |
| UX-009: Inconsistent Patterns | Same action, different look | Design system enforcement |
| UX-010: Error Neglect | "Something went wrong" | Design all states |

## Usability Testing Prompts

Use these during testing to surface anti-patterns:

1. "What happens when you click this button?" → Reveals status visibility
2. "How would you undo that?" → Reveals control & freedom
3. "Can you show me where settings are?" → Reveals navigation clarity
4. "What would you do if this failed?" → Reveals error handling
5. "Can you complete this form using only keyboard?" → Reveals accessibility

## Resources

- **Books**: "Don't Make Me Think" (Krug), "The Design of Everyday Things" (Norman)
- **Standards**: WCAG 2.1, Nielsen Heuristics
- **Tools**: UsabilityHub, Maze, UserTesting
