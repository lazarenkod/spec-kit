# AI Responsibility Assessment

> **Purpose**: Ensure AI/ML-powered products are built responsibly with appropriate safeguards for bias, transparency, privacy, and safety.

**Applicability**: Required for concepts with AI/ML components. Skip if product has no AI functionality.

## AI Responsibility Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  RESPONSIBLE AI FRAMEWORK                        │
│                                                                  │
│  Bias & Fairness → Transparency → Privacy → Safety              │
│                                                                  │
│  "AI amplifies both benefits and harms. Build responsibly."     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Bias & Fairness Assessment

### Training Data Review
| Data Source | Size | Demographic Coverage | Known Biases | Mitigation |
|-------------|:----:|---------------------|--------------|------------|
| [Source 1] | [N] | [Groups represented] | [Issues] | [Action] |

### Fairness Testing
- [ ] Performance tested across demographic groups
- [ ] Disparate impact analysis completed
- [ ] Error rates compared across protected classes
- [ ] Edge cases identified for underrepresented groups

### Bias Mitigation Strategies
| Risk | Strategy | Status |
|------|----------|:------:|
| Training data imbalance | [e.g., Oversampling, synthetic data] | `Planned` |
| Historical bias in labels | [e.g., Re-labeling, bias-aware loss] | `Planned` |
| Feedback loop amplification | [e.g., Diversity injection, monitoring] | `Planned` |

---

## 2. Transparency Assessment

### Explainability
| Decision Type | Explainability Level | Method |
|--------------|:--------------------:|--------|
| [e.g., Content recommendation] | `HIGH` / `MEDIUM` / `LOW` | [e.g., Feature importance, attention visualization] |

### User Disclosure
- [ ] AI involvement clearly disclosed to users
- [ ] Users understand when AI is making/influencing decisions
- [ ] Confidence levels communicated where appropriate
- [ ] Limitations clearly stated

### Human Override
| Scenario | Override Available? | Process |
|----------|:-------------------:|---------|
| [e.g., Content moderation] | ✅ / ❌ | [Appeal process] |
| [e.g., Recommendation rejection] | ✅ / ❌ | [User control] |

---

## 3. Privacy Assessment

### Data Minimization
- [ ] Only necessary data collected for AI functionality
- [ ] Data requirements justified and documented
- [ ] Aggregation used where individual data not needed

### Retention & Deletion
| Data Type | Retention Period | Deletion Process | User Control |
|-----------|:----------------:|------------------|:------------:|
| [e.g., User inputs] | [Duration] | [Process] | ✅ / ❌ |
| [e.g., Model training data] | [Duration] | [Process] | ✅ / ❌ |

### Consent & Control
- [ ] Explicit consent obtained for AI processing
- [ ] Users can opt out of AI features
- [ ] Right to deletion implemented
- [ ] Data portability supported

---

## 4. Safety Assessment

### Failure Modes
| Failure Mode | Probability | Impact | Mitigation |
|--------------|:-----------:|:------:|------------|
| [e.g., Hallucination] | HIGH/MED/LOW | [Impact] | [Strategy] |
| [e.g., Adversarial attack] | HIGH/MED/LOW | [Impact] | [Strategy] |
| [e.g., Model degradation] | HIGH/MED/LOW | [Impact] | [Strategy] |

### Graceful Degradation
- [ ] Fallback behavior defined when AI fails
- [ ] User notified of degraded functionality
- [ ] Core product usable without AI features

### Human-in-the-Loop
| Decision Type | Risk Level | Human Review Required? |
|--------------|:----------:|:----------------------:|
| [e.g., High-stakes recommendation] | HIGH | ✅ Mandatory |
| [e.g., Content generation] | MEDIUM | ⚠️ Sampling |
| [e.g., Personalization] | LOW | ❌ Automated |

### Monitoring & Drift
- [ ] Model performance monitoring in place
- [ ] Data drift detection implemented
- [ ] Retraining triggers defined
- [ ] Incident response process documented

---

## AI Responsibility Summary

| Dimension | Status | Key Gaps | Priority |
|-----------|:------:|----------|:--------:|
| **Bias & Fairness** | 🟢 🟡 🔴 | [Gaps] | P1/P2/P3 |
| **Transparency** | 🟢 🟡 🔴 | [Gaps] | P1/P2/P3 |
| **Privacy** | 🟢 🟡 🔴 | [Gaps] | P1/P2/P3 |
| **Safety** | 🟢 🟡 🔴 | [Gaps] | P1/P2/P3 |

**Legend**: 🟢 Complete | 🟡 Partial | 🔴 Not Started

---

## AI Responsibility Quality Checklist

- [ ] AI components identified and documented
- [ ] Bias risks assessed with mitigation strategies
- [ ] Transparency mechanisms designed (explainability, disclosure)
- [ ] Privacy requirements mapped (consent, retention, deletion)
- [ ] Safety measures in place (fallbacks, human review, monitoring)
- [ ] Responsible AI owner assigned
- [ ] Review cadence established (quarterly minimum)

---

## Integration Notes

- **Feeds into**: Risk Assessment (AI-specific risks), Technical Hints (AI infrastructure needs)
- **Depends on**: Feature Hierarchy (which features use AI), Persona-JTBD (user expectations)
- **Connected to**: Pre-Mortem (AI failure scenarios), Constitution (AI principles alignment)
- **CQS Impact**: Improves Risk (+2 pts) for AI products through responsible AI review
