# Evidence Tracking

> **Purpose**: Track and score evidence quality for each concept claim to enable evidence-based CQS scoring.

## Evidence Tiers

| Tier | Code | Points | Criteria | Examples |
|------|:----:|:------:|----------|----------|
| **VERY_STRONG** | VS | 30 | Primary research, verified data, multiple independent sources | Customer interviews (n≥10), A/B test results, financial audits |
| **STRONG** | S | 25 | Credible secondary sources, recent data (<1 year) | Industry reports (Gartner, IDC), verified case studies, SEC filings |
| **MEDIUM** | M | 20 | Industry reports, analyst estimates, expert opinions | Analyst estimates, conference talks, blog posts from practitioners |
| **WEAK** | W | 5 | Assumptions, extrapolations, outdated data (>2 years) | Founder intuition, extrapolated trends, anecdotal evidence |
| **NONE** | N | 0 | No evidence provided | Unsubstantiated claims |

---

## Evidence Requirements by Component

### Market Validation (20% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| TAM Calculation | ≥3 independent sources, methodology documented | STRONG | 30 |
| SAM Filters | ≥2 sources for segment sizing | MEDIUM | 25 |
| SOM Estimate | Comparable company data OR customer intent signals | MEDIUM | 20 |
| Competitive Matrix | ≥3 competitors analyzed with pricing data | STRONG | 25 |

**Evidence Examples**:
- ✅ STRONG: "TAM of $50B based on Gartner 2024 report + IDC forecast + company 10-K filings"
- ⚠️ WEAK: "TAM estimated at $50B based on market trends"
- ❌ NONE: "Large market opportunity"

### Persona Depth (15% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| Persona Definition | ≥5 customer interviews OR ≥100 survey responses | STRONG | 30 |
| JTBD Functional | ≥3 evidence points per JTBD | MEDIUM | 25 |
| JTBD Emotional | ≥2 quotes from target users | MEDIUM | 15 |
| Willingness to Pay | Pricing research OR Van Westendorp analysis | STRONG | 15 |
| Success Criteria | Validated with ≥3 users | MEDIUM | 15 |

**Evidence Examples**:
- ✅ VERY_STRONG: "Based on 15 customer interviews conducted Dec 2024, transcript IDs: INT-001 to INT-015"
- ⚠️ WEAK: "Based on founder's experience in the industry"

### Metrics Quality (15% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| North Star Metric | Benchmark data from ≥2 comparable companies | STRONG | 40 |
| SMART Validation | Each metric has baseline + target | MEDIUM | 30 |
| Leading Indicators | Correlation evidence OR industry standard | MEDIUM | 15 |
| Lagging Indicators | Defined measurement methodology | MEDIUM | 15 |

### Feature Completeness (15% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| Feature Hierarchy | Traced to ≥1 JTBD each | MEDIUM | 30 |
| Wave Assignments | Dependency analysis documented | MEDIUM | 25 |
| Golden Path | User journey validated with ≥3 users | STRONG | 25 |
| UX Foundations | Competitive analysis completed | MEDIUM | 20 |

### Risk Assessment (10% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| Risk Identification | Industry research OR expert consultation | MEDIUM | 30 |
| Mitigations | Similar solutions documented | MEDIUM | 25 |
| Contingencies | Resource estimates provided | MEDIUM | 15 |
| Pivot Criteria | Quantitative thresholds defined | MEDIUM | 30 |

### Technical Hints (10% weight)

| Claim Type | Minimum Evidence | Tier Required | Points |
|------------|------------------|:-------------:|:------:|
| Domain Entities | Architecture review OR prototype | STRONG | 35 |
| API Surface | Comparable system analysis | MEDIUM | 25 |
| Integration Complexity | Documentation review completed | MEDIUM | 20 |
| Constitution Conflicts | Explicit resolution documented | MEDIUM | 20 |

---

## Evidence Registry

Track all evidence sources used in concept:

| ID | Claim | Component | Source | Tier | Date | Notes |
|:--:|-------|-----------|--------|:----:|:----:|-------|
| EV-001 | TAM = $50B | Market | Gartner Report 2024 | S | 2024-12 | p.45 |
| EV-002 | Primary persona: DevOps Engineer | Persona | 12 customer interviews | VS | 2024-11 | Transcripts attached |
| EV-003 | 40% of users need feature X | Feature | Survey (n=150) | S | 2024-12 | Response rate 35% |
| ... | ... | ... | ... | ... | ... | ... |

---

## Evidence Gap Analysis

Identify claims lacking sufficient evidence:

| Component | Claim | Current Tier | Required Tier | Gap | Action |
|-----------|-------|:------------:|:-------------:|:---:|--------|
| Market | SAM sizing | WEAK | MEDIUM | -15 pts | Conduct segment research |
| Persona | WTP analysis | NONE | STRONG | -25 pts | Run Van Westendorp survey |
| ... | ... | ... | ... | ... | ... |

**Total Evidence Gap**: -XX points

---

## Cross-Validation Matrix

For critical claims, require multiple independent sources:

| Claim | Source 1 | Source 2 | Source 3 | Variance | Status |
|-------|----------|----------|----------|:--------:|:------:|
| TAM = $50B | Gartner: $48B | IDC: $52B | Bottom-up: $51B | 8% | ✅ Valid |
| Competitor A pricing | Website: $99 | G2: $99 | Sales call: $99 | 0% | ✅ Valid |
| ... | ... | ... | ... | ... | ... |

**Variance Threshold**: < 30% for VALID status

---

## Evidence Collection Checklist

### Before Starting Concept
- [ ] Schedule ≥5 customer interviews
- [ ] Prepare survey (target n≥100)
- [ ] Identify industry reports to review
- [ ] Set up competitive monitoring

### During Concept Development
- [ ] Document source for every quantitative claim
- [ ] Record interview quotes for qualitative claims
- [ ] Cross-validate critical numbers (TAM, pricing)
- [ ] Flag assumptions explicitly

### Before CQS Calculation
- [ ] Complete Evidence Registry
- [ ] Run Evidence Gap Analysis
- [ ] Verify Cross-Validation Matrix
- [ ] Calculate tier-adjusted scores

---

## AI-Assisted Evidence Collection

When using research agents, evidence is automatically tracked:

| Agent | Evidence Type | Auto-Captured |
|-------|---------------|:-------------:|
| market-intelligence-ai | TAM/SAM/SOM sources | ✅ |
| competitive-intelligence-ai | Competitor pricing, features | ✅ |
| persona-researcher-ai | User quotes, pain points | ✅ |
| trend-analyst-ai | Trend sources, timing signals | ✅ |

Agent outputs include `evidence_links[]` array for automatic registry population.
