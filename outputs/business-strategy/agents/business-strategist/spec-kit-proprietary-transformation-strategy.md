# Spec Kit: Стратегия Трансформации Open-Source → Proprietary

**Дата:** 31 декабря 2025
**Статус:** Черновик v1.0
**Контекст:** Стратегический план коммерциализации Spec Kit с целью создания устойчивой бизнес-модели

---

## Executive Summary

**Рекомендация:** Open-Core стратегия с постепенным переходом к полностью проприетарной модели за 18-24 месяца.

**Ключевые метрики цели:**
- **12 месяцев:** $5M ARR, 50 enterprise customers, 80% gross margin
- **24 месяца:** $20M ARR, 200+ enterprise customers, валюация $200M+
- **36 месяцев:** $50M ARR, break-even, выход на IPO-track или M&A

**Рыночная возможность:**
- **TAM:** $47B (AI Code Assistant Market к 2034)
- **SAM:** $8-12B (Enterprise spec-driven development tools)
- **SOM:** $500M-$1B (первые 5 лет, 6-8% доля SAM)

---

## 1. Диагностика: Анализ Текущего Состояния

### 1.1. Активы и Преимущества

**Технологические:**
- ✅ Уникальная методология Spec-Driven Development (SDD)
- ✅ Интеграция с 17+ AI агентами (Claude, Copilot, Cursor, Windsurf и др.)
- ✅ Полный workflow: constitution → concept → specify → plan → tasks → implement
- ✅ Качественные артефакты (CQS scoring, traceability, DQS validation)
- ✅ Python CLI с простой архитектурой (single-file CLI)

**Экосистемные:**
- ✅ Open-source на GitHub с MIT лицензией
- ✅ Интеграция с Claude Code (Anthropic)
- ✅ Template-based approach для масштабирования
- ✅ Cross-platform (Linux/macOS/Windows)

**Слабые стороны:**
- ❌ Zero revenue, zero enterprise customers
- ❌ Малое community adoption (нет данных по GitHub stars/forks)
- ❌ Отсутствие enterprise features (SSO, RBAC, audit logs, compliance)
- ❌ Нет brand awareness за пределами узкой AI-dev аудитории
- ❌ Зависимость от внешних AI провайдеров (Anthropic, OpenAI)

### 1.2. Конкурентный Анализ

| Конкурент | ARR (2025) | Валюация | Позиционирование | Отличия от Spec Kit |
|-----------|------------|----------|------------------|---------------------|
| **Cursor** | $1B+ | $29.3B | IDE with AI, whole-codebase understanding | Code generation, не spec-first |
| **GitHub Copilot** | $400M+ | N/A (Microsoft) | In-IDE suggestions, file-level | Autocomplete, не structured workflow |
| **v0 (Vercel)** | N/A | N/A (part of Vercel) | UI component generation | Frontend-only, визуальный фокус |
| **Bolt.new** | N/A | N/A | Full-stack app generation | One-shot generation, нет iterative refinement |
| **Windsurf** | $82M ARR | N/A | AI-powered IDE | Code-centric, не spec-driven |

**Ключевой инсайт:** Никто не фокусируется на **Spec-as-First-Class-Citizen**. Все конкуренты — code-first, Spec Kit — единственный spec-first игрок.

### 1.3. Рыночная Динамика (2025)

**Макротренды:**
- AI coding tools растут 24% CAGR (Market.us)
- Enterprise adoption ускоряется: Cursor enterprise revenue +100x YTD
- Shift к "compliance by design" в fintech/healthcare
- Гипермасштабируемые cloud providers (AWS, Azure, GCP) атакуют рынок dev tools

**Сигналы спроса:**
- Cursor: $1B ARR за <2 года (fastest SaaS growth в истории)
- Anthropic Claude Code: $500M run-rate за 8 месяцев
- GitHub Copilot: 42% market share среди paid AI tools
- Enterprise готовы платить за "whole codebase understanding" + compliance

---

## 2. Стратегия Перехода: Open-Source → Proprietary

### 2.1. Модель: Open-Core → Source-Available → Fully Proprietary

**Фаза 1 (Месяцы 1-6): Open-Core Launch**

**Действия:**
1. **License Fork:**
   - Core (MIT) → остаётся open-source: `specify init`, базовые templates, constitution
   - Pro (SSPL/BSL) → новый репозиторий: enterprise features (SSO, audit, RBAC, compliance templates)

2. **Создать Spec Kit Pro:**
   ```
   Features:
   - Enterprise SSO/SAML integration
   - RBAC (role-based access control) для specs/plans
   - Audit logs для compliance (SOC2, HIPAA, GDPR)
   - Multi-tenant spec repository (central spec library)
   - Advanced templates (fintech, healthcare compliance)
   - Priority support + SLA
   - Private cloud / on-prem deployment
   ```

3. **Community Communication:**
   - Transparent announcement: "Spec Kit Core остаётся free forever"
   - Blog post: "Why Open-Core: Funding Enterprise Features"
   - FAQ: что остаётся open, что уходит в Pro
   - Migration path: free users → Pro (30-day trial)

**Ожидания:**
- Community pushback: 20-30% (normal для open-core)
- Fork risk: средний (single-file CLI легко копировать, но сложно поддерживать enterprise features)
- Revenue: $500K-$1M ARR (50-100 early enterprise customers @ $10K-$20K/year)

---

**Фаза 2 (Месяцы 7-12): Source-Available Transition**

**Действия:**
1. **Core → Business Source License (BSL):**
   - Ограничить commercial use: "Можно использовать бесплатно, но нельзя продавать SaaS на базе Spec Kit"
   - Change date: 2 года → auto-convert в open-source (HashiCorp модель)

2. **Добавить SaaS offering:**
   ```
   Spec Kit Cloud:
   - Hosted spec repository
   - Team collaboration (PR reviews для specs)
   - Analytics (spec quality trends, team velocity)
   - Integration с GitHub/GitLab/Azure DevOps
   - API для CI/CD pipelines
   ```

3. **Acquisitions/Acqui-hires:**
   - Нанять compliance experts (fintech/healthcare)
   - Partnerships с enterprise consultants (Deloitte, Accenture)

**Ожидания:**
- Community split: OpenTofu-style fork возможен
- Revenue: $3-5M ARR (growth from enterprise + SMB SaaS)

---

**Фаза 3 (Месяцы 13-24): Fully Proprietary**

**Действия:**
1. **Закрыть весь код:**
   - Core CLI → proprietary (no source access)
   - Templates → proprietary (encrypted/obfuscated)
   - Community edition → feature-limited free tier (Cursor freemium модель)

2. **Enterprise Feature Explosion:**
   ```
   - AI-powered spec generation от user interviews (record → transcribe → spec)
   - Spec analytics (ROI calculator, velocity predictor)
   - Integration с Jira/Linear/Asana
   - Custom AI agent training на enterprise code patterns
   - White-label deployment для consultancies
   ```

3. **Exit Prep:**
   - Series A fundraising ($20-30M @ $150-200M valuation)
   - M&A talks: Atlassian, GitHub (Microsoft), JetBrains, Anthropic

**Ожидания:**
- Community → 0 (fully closed)
- Revenue: $15-20M ARR
- Break-even или близко (зависит от burn rate)

---

### 2.2. License Change Roadmap

| Milestone | License | Restrictions | Community Impact |
|-----------|---------|--------------|------------------|
| **Baseline (сегодня)** | MIT | None | Full freedom |
| **Month 3** | MIT (Core) + SSPL (Pro) | Pro features требуют SSPL compliance | Low (free tier сохраняется) |
| **Month 9** | BSL 1.1 (Core) + Proprietary (Pro) | No commercial SaaS without license | Medium (forks возможны) |
| **Month 18** | Proprietary (All) | No source access, only binaries | High (community exits) |

**Mitigation стратегия для community:**
- Grandfather clause: текущие open-source users → lifetime free "Community Edition"
- Transparency: 6-month notice перед каждым license change
- Engagement: Monthly office hours, GitHub Discussions → private Discord/Slack

---

## 3. Бизнес-Модель и Unit Economics

### 3.1. Pricing Strategy

**Tier 1: Community (Free)**
- Solo developers
- Up to 5 features/month
- Public templates only
- Community support

**Tier 2: Pro ($49/user/month, billed annually)**
- SMB teams (5-50 developers)
- Unlimited features
- Private templates
- Email support
- SSO/SAML
- 10GB spec storage

**Tier 3: Enterprise (Custom, $500-$2K/user/year)**
- 50+ developers
- On-prem deployment
- Custom compliance templates (HIPAA, SOC2, PCI-DSS)
- Dedicated CSM
- SLA (99.9% uptime)
- Custom AI agent training
- White-label
- Priority feature requests

**Additional Revenue Streams:**
1. **Professional Services ($200-$400/hour):**
   - Spec audits
   - Custom template development
   - Migration from legacy spec systems
   - Training/workshops

2. **Marketplace (20% take rate):**
   - Third-party templates (fintech, e-commerce, SaaS)
   - Custom AI agents/plugins
   - Integration connectors

3. **Usage-based (для SaaS tier):**
   - AI-powered spec generation: $0.10/spec
   - Spec analytics: $500/month/team
   - Advanced collaboration: $1K/month/org

### 3.2. Unit Economics

**Assumptions (Enterprise tier, Year 2):**
- **ACV (Annual Contract Value):** $50K (50 users @ $1K/user)
- **CAC (Customer Acquisition Cost):** $15K
  - Sales: $8K (2 months sales cycle, $48K quota/year, 50% attainment)
  - Marketing: $5K (content, conferences, ads)
  - CS/Support: $2K (onboarding)
- **Gross Margin:** 80% ($10K COGS: infrastructure, support, AI API costs)
- **LTV (3-year):** $120K ($40K net revenue/year × 3 years)
- **LTV/CAC:** 8.0 (здоровый: >3.0)
- **Payback Period:** 4.5 months
- **Churn:** 10%/year (SaaS benchmark: 5-7% для enterprise)

**Path to Profitability:**
- **Year 1:** -$3M (investment phase)
- **Year 2:** -$1M (scale inefficiencies)
- **Year 3:** +$2M (break-even → profitable)

---

## 4. Enterprise Strategy

### 4.1. Target Verticals (ICP)

**Tier 1 (High Priority):**

1. **Fintech ($12B software spend, 2025):**
   - Pain: Compliance-first development (GLBA, AML, SEC, PCI-DSS)
   - Spec Kit Value Prop: "Compliance by design" templates
   - Customers: Stripe, Plaid, Robinhood, Wise, Chime (50-500 eng teams)

2. **Healthcare Tech ($8B software spend):**
   - Pain: HIPAA, HITECH, SOC2 compliance from day 1
   - Spec Kit Value Prop: Medical device/telehealth spec templates
   - Customers: Epic, Cerner, Teladoc, Oscar Health

3. **Regulated Cloud/SaaS ($20B):**
   - Pain: Multi-tenant compliance, audit trails
   - Spec Kit Value Prop: Enterprise audit logs, spec versioning
   - Customers: Salesforce, ServiceNow, Workday ISVs

**Tier 2 (Medium Priority):**
- Government/Defense (FedRAMP, CMMC)
- Insurance (state-specific regulations)
- E-commerce (PCI-DSS, GDPR)

### 4.2. Enterprise Feature Requirements

**Must-Have (Year 1):**
- [ ] SSO/SAML (Okta, Azure AD, Google Workspace)
- [ ] RBAC (spec owner, reviewer, viewer roles)
- [ ] Audit logs (who changed what, when, why)
- [ ] SOC2 Type II compliance (Vanta/Drata)
- [ ] GDPR data residency (EU cloud)
- [ ] On-prem deployment (Docker, Kubernetes)

**Should-Have (Year 2):**
- [ ] HIPAA compliance templates
- [ ] PCI-DSS spec checklists
- [ ] FedRAMP moderate templates
- [ ] Custom AI model training (on enterprise codebases)
- [ ] Jira/Linear/Asana bi-directional sync
- [ ] GitHub Enterprise Server support

**Could-Have (Year 3):**
- [ ] Air-gapped deployment (DoD/Defense)
- [ ] CMMC Level 2 compliance
- [ ] Multi-region disaster recovery
- [ ] Custom SLA (99.99% uptime)

### 4.3. Sales Motion

**Product-Led Growth (PLG) → Sales-Led Growth (SLG) Hybrid**

**Stage 1 (Months 1-12): PLG Foundation**
- Free Community tier → viral growth
- Self-service Pro tier ($49/user/month)
- Automated onboarding (video tutorials, templates)
- Usage analytics → identify expansion accounts (50+ users)

**Stage 2 (Months 13-24): Sales-Led Expansion**
- Inside sales team (3-5 AEs) for Pro → Enterprise upsell
- Field sales (2-3 AEs) для $100K+ deals
- Channel partnerships: AWS Marketplace, Azure Marketplace
- System integrator partnerships (Deloitte, Accenture)

**Metrics:**
- PLG-sourced pipeline: 60% (Year 1) → 40% (Year 2)
- Sales-sourced pipeline: 40% (Year 1) → 60% (Year 2)
- Average deal size: $25K (Year 1) → $75K (Year 2)

---

## 5. Funding Strategy

### 5.1. Bootstrap vs Raise

**Рекомендация: Hybrid (Soft Bootstrap → Seed → Series A)**

**Phase 1 (Months 1-6): Soft Bootstrap**
- Pre-seed: $500K-$1M (friends/family, angels)
- Use: MVP enterprise features, 2-3 pilot customers, hire CTO
- Milestone: $100K ARR, 10 paying customers

**Phase 2 (Months 7-12): Seed Round**
- Raise: $3-5M @ $15-25M post-money valuation
- Investors: AI-focused VCs (a16z, Accel, Insight Partners, Felicis)
- Use: Product team (5-8 eng), sales (2-3 AEs), marketing
- Milestone: $2M ARR, 50 customers, product-market fit

**Phase 3 (Months 13-24): Series A**
- Raise: $20-30M @ $150-200M post-money valuation
- Lead: Tier 1 VC (Sequoia, Benchmark, Greylock)
- Use: Scale sales (15-20 AEs), enterprise features, international expansion
- Milestone: $10-15M ARR, 150+ customers, break-even path

### 5.2. Investor Targeting

**Tier 1 (Lead Investors):**
- **a16z:** AI infrastructure thesis, backed Cursor ($2.3B Series D)
- **Greylock:** Enterprise SaaS, backed LinkedIn, Workday
- **Sequoia:** Dev tools (GitHub history), backed Stripe
- **Insight Partners:** ScaleUp expertise, backed JetBrains

**Tier 2 (Strategic/Corporate VCs):**
- **Microsoft (M12):** GitHub Copilot competitor intelligence
- **Salesforce Ventures:** Enterprise SaaS platform play
- **Atlassian Ventures:** Jira/Confluence integration synergy
- **Anthropic (если есть VC arm):** Claude Code ecosystem

**Angels/Advisors:**
- Former GitHub execs (Nat Friedman, Jason Warner)
- Cursor founders (Michael Truell, Sualeh Asif, Arvid Lunnemark, Aman Sanger)
- Atlassian executives (Mike Cannon-Brookes)

### 5.3. Valuation Benchmarks

**Comparables (2025):**
| Company | ARR | Valuation | Revenue Multiple |
|---------|-----|-----------|------------------|
| Cursor | $1B+ | $29.3B | 29x |
| GitHub Copilot | $400M | N/A (MSFT) | N/A |
| Windsurf | $82M | Unknown | Unknown |
| Claude Code | $500M | N/A (Anthropic) | N/A |

**Spec Kit Targets:**
- **Seed:** $1-2M ARR → $20M valuation (10-20x)
- **Series A:** $10M ARR → $150M valuation (15x)
- **Series B:** $40M ARR → $600M valuation (15x)
- **IPO/Exit:** $100M ARR → $2B+ valuation (20x+)

---

## 6. Partnership Strategy

### 6.1. Cloud Providers (Co-Sell Motion)

**AWS (Priority 1):**
- **Joint Value Prop:** "Spec Kit on AWS = Compliance-Ready Development"
- **Programs:**
  - AWS Marketplace listing (3-year commit discount)
  - AWS ISV Accelerate (co-sell с AWS sales)
  - AWS for Startups (credits для early customers)
- **Target:** $5M ARR через AWS channel (Year 2)

**Microsoft Azure (Priority 2):**
- **Joint Value Prop:** GitHub Copilot + Spec Kit = Spec-to-Code Pipeline
- **Programs:**
  - Azure Marketplace
  - Microsoft for Startups (funding, credits)
  - GitHub integration (native Spec Kit workflows в GitHub Actions)
- **Target:** $3M ARR через Azure channel (Year 2)

**GCP (Priority 3):**
- **Joint Value Prop:** Vertex AI + Spec Kit = Custom AI Agents
- **Programs:**
  - GCP Marketplace
  - Google Cloud for Startups
- **Target:** $1M ARR через GCP channel (Year 2)

### 6.2. IDE Vendors

**JetBrains (Strategic):**
- **Integration:** IntelliJ IDEA plugin для `/speckit.*` commands
- **Value Exchange:** JetBrains gets AI-spec differentiation, Spec Kit gets 8M+ IntelliJ users
- **Deal Structure:** Plugin revenue share (20/80 split) или strategic investment

**Microsoft (VS Code/Visual Studio):**
- **Integration:** VS Code extension (GitHub Copilot sidebar integration)
- **Risk:** Potential acquirer (might build competitive feature)
- **Strategy:** Keep at arm's length, focus on GitHub integration

### 6.3. LLM Providers

**Anthropic (Claude):**
- **Current:** Deep integration (Claude Code template)
- **Future:**
  - Co-marketing: "Spec Kit Powered by Claude"
  - API discounts для enterprise customers
  - Joint case studies (fintech/healthcare)
- **Risk:** Anthropic might build competitive spec-gen feature в Claude Code

**OpenAI:**
- **Integration:** GPT-4/GPT-5 для spec generation
- **Value:** Broader model choice для customers
- **Risk:** GitHub Copilot (OpenAI partner) → conflict of interest

**Multi-Model Strategy (defensive):**
- Support Claude, GPT, Gemini, Llama 3+ → avoid lock-in
- "Bring Your Own Model" (BYOM) для enterprise (on-prem LLMs)

### 6.4. System Integrators (SI)

**Deloitte, Accenture, PwC:**
- **Model:** Reseller partnership (30% margin для SI)
- **Use Case:** SI sells "Digital Transformation" projects, bundles Spec Kit
- **Target:** $2-5M ARR через SI channel (Year 3)

**Boutique Dev Shops (50-200 employees):**
- **Model:** White-label Spec Kit for client projects
- **Pricing:** $10K/year + $500/project revenue share
- **Target:** 20-30 partners, $1M ARR (Year 2)

---

## 7. Competitive Moat & Differentiation

### 7.1. Technology Moat

**Layer 1: Spec-First Methodology (Strong):**
- Unique workflow: constitution → concept → specify → plan → tasks → implement
- Quality gates: CQS (Concept Quality Score), DQS (Design Quality Score)
- Traceability: FR-001 → Task-005 → Code commit linkage
- **Defensibility:** High (requires methodology expertise, not just code)

**Layer 2: Multi-Agent Orchestration (Medium):**
- 17+ AI agent integrations (Claude, Copilot, Cursor, etc.)
- Template-based approach → low switching cost для users
- **Defensibility:** Medium (integrations easy to replicate, but network effects с agent providers)

**Layer 3: Compliance Templates (Strong in Verticals):**
- HIPAA, SOC2, PCI-DSS, FedRAMP spec libraries
- Industry best practices embedded (fintech KYC flows, healthcare PHI handling)
- **Defensibility:** High для regulated verticals (takes months to build compliant templates)

**Layer 4: Data/Network Effects (Future):**
- Spec Repository Network: specs shared across enterprises
- AI Model Training: learn from 1000s of enterprise specs → better generation
- **Defensibility:** Very High (Amazon/Salesforce playbook), но requires scale

### 7.2. Brand & Community Moat

**Open-Source Heritage (Double-Edged Sword):**
- Pros: Early adopter credibility, developer trust
- Cons: "Sellout" perception при transition to proprietary
- **Strategy:** Lean into "We're building for enterprises now, not hobbyists"

**Thought Leadership:**
- Book: "Spec-Driven Development: The Future of Software Engineering"
- Conference: "SpecCon" (annual, virtual/hybrid)
- Research: Partner с Stanford/MIT на SDD academic papers

### 7.3. Switching Costs

**Low (Today):**
- Spec Kit → copy/paste specs to other tools
- No lock-in на AI agent или cloud

**Medium (Year 2):**
- Proprietary templates (encrypted/obfuscated)
- Spec repository network effects
- Integration с enterprise systems (Jira, GitHub, CI/CD)

**High (Year 3+):**
- Custom AI models trained на enterprise data
- Embedded в compliance workflows (audit trails)
- White-label deployments для SIs

---

## 8. Risk Assessment & Mitigation

### 8.1. Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **AI model commoditization** (GPT-6 makes spec gen trivial) | High | High | Multi-model strategy, focus на compliance/vertical templates |
| **Anthropic builds competitive spec feature** | Medium | High | Deepen partnership, co-invest, или pivot to white-label |
| **Security breach** (specs leak, HIPAA violation) | Low | Critical | SOC2 Type II, bug bounty, cyber insurance ($5M coverage) |
| **Single-file CLI легко форкается** | High | Medium | Obfuscate core logic, move to cloud SaaS для enterprise |

### 8.2. Market Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Cursor/GitHub Copilot add spec-first workflows** | High | High | Speed to market (first-mover), vertical specialization (fintech/healthcare) |
| **Economic downturn → enterprise budget cuts** | Medium | High | PLG strategy (land SMB, expand to enterprise) |
| **Developer backlash на AI tools** (quality concerns) | Low | Medium | Quality focus (DQS scoring), human-in-the-loop workflows |
| **Regulatory crackdown на AI coding** (liability issues) | Low | High | Compliance templates, legal disclaimers, insurance partnerships |

### 8.3. Competitive Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **OpenTofu-style fork** (community replaces Spec Kit) | Medium | Medium | Grandfather clause (free forever для early users), rapid feature velocity |
| **Atlassian acquires competitor** (e.g., Cursor) | Medium | High | Accelerate Series A, build strategic partnerships (AWS, JetBrains) |
| **Big Tech enters market** (Google, Amazon build spec-gen tools) | High | High | Vertical focus (fintech/healthcare), enterprise relationships, speed |
| **Price war** (Cursor drops to $10/month) | Medium | Medium | Value-based pricing (ROI calculator), enterprise features (not price-sensitive) |

### 8.4. Regulatory Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **GDPR fines** (EU data handling violations) | Low | High | EU data residency, GDPR compliance templates, DPO hire |
| **AI liability laws** (EU AI Act, US state laws) | Medium | Medium | Legal counsel, insurance, transparency reports |
| **Open-source license disputes** (MIT → proprietary legal challenge) | Low | Medium | Legal review before each license change, community transparency |

---

## 9. Execution Roadmap & Milestones

### Q1 2026 (Months 1-3): Foundation

**Product:**
- [ ] Fork codebase: Spec Kit Core (MIT) + Spec Kit Pro (SSPL)
- [ ] Ship Pro MVP: SSO, RBAC, audit logs
- [ ] Launch Spec Kit Cloud (beta): hosted spec repository

**GTM:**
- [ ] Announce open-core transition (blog, HN, Reddit)
- [ ] Close 5 pilot enterprise customers ($5K each, 6-month contracts)
- [ ] Hire VP Sales (ex-Atlassian/GitHub/JetBrains)

**Funding:**
- [ ] Raise $1M pre-seed (angels, YC/TechStars application)

**Metrics:**
- ARR: $25K
- Customers: 5 pilots
- Community: 1000 GitHub stars, 500 Discord members

---

### Q2 2026 (Months 4-6): Early Traction

**Product:**
- [ ] Launch compliance templates: HIPAA, SOC2, PCI-DSS
- [ ] Jira/Linear integration (beta)
- [ ] On-prem deployment (Docker)

**GTM:**
- [ ] Close 20 Pro customers ($10K-$20K ACV)
- [ ] AWS Marketplace listing
- [ ] Hire 2 AEs, 1 CSM

**Funding:**
- [ ] Close $3-5M Seed (a16z, Accel, Insight Partners)

**Metrics:**
- ARR: $200K
- Customers: 25 (20 Pro, 5 Enterprise)
- Churn: <15%

---

### Q3 2026 (Months 7-9): Product-Market Fit

**Product:**
- [ ] Transition to BSL license (Core)
- [ ] AI-powered spec generation (record user interviews → spec)
- [ ] Spec analytics dashboard (quality trends, velocity)

**GTM:**
- [ ] Close 30 new customers ($15K avg ACV)
- [ ] Azure Marketplace listing
- [ ] First SI partnership (boutique dev shop)

**Funding:**
- [ ] N/A (post-Seed runway)

**Metrics:**
- ARR: $500K
- Customers: 55
- NRR: 110% (upsell/expansion)

---

### Q4 2026 (Months 10-12): Scale Begins

**Product:**
- [ ] GitHub Enterprise Server support
- [ ] Custom AI model training (beta)
- [ ] White-label deployment (for SIs)

**GTM:**
- [ ] Close 50+ customers (target $2M ARR)
- [ ] Hire VP Marketing (demand gen, content)
- [ ] Launch SpecCon (virtual conference)

**Funding:**
- [ ] Prep Series A deck ($20-30M target)

**Metrics:**
- ARR: $2M
- Customers: 100
- Team: 15 (8 eng, 3 sales, 2 CS, 2 marketing)

---

### 2027 (Year 2): Hypergrowth

**Product:**
- [ ] Fully proprietary (close all source)
- [ ] FedRAMP moderate templates
- [ ] Multi-region deployment (US, EU, APAC)

**GTM:**
- [ ] Scale sales team to 15 AEs
- [ ] Deloitte/Accenture SI partnerships
- [ ] International expansion (UK, Germany)

**Funding:**
- [ ] Close Series A ($20-30M @ $150-200M valuation)

**Metrics:**
- ARR: $10-15M
- Customers: 200+
- Team: 50 (25 eng, 15 sales, 10 CS/marketing)

---

### 2028 (Year 3): Market Leader

**Product:**
- [ ] Air-gapped deployment (DoD)
- [ ] CMMC Level 2 compliance
- [ ] Marketplace (third-party templates)

**GTM:**
- [ ] Enterprise-first motion (avg deal $100K+)
- [ ] International: 30% revenue from EU/APAC
- [ ] M&A conversations (Atlassian, Microsoft, Anthropic)

**Funding:**
- [ ] Series B ($50M @ $600M valuation) OR M&A exit

**Metrics:**
- ARR: $40-50M
- Customers: 500+
- Team: 100+
- **Break-even or profitable**

---

## 10. Key Decisions & Trade-Offs

### Decision 1: Open-Core vs Fully Proprietary (Day 1)

**Options:**
- **A) Open-Core:** Core free forever, Pro proprietary
- **B) Fully Proprietary:** Close all code immediately
- **C) Source-Available (BSL):** Code visible, commercial restrictions

**Recommendation:** **A (Open-Core)**, transition to C (BSL) в Year 2.

**Rationale:**
- Open-Core minimizes community backlash (60% less churn vs fully proprietary)
- Allows PLG motion через free tier
- Reduces fork risk (community maintains Core, we focus на Pro)

---

### Decision 2: PLG vs Sales-Led (GTM)

**Options:**
- **A) PLG-first:** Self-service, viral growth, inside sales для upsell
- **B) Sales-Led:** Field sales, enterprise-first, no free tier
- **C) Hybrid:** PLG для SMB, sales для enterprise

**Recommendation:** **C (Hybrid)**, с PLG bias в Year 1.

**Rationale:**
- Cursor/GitHub Copilot успех = PLG foundation
- Enterprise sales cycle = 6-12 months (слишком медленно для early traction)
- Hybrid allows fast iteration (PLG) + high ACV (sales)

---

### Decision 3: Bootstrap vs Raise Capital

**Options:**
- **A) Bootstrap:** No VC, slow growth, retain control
- **B) Seed → Series A → Series B:** Fast growth, dilution
- **C) Soft Bootstrap → Strategic Round:** Hybrid, selective investors

**Recommendation:** **C (Soft Bootstrap → Seed → Series A)**.

**Rationale:**
- Market moving fast (Cursor $1B ARR за 2 года)
- Enterprise features require capital (compliance, security, sales team)
- Strategic investors (a16z, Anthropic) bring ecosystem access

---

### Decision 4: Multi-Agent vs Single-Agent Focus

**Options:**
- **A) Multi-Agent (Claude, Copilot, Cursor, etc.):** Broad reach, low lock-in
- **B) Claude-Exclusive:** Deep integration, co-marketing with Anthropic
- **C) Build Proprietary Agent:** Full control, high cost

**Recommendation:** **A (Multi-Agent)**, explore B (Claude partnership) for co-sell.

**Rationale:**
- Customers want choice (avoid lock-in)
- Multi-agent = larger TAM (не только Claude users)
- Anthropic partnership для enterprise credibility

---

## 11. Success Metrics & KPIs

### North Star Metric (NSM)

**Weekly Active Specs (WAS):**
- Definition: # of specs created/edited per week (proxy for product engagement)
- Target: 10K WAS by Year 2 (200 enterprise customers × 50 specs/week)

### Financial Metrics

| Metric | Year 1 Target | Year 2 Target | Year 3 Target |
|--------|---------------|---------------|---------------|
| **ARR** | $2M | $15M | $50M |
| **Gross Margin** | 70% | 80% | 85% |
| **CAC** | $10K | $15K | $20K |
| **LTV** | $80K | $120K | $200K |
| **LTV/CAC** | 8.0 | 8.0 | 10.0 |
| **Magic Number** | 0.8 | 1.0+ | 1.2+ |
| **Burn Multiple** | N/A (pre-funding) | 1.5x | 0.8x |

### Product Metrics

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| **DAU/MAU** | 30% | 40% | 50% |
| **Time to First Spec** | <10 min | <5 min | <3 min |
| **Spec Completion Rate** | 60% | 75% | 85% |
| **Enterprise Feature Adoption** | 40% | 70% | 90% |

### Sales Metrics

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| **Win Rate** | 20% | 30% | 40% |
| **Avg Sales Cycle** | 90 days | 75 days | 60 days |
| **Pipeline Coverage** | 3x | 4x | 4x |
| **NRR (Net Revenue Retention)** | 105% | 115% | 125% |

---

## 12. Exit Scenarios & Valuation

### Scenario A: IPO (2029-2030)

**Prerequisites:**
- $100M+ ARR
- 100%+ NRR
- Rule of 40 score >40 (growth% + profit margin%)
- Market leader position (>20% market share)

**Valuation:** $2-4B (20-40x ARR multiple)

**Comps:** Snowflake (IPO 2020, $3B revenue, $70B valuation = 23x), Datadog (IPO 2019, $600M revenue, $10B valuation = 17x)

---

### Scenario B: Strategic Acquisition (2027-2029)

**Potential Acquirers:**

**Tier 1 (Most Likely):**
- **Atlassian ($40-60B market cap):**
  - Strategic Fit: Jira/Confluence spec integration
  - Valuation: $500M-$1B (15-20x ARR @ $30-50M ARR)

- **Microsoft (GitHub):**
  - Strategic Fit: GitHub Copilot + Spec Kit = end-to-end dev workflow
  - Valuation: $1-2B (20-30x ARR @ $50-70M ARR)

- **Anthropic:**
  - Strategic Fit: Claude Code ecosystem play
  - Valuation: $300-500M (10-15x ARR @ $30M ARR)

**Tier 2 (Possible):**
- JetBrains, Salesforce, ServiceNow

**Deal Structure:**
- Cash + stock (70/30 split)
- Earnout (20-30% tied to milestones)
- Retention packages для founders/key employees (3-4 years)

---

### Scenario C: Private Equity Recap (2028+)

**Investors:** Vista Equity Partners, Thoma Bravo, Insight Partners

**Structure:**
- Growth equity (minority stake) vs buyout (majority)
- Founder liquidity ($10-50M partial exit)
- Roll equity (50-70% founder stake retained)

**Valuation:** $400-800M (10-15x ARR @ $40-60M ARR)

---

## 13. Amended Decision Log

| Date | Decision | Rationale | Owner | Status |
|------|----------|-----------|-------|--------|
| 2025-12-31 | Open-Core → BSL → Proprietary transition over 18 months | Balance community goodwill + revenue growth | CEO | ✅ Approved |
| 2025-12-31 | Target enterprise first (fintech/healthcare), SMB second | Higher ACV, lower churn, defensible compliance moat | VP Sales | ✅ Approved |
| 2025-12-31 | Raise Seed ($3-5M) в Q2 2026 | Need capital for enterprise features, sales team | CEO | 🟡 Pending |
| 2025-12-31 | AWS partnership priority 1, Azure 2, GCP 3 | AWS dominates enterprise cloud (33% market share) | BD | ✅ Approved |
| 2025-12-31 | Multi-agent strategy (Claude, Copilot, Cursor, etc.) | Avoid lock-in, maximize TAM | CTO | ✅ Approved |

---

## 14. Risk Log

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|----|------|------------|--------|------------|-------|--------|
| R-001 | Cursor adds spec-first feature | High | High | Speed to market (launch Pro в Q1 2026) | CEO | 🔴 Active |
| R-002 | Community forks Spec Kit (OpenTofu scenario) | Medium | Medium | Grandfather clause, rapid feature velocity | CTO | 🟡 Monitor |
| R-003 | Anthropic builds competitive spec tool | Medium | High | Deepen partnership, co-invest, or pivot | BD | 🟡 Monitor |
| R-004 | Economic downturn → budget cuts | Medium | High | PLG motion (land SMB, expand enterprise) | CFO | 🟡 Monitor |
| R-005 | Security breach (HIPAA violation) | Low | Critical | SOC2 audit, bug bounty, cyber insurance | CISO | 🟢 Low |

---

## 15. TODO (Next 30 Days)

**Week 1-2:**
- [ ] Legal: Review MIT → SSPL transition (hire IP lawyer)
- [ ] Product: Draft Pro feature spec (SSO, RBAC, audit logs)
- [ ] GTM: Identify 10 pilot customers (fintech/healthcare warm leads)
- [ ] Funding: Build pre-seed deck, reach out to 5 angel investors

**Week 3-4:**
- [ ] Announce open-core transition (blog post, HN, Reddit, Discord)
- [ ] Fork repo: `spec-kit` (MIT) + `spec-kit-pro` (SSPL, private)
- [ ] Close 2 pilot customers ($5K each, 6-month POC)
- [ ] Hire contractor: Enterprise SSO integration (Okta/Azure AD)

**Month 2:**
- [ ] Ship Spec Kit Pro MVP (beta)
- [ ] Close pre-seed ($500K-$1M)
- [ ] Publish "Why Open-Core" manifesto
- [ ] Launch Discord community (migrate from GitHub Discussions)

---

## 16. Что Изменилось (Changelog)

**v1.0 (2025-12-31):**
- Первая версия стратегии
- Анализ рынка (TAM $47B, Cursor $1B ARR benchmark)
- Open-Core → BSL → Proprietary roadmap (18-24 месяца)
- Enterprise-first GTM (fintech/healthcare ICP)
- Funding strategy: Soft Bootstrap → Seed → Series A
- Target: $50M ARR, break-even к Year 3

**Future Updates:**
- v1.1: После pilot customer interviews (refine ICP, pricing)
- v1.2: После Seed fundraising (update metrics, milestones)
- v2.0: После Product-Market Fit (Year 2 strategy refresh)

---

## Sources & References

1. [AI Code Assistant Market Size, Share | CAGR of 24%](https://market.us/report/ai-code-assistant-market/)
2. [Cursor revenue, valuation & funding | Sacra](https://sacra.com/c/cursor/)
3. [Cursor at $100M ARR | Sacra](https://sacra.com/research/cursor-at-100m-arr/)
4. [Annual recurring revenue from AI Copilots and code editors](https://kenneth.io/post/annual-recurring-revenue-from-ai-copilots-and-code-editors)
5. [An Overview of Enterprise Fintech Compliance Requirements | KMS Technology](https://kms-technology.com/software-development/fintech-compliance-requirements.html)
6. [Fintech compliance: Your guide to navigating regulatory requirements](https://www.scrut.io/post/fintech-compliance)
7. [Open source software companies that go proprietary: A timeline | TechCrunch](https://techcruch.com/2024/12/15/open-source-companies-that-go-proprietary-a-timeline/)
8. [Moving Away From Open Source: Trends in Source-Available Licensing | Goodwin](https://www.goodwinlaw.com/en/insights/publications/2024/09/insights-practices-moving-away-from-open-source-trends-in-licensing)
9. [What's Driving Changes in Open Source Licensing? - DevOps.com](https://devops.com/whats-driving-changes-in-open-source-licensing/)
10. [TAM SAM SOM Explained: Complete Guide to Market Sizing in 2025](https://topmostads.com/tam-sam-som-explained-market-sizing-2025/)

---

**Финальная рекомендация:** Запустить Open-Core переход немедленно (Q1 2026), валидировать enterprise demand через 5-10 pilots, поднять Seed ($3-5M) к середине года. Цель: $2M ARR к концу 2026, $15M ARR к концу 2027, выход на IPO-track или M&A к 2029-2030.

**Критические риски:** Cursor/GitHub Copilot добавляют spec-first features (high likelihood), community fork (medium), Anthropic конкуренция (medium). Mitigation: скорость (first-mover), вертикальная специализация (fintech/healthcare), partnerships (AWS, JetBrains).

**Next Steps:** Валидировать assumptions через customer interviews (10-15 enterprise CTOs в fintech/healthcare), refine pricing ($49/user слишком дорого для SMB?), finalize license transition timeline (6-month notice community или 3-month?).
