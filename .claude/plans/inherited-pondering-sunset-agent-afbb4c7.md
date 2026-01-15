# Implementation Plan: UX Quality & Brand Questions for `/speckit.design`

**Date**: 2026-01-11  
**Objective**: Expand `/speckit.design` with 8-10 new questions focused on UX quality and brand/audience, using conditional logic and following constitution/concept patterns.

---

## 1. Overview

This plan adds **10 new questions** to `/speckit.design` (split into 2 new batches) focused on:
- **UX Quality**: Usability targets, user flow complexity, accessibility beyond WCAG, user empowerment
- **Brand & Audience**: Brand personality, tone of voice, target audience sophistication, emotional design goals

The questions follow the successful pattern from `/speckit.constitution` (Q6-Q9.5) and `/speckit.concept` (Q6-Q10) with:
- Interactive `AskUserQuestion` tool with headers + multiSelect options
- Conditional logic based on app type (from constitution.md Q1) and previous answers
- Storage in constitution.md `design_system` section
- Integration with design token generation and DQS scoring

---

## 2. New Questions Design (Batch 5 & 6)

### **Batch 5: UX Quality (Questions 13-17)**

Questions 13-17 are asked **AFTER Batch 4 (Framework/Aesthetic)** and focus on usability, flows, and accessibility.

#### Q13: Usability Target Level

**Question**: "What is your target usability quality level?"

**Header**: "Usability"

**Options**:
- "Best-in-class (Top 10% of industry, SUS ≥85)" — Premium products, competitive advantage
- "Competitive (Industry average, SUS 70-84)" — Good enough for most users (Recommended)
- "Acceptable (Functional, SUS 60-69)" — MVP/prototype level
- "Low priority (No usability testing planned)" — Internal tools, throwaway code

**Conditional Logic**: 
- Always ask (all app types)
- If constitution.md `target_scale: enterprise` → Default to "Best-in-class"
- If constitution.md `target_scale: prototype` → Default to "Low priority"

**Storage**: 
```yaml
design_system:
  ux_quality:
    usability_target: "competitive"  # best | competitive | acceptable | low
    sus_threshold: 70                # System Usability Scale target
```

**Impact on Design**:
- **Best-in-class**: Design specs include SUS testing plan, A/B testing for critical flows, user testing checkpoints
- **Competitive**: Basic usability heuristic evaluation in design.md
- **Acceptable/Low**: Minimal usability notes

**DQS Integration**: Add "Usability Testing" dimension (0-20 points):
- Best-in-class with SUS plan: 20 points
- Competitive with heuristics: 15 points
- Acceptable: 10 points
- Low priority: 5 points

---

#### Q14: User Flow Complexity

**Question**: "How complex are the typical user flows in this application?"

**Header**: "Flow Complexity"

**Options**:
- "Simple (1-3 steps, single screen)" — Landing pages, calculators, simple forms
- "Moderate (4-7 steps, 2-3 screens)" — Checkout flows, onboarding, multi-step forms (Recommended)
- "Complex (8-15 steps, 4+ screens)" — Enterprise workflows, approval processes, wizards
- "Very Complex (15+ steps, branching logic)" — Healthcare intake, financial applications, configuration wizards

**Conditional Logic**:
- Always ask (all app types)
- If constitution.md app type = "API/Backend" → Skip (no UI flows)
- If constitution.md domain = "E-commerce" → Default to "Moderate" (checkout flows)
- If constitution.md domain = "Healthcare" or "Fintech" → Default to "Complex" (compliance-heavy)

**Storage**:
```yaml
design_system:
  ux_quality:
    flow_complexity: "moderate"      # simple | moderate | complex | very_complex
    avg_steps_per_flow: 5            # Estimated average steps
```

**Impact on Design**:
- **Simple**: Minimal flow diagrams, inline validation
- **Moderate**: Step indicators, progress bars, clear exit points
- **Complex**: Comprehensive flow diagrams, step navigation, save/resume functionality, breadcrumbs
- **Very Complex**: Branching flow visualizations, contextual help, wizards, undo/redo patterns

**DQS Integration**: Add "Flow Documentation" dimension (0-15 points):
- Very Complex with full flow diagrams: 15 points
- Complex with flow diagrams: 12 points
- Moderate with flow notes: 10 points
- Simple with inline notes: 8 points

---

#### Q15: Accessibility Empowerment Level

**Question**: "Beyond WCAG compliance, what level of accessibility empowerment do you target?"

**Header**: "A11y Empowerment"

**Options**:
- "Inclusive Excellence (Accessibility as innovation driver)" — A11y first, power user features for assistive tech
- "Proactive (User testing with diverse abilities)" — Regular testing with screen readers, keyboard users
- "Compliance+ (WCAG + usability best practices)" — Standard compliance plus user-friendly extras (Recommended)
- "Compliance Only (WCAG 2.1 AA minimum)" — Legal minimum, no extra effort

**Conditional Logic**:
- Only ask if constitution.md app type = "Web" OR "Mobile" OR "Desktop"
- If constitution.md `accessibility_level: wcag22-aaa` → Default to "Inclusive Excellence"
- If constitution.md `accessibility_level: wcag21-a` → Default to "Compliance Only"

**Storage**:
```yaml
design_system:
  ux_quality:
    a11y_empowerment: "compliance_plus"  # inclusive | proactive | compliance_plus | compliance_only
    screen_reader_optimized: true        # Extra optimizations beyond WCAG
    keyboard_shortcuts: true             # Custom keyboard shortcuts
```

**Impact on Design**:
- **Inclusive Excellence**: 
  - Design specs include screen reader UX annotations (not just ARIA labels)
  - Keyboard shortcut system design
  - High contrast mode beyond auto-inversion
  - Haptic/audio feedback design for mobile
- **Proactive**: 
  - Screen reader testing plan in design.md
  - Keyboard navigation flows documented
- **Compliance+**: 
  - Standard ARIA annotations
  - Focus management notes
- **Compliance Only**: 
  - Minimal a11y notes (color contrast only)

**DQS Integration**: Enhance existing "Accessibility Compliance" dimension (0-20 points):
- Inclusive Excellence: 20 points (replaces current 15 for WCAG AA)
- Proactive: 18 points
- Compliance+: 15 points
- Compliance Only: 12 points

---

#### Q16: Error Prevention Strategy

**Question**: "What is your strategy for preventing user errors?"

**Header**: "Error Prevention"

**Options**:
- "Proactive (Prevent errors before they happen)" — Constraints, smart defaults, inline validation, confirmation dialogs
- "Reactive (Clear error messages and recovery)" — Good error messages, easy undo, helpful recovery paths (Recommended)
- "Minimal (Basic validation only)" — Server-side validation, generic error messages
- "None (Users figure it out)" — No error handling design

**Conditional Logic**:
- Only ask if Q14 answer = "Moderate", "Complex", or "Very Complex" (simple flows don't need sophisticated error prevention)
- If constitution.md domain = "Fintech" or "Healthcare" → Default to "Proactive" (high-stakes errors)
- If constitution.md domain = "Gaming" → Skip (game UI has different error paradigms)

**Storage**:
```yaml
design_system:
  ux_quality:
    error_prevention: "reactive"         # proactive | reactive | minimal | none
    inline_validation: true              # Real-time validation
    confirmation_dialogs: false          # For destructive actions
    undo_redo: false                     # Undo/redo support
```

**Impact on Design**:
- **Proactive**: 
  - Design specs include constraint rules (e.g., disabled buttons until valid)
  - Smart default recommendations
  - Confirmation dialog patterns for destructive actions
  - Inline validation specifications
- **Reactive**: 
  - Error message content guidelines
  - Error state component designs
  - Recovery flow diagrams
- **Minimal**: 
  - Basic error state notes
- **None**: 
  - No error handling in design specs

**DQS Integration**: Add "Error Handling" dimension (0-10 points):
- Proactive with full specs: 10 points
- Reactive with recovery flows: 8 points
- Minimal: 5 points
- None: 2 points

---

#### Q17: Responsive Design Breakpoints

**Question**: "What responsive design strategy should be implemented?"

**Header**: "Responsive Strategy"

**Options**:
- "Mobile-First (Design for small screens, scale up)" — Mobile app feel on all devices
- "Desktop-First (Design for large screens, adapt down)" — Data-heavy apps, dashboards (Recommended for SaaS)
- "Platform-Optimized (Different layouts per device)" — iOS/Android native patterns, desktop web
- "Single Breakpoint (Desktop + Mobile views only)" — Simplest approach, no tablet optimization
- "Fluid (No breakpoints, fully responsive)" — CSS Grid/Flexbox responsive

**Conditional Logic**:
- Only ask if constitution.md app type = "Web Application"
- If constitution.md app type = "Mobile Application" → Skip (native responsive)
- If constitution.md domain = "SaaS" → Default to "Desktop-First"
- If constitution.md domain = "E-commerce" or "Marketing" → Default to "Mobile-First"

**Storage**:
```yaml
design_system:
  ux_quality:
    responsive_strategy: "desktop_first"  # mobile_first | desktop_first | platform_optimized | single_breakpoint | fluid
    breakpoints:
      mobile: "320px"
      tablet: "768px"
      desktop: "1024px"
      wide: "1440px"
```

**Impact on Design**:
- **Mobile-First**: 
  - Wireframes start at 375px mobile width
  - Progressive enhancement notes
  - Touch-first interaction patterns
- **Desktop-First**: 
  - Wireframes start at 1440px desktop width
  - Graceful degradation notes
  - Mouse/keyboard-first patterns
- **Platform-Optimized**: 
  - Separate wireframe sets per platform
  - Platform-specific component variants
- **Single Breakpoint**: 
  - Two wireframe sets (mobile 375px, desktop 1440px)
- **Fluid**: 
  - Container query annotations
  - Flexible grid specifications

**DQS Integration**: Add "Responsive Design" dimension (0-15 points):
- Platform-Optimized with all breakpoints: 15 points
- Mobile/Desktop-First with 3+ breakpoints: 12 points
- Fluid with container queries: 12 points
- Single Breakpoint: 8 points

---

### **Batch 6: Brand & Audience (Questions 18-22)**

Questions 18-22 are asked **AFTER Batch 5 (UX Quality)** and focus on brand personality, tone, audience, and emotional design.

#### Q18: Brand Personality Archetype

**Question**: "What brand personality archetype best represents your product?"

**Header**: "Brand Archetype"

**Options**:
- "The Innovator (Bold, forward-thinking, disruptive)" — Startups, tech products, cutting-edge tools
- "The Trusted Advisor (Professional, reliable, expert)" — Enterprise SaaS, financial tools, healthcare (Recommended)
- "The Friend (Approachable, warm, helpful)" — Consumer apps, social platforms, collaboration tools
- "The Performer (Exciting, energetic, entertaining)" — Gaming, media, lifestyle apps
- "The Minimalist (Clean, simple, refined)" — Productivity tools, design apps, premium products

**Conditional Logic**:
- Always ask (all app types)
- If constitution.md domain = "Fintech" or "Healthcare" → Default to "Trusted Advisor"
- If constitution.md domain = "Gaming" → Default to "Performer"
- If aesthetic_preset = "Linear" or "Vercel" → Default to "Minimalist"
- If aesthetic_preset = "Stripe" or "Apple" → Default to "Trusted Advisor"
- If aesthetic_preset = "Slack" or "Figma" → Default to "Friend"

**Storage**:
```yaml
design_system:
  brand_audience:
    archetype: "trusted_advisor"         # innovator | trusted_advisor | friend | performer | minimalist
    personality_keywords: ["professional", "reliable", "expert"]
```

**Impact on Design**:
- **Innovator**: 
  - Bold color choices, unconventional layouts
  - Animation-heavy, experimental patterns
  - Cutting-edge component designs
- **Trusted Advisor**: 
  - Conservative color palette, traditional layouts
  - Subtle animations, proven patterns
  - Data visualization focus
- **Friend**: 
  - Warm colors, rounded corners, friendly illustrations
  - Micro-interactions, delightful details
  - Conversational UI patterns
- **Performer**: 
  - Vibrant colors, bold typography, dramatic shadows
  - Rich animations, immersive experiences
  - Entertainment-first design
- **Minimalist**: 
  - Monochromatic palette, lots of white space
  - Minimal animations, clean lines
  - Content-first design

**DQS Integration**: Add "Brand Consistency" dimension (0-15 points):
- Archetype clearly reflected in visual specs: 15 points
- Archetype mentioned but not fully expressed: 10 points
- No archetype alignment: 5 points

---

#### Q19: Tone of Voice

**Question**: "What tone of voice should the UI copy and microcopy use?"

**Header**: "Tone of Voice"

**Options**:
- "Formal (Professional, third-person, no contractions)" — Legal, healthcare, enterprise
- "Professional (Clear, direct, some personality)" — SaaS, B2B tools (Recommended)
- "Conversational (Friendly, second-person, contractions)" — Consumer apps, social platforms
- "Playful (Witty, humorous, personality-driven)" — Gaming, lifestyle, creative tools
- "Technical (Precise, jargon-heavy, expert-focused)" — Developer tools, APIs, technical products

**Conditional Logic**:
- Always ask (all app types)
- If constitution.md domain = "Healthcare" or "Fintech" → Default to "Formal"
- If constitution.md domain = "Gaming" → Default to "Playful"
- If constitution.md app type = "API/Backend Service" → Default to "Technical"
- Must align with Q18 archetype:
  - "Trusted Advisor" → "Formal" or "Professional"
  - "Friend" → "Conversational" or "Playful"
  - "Minimalist" → "Professional" or "Technical"

**Storage**:
```yaml
design_system:
  brand_audience:
    tone_of_voice: "professional"        # formal | professional | conversational | playful | technical
    use_contractions: true               # "Don't" vs "Do not"
    person: "second"                     # first | second | third
    humor_level: "subtle"                # none | subtle | moderate | high
```

**Impact on Design**:
- **Formal**: 
  - Microcopy examples in third-person
  - No emoji, no contractions
  - Long-form error messages
- **Professional**: 
  - Microcopy examples in second-person
  - Occasional contractions, clear language
  - Balanced error messages
- **Conversational**: 
  - Friendly microcopy examples
  - Frequent contractions, casual language
  - Helpful, empathetic error messages
- **Playful**: 
  - Witty microcopy examples
  - Emoji, slang, personality
  - Creative error messages (e.g., "Oops!" instead of "Error")
- **Technical**: 
  - Precise terminology, no fluff
  - Technical error codes
  - Developer-focused language

**DQS Integration**: Enhance "Brand Consistency" dimension (add 5 points if tone guidelines documented):
- Tone guidelines with examples: +5 points
- No tone guidelines: +0 points

---

#### Q20: Target Audience Sophistication

**Question**: "What is the technical sophistication level of your target users?"

**Header**: "User Sophistication"

**Options**:
- "Expert (Power users, professionals, developers)" — Complex workflows, keyboard shortcuts, dense information
- "Intermediate (Familiar with similar tools)" — Standard patterns, moderate learning curve (Recommended)
- "Beginner (First-time users, needs guidance)" — Onboarding, tooltips, progressive disclosure
- "Non-technical (Seniors, low digital literacy)" — Extra-simple, forgiving, generous feedback

**Conditional Logic**:
- Always ask (all app types)
- If constitution.md app type = "CLI Tool" or "API" → Default to "Expert"
- If constitution.md domain = "Healthcare" → Default to "Intermediate" (clinical staff, not general public)
- If constitution.md domain = "Gaming" → Skip (gaming has different sophistication metrics)

**Storage**:
```yaml
design_system:
  brand_audience:
    user_sophistication: "intermediate"  # expert | intermediate | beginner | non_technical
    onboarding_required: true            # Onboarding flow needed
    tooltips_frequency: "moderate"       # none | minimal | moderate | generous
    keyboard_shortcuts: false            # Power user shortcuts
```

**Impact on Design**:
- **Expert**: 
  - Dense information architecture
  - Keyboard shortcut system
  - Minimal onboarding, assumes familiarity
  - Advanced customization options
- **Intermediate**: 
  - Balanced information density
  - Some tooltips on complex features
  - Quick onboarding for new concepts
  - Standard patterns
- **Beginner**: 
  - Progressive disclosure patterns
  - Comprehensive onboarding flow
  - Generous tooltips and help
  - Forgiving error recovery
- **Non-technical**: 
  - Extreme simplicity, large touch targets
  - Step-by-step wizards
  - Contextual help on every screen
  - Extra error prevention

**DQS Integration**: Add "User Empowerment" dimension (0-10 points):
- Sophistication level aligned with onboarding/tooltips design: 10 points
- Mismatch (e.g., expert users but beginner UI): 5 points
- No consideration: 2 points

---

#### Q21: Emotional Design Goal

**Question**: "What primary emotion should users feel when using this product?"

**Header**: "Emotional Goal"

**Options**:
- "Confidence (Trust, security, reliability)" — Financial tools, healthcare, enterprise (Recommended)
- "Delight (Joy, surprise, playfulness)" — Consumer apps, lifestyle, creative tools
- "Empowerment (Control, mastery, productivity)" — Productivity tools, developer platforms
- "Calm (Peace, simplicity, focus)" — Meditation apps, minimalist tools, content platforms
- "Excitement (Energy, anticipation, thrill)" — Gaming, social media, entertainment

**Conditional Logic**:
- Always ask (all app types except API)
- If constitution.md domain = "Fintech" or "Healthcare" → Default to "Confidence"
- If constitution.md domain = "Gaming" → Default to "Excitement"
- Must align with Q18 archetype:
  - "Trusted Advisor" → "Confidence"
  - "Friend" → "Delight"
  - "Performer" → "Excitement"
  - "Minimalist" → "Calm"
  - "Innovator" → "Empowerment"

**Storage**:
```yaml
design_system:
  brand_audience:
    emotional_goal: "confidence"         # confidence | delight | empowerment | calm | excitement
    micro_interactions: "subtle"         # none | subtle | moderate | rich
    illustration_style: "professional"   # none | professional | friendly | playful
```

**Impact on Design**:
- **Confidence**: 
  - Stable, predictable animations
  - Professional color palette
  - Clear status indicators and feedback
  - Security-focused microcopy
- **Delight**: 
  - Playful micro-interactions
  - Friendly illustrations
  - Surprise-and-delight moments
  - Positive reinforcement patterns
- **Empowerment**: 
  - Power user shortcuts
  - Customization options
  - Progress indicators
  - Achievement patterns
- **Calm**: 
  - Minimal animations
  - Soft color palette
  - Generous white space
  - Distraction-free layouts
- **Excitement**: 
  - Rich animations
  - Bold colors
  - Dynamic layouts
  - Gamification elements

**DQS Integration**: Add "Emotional Design" dimension (0-10 points):
- Emotional goal clearly reflected in visual specs: 10 points
- Emotional goal mentioned but not expressed: 6 points
- No emotional design consideration: 2 points

---

#### Q22: Audience Demographics Priority

**Question**: "Which audience demographic considerations are most critical for your design?"

**Header**: "Demographics"

**Options** (Multi-select allowed):
- "Age Range (Seniors, youth, children)" — Age-appropriate patterns, readability
- "Global Audience (Internationalization, RTL, cultural)" — i18n, localization, cultural sensitivity
- "Neurodiversity (ADHD, autism, dyslexia)" — Reduced motion, clear structure, readability
- "Low Bandwidth (Slow connections, data constraints)" — Performance, image optimization, offline
- "None (Homogeneous audience)" — No special demographic considerations (Recommended)

**Conditional Logic**:
- Always ask (all app types)
- If constitution.md `language: ru` or `zh` or `ar` → Auto-select "Global Audience"
- If constitution.md `accessibility_level: wcag22-aa` or higher → Auto-suggest "Neurodiversity"
- Multiple selections allowed

**Storage**:
```yaml
design_system:
  brand_audience:
    demographics_priority: ["global_audience", "neurodiversity"]  # Array of priorities
    i18n_support: true               # Internationalization
    rtl_support: false               # Right-to-left languages
    reduced_motion_default: false    # Respect prefers-reduced-motion
    performance_budget: "moderate"   # strict | moderate | relaxed
```

**Impact on Design**:
- **Age Range**: 
  - Font size recommendations based on age
  - Color contrast adjustments
  - Touch target sizing notes
- **Global Audience**: 
  - i18n annotations in wireframes
  - Text expansion notes (German +30%)
  - Cultural color considerations
  - RTL layout variants
- **Neurodiversity**: 
  - Reduced motion variants
  - Clear visual hierarchy
  - Dyslexia-friendly typography notes
  - Predictable navigation patterns
- **Low Bandwidth**: 
  - Performance budget in design specs
  - Lazy loading patterns
  - Offline-first considerations
  - Image optimization guidelines
- **None**: 
  - Standard design considerations

**DQS Integration**: Add "Inclusive Design" dimension (0-10 points):
- 2+ demographic priorities with design accommodations: 10 points
- 1 demographic priority with design accommodations: 7 points
- None selected: 5 points

---

## 3. Question Insertion Strategy

### Where to Add Questions

**Option A: Extend `templates/shared/design-questionnaire.md` (RECOMMENDED)**

Add Batch 5 and Batch 6 to the existing questionnaire file:

```markdown
## Batch 5: UX Quality (Questions 13-17)
...

## Batch 6: Brand & Audience (Questions 18-22)
...
```

**Rationale**: 
- Keeps all design questions in one place
- Easier to maintain
- Follows existing pattern

**Alternative**: Create separate `templates/shared/design-ux-brand-questionnaire.md` and include it via `{{include:}}` in design.md

---

### When Questions Are Asked

Questions are asked in `design_system_generation` mode (the primary mode when `--design-system` flag is passed or no spec.md exists).

**Execution Order**:
1. Batch 1 (Visual Foundation) — Q1-Q4
2. Batch 2 (Typography & Motion) — Q5-Q8
3. Batch 3 (Icons & Motion) — Q9-Q10
4. Batch 4 (Design Presets) — Q11-Q12
5. **NEW: Batch 5 (UX Quality)** — Q13-Q17
6. **NEW: Batch 6 (Brand & Audience)** — Q18-Q22

**Skip Logic**:
- If `--quick` or `--defaults` flag → Skip all batches, use defaults
- If `--skip-ux-questions` flag (new) → Skip Batch 5 only
- If `--skip-brand-questions` flag (new) → Skip Batch 6 only

---

### Conditional Logic Implementation

Conditional questions are skipped based on:

1. **Constitution.md values** (read from `/memory/constitution.md`):
   - `app_type` (from constitution Q1)
   - `domain` (from constitution Q2)
   - `target_scale` (from constitution Q6)
   - `accessibility_level` (from constitution Q9)
   - `language` (from Project Settings)

2. **Previous design questionnaire answers**:
   - `aesthetic_preset` (from Q12)
   - `flow_complexity` (from Q14) — affects Q16

**Implementation Pattern** (same as constitution):

```text
IF constitution.md.app_type == "API/Backend Service":
  SKIP Q14 (user flows not applicable)

IF Q14.answer IN ["Simple"]:
  SKIP Q16 (error prevention not critical for simple flows)

IF aesthetic_preset == "Stripe":
  DEFAULT Q18 to "Trusted Advisor"
```

---

## 4. Storage & Integration

### Storage Location

Store all new answers in **constitution.md** under the existing `design_system` section:

```yaml
design_system:
  # Existing fields (Q11-Q12)
  framework: "shadcn/ui"
  aesthetic: "linear"
  enforcement_level: "warn"
  
  # NEW: UX Quality section (Q13-Q17)
  ux_quality:
    usability_target: "competitive"          # Q13
    sus_threshold: 70
    flow_complexity: "moderate"              # Q14
    avg_steps_per_flow: 5
    a11y_empowerment: "compliance_plus"      # Q15
    screen_reader_optimized: true
    keyboard_shortcuts: false
    error_prevention: "reactive"             # Q16
    inline_validation: true
    confirmation_dialogs: false
    undo_redo: false
    responsive_strategy: "desktop_first"     # Q17
    breakpoints:
      mobile: "320px"
      tablet: "768px"
      desktop: "1024px"
      wide: "1440px"
  
  # NEW: Brand & Audience section (Q18-Q22)
  brand_audience:
    archetype: "trusted_advisor"             # Q18
    personality_keywords: ["professional", "reliable", "expert"]
    tone_of_voice: "professional"            # Q19
    use_contractions: true
    person: "second"
    humor_level: "subtle"
    user_sophistication: "intermediate"      # Q20
    onboarding_required: true
    tooltips_frequency: "moderate"
    keyboard_shortcuts: false
    emotional_goal: "confidence"             # Q21
    micro_interactions: "subtle"
    illustration_style: "professional"
    demographics_priority: ["global_audience"]  # Q22 (multi-select)
    i18n_support: true
    rtl_support: false
    reduced_motion_default: false
    performance_budget: "moderate"
  
  # Existing theme tokens
  theme:
    colors: ...
    typography: ...
```

**Rationale**:
- Constitution is the single source of truth for project-wide settings
- Cross-command integration: `/speckit.specify` can read UX/brand values to influence functional requirements
- Enables constitution-based validation via `/speckit.analyze`

---

### Integration with Design Generation

New answers influence design outputs in **5 waves of agent orchestration**:

#### Wave 1: Research & Analysis

**design-researcher** agent:
- Read `constitution.md → design_system.brand_audience.archetype` → Tailor competitor research to archetype
- Read `constitution.md → design_system.ux_quality.usability_target` → Include usability benchmarking if "best-in-class"

**pattern-analyst** agent:
- Read `constitution.md → design_system.ux_quality.responsive_strategy` → Identify existing responsive patterns matching strategy

#### Wave 2: Design Generation

**ux-designer** agent:
- Read `constitution.md → design_system.ux_quality.flow_complexity` → Adjust wireframe detail level:
  - "Simple" → Inline flows only
  - "Moderate" → Step-by-step flow diagrams
  - "Complex" → Comprehensive flow diagrams with branching
  - "Very Complex" → State machine diagrams + wizard patterns
- Read `constitution.md → design_system.ux_quality.a11y_empowerment` → Add accessibility annotations:
  - "Inclusive Excellence" → Screen reader UX notes, keyboard shortcut designs
  - "Proactive" → Screen reader testing plan
  - "Compliance+" → Standard ARIA annotations
  - "Compliance Only" → Color contrast only
- Read `constitution.md → design_system.ux_quality.error_prevention` → Add error handling patterns:
  - "Proactive" → Constraint rules, confirmation dialogs
  - "Reactive" → Error message guidelines, recovery flows
- Read `constitution.md → design_system.ux_quality.responsive_strategy` → Generate breakpoint-specific wireframes

**product-designer** agent:
- Read `constitution.md → design_system.brand_audience.archetype` → Adjust visual language:
  - "Innovator" → Bold colors, unconventional layouts
  - "Trusted Advisor" → Conservative palette, traditional layouts
  - "Friend" → Warm colors, rounded corners
  - "Performer" → Vibrant colors, dramatic shadows
  - "Minimalist" → Monochromatic, lots of white space
- Read `constitution.md → design_system.brand_audience.tone_of_voice` → Generate microcopy examples:
  - "Formal" → Third-person, no contractions
  - "Professional" → Second-person, clear
  - "Conversational" → Friendly, contractions
  - "Playful" → Witty, emoji
  - "Technical" → Precise, jargon
- Read `constitution.md → design_system.brand_audience.emotional_goal` → Adjust animation complexity:
  - "Confidence" → Stable, predictable
  - "Delight" → Playful, surprise-and-delight
  - "Calm" → Minimal, soft
  - "Excitement" → Rich, dynamic
- Read `constitution.md → design_system.brand_audience.user_sophistication` → Adjust information density:
  - "Expert" → Dense layouts, keyboard shortcuts
  - "Intermediate" → Balanced, some tooltips
  - "Beginner" → Progressive disclosure, onboarding
  - "Non-technical" → Extra-simple, generous feedback

**motion-designer** agent:
- Read `constitution.md → design_system.brand_audience.emotional_goal` → Adjust animation style to match emotion
- Read `constitution.md → design_system.brand_audience.demographics_priority` → If "Neurodiversity" selected, add reduced-motion variants

#### Wave 3: System Generation

**system-architect** agent:
- Read `constitution.md → design_system.ux_quality.usability_target` → Generate usability testing plan if "best-in-class"
- Read `constitution.md → design_system.ux_quality.flow_complexity` → Generate appropriate navigation patterns
- Read `constitution.md → design_system.brand_audience.demographics_priority` → Generate i18n/RTL/performance guidelines

#### Wave 4: Integration

**integration-engineer** agent:
- Read `constitution.md → design_system.ux_quality.responsive_strategy` → Generate appropriate CSS framework recommendations
- Read `constitution.md → design_system.brand_audience.demographics_priority` → If "Low Bandwidth", add performance budget

#### Wave 5: Validation

**design-validator** agent:
- Compute enhanced DQS with new dimensions (see Section 5)

---

### Cross-Command Integration

#### `/speckit.specify` Integration

When generating `spec.md`, read constitution to influence functional requirements:

```text
IF constitution.md.design_system.ux_quality.usability_target == "best-in-class":
  ADD NFR: "System SHALL achieve SUS score ≥85 in usability testing"

IF constitution.md.design_system.ux_quality.a11y_empowerment == "inclusive":
  ADD NFR: "System SHALL support custom keyboard shortcuts for power users"
  ADD NFR: "System SHALL provide screen reader optimizations beyond WCAG AA"

IF constitution.md.design_system.brand_audience.demographics_priority CONTAINS "global_audience":
  ADD NFR: "System SHALL support i18n with text expansion up to 30%"
  ADD NFR: "System SHALL support RTL languages (Arabic, Hebrew)"

IF constitution.md.design_system.brand_audience.demographics_priority CONTAINS "low_bandwidth":
  ADD NFR: "System SHALL implement lazy loading for images and defer non-critical JS"
  ADD NFR: "System SHALL achieve First Contentful Paint < 1.5s on 3G"
```

#### `/speckit.plan` Integration

When generating `plan.md`, read constitution to add design foundation phase tasks:

```text
IF constitution.md.design_system.brand_audience.emotional_goal == "delight":
  ADD Phase 2c: Micro-interactions Design
    - Design surprise-and-delight moments
    - Implement playful animations
    - Add positive reinforcement patterns

IF constitution.md.design_system.ux_quality.flow_complexity IN ["complex", "very_complex"]:
  ADD Phase 2b: User Flow Engineering
    - Implement wizard pattern
    - Add save/resume functionality
    - Build step navigation system
```

#### `/speckit.analyze` Integration

When validating design.md, check alignment with constitution:

```text
CHECK: design.md flow diagrams exist IF constitution.md.ux_quality.flow_complexity IN ["complex", "very_complex"]
  SEVERITY: HIGH if missing

CHECK: design.md microcopy matches constitution.md.brand_audience.tone_of_voice
  SEVERITY: MEDIUM if mismatch

CHECK: design.md emotional_goal matches constitution.md.brand_audience.emotional_goal
  SEVERITY: MEDIUM if mismatch
```

---

## 5. DQS (Design Quality Score) Integration

### Current DQS Dimensions (0-100 total)

Existing dimensions (from design.md validation):
1. **Visual Specifications** (0-25 points) — Color tokens, typography scale, spacing scale
2. **Component Documentation** (0-25 points) — Component specs, variants, states
3. **Accessibility Compliance** (0-20 points) — WCAG 2.1 AA color contrast, ARIA annotations
4. **Interaction Design** (0-15 points) — User flows, wireframes, states
5. **Design System Maturity** (0-15 points) — Token usage, pattern consistency

---

### Enhanced DQS Dimensions (0-120 total)

Add 6 new dimensions based on new questions:

#### **6. Usability Testing** (0-20 points) — NEW from Q13

Scoring:
- **20 points**: Best-in-class target + SUS testing plan in design.md + User testing checkpoints
- **15 points**: Competitive target + Usability heuristic evaluation
- **10 points**: Acceptable target + Basic usability notes
- **5 points**: Low priority / No usability considerations

Validation:
```text
IF constitution.md.ux_quality.usability_target == "best":
  EXPECT: design.md contains "SUS testing" OR "System Usability Scale"
  EXPECT: design.md contains user testing checkpoints
  POINTS: 20

IF constitution.md.ux_quality.usability_target == "competitive":
  EXPECT: design.md contains heuristic evaluation notes
  POINTS: 15
```

---

#### **7. Flow Documentation** (0-15 points) — NEW from Q14

Scoring:
- **15 points**: Very Complex flows + Full state machine diagrams + Wizard patterns
- **12 points**: Complex flows + Comprehensive flow diagrams with branching
- **10 points**: Moderate flows + Step-by-step flow diagrams
- **8 points**: Simple flows + Inline flow notes
- **0 points**: No flow documentation

Validation:
```text
IF constitution.md.ux_quality.flow_complexity == "very_complex":
  EXPECT: design.md contains state machine diagrams OR wizard patterns
  EXPECT: design.md contains branching logic diagrams
  POINTS: 15

IF constitution.md.ux_quality.flow_complexity == "complex":
  EXPECT: design.md contains flow diagrams with ≥4 steps
  POINTS: 12
```

---

#### **8. A11y Empowerment** (0-10 points) — NEW from Q15, enhances existing dimension

Scoring (replaces part of existing "Accessibility Compliance" dimension):
- **10 points**: Inclusive Excellence + Screen reader UX annotations + Keyboard shortcuts + High contrast mode
- **8 points**: Proactive + Screen reader testing plan + Keyboard navigation flows
- **6 points**: Compliance+ + Standard ARIA annotations + Focus management
- **4 points**: Compliance Only + Color contrast only

Validation:
```text
IF constitution.md.ux_quality.a11y_empowerment == "inclusive":
  EXPECT: design.md contains "screen reader UX" notes (not just ARIA)
  EXPECT: design.md contains keyboard shortcut system
  EXPECT: design.md contains high contrast mode design
  POINTS: 10

IF constitution.md.ux_quality.a11y_empowerment == "proactive":
  EXPECT: design.md contains screen reader testing plan
  EXPECT: design.md contains keyboard navigation flows
  POINTS: 8
```

---

#### **9. Error Handling** (0-10 points) — NEW from Q16

Scoring:
- **10 points**: Proactive prevention + Constraint rules + Confirmation dialogs + Inline validation specs
- **8 points**: Reactive recovery + Error message guidelines + Recovery flow diagrams
- **5 points**: Minimal validation + Basic error state notes
- **2 points**: No error handling design

Validation:
```text
IF constitution.md.ux_quality.error_prevention == "proactive":
  EXPECT: design.md contains constraint rules
  EXPECT: design.md contains confirmation dialog patterns
  EXPECT: design.md contains inline validation specifications
  POINTS: 10

IF constitution.md.ux_quality.error_prevention == "reactive":
  EXPECT: design.md contains error message content guidelines
  EXPECT: design.md contains error state designs
  EXPECT: design.md contains recovery flow diagrams
  POINTS: 8
```

---

#### **10. Responsive Design** (0-15 points) — NEW from Q17

Scoring:
- **15 points**: Platform-Optimized + Separate wireframes per platform + Platform-specific variants
- **12 points**: Mobile/Desktop-First + 3+ breakpoints + Responsive wireframes
- **12 points**: Fluid + Container queries + Flexible grid specs
- **8 points**: Single Breakpoint + 2 wireframe sets
- **0 points**: No responsive design

Validation:
```text
IF constitution.md.ux_quality.responsive_strategy == "platform_optimized":
  EXPECT: design.md contains separate wireframe sets for mobile/tablet/desktop
  EXPECT: design.md contains platform-specific component variants
  POINTS: 15

IF constitution.md.ux_quality.responsive_strategy IN ["mobile_first", "desktop_first"]:
  EXPECT: design.md defines ≥3 breakpoints
  EXPECT: design.md contains responsive wireframes
  POINTS: 12
```

---

#### **11. Brand Consistency** (0-15 points) — NEW from Q18 + Q19

Scoring:
- **15 points**: Archetype clearly reflected in visual specs + Tone guidelines with examples + Emotional goal expressed
- **10 points**: Archetype mentioned + Tone guidelines + Emotional goal mentioned
- **5 points**: No archetype alignment / Generic design

Validation:
```text
IF constitution.md.brand_audience.archetype == "trusted_advisor":
  EXPECT: design.md contains conservative color palette
  EXPECT: design.md contains traditional layouts
  EXPECT: design.md contains subtle animations
  POINTS: 15 (if all present)

CHECK: design.md microcopy examples match constitution.md.brand_audience.tone_of_voice
  - "formal" → third-person, no contractions
  - "professional" → second-person, clear
  - "conversational" → friendly, contractions
  - "playful" → witty, emoji
  POINTS: +5 if match
```

---

#### **12. Emotional Design** (0-10 points) — NEW from Q21

Scoring:
- **10 points**: Emotional goal clearly reflected in visual specs + Animation style matches + Color/imagery aligned
- **6 points**: Emotional goal mentioned but not fully expressed
- **2 points**: No emotional design consideration

Validation:
```text
IF constitution.md.brand_audience.emotional_goal == "confidence":
  EXPECT: design.md contains stable, predictable animation notes
  EXPECT: design.md contains professional color palette
  EXPECT: design.md contains clear status indicators
  POINTS: 10

IF constitution.md.brand_audience.emotional_goal == "delight":
  EXPECT: design.md contains playful micro-interactions
  EXPECT: design.md contains friendly illustrations
  EXPECT: design.md contains surprise-and-delight moments
  POINTS: 10
```

---

#### **13. User Empowerment** (0-10 points) — NEW from Q20

Scoring:
- **10 points**: User sophistication aligned with onboarding/tooltips/information density
- **5 points**: Mismatch (e.g., expert users but beginner UI)
- **2 points**: No consideration

Validation:
```text
IF constitution.md.brand_audience.user_sophistication == "expert":
  EXPECT: design.md contains dense information architecture
  EXPECT: design.md contains keyboard shortcut system
  EXPECT: design.md does NOT contain excessive onboarding
  POINTS: 10

IF constitution.md.brand_audience.user_sophistication == "beginner":
  EXPECT: design.md contains progressive disclosure patterns
  EXPECT: design.md contains comprehensive onboarding flow
  EXPECT: design.md contains generous tooltips
  POINTS: 10
```

---

#### **14. Inclusive Design** (0-10 points) — NEW from Q22

Scoring:
- **10 points**: 2+ demographic priorities with design accommodations in design.md
- **7 points**: 1 demographic priority with design accommodations
- **5 points**: None selected but standard accessibility
- **0 points**: No demographic considerations

Validation:
```text
IF "global_audience" IN constitution.md.brand_audience.demographics_priority:
  EXPECT: design.md contains i18n annotations
  EXPECT: design.md contains text expansion notes (German +30%)
  EXPECT: design.md contains RTL layout variants (if RTL languages)
  POINTS: +5

IF "neurodiversity" IN constitution.md.brand_audience.demographics_priority:
  EXPECT: design.md contains reduced motion variants
  EXPECT: design.md contains clear visual hierarchy notes
  EXPECT: design.md contains dyslexia-friendly typography
  POINTS: +5

IF "low_bandwidth" IN constitution.md.brand_audience.demographics_priority:
  EXPECT: design.md contains performance budget
  EXPECT: design.md contains lazy loading patterns
  EXPECT: design.md contains offline-first considerations
  POINTS: +5
```

---

### Updated DQS Calculation

```text
DQS = Visual Specs (0-25)
    + Component Docs (0-25)
    + A11y Empowerment (0-10)         # Enhanced from existing Accessibility (0-20)
    + Interaction Design (0-15)
    + Design System Maturity (0-15)
    + Usability Testing (0-20)        # NEW
    + Flow Documentation (0-15)       # NEW
    + Error Handling (0-10)           # NEW
    + Responsive Design (0-15)        # NEW
    + Brand Consistency (0-15)        # NEW
    + Emotional Design (0-10)         # NEW
    + User Empowerment (0-10)         # NEW
    + Inclusive Design (0-10)         # NEW

Total: 0-180 points
```

**Normalization**: Scale to 0-100 for consistency with SQS/CQS:

```text
DQS_normalized = (DQS_raw / 180) * 100
```

**Thresholds**:
- **≥80**: Excellent design (production-ready)
- **70-79**: Good design (minor improvements needed)
- **60-69**: Acceptable design (significant gaps)
- **<60**: Poor design (major rework required)

**Quality Gate**: `QG-DQS-001` threshold remains **≥70** (normalized).

---

## 6. Example Questions with Full Structure

### Example 1: Q13 Usability Target Level

```yaml
question_id: Q13
batch: 5
category: "UX Quality"
order: 13

question:
  text: "What is your target usability quality level?"
  header: "Usability"
  description: "This determines usability testing requirements and SUS (System Usability Scale) targets."

options:
  - value: "best"
    label: "Best-in-class (Top 10% of industry, SUS ≥85)"
    description: "Premium products where usability is a competitive advantage"
    impact:
      - "Design specs include SUS testing plan"
      - "A/B testing for critical flows"
      - "User testing checkpoints in design.md"
    examples: ["Apple.com", "Linear", "Stripe Dashboard"]
  
  - value: "competitive"
    label: "Competitive (Industry average, SUS 70-84)"
    description: "Good enough for most users"
    recommended: true
    impact:
      - "Basic usability heuristic evaluation"
      - "Standard usability notes in design.md"
    examples: ["Most SaaS products", "GitHub", "Notion"]
  
  - value: "acceptable"
    label: "Acceptable (Functional, SUS 60-69)"
    description: "MVP/prototype level, minimal usability focus"
    impact:
      - "Minimal usability notes"
    examples: ["Internal tools", "MVPs"]
  
  - value: "low"
    label: "Low priority (No usability testing planned)"
    description: "Internal tools, throwaway code"
    impact:
      - "No usability testing requirements"
    examples: ["Prototypes", "Personal projects"]

conditional_logic:
  - condition: "constitution.md.target_scale == 'enterprise'"
    action: "default_to: best"
    rationale: "Enterprise scale demands best-in-class usability"
  
  - condition: "constitution.md.target_scale == 'prototype'"
    action: "default_to: low"
    rationale: "Prototypes don't need formal usability testing"

storage:
  location: "constitution.md"
  path: "design_system.ux_quality.usability_target"
  additional_fields:
    - field: "sus_threshold"
      derived_from: "option.value"
      mapping:
        best: 85
        competitive: 70
        acceptable: 60
        low: 0

impact_on_design:
  artifacts: ["design.md", "plan.md"]
  
  design_md_changes:
    best:
      - section: "§ Usability Testing"
        content: "SUS testing plan with target ≥85"
      - section: "§ User Flows"
        content: "A/B testing notes for critical flows"
      - section: "§ Validation"
        content: "User testing checkpoints"
    
    competitive:
      - section: "§ Usability Testing"
        content: "Heuristic evaluation notes"
    
    acceptable:
      - section: "§ Usability Testing"
        content: "Minimal usability notes"
    
    low:
      - section: "§ Usability Testing"
        content: null  # Section omitted
  
  plan_md_changes:
    best:
      - phase: "Phase 2d: Usability Testing"
        tasks:
          - "Set up SUS testing framework"
          - "Conduct baseline usability testing"
          - "Implement A/B testing for critical flows"
    
    competitive:
      - phase: "Phase 2d: Usability Validation"
        tasks:
          - "Perform heuristic evaluation"

dqs_integration:
  dimension: "Usability Testing"
  max_points: 20
  scoring:
    best_with_plan: 20
    competitive_with_heuristics: 15
    acceptable: 10
    low: 5
  
  validation_rules:
    - condition: "usability_target == 'best'"
      expect: "design.md contains 'SUS testing' OR 'System Usability Scale'"
      severity: "HIGH"
    
    - condition: "usability_target == 'best'"
      expect: "design.md contains user testing checkpoints"
      severity: "HIGH"
    
    - condition: "usability_target == 'competitive'"
      expect: "design.md contains heuristic evaluation notes"
      severity: "MEDIUM"
```

---

### Example 2: Q18 Brand Personality Archetype

```yaml
question_id: Q18
batch: 6
category: "Brand & Audience"
order: 18

question:
  text: "What brand personality archetype best represents your product?"
  header: "Brand Archetype"
  description: "This shapes visual language, tone, and overall design philosophy."

options:
  - value: "innovator"
    label: "The Innovator (Bold, forward-thinking, disruptive)"
    description: "Startups, tech products, cutting-edge tools"
    personality_keywords: ["bold", "experimental", "cutting-edge"]
    visual_style:
      colors: "Bold color choices, unconventional palettes"
      layouts: "Unconventional layouts, asymmetric grids"
      animations: "Animation-heavy, experimental"
      components: "Cutting-edge, custom patterns"
    examples: ["Tesla", "Figma", "Linear"]
  
  - value: "trusted_advisor"
    label: "The Trusted Advisor (Professional, reliable, expert)"
    description: "Enterprise SaaS, financial tools, healthcare"
    recommended: true
    personality_keywords: ["professional", "reliable", "expert"]
    visual_style:
      colors: "Conservative palette, traditional blues/grays"
      layouts: "Traditional layouts, symmetric grids"
      animations: "Subtle, proven patterns"
      components: "Data visualization focus"
    examples: ["Stripe", "AWS", "Salesforce"]
  
  - value: "friend"
    label: "The Friend (Approachable, warm, helpful)"
    description: "Consumer apps, social platforms, collaboration tools"
    personality_keywords: ["approachable", "warm", "helpful"]
    visual_style:
      colors: "Warm colors, friendly palette"
      layouts: "Rounded corners, friendly layouts"
      animations: "Micro-interactions, delightful"
      components: "Conversational UI patterns"
    examples: ["Slack", "Notion", "Airbnb"]
  
  - value: "performer"
    label: "The Performer (Exciting, energetic, entertaining)"
    description: "Gaming, media, lifestyle apps"
    personality_keywords: ["exciting", "energetic", "entertaining"]
    visual_style:
      colors: "Vibrant, bold, dramatic"
      layouts: "Dynamic, immersive"
      animations: "Rich, theatrical"
      components: "Entertainment-first"
    examples: ["Spotify", "TikTok", "Fortnite"]
  
  - value: "minimalist"
    label: "The Minimalist (Clean, simple, refined)"
    description: "Productivity tools, design apps, premium products"
    personality_keywords: ["clean", "simple", "refined"]
    visual_style:
      colors: "Monochromatic, lots of white space"
      layouts: "Content-first, generous spacing"
      animations: "Minimal, purposeful"
      components: "Clean lines, simplicity"
    examples: ["Apple", "Vercel", "Linear"]

conditional_logic:
  - condition: "constitution.md.domain == 'fintech' OR constitution.md.domain == 'healthcare'"
    action: "default_to: trusted_advisor"
    rationale: "Financial and healthcare products require trust and reliability"
  
  - condition: "constitution.md.domain == 'gaming'"
    action: "default_to: performer"
    rationale: "Gaming requires excitement and energy"
  
  - condition: "aesthetic_preset == 'linear' OR aesthetic_preset == 'vercel'"
    action: "default_to: minimalist"
    rationale: "Linear and Vercel aesthetics are minimalist"
  
  - condition: "aesthetic_preset == 'stripe' OR aesthetic_preset == 'apple'"
    action: "default_to: trusted_advisor"
    rationale: "Stripe and Apple aesthetics convey trust"
  
  - condition: "aesthetic_preset == 'slack' OR aesthetic_preset == 'figma'"
    action: "default_to: friend"
    rationale: "Slack and Figma aesthetics are friendly"

storage:
  location: "constitution.md"
  path: "design_system.brand_audience.archetype"
  additional_fields:
    - field: "personality_keywords"
      derived_from: "option.personality_keywords"
      type: "array"

impact_on_design:
  artifacts: ["design.md", "design-system.md"]
  
  design_md_changes:
    innovator:
      - section: "§ Visual Language"
        content:
          - "Bold color palette with unconventional combinations"
          - "Asymmetric layouts with experimental components"
          - "Animation-heavy interactions, cutting-edge patterns"
      - section: "§ Brand Personality"
        content: "Innovator archetype: Bold, forward-thinking, disruptive"
    
    trusted_advisor:
      - section: "§ Visual Language"
        content:
          - "Conservative color palette (blues, grays, professional)"
          - "Traditional symmetric layouts with proven patterns"
          - "Subtle animations, data visualization focus"
      - section: "§ Brand Personality"
        content: "Trusted Advisor archetype: Professional, reliable, expert"
    
    friend:
      - section: "§ Visual Language"
        content:
          - "Warm color palette with friendly tones"
          - "Rounded corners, approachable layouts"
          - "Micro-interactions, delightful details"
      - section: "§ Brand Personality"
        content: "Friend archetype: Approachable, warm, helpful"
    
    performer:
      - section: "§ Visual Language"
        content:
          - "Vibrant, bold color palette with high energy"
          - "Dynamic layouts, immersive experiences"
          - "Rich animations, theatrical interactions"
      - section: "§ Brand Personality"
        content: "Performer archetype: Exciting, energetic, entertaining"
    
    minimalist:
      - section: "§ Visual Language"
        content:
          - "Monochromatic palette with generous white space"
          - "Content-first layouts, clean lines"
          - "Minimal animations, purposeful simplicity"
      - section: "§ Brand Personality"
        content: "Minimalist archetype: Clean, simple, refined"
  
  token_adjustments:
    innovator:
      colors: "Experimental palette (e.g., purple #8B5CF6, teal #14B8A6)"
      corner_radius: "Mixed (0px buttons, 16px cards for contrast)"
      shadows: "Dramatic (large shadows for depth)"
      animations: "Rich (spring animations, staggers)"
    
    trusted_advisor:
      colors: "Traditional palette (blue #3B82F6, gray #6B7280)"
      corner_radius: "Soft (4-8px, consistent)"
      shadows: "Subtle (minimal elevation)"
      animations: "Standard (ease-out, predictable)"
    
    friend:
      colors: "Warm palette (coral #FF6B6B, yellow #FFD93D)"
      corner_radius: "Rounded (12-16px, friendly)"
      shadows: "Elevated (moderate shadows)"
      animations: "Standard (micro-interactions)"
    
    performer:
      colors: "Vibrant palette (red #EF4444, purple #A855F7)"
      corner_radius: "Pill (full rounded, energetic)"
      shadows: "Dramatic (high contrast)"
      animations: "Rich (complex, theatrical)"
    
    minimalist:
      colors: "Monochromatic (black #000000, white #FFFFFF, gray #E5E7EB)"
      corner_radius: "Sharp (0-2px, clean)"
      shadows: "None (flat design)"
      animations: "Minimal (fade only)"

dqs_integration:
  dimension: "Brand Consistency"
  max_points: 15
  scoring:
    archetype_reflected_in_specs: 15
    archetype_mentioned_not_expressed: 10
    no_alignment: 5
  
  validation_rules:
    - condition: "archetype == 'trusted_advisor'"
      expect: "design.md contains 'conservative' OR 'professional' color palette"
      severity: "MEDIUM"
    
    - condition: "archetype == 'trusted_advisor'"
      expect: "design.md contains 'traditional' OR 'symmetric' layouts"
      severity: "MEDIUM"
    
    - condition: "archetype == 'innovator'"
      expect: "design.md contains 'bold' OR 'experimental' OR 'unconventional'"
      severity: "MEDIUM"
    
    - condition: "archetype == 'friend'"
      expect: "design.md contains 'warm' OR 'friendly' OR 'rounded corners'"
      severity: "MEDIUM"
    
    - condition: "archetype == 'performer'"
      expect: "design.md contains 'vibrant' OR 'dramatic' OR 'rich animations'"
      severity: "MEDIUM"
    
    - condition: "archetype == 'minimalist'"
      expect: "design.md contains 'monochromatic' OR 'white space' OR 'minimal'"
      severity: "MEDIUM"
```

---

### Example 3: Q16 Error Prevention Strategy

```yaml
question_id: Q16
batch: 5
category: "UX Quality"
order: 16

question:
  text: "What is your strategy for preventing user errors?"
  header: "Error Prevention"
  description: "Determines error handling patterns, validation, and recovery flows."

options:
  - value: "proactive"
    label: "Proactive (Prevent errors before they happen)"
    description: "Constraints, smart defaults, inline validation, confirmation dialogs"
    impact:
      - "Constraint rules in design specs"
      - "Smart default recommendations"
      - "Confirmation dialog patterns"
      - "Inline validation specifications"
    examples: ["Banking apps", "Healthcare systems", "E-commerce checkouts"]
  
  - value: "reactive"
    label: "Reactive (Clear error messages and recovery)"
    description: "Good error messages, easy undo, helpful recovery paths"
    recommended: true
    impact:
      - "Error message content guidelines"
      - "Error state component designs"
      - "Recovery flow diagrams"
    examples: ["Most SaaS products", "Gmail", "Notion"]
  
  - value: "minimal"
    label: "Minimal (Basic validation only)"
    description: "Server-side validation, generic error messages"
    impact:
      - "Basic error state notes"
    examples: ["Internal tools", "Admin panels"]
  
  - value: "none"
    label: "None (Users figure it out)"
    description: "No error handling design"
    impact:
      - "No error handling specifications"
    examples: ["Prototypes", "Developer tools"]

conditional_logic:
  - condition: "Q14.answer == 'simple'"
    action: "skip_question"
    rationale: "Simple flows don't need sophisticated error prevention"
  
  - condition: "Q14.answer IN ['moderate', 'complex', 'very_complex']"
    action: "ask_question"
    rationale: "Complex flows benefit from error prevention"
  
  - condition: "constitution.md.domain == 'fintech' OR constitution.md.domain == 'healthcare'"
    action: "default_to: proactive"
    rationale: "High-stakes domains require proactive error prevention"
  
  - condition: "constitution.md.domain == 'gaming'"
    action: "skip_question"
    rationale: "Gaming UI has different error paradigms"

storage:
  location: "constitution.md"
  path: "design_system.ux_quality.error_prevention"
  additional_fields:
    - field: "inline_validation"
      derived_from: "option.value"
      mapping:
        proactive: true
        reactive: true
        minimal: false
        none: false
    
    - field: "confirmation_dialogs"
      derived_from: "option.value"
      mapping:
        proactive: true
        reactive: false
        minimal: false
        none: false
    
    - field: "undo_redo"
      derived_from: "option.value"
      mapping:
        proactive: true
        reactive: true
        minimal: false
        none: false

impact_on_design:
  artifacts: ["design.md", "components.md"]
  
  design_md_changes:
    proactive:
      - section: "§ Error Prevention"
        content:
          - "**Constraint Rules**: Disabled buttons until form valid"
          - "**Smart Defaults**: Pre-fill common values"
          - "**Inline Validation**: Real-time validation on blur"
          - "**Confirmation Dialogs**: For destructive actions (delete, archive)"
      
      - section: "§ Component States"
        content:
          - "Button: disabled state when form invalid"
          - "Input: inline validation indicators (checkmark/error)"
          - "Dialog: confirmation dialog pattern"
      
      - section: "§ Validation Rules"
        content:
          - "Email: RFC 5322 validation"
          - "Password: 8+ chars, 1 uppercase, 1 number"
          - "Date: ISO 8601 format, future dates only"
    
    reactive:
      - section: "§ Error Handling"
        content:
          - "**Error Messages**: Clear, actionable, non-technical"
          - "**Error States**: Red border, error icon, helper text"
          - "**Recovery Flows**: Undo button for 5 seconds after action"
      
      - section: "§ Error Message Guidelines"
        content:
          - "Pattern: '[What happened] [Why] [What to do]'"
          - "Example: 'Email already exists. Please use a different email or log in.'"
    
    minimal:
      - section: "§ Error Handling"
        content:
          - "Basic server-side validation"
          - "Generic error messages"
    
    none:
      - section: "§ Error Handling"
        content: null  # Section omitted

dqs_integration:
  dimension: "Error Handling"
  max_points: 10
  scoring:
    proactive_with_specs: 10
    reactive_with_recovery: 8
    minimal: 5
    none: 2
  
  validation_rules:
    - condition: "error_prevention == 'proactive'"
      expect: "design.md contains constraint rules"
      severity: "HIGH"
    
    - condition: "error_prevention == 'proactive'"
      expect: "design.md contains confirmation dialog patterns"
      severity: "HIGH"
    
    - condition: "error_prevention == 'proactive'"
      expect: "design.md contains inline validation specifications"
      severity: "HIGH"
    
    - condition: "error_prevention == 'reactive'"
      expect: "design.md contains error message guidelines"
      severity: "MEDIUM"
    
    - condition: "error_prevention == 'reactive'"
      expect: "design.md contains recovery flow diagrams"
      severity: "MEDIUM"
```

---

## 7. Files to Modify

### **File 1: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/shared/design-questionnaire.md`** (PRIMARY)

**Changes**:
1. Add new section "## Batch 5: UX Quality (Questions 13-17)" after Batch 4
2. Add new section "## Batch 6: Brand & Audience (Questions 18-22)" after Batch 5
3. Update STEP 3 in "Interactive Collection Flow" to include new batches:

```markdown
  Batch 5 (UX Quality):
    Q13: "What is your target usability quality level?"
    Q14: "How complex are the typical user flows?"
    Q15: "Beyond WCAG compliance, what level of accessibility empowerment?"
    Q16: "What is your strategy for preventing user errors?"
    Q17: "What responsive design strategy?"

  Batch 6 (Brand & Audience):
    Q18: "What brand personality archetype?"
    Q19: "What tone of voice should UI copy use?"
    Q20: "What is the technical sophistication level of target users?"
    Q21: "What primary emotion should users feel?"
    Q22: "Which audience demographic considerations are most critical?"
```

4. Update STEP 3 "Store Responses" to include new fields:

```markdown
  design_preferences = {
    theme_mode: response_1,
    ...
    framework_preset: response_11,
    aesthetic_preset: response_12,
    
    # NEW: UX Quality
    usability_target: response_13,
    flow_complexity: response_14,
    a11y_empowerment: response_15,
    error_prevention: response_16,
    responsive_strategy: response_17,
    
    # NEW: Brand & Audience
    brand_archetype: response_18,
    tone_of_voice: response_19,
    user_sophistication: response_20,
    emotional_goal: response_21,
    demographics_priority: response_22  # Array
  }
```

5. Add conditional logic section after Storage:

```markdown
## Conditional Logic Rules

### Batch 5 Conditions

**Q13: Usability Target**
- IF constitution.md.target_scale == "enterprise" → Default to "best"
- IF constitution.md.target_scale == "prototype" → Default to "low"

**Q14: Flow Complexity**
- IF constitution.md.app_type == "API/Backend Service" → Skip
- IF constitution.md.domain == "E-commerce" → Default to "moderate"
- IF constitution.md.domain == "Healthcare" OR "Fintech" → Default to "complex"

**Q15: A11y Empowerment**
- ONLY ASK IF constitution.md.app_type IN ["Web", "Mobile", "Desktop"]
- IF constitution.md.accessibility_level == "wcag22-aaa" → Default to "inclusive"
- IF constitution.md.accessibility_level == "wcag21-a" → Default to "compliance_only"

**Q16: Error Prevention**
- ONLY ASK IF Q14.answer IN ["moderate", "complex", "very_complex"]
- IF constitution.md.domain IN ["fintech", "healthcare"] → Default to "proactive"
- IF constitution.md.domain == "gaming" → Skip

**Q17: Responsive Strategy**
- ONLY ASK IF constitution.md.app_type == "Web Application"
- IF constitution.md.app_type == "Mobile Application" → Skip
- IF constitution.md.domain == "SaaS" → Default to "desktop_first"
- IF constitution.md.domain IN ["E-commerce", "Marketing"] → Default to "mobile_first"

### Batch 6 Conditions

**Q18: Brand Archetype**
- IF constitution.md.domain IN ["fintech", "healthcare"] → Default to "trusted_advisor"
- IF constitution.md.domain == "gaming" → Default to "performer"
- IF aesthetic_preset IN ["linear", "vercel"] → Default to "minimalist"
- IF aesthetic_preset IN ["stripe", "apple"] → Default to "trusted_advisor"
- IF aesthetic_preset IN ["slack", "figma"] → Default to "friend"

**Q19: Tone of Voice**
- IF constitution.md.domain IN ["healthcare", "fintech"] → Default to "formal"
- IF constitution.md.domain == "gaming" → Default to "playful"
- IF constitution.md.app_type == "API/Backend Service" → Default to "technical"
- MUST ALIGN with Q18:
  - "Trusted Advisor" → "formal" OR "professional"
  - "Friend" → "conversational" OR "playful"
  - "Minimalist" → "professional" OR "technical"

**Q20: User Sophistication**
- IF constitution.md.app_type IN ["CLI Tool", "API"] → Default to "expert"
- IF constitution.md.domain == "healthcare" → Default to "intermediate"
- IF constitution.md.domain == "gaming" → Skip

**Q21: Emotional Goal**
- SKIP IF constitution.md.app_type == "API"
- IF constitution.md.domain IN ["fintech", "healthcare"] → Default to "confidence"
- IF constitution.md.domain == "gaming" → Default to "excitement"
- MUST ALIGN with Q18:
  - "Trusted Advisor" → "confidence"
  - "Friend" → "delight"
  - "Performer" → "excitement"
  - "Minimalist" → "calm"
  - "Innovator" → "empowerment"

**Q22: Demographics Priority**
- IF constitution.md.language IN ["ru", "zh", "ar"] → Auto-select "global_audience"
- IF constitution.md.accessibility_level >= "wcag22-aa" → Auto-suggest "neurodiversity"
- Multiple selections allowed
```

6. Add section "## Storage in constitution.md":

```markdown
## Storage in constitution.md

All responses stored in `/memory/constitution.md` under `design_system` section:

```yaml
design_system:
  framework: "shadcn/ui"              # Q11
  aesthetic: "linear"                 # Q12
  enforcement_level: "warn"
  
  ux_quality:
    usability_target: "competitive"   # Q13
    sus_threshold: 70
    flow_complexity: "moderate"       # Q14
    avg_steps_per_flow: 5
    a11y_empowerment: "compliance_plus"  # Q15
    screen_reader_optimized: true
    keyboard_shortcuts: false
    error_prevention: "reactive"      # Q16
    inline_validation: true
    confirmation_dialogs: false
    undo_redo: false
    responsive_strategy: "desktop_first"  # Q17
    breakpoints:
      mobile: "320px"
      tablet: "768px"
      desktop: "1024px"
      wide: "1440px"
  
  brand_audience:
    archetype: "trusted_advisor"      # Q18
    personality_keywords: ["professional", "reliable", "expert"]
    tone_of_voice: "professional"     # Q19
    use_contractions: true
    person: "second"
    humor_level: "subtle"
    user_sophistication: "intermediate"  # Q20
    onboarding_required: true
    tooltips_frequency: "moderate"
    keyboard_shortcuts: false
    emotional_goal: "confidence"      # Q21
    micro_interactions: "subtle"
    illustration_style: "professional"
    demographics_priority: ["global_audience"]  # Q22 (multi-select)
    i18n_support: true
    rtl_support: false
    reduced_motion_default: false
    performance_budget: "moderate"
```
```

7. Add section "## Impact on Design Generation":

(Add detailed mappings from Section 4 of this plan)

---

### **File 2: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/commands/design.md`** (SECONDARY)

**Changes**:
1. Update frontmatter `pre_gates` to check constitution for new settings:

```yaml
pre_gates:
  - gate: IG-DESIGN-001
    name: Spec Quality Check
    check: "SQS >= 70 from spec.md"
    severity: HIGH
  
  # NEW: Check constitution completeness
  - gate: IG-DESIGN-002
    name: Constitution Design Settings Check
    check: "constitution.md has design_system.ux_quality OR --quick flag"
    severity: MEDIUM
    auto_remediation: false
    description: "Verify constitution has UX/brand settings before design generation"
```

2. Update `gates` to include new DQS dimensions:

```yaml
gates:
  - gate: QG-DQS-001
    name: Minimum Design Quality Score
    check: "DQS >= 70"
    severity: CRITICAL
    phase: POST
    description: "Enhanced DQS includes 14 dimensions (180 points normalized to 100)"
```

3. In "Phase 1: Design System Generation Mode", update STEP 3 to reference new batches:

```markdown
  3. COLLECT extended design preferences (interactive):
     {{include: shared/design-questionnaire.md}}
     
     Execute Batch 1-6 via AskUserQuestion tool:
     - Batch 1-2: Visual Foundation
     - Batch 3: Icons & Motion
     - Batch 4: Design Presets
     - Batch 5: UX Quality (NEW)
     - Batch 6: Brand & Audience (NEW)
     
     SKIP if --quick OR --defaults OR all values in constitution.md
```

4. Update subagent prompts to read new constitution fields:

**design-researcher agent**:
```markdown
## Context
Feature: {{FEATURE_DIR}}
Spec: {{FEATURE_DIR}}/spec.md
Constitution: memory/constitution.md

READ constitution.md.design_system.brand_audience.archetype
READ constitution.md.design_system.ux_quality.usability_target

## Task
Research design context and gather inputs:
1. Analyze spec.md for UI-related functional requirements
2. Extract brand guidelines from constitution (including archetype, tone)
3. Identify target user personas and sophistication level from constitution
4. Research competitor UX patterns aligned with brand archetype
5. IF usability_target == "best-in-class", include SUS benchmarking research
```

**ux-designer agent**:
```markdown
## Context
...
READ constitution.md.design_system.ux_quality.flow_complexity
READ constitution.md.design_system.ux_quality.a11y_empowerment
READ constitution.md.design_system.ux_quality.error_prevention
READ constitution.md.design_system.ux_quality.responsive_strategy

## Task
Create UX specifications adjusted for:
1. Flow complexity:
   - IF "simple" → Inline flows only
   - IF "moderate" → Step-by-step diagrams
   - IF "complex" → Comprehensive diagrams with branching
   - IF "very_complex" → State machine diagrams + wizard patterns
2. A11y empowerment:
   - IF "inclusive" → Screen reader UX notes, keyboard shortcuts
   - IF "proactive" → Screen reader testing plan
   - IF "compliance+" → Standard ARIA annotations
3. Error prevention:
   - IF "proactive" → Constraint rules, confirmation dialogs
   - IF "reactive" → Error message guidelines, recovery flows
4. Responsive strategy:
   - Generate breakpoint-specific wireframes per strategy
```

**product-designer agent**:
```markdown
## Context
...
READ constitution.md.design_system.brand_audience.archetype
READ constitution.md.design_system.brand_audience.tone_of_voice
READ constitution.md.design_system.brand_audience.emotional_goal
READ constitution.md.design_system.brand_audience.user_sophistication

## Task
Create visual specifications adjusted for:
1. Brand archetype:
   - "Innovator" → Bold colors, unconventional layouts
   - "Trusted Advisor" → Conservative palette, traditional layouts
   - "Friend" → Warm colors, rounded corners
   - "Performer" → Vibrant colors, dramatic shadows
   - "Minimalist" → Monochromatic, white space
2. Tone of voice → Generate microcopy examples:
   - "Formal" → Third-person, no contractions
   - "Professional" → Second-person, clear
   - "Conversational" → Friendly, contractions
   - "Playful" → Witty, emoji
   - "Technical" → Precise, jargon
3. Emotional goal → Adjust animation complexity:
   - "Confidence" → Stable, predictable
   - "Delight" → Playful, surprise
   - "Calm" → Minimal, soft
   - "Excitement" → Rich, dynamic
4. User sophistication → Adjust information density:
   - "Expert" → Dense layouts, keyboard shortcuts
   - "Intermediate" → Balanced, some tooltips
   - "Beginner" → Progressive disclosure, onboarding
```

5. Add new CLI flags:

```markdown
### Flags

**Design System Flags**:
- `--design-system` — Generate complete design system (triggers Batch 1-6)
- `--quick` — Skip all questionnaires, use defaults
- `--defaults` — Use default answers for all questions
- `--skip-ux-questions` — Skip Batch 5 (UX Quality questions) (NEW)
- `--skip-brand-questions` — Skip Batch 6 (Brand questions) (NEW)
```

---

### **File 3: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/memory/constitution.md`** (TERTIARY)

**Changes**:
1. Update "## Design System Configuration" section to document new fields:

```markdown
## Design System Configuration

### Design System Settings

Configure your UI framework, aesthetic presets, UX quality targets, and brand personality:

```yaml
design_system:
  # Framework & Aesthetic (Q11-Q12)
  framework: "shadcn/ui"              # Component library
  aesthetic: "linear"                 # Brand visual style
  enforcement_level: "warn"
  
  # UX Quality Targets (Q13-Q17)
  ux_quality:
    usability_target: "competitive"   # best | competitive | acceptable | low
    sus_threshold: 70                 # System Usability Scale target
    flow_complexity: "moderate"       # simple | moderate | complex | very_complex
    avg_steps_per_flow: 5
    a11y_empowerment: "compliance_plus"  # inclusive | proactive | compliance_plus | compliance_only
    screen_reader_optimized: true
    keyboard_shortcuts: false
    error_prevention: "reactive"      # proactive | reactive | minimal | none
    inline_validation: true
    confirmation_dialogs: false
    undo_redo: false
    responsive_strategy: "desktop_first"  # mobile_first | desktop_first | platform_optimized | single_breakpoint | fluid
    breakpoints:
      mobile: "320px"
      tablet: "768px"
      desktop: "1024px"
      wide: "1440px"
  
  # Brand & Audience (Q18-Q22)
  brand_audience:
    archetype: "trusted_advisor"      # innovator | trusted_advisor | friend | performer | minimalist
    personality_keywords: ["professional", "reliable", "expert"]
    tone_of_voice: "professional"     # formal | professional | conversational | playful | technical
    use_contractions: true
    person: "second"                  # first | second | third
    humor_level: "subtle"             # none | subtle | moderate | high
    user_sophistication: "intermediate"  # expert | intermediate | beginner | non_technical
    onboarding_required: true
    tooltips_frequency: "moderate"    # none | minimal | moderate | generous
    keyboard_shortcuts: false
    emotional_goal: "confidence"      # confidence | delight | empowerment | calm | excitement
    micro_interactions: "subtle"      # none | subtle | moderate | rich
    illustration_style: "professional"  # none | professional | friendly | playful
    demographics_priority: ["global_audience"]  # Array: age_range, global_audience, neurodiversity, low_bandwidth, none
    i18n_support: true
    rtl_support: false
    reduced_motion_default: false
    performance_budget: "moderate"    # strict | moderate | relaxed
  
  # Theme Tokens (unchanged)
  theme:
    colors: ...
    typography: ...
```
```

2. Add new section "### UX Quality Guidelines":

```markdown
### UX Quality Guidelines

These settings (from `/speckit.design` Batch 5) define usability, flow complexity, accessibility, error handling, and responsive strategies.

**Usability Target**:
- **Best-in-class**: SUS ≥85, comprehensive testing plan
- **Competitive**: SUS 70-84, heuristic evaluation
- **Acceptable**: SUS 60-69, minimal testing
- **Low priority**: No formal usability requirements

**Flow Complexity**:
- **Simple**: 1-3 steps, single screen
- **Moderate**: 4-7 steps, 2-3 screens
- **Complex**: 8-15 steps, 4+ screens, branching logic
- **Very Complex**: 15+ steps, state machines, wizards

**A11y Empowerment** (beyond WCAG):
- **Inclusive Excellence**: Accessibility as innovation driver
- **Proactive**: User testing with diverse abilities
- **Compliance+**: WCAG + usability best practices
- **Compliance Only**: WCAG 2.1 AA minimum

**Error Prevention**:
- **Proactive**: Prevent errors before they happen (constraints, confirmations)
- **Reactive**: Clear error messages and recovery paths
- **Minimal**: Basic validation only
- **None**: No error handling design

**Responsive Strategy**:
- **Mobile-First**: Design for small screens, scale up
- **Desktop-First**: Design for large screens, adapt down
- **Platform-Optimized**: Different layouts per device
- **Single Breakpoint**: Desktop + Mobile views only
- **Fluid**: No breakpoints, fully responsive (Grid/Flexbox)
```

3. Add new section "### Brand & Audience Guidelines":

```markdown
### Brand & Audience Guidelines

These settings (from `/speckit.design` Batch 6) define brand personality, tone, target audience, and emotional design goals.

**Brand Archetype**:
- **Innovator**: Bold, forward-thinking (startups, tech)
- **Trusted Advisor**: Professional, reliable (enterprise, fintech, healthcare)
- **Friend**: Approachable, warm (consumer apps, collaboration)
- **Performer**: Exciting, energetic (gaming, media)
- **Minimalist**: Clean, simple (productivity, design tools)

**Tone of Voice**:
- **Formal**: Professional, third-person, no contractions (legal, healthcare)
- **Professional**: Clear, direct, some personality (SaaS, B2B)
- **Conversational**: Friendly, second-person, contractions (consumer apps)
- **Playful**: Witty, humorous, personality-driven (gaming, lifestyle)
- **Technical**: Precise, jargon-heavy, expert-focused (developer tools)

**User Sophistication**:
- **Expert**: Power users, professionals (dense UI, keyboard shortcuts)
- **Intermediate**: Familiar with similar tools (standard patterns)
- **Beginner**: First-time users (onboarding, tooltips)
- **Non-technical**: Seniors, low digital literacy (extra-simple, forgiving)

**Emotional Goal**:
- **Confidence**: Trust, security, reliability (financial, healthcare)
- **Delight**: Joy, surprise, playfulness (consumer apps)
- **Empowerment**: Control, mastery, productivity (productivity tools)
- **Calm**: Peace, simplicity, focus (meditation, minimalist tools)
- **Excitement**: Energy, anticipation, thrill (gaming, social media)

**Demographics Priority** (multi-select):
- **Age Range**: Seniors, youth, children (age-appropriate patterns)
- **Global Audience**: i18n, RTL, cultural sensitivity
- **Neurodiversity**: ADHD, autism, dyslexia (reduced motion, clear structure)
- **Low Bandwidth**: Slow connections (performance, lazy loading)
- **None**: Homogeneous audience (no special considerations)
```

---

### **File 4: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/shared/design-quality-score.md`** (NEW FILE)

**Changes**:
1. Create new file documenting enhanced DQS calculation
2. Include all 14 dimensions with scoring rules (copy from Section 5 of this plan)
3. Add validation rules for each dimension
4. Document normalization formula

**File Structure**:
```markdown
# Design Quality Score (DQS) v2.0

## Overview

DQS evaluates design.md quality across 14 dimensions (180 points, normalized to 0-100).

**Threshold**: ≥70 (normalized) for production-ready design.

## Dimensions

### 1. Visual Specifications (0-25 points)
...

### 2. Component Documentation (0-25 points)
...

### 3. A11y Empowerment (0-10 points)
...

(Include all 14 dimensions from Section 5)

## Calculation

```text
DQS_raw = sum(all 14 dimensions)  # 0-180 points
DQS_normalized = (DQS_raw / 180) * 100  # 0-100 scale
```

## Validation Rules

(Include all validation rules from Section 5)

## Quality Gates

- **QG-DQS-001**: Minimum Design Quality Score (DQS ≥ 70)
- **QG-DQS-002**: Accessibility Compliance (A11y dimension ≥ 6)
- **QG-DQS-003**: Token Compliance (WCAG 2.1 AA color contrast)
```

---

### **File 5: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/docs/COMMANDS_GUIDE.md`** (UPDATE REQUIRED)

**Changes** (per CLAUDE.md maintenance rules):
1. Update `/speckit.design` section:
   - Add new flags: `--skip-ux-questions`, `--skip-brand-questions`
   - Update description to mention "10 new UX/brand questions"
2. Update Quick Reference tables:
   - Add new flags to flags table
3. Update footer with new version and timestamp

---

### **File 6: `/Users/dmitry.lazarenko/Documents/projects/spec-kit/CHANGELOG.md`** (UPDATE REQUIRED)

**Changes**:
1. Add new version entry (increment patch: current version + 0.0.1)
2. Format:

```markdown
## [X.Y.Z+1] - 2026-01-11

### Added
- **10 new design questions** in `/speckit.design` focused on UX quality and brand/audience:
  - Batch 5: Q13-Q17 (Usability targets, flow complexity, a11y empowerment, error prevention, responsive strategy)
  - Batch 6: Q18-Q22 (Brand archetype, tone of voice, user sophistication, emotional goal, demographics)
- **Enhanced DQS** (Design Quality Score) with 8 new dimensions (180 points normalized to 100)
- **Constitution integration**: New `ux_quality` and `brand_audience` sections in `design_system` config
- **Conditional logic**: Questions adapt based on app type, domain, scale, and previous answers
- **Cross-command integration**: `/speckit.specify` and `/speckit.plan` read new settings to influence requirements and tasks
- **New CLI flags**: `--skip-ux-questions`, `--skip-brand-questions` to skip question batches

### Changed
- **DQS calculation**: Expanded from 5 to 14 dimensions (backwards-compatible normalization)
- **Design agent prompts**: Updated to read and apply new constitution settings
- **constitution.md template**: Added UX Quality and Brand & Audience documentation sections

### Technical Details
- Files modified: 6 (design-questionnaire.md, design.md, constitution.md, design-quality-score.md [new], COMMANDS_GUIDE.md, CHANGELOG.md)
- Questions: 10 new (5 UX, 5 Brand/Audience)
- Conditional logic rules: 22 conditions across 10 questions
- Storage fields: 30+ new fields in constitution.md
- DQS dimensions: 8 new (Usability Testing, Flow Docs, A11y Empowerment, Error Handling, Responsive, Brand Consistency, Emotional Design, User Empowerment, Inclusive Design)
```

---

## 8. Implementation Sequencing

### Phase 1: Core Question Definition (Day 1)

**Tasks**:
1. Write 10 question definitions in YAML format (all fields: text, header, options, conditional_logic, storage, impact, DQS)
2. Map all conditional logic dependencies (22 conditions)
3. Define storage schema in constitution.md
4. Document all derived fields and mappings

**Deliverable**: Complete question specifications (can be validated against constitution Q6-Q9.5 pattern)

---

### Phase 2: Questionnaire Integration (Day 2)

**Tasks**:
1. Update `templates/shared/design-questionnaire.md`:
   - Add Batch 5 section (Q13-Q17)
   - Add Batch 6 section (Q18-Q22)
   - Add conditional logic rules
   - Add storage mapping
   - Add impact on design generation
2. Test: Verify markdown syntax, YAML blocks, example code

**Deliverable**: Updated design-questionnaire.md with 10 new questions

---

### Phase 3: Command Template Updates (Day 3)

**Tasks**:
1. Update `templates/commands/design.md`:
   - Add IG-DESIGN-002 pre-gate
   - Update subagent prompts (design-researcher, ux-designer, product-designer, motion-designer)
   - Add new CLI flags documentation
   - Update Phase 1 flow to reference Batch 5-6
2. Test: Verify YAML frontmatter, agent prompt syntax

**Deliverable**: Updated design.md with new constitution integration

---

### Phase 4: Constitution Template Updates (Day 4)

**Tasks**:
1. Update `memory/constitution.md`:
   - Add `ux_quality` section to `design_system` block
   - Add `brand_audience` section to `design_system` block
   - Add "UX Quality Guidelines" section
   - Add "Brand & Audience Guidelines" section
2. Test: Verify YAML syntax, template placeholders

**Deliverable**: Updated constitution.md template

---

### Phase 5: DQS Enhancement (Day 5)

**Tasks**:
1. Create `templates/shared/design-quality-score.md`:
   - Document 14 dimensions
   - Add scoring rules for 8 new dimensions
   - Add validation rules
   - Add normalization formula
2. Update design.md validation logic to use enhanced DQS

**Deliverable**: Complete DQS v2.0 specification

---

### Phase 6: Cross-Command Integration (Day 6)

**Tasks**:
1. Update `/speckit.specify` to read constitution UX/brand settings and generate NFRs
2. Update `/speckit.plan` to add design foundation tasks based on settings
3. Update `/speckit.analyze` to validate design.md against constitution settings
4. Test: Verify cross-command data flow

**Deliverable**: Integrated workflow across commands

---

### Phase 7: Documentation Updates (Day 7)

**Tasks**:
1. Update `docs/COMMANDS_GUIDE.md`:
   - Add new flags to `/speckit.design` section
   - Update Quick Reference tables
   - Update version/timestamp in footer
2. Update `CHANGELOG.md`:
   - Add new version entry
   - Document all changes
3. Update `pyproject.toml`:
   - Increment version

**Deliverable**: Complete documentation suite

---

### Phase 8: Testing & Validation (Day 8)

**Tasks**:
1. Test question conditional logic (simulate different constitution states)
2. Test storage in constitution.md (verify YAML structure)
3. Test design.md generation with new settings (verify agent prompt integration)
4. Test enhanced DQS calculation (verify all 14 dimensions)
5. Test cross-command integration (specify → design → plan → analyze)

**Deliverable**: Validated implementation

---

## 9. Risk Mitigation

### Risk 1: Conditional Logic Complexity

**Risk**: 22 conditional rules may create unexpected skip patterns or default value conflicts.

**Mitigation**:
1. Create decision tree diagram for all conditionals
2. Test matrix: 8 app types × 7 domains × 4 scales = 224 combinations (sample 20%)
3. Add fallback: If conditional logic fails, ask question anyway (safe default)

---

### Risk 2: Storage Schema Conflicts

**Risk**: constitution.md `design_system` block may conflict with existing user configurations.

**Mitigation**:
1. Make all new fields optional (don't break existing constitutions)
2. Add migration guide in CHANGELOG for users who already have design_system configured
3. Use nested structure (`ux_quality`, `brand_audience`) to avoid field name collisions

---

### Risk 3: DQS Threshold Changes

**Risk**: Enhanced DQS with 14 dimensions may cause existing designs to fail QG-DQS-001 gate.

**Mitigation**:
1. Normalize to 0-100 (backwards compatible)
2. Keep threshold at 70 (unchanged)
3. Add grace period: Warn for 1 month before enforcing new dimensions as CRITICAL

---

### Risk 4: Agent Prompt Token Bloat

**Risk**: Adding constitution reads to agent prompts may exceed token limits.

**Mitigation**:
1. Use cache_control: ephemeral for constitution.md (only fetch once per session)
2. Selective reads: Agents only read relevant sections (e.g., ux-designer reads `ux_quality`, product-designer reads `brand_audience`)
3. Use `{{CONSTITUTION_UX}}` template variables instead of full file reads

---

### Risk 5: Cross-Command Data Sync Issues

**Risk**: If constitution.md is updated manually, cross-command integration may break.

**Mitigation**:
1. Add pre-gate: IG-DESIGN-002 checks constitution.md has `ux_quality` OR `--quick` flag
2. Add auto-remediation: If missing, offer to run `/speckit.design --design-system` to populate
3. Validate YAML schema in constitution.md before reading

---

## 10. Success Criteria

### Functional Requirements

1. ✅ All 10 questions execute correctly via `AskUserQuestion` tool
2. ✅ Conditional logic skips/defaults questions based on constitution values
3. ✅ Answers stored in constitution.md `design_system.ux_quality` and `design_system.brand_audience`
4. ✅ Design agents read constitution and apply settings to generated design.md
5. ✅ Enhanced DQS calculates 14 dimensions correctly
6. ✅ Cross-command integration works (`/speckit.specify`, `/speckit.plan`, `/speckit.analyze`)

---

### Quality Requirements

1. ✅ DQS threshold ≥70 (normalized) for production-ready design
2. ✅ No breaking changes to existing constitution.md configurations
3. ✅ All new questions follow constitution Q6-Q9.5 pattern (header, options, defaults, impact)
4. ✅ Documentation updated (COMMANDS_GUIDE.md, CHANGELOG.md, constitution.md template)

---

### User Experience Requirements

1. ✅ Question batches execute in <2 minutes (5 questions × 20s = 100s per batch)
2. ✅ Skip flags work (`--skip-ux-questions`, `--skip-brand-questions`)
3. ✅ Default values are sensible (users can accept defaults for 80% of questions)
4. ✅ Error messages are clear if conditional logic fails

---

### Performance Requirements

1. ✅ Constitution.md reads cached (not fetched on every agent call)
2. ✅ Agent prompts <10K tokens (including constitution snippets)
3. ✅ DQS calculation <500ms (14 dimensions, ~100 validation rules)

---

## 11. Open Questions & Decisions

### Q1: Should Q22 (Demographics) be multi-select or single-select?

**Decision**: **Multi-select** (allows selecting both "Global Audience" + "Neurodiversity")

**Rationale**: Demographics are not mutually exclusive. A product can target global users AND neurodiverse users.

**Implementation**: Store as array in constitution.md: `demographics_priority: ["global_audience", "neurodiversity"]`

---

### Q2: Should new questions be mandatory or optional?

**Decision**: **Optional** with smart defaults

**Rationale**: 
- Existing users shouldn't be forced to answer 10 new questions
- New users benefit from full questionnaire
- `--quick` flag skips all questions (use defaults)

**Implementation**: 
- If constitution.md has `ux_quality` section → Skip Batch 5
- If constitution.md has `brand_audience` section → Skip Batch 6
- If `--quick` flag → Skip all batches

---

### Q3: Should DQS threshold change from 70 to 80?

**Decision**: **Keep at 70** (unchanged)

**Rationale**:
- Enhanced DQS with 14 dimensions is already stricter
- Changing threshold would break existing workflows
- Users can strengthen in constitution: `QG-DQS-001: SHOULD (70%) → MUST (80%)`

---

### Q4: Should emotional_goal validation be CRITICAL or MEDIUM?

**Decision**: **MEDIUM severity**

**Rationale**:
- Emotional design is subjective (no objective validation)
- Misalignment with archetype is a quality issue, not a blocker
- CRITICAL reserved for objective failures (missing wireframes, contrast violations)

---

### Q5: Should we add example mockups for each brand archetype?

**Decision**: **No** (out of scope for this plan)

**Rationale**:
- This plan focuses on question infrastructure and integration
- Example mockups would be a separate feature (could use `/speckit.preview` integration)
- Can be added in future iteration

---

## 12. Future Enhancements (Out of Scope)

1. **Visual Archetype Gallery**: Generate example design.md snippets for each archetype (Future v2.1)
2. **Tone of Voice Linter**: Auto-validate microcopy in design.md matches tone settings (Future v2.2)
3. **Usability Testing Integration**: Auto-generate SUS survey and analysis scripts (Future v2.3)
4. **A11y Automation**: Generate WCAG test scripts based on a11y_empowerment level (Future v2.4)
5. **Responsive Preview**: Generate breakpoint previews via `/speckit.preview` (Future v2.5)

---

## 13. Summary

This plan adds **10 high-quality UX and brand questions** to `/speckit.design` that:

✅ Follow proven constitution/concept patterns  
✅ Use sophisticated conditional logic (22 rules)  
✅ Store in constitution.md for cross-command integration  
✅ Influence design generation through agent prompts  
✅ Enhance DQS with 8 new dimensions (14 total, 180 points)  
✅ Enable brand-aligned, usability-focused design specs  

**Estimated Implementation**: 8 days (1 developer)  
**Files Modified**: 6 core files + 1 new file  
**Questions Added**: 10 (5 UX Quality, 5 Brand & Audience)  
**Conditional Logic**: 22 rules across 10 questions  
**Storage Fields**: 30+ in constitution.md  
**DQS Dimensions**: 8 new (total 14, 180 points normalized to 100)  

---

# Critical Files for Implementation

- **/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/shared/design-questionnaire.md** — PRIMARY: Add Batch 5 (Q13-Q17) and Batch 6 (Q18-Q22) with full question definitions, conditional logic, storage mappings, and impact specifications

- **/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/commands/design.md** — SECONDARY: Update subagent prompts (design-researcher, ux-designer, product-designer) to read new constitution.md fields and apply UX/brand settings; add new CLI flags and pre-gates

- **/Users/dmitry.lazarenko/Documents/projects/spec-kit/memory/constitution.md** — TERTIARY: Add `ux_quality` and `brand_audience` sections to `design_system` config block with complete YAML schema and documentation

- **/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/shared/design-quality-score.md** — NEW FILE: Document enhanced DQS v2.0 with 14 dimensions (8 new), scoring rules, validation logic, and normalization formula

- **/Users/dmitry.lazarenko/Documents/projects/spec-kit/templates/commands/specify.md** — CROSS-COMMAND: Update to read constitution.md UX/brand settings and auto-generate NFRs for usability, i18n, performance based on targets (enables constitution-driven requirements)

---

**Plan Status**: ✅ COMPLETE — Ready for implementation

**Next Steps**: Review plan with stakeholders → Approve → Execute Phase 1 (Question Definition)
