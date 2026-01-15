# Decision Log: Business Strategy Recommendations

**Project**: spec-kit `/speckit.concept` Enhancement
**Agent**: Business Strategist
**Purpose**: Track strategic decisions and recommendations

---

## Decision #001: Strategic Gap Analysis Scope

**Date**: 2026-01-01
**Status**: ✅ Complete
**Decision Type**: Analysis scope definition

### Context
User requested analysis of what's MISSING in `/speckit.concept` to match Fortune 500 corporate strategy standards (Amazon, Microsoft, Google, Oracle).

### Decision
Structured analysis into 5 categories:
1. Strategic Planning Gaps
2. Investment-Grade Analysis
3. Scenario Planning
4. Strategic Alternatives
5. Execution Readiness

### Rationale
- Fortune 500 strategy frameworks cluster into these 5 domains
- Aligns with how Board/CEO review investment decisions
- Covers full spectrum: Market → Strategy → Execution → Finance

### Outcome
**Deliverables created**:
1. `/outputs/business-strategy/agents/business-strategist/2026-01-01_concept-strategic-gaps-analysis.md` (17 pages, 50+ frameworks)
2. `/outputs/business-strategy/agents/business-strategist/2026-01-01_executive-summary.md` (quick reference)
3. `/outputs/business-strategy/agents/business-strategist/2026-01-01_framework-comparison.md` (visual comparison)

### Next Steps
- [ ] Review with product team
- [ ] Prioritize frameworks (Tier 1 vs 2 vs 3)
- [ ] Prototype enhanced template

---

## Decision #002: Tier Classification (Priority Framework)

**Date**: 2026-01-01
**Status**: ✅ Complete
**Decision Type**: Prioritization framework

### Context
Identified 14 missing frameworks. Need prioritization for phased rollout.

### Decision
**Tier 1 (Critical)**: 5 frameworks — Must-have for Board credibility
1. Investment Thesis
2. Strategic Alternatives (Build/Buy/Partner)
3. Financial Sensitivity
4. Three Horizons
5. Pre-Mortem

**Tier 2 (High Value)**: 5 frameworks — Best practice, differentiating
6. PRFAQ (Working Backwards)
7. Scenario Planning (2×2)
8. Strategic Options
9. Execution Confidence
10. Portfolio View

**Tier 3 (Nice-to-Have)**: 4 frameworks — Corporate polish
11. MOALS/OSM
12. Ecosystem Strategy
13. Value-Based Pricing
14. Investment Readiness Score

### Rationale
**Tier 1 criteria**:
- Required for Board/exec approval in Fortune 500
- High impact on decision quality
- Relatively low implementation effort (88 hours total)

**Tier 2 criteria**:
- Used by best-in-class companies (Amazon PRFAQ, Google pre-mortems)
- Significant value but not universally required
- Medium implementation effort (136 hours)

**Tier 3 criteria**:
- Advanced frameworks for mature orgs
- High effort, specialized use cases

### Outcome
**Recommended rollout**:
- Phase 1 (Weeks 1-3): Tier 1 → `--mode=board` flag
- Phase 2 (Weeks 4-7): Tier 2 → optional sections
- Phase 3 (Weeks 8-12): Tier 3 → enterprise features

**ROI estimate**:
- Tier 1 investment: $15,600 (88 hours @ $150/hr)
- Return: $500K-$1.5M saved (100 users × $5K-$15K consulting fees)
- **ROI: 32-96×**

### Dependencies
- Product team approval on roadmap
- Design resources for templates
- QA resources for testing

### Review Trigger
Re-evaluate Tier 2/3 scope after Tier 1 beta (5 users, 30 days)

---

## Decision #003: Board Mode Flag Design

**Date**: 2026-01-01
**Status**: 🟡 Proposed (pending review)
**Decision Type**: Product design

### Context
Current `/speckit.concept` generates product-focused concepts. Need way to toggle "board-ready" mode.

### Decision
Add `--mode` flag to `/speckit.concept`:

```bash
# Default mode (current behavior)
/speckit.concept "Build task manager for teams"

# Board mode (adds Tier 1 frameworks)
/speckit.concept --mode=board "Build task manager for teams"

# Executive mode (adds Tier 1 + Tier 2)
/speckit.concept --mode=executive "Build task manager for teams"
```

**Mode comparison**:

| Feature | Default | Board | Executive |
|---------|:-------:|:-----:|:---------:|
| TAM/SAM/SOM | ✅ | ✅ | ✅ |
| JTBD Personas | ✅ | ✅ | ✅ |
| Risk Matrix | ✅ | ✅ | ✅ |
| Investment Thesis | ❌ | ✅ | ✅ |
| Strategic Alternatives | ❌ | ✅ | ✅ |
| Financial Sensitivity | ❌ | ✅ | ✅ |
| Three Horizons | ❌ | ✅ | ✅ |
| Pre-Mortem | ❌ | ✅ | ✅ |
| PRFAQ | ❌ | ❌ | ✅ |
| Scenario Planning | ❌ | ❌ | ✅ |
| Strategic Options | ❌ | ❌ | ✅ |
| Execution Confidence | ❌ | ❌ | ✅ |
| Portfolio View | ❌ | ❌ | ✅ |

### Rationale
**Why flags vs separate command**:
- Same underlying concept, different depth
- Users can upgrade from default → board → executive
- Backwards compatible (default mode unchanged)

**Why "board" vs "strategy"**:
- Clear target audience (Board/CEO level)
- Matches user mental model ("boardify this concept")
- Differentiates from product strategy (already covered)

### Alternatives Considered
1. **Separate command** (`/speckit.strategy`):
   - ❌ Confusing (concept vs strategy overlap)
   - ❌ Duplicates structure

2. **Auto-detect** (based on input complexity):
   - ❌ Unpredictable behavior
   - ❌ Users want explicit control

3. **Progressive enhancement** (ask after default):
   - ✅ Could work, but verbose
   - ❌ Breaks flow for users who know they need board mode

### Outcome
**Recommendation**: Implement `--mode=board` flag in Phase 1 (Tier 1 frameworks only).

**Success criteria**:
- [ ] 5 beta users create board-ready concepts
- [ ] 80% pass exec review on first submission (vs <50% currently)
- [ ] Time-to-approval reduced by 50% (1 review cycle vs 2-3)

### Review Trigger
After 30 days of beta usage, analyze:
- Mode adoption rate (default vs board vs executive)
- User feedback on flag naming
- Decision to add `--mode=executive` in Phase 2

---

## Decision #004: Financial Model Integration Strategy

**Date**: 2026-01-01
**Status**: 🟡 Proposed (pending technical review)
**Decision Type**: Technical architecture

### Context
Tier 1 frameworks require **Financial Sensitivity Analysis** with NPV/IRR calculations. Two approaches:

### Decision (PENDING)
**Option A: Template-based** (manual calculation)
- User fills out revenue/cost assumptions in markdown tables
- Agent provides formulas, user calculates in spreadsheet
- **Pros**: Simple, no dependencies
- **Cons**: Error-prone, not interactive

**Option B: Interactive calculator** (embedded tool)
- Agent generates Python script for NPV/IRR calculation
- User inputs assumptions, script outputs scenarios
- **Pros**: Accurate, reproducible
- **Cons**: Requires Python execution environment

**Option C: Hybrid** (template + optional script)
- Template with manual tables (always works)
- Optional: Generate Python script if user wants automation
- **Pros**: Best of both worlds
- **Cons**: More complex to maintain

### Recommendation (Pending)
**Start with Option A** (template-based) for Phase 1:
- Faster to ship (no code generation needed)
- Validates user demand for financial modeling
- Upgrade to Option C in Phase 2 if users request automation

### Open Questions
- [ ] Do target users (PMs, execs) have Python/spreadsheet skills?
- [ ] Should we integrate with Google Sheets API for auto-calc?
- [ ] What's the accuracy requirement (ballpark vs CFO-grade)?

### Review Trigger
After Phase 1 beta (30 days):
- Survey users: "Would you use an automated NPV calculator?"
- If >60% say yes → build Option B/C in Phase 2

---

## Decision #005: Example Library Strategy

**Date**: 2026-01-01
**Status**: 🟡 Proposed
**Decision Type**: Documentation & enablement

### Context
New frameworks (PRFAQ, Pre-Mortem, etc.) need concrete examples. Users won't understand abstract templates.

### Decision
Create **Example Library** with real-world strategy documents:

**Tier 1 Examples** (public domain or synthesized):
1. **Amazon PRFAQ**: Kindle Fire launch (synthesized from public interviews)
2. **Microsoft Horizon**: Azure strategy classification (based on Satya's memos)
3. **Google Pre-Mortem**: Google Wave failure analysis (post-mortem → pre-mortem)
4. **Investment Thesis**: Stripe Series A pitch (public deck)
5. **Build vs Buy vs Partner**: Figma acquisition rationale (synthesized)

**Tier 2 Examples**:
6. **Scenario Planning**: Netflix streaming pivot (2007-2011 scenarios)
7. **Strategic Options**: Airbnb Experiences (platform option exercise)

### Rationale
**Why real examples matter**:
- Users pattern-match ("make mine like Amazon's")
- Concrete > abstract (see filled template, not blank)
- Credibility (Fortune 500 actually use these)

**Why synthesized (not verbatim)**:
- Legal risk (confidential docs)
- Pedagogical clarity (real docs have context noise)
- Customizable (adjust complexity for different industries)

### Outcome
**Deliverables**:
- `/templates/examples/prfaq-kindle.md`
- `/templates/examples/horizon-azure.md`
- `/templates/examples/premortem-wave.md`
- `/templates/examples/investment-stripe.md`
- `/templates/examples/buildbuybuy-figma.md`

**Reference in templates**:
```markdown
## Investment Thesis

> **Example**: See [Stripe Series A Investment Thesis](examples/investment-stripe.md)

[Template starts here...]
```

### Effort Estimate
- Research per example: 2-4 hours
- Writing per example: 4-6 hours
- **Total for 5 examples**: 30-50 hours

### Review Trigger
After examples published:
- Track which examples users reference most
- Update low-usage examples with better content

---

## Decision #006: Positioning Strategy for spec-kit

**Date**: 2026-01-01
**Status**: 💡 Insight (for product/marketing team)
**Decision Type**: Strategic positioning

### Context
Adding Tier 1-3 frameworks changes **what spec-kit is**:
- **Before**: Developer productivity tool (spec-driven development)
- **After**: Strategic planning platform (product + strategy)

### Insight
**Competitive positioning shift**:

| Competitor | Before | After Enhancement |
|------------|--------|-------------------|
| **Confluence/Notion** | ✅ Comparable (both do specs) | ✅ Superior (only one with strategy frameworks) |
| **Aha!/ProductPlan** | ✅ Comparable (roadmaps) | ✅ Superior (investment-grade concepts) |
| **McKinsey/BCG** | ❌ Different market (consulting) | ⚠️ Competitive threat (we automate their frameworks) |

**New value propositions**:

**For Product Managers**:
- "Create board-ready concepts in 30 minutes, not 30 hours"
- "Never get your concept rejected for 'lack of strategic rigor' again"

**For Executives**:
- "Standardize how teams pitch ideas — compare apples to apples"
- "Built-in investment framework = faster, better capital allocation"

**For Companies**:
- "Replace $50K McKinsey strategy engagement with $5K software"
- "Democratize strategic thinking across all teams"

### Recommendation
**Positioning statement**:
> spec-kit: The only development platform that speaks both product AND boardroom.
>
> Generate investment-grade strategic concepts using Fortune 500 frameworks (Amazon PRFAQ, McKinsey Three Horizons, VC sensitivity analysis) — then seamlessly flow into spec-driven development.

**Differentiation**:
- **Not just**: "Write better specs" (Confluence does that)
- **But**: "Make strategic decisions with Board-level rigor, then execute with spec-driven precision"

### Pricing Implications
**Current**: Free tier + Pro ($X/mo)
**Enhanced opportunity**:
- **Free**: Default mode (product specs)
- **Pro**: Board mode (Tier 1 frameworks)
- **Enterprise**: Executive mode (Tier 2 + portfolio dashboard)

**Justification**:
- Board mode saves $5K-$15K in consulting fees per concept
- $99/mo Pro tier = 1 concept ROI (vs $5K consultant)
- $499/mo Enterprise = 1 major strategy project ROI (vs $50K McKinsey)

### Review Trigger
After Phase 1 launch:
- Track conversion: Default → Board mode (activation metric)
- Survey: "Would you pay for Board mode?" (pricing validation)
- Competitive analysis: Did Aha!/ProductPlan respond?

---

## Decisions Summary

| ID | Decision | Status | Impact | Next Action |
|----|----------|:------:|--------|-------------|
| #001 | Strategic Gap Analysis Scope | ✅ Complete | High | Review with team |
| #002 | Tier Classification | ✅ Complete | High | Get roadmap approval |
| #003 | Board Mode Flag | 🟡 Proposed | High | Design review |
| #004 | Financial Model Integration | 🟡 Proposed | Medium | Technical feasibility |
| #005 | Example Library | 🟡 Proposed | Medium | Assign writer |
| #006 | Positioning Strategy | 💡 Insight | High | Product/marketing review |

---

## Next Review: 2026-01-15

**Agenda**:
1. Product team feedback on Tier 1 scope
2. Technical feasibility review (Decision #004)
3. Go/No-Go on Phase 1 (Board mode MVP)
4. Assign owners for example library (Decision #005)

**Success criteria for review**:
- [ ] Tier 1 frameworks approved for Phase 1
- [ ] `--mode=board` design finalized
- [ ] Phase 1 timeline confirmed (3 weeks target)
- [ ] Beta user recruitment plan (5 users)

---

**Log maintained by**: Business Strategist Agent
**Last updated**: 2026-01-01
