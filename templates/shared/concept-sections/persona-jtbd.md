# Deep Persona Framework (JTBD-Enhanced)

> **Purpose**: Understand users beyond demographics — capture their Jobs-to-be-Done.

## Persona Template

### Persona: [Name] — [Role/Title]

#### Demographics
| Attribute | Value |
|-----------|-------|
| **Segment** | [B2B SMB / B2B Mid-Market / B2B Enterprise / B2C Consumer / B2C Prosumer] |
| **Industry** | [Vertical if B2B] |
| **Tech Comfort** | [Low / Medium / High] |
| **Frequency of Use** | [Daily power user / Weekly regular / Monthly occasional / One-time] |
| **Decision Authority** | [End user / Influencer / Budget holder / Final decision maker] |

#### Context
- **Current tools**: [What they use today]
- **Team size**: [Solo / Small team / Large org]
- **Pain intensity**: [1-10] — [Brief explanation]

---

#### Jobs-to-be-Done (JTBD)

| Job Type | When I... | I want to... | So I can... |
|----------|-----------|--------------|-------------|
| **Functional** | [trigger situation] | [action/capability] | [functional outcome] |
| **Emotional** | [trigger situation] | [feel/experience] | [emotional state] |
| **Social** | [trigger situation] | [appear/be seen as] | [social perception] |

##### Functional Jobs (Core)
1. **Primary job**: When [situation], I want to [action], so I can [outcome]
2. **Secondary job**: When [situation], I want to [action], so I can [outcome]

##### Emotional Jobs (Experience)
1. When [situation], I want to feel [emotion], so I can [state]
2. When [situation], I want to avoid feeling [negative emotion]

##### Social Jobs (Perception)
1. When [situation], I want to appear [perception] to [audience]

---

#### Willingness to Pay

| Factor | Value | Notes |
|--------|-------|-------|
| **Current spend on alternatives** | $[X]/mo | [What tools/services] |
| **Budget authority** | $[X]/mo without approval | [Approval needed above] |
| **Pain severity** | [1-10] | [Higher = more willing to pay] |
| **Switching cost tolerance** | [Low / Medium / High] | [Barriers to switching] |
| **Price sensitivity** | [Low / Medium / High] | [How much price matters] |

##### Value Equation
- **Gains from switching**: [Time saved, money saved, outcomes improved]
- **Pains of switching**: [Learning curve, data migration, team adoption]
- **Net value perception**: [Positive / Neutral / Negative]

---

#### Success Criteria

| Priority | Criteria | Measurable Indicator |
|----------|----------|---------------------|
| **Must have** | [Non-negotiable outcome] | [How we know it's achieved] |
| **Must have** | [Non-negotiable outcome] | [How we know it's achieved] |
| **Nice to have** | [Delighter] | [How we measure satisfaction] |
| **Nice to have** | [Delighter] | [How we measure satisfaction] |

##### Deal Breakers (Instant Churn Triggers)
- [ ] [Unacceptable experience/outcome]
- [ ] [Missing critical capability]
- [ ] [Performance below threshold]

---

#### User Journey Touchpoints

| Stage | Action | Emotion | Opportunity |
|-------|--------|---------|-------------|
| **Awareness** | [How they find us] | [Curious / Skeptical] | [First impression] |
| **Consideration** | [Evaluation process] | [Hopeful / Anxious] | [Build confidence] |
| **Decision** | [Purchase/signup] | [Committed / Hesitant] | [Reduce friction] |
| **Onboarding** | [First use] | [Excited / Overwhelmed] | [Time to value] |
| **Adoption** | [Regular use] | [Satisfied / Frustrated] | [Habit formation] |
| **Advocacy** | [Recommending] | [Proud / Indifferent] | [Viral growth] |

---

## Additional Personas

> Repeat the template above for each significant persona (recommend 2-4 total)

### Persona 2: [Name] — [Role]
[Use template above]

### Persona 3: [Name] — [Role]
[Use template above]

---

## Persona Prioritization

| Persona | Revenue Potential | Acquisition Cost | Strategic Value | Priority |
|---------|------------------|------------------|-----------------|----------|
| [Persona 1] | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] | [P0/P1/P2] |
| [Persona 2] | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] | [P0/P1/P2] |
| [Persona 3] | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] | [P0/P1/P2] |

**Primary target**: [Persona name] — [Why they're the beachhead]

---

## AI-Assisted Persona Synthesis

> **Purpose**: Generate data-validated personas from real user evidence, not PM intuition. Transform persona development from guesswork to systematic evidence collection.

### Data Sources for AI Persona Generation

| Source Type | Platforms | AI Task | Evidence Tier |
|-------------|-----------|---------|:-------------:|
| **Public Reviews** | G2, Capterra, TrustRadius (B2B) | Extract pain points, feature requests, sentiment | STRONG |
| **App Reviews** | App Store, Google Play (B2C) | Extract UX frustrations, delight moments | STRONG |
| **Community Discourse** | Reddit, HackerNews (Prosumer) | Identify repeated pain points (frequency = severity) | MEDIUM |
| **Job Postings** | LinkedIn, Indeed | Extract responsibilities, required tools, KPIs | STRONG |
| **Industry Reports** | Gartner, Forrester, McKinsey | Extract budget data, market segments, WTP | VERY_STRONG |
| **Social Media** | LinkedIn, Twitter/X | Identify workflow pain, tool frustrations | MEDIUM |

### AI Persona Synthesis Prompt

Use this prompt with `persona-researcher-ai` for data-driven persona generation:

```markdown
## AI Persona Synthesis Task

Based on research data from [DATA_SOURCES], synthesize 2-4 distinct user personas for [PRODUCT_CONCEPT].

For each persona:

1. **Demographics** (from job postings, industry reports):
   - Job title, industry, company size
   - Tech comfort level (infer from tools in job descriptions)
   - Frequency of use (infer from problem severity in reviews)

2. **Jobs-to-be-Done** (from reviews, forum discussions):
   - Functional: Extract from "I wish I could..." statements
   - Emotional: Extract from sentiment analysis of frustration/delight
   - Social: Extract from status-signaling language in reviews
   - **Require ≥3 evidence citations per JTBD**

3. **Willingness-to-Pay** (from pricing data, budget reports):
   - Current spend: Extract from "We pay $X/mo for [alternative]"
   - Pain severity: Score 1-10 based on complaint frequency/intensity
   - Switching cost: High if "locked in", Low if "easy to replace"

4. **Success Criteria** (from KPIs in job postings, reviews):
   - Must have: Features in >50% of positive reviews
   - Nice to have: Features in 20-50% of reviews
   - Deal breakers: Issues in >30% of negative reviews

**Output**: JTBD-Enhanced persona profiles with [EV-XXX] source citations.
```

### Evidence Requirements per Persona

| Element | Minimum Evidence | Tier Required | Points |
|---------|------------------|:-------------:|:------:|
| Demographics | ≥3 job postings analyzed | STRONG | 25 |
| Functional JTBD | ≥5 review citations | STRONG | 25 |
| Emotional JTBD | ≥3 sentiment examples | MEDIUM | 20 |
| Social JTBD | ≥2 status-signaling quotes | MEDIUM | 15 |
| WTP | Pricing data from ≥2 alternatives | STRONG | 25 |
| Deal Breakers | ≥10 negative review patterns | STRONG | 20 |

### Validation Layer

Cross-reference AI-generated personas with:
- [ ] Customer interviews (if available)
- [ ] Sales team feedback
- [ ] Support ticket analysis
- [ ] Usage analytics (for existing products)

### Persona Quality Gate

| Persona Element | Evidence Status | Action |
|-----------------|:---------------:|--------|
| Demographics | ✅ VS/S | Proceed |
| Demographics | ⚠️ M | Proceed with caution |
| Demographics | ❌ W/N | Block — gather more evidence |
| JTBD Functional | ✅ VS/S | Proceed |
| JTBD Functional | ❌ M/W/N | Block — minimum STRONG required |
| WTP | ✅ VS/S | Proceed |
| WTP | ❌ M/W/N | Warn — conduct pricing research |

---

## Integration Notes

- **CQS Impact**: Persona Depth component (15% weight) directly uses evidence tiers from this section
- **Agent Dependency**: `persona-researcher-ai` populates evidence automatically
- **JTBD Links**: Each feature should trace back to ≥1 JTBD (>80% coverage required for CQS transparency points)
