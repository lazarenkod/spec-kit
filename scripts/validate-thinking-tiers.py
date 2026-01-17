#!/usr/bin/env python3
"""Validate thinking tier configuration across all command templates.

This script validates that all command templates have correct 7-tier
thinking budget configurations according to their category.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set

# Category definitions and expected tier configurations
CATEGORIES = {
    "A": {
        "name": "Lightweight",
        "tiers": 4,
        "choices": ["minimal", "quick", "standard", "thorough"],
        "default": "minimal",
        "commands": [
            "list", "help", "staging", "switch", "taskstoissues",
            "migrate", "reverse-engineer", "speckit.concept.switch"
        ],
    },
    "B": {
        "name": "Core Workflow",
        "tiers": 7,
        "choices": ["minimal", "quick", "standard", "thorough", "deep", "expert", "ultrathink"],
        "default": "standard",
        "commands": [
            "specify", "plan", "tasks", "clarify", "baseline", "extend",
            "validate-concept", "checklist", "properties", "verify"
        ],
    },
    "C": {
        "name": "Strategic",
        "tiers": 6,
        "choices": ["quick", "standard", "thorough", "deep", "expert", "ultrathink"],
        "default": "thorough",
        "commands": [
            "concept", "constitution", "design", "analytics",
            "discover", "concept-variants", "balance"
        ],
    },
    "D": {
        "name": "Orchestration",
        "tiers": 5,
        "choices": ["standard", "thorough", "deep", "expert", "ultrathink"],
        "default": "thorough",
        "commands": [
            "implement", "analyze", "preview", "launch", "monitor", "ship"
        ],
    },
    "E": {
        "name": "Drift Management",
        "tiers": 2,
        "choices": ["standard", "ultrathink"],
        "default": "standard",
        "commands": ["speckit.fix", "speckit.merge"],
    },
    "F": {
        "name": "Game/Mobile",
        "tiers": 6,
        "choices": ["quick", "standard", "thorough", "deep", "expert", "ultrathink"],
        "default": "standard",
        "commands": [
            "liveops", "playtest", "softlaunch", "mobile",
            "games-concept", "games-mechanics", "games-progression",
            "games-virality", "gdd"
        ],
    },
    "G": {
        "name": "Integration",
        "tiers": 5,
        "choices": ["quick", "standard", "thorough", "deep", "ultrathink"],
        "default": "standard",
        "commands": ["integrate"],
    },
}


def find_category(command: str) -> str:
    """Find which category a command belongs to."""
    for cat_id, cat_info in CATEGORIES.items():
        if command in cat_info["commands"]:
            return cat_id
    return None


def extract_yaml_frontmatter(content: str) -> str:
    """Extract YAML frontmatter from markdown file."""
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1)
    return ""


def validate_flags_section(yaml_content: str, command: str, category: str) -> List[str]:
    """Validate flags section has correct tier choices."""
    errors = []
    expected = CATEGORIES[category]

    # Find --thinking-depth flag section
    flag_pattern = r'- name: --thinking-depth.*?(?=\n  - name:|$)'
    flag_match = re.search(flag_pattern, yaml_content, re.DOTALL)

    if not flag_match:
        errors.append(f"Missing --thinking-depth flag definition")
        return errors

    flag_section = flag_match.group(0)

    # Check choices
    choices_match = re.search(r'choices:\s*\[(.*?)\]', flag_section)
    if not choices_match:
        errors.append(f"Missing choices array in --thinking-depth flag")
    else:
        choices_str = choices_match.group(1)
        actual_choices = [c.strip() for c in choices_str.split(',')]
        expected_choices = expected["choices"]

        if actual_choices != expected_choices:
            errors.append(
                f"Flag choices mismatch: expected {expected_choices}, got {actual_choices}"
            )

    # Check default
    default_match = re.search(r'default:\s*(\w+)', flag_section)
    if not default_match:
        errors.append(f"Missing default value in --thinking-depth flag")
    else:
        actual_default = default_match.group(1)
        expected_default = expected["default"]

        if actual_default != expected_default:
            errors.append(
                f"Flag default mismatch: expected {expected_default}, got {actual_default}"
            )

    return errors


def validate_rate_limits(yaml_content: str, command: str, category: str) -> List[str]:
    """Validate rate_limits section has correct tier definitions."""
    errors = []
    expected = CATEGORIES[category]
    expected_tiers = set(expected["choices"])

    # Find rate_limits.tiers section
    tiers_pattern = r'rate_limits:.*?tiers:(.*?)(?=\n\w|$)'
    tiers_match = re.search(tiers_pattern, yaml_content, re.DOTALL)

    if not tiers_match:
        errors.append(f"Missing rate_limits.tiers section")
        return errors

    tiers_section = tiers_match.group(1)

    # Extract tier names (looking for patterns like "minimal:", "quick:", etc.)
    tier_names = set(re.findall(r'\n\s{4,6}(\w+):', tiers_section))

    # Filter out non-tier keys (like 'default_tier', 'max_parallel', etc.)
    tier_names = {t for t in tier_names if t in expected_tiers or t in ['free', 'pro', 'max']}

    # For non-E category, we expect tier names to match choices
    # For E category (2-tier), old structure might use free/pro/max instead
    if category != "E":
        missing_tiers = expected_tiers - tier_names
        extra_tiers = tier_names - expected_tiers - {'free', 'pro', 'max'}

        if missing_tiers and not ('free' in tier_names or 'pro' in tier_names):
            errors.append(f"Missing tier definitions: {missing_tiers}")
        if extra_tiers:
            errors.append(f"Unexpected tier definitions: {extra_tiers}")

    return errors


def validate_depth_defaults(yaml_content: str, command: str, category: str) -> List[str]:
    """Validate depth_defaults section has correct tier configurations."""
    errors = []
    expected = CATEGORIES[category]
    expected_tiers = set(expected["choices"])

    # Find depth_defaults section
    defaults_pattern = r'depth_defaults:(.*?)(?=\n\w|$)'
    defaults_match = re.search(defaults_pattern, yaml_content, re.DOTALL)

    if not defaults_match:
        errors.append(f"Missing depth_defaults section")
        return errors

    defaults_section = defaults_match.group(1)

    # Extract tier names
    tier_names = set(re.findall(r'\n\s{4}(\w+):', defaults_section))

    missing_tiers = expected_tiers - tier_names
    extra_tiers = tier_names - expected_tiers

    if missing_tiers:
        errors.append(f"Missing depth_defaults configurations: {missing_tiers}")
    if extra_tiers:
        errors.append(f"Unexpected depth_defaults configurations: {extra_tiers}")

    return errors


def validate_cost_breakdown(yaml_content: str, command: str, category: str) -> List[str]:
    """Validate cost_breakdown section has entries for all tiers."""
    errors = []
    expected = CATEGORIES[category]
    expected_tiers = set(expected["choices"])

    # Find cost_breakdown section
    breakdown_pattern = r'cost_breakdown:(.*?)(?=\n\w|$)'
    breakdown_match = re.search(breakdown_pattern, yaml_content, re.DOTALL)

    if not breakdown_match:
        errors.append(f"Missing cost_breakdown section")
        return errors

    breakdown_section = breakdown_match.group(1)

    # Extract tier names
    tier_names = set(re.findall(r'\n\s{4}(\w+):', breakdown_section))

    missing_tiers = expected_tiers - tier_names
    extra_tiers = tier_names - expected_tiers

    if missing_tiers:
        errors.append(f"Missing cost_breakdown entries: {missing_tiers}")
    if extra_tiers:
        errors.append(f"Unexpected cost_breakdown entries: {extra_tiers}")

    return errors


def validate_template(template_path: Path) -> Dict[str, List[str]]:
    """Validate a single template file."""
    command = template_path.stem

    # Skip .COMPRESSED.md files
    if ".COMPRESSED" in template_path.name:
        return {}

    category = find_category(command)
    if not category:
        return {command: [f"Unknown command category"]}

    try:
        content = template_path.read_text()
    except Exception as e:
        return {command: [f"Failed to read file: {e}"]}

    yaml_content = extract_yaml_frontmatter(content)
    if not yaml_content:
        return {command: [f"No YAML frontmatter found"]}

    errors = []

    # Validate each section
    errors.extend(validate_flags_section(yaml_content, command, category))
    errors.extend(validate_rate_limits(yaml_content, command, category))
    errors.extend(validate_depth_defaults(yaml_content, command, category))
    errors.extend(validate_cost_breakdown(yaml_content, command, category))

    if errors:
        return {command: errors}

    return {}


def main():
    """Main validation function."""
    templates_dir = Path(__file__).parent.parent / "templates" / "commands"

    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        sys.exit(1)

    print("🔍 Validating thinking tier configurations...")
    print(f"📁 Templates directory: {templates_dir}")
    print()

    all_errors = {}
    validated_count = 0

    for template_file in sorted(templates_dir.glob("*.md")):
        if ".COMPRESSED" in template_file.name:
            continue

        errors = validate_template(template_file)
        if errors:
            all_errors.update(errors)

        validated_count += 1

    print(f"✅ Validated {validated_count} command templates")
    print()

    if all_errors:
        print(f"❌ Found validation errors in {len(all_errors)} templates:")
        print()

        for command, errors in sorted(all_errors.items()):
            category = find_category(command)
            cat_name = CATEGORIES[category]["name"] if category else "Unknown"
            print(f"  {command}.md (Category {category}: {cat_name})")
            for error in errors:
                print(f"    • {error}")
            print()

        sys.exit(1)
    else:
        print("✅ All templates validated successfully!")
        print()
        print("Summary by category:")
        for cat_id, cat_info in CATEGORIES.items():
            print(f"  {cat_id} - {cat_info['name']}: {len(cat_info['commands'])} commands, {cat_info['tiers']} tiers")

        sys.exit(0)


if __name__ == "__main__":
    main()
