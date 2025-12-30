# Anti-Slop Quality Rules

> Explicit rules against generic AI-generated content. Import this module in all artifact-generating commands.

## Purpose

Prevent AI-generated artifacts from containing:
1. Cliché openings and conclusions
2. Hedge phrases that add no value
3. Generic buzzwords over substance
4. Safe middle-ground recommendations (without commitment)

---

## Forbidden Phrases

### Opening Clichés (NEVER use)

```text
FORBIDDEN_OPENINGS = [
  # English
  "In today's fast-paced world...",
  "In an increasingly digital landscape...",
  "It's important to note that...",
  "It's worth mentioning that...",
  "At the end of the day...",
  "When it comes to...",
  "In order to...",
  "First and foremost...",
  "Last but not least...",
  "Needless to say...",
  "As we all know...",
  "It goes without saying...",

  # Russian
  "В современном мире...",
  "В эпоху цифровизации...",
  "Стоит отметить, что...",
  "Важно понимать, что...",
  "Не секрет, что...",
  "Как известно...",
  "Прежде всего...",
  "В первую очередь стоит сказать...",
  "Нельзя не упомянуть..."
]
```

### Hedge Phrases (Remove or commit)

```text
HEDGE_PHRASES = [
  # Uncertainty markers
  "may or may not",
  "might potentially",
  "could possibly",
  "perhaps maybe",
  "it depends",
  "it varies",

  # Weasel words
  "arguably",
  "presumably",
  "supposedly",
  "generally speaking",
  "in most cases",
  "more or less",

  # Russian
  "может быть или не быть",
  "возможно, потенциально",
  "в целом и общем",
  "как правило",
  "в большинстве случаев"
]

# FIX: Replace hedge with commitment or remove entirely
# BAD: "This approach might potentially improve performance"
# GOOD: "This approach improves performance by 30%" OR remove if unproven
```

### Generic Conclusions (NEVER use)

```text
FORBIDDEN_CONCLUSIONS = [
  "In conclusion...",
  "To summarize...",
  "To sum up...",
  "All in all...",
  "In summary...",
  "At the end of the day...",
  "The bottom line is...",

  # Russian
  "В заключение...",
  "Подводя итоги...",
  "Резюмируя...",
  "В итоге...",
  "Таким образом, можно сделать вывод..."
]

# FIX: End with action items or next steps, not summary
```

---

## Forbidden Patterns

### 1. Content-Free Bullets

```text
# BAD - Bullet says nothing specific
- Improve user experience
- Enhance performance
- Ensure security
- Optimize workflow

# GOOD - Each bullet is actionable and specific
- Add auto-save every 30 seconds to prevent data loss
- Cache API responses for 5 minutes to reduce latency by 60%
- Implement rate limiting (100 req/min) to prevent abuse
- Replace 4-click export flow with single-action download button
```

### 2. Safe Middle-Ground (No Recommendation)

```text
# BAD - Lists options without commitment
"Consider both monolith and microservices architectures.
 Each has trade-offs. The choice depends on your specific needs."

# GOOD - Makes a clear recommendation with reasoning
"Recommendation: Start with a modular monolith.

Why: Your team of 3 developers can't justify microservices overhead.
     A modular monolith gives 80% of the organizational benefits
     while avoiding network complexity and deployment coordination.

When to revisit: If team grows past 10 OR monthly deploys exceed 50."
```

### 3. Buzzword Density (Max 2 per paragraph)

```text
BUZZWORDS = [
  "synergy", "leverage", "paradigm", "holistic", "robust",
  "scalable", "innovative", "cutting-edge", "best-in-class",
  "world-class", "next-generation", "game-changing", "disruptive",
  "seamless", "frictionless", "end-to-end", "360-degree",
  "синергия", "левередж", "парадигма", "холистический", "инновационный"
]

# Rule: If paragraph contains >2 buzzwords, rewrite with specifics

# BAD
"Our innovative, cutting-edge solution leverages synergies
 to deliver a seamless, holistic, best-in-class experience."

# GOOD
"Our notification system sends alerts in <100ms using WebSockets,
 with 99.9% delivery rate across mobile and desktop."
```

---

## Quality Rules

### Rule 1: Specific > Generic

```text
REPLACE generic nouns with specific ones:

| Generic | Specific (example) |
|---------|-------------------|
| users | "Marketing Manager Maria" |
| system | "payment processing API" |
| process | "invoice approval workflow" |
| data | "customer purchase history" |
| solution | "real-time inventory sync" |
| platform | "Shopify integration layer" |
| stakeholders | "CFO and Head of Sales" |
```

### Rule 2: Bold > Safe

```text
COMMIT to a recommendation. Don't just list options.

BAD: "There are several approaches to consider..."
GOOD: "Use PostgreSQL for this use case. Here's why..."

BAD: "The best choice depends on your needs."
GOOD: "For <50K users: SQLite. For 50K-1M: PostgreSQL. For >1M: Cassandra."
```

### Rule 3: Concrete > Abstract

```text
INCLUDE numbers, dates, names wherever possible.

BAD: "Response times will improve significantly."
GOOD: "P95 latency drops from 800ms to 120ms."

BAD: "We'll deliver this soon."
GOOD: "MVP ships January 15. Full release February 28."

BAD: "Several team members will be involved."
GOOD: "Alice (frontend), Bob (backend), and Carol (QA) own this feature."
```

### Rule 4: Direct > Hedged

```text
REMOVE uncertainty unless genuinely uncertain.

BAD: "This might potentially help with..."
GOOD: "This solves..." OR "This reduces X by Y%"

BAD: "Users may or may not prefer this approach."
GOOD: "User research shows 73% prefer this approach."
  OR: "We need user testing to validate preference."
```

### Rule 5: Fresh > Cliché

```text
REWRITE any phrase that sounds like generic AI output.

Test: Would this sentence appear in 1000 other AI-generated docs?
If yes → Rewrite with project-specific details.

BAD: "In today's digital landscape, user experience is paramount."
GOOD: "Our checkout abandonment rate is 68% — 23% higher than industry average.
       The culprit: 7 form fields where competitors use 3."
```

---

## Integration

### Import in Commands

Add to the top of artifact-generating commands:

```text
## Quality Rules

IMPORT: templates/shared/quality/anti-slop.md

APPLY anti-slop rules to ALL prose content:
- Check against FORBIDDEN_OPENINGS before writing any section
- Check against HEDGE_PHRASES and replace with commitments
- Verify BUZZWORD_DENSITY < 2 per paragraph
- Apply QUALITY_RULES to each section
```

### Self-Review Checks

```text
ANTI_SLOP_CHECKS = [
  {
    id: "SR-SLOP-01",
    name: "Forbidden Phrases",
    severity: MEDIUM,
    auto_fixable: true,
    check: SCAN_FOR(FORBIDDEN_OPENINGS + FORBIDDEN_CONCLUSIONS)
  },
  {
    id: "SR-SLOP-02",
    name: "Hedge Phrase Density",
    severity: LOW,
    auto_fixable: true,
    check: COUNT(HEDGE_PHRASES) / SECTION_COUNT < 2
  },
  {
    id: "SR-SLOP-03",
    name: "Specificity Check",
    severity: HIGH,
    auto_fixable: false,
    check: FLAG_GENERIC_TERMS(["users", "system", "process", "data"])
  },
  {
    id: "SR-SLOP-04",
    name: "Buzzword Density",
    severity: MEDIUM,
    auto_fixable: false,
    check: BUZZWORDS_PER_PARAGRAPH <= 2
  },
  {
    id: "SR-SLOP-05",
    name: "Recommendation Present",
    severity: HIGH,
    auto_fixable: false,
    check: DECISION_SECTIONS_HAVE_RECOMMENDATION
  }
]
```

---

## Examples

### Before/After: Feature Description

**Before (Slop):**
> In today's fast-paced world, it's important to note that users need a seamless,
> frictionless experience. Our innovative solution leverages cutting-edge technology
> to deliver a holistic, end-to-end platform. The system might potentially improve
> user satisfaction. In conclusion, this feature is important for various stakeholders.

**After (Quality):**
> Marketing teams waste 4 hours/week copying data between Salesforce and Mailchimp.
> This sync feature eliminates manual copying by auto-syncing contacts every 15 minutes.
> Expected impact: Save 200+ hours/year per team. Reduce data entry errors by 90%.

### Before/After: Technical Decision

**Before (Slop):**
> When it comes to database selection, there are several options to consider.
> Both SQL and NoSQL have their trade-offs. The best choice depends on your
> specific requirements. Generally speaking, it's important to evaluate scalability,
> consistency, and other factors.

**After (Quality):**
> **Recommendation: PostgreSQL 15**
>
> Why this choice:
> - Our data is relational (orders → customers → products)
> - Transaction integrity is critical (payments)
> - Team has PostgreSQL experience (0 learning curve)
>
> Why not alternatives:
> - MongoDB: Would require denormalization, increasing data inconsistency risk
> - MySQL: Lacks JSON support we need for flexible product attributes
> - DynamoDB: Overkill for our 10K daily transactions
