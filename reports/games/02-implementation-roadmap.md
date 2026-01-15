# Implementation Roadmap: Spec-Kit для Мобильных Игр

**Дата**: 2026-01-12
**Timeline**: 12 недель (3 фазы)
**Ресурсы**: 1-2 разработчика

---

## Overview

Дорожная карта для трансформации Spec-Kit из **"good for mobile apps with game elements"** в **"production-ready for viral mobile game development"**.

**Ключевые вехи:**
- ✅ **Phase 1 (4 weeks)**: Critical gaps - GDD, Playtesting, Soft Launch
- ⚠️  **Phase 2 (4 weeks)**: High-priority integrations - Unity, Analytics, Balance
- 📊 **Phase 3 (4 weeks)**: Polish & optimization - ML, Unreal, Advanced features

---

## Phase 1: Critical Gaps (Weeks 1-4) - P0

**Цель**: Устранить блокирующие пробелы для production использования.

### Week 1: GDD Command + Template

**Deliverables:**
- ✅ `/speckit.gdd` command (already created in `templates/commands/gdd.md`)
- ✅ GDDQS (GDD Quality Score) rubric (0-100)
- ✅ Quality gates (QG-GDD-001..004)

**Integration Tasks:**
1. **Add to CLI** (`src/specify_cli/__init__.py`)
   ```python
   GAME_COMMANDS = ["gdd", "playtest", "balance", "softlaunch", "liveops", "analytics"]

   @app.command()
   def gdd(
       feature_id: str = typer.Option(..., help="Feature ID (e.g., 001-core-gameplay)"),
       mode: str = typer.Option("create", help="create|update|view"),
   ):
       """Create and maintain living Game Design Document."""
       # Implementation
   ```

2. **Update COMMANDS_GUIDE.md**
   - Add `/speckit.gdd` section with examples
   - Update workflow diagram (constitution → concept → gdd → specify)

3. **Add persona** (`templates/personas/game-designer-agent.md`)
   ```yaml
   persona: game-designer-agent
   expertise:
     - Game design patterns (casual, mid-core, RPG, hyper-casual)
     - Core loop design + metagame architecture
     - Player psychology + motivation
     - Industry benchmarks (Supercell, King, Voodoo)
   tools:
     - GDD templates with 10 sections
     - Core loop diagram generator
     - Progression curve visualizer
   ```

4. **Test & Validate**
   ```bash
   cd /path/to/test-game-project
   specify gdd 001-core-gameplay --mode create
   # Verify: specs/features/001-core-gameplay/gdd.md created
   # Verify: GDDQS calculated
   # Verify: Quality gates checked
   ```

**Effort**: 5 days (1 week with testing)

---

### Week 2: Playtest Command + Framework

**Deliverables:**
- ✅ `/speckit.playtest` command (already created in `templates/commands/playtest.md`)
- ✅ Session templates (internal, external, focus group)
- ✅ Survey designer (auto-generate questions)
- ✅ Quality gates (QG-PLAYTEST-001..004)

**Integration Tasks:**
1. **Add to CLI**
   ```python
   @app.command()
   def playtest(
       feature_id: str = typer.Option(...),
       mode: str = typer.Option("internal", help="internal|external|friends_family|closed_beta|open_beta|focus_group"),
       participants: int = typer.Option(5, help="Number of participants"),
   ):
       """Plan and execute playtesting sessions."""
       # Implementation
   ```

2. **Create survey designer** (`src/specify_cli/playtest_survey.py`)
   ```python
   def generate_playtest_survey(feature_type: str, core_mechanics: List[str]):
       """Auto-generate playtest survey based on feature type."""
       questions = {
           "comprehension": [
               f"Did you understand how {mechanic} works? (1-10)",
               # ... generate 5 comprehension questions
           ],
           "engagement": [
               "How fun was the gameplay? (1-10)",
               # ... generate 5 engagement questions
           ],
           "nps": [
               "How likely would you recommend this game? (0-10)"
           ]
       }
       return questions
   ```

3. **Add PlaytestCloud API integration** (optional, Phase 2)
   ```python
   # src/specify_cli/integrations/playtestcloud.py
   class PlaytestCloudClient:
       def create_session(self, build_url, participant_criteria):
           # API call to PlaytestCloud
           pass
   ```

4. **Test & Validate**
   ```bash
   specify playtest 001-core-gameplay --mode internal --participants 8
   # Verify: reports/playtest-session-{date}.md created
   # Verify: Survey questions generated
   # Verify: NPS calculated post-session
   ```

**Effort**: 5 days (1 week with testing)

---

### Week 3: Soft Launch Command

**Deliverables:**
- ✅ `/speckit.softlaunch` command (already created in `templates/commands/softlaunch.md`)
- ✅ 3-phase rollout template
- ✅ Decision tree (GO/ITERATE/PIVOT/KILL)
- ✅ Quality gates (QG-SOFTLAUNCH-001..005)

**Integration Tasks:**
1. **Add to CLI**
   ```python
   @app.command()
   def softlaunch(
       feature_id: str = typer.Option(...),
       phase: int = typer.Option(1, help="1=Test Market, 2=Scale Test, 3=Global"),
       genre: str = typer.Option(..., help="hyper-casual|casual|mid-core|rpg"),
   ):
       """Plan and execute geographic soft launch."""
       # Implementation
   ```

2. **Create decision tree validator** (`src/specify_cli/softlaunch_decision.py`)
   ```python
   def evaluate_phase_metrics(phase: int, metrics: dict, genre: str):
       """Evaluate metrics against thresholds, return decision."""
       thresholds = GENRE_THRESHOLDS[genre][f"phase_{phase}"]

       d1 = metrics["d1_retention"]
       cpi = metrics["cpi"]
       ltv_cpi_ratio = metrics.get("ltv_cpi_ratio", 0)

       if phase == 1:
           if d1 >= thresholds["d1"] and cpi <= thresholds["cpi"]:
               return "GO"
           elif d1 >= 0.30:
               return "ITERATE"
           elif d1 >= 0.25:
               return "PIVOT"
           else:
               return "KILL"
       # ... similar logic for phase 2, 3
   ```

3. **Test & Validate**
   ```bash
   specify softlaunch 001-core-gameplay --phase 1 --genre casual
   # Verify: specs/features/001-core-gameplay/softlaunch-plan.md created
   # Verify: Regional markets selected
   # Verify: Decision tree logic correct
   ```

**Effort**: 4 days

---

### Week 4: Quality Gates Registry Update

**Deliverables:**
- ✅ Add 30+ new Quality Gates to `memory/domains/quality-gates.md`
- ✅ Update inline gates for game commands

**Tasks:**
1. **Extend quality-gates.md**
   ```markdown
   ## Retention Quality Gates (QG-RET-xxx)

   ### QG-RET-001: D1 Retention Target
   **Level**: MUST (for live service games)
   **Threshold**: Genre-specific (see table)
   **Phase**: Post-Soft-Launch

   | Genre | Min D1 | Target D1 | Top 10% |
   |-------|--------|-----------|---------|
   | Hyper-casual | 35% | 45% | 55% |
   | Casual | 40% | 50% | 60% |
   | Mid-core | 45% | 55% | 65% |

   ### QG-GDD-001: Core Loop Defined
   ### QG-PLAYTEST-001: Sample Size
   ### QG-BALANCE-001: Difficulty Curve
   ### QG-SOFTLAUNCH-001: D1 Retention
   # ... +25 more gates
   ```

2. **Update ARCHITECTURE.md**
   - Section 5.2: Add game-specific quality gates table
   - Update quality gate count (120 → 150+)

3. **Documentation**
   - Update COMMANDS_GUIDE.md with quality gates for each game command
   - Add examples of gate failures + remediation

**Effort**: 3 days

---

## Phase 1 Summary

| Week | Deliverable | Status | Validation |
|------|-------------|--------|------------|
| 1 | `/speckit.gdd` integrated | ✅ Ready | Run on test project |
| 2 | `/speckit.playtest` integrated | ✅ Ready | Run internal playtest |
| 3 | `/speckit.softlaunch` integrated | ✅ Ready | Create soft launch plan |
| 4 | Quality gates updated | ✅ Ready | Review documentation |

**Phase 1 Exit Criteria:**
- ✅ All 3 P0 commands functional in CLI
- ✅ Documentation complete (COMMANDS_GUIDE.md updated)
- ✅ Quality gates registry extended
- ✅ 1+ test project successfully uses all commands

**Deliverable Files Created:**
- `templates/commands/gdd.md` ✅
- `templates/commands/playtest.md` ✅
- `templates/commands/softlaunch.md` ✅
- `templates/personas/game-designer-agent.md` (new)
- `templates/personas/ux-researcher-agent.md` (new)
- `templates/personas/product-manager-agent.md` (new)

---

## Phase 2: High-Priority Integrations (Weeks 5-8) - P1

**Цель**: Добавить ключевые интеграции для production workflow.

### Week 5: Balance Command + Simulation

**Deliverables:**
- ✅ `/speckit.balance` command (already created in `templates/commands/balance.md`)
- ✅ Difficulty curve simulator (Python)
- ✅ Meta concentration analyzer
- ✅ Quality gates (QG-BALANCE-001..006)

**Tasks:**
1. **Add to CLI**
2. **Create simulation scripts** (`scripts/balance/`)
   ```bash
   scripts/balance/
   ├── difficulty_curve.py
   ├── meta_concentration.py
   ├── power_variance.py
   └── bot_simulation.py (advanced, optional)
   ```
3. **Test on example game** (e.g., match-3 prototype)

**Effort**: 1.5 weeks

---

### Week 6-7: Unity Editor Plugin

**Deliverables:**
- Unity Editor plugin for in-editor spec validation
- Profiler data export button
- Quality gate status panel

**Tasks:**
1. **Create Unity package** (`unity-plugin/`)
   ```csharp
   // SpecKitEditorWindow.cs
   public class SpecKitEditorWindow : EditorWindow {
       [MenuItem("Tools/Spec-Kit/Validate Specs")]
       static void ValidateSpecs() {
           // Read specs/features/*/spec.md
           // Validate FR-xxx implemented
           // Show report in editor window
       }

       [MenuItem("Tools/Spec-Kit/Export Profiler Data")]
       static void ExportProfilerData() {
           // Parse Unity Profiler logs
           // Export to JSON for QG validation
       }
   }
   ```

2. **Add to Asset Store** (optional, for distribution)
3. **Documentation** (`docs/unity-integration.md`)

**Effort**: 2 weeks

---

### Week 8: GameAnalytics Integration

**Deliverables:**
- GameAnalytics API client
- Automated cohort reports
- D1/D7/D30 dashboard

**Tasks:**
1. **Create API client** (`src/specify_cli/integrations/gameanalytics.py`)
   ```python
   class GameAnalyticsClient:
       def fetch_retention_cohorts(self, game_key: str, days: int = 30):
           # API call to GameAnalytics
           # Return D1, D7, D30 retention data
           pass
   ```

2. **Add `/speckit.analytics` command**
3. **Test on real game data** (requires GameAnalytics account)

**Effort**: 1 week

---

## Phase 2 Summary

| Week | Deliverable | Effort | Dependencies |
|------|-------------|--------|--------------|
| 5 | `/speckit.balance` + simulations | 1.5 weeks | Python, NumPy |
| 6-7 | Unity Editor plugin | 2 weeks | Unity 2022 LTS |
| 8 | GameAnalytics integration | 1 week | GA API key |

**Phase 2 Exit Criteria:**
- ✅ Balance simulations run successfully
- ✅ Unity plugin installable via Package Manager
- ✅ GameAnalytics client fetches real data

---

## Phase 3: Polish & Optimization (Weeks 9-12) - P2

**Цель**: Advanced features, ML integration, Unreal support.

### Week 9-10: Unreal Engine Integration

**Tasks:**
- Unreal Blueprint integration
- Unreal Insights data export
- Console profiling (PlayStation SDK, Xbox GDK)

**Effort**: 2 weeks

---

### Week 11: ML-Enhanced Economy Simulation

**Tasks:**
- Churn prediction model (XGBoost)
- Whale behavior modeling (K-means clustering)
- Dynamic pricing optimization (Contextual Bandit)

**Effort**: 1 week

---

### Week 12: PlaytestCloud Integration + Final Polish

**Tasks:**
- PlaytestCloud API integration
- Advanced features (core loop validation, CPI prediction)
- Performance optimization
- Final documentation pass

**Effort**: 1 week

---

## Implementation Team

**Recommended Team:**
- 1x Senior Backend Engineer (spec-kit CLI, Python, API integrations)
- 1x Unity/Unreal Engineer (game engine plugins)
- 0.5x Designer (GDD templates, playtest surveys)
- 0.5x QA (testing, validation, example projects)

**Total**: 3 FTE for 12 weeks = 36 person-weeks

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Unity/Unreal plugin complexity | MEDIUM | HIGH | Start with minimal MVP, iterate based on feedback |
| GameAnalytics API changes | LOW | MEDIUM | Use official SDK, monitor changelogs |
| Community adoption slow | MEDIUM | HIGH | Create showcase projects, write tutorials, engage on Twitter/Reddit |
| Quality gate tuning difficult | MEDIUM | MEDIUM | Start with conservative thresholds, tune based on user feedback |

---

## Success Metrics (6 months post-launch)

| Metric | Baseline | Target | Actual (TBD) |
|--------|----------|--------|--------------|
| **Games Created** | 0 | 50+ | ___ |
| **Soft Launches** | 0 | 10+ | ___ |
| **Global Launches** | 0 | 3+ | ___ |
| **Avg D1 Retention** | N/A | 45%+ | ___ |
| **GDD Adoption Rate** | 0% | 80%+ | ___ |
| **Playtest Sessions** | 0 | 200+ | ___ |
| **Community NPS** | N/A | 50+ | ___ |

---

## Timeline Visualization

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       12-WEEK IMPLEMENTATION ROADMAP                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  PHASE 1: CRITICAL GAPS (P0) - Weeks 1-4                                  │
│  ┌────────┬────────┬────────┬────────┐                                    │
│  │ Week 1 │ Week 2 │ Week 3 │ Week 4 │                                    │
│  │  GDD   │Playtest│Softlnch│QG Update│                                   │
│  └────────┴────────┴────────┴────────┘                                    │
│                                                                            │
│  PHASE 2: HIGH-PRIORITY (P1) - Weeks 5-8                                  │
│  ┌─────────┬──────────────┬────────┐                                      │
│  │ Week 5  │  Weeks 6-7   │ Week 8 │                                      │
│  │ Balance │Unity Plugin  │Analytics│                                     │
│  └─────────┴──────────────┴────────┘                                      │
│                                                                            │
│  PHASE 3: POLISH & OPTIMIZATION (P2) - Weeks 9-12                         │
│  ┌──────────────┬────────┬─────────────┐                                 │
│  │  Weeks 9-10  │ Week 11│   Week 12   │                                 │
│  │Unreal Plugin │ML Econ │PlaytestCloud│                                 │
│  └──────────────┴────────┴─────────────┘                                 │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Получить approval** от spec-kit maintainers
2. **Phase 1 Kickoff** (Week 1: `/speckit.gdd` integration)
3. **Recruit beta testers** (3-5 game studios)
4. **Set up telemetry** (command usage tracking)
5. **Community engagement** (announce on Twitter, Reddit r/gamedev)

---

**Дата**: 2026-01-12
**Версия**: 1.0
**Статус**: Ready for Implementation

**См. также:**
- `00-executive-summary.md` - краткое резюме
- `01-gap-analysis.md` - детальный анализ пробелов
- `04-industry-benchmarks.md` - бенчмарки индустрии
