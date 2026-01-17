# LTV/CAC Calculation Formula

## LTV (Lifetime Value)

**Formula**:
```
LTV = ARPDAU × Average Lifetime Days
```

**Breakdown by Player Segment**:

| Segment | % of Players | LTV Range | Revenue Contribution | Description |
|---------|--------------|-----------|----------------------|-------------|
| **Minnows** (non-payers) | 80-90% | $0.50-$2.00 | 5-15% | Ad revenue only |
| **Dolphins** (small spenders) | 8-15% | $5-$20 | 20-35% | 1-3 IAP purchases |
| **Whales** (big spenders) | 1-3% | $50-$500 | 50-75% | Recurring IAP, VIP |

**Blended LTV Calculation**:
```
Blended LTV = (% Minnows × LTV_Minnows) + (% Dolphins × LTV_Dolphins) + (% Whales × LTV_Whales)

Example:
  = (85% × $1.00) + (12% × $10) + (3% × $150)
  = $0.85 + $1.20 + $4.50
  = $6.55 per user
```

## CAC (Customer Acquisition Cost)

**Formula**:
```
CAC = Total marketing spend / New users acquired
```

**Regional CAC Benchmarks** (US iOS = baseline):

| Region | Casual/Puzzle | Mid-core | Adjustment Factor |
|--------|---------------|----------|-------------------|
| US iOS | $1.50-$4.00 | $2.00-$6.00 | 1.0x (baseline) |
| US Android | $1.00-$2.80 | $1.40-$4.20 | 0.7x iOS |
| EU iOS | $1.20-$3.20 | $1.60-$4.80 | 0.8x US |
| APAC iOS | $0.80-$2.00 | $1.00-$3.00 | 0.5x US |

**CPI Volatility Factors**:
- Q4 (holiday season): +30-50% CPI (increased competition)
- New iOS release: +20-30% CPI (early adopter premium)
- Genre saturation: Match-3 CPI inflated 2x vs 2020

## Target LTV/CAC Ratios

| Ratio | Status | Description |
|-------|--------|-------------|
| **1.5x** | Break-even | Minimum viable with margins |
| **3.0x** | Healthy | Sustainable UA scaling |
| **5.0x+** | Excellent | Aggressive growth mode |

## Payback Period

**Time to recover CAC**:
- **D7 LTV target**: 50-100% of CAC (7-day payback)
- **D30 LTV target**: 150-300% of CAC (1-month ROI positive)

## Genre-Specific Benchmarks

| Genre | Avg LTV | Avg CAC | Target Ratio | Source |
|-------|---------|---------|--------------|--------|
| **Match-3** | $2.50 | $0.80 | 3.1x | Sensor Tower |
| **Idle** | $4.20 | $1.20 | 3.5x | GameRefinery |
| **Sorting** | $1.80 | $0.60 | 3.0x | Sensor Tower |
| **Arcade** | $2.20 | $0.90 | 2.4x | GameRefinery |
| **Puzzle** | $3.00 | $1.00 | 3.0x | Sensor Tower |

## ARPDAU Estimation

**Formula**:
```
ARPDAU = (Ad Revenue per DAU) + (IAP Revenue per DAU)

Ad Revenue = (Ad impressions per DAU) × (eCPM / 1000) × Fill Rate
Example: 5 impressions × ($10 / 1000) × 0.85 = $0.0425

IAP Revenue = (IAP conversion %) × (ARPPU)
Example: 5% × $10 = $0.50

Total ARPDAU = $0.0425 + $0.50 = $0.54
```

**Genre ARPDAU Benchmarks**:

| Genre | ARPDAU Range | Primary Monetization | Source |
|-------|--------------|----------------------|--------|
| Hyper-casual | $0.05-$0.15 | Ads (rewarded video, interstitials) | Sensor Tower |
| Casual | $0.15-$0.40 | Hybrid (IAP + ads) | GameRefinery |
| Mid-core | $0.30-$0.80 | IAP (gacha, VIP pass) | Sensor Tower |
| Hardcore | $0.80-$2.50 | IAP (competitive advantage) | GameRefinery |

---

**Evidence tier**: STRONG (Sensor Tower Q3 2025, GameRefinery Mobile Gaming Benchmark Report 2025)
