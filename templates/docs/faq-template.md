# FAQ Template

This template generates FAQ documentation from edge cases, user stories, and common questions.

## Usage

This template is used by:
- `/speckit.specify` — generates FAQ seeds from AS-xxx edge cases
- `/speckit.implement` — enriches FAQ with implementation details
- `/speckit.docs build --type faq` — regenerates FAQ documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| spec.md AS-xxx | Edge cases, error scenarios, boundary conditions |
| spec.md US-xxx | Common user questions from user stories |
| issue tracker | Frequently asked questions from GitHub/GitLab issues |
| support logs | Common support requests (if available) |
| documentation | Cross-references to detailed guides |

## Template Structure

```markdown
# Frequently Asked Questions (FAQ)

> Last Updated: {generation timestamp}

This FAQ answers common questions about {Project Name}. Can't find your answer? Check our [full documentation]({docs-url}) or [ask in discussions]({discussions-url}).

## Quick Links

- [Getting Started](#getting-started)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Account & Billing](#account--billing) (if applicable)
- [Technical](#technical)
- [Contributing](#contributing)

---

## Getting Started

### What is {Project Name}?

{One-paragraph description from spec.md Objective}

**Key Features:**
{From spec.md FR-xxx}
- {Feature 1}
- {Feature 2}
- {Feature 3}

**Learn more:** [User Guide](./user-guide/index.md)

---

### How do I install {Project Name}?

**Quick Start (5 minutes):**
```bash
{Quick install command from RUNNING.md}
```

**Detailed Instructions:** [Installation Guide](./installation/quick-start.md)

**System Requirements:**
- {OS requirement}
- {Memory requirement}
- {Other requirements}

---

### Do I need an account?

{From spec.md authentication requirements}

**Answer:** {Yes/No/It depends}

{Explanation}

**Related:**
- [Creating an Account](./user-guide/account-creation.md)
- [Authentication Guide](./user-guide/authentication.md)

---

### Is {Project Name} free?

{From constitution or concept}

**Answer:** {Pricing model}

{Explanation}

**Learn more:** [Pricing Page]({pricing-url}) (if applicable)

---

## Features

{Generated from FR-xxx in spec.md}

### {Feature Category}

#### Can I {common question from US-xxx}?

**Answer:** {Yes/No/Partially}

{Explanation with reference to AS-xxx}

**How to:**
1. {Step 1 from user guide}
2. {Step 2}
3. {Step 3}

**Example:**
{Example from AS-xxx GIVEN/WHEN/THEN}

**Learn more:** [{Feature} Guide](./user-guide/{feature}.md)

---

#### What happens if {edge case from AS-xxx}?

**Scenario:** {AS-xxx edge case description}

**Answer:** {Behavior from AS-xxx THEN clause}

**Why:** {Technical explanation}

**Workaround:** {If applicable}

---

#### Can I use {Feature A} with {Feature B}?

**Answer:** {Yes/No/With limitations}

{Explanation of compatibility}

**Limitations:**
- {Limitation 1}
- {Limitation 2}

**Alternatives:**
- {Alternative approach}

---

## Troubleshooting

{Generated from common errors in AS-xxx and support logs}

### Why am I seeing "{Error Message}"?

**Error:** `{Error Code/Message}`

**Common Causes:**
1. {Cause from AS-xxx edge case}
2. {Cause from error handling code}

**How to Fix:**
```bash
{Fix command}
```

**Still not working?** See [Troubleshooting Guide](./troubleshooting/common-issues.md#{error-anchor})

---

### The application is slow. How can I improve performance?

**Quick Checks:**
1. Check system resources: `{resource check command}`
2. Clear cache: `{cache clear command}`
3. Check network latency: `{network test command}`

**Common Issues:**
- {Performance issue 1} → [Fix](./troubleshooting/performance.md#issue-1)
- {Performance issue 2} → [Fix](./troubleshooting/performance.md#issue-2)

**Detailed Guide:** [Performance Optimization](./admin-guide/performance-tuning.md)

---

### I forgot my password. How do I reset it?

**Steps:**
1. {Step from user guide}
2. {Step 2}
3. {Step 3}

**Didn't receive reset email?**
- Check spam folder
- Wait 5 minutes and try again
- Contact support: {support-email}

**Learn more:** [Password Reset Guide](./user-guide/password-reset.md)

---

### Can I recover deleted data?

**Answer:** {Yes/No/It depends}

{Explanation}

**Recovery Options:**
- {Option 1 with timeline}
- {Option 2 with requirements}

**Prevention:**
- Enable backups: [Backup Guide](./admin-guide/backup-restore.md)

---

## Account & Billing

{If applicable}

### How do I upgrade my plan?

{Upgrade process}

**Related:** [Pricing Plans]({pricing-url})

---

### How do I cancel my subscription?

{Cancellation process}

**What happens after cancellation:**
- {Consequence 1}
- {Consequence 2}

---

### Do you offer refunds?

{Refund policy}

---

## Technical

{For developers and advanced users}

### What technologies does {Project Name} use?

{From plan.md tech stack}

**Backend:**
- {Technology 1}
- {Technology 2}

**Frontend:**
- {Technology 1}
- {Technology 2}

**Infrastructure:**
- {Technology 1}
- {Technology 2}

**Full Stack:** [Architecture Overview](./developer-guide/architecture/overview.md)

---

### Is there an API?

**Answer:** {Yes/No}

{API description}

**API Documentation:** [API Reference](./developer-guide/api-reference/index.md)

**Authentication:** {Auth method}

**Rate Limits:** {Rate limit info}

---

### Can I self-host {Project Name}?

**Answer:** {Yes/No}

{Explanation}

**Installation Guide:** [Production Deployment](./admin-guide/deployment.md)

**System Requirements:** [Installation Guide](./installation/prerequisites.md)

---

### Is {Project Name} open source?

**License:** {License name}

**Repository:** {Repository URL}

**Contributing:** [Contributing Guide](./contributing.md)

---

### How do I integrate {Project Name} with {External Service}?

**Integration Available:** {Yes/No/Via API}

{Integration instructions}

**Documentation:** [Integration Guide](./developer-guide/integrations/{service}.md)

---

### Does {Project Name} support {Feature/Technology}?

**Answer:** {Yes/No/Planned/Not planned}

{Explanation}

**Alternatives:**
- {Alternative 1}
- {Alternative 2}

**Feature Requests:** [Request Feature]({feature-request-url})

---

## Security & Privacy

### Is {Project Name} secure?

**Security Measures:**
{From spec.md Security Considerations}
- {Security measure 1}
- {Security measure 2}

**Compliance:** {Compliance standards if applicable}

**Security Policy:** [Security Documentation](./SECURITY.md)

**Report Security Issues:** {security-email}

---

### What data do you collect?

{From privacy policy or spec}

**Data Collection:**
- {Data type 1}: {Purpose}
- {Data type 2}: {Purpose}

**Privacy Policy:** [{Privacy Policy URL}]({privacy-url})

**Data Retention:** {Retention policy}

---

### Can I export my data?

**Answer:** {Yes/No}

{Export process}

**Export Formats:** {Formats available}

**Data Portability:** [Data Export Guide](./user-guide/data-export.md)

---

## Contributing

### How can I contribute?

**Ways to Contribute:**
1. **Code contributions:** [Contributing Guide](./contributing.md)
2. **Bug reports:** [Issue Tracker]({issues-url})
3. **Feature requests:** [Discussions]({discussions-url})
4. **Documentation:** [Docs Contributions](./contributing.md#documentation)
5. **Translations:** [Translation Guide](./contributing.md#translations) (if applicable)

**First-time contributor?** Look for [`good first issue`]({issues-url}?q=label%3A%22good+first+issue%22) label.

---

### I found a bug. How do I report it?

**Bug Report Checklist:**
- [ ] Search existing issues
- [ ] Can you reproduce it?
- [ ] Collect diagnostic information

**Report Here:** [Issue Tracker]({issues-url})

**Include:**
- Steps to reproduce
- Expected vs actual behavior
- System information
- Logs (if applicable)

**Template:** Use our [bug report template]({bug-template-url})

---

### Can I request a feature?

**Yes!** We welcome feature requests.

**How to Request:**
1. Search existing requests: [Discussions]({discussions-url})
2. Open new discussion with:
   - Use case
   - Expected behavior
   - Why it's valuable

**Approval Process:** {Feature approval process}

---

## Still Have Questions?

### Search Documentation

Use the search bar at the top to find specific topics.

**Main Sections:**
- [User Guide](./user-guide/index.md) — How to use features
- [Admin Guide](./admin-guide/index.md) — Installation and configuration
- [Developer Guide](./developer-guide/index.md) — API and integration
- [Troubleshooting](./troubleshooting/index.md) — Common problems

---

### Community

**Get help from the community:**
- 💬 Discussions: {discussions-url}
- 💬 Chat: {chat-url} (Discord/Slack)
- 📧 Mailing List: {mailing-list-url}
- 🐦 Twitter: {twitter-url}

---

### Support

**Need direct support?**
- 📧 Email: {support-email}
- 📝 Support Portal: {support-portal-url}
- ⏰ Response Time: {expected-response-time}

**For urgent issues:**
- Priority support (if available): {priority-support-url}
- Emergency contact: {emergency-contact}

---

## FAQ Maintenance

**This FAQ is generated from:**
- User Stories and Acceptance Scenarios in spec.md
- Common issues from troubleshooting guides
- Support tickets and community questions

**Help improve this FAQ:**
- Suggest additions: [Discussions]({discussions-url})
- Report outdated answers: [Issue Tracker]({issues-url})

---

*Last updated: {generation timestamp}*
*Generated from: {spec.md AS-xxx}, {issue tracker analysis}, {support logs}*
```

## Generation Instructions for AI Agents

### Step 1: Extract Questions from Edge Cases (AS-xxx)

```python
faq_entries = []

for scenario in spec.md.acceptance_scenarios:
    # Edge cases often represent common questions
    if "edge" in scenario.tags or "boundary" in scenario.tags:
        question = infer_question_from_scenario(scenario)
        answer = scenario.then + additional_explanation

        faq_entries.append({
            "category": categorize_by_feature(scenario.fr_id),
            "question": question,
            "answer": answer,
            "source": scenario.id,
            "related_doc": find_related_guide(scenario)
        })
```

### Step 2: Generate Questions from User Stories

```python
for user_story in spec.md.user_stories:
    # Common questions about capabilities
    question = f"Can I {user_story.goal}?"
    answer = f"Yes! {user_story.benefit}"

    faq_entries.append({
        "category": "Features",
        "question": question,
        "answer": answer + "\n\nHow to: " + link_to_user_guide(user_story),
        "source": user_story.id
    })
```

### Step 3: Extract from Issue Tracker

```python
if github_issues_available:
    common_questions = analyze_github_issues(
        labels=["question", "faq"],
        min_frequency=3  # Asked at least 3 times
    )

    for issue in common_questions:
        faq_entries.append({
            "category": categorize(issue),
            "question": issue.title,
            "answer": extract_accepted_answer(issue),
            "source": issue.url
        })
```

### Step 4: Categorize and Sort

```python
categories = {
    "Getting Started": [],
    "Features": [],
    "Troubleshooting": [],
    "Technical": [],
    "Security & Privacy": [],
    "Contributing": []
}

for entry in faq_entries:
    category = entry["category"]
    categories[category].append(entry)

# Sort by frequency/importance
for category in categories:
    categories[category].sort(key=lambda x: x.frequency, reverse=True)
```

### Step 5: Add Cross-References

```python
for entry in faq_entries:
    # Find related documentation
    related_docs = find_related_documentation(entry)

    # Add "Learn more" links
    entry["see_also"] = related_docs

    # Add "Related questions" links
    entry["related_questions"] = find_related_faq(entry, faq_entries)
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:faq:authentication -->
{Auto-generated authentication FAQ}
<!-- /speckit:auto:faq:authentication -->

<!-- MANUAL FAQ ENTRY -->
### Custom question added by team
Answer...
<!-- /MANUAL FAQ ENTRY -->
```

## Quality Checks

- [ ] All major features have FAQ entries
- [ ] Common error scenarios covered
- [ ] Questions are clear and searchable
- [ ] Answers are concise but complete
- [ ] Cross-references to detailed guides
- [ ] No duplicate questions
- [ ] Categories logical and balanced
- [ ] Contact information current

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
