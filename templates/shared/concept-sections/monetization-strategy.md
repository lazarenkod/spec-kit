# Monetization Strategy Framework

## Overview

Framework для выбора и имплементации этичной монетизации мобильных игр, соответствующей GAM-004 (Fair Monetization).

## Monetization Models

### Premium (Pay Once)

**Characteristics**:
- One-time purchase ($0.99 - $9.99 typical)
- No ads, no IAP
- All content unlockable through play

**Best For**:
- Hyper-casual with strong IP
- Premium puzzle/narrative games
- Ports of successful PC/console games

**Revenue Potential**: Low (single transaction)
**LTV**: $1-10
**KPIs**: Downloads, conversion rate (demo → full)

**Example**: Monument Valley, Stardew Valley Mobile

### Free-to-Play + IAP

**Characteristics**:
- Free download
- Core loop free, acceleration/cosmetics purchasable
- Typical IAP: $0.99 - $99.99 (whale tiers up to $999)

**Best For**:
- Mid-core (RPG, strategy)
- Core (competitive, social)

**Revenue Potential**: High (recurring)
**LTV**: $5-50 (avg), $500+ (whales)
**KPIs**: Conversion rate (3-5% typical), ARPU, ARPPU

**IAP Categories**:
- **Consumables**: Currency, energy, boosts (recurring purchases)
- **Non-consumables**: Unlocks, permanent upgrades (one-time)
- **Subscriptions**: Battle passes, VIP tiers (recurring, predictable)

### Free-to-Play + Ads

**Characteristics**:
- Free download and play
- Ads shown (interstitial, rewarded video, banners)
- Optional IAP to remove ads or supplement ad revenue

**Best For**:
- Hyper-casual (high volume, low engagement)
- Casual (puzzle, match-3)

**Revenue Potential**: Medium (volume-dependent)
**LTV**: $0.50-3
**KPIs**: Impressions, eCPM, fill rate, ad engagement

**Ad Types**:
- **Rewarded Video**: 30s video for in-game reward (highest eCPM: $10-50)
- **Interstitial**: Full-screen between levels (eCPM: $5-15)
- **Banner**: Always visible (lowest eCPM: $1-3, annoying)

### Hybrid (IAP + Ads)

**Characteristics**:
- Both IAP and rewarded ads
- Ads = F2P player monetization
- IAP = skip ads + acceleration

**Best For**:
- Casual with depth
- Mid-core with broad audience

**Revenue Potential**: Highest (dual monetization)
**LTV**: $3-20
**KPIs**: IAP conversion, ad engagement, DAU

### Battle Pass

**Characteristics**:
- Seasonal subscription ($9.99 - $19.99 typical)
- Free tier + premium tier
- Time-limited (30-90 days)

**Best For**:
- Live service games
- Core competitive games

**Revenue Potential**: High (recurring, predictable)
**LTV**: $50-200
**KPIs**: Pass purchase rate, completion rate, renewal rate

## Ethical Pricing Principles (GAM-004 Compliance)

### ✅ Do

- **Transparent Pricing**: Show real currency prices alongside virtual currency
- **Disclose Drop Rates**: For gacha/loot boxes, show exact % (required by Apple/Google)
- **Viable F2P Path**: Core content accessible without spending
- **Value Propositions**: IAP provides clear time-saving or cosmetic value
- **Spending Limits**: Daily/weekly caps, parental controls
- **Regional Pricing**: Adjust for purchasing power (India $0.99, US $2.99, etc.)

### ❌ Don't

- **Pay-to-Win PvP**: Direct power advantage from spending in competitive modes
- **Predatory FOMO**: Fake countdown timers, limited-time pressure
- **Dark Patterns**: Hidden costs, misleading bundle values
- **Loot Box Gambling**: Games targeting kids with gacha mechanics (COPPA)
- **Bait-and-Switch**: Free trial that suddenly requires payment to continue

## Pricing Psychology

### Anchoring
- Show high-priced "worst value" option to make mid-tier seem reasonable
- Example: $99.99 (1000 gems) → $19.99 (250 gems, "best value" badge)

### Bundles
- Package currency + items for perceived value
- "Starter Pack" at $4.99 = 500 gems + Rare Character (separately $10)

### First-Time Buyer
- Aggressive first-purchase discount (5x value)
- Convert 3-5% of players into payers

### Whale Targeting
- High-tier IAP ($99.99, $499.99) for top 0.1%
- VIP systems with escalating benefits

## KPI Targets by Model

| Model | Conversion | ARPU | LTV | Retention D7 |
|-------|-----------|------|-----|--------------|
| Premium | 5-10% (demo) | $1-5 | $5-10 | 30-40% |
| F2P + IAP | 3-5% | $0.50-2 | $10-30 | 20-30% |
| F2P + Ads | N/A | $0.20-0.50 | $1-3 | 15-25% |
| Hybrid | 2-4% | $0.80-3 | $15-50 | 25-35% |
| Battle Pass | 10-20% | $2-5 | $50-200 | 35-45% |

## Regional Compliance

### Belgium & Netherlands
- Loot boxes = gambling, **banned**
- Alternative: Direct purchase or progression-based unlocks

### Japan
- "Kompu gacha" (complete-the-set) **banned**
- Must disclose all drop rates
- Age gates for purchases

### China
- Drop rates disclosure **mandatory**
- Anti-addiction systems for minors
- Real-name registration

### EU (GDPR)
- No personal data collection from <16 without parental consent
- Right to data deletion

### US (COPPA)
- No personal data from <13 without verifiable parental consent
- Age-gate before any data collection

## Validation Checklist

- [ ] Pricing transparent (real currency shown)
- [ ] Loot box drop rates disclosed (if applicable)
- [ ] F2P path to core content exists
- [ ] No pay-to-win in PvP modes
- [ ] Spending limits and parental controls implemented
- [ ] Regional compliance verified (Belgium, Japan, China, EU, US)
- [ ] KPI targets aligned with genre and model
- [ ] Ethics review: Would you let your child play this monetization model?

## References

- Apple App Store Review Guidelines (Section 3.1.1 - In-App Purchases)
- Google Play Policy (Payments, Subscriptions, Refunds)
- Deconstructor of Fun (monetization teardowns)
