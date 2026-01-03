# Financial Sensitivity Analysis

> **Purpose**: Quantify financial outcomes under varying assumptions to identify key value drivers, validate investment resilience, and enable confident executive decision-making with risk-adjusted projections.

## Executive Summary

| Scenario | NPV | IRR | Payback | Probability | Risk-Adjusted NPV |
|----------|----:|----:|--------:|:-----------:|------------------:|
| Base Case | $[X]K | [X]% | [X] mo | [X]% | $[X]K |
| Optimistic | $[X]K | [X]% | [X] mo | [X]% | $[X]K |
| Pessimistic | $[X]K | [X]% | [X] mo | [X]% | $[X]K |
| **Expected Value** | | | | 100% | **$[X]K** |

---

## Base Case Assumptions

### Revenue Drivers

| Variable | Base Value | Source/Rationale |
|----------|:----------:|------------------|
| Total Addressable Market | $[X]M | [Market research source] |
| Serviceable Addressable Market | $[X]M | [Geographic/segment filter] |
| Market Penetration (Year 3) | [X]% | [Comparable benchmarks] |
| Average Revenue Per User (ARPU) | $[X]/mo | [Pricing analysis] |
| Conversion Rate | [X]% | [Funnel analysis/benchmarks] |
| Net Revenue Retention | [X]% | [Industry benchmarks] |

### Cost Drivers

| Variable | Base Value | Source/Rationale |
|----------|:----------:|------------------|
| Customer Acquisition Cost (CAC) | $[X] | [Channel analysis] |
| Cost of Goods Sold (COGS) | [X]% | [Operational analysis] |
| Development Investment | $[X]K | [Engineering estimates] |
| Operating Expenses | $[X]K/mo | [Budget analysis] |
| Annual OpEx Growth | [X]% | [Hiring plan] |

---

## NPV/IRR Calculation

### Discount Rate Justification

| Component | Rate | Rationale |
|-----------|:----:|-----------|
| Risk-Free Rate | [X]% | [10-year Treasury] |
| Market Risk Premium | [X]% | [Industry standard] |
| Company Risk Premium | [X]% | [Stage/execution risk] |
| **WACC/Discount Rate** | **[X]%** | [Sum of components] |

### Cash Flow Projections

| Year | Revenue | COGS | OpEx | CAPEX | FCF | Discounted FCF |
|:----:|--------:|-----:|-----:|------:|----:|---------------:|
| 0 | $0 | $0 | $[X]K | $[X]K | -$[X]K | -$[X]K |
| 1 | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| 2 | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| 3 | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| 4 | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| 5 | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| **Terminal** | | | | | $[X]K | $[X]K |
| **Total** | | | | | | **$[X]K** |

### Scenario Comparison

| Metric | Pessimistic | Base | Optimistic |
|--------|------------:|-----:|-----------:|
| 5-Year Revenue | $[X]K | $[X]K | $[X]K |
| 5-Year FCF | $[X]K | $[X]K | $[X]K |
| **NPV** | $[X]K | $[X]K | $[X]K |
| **IRR** | [X]% | [X]% | [X]% |
| **Payback Period** | [X] mo | [X] mo | [X] mo |

---

## Sensitivity Analysis

### Single-Variable Sensitivity

| Variable | -20% | -10% | Base | +10% | +20% | Impact Rank |
|----------|-----:|-----:|-----:|-----:|-----:|:-----------:|
| Market Size | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |
| Conversion Rate | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |
| ARPU | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |
| CAC | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |
| NRR | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |
| Development Cost | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K | [1-6] |

*NPV values shown; Impact Rank 1 = highest sensitivity*

### Tornado Diagram (Visual Representation)

```
                    NPV Impact (Deviation from Base Case)
                    -$500K        $0        +$500K
                    ◄───────────────┼───────────────►
                         │         │         │
Market Size        ██████████████████████████████████  [Most Sensitive]
                         │         │         │
ARPU               ████████████████████████████
                         │         │         │
Conversion Rate    ██████████████████████
                         │         │         │
NRR                ████████████████
                         │         │         │
CAC                ██████████
                         │         │         │
Development Cost   ████                              [Least Sensitive]
                         │         │         │
                    -$500K        $0        +$500K
```

### Key Sensitivity Insights

| Variable | Sensitivity | Implication | Mitigation |
|----------|:-----------:|-------------|------------|
| [Most sensitive] | High | [NPV swings $X per 10% change] | [De-risk strategy] |
| [Second most sensitive] | High | [NPV swings $X per 10% change] | [De-risk strategy] |
| [Third most sensitive] | Medium | [NPV swings $X per 10% change] | [Monitor closely] |

---

## Break-Even Analysis

### Unit Economics Break-Even

| Metric | Calculation | Value |
|--------|-------------|------:|
| Gross Margin | ARPU - Variable Costs | $[X]/user |
| Break-Even Users | Fixed Costs / Gross Margin | [X] users |
| Break-Even MRR | Break-Even Users × ARPU | $[X]K |
| Break-Even ARR | Break-Even MRR × 12 | $[X]K |

### Time to Break-Even

| Scenario | Monthly Burn | Growth Rate | Break-Even Date |
|----------|-------------:|:-----------:|:---------------:|
| Pessimistic | $[X]K | [X]% MoM | [Month Year] |
| Base | $[X]K | [X]% MoM | [Month Year] |
| Optimistic | $[X]K | [X]% MoM | [Month Year] |

### Cash Requirement to Break-Even

| Scenario | Months to B/E | Peak Cash Need | Runway Required |
|----------|:-------------:|---------------:|----------------:|
| Pessimistic | [X] mo | $[X]K | $[X]K (+20% buffer) |
| Base | [X] mo | $[X]K | $[X]K (+20% buffer) |
| Optimistic | [X] mo | $[X]K | $[X]K (+20% buffer) |

---

## Two-Variable Sensitivity Matrix

### NPV by Market Size × Conversion Rate

| | Conv 2% | Conv 3% | Conv 4% | Conv 5% | Conv 6% |
|-----|--------:|--------:|--------:|--------:|--------:|
| **TAM $50M** | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| **TAM $75M** | $[X]K | $[X]K | **$[X]K** | $[X]K | $[X]K |
| **TAM $100M** | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| **TAM $125M** | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |
| **TAM $150M** | $[X]K | $[X]K | $[X]K | $[X]K | $[X]K |

*Bold = Base case; Shaded cells indicate NPV < 0 (not viable)*

---

## Monte Carlo Simulation (Advanced)

> *Optional: For rigorous probabilistic analysis when stakes are high ($1M+ investment)*

### Input Distributions

| Variable | Distribution | Parameters | Rationale |
|----------|:------------:|------------|-----------|
| Market Size | Triangular | Min: $[X]M, Mode: $[X]M, Max: $[X]M | [Bounded uncertainty] |
| Conversion Rate | Normal | μ=[X]%, σ=[X]% | [Historical variance] |
| ARPU | Lognormal | μ=$[X], σ=$[X] | [Right-skewed pricing] |
| CAC | Triangular | Min: $[X], Mode: $[X], Max: $[X] | [Channel variability] |

### Simulation Results (10,000 iterations)

| Metric | Value |
|--------|------:|
| Mean NPV | $[X]K |
| Median NPV | $[X]K |
| Standard Deviation | $[X]K |
| 10th Percentile (downside) | $[X]K |
| 90th Percentile (upside) | $[X]K |
| Probability of NPV > 0 | [X]% |
| Probability of NPV > $[X]K target | [X]% |

### NPV Distribution

```
Probability
    │
 15%│          ┌───┐
    │        ┌─┘   └─┐
 10%│      ┌─┘       └─┐
    │    ┌─┘           └─┐
  5%│  ┌─┘               └─┐
    │┌─┘                   └─┐
  0%└────────────────────────────
    -$500K    $0    +$500K   +$1M
                 NPV

    P(NPV > 0) = [X]%
```

---

## Decision Thresholds

### Go/No-Go Criteria

| Metric | Minimum Threshold | Base Case | Status |
|--------|:-----------------:|:---------:|:------:|
| NPV | > $0 | $[X]K | [PASS/FAIL] |
| IRR | > [X]% (hurdle rate) | [X]% | [PASS/FAIL] |
| Payback | < [X] months | [X] mo | [PASS/FAIL] |
| P(NPV > 0) | > 70% | [X]% | [PASS/FAIL] |
| Peak Cash Need | < $[X]K (available) | $[X]K | [PASS/FAIL] |

### Investment Decision Matrix

| NPV Result | IRR Result | Recommendation |
|:----------:|:----------:|----------------|
| Positive | > Hurdle | **Approve with standard governance** |
| Positive | < Hurdle | Approve with enhanced monitoring |
| Negative | > Hurdle | Review assumptions; conditional approval |
| Negative | < Hurdle | **Reject or fundamental pivot required** |

---

## Financial Sensitivity Quality Checklist

- [ ] Base case assumptions documented with sources
- [ ] NPV/IRR calculated with explicit discount rate justification
- [ ] Cash flow projections cover minimum 5 years + terminal value
- [ ] Three scenarios (Base/Optimistic/Pessimistic) fully modeled
- [ ] Single-variable sensitivity completed for 5+ key variables
- [ ] Tornado diagram priorities established (impact ranking)
- [ ] Break-even analysis includes units, revenue, and time
- [ ] Two-variable sensitivity matrix for top 2 drivers
- [ ] Monte Carlo guidance included (optional execution)
- [ ] Go/No-Go thresholds defined with clear pass/fail criteria

---

## Integration Notes

- **Feeds into**: Risk matrix (financial risks), Scenario planning (financial outcomes per scenario)
- **Depends on**: Market framework (TAM/SAM), Business model canvas (revenue/cost structure), Strategic alternatives (investment amounts)
- **CQS Impact**: Improves Business Model (+4 pts) and Risk (+3 pts) scores through quantified financial analysis
