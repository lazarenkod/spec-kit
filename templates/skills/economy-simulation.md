# Economy Simulation Skill

**Version**: 1.0.0
**Agent**: game-economist-agent
**Command**: `/speckit.analyze --profile game-economy`
**Quality Gates**: QG-ECONOMY-001, QG-ECONOMY-002, QG-ECONOMY-003, QG-ECONOMY-004

---

## Overview

This skill provides a comprehensive framework for simulating game economies using Monte Carlo methods to validate economic balance, detect pay-to-win patterns, and ensure F2P player progression is fair and engaging.

### Key Capabilities

1. **Monte Carlo Simulation**: Run 10,000+ simulations per player archetype (F2P, dolphin, whale)
2. **Economic Metrics**: Calculate Gini coefficient, inflation rate, wealth distribution
3. **Progression Analysis**: Validate F2P milestone reachability within time budgets
4. **P2W Detection**: Analyze PvP power gaps and exclusive content accessibility
5. **Balance Recommendations**: Generate actionable economy tweaks for failed gates

### Simulation Scope

- **Duration**: 90 days (covers early to mid-game)
- **Archetypes**: F2P, dolphin, whale with realistic spending and playtime
- **Metrics**: Wealth distribution, power progression, milestone completion times
- **Validation**: 4 quality gates (Gini, inflation, F2P reachability, P2W)

---

## Economy Design Input Format

### Required Schema (game-economy-design.md)

```yaml
# Game Economy Design

## Currencies

### Hard Currency (Premium)
- **Name**: Gems
- **Earn Rate (F2P)**: 50 per day
- **Earn Rate (Whale)**: 5000 per day (via purchases)
- **Primary Sources**: Daily login (10), quest completion (20), event rewards (50-100)
- **Primary Sinks**: Gacha pulls (300), stamina refills (50), premium upgrades (1000+)

### Soft Currency (Farmable)
- **Name**: Gold
- **Earn Rate**: 1000 per day
- **Primary Sources**: Battles (50), quests (200), auto-farming
- **Primary Sinks**: Upgrades (500-5000), crafting (1000), unit leveling (2000)

### Premium Currency (Optional)
- **Name**: Battle Pass Points
- **Earn Rate**: $9.99/month subscription
- **Benefits**: 2x rewards, exclusive cosmetics, 500 gems/week

## Progression Milestones

### Early Game (Days 1-14)
| Milestone | F2P Time Budget | Whale Time Budget | Power Requirement | Rewards |
|-----------|-----------------|-------------------|-------------------|---------|
| Reach Level 10 | 7 days | 1 day | 500 | Unlock PvP |
| Clear Chapter 3 | 10 days | 2 days | 800 | Unlock Raid Mode |
| Unlock Hero Slot 4 | 14 days | 3 days | 1200 | +1 team slot |

### Mid Game (Days 15-60)
| Milestone | F2P Time Budget | Whale Time Budget | Power Requirement | Rewards |
|-----------|-----------------|-------------------|-------------------|---------|
| Unlock Raid Mode | 30 days | 3 days | 2000 | Guild content |
| Reach Level 30 | 45 days | 7 days | 3500 | Advanced upgrades |
| Clear Chapter 10 | 60 days | 10 days | 5000 | Endgame content |

### Late Game (Days 61+)
| Milestone | F2P Time Budget | Whale Time Budget | Power Requirement | Rewards |
|-----------|-----------------|-------------------|-------------------|---------|
| Reach Level 50 | 120 days | 20 days | 8000 | Max level cap |
| Clear All Chapters | 180 days | 30 days | 12000 | Completion reward |

## Gacha System (if applicable)

### Character Summon
- **SSR Rate**: 1% (premium characters)
- **SR Rate**: 10% (rare characters)
- **R Rate**: 89% (common characters)
- **Cost**: 300 gems per pull
- **Pity System**: Guaranteed SSR at 90 pulls (27,000 gems)
- **Duplicate Handling**: Convert to upgrade materials (1 SSR = 100 shards)

### Expected Value
- **F2P**: 1 SSR per 9,000 gems (180 days at 50/day)
- **Whale**: 1 SSR per 9,000 gems (1.8 days at 5000/day)
- **Pity**: Guaranteed SSR every 90 pulls (safety net)

## PvP System

### Power Scaling
- **Formula**: `power = base_stats + equipment + skills`
- **Skill Factor**: 30% (player skill can overcome 30% power disadvantage)
- **Matchmaking**: ±20% power bracket
- **Rewards**: Cosmetic only (no P2W advantages)

### Competitive Balance
- **Power Gap Tolerance**: Whale vs F2P should be < 2.0x at same time investment
- **Exclusive Content**: No PvP-critical items locked behind paywall
- **Seasonal Resets**: Quarterly seasons with fresh starts

## Monetization

### Pricing Strategy
- **Small Pack**: $0.99 (100 gems) - 2x value vs base
- **Medium Pack**: $4.99 (600 gems) - 2.4x value
- **Large Pack**: $9.99 (1300 gems) - 2.6x value
- **Whale Pack**: $99.99 (15000 gems) - 3x value
- **Battle Pass**: $9.99/month (2000 gems + rewards)

### Conversion Funnel
- **Trial Payers**: 5% convert at $0.99
- **Dolphins**: 2% convert at $10-50/month
- **Whales**: 0.5% convert at $500+/month

### Ethical Constraints
- **Loot Box Disclosures**: Display odds prominently
- **Spending Limits**: Warn at $100/day, hard cap at $500/day
- **No FOMO**: Limited events return quarterly
- **No Predatory Timers**: Wait timers can be skipped with soft currency
```

---

## Monte Carlo Simulation Framework

### Player Archetype Definitions

#### F2P Player
```python
F2P_ARCHETYPE = {
    "spending": 0,  # $0/month
    "playtime_hours_per_day": 1.5,  # 1-2 hours
    "hard_currency_earn_rate": 50,  # gems/day
    "soft_currency_earn_rate": 1000,  # gold/day
    "efficiency": 0.7,  # 70% optimal resource usage
    "gacha_pulls_per_month": 15,  # 50 gems/day * 30 / 300 gems per pull
    "retention_rate": 0.5,  # 50% still playing after 90 days
}
```

#### Dolphin Player
```python
DOLPHIN_ARCHETYPE = {
    "spending": 25,  # $25/month
    "playtime_hours_per_day": 3,  # 2-4 hours
    "hard_currency_earn_rate": 50 + 500,  # base + purchases
    "soft_currency_earn_rate": 1500,  # More playtime
    "efficiency": 0.85,  # 85% optimal
    "gacha_pulls_per_month": 50,  # (50+500)*30 / 300
    "retention_rate": 0.7,  # 70% retention
}
```

#### Whale Player
```python
WHALE_ARCHETYPE = {
    "spending": 500,  # $500/month
    "playtime_hours_per_day": 6,  # 4-8 hours
    "hard_currency_earn_rate": 50 + 5000,  # base + purchases
    "soft_currency_earn_rate": 2500,  # Maximum farming
    "efficiency": 0.95,  # 95% optimal
    "gacha_pulls_per_month": 500,  # (50+5000)*30 / 300
    "retention_rate": 0.9,  # 90% retention
}
```

### Core Simulation Algorithm

```python
import numpy as np
import random
from typing import Dict, List, Tuple

class PlayerSimulation:
    """Monte Carlo simulation for a single player over N days"""

    def __init__(self, archetype: Dict, economy_config: Dict, duration_days: int = 90):
        self.archetype = archetype
        self.economy = economy_config
        self.duration = duration_days

        # Initialize player state
        self.state = {
            "day": 0,
            "hard_currency": 0,
            "soft_currency": 0,
            "power_level": 100,  # Starting power
            "milestones_reached": [],
            "gacha_pulls": 0,
            "pity_counter": 0,
            "ssr_units": [],
            "total_spent": 0,
        }

    def simulate(self) -> Dict:
        """Run simulation for full duration"""
        for day in range(1, self.duration + 1):
            self.state["day"] = day

            # Daily earnings
            self._earn_currency()

            # Spending behavior
            self._spend_currency()

            # Power progression
            self._update_power()

            # Check milestones
            self._check_milestones()

            # Random events
            self._process_events()

        return self._compile_results()

    def _earn_currency(self):
        """Daily currency earnings with variance"""
        # Base earnings
        hard_earn = self.archetype["hard_currency_earn_rate"]
        soft_earn = self.archetype["soft_currency_earn_rate"]

        # Add variance (±20%)
        hard_variance = np.random.uniform(0.8, 1.2)
        soft_variance = np.random.uniform(0.8, 1.2)

        self.state["hard_currency"] += int(hard_earn * hard_variance)
        self.state["soft_currency"] += int(soft_earn * soft_variance)

    def _spend_currency(self):
        """Spending behavior based on archetype"""
        # Gacha spending priority
        if self.state["hard_currency"] >= 300:  # Cost per pull
            pull_chance = self.archetype["efficiency"]  # How often they pull
            if random.random() < pull_chance:
                self._gacha_pull()

        # Upgrade spending
        upgrade_cost = self._calculate_upgrade_cost()
        if self.state["soft_currency"] >= upgrade_cost:
            self.state["soft_currency"] -= upgrade_cost
            self.state["power_level"] += random.randint(50, 150)

    def _gacha_pull(self):
        """Simulate gacha pull with rates"""
        self.state["hard_currency"] -= 300
        self.state["gacha_pulls"] += 1
        self.state["pity_counter"] += 1

        # Check pity system (guaranteed SSR at 90)
        if self.state["pity_counter"] >= 90:
            self._obtain_ssr()
            self.state["pity_counter"] = 0
            return

        # Normal rates
        roll = random.random()
        if roll < 0.01:  # 1% SSR
            self._obtain_ssr()
            self.state["pity_counter"] = 0
        elif roll < 0.11:  # 10% SR
            self.state["power_level"] += random.randint(100, 200)
        else:  # 89% R
            self.state["power_level"] += random.randint(20, 50)

    def _obtain_ssr(self):
        """Obtain SSR unit"""
        ssr_id = f"SSR_{len(self.state['ssr_units']) + 1}"
        self.state["ssr_units"].append(ssr_id)
        self.state["power_level"] += random.randint(500, 1000)

    def _calculate_upgrade_cost(self) -> int:
        """Calculate upgrade cost with inflation"""
        base_cost = 500
        level_multiplier = 1 + (self.state["power_level"] / 10000)
        day_inflation = 1 + (self.state["day"] / 365) * 0.10  # 10% annual inflation
        return int(base_cost * level_multiplier * day_inflation)

    def _update_power(self):
        """Update power level from playtime"""
        # Passive power gain from gameplay
        playtime_power = self.archetype["playtime_hours_per_day"] * 10
        self.state["power_level"] += int(playtime_power * np.random.uniform(0.8, 1.2))

    def _check_milestones(self):
        """Check if milestones are reached"""
        for milestone in self.economy["progression_milestones"]:
            if milestone["name"] not in self.state["milestones_reached"]:
                if self.state["power_level"] >= milestone["power_requirement"]:
                    self.state["milestones_reached"].append(milestone["name"])

    def _process_events(self):
        """Random events (bonus rewards, limited events)"""
        if random.random() < 0.05:  # 5% chance per day
            self.state["hard_currency"] += random.randint(50, 200)
            self.state["soft_currency"] += random.randint(500, 2000)

    def _compile_results(self) -> Dict:
        """Compile final simulation results"""
        return {
            "archetype": self.archetype,
            "final_day": self.state["day"],
            "hard_currency": self.state["hard_currency"],
            "soft_currency": self.state["soft_currency"],
            "power_level": self.state["power_level"],
            "milestones_reached": self.state["milestones_reached"],
            "milestone_times": self._get_milestone_times(),
            "gacha_pulls": self.state["gacha_pulls"],
            "ssr_count": len(self.state["ssr_units"]),
            "total_spent": self.archetype["spending"] * 3,  # 3 months
        }

    def _get_milestone_times(self) -> Dict:
        """Get day when each milestone was reached"""
        # Simplified: return estimated times based on power progression
        times = {}
        for milestone in self.state["milestones_reached"]:
            # Estimate based on power requirement and progression rate
            times[milestone] = self.state["day"]  # Placeholder
        return times


def run_monte_carlo_simulation(
    economy_config: Dict,
    archetype: Dict,
    n_simulations: int = 10000,
    duration_days: int = 90
) -> List[Dict]:
    """
    Run Monte Carlo simulation for N iterations

    Args:
        economy_config: Parsed economy design
        archetype: Player archetype (F2P, dolphin, whale)
        n_simulations: Number of simulations to run
        duration_days: Simulation duration

    Returns:
        List of simulation results
    """
    results = []

    for i in range(n_simulations):
        sim = PlayerSimulation(archetype, economy_config, duration_days)
        result = sim.simulate()
        results.append(result)

        # Progress logging
        if (i + 1) % 1000 == 0:
            print(f"Completed {i + 1}/{n_simulations} simulations")

    return results
```

---

## Economic Metrics Calculation

### 1. Gini Coefficient (QG-ECONOMY-001)

**Purpose**: Measure wealth inequality across player population

```python
def calculate_gini_coefficient(wealth_distribution: List[float]) -> float:
    """
    Calculate Gini coefficient from wealth distribution

    Gini = 0 → perfect equality (everyone has same wealth)
    Gini = 1 → perfect inequality (one player has all wealth)

    Target: Gini < 0.6 (moderate inequality acceptable in F2P games)

    Args:
        wealth_distribution: List of total wealth values (all currencies combined)

    Returns:
        Gini coefficient (0.0 to 1.0)
    """
    sorted_wealth = np.sort(wealth_distribution)
    n = len(sorted_wealth)
    cumulative_wealth = np.cumsum(sorted_wealth)

    # Gini formula: (2 * sum of weighted wealth) / (n * total_wealth) - (n+1)/n
    gini = (2 * np.sum((np.arange(n) + 1) * sorted_wealth)) / (n * cumulative_wealth[-1]) - (n + 1) / n

    return gini


def validate_gini_coefficient(
    f2p_results: List[Dict],
    dolphin_results: List[Dict],
    whale_results: List[Dict]
) -> Tuple[float, str]:
    """
    Validate Gini coefficient across all player archetypes

    Returns:
        (gini_value, "PASS" or "FAIL")
    """
    # Combine all wealth values
    wealth_distribution = []

    for result in f2p_results:
        total_wealth = result["hard_currency"] + result["soft_currency"] / 10  # Convert to equivalent
        wealth_distribution.append(total_wealth)

    for result in dolphin_results:
        total_wealth = result["hard_currency"] + result["soft_currency"] / 10
        wealth_distribution.append(total_wealth)

    for result in whale_results:
        total_wealth = result["hard_currency"] + result["soft_currency"] / 10
        wealth_distribution.append(total_wealth)

    gini = calculate_gini_coefficient(wealth_distribution)
    status = "PASS" if gini < 0.6 else "FAIL"

    return gini, status


# Example usage
gini_value, status = validate_gini_coefficient(f2p_results, dolphin_results, whale_results)
print(f"Gini Coefficient: {gini_value:.2f} ({status})")
```

### 2. Inflation Rate (QG-ECONOMY-002)

**Purpose**: Measure currency value decay over time

```python
def calculate_inflation_rate(simulation_results: List[Dict], economy_config: Dict) -> float:
    """
    Calculate monthly inflation rate by comparing upgrade costs over time

    Inflation = (cost_week4 - cost_week1) / cost_week1 * 100%

    Target: < 10% per month

    Args:
        simulation_results: Results from simulations
        economy_config: Economy configuration

    Returns:
        Inflation rate (percentage)
    """
    # Sample upgrade costs at Week 1 and Week 4
    week1_costs = []
    week4_costs = []

    for result in simulation_results:
        # Reconstruct upgrade costs at different time points
        # Week 1 (day 7): base_cost * level_multiplier * day_inflation
        power_week1 = result["power_level"] * 0.3  # Estimate 30% of final power
        cost_week1 = 500 * (1 + power_week1 / 10000) * (1 + (7 / 365) * 0.10)
        week1_costs.append(cost_week1)

        # Week 4 (day 28)
        power_week4 = result["power_level"] * 0.6  # Estimate 60% of final power
        cost_week4 = 500 * (1 + power_week4 / 10000) * (1 + (28 / 365) * 0.10)
        week4_costs.append(cost_week4)

    avg_week1 = np.mean(week1_costs)
    avg_week4 = np.mean(week4_costs)

    inflation_rate = ((avg_week4 - avg_week1) / avg_week1) * 100

    return inflation_rate


def validate_inflation_rate(f2p_results: List[Dict], economy_config: Dict) -> Tuple[float, str]:
    """
    Validate inflation rate (use F2P as baseline)

    Returns:
        (inflation_rate, "PASS" or "FAIL")
    """
    inflation = calculate_inflation_rate(f2p_results, economy_config)
    status = "PASS" if inflation < 10.0 else "FAIL"

    return inflation, status


# Example usage
inflation_rate, status = validate_inflation_rate(f2p_results, economy_config)
print(f"Inflation Rate: {inflation_rate:.1f}%/month ({status})")
```

### 3. F2P Milestone Reachability (QG-ECONOMY-003)

**Purpose**: Validate all major milestones are reachable by F2P within time budgets

```python
def validate_f2p_milestones(
    f2p_results: List[Dict],
    economy_config: Dict
) -> Tuple[Dict, str]:
    """
    Check if F2P players can reach milestones within time budgets

    Target:
    - Early game (Level 1-10): < 14 days
    - Mid game (Level 11-30): < 60 days
    - Late game (Level 31+): < 180 days

    Args:
        f2p_results: F2P simulation results
        economy_config: Economy configuration with milestones

    Returns:
        (milestone_times, "PASS" or "FAIL")
    """
    milestone_data = {}
    all_passed = True

    for milestone in economy_config["progression_milestones"]:
        milestone_name = milestone["name"]
        time_budget = milestone["f2p_time_budget"]

        # Calculate median time to reach this milestone
        times_to_reach = []
        for result in f2p_results:
            if milestone_name in result["milestones_reached"]:
                # Estimate time based on power progression
                power_req = milestone["power_requirement"]
                final_power = result["power_level"]
                estimated_day = int((power_req / final_power) * result["final_day"])
                times_to_reach.append(estimated_day)

        if not times_to_reach:
            median_time = None
            status = "FAIL"
            all_passed = False
        else:
            median_time = int(np.median(times_to_reach))
            status = "PASS" if median_time <= time_budget else "FAIL"
            if status == "FAIL":
                all_passed = False

        milestone_data[milestone_name] = {
            "time_budget": time_budget,
            "median_time": median_time,
            "status": status,
            "sample_size": len(times_to_reach),
        }

    overall_status = "PASS" if all_passed else "FAIL"

    return milestone_data, overall_status


# Example usage
milestone_data, status = validate_f2p_milestones(f2p_results, economy_config)
print(f"F2P Milestone Reachability: {status}")
for name, data in milestone_data.items():
    print(f"  {name}: {data['median_time']} days (budget: {data['time_budget']}) - {data['status']}")
```

### 4. Pay-to-Win Detection (QG-ECONOMY-004)

**Purpose**: Detect unfair PvP advantages and exclusive content

```python
def calculate_power_gap(
    f2p_results: List[Dict],
    whale_results: List[Dict],
    same_time_investment: int = 30
) -> float:
    """
    Calculate power gap between F2P and whale at same time investment

    Target: Power gap < 2.0x (whale should not have >2x advantage)

    Args:
        f2p_results: F2P simulation results
        whale_results: Whale simulation results
        same_time_investment: Day to compare (default 30 days)

    Returns:
        Power gap ratio (whale / f2p)
    """
    # Estimate power at day 30 for both groups
    f2p_power_30d = []
    for result in f2p_results:
        # Estimate power at day 30 (linear interpolation)
        power_30d = result["power_level"] * (same_time_investment / result["final_day"])
        f2p_power_30d.append(power_30d)

    whale_power_30d = []
    for result in whale_results:
        power_30d = result["power_level"] * (same_time_investment / result["final_day"])
        whale_power_30d.append(power_30d)

    median_f2p = np.median(f2p_power_30d)
    median_whale = np.median(whale_power_30d)

    power_gap = median_whale / median_f2p

    return power_gap


def check_exclusive_content(economy_config: Dict) -> Tuple[List[str], str]:
    """
    Check for PvP-critical items locked behind paywall

    Returns:
        (list_of_issues, "PASS" or "FAIL")
    """
    issues = []

    # Check PvP accessibility
    pvp_config = economy_config.get("pvp", {})
    if not pvp_config.get("enabled", False):
        return [], "PASS"  # No PvP, no P2W concern

    # Check for exclusive PvP advantages
    rewards = pvp_config.get("rewards", "")
    if "exclusive" in rewards.lower() and "power" in rewards.lower():
        issues.append("PvP rewards contain exclusive power-increasing items")

    # Check gacha system for PvP-required characters
    gacha_config = economy_config.get("gacha", {})
    if gacha_config:
        ssr_rate = gacha_config.get("ssr_rate", 0)
        pity_system = gacha_config.get("pity_system", False)

        if ssr_rate < 0.01 and not pity_system:
            issues.append("Gacha has low SSR rate (<1%) without pity system")

    status = "PASS" if len(issues) == 0 else "FAIL"
    return issues, status


def validate_pay_to_win(
    f2p_results: List[Dict],
    whale_results: List[Dict],
    economy_config: Dict
) -> Tuple[Dict, str]:
    """
    Comprehensive P2W validation

    Returns:
        (p2w_data, "PASS" or "FAIL")
    """
    power_gap = calculate_power_gap(f2p_results, whale_results, same_time_investment=30)
    exclusive_issues, exclusive_status = check_exclusive_content(economy_config)

    p2w_data = {
        "power_gap_30d": power_gap,
        "power_gap_status": "PASS" if power_gap < 2.0 else "FAIL",
        "exclusive_content_issues": exclusive_issues,
        "exclusive_content_status": exclusive_status,
    }

    overall_status = "PASS" if p2w_data["power_gap_status"] == "PASS" and exclusive_status == "PASS" else "FAIL"

    return p2w_data, overall_status


# Example usage
p2w_data, status = validate_pay_to_win(f2p_results, whale_results, economy_config)
print(f"Pay-to-Win Check: {status}")
print(f"  Power Gap (30d): {p2w_data['power_gap_30d']:.2f}x")
print(f"  Exclusive Content: {p2w_data['exclusive_content_status']}")
```

---

## Report Generation

### Performance Report Template

```markdown
# Game Economy Simulation Report

**Simulation Date**: {{TIMESTAMP}}
**Simulations per Archetype**: {{N_SIMULATIONS}}
**Duration**: {{DURATION_DAYS}} days

---

## Executive Summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Gini Coefficient | {{GINI_VALUE}} | < 0.6 | {{GINI_STATUS}} |
| Inflation Rate | {{INFLATION_RATE}}%/month | < 10% | {{INFLATION_STATUS}} |
| F2P Milestone Reach | {{F2P_MILESTONE_PERCENT}}% | 100% | {{F2P_MILESTONE_STATUS}} |
| P2W Score | {{P2W_SCORE}} | 0 (no P2W) | {{P2W_STATUS}} |

**Overall Economic Health Score**: {{HEALTH_SCORE}}/100 {{HEALTH_EMOJI}}

---

## Quality Gate Summary

| Gate ID | Description | Status |
|---------|-------------|--------|
| QG-ECONOMY-001 | Gini Coefficient < 0.6 | {{QG_001_STATUS}} |
| QG-ECONOMY-002 | Inflation < 10%/month | {{QG_002_STATUS}} |
| QG-ECONOMY-003 | F2P Milestones Reachable | {{QG_003_STATUS}} |
| QG-ECONOMY-004 | No P2W in PvP | {{QG_004_STATUS}} |

---

## Simulation Details

### Player Archetypes

| Archetype | Spending | Playtime | Sample Size |
|-----------|----------|----------|-------------|
| F2P | $0/month | {{F2P_PLAYTIME}} hrs/day | {{N_SIMULATIONS}} |
| Dolphin | ${{DOLPHIN_SPEND}}/month | {{DOLPHIN_PLAYTIME}} hrs/day | {{N_SIMULATIONS}} |
| Whale | ${{WHALE_SPEND}}/month | {{WHALE_PLAYTIME}} hrs/day | {{N_SIMULATIONS}} |

### Wealth Distribution (Day {{DURATION_DAYS}})

**F2P Players**:
- Median {{HARD_CURRENCY_NAME}}: {{F2P_HARD_MEDIAN}}
- Median {{SOFT_CURRENCY_NAME}}: {{F2P_SOFT_MEDIAN}}
- Power Level: {{F2P_POWER_MEDIAN}}

**Whale Players**:
- Median {{HARD_CURRENCY_NAME}}: {{WHALE_HARD_MEDIAN}}
- Median {{SOFT_CURRENCY_NAME}}: {{WHALE_SOFT_MEDIAN}}
- Power Level: {{WHALE_POWER_MEDIAN}}

**Gini Coefficient**: {{GINI_VALUE}} ({{GINI_INTERPRETATION}})

---

## Economic Metrics

### 1. Gini Coefficient Analysis (QG-ECONOMY-001)

**Result**: {{GINI_VALUE}} {{GINI_STATUS}}
**Threshold**: < 0.6
**Interpretation**: {{GINI_INTERPRETATION}}

### 2. Inflation Rate (QG-ECONOMY-002)

**Result**: {{INFLATION_RATE}}% per month {{INFLATION_STATUS}}
**Threshold**: < 10%
**Calculation**:
- Week 1 average upgrade cost: {{WEEK1_COST}} {{SOFT_CURRENCY_NAME}}
- Week 4 average upgrade cost: {{WEEK4_COST}} {{SOFT_CURRENCY_NAME}}
- Inflation: ({{WEEK4_COST}} - {{WEEK1_COST}}) / {{WEEK1_COST}} = {{INFLATION_RATE}}%

**Interpretation**: {{INFLATION_INTERPRETATION}}

### 3. F2P Milestone Reachability (QG-ECONOMY-003)

| Milestone | Time Budget | Median F2P Time | Status |
|-----------|-------------|-----------------|--------|
{{#each MILESTONES}}
| {{name}} | {{time_budget}} days | {{median_time}} days | {{status}} |
{{/each}}

**Result**: {{F2P_MILESTONE_STATUS}}
**Interpretation**: {{F2P_MILESTONE_INTERPRETATION}}

### 4. Pay-to-Win Analysis (QG-ECONOMY-004)

**PvP Power Gap (30-day comparison)**:
- F2P median power: {{F2P_POWER_30D}}
- Whale median power: {{WHALE_POWER_30D}}
- Power gap ratio: {{POWER_GAP}}x

**Result**: {{POWER_GAP}}x {{POWER_GAP_STATUS}} (threshold: < 2.0x)
**Interpretation**: {{POWER_GAP_INTERPRETATION}}

**Exclusive Content Check**:
{{#each EXCLUSIVE_ISSUES}}
- ❌ {{issue}}
{{/each}}
{{#if NO_EXCLUSIVE_ISSUES}}
- ✅ All PvP modes accessible to F2P
- ✅ No PvP-critical items locked behind paywall
{{/if}}

---

## Recommendations

### Strengths
{{#each STRENGTHS}}
- ✅ {{strength}}
{{/each}}

### Issues Detected
{{#each ISSUES}}
- ❌ {{issue}}
{{/each}}

### Suggested Fixes
{{#each RECOMMENDATIONS}}
{{priority}}. **{{title}}**
   - **Current**: {{current_value}}
   - **Target**: {{target_value}}
   - **Action**: {{action}}
   - **Expected Impact**: {{impact}}

{{/each}}

---

## Appendix: Raw Data

See `reports/economy-metrics.json` for detailed simulation data.

### JSON Structure
```json
{
  "simulation_metadata": {
    "timestamp": "{{TIMESTAMP}}",
    "n_simulations": {{N_SIMULATIONS}},
    "duration_days": {{DURATION_DAYS}},
    "archetypes": ["f2p", "dolphin", "whale"]
  },
  "gini_coefficient": {
    "value": {{GINI_VALUE}},
    "threshold": 0.6,
    "status": "{{GINI_STATUS}}"
  },
  "inflation_rate": {
    "value": {{INFLATION_RATE}},
    "threshold": 10.0,
    "status": "{{INFLATION_STATUS}}"
  },
  "f2p_milestones": {{F2P_MILESTONE_JSON}},
  "p2w_analysis": {{P2W_JSON}},
  "quality_gates": {
    "QG-ECONOMY-001": "{{QG_001_STATUS}}",
    "QG-ECONOMY-002": "{{QG_002_STATUS}}",
    "QG-ECONOMY-003": "{{QG_003_STATUS}}",
    "QG-ECONOMY-004": "{{QG_004_STATUS}}"
  },
  "economic_health_score": {{HEALTH_SCORE}}
}
```
```

---

## Usage Examples

### Example 1: Run Full Economy Simulation

```bash
# Via /speckit.analyze
specify analyze --profile game-economy

# Output:
# ✅ Parsing game-economy-design.md
# ✅ Running Monte Carlo simulations (30,000 total)
#    - F2P: 10,000 simulations
#    - Dolphin: 10,000 simulations
#    - Whale: 10,000 simulations
# ✅ Calculating economic metrics
# ✅ Validating quality gates
#    - QG-ECONOMY-001: PASS (Gini = 0.52)
#    - QG-ECONOMY-002: PASS (Inflation = 8.3%)
#    - QG-ECONOMY-003: PASS (All milestones reachable)
#    - QG-ECONOMY-004: PASS (Power gap = 1.92x)
# ✅ Generated reports/economy-simulation-report.md
# ✅ Generated reports/economy-metrics.json
#
# Economic Health Score: 95/100 ✅
```

### Example 2: Detect P2W Issue

```yaml
# game-economy-design.md (imbalanced)
currencies:
  hard_currency:
    earn_rate_f2p: 10/day  # Too low!
    earn_rate_whale: 10000/day  # Too high!

pvp:
  enabled: true
  power_scaling: "exponential"  # Problematic!
  exclusive_characters: true  # P2W flag!
```

```bash
specify analyze --profile game-economy

# Output:
# ❌ QG-ECONOMY-001: FAIL (Gini = 0.85, threshold < 0.6)
# ❌ QG-ECONOMY-004: FAIL (Power gap = 4.2x, threshold < 2.0x)
#
# Issues Detected:
# 1. Extreme wealth inequality (Gini 0.85)
#    - F2P earn rate too low (10/day vs whale 10000/day)
#    - Recommendation: Increase F2P rate to 50/day
#
# 2. Pay-to-Win in PvP (power gap 4.2x)
#    - Exponential power scaling favors whales excessively
#    - Exclusive characters locked behind paywall
#    - Recommendation: Switch to linear scaling, make all characters earnable
#
# Economic Health Score: 35/100 ❌
```

### Example 3: Validate Balanced Economy

```yaml
# game-economy-design.md (well-balanced)
currencies:
  hard_currency:
    earn_rate_f2p: 50/day
    earn_rate_whale: 5000/day

progression_milestones:
  - name: "Level 10"
    f2p_time_budget: 7 days
    power_requirement: 500

pvp:
  enabled: true
  power_scaling: "linear"
  skill_factor: 0.3  # 30% skill-based
  rewards: "cosmetic_only"  # No P2W
```

```bash
specify analyze --profile game-economy

# Output:
# ✅ QG-ECONOMY-001: PASS (Gini = 0.52)
# ✅ QG-ECONOMY-002: PASS (Inflation = 8.3%)
# ✅ QG-ECONOMY-003: PASS (All milestones reachable)
# ✅ QG-ECONOMY-004: PASS (Power gap = 1.92x)
#
# Economic Health Score: 95/100 ✅
#
# Strengths:
# - F2P progression well-paced
# - Moderate wealth inequality (Gini 0.52)
# - PvP competitive balance maintained
# - No predatory P2W mechanics
```

---

## Best Practices

### 1. Simulation Design

**DO**:
- Run at least 10,000 simulations per archetype for statistical significance
- Include variance in daily earnings (±20%) to model real player behavior
- Model retention rates (F2P 50%, whale 90%)
- Include random events (bonus rewards, limited events)

**DON'T**:
- Use deterministic simulations (no variance = unrealistic)
- Ignore player churn (retention rates matter)
- Simulate only whales (F2P progression is critical)
- Skip edge cases (what if player never pulls gacha?)

### 2. Economic Metrics

**DO**:
- Calculate Gini coefficient across all archetypes (not just F2P)
- Measure inflation using upgrade costs (not just currency supply)
- Validate F2P milestone times with percentiles (median + p95)
- Check PvP power gaps at multiple time points (30d, 60d, 90d)

**DON'T**:
- Compare whale vs F2P at different time investments
- Use average instead of median (outliers skew results)
- Ignore skill factor in PvP balance (30% skill can overcome 30% power gap)
- Forget to check exclusive content (not just power gaps)

### 3. Balance Recommendations

**DO**:
- Provide specific parameter tweaks ("Increase F2P gem rate from 50 to 60/day")
- Explain expected impact ("Should reduce Gini from 0.65 to 0.58")
- Prioritize recommendations (P2W issues > mild inflation)
- Suggest iterative testing ("Test with 60/day, measure Gini, adjust if needed")

**DON'T**:
- Give vague advice ("Make economy more balanced")
- Recommend breaking changes ("Remove all monetization")
- Ignore business constraints (developers need revenue)
- Over-optimize for F2P at whale expense (balance is key)

---

## Error Handling

### Missing Economy Design

```python
# Check if economy design exists
if not os.path.exists("templates/shared/concept-sections/game-economy-design.md"):
    print("❌ ERROR: game-economy-design.md not found")
    print("Run `/speckit.concept` with game type to generate economy design")
    sys.exit(1)
```

### Invalid Parameters

```python
# Validate economy parameters
def validate_economy_config(config: Dict) -> List[str]:
    errors = []

    # Check required fields
    if "currencies" not in config:
        errors.append("Missing 'currencies' section")

    if "progression_milestones" not in config:
        errors.append("Missing 'progression_milestones' section")

    # Validate earn rates
    if config.get("currencies", {}).get("hard_currency", {}).get("earn_rate_f2p", 0) <= 0:
        errors.append("earn_rate_f2p must be positive")

    # Validate milestones
    for milestone in config.get("progression_milestones", []):
        if milestone.get("f2p_time_budget", 0) <= 0:
            errors.append(f"Milestone '{milestone.get('name')}' has invalid time budget")

    return errors

errors = validate_economy_config(economy_config)
if errors:
    print("❌ Invalid economy configuration:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
```

### Simulation Failures

```python
# Handle non-convergent simulations
def detect_simulation_outliers(results: List[Dict]) -> List[int]:
    """Detect simulations with extreme outliers (>5σ)"""
    power_levels = [r["power_level"] for r in results]
    mean_power = np.mean(power_levels)
    std_power = np.std(power_levels)

    outliers = []
    for i, result in enumerate(results):
        z_score = abs((result["power_level"] - mean_power) / std_power)
        if z_score > 5:
            outliers.append(i)

    return outliers

outliers = detect_simulation_outliers(f2p_results)
if len(outliers) > len(f2p_results) * 0.05:  # > 5% outliers
    print(f"⚠️  WARNING: {len(outliers)} outlier simulations detected")
    print("Consider rerunning with adjusted parameters")
```

---

## Version History

- **1.0.0** (2026-01-11): Initial skill for Phase 4 mobile agents implementation
