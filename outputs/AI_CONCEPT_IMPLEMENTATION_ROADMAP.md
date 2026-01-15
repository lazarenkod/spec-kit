# AI-Augmented Concept: Implementation Roadmap

**Date**: 2026-01-01
**Purpose**: Tactical roadmap for implementing AI enhancements to `/speckit.concept`
**Owner**: Product & Engineering
**Timeline**: Q1-Q3 2026

---

## Executive Summary

This roadmap breaks down the AI-era concept evolution into **actionable sprints** with clear deliverables, success metrics, and resource requirements.

**Total Effort**: 8-12 engineering weeks (spread across 3 quarters)
**Investment**: ~$5K in API costs (development + testing)
**Expected ROI**: 10-20x time savings for users, 30-50% CQS quality improvement

---

## Phase 1: Foundation (Q1 2026) — 4 weeks

### Sprint 1.1: Multi-Agent Research Framework (2 weeks)

**Goal**: Automate market research with parallel AI agents.

**Deliverables**:

1. **Agent Orchestration Layer**:
   ```yaml
   # File: src/specify_cli/agents/orchestrator.py

   class ConceptResearchOrchestrator:
       """Manages parallel AI research agents for concept generation."""

       def __init__(self, model="sonnet-4.5"):
           self.model = model
           self.agents = []
           self.shared_memory = {}

       def add_agent(self, role, prompt_template, tools=[]):
           """Register a research agent."""
           agent = {
               "role": role,
               "prompt": prompt_template,
               "tools": tools,
               "status": "pending"
           }
           self.agents.append(agent)

       async def execute_parallel(self, user_input):
           """Execute all agents in parallel, return aggregated results."""
           tasks = [self._run_agent(agent, user_input) for agent in self.agents]
           results = await asyncio.gather(*tasks)
           return self._synthesize_results(results)

       def _synthesize_results(self, results):
           """Cross-reference findings, resolve conflicts, generate consensus."""
           # TODO: Implement synthesis logic
           pass
   ```

2. **Research Agent Prompts**:
   ```python
   # File: templates/prompts/research-agents.yaml

   market_intelligence:
     role: market-intelligence-ai
     model: sonnet-4.5
     tools: [web_search]
     prompt: |
       Research market opportunity for: {user_input}

       Tasks:
       1. TAM/SAM/SOM Calculation (bottom-up + top-down)
       2. Growth signals (VC funding, market trends)
       3. Regulatory landscape (compliance requirements)

       Requirements:
       - All numbers require ≥2 sources (cite URLs)
       - Mark estimates as [High/Medium/Low Confidence]
       - Cross-validate bottom-up vs top-down TAM

       Output format: JSON with {tam, sam, som, sources, confidence}

   competitive_intelligence:
     role: competitive-intelligence-ai
     # ... (similar structure)

   persona_researcher:
     role: persona-researcher-ai
     # ... (similar structure)
   ```

3. **Web Search Integration**:
   - Leverage existing `WebSearch` tool
   - Add rate limiting (max 5 searches per agent)
   - Implement caching (avoid duplicate searches)

4. **Evidence Validation**:
   ```python
   # File: src/specify_cli/validation/evidence.py

   class EvidenceValidator:
       """Validates AI-generated claims have sufficient sources."""

       def validate_claim(self, claim, sources):
           """Check if claim has ≥2 credible sources."""
           if len(sources) < 2:
               return {"valid": False, "reason": "Insufficient sources (<2)"}

           # Check source credibility (heuristic)
           credible = [s for s in sources if self._is_credible(s)]
           if len(credible) < 2:
               return {"valid": False, "reason": "Sources not credible"}

           return {"valid": True, "confidence": self._calculate_confidence(sources)}

       def _is_credible(self, source_url):
           """Heuristic: .edu, .gov, major research firms = credible."""
           credible_domains = [".edu", ".gov", "gartner.com", "forrester.com", "mckinsey.com"]
           return any(domain in source_url for domain in credible_domains)
   ```

**Success Metrics**:
- [ ] 4 research agents implemented (market, competitive, persona, trend)
- [ ] Parallel execution reduces research time: 8 hours → <1 hour
- [ ] Evidence validation enforces ≥2 sources for quantitative claims
- [ ] Unit tests cover agent orchestration, evidence validation

**Resources**:
- 1 senior engineer (full-time, 2 weeks)
- API costs: ~$50 (testing with 50 concepts)

---

### Sprint 1.2: Evidence-Based CQS (2 weeks)

**Goal**: Upgrade CQS to require quantitative evidence.

**Deliverables**:

1. **Enhanced CQS Scoring Logic**:
   ```python
   # File: src/specify_cli/scoring/cqs_enhanced.py

   class EnhancedCQS:
       """Evidence-based Concept Quality Score calculator."""

       EVIDENCE_REQUIREMENTS = {
           "market_validation": {
               "problem_validated": {"type": "count", "min": 5, "unit": "interviews"},
               "market_exists": {"type": "count", "min": 3, "unit": "competitors"},
               "budget_exists": {"type": "count", "min": 3, "unit": "pricing_sources"},
               "timing_right": {"type": "count", "min": 2, "unit": "trend_sources"},
           },
           "persona_depth": {
               "personas_defined": {"type": "count", "min": 2, "unit": "personas"},
               "jtbd_functional": {"type": "bool", "required": True},
               "wtp_assessed": {"type": "bool", "required": True},
           },
           # ... (other components)
       }

       def calculate(self, concept_data):
           """Calculate CQS with evidence validation."""
           scores = {}

           for component, requirements in self.EVIDENCE_REQUIREMENTS.items():
               score = self._score_component(concept_data, requirements)
               scores[component] = score

           # Weighted average
           weights = {"market_validation": 0.25, "persona_depth": 0.20, ...}
           cqs = sum(scores[k] * weights[k] for k in weights) * 100

           return {
               "cqs": round(cqs, 1),
               "components": scores,
               "evidence_gaps": self._identify_gaps(concept_data, requirements)
           }

       def _score_component(self, concept_data, requirements):
           """Score component based on evidence thresholds."""
           points_earned = 0
           points_possible = sum(req.get("points", 0) for req in requirements.values())

           for criterion, req in requirements.items():
               if self._meets_evidence_threshold(concept_data, criterion, req):
                   points_earned += req.get("points", 0)

           return points_earned / points_possible if points_possible > 0 else 0
   ```

2. **Evidence Collection Templates**:
   ```markdown
   # File: templates/shared/concept-sections/evidence-collection.md

   ## Market Validation Evidence

   ### Problem Validated
   **Requirement**: ≥5 customer interviews OR ≥100 survey responses

   Evidence:
   - [ ] Interview 1: [Name/Role] — [Date] — [Key pain point]
   - [ ] Interview 2: [Name/Role] — [Date] — [Key pain point]
   - [ ] ... (repeat for ≥5)

   OR

   - [ ] Survey: [Platform] — [Date] — [N responses] — [Summary]

   **Status**: ✅ Met (5 interviews) | ⚠️ Partial (3 interviews) | ❌ Not met

   ### Market Exists
   **Requirement**: ≥3 competitors with public pricing OR VC funding in space

   Evidence:
   - [ ] Competitor 1: [Name] — [Pricing URL] — [Tier structure]
   - [ ] Competitor 2: [Name] — [Pricing URL] — [Tier structure]
   - [ ] Competitor 3: [Name] — [Pricing URL] — [Tier structure]

   **Status**: ✅ Met | ⚠️ Partial | ❌ Not met
   ```

3. **CQS Dashboard Generator**:
   ```python
   # File: src/specify_cli/reporting/cqs_dashboard.py

   class CQSDashboard:
       """Generate interactive HTML dashboard for CQS visualization."""

       def generate(self, cqs_data, output_path="specs/concept-dashboard.html"):
           """Create single-file HTML dashboard with Chart.js visualizations."""

           html = f"""
           <!DOCTYPE html>
           <html>
           <head>
               <title>Concept Quality Dashboard</title>
               <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
               <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2/dist/tailwind.min.css" rel="stylesheet">
           </head>
           <body class="bg-gray-100 p-8">
               <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-lg p-8">
                   <h1 class="text-3xl font-bold mb-8">Concept Quality Score: {cqs_data['cqs']}/100</h1>

                   <!-- CQS Gauge -->
                   <div class="mb-8">
                       <canvas id="cqsGauge"></canvas>
                   </div>

                   <!-- Component Radar Chart -->
                   <div class="mb-8">
                       <canvas id="componentRadar"></canvas>
                   </div>

                   <!-- Evidence Heatmap -->
                   <div class="mb-8">
                       <h2 class="text-2xl font-bold mb-4">Evidence Quality</h2>
                       {self._generate_evidence_heatmap(cqs_data['evidence_gaps'])}
                   </div>

                   <!-- Action Items -->
                   <div>
                       <h2 class="text-2xl font-bold mb-4">Top Actions to Improve CQS</h2>
                       {self._generate_action_items(cqs_data)}
                   </div>
               </div>

               <script>
                   // Chart.js initialization
                   {self._generate_chart_js(cqs_data)}
               </script>
           </body>
           </html>
           """

           with open(output_path, 'w') as f:
               f.write(html)

           return output_path
   ```

**Success Metrics**:
- [ ] CQS calculator enforces evidence requirements
- [ ] Dashboard visualizes CQS components + gaps
- [ ] Accuracy test: AI CQS vs manual PM CQS correlation ≥ 0.80
- [ ] User testing: 5 PMs confirm dashboard is actionable

**Resources**:
- 1 senior engineer (full-time, 2 weeks)
- 1 designer (part-time, 3 days for dashboard UX)
- API costs: ~$30 (testing CQS calculation)

---

## Phase 2: AI Product Safety (Q2 2026) — 2 weeks

### Sprint 2.1: Responsible AI Assessment Framework (2 weeks)

**Goal**: Add AI ethics/safety checks for AI-powered products.

**Deliverables**:

1. **AI Product Detection**:
   ```python
   # File: src/specify_cli/detection/ai_product.py

   class AIProductDetector:
       """Detects if product concept involves AI/ML functionality."""

       AI_KEYWORDS = [
           "llm", "large language model", "gpt", "chatgpt", "claude",
           "generative ai", "ai-generated", "machine learning", "ml model",
           "recommendation engine", "personalization", "sentiment analysis",
           "computer vision", "image recognition", "speech recognition"
       ]

       def is_ai_product(self, concept_text):
           """Return True if concept mentions AI/ML functionality."""
           text_lower = concept_text.lower()
           return any(keyword in text_lower for keyword in self.AI_KEYWORDS)

       def extract_ai_features(self, concept_text):
           """Extract specific AI features mentioned in concept."""
           # Use LLM to extract AI-related features
           prompt = f"""
           Analyze this product concept and list all AI/ML features:

           {concept_text}

           Output JSON: {{"ai_features": ["feature1", "feature2"], "risk_level": "low/medium/high"}}
           """
           # ... (call LLM, parse response)
   ```

2. **Responsible AI Templates**:
   ```markdown
   # File: templates/shared/concept-sections/ai-responsibility.md

   ## AI Responsibility Assessment

   **Trigger**: Product uses AI/ML for: [list AI features from detection]

   ### 1. Fairness & Bias Testing

   | Bias Risk | Likelihood | Impact | Mitigation | Owner | Status |
   |-----------|:----------:|:------:|------------|-------|:------:|
   | Training data bias (demographic) | [1-5] | [1-5] | Diverse dataset, bias testing | ML Eng | [ ] |
   | Output bias (protected attributes) | [1-5] | [1-5] | Red-teaming, adversarial prompts | QA | [ ] |
   | Feedback loop amplification | [1-5] | [1-5] | Regular bias audits | PM | [ ] |

   **Bias Testing Plan**:
   - [ ] Test across demographics (age, gender, geography, language)
   - [ ] Measure output variance (target: <10% delta across groups)
   - [ ] Document mitigation in spec (e.g., "Constitutional AI to reduce stereotypes")

   ### 2. Transparency & Explainability

   | User Right | Implementation | Spec Story ID | Status |
   |------------|----------------|---------------|:------:|
   | Know when AI is used | "AI-generated" label on outputs | [auto-generate] | [ ] |
   | Understand how it works | "How this works" tooltip/modal | [auto-generate] | [ ] |
   | Appeal AI decisions | Human review escalation flow | [auto-generate] | [ ] |

   ### 3. Safety Red-Team Scenarios

   | Scenario | Attack Vector | Expected Harm | Mitigation | Test Status |
   |----------|---------------|---------------|------------|:-----------:|
   | Prompt injection | "Ignore previous instructions..." | System compromise | Input sanitization + output validation | [ ] |
   | PII extraction | "List training data examples" | Privacy breach | No training data in prompts, output filtering | [ ] |
   | Harmful content generation | Adversarial prompts | Reputational risk | Content moderation API (OpenAI Moderation) | [ ] |
   | Automated abuse | Bot-driven spam | Service degradation | Rate limiting, CAPTCHA | [ ] |

   **Red-Team Protocol**:
   - [ ] Before launch: ≥20 adversarial prompts tested
   - [ ] Post-launch: Weekly security testing with new attack vectors
   - [ ] Incident response: <1 hour to disable feature if critical vulnerability

   ### 4. Regulatory Compliance

   | Regulation | Applies? | Requirements | Compliance Actions | Status |
   |------------|:--------:|--------------|-------------------|:------:|
   | **EU AI Act** (2024) | Yes/No | Risk assessment, transparency, human oversight | [auto-generate checklist] | [ ] |
   | **GDPR** (EU) | Yes/No | DPIA, right to erasure, data minimization | [auto-generate checklist] | [ ] |
   | **CCPA** (California) | Yes/No | Privacy policy, opt-out, data export | [auto-generate checklist] | [ ] |

   ### 5. AI-Specific Feature Stories

   **Auto-generated stories for AI safety**:

   - [ ] **EPIC-AI.F01.S01**: Display "AI-generated" label on all AI outputs
   - [ ] **EPIC-AI.F01.S02**: Implement "Report AI issue" button for user feedback
   - [ ] **EPIC-AI.F02.S01**: Add input sanitization for prompt injection prevention
   - [ ] **EPIC-AI.F02.S02**: Integrate content moderation API for harmful content filtering
   - [ ] **EPIC-AI.F03.S01**: Build admin dashboard for bias monitoring (output variance by demographic)

   **Priority**: P1a (must ship with initial AI feature)
   ```

3. **Auto-Story Generation**:
   ```python
   # File: src/specify_cli/generators/ai_safety_stories.py

   class AISafetyStoryGenerator:
       """Generate safety-related user stories for AI products."""

       SAFETY_STORY_TEMPLATES = {
           "transparency": [
               "As a user, I want to know when content is AI-generated, so I can assess its reliability",
               "As a user, I want to understand how AI recommendations work, so I can trust the system"
           ],
           "safety": [
               "As an admin, I want to monitor AI outputs for bias, so I can maintain fairness",
               "As a user, I want to report problematic AI outputs, so the system can improve"
           ],
           "privacy": [
               "As a user, I want to opt-out of AI training data, so my privacy is protected",
               "As a user, I want to delete my AI interaction history, so I control my data"
           ]
       }

       def generate_stories(self, ai_features):
           """Generate safety stories based on AI features mentioned."""
           stories = []

           for feature in ai_features:
               risk_category = self._classify_risk(feature)
               relevant_templates = self.SAFETY_STORY_TEMPLATES.get(risk_category, [])

               for template in relevant_templates:
                   story = {
                       "id": f"EPIC-AI.F{len(stories)+1:02d}.S01",
                       "description": template,
                       "priority": "P1a",
                       "wave": 1,
                       "acceptance_criteria": self._generate_ac(template)
                   }
                   stories.append(story)

           return stories
   ```

**Success Metrics**:
- [ ] AI product detection accuracy ≥ 95% (test on 100 concepts)
- [ ] 100% of detected AI products get Responsibility Assessment section
- [ ] ≥5 safety stories auto-generated per AI feature
- [ ] User validation: 5 AI product PMs confirm checklist is comprehensive

**Resources**:
- 1 senior engineer (full-time, 2 weeks)
- 1 AI safety consultant (part-time, 5 days for checklist validation)
- API costs: ~$20

---

## Phase 3: Continuous Validation (Q3 2026) — 4 weeks

### Sprint 3.1: Competitive Monitoring (2 weeks)

**Goal**: Auto-track competitor changes, alert PM to shifts.

**Deliverables**:

1. **Competitor Snapshot System**:
   ```python
   # File: src/specify_cli/monitoring/competitive.py

   class CompetitiveMonitor:
       """Track competitor changes over time."""

       def __init__(self, snapshot_path=".speckit/competitive-snapshots/"):
           self.snapshot_path = Path(snapshot_path)
           self.snapshot_path.mkdir(parents=True, exist_ok=True)

       def capture_snapshot(self, competitor_name):
           """Scrape competitor data and store snapshot."""
           snapshot = {
               "date": datetime.now().isoformat(),
               "competitor": competitor_name,
               "features": self._extract_features(competitor_name),
               "pricing": self._extract_pricing(competitor_name),
               "user_sentiment": self._extract_sentiment(competitor_name)
           }

           snapshot_file = self.snapshot_path / f"{competitor_name}_{datetime.now():%Y%m%d}.json"
           with open(snapshot_file, 'w') as f:
               json.dump(snapshot, f, indent=2)

           return snapshot

       def detect_changes(self, competitor_name):
           """Compare latest snapshot to previous, generate diff."""
           snapshots = sorted(self.snapshot_path.glob(f"{competitor_name}_*.json"))

           if len(snapshots) < 2:
               return {"changes": [], "message": "Not enough snapshots for comparison"}

           prev_snapshot = json.load(open(snapshots[-2]))
           curr_snapshot = json.load(open(snapshots[-1]))

           changes = self._diff_snapshots(prev_snapshot, curr_snapshot)
           return changes

       def _diff_snapshots(self, prev, curr):
           """Identify meaningful changes between snapshots."""
           changes = []

           # Feature changes
           prev_features = set(prev.get("features", []))
           curr_features = set(curr.get("features", []))

           new_features = curr_features - prev_features
           removed_features = prev_features - curr_features

           if new_features:
               changes.append({
                   "type": "feature_added",
                   "impact": "high",
                   "details": list(new_features),
                   "recommendation": "Review if this affects our differentiation"
               })

           # Pricing changes
           prev_pricing = prev.get("pricing", {})
           curr_pricing = curr.get("pricing", {})

           if prev_pricing != curr_pricing:
               changes.append({
                   "type": "pricing_changed",
                   "impact": "medium",
                   "details": {"from": prev_pricing, "to": curr_pricing},
                   "recommendation": "Consider adjusting our pricing strategy"
               })

           # Sentiment changes
           prev_sentiment = prev.get("user_sentiment", 0)
           curr_sentiment = curr.get("user_sentiment", 0)
           sentiment_delta = curr_sentiment - prev_sentiment

           if abs(sentiment_delta) > 0.5:  # Significant shift
               changes.append({
                   "type": "sentiment_shift",
                   "impact": "low" if sentiment_delta > 0 else "medium",
                   "details": {"delta": sentiment_delta, "direction": "improved" if sentiment_delta > 0 else "declined"},
                   "recommendation": "Opportunity to capture frustrated users" if sentiment_delta < 0 else "Monitor competitive pressure"
               })

           return changes
   ```

2. **Monitoring CLI Command**:
   ```bash
   # Add to src/specify_cli/__init__.py

   @click.command()
   @click.option('--frequency', default='weekly', type=click.Choice(['daily', 'weekly', 'monthly']))
   def monitor_competitors(frequency):
       """Monitor competitors for changes and generate alerts."""

       # Load competitors from concept.md
       concept = load_concept()
       competitors = extract_competitors(concept)

       monitor = CompetitiveMonitor()

       for competitor in competitors:
           click.echo(f"Capturing snapshot for {competitor}...")
           snapshot = monitor.capture_snapshot(competitor)

           click.echo(f"Detecting changes for {competitor}...")
           changes = monitor.detect_changes(competitor)

           if changes.get("changes"):
               click.echo(f"⚠️  Changes detected for {competitor}:")
               for change in changes["changes"]:
                   click.echo(f"  - {change['type']}: {change['recommendation']}")

               # Generate report
               report_path = f"specs/competitive-update-{datetime.now():%Y%m%d}.md"
               generate_competitive_report(changes, report_path)
               click.echo(f"📄 Report saved: {report_path}")
   ```

3. **Alert System** (GitHub Actions integration):
   ```yaml
   # File: .github/workflows/competitive-monitoring.yml

   name: Competitive Monitoring

   on:
     schedule:
       - cron: '0 9 * * 1'  # Every Monday at 9 AM
     workflow_dispatch:  # Manual trigger

   jobs:
     monitor:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3

         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install Specify CLI
           run: pip install -e .

         - name: Run Competitive Monitoring
           run: speckit monitor-competitors --frequency weekly
           env:
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

         - name: Create Issue if Changes Detected
           if: success()
           uses: peter-evans/create-issue-from-file@v4
           with:
             title: 'Competitive Update: Changes Detected'
             content-filepath: specs/competitive-update-*.md
             labels: competitive-intelligence, needs-review
   ```

**Success Metrics**:
- [ ] Monitoring detects ≥80% of real competitor changes (test with historical data)
- [ ] False positive rate <20% (changes that don't matter)
- [ ] Alert delivery latency <24 hours (from change to notification)
- [ ] User adoption: ≥30% of projects enable monitoring (optional feature)

**Resources**:
- 1 engineer (full-time, 2 weeks)
- API costs: ~$100/month (for 10 competitors monitored weekly)

---

### Sprint 3.2: Concept Validation Command (2 weeks)

**Goal**: Enable periodic re-validation of concept assumptions.

**Deliverables**:

1. **Validation Command**:
   ```python
   # File: src/specify_cli/commands/validate_concept.py

   @click.command()
   @click.option('--full', is_flag=True, help='Re-run all research (vs incremental)')
   @click.option('--components', multiple=True, type=click.Choice(['market', 'personas', 'competitive', 'all']))
   def validate_concept(full, components):
       """Re-validate concept assumptions with fresh data."""

       if not Path("specs/concept.md").exists():
           click.echo("❌ No concept found. Run `/speckit.concept` first.")
           return

       concept = load_concept()

       # Default to all components
       if not components or 'all' in components:
           components = ['market', 'personas', 'competitive']

       click.echo(f"🔍 Validating concept components: {', '.join(components)}")

       results = {}

       if 'market' in components:
           click.echo("📊 Re-researching market data...")
           results['market'] = validate_market(concept, full_research=full)

       if 'personas' in components:
           click.echo("👥 Re-validating personas...")
           results['personas'] = validate_personas(concept, full_research=full)

       if 'competitive' in components:
           click.echo("🏆 Re-analyzing competitors...")
           results['competitive'] = validate_competitive(concept, full_research=full)

       # Generate validation report
       report = generate_validation_report(concept, results)
       report_path = f"specs/concept-validation-{datetime.now():%Y%m%d}.md"

       with open(report_path, 'w') as f:
           f.write(report)

       click.echo(f"✅ Validation complete. Report: {report_path}")

       # Show summary
       show_validation_summary(results)
   ```

2. **Validation Report Template**:
   ```markdown
   # File: templates/concept-validation-report.md

   # Concept Validation Report

   **Date**: {validation_date}
   **Original Concept**: {concept_date} ({days_since} days ago)
   **Components Validated**: {components}

   ---

   ## Summary

   | Component | Status | Changes Detected | CQS Impact | Action Required |
   |-----------|:------:|------------------|:----------:|-----------------|
   | Market | {status_icon} | {change_summary} | {delta} | {action} |
   | Personas | {status_icon} | {change_summary} | {delta} | {action} |
   | Competitive | {status_icon} | {change_summary} | {delta} | {action} |

   **Status Icons**: ✅ No major changes | ⚠️ Minor updates needed | 🔴 Significant changes

   ---

   ## Market Validation Changes

   ### TAM/SAM/SOM

   | Metric | Original | Current | Change | Source |
   |--------|----------|---------|:------:|--------|
   | TAM | ${original_tam} | ${current_tam} | {delta}% | {source} |
   | SAM | ${original_sam} | ${current_sam} | {delta}% | {source} |
   | SOM | ${original_som} | ${current_som} | {delta}% | {source} |

   **Interpretation**: {tam_interpretation}

   ### Competitive Landscape

   **New Entrants** (since last validation):
   - {new_competitor_1}: {brief_description}
   - {new_competitor_2}: {brief_description}

   **Feature Gaps Closed** (competitors caught up):
   - {feature_1}: Now offered by {competitor_name}
   - {feature_2}: Now offered by {competitor_name}

   **New Opportunities** (gaps opened):
   - {opportunity_1}: {description}

   ---

   ## CQS Re-Calculation

   | Component | Original Score | Current Score | Delta | Reason for Change |
   |-----------|:--------------:|:-------------:|:-----:|-------------------|
   | Market | {orig}/100 | {curr}/100 | {delta} | {reason} |
   | Persona | {orig}/100 | {curr}/100 | {delta} | {reason} |
   | Features | {orig}/100 | {curr}/100 | {delta} | {reason} |
   | **Total CQS** | **{orig_cqs}** | **{curr_cqs}** | **{delta_cqs}** | |

   ---

   ## Recommended Actions

   ### High Priority (CQS impact > 10 points)
   1. {action_1}
   2. {action_2}

   ### Medium Priority (CQS impact 5-10 points)
   1. {action_1}

   ### Low Priority (CQS impact < 5 points)
   1. {action_1}

   ---

   ## Next Validation

   **Recommended frequency**: {frequency} (based on market volatility)
   **Next validation due**: {next_date}
   ```

**Success Metrics**:
- [ ] Validation command detects ≥70% of real market changes (vs manual PM review)
- [ ] CQS delta accuracy ≥ 80% (automated vs manual re-calculation)
- [ ] User adoption: ≥20% of projects run validation quarterly
- [ ] Actionability: Users act on ≥50% of "High Priority" recommendations

**Resources**:
- 1 engineer (full-time, 2 weeks)
- API costs: ~$50 (testing validation on 20 concepts)

---

## Budget Summary

| Phase | Effort | Engineer Cost | API Costs | Total |
|-------|--------|--------------|-----------|-------|
| **Phase 1: Foundation** | 4 weeks | $20,000 | $80 | $20,080 |
| **Phase 2: AI Safety** | 2 weeks | $10,000 + $5,000 (consultant) | $20 | $15,020 |
| **Phase 3: Continuous Validation** | 4 weeks | $20,000 | $150 | $20,150 |
| **Total** | 10 weeks | $55,000 | $250 | **$55,250** |

**Ongoing Costs** (per month):
- Competitive monitoring: ~$100/mo (API calls)
- Concept validation (if run monthly): ~$50/mo
- **Total recurring**: ~$150/mo

**Break-Even Analysis**:
- PM time saved per concept: 6 hours × $100/hr = $600
- Cost per AI-augmented concept: ~$1 (API) + amortized dev cost
- Break-even: ~100 concepts (achievable in first 6 months if 20+ projects adopt)

---

## Risk Mitigation

### Technical Risks

**Risk 1: LLM API Rate Limits**
- **Mitigation**: Implement exponential backoff, queue system for research agents
- **Fallback**: Degrade to fewer agents (4 → 2) if rate limited

**Risk 2: Web Search Reliability**
- **Mitigation**: Cache search results (30-day TTL), retry failed searches
- **Fallback**: Manual research prompt if all searches fail

**Risk 3: Evidence Validation False Negatives**
- **Mitigation**: Human override ("I have evidence, trust me" flag)
- **Monitoring**: Track override rate (>20% = validation too strict)

### Product Risks

**Risk 4: Users Over-Trust AI**
- **Mitigation**: Prominent disclaimers, confidence levels (High/Med/Low)
- **UX**: Require PM approval for all CQS components (no auto-accept)

**Risk 5: CQS Inflation**
- **Mitigation**: Evidence requirements prevent gaming
- **Validation**: Quarterly audit of high-CQS concepts (do they succeed?)

**Risk 6: Low Adoption**
- **Mitigation**: Make AI-augmented mode opt-in (default to manual)
- **User research**: Interview PMs to understand barriers

---

## Success Criteria (Go/No-Go for GA)

**Before releasing to all users**:

1. **Accuracy**: CQS correlation with manual PM ≥ 0.80 (on 50 test concepts)
2. **Speed**: Research time reduction ≥ 70% (8 hours → <2.5 hours)
3. **Reliability**: API success rate ≥ 95% (agent execution completes)
4. **User Satisfaction**: ≥4.0/5 rating from beta testers (n ≥ 20)
5. **Safety**: 100% of AI products get Responsibility Assessment (no false negatives)

**If any criterion fails**: Iterate for 1 more sprint before GA.

---

## Post-Launch Metrics

**Track monthly**:

1. **Adoption Rate**: % of `/speckit.concept` runs that use AI mode
2. **CQS Distribution**: Median CQS (target: ≥75 by month 3)
3. **Time Savings**: Avg time to CQS ≥ 80 (target: <1 hour)
4. **Validation Frequency**: % of concepts re-validated (target: ≥10% quarterly)
5. **Competitive Monitoring**: % of projects with monitoring enabled (target: ≥20%)

**Review quarterly**: Adjust prompts, evidence thresholds based on user feedback.

---

## Appendix: Technical Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    /speckit.concept (AI Mode)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              ConceptResearchOrchestrator                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Parallel Agent Execution (asyncio)                  │   │
│  │                                                       │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│   │
│  │  │ Market   │ │Competitive│ │ Persona  │ │  Trend   ││   │
│  │  │ Research │ │ Analysis  │ │ Research │ │ Analysis ││   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘│   │
│  │       │             │             │             │     │   │
│  │       └─────────────┴─────────────┴─────────────┘     │   │
│  │                          │                            │   │
│  │                    Shared Memory                      │   │
│  │                (research_db.json)                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Evidence Validator                        │
│  - Check source count (≥2)                                  │
│  - Validate source credibility                              │
│  - Cross-reference claims                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Enhanced CQS Calculator                   │
│  - Score components with evidence thresholds                │
│  - Identify gaps                                            │
│  - Generate recommendations                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation                        │
│  - concept.md (enhanced with sources)                       │
│  - concept-dashboard.html (visualization)                   │
│  - evidence-collection.md (for manual input)                │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input → Agent Orchestrator → [4 parallel agents] → Shared Memory
                                                              │
                                                              ▼
                                                    Evidence Validator
                                                              │
                                                              ▼
                                                       CQS Calculator
                                                              │
                                                              ▼
                                                    concept.md + dashboard
```

---

**Document Version**: 1.0
**Owner**: Engineering Team
**Review Frequency**: After each sprint
**Next Update**: End of Q1 2026 (after Phase 1 completion)
