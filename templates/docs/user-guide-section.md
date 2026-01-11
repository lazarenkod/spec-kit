# User Guide Section Template

This template generates user-facing documentation sections from User Stories (US-xxx) and Acceptance Scenarios (AS-xxx).

## Usage

This template is used by:
- `/speckit.specify` — generates initial docs outline from spec.md
- `/speckit.implement` — synthesizes complete user guides from implementation
- `/speckit.docs build --type user-guide` — regenerates user documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| spec.md US-xxx | Feature descriptions, user goals, workflows |
| spec.md AS-xxx | Expected outcomes, examples, edge cases |
| code analysis | Actual UI elements, validation rules, error messages |
| system specs | Current behavior, API endpoints used |

## Template Structure

```markdown
# {Feature Name}

> **Target Audience**: End users
> **Skill Level**: {Beginner/Intermediate/Advanced}
> **Estimated Time**: {X minutes}

## Overview

{One-paragraph description of what this feature does and why users would use it}

## Before You Begin

**Prerequisites:**
- {List prerequisites from US-xxx conditions}

**What You'll Need:**
- {Required accounts, permissions, data}

## Step-by-Step Guide

### {Step 1 Title from US-xxx}

{Clear instructions derived from US action}

**Example:**
```
{Concrete example from AS-xxx GIVEN/WHEN/THEN}
```

**Expected Result:**
- {FROM AS-xxx THEN clause}

**Troubleshooting:**
- **Problem**: {FROM AS-xxx edge cases}
  **Solution**: {Resolution steps}

### {Step 2 Title}

{Repeat structure for each step}

## What's Next

After completing this guide, you can:
- {Link to related user guide}
- {Link to advanced features}
- {Link to FAQ if relevant}

## Tips and Best Practices

{Tips derived from AS-xxx success scenarios and edge cases}

- ✅ **Do**: {Recommended approaches}
- ❌ **Don't**: {Anti-patterns from edge cases}

## Common Questions

{FAQ items derived from AS-xxx edge cases and error scenarios}

**Q: {Question from edge case}**
A: {Answer with reference to AS-xxx}

## See Also

- {Link to related user guide}
- {Link to API reference if power users}
- {Link to troubleshooting for common issues}

---

*Last updated: {generation timestamp}*
*Generated from: {spec.md path}, {implementation files}*
```

## Generation Instructions for AI Agents

### Step 1: Extract User Stories

```python
# Pseudocode for extraction
for user_story in spec.md:
    if user_story.startswith("US-"):
        title = user_story.title
        actor = user_story.actor  # "As a {actor}"
        goal = user_story.goal    # "I want to {goal}"
        benefit = user_story.benefit  # "So that {benefit}"

        # Map to documentation section
        section_title = goal  # Use goal as section title
        overview = f"{actor} can {goal}. This allows {benefit}."
```

### Step 2: Extract Steps from Acceptance Scenarios

```python
for acceptance_scenario in spec.md:
    if acceptance_scenario.fr_id == current_feature:
        # Parse GIVEN/WHEN/THEN structure
        prerequisites = acceptance_scenario.given  # → "Before You Begin"
        actions = acceptance_scenario.when  # → "Step-by-Step"
        outcomes = acceptance_scenario.then  # → "Expected Result"

        # Generate step-by-step instructions
        step = {
            "title": infer_action_from_when(actions),
            "instructions": convert_to_imperative(actions),
            "example": format_as_example(given, when, then),
            "expected_result": outcomes
        }
```

### Step 3: Extract Troubleshooting from Edge Cases

```python
for scenario in spec.md.acceptance_scenarios:
    if "error" in scenario.then or "invalid" in scenario.when:
        problem = scenario.when  # What went wrong
        solution = infer_resolution(scenario.then)

        troubleshooting_entry = {
            "problem": problem,
            "solution": solution,
            "reference": scenario.id
        }
```

### Step 4: Generate FAQ from Edge Cases

```python
edge_cases = [s for s in acceptance_scenarios if s.tags.includes("edge")]

for edge_case in edge_cases:
    question = infer_question_from_scenario(edge_case.when)
    answer = edge_case.then + explanation_from_implementation

    faq_entry = {"question": question, "answer": answer}
```

### Step 5: Cross-Reference Building

```python
# Link to related documentation
related_features = find_features_with_shared_entities(current_feature)
for feature in related_features:
    add_see_also_link(f"docs/user-guide/{feature.slug}.md")

# Link to API reference if feature has API endpoints
if current_feature.has_api_endpoints:
    add_see_also_link(f"docs/api-reference/endpoints/{feature.api_path}.md")

# Link to troubleshooting
if current_feature.has_error_scenarios:
    add_see_also_link(f"docs/troubleshooting/common-issues.md#{feature.slug}")
```

## Example Output

Given this User Story:

```markdown
### US-001: User Registration

**As a** new user
**I want to** create an account with my email and password
**So that** I can access personalized features
```

And this Acceptance Scenario:

```markdown
### AS-001: Successful Registration

**GIVEN** I am on the registration page
**AND** I have a valid email address
**WHEN** I enter my email "user@example.com"
**AND** I enter a password with at least 8 characters
**AND** I click "Create Account"
**THEN** I should see a success message
**AND** I should receive a verification email
**AND** I should be redirected to the dashboard
```

Generate:

```markdown
# Creating Your Account

> **Target Audience**: End users
> **Skill Level**: Beginner
> **Estimated Time**: 5 minutes

## Overview

Create a new account to access personalized features like saved preferences, custom dashboards, and collaboration tools.

## Before You Begin

**Prerequisites:**
- A valid email address
- Internet connection

**What You'll Need:**
- Email address you have access to (for verification)

## Step-by-Step Guide

### Step 1: Navigate to Registration Page

1. Go to the application homepage
2. Click **Sign Up** in the top-right corner
3. You'll see the registration form

### Step 2: Enter Your Email

1. In the **Email** field, enter your email address
2. Example: `user@example.com`

**Expected Result:**
- Email field should display your entered email
- No validation errors should appear (if email is valid)

### Step 3: Create a Strong Password

1. In the **Password** field, enter a password with at least 8 characters
2. Your password should include:
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number

**Troubleshooting:**
- **Problem**: "Password too weak" error appears
  **Solution**: Ensure your password meets the requirements above

### Step 4: Complete Registration

1. Click the **Create Account** button
2. Wait for the confirmation screen (usually 1-2 seconds)

**Expected Result:**
- Success message: "Account created successfully!"
- Verification email sent to your inbox
- Automatic redirect to your dashboard

## What's Next

After creating your account:
- [Verify your email address](./email-verification.md)
- [Set up your profile](./profile-setup.md)
- [Explore the dashboard](./dashboard-overview.md)

## Tips and Best Practices

- ✅ **Do**: Use a unique password you don't use elsewhere
- ✅ **Do**: Check your spam folder if verification email doesn't arrive
- ❌ **Don't**: Share your password with anyone
- ❌ **Don't**: Use simple passwords like "password123"

## Common Questions

**Q: I didn't receive the verification email. What should I do?**
A: Check your spam folder first. If not there, click "Resend Verification Email" on the dashboard.

**Q: Can I change my email address later?**
A: Yes, you can update your email in Account Settings after verifying your current email.

**Q: What if my email is already registered?**
A: You'll see an error message. Try [resetting your password](./password-reset.md) if you forgot it.

## See Also

- [Email Verification Guide](./email-verification.md)
- [Password Reset](./password-reset.md)
- [Troubleshooting Login Issues](../troubleshooting/login-errors.md)

---

*Last updated: 2024-03-20 14:30 UTC*
*Generated from: specs/features/001-registration/spec.md, src/auth/register.ts*
```

## Auto-Update Markers

When regenerating documentation, use markers to preserve manual edits:

```markdown
<!-- speckit:auto:user-guide:registration -->
{Auto-generated content here}
<!-- /speckit:auto:user-guide:registration -->

<!-- MANUAL SECTION - PRESERVED ON REGENERATION -->
## Additional Notes from Support Team

Users often ask about...
<!-- /MANUAL SECTION -->
```

## Audience Adaptation Rules

Adapt language based on target audience (from constitution or concept):

| Audience Type | Language Style | Technical Detail |
|---------------|---------------|------------------|
| Non-technical users | Simple, conversational, avoid jargon | Minimal, focus on UI |
| Business users | Professional, goal-oriented | Medium, mention workflows |
| Power users | Efficient, shortcut-focused | High, include keyboard shortcuts |
| Developers using product | Technical but clear | Very high, mention APIs |

## Accessibility Guidelines

Ensure generated documentation is accessible:

- Use clear hierarchical heading structure (H1 → H2 → H3)
- Include alt text for all images/screenshots
- Use descriptive link text (not "click here")
- Provide keyboard navigation instructions
- Use tables for structured data, not layout
- Ensure code examples are readable by screen readers

## Quality Checks

Before finalizing user guide section:

- [ ] All US-xxx referenced have corresponding documentation
- [ ] All AS-xxx success scenarios have step-by-step instructions
- [ ] All edge cases have troubleshooting entries
- [ ] Cross-references to related docs exist
- [ ] Examples are concrete (no "enter your value here")
- [ ] Estimated time is realistic (test with sample user)
- [ ] Screenshots placeholders added where UI is mentioned
- [ ] No broken internal links
- [ ] Consistent terminology with glossary

## Integration with Other Templates

This template works with:

- **troubleshooting-section.md** — generates troubleshooting entries from same AS-xxx
- **faq-template.md** — generates FAQ from same edge cases
- **api-reference-template.md** — links to API docs if feature has endpoints

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
