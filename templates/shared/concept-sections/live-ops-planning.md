# Live Operations Planning Framework

## Overview

Framework for planning and executing live operations (LiveOps) in event-driven games, covering infrastructure, event calendars, remote configuration, A/B testing, and monitoring strategies.

**Target Games**: F2P mobile games, live service games, GaaS (Games as a Service)
**Key Principle**: Maximize player engagement and retention through dynamic content updates without app store releases

## Infrastructure Requirements

### Remote Configuration

**Purpose**: Update game parameters server-side without app updates

**Key Parameters**:
- **Economy Tuning**: Currency rewards, shop prices, energy costs
- **Difficulty Balancing**: Enemy health, XP curves, level gating
- **Feature Toggles**: Enable/disable features for specific user segments
- **Event Parameters**: Start/end times, rewards, difficulty
- **A/B Test Variables**: UI variants, pricing tiers, onboarding flows

**Tools**:
- **Firebase Remote Config**: Free tier up to 10M daily fetches, 5-minute cache TTL
- **PlayFab Title Data**: Enterprise-grade, $0.15/1000 API calls
- **Custom Solution**: Redis + REST API for full control

**Rollback Plan**:
1. Detect anomaly (crash rate >5%, revenue drop >20%)
2. Revert to last known good config (1-click)
3. Wait 5 minutes for cache TTL
4. Monitor recovery metrics

### A/B Testing

**Purpose**: Validate design decisions with statistical confidence before full rollout

**Typical Tests**:
- **Onboarding Flow**: Tutorial length, skip option, hand-holding vs. freedom
- **IAP Pricing**: $4.99 vs. $9.99 starter pack
- **Ad Frequency**: Interstitial every 3 levels vs. every 5 levels
- **UI Variants**: Button placement, color, wording

**Success Criteria**:
- Minimum sample size: 1000 users per variant
- Statistical significance: p < 0.05 (95% confidence)
- Run duration: 7-14 days (capture weekly cycles)
- Primary metric: D7 retention, ARPU, or conversion rate

**Tools**:
- **Firebase A/B Testing**: Free, integrated with Analytics
- **Optimizely**: Enterprise ($50K+/year), multivariate testing
- **Custom**: Feature flags + analytics pipeline

### Event System

**Purpose**: Deploy time-limited content to create urgency and FOMO

**Event Types**:
- **Recurring Events**: Daily login, weekend boost (low effort, high retention)
- **Seasonal Events**: Halloween, Christmas, Summer (high effort, high revenue)
- **Live Ops Events**: Limited-time challenges, leaderboards (medium effort, engagement spike)
- **Collaborative Events**: Community goals, raid bosses (high social engagement)

**Technical Requirements**:
- Server-authoritative start/end times (prevent client-side cheating)
- Graceful degradation if server unreachable (offline mode with cached rewards)
- Event data preloaded in app bundle (reduce download friction)
- Localized event descriptions and notifications

## Event Calendar (First 90 Days)

### Week 1-2: Soft Launch

**Goals**: Validate core loop, tune economy, baseline metrics

**Activities**:
- No events (focus on core stability)
- Remote config enabled, default values only
- Daily monitoring: crash rate, D1/D7 retention, session length

**Metrics to Establish**:
- Baseline D1: 40-50% (mobile games)
- Baseline D7: 20-30%
- Baseline ARPU: $0.10-0.50 (F2P + Ads)

### Week 3-4: First Event Test

**Event**: "Welcome Week" — Daily login bonuses

**Structure**:
- Day 1: 100 coins
- Day 3: 300 coins + 1 rare item
- Day 7: 1000 coins + exclusive character

**Goals**:
- Test event infrastructure (start/end triggers, reward delivery)
- Improve D7 retention by 5-10%
- Collect data on event engagement

**A/B Test**:
- Control: No event
- Variant A: Welcome Week as described
- Variant B: Welcome Week with push notifications
- Hypothesis: Variant B increases D7 by 8% vs. Control

### Week 5-8: Regular Event Cadence

**Frequency**: One event every 2 weeks

**Event Rotation**:
- Week 5: "Weekend Warrior" — 2x XP Saturday-Sunday
- Week 7: "Treasure Hunt" — Hidden collectibles in levels

**Goals**:
- Establish predictable event rhythm
- Test different event types (economy boost vs. new content)
- Increase DAU by 15% during event windows

### Week 9-12: Seasonal Event

**Event**: "Halloween Havoc" (if timing aligns)

**Structure**:
- New themed levels (3-5)
- Limited-time cosmetics (IAP + in-game currency)
- Leaderboard with exclusive rewards (top 100)

**Goals**:
- Revenue spike: 50-100% increase during event
- New player acquisition: Themed ASO + UA campaigns
- Retention: 30% of event participants return post-event

## Remote Config Strategy

### Configuration Tiers

| Tier | User % | Rollout Strategy | Rollback Trigger |
|------|--------|------------------|------------------|
| **Bronze (Canary)** | 5% | Random sampling, Beta testers | Crash rate >3% or revenue drop >15% |
| **Silver** | 25% | Phased rollout over 24h | Revenue drop >10% or retention drop >5% |
| **Gold (Full)** | 100% | After 72h Silver stability | Any critical metric regression |

### Example Rollout: Energy Regen Time

**Current**: 1 energy per 5 minutes (baseline)
**Test**: 1 energy per 3 minutes (increase session frequency)

**Day 1-3 (Bronze)**:
- Deploy to 5% (canary)
- Monitor: Session frequency, session length, DAU

**Day 4-6 (Silver)**:
- If metrics stable or improved, expand to 25%
- Monitor: Revenue (faster energy = less IAP?), retention

**Day 7+ (Gold)**:
- If revenue neutral or positive, full rollout
- Document: New baseline = 3-minute regen

**Rollback Example**:
- Silver phase shows 12% revenue drop
- Immediate rollback to 5-minute regen
- Hypothesis: Players no longer need to buy energy refills
- Decision: Keep 5-minute baseline, test 4-minute instead

## Push Notification Strategy

### Frequency Caps

**Hard Limits** (anti-spam):
- Maximum 3 notifications per day
- Maximum 10 notifications per week
- Minimum 4-hour gap between notifications

**Soft Limits** (engagement-based):
- If user hasn't opened app in 7 days: 1 notification per day max
- If user opted out once: No promotional notifications, only transactional

### Notification Types

| Type | Trigger | Example | Frequency |
|------|---------|---------|-----------|
| **Transactional** | User action | "Your crafting is complete!" | Unlimited (user-initiated) |
| **Re-engagement** | Lapsed user | "Your kingdom needs you! 3 days of rewards waiting" | 1x per week max |
| **Event Start** | Server-side event | "Halloween Havoc starts NOW!" | 1x per event |
| **Energy Full** | Resource capped | "Your energy is full! Don't waste it!" | 1x per day max |
| **Promotional** | Marketing campaign | "50% off on Gem Packs today only!" | 2x per month max |

### Opt-Out Policy

- **Granular Control**: Let users opt out of categories (promotional, event, energy)
- **Honor Immediately**: Don't send notification if user opted out <1 hour ago
- **In-App Settings**: Push notification preferences in settings menu
- **Re-engagement**: Offer re-opt-in with incentive (100 coins for enabling notifications)

### Localization

- Translate all notifications (10+ languages for global launch)
- Time zone-aware scheduling (send at 10 AM local time, not 10 AM UTC)
- Cultural sensitivity (no Halloween event in countries where not celebrated)

## A/B Testing Roadmap

### Month 1: Onboarding Optimization

**Test**: Tutorial length

- **Control**: Full 5-minute tutorial (20 steps)
- **Variant A**: Short 2-minute tutorial (8 steps) + "Learn as you play" tooltips
- **Variant B**: Skippable tutorial with "Pro Mode" toggle

**Primary Metric**: D1 retention
**Hypothesis**: Variant A increases D1 by 5% (less hand-holding)
**Sample Size**: 3000 users (1000 per variant)
**Duration**: 14 days

### Month 2: IAP Pricing

**Test**: Starter Pack price

- **Control**: $4.99 (500 gems + character)
- **Variant A**: $9.99 (1200 gems + character + bonus item)
- **Variant B**: $2.99 (250 gems + character)

**Primary Metric**: Conversion rate, total revenue
**Hypothesis**: Variant B converts 2x more users, higher total revenue despite lower price
**Sample Size**: 5000 users (1667 per variant)
**Duration**: 21 days (capture 3 weeks of purchasing behavior)

### Month 3: Ad Frequency

**Test**: Interstitial ad frequency (F2P users only)

- **Control**: Interstitial every 3 levels
- **Variant A**: Interstitial every 5 levels
- **Variant B**: Interstitial every 2 levels

**Primary Metric**: D7 retention, ad revenue per DAU
**Hypothesis**: Variant A increases retention by 8% without hurting ad revenue (higher engagement = more sessions = more total impressions)
**Sample Size**: 10,000 users (3333 per variant)
**Duration**: 14 days

## Monitoring Dashboard

### Real-Time Metrics (Alerts)

**Critical**:
- Crash rate >5%: Immediate rollback
- Server uptime <99%: Investigate infrastructure
- Transaction failure rate >2%: Payment provider issue

**High Priority**:
- DAU drop >20% YoY: Possible competitor launch or technical issue
- Session length drop >15%: Core loop engagement problem
- Ad fill rate <90%: Ad network issue

### Daily Metrics

- DAU, WAU, MAU
- D1, D7, D30 retention cohorts
- ARPU, ARPPU, conversion rate
- Ad impressions, eCPM, revenue
- Event participation rate

### Weekly Metrics

- LTV projections (cohort-based)
- Churn analysis (why players leave)
- Feature usage (which features are ignored?)
- A/B test results (statistical significance reached?)

## Validation Checklist

- [ ] Remote config system deployed (Firebase, PlayFab, or custom)
- [ ] Rollback procedure tested (can revert config in <5 minutes)
- [ ] A/B testing framework integrated (minimum 1000 users per variant)
- [ ] Event system infrastructure ready (server-authoritative timers)
- [ ] Push notification service configured (FCM for Android, APNs for iOS)
- [ ] Notification frequency caps enforced (3/day, 10/week)
- [ ] Opt-out policy implemented (granular categories, immediate honor)
- [ ] Monitoring dashboard built (real-time alerts, daily/weekly reports)
- [ ] First 90-day event calendar planned (soft launch → seasonal event)
- [ ] Team trained on LiveOps workflow (how to deploy config, trigger events, analyze results)

## References

- **Firebase Remote Config Documentation**: https://firebase.google.com/docs/remote-config
- **PlayFab LiveOps Guide**: https://learn.microsoft.com/en-us/gaming/playfab/features/liveops/
- **"The Art of Live Ops" by Alexander Zacherl** (Mobile Free-to-Play blog)
- **GDC Talks**: "Live Ops at King: How Candy Crush Generates $1B/Year"
- **Deconstructor of Fun**: https://www.deconstructoroffun.com (LiveOps teardowns)
