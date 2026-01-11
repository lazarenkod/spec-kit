# Feature Specification: {{feature_name}}

**Status**: EXTRACTED (Reverse-Engineered)
**Extraction Date**: {{ISO_DATE}}
**Extraction Source**: Codebase analysis
**Average Confidence**: {{average_confidence}}

> ⚠️ **IMPORTANT**: This specification was automatically extracted from code.
> Review all requirements (especially those marked with low confidence < 0.70) for hallucinations before merging into canonical spec.md.

---

## Feature Description

{{feature_description}}

<!-- AUTO-GENERATED: This description was synthesized from discovered APIs and entities. Verify accuracy. -->

---

## User Stories

{{#each user_stories}}
### US{{@index+1}}: {{this.title}}

**As a** {{this.actor}}
**I want to** {{this.action}}
**So that** {{this.benefit}}

<!-- Confidence: {{this.confidence}} | Source: {{this.source}} -->

{{/each}}

---

## Functional Requirements

{{#each functional_requirements}}
### {{this.id}}: {{this.title}}

<!-- Confidence: {{this.confidence}} | Source: {{this.source}} | File: {{this.file}}:{{this.line}} -->
<!-- Hallucination Risk: {{this.hallucination_risk}} -->

{{this.description}}

{{#if this.api_signature}}
**API**: `{{this.api_signature}}`
{{/if}}

{{#if this.endpoint}}
**Endpoint**: `{{this.method}} {{this.endpoint}}`
{{/if}}

{{#if this.entity}}
**Domain Entity**: {{this.entity}}
{{/if}}

{{#if this.confidence < 0.70}}
> ⚠️ **Low Confidence ({{this.confidence}})**: Verify this requirement against actual code behavior.
{{/if}}

{{#if this.existing_annotation}}
✅ **Verified**: This requirement has explicit @speckit:{{this.existing_annotation}} annotation in code.
{{/if}}

---

{{/each}}

## Acceptance Scenarios

{{#each acceptance_scenarios}}
### {{this.id}}: {{this.title}}

<!-- Confidence: {{this.confidence}} | Source: {{this.source}} | File: {{this.file}}:{{this.line}} -->

**Mapped FRs**: {{#each this.fr_ids}}{{this}}, {{/each}}

**Given** {{this.gherkin.given}}
**When** {{this.gherkin.when}}
**Then** {{this.gherkin.then}}

{{#if this.test_file}}
**Test**: {{this.test_file}}:{{this.test_line}}
{{/if}}

{{#if this.confidence < 0.70}}
> ⚠️ **Low Confidence ({{this.confidence}})**: Verify Gherkin mapping against actual test assertions.
{{/if}}

---

{{/each}}

## Edge Cases

{{#if edge_cases.length > 0}}
{{#each edge_cases}}
### EC-{{@index+1}}: {{this.description}}

<!-- Confidence: {{this.confidence}} | Source: {{this.source}} -->

{{this.handling}}

{{/each}}
{{else}}
> ⚠️ **No edge cases extracted**: Edge case handling not detected in code. Manual review recommended.
{{/if}}

---

## Non-Functional Requirements

{{#if nfrs.length > 0}}
{{#each nfrs}}
### NFR-{{@index+1}}: {{this.category}} - {{this.title}}

<!-- Confidence: {{this.confidence}} | Source: {{this.source}} -->

{{this.description}}

{{#if this.measurable}}
**Target**: {{this.target}}
{{else}}
> ⚠️ **Not measurable**: No specific performance/security targets found in code.
{{/if}}

{{/each}}
{{else}}
> ℹ️ **No NFRs extracted**: Performance, security, or scalability requirements not explicitly defined in code.
{{/if}}

---

## Out of Scope

<!-- Items excluded from extraction (marked with @internal, or explicitly out-of-scope) -->

{{#if out_of_scope.length > 0}}
{{#each out_of_scope}}
- {{this.description}} (Reason: {{this.reason}})
{{/each}}
{{else}}
> ℹ️ **No explicit out-of-scope markers found**
{{/if}}

---

## Traceability Matrix

| FR ID | Description | Implementation | Test Coverage | Confidence |
|-------|-------------|----------------|---------------|------------|
{{#each traceability_matrix}}
| {{this.fr_id}} | {{truncate this.description 50}} | {{this.file}}:{{this.line}} | {{this.test_status}} | {{this.confidence}} |
{{/each}}

---

## Extraction Metadata

**Scan Scope**: {{scan_scope_patterns}}
**Language**: {{primary_language}}
**Framework**: {{detected_framework}}

**Discovery Statistics**:
- Files scanned: {{files_scanned}}
- APIs discovered: {{apis_discovered}}
- Entities discovered: {{entities_discovered}}
- Tests analyzed: {{tests_analyzed}}
- Existing annotations found: {{existing_annotations_found}}

**Confidence Breakdown**:
| Confidence | Count | Percentage |
|------------|-------|------------|
| Explicit (0.90-1.00) | {{explicit_count}} | {{explicit_percentage}}% |
| High (0.70-0.89) | {{high_count}} | {{high_percentage}}% |
| Medium (0.50-0.69) | {{medium_count}} | {{medium_percentage}}% |
| Low (0.00-0.49) | {{low_count}} | {{low_percentage}}% |

**Hallucination Warnings**: {{hallucination_count}}
{{#each hallucination_warnings}}
- **{{this.fr_id}}** [{{this.severity}}]: {{this.reason}}
{{/each}}

---

## Next Steps

1. **Review low-confidence items** ({{low_confidence_count}} FRs with confidence < 0.70)
2. **Verify hallucination warnings** ({{hallucination_count}} items flagged)
3. **Compare with canonical spec** (see drift-report.md)
4. **Merge verified FRs** into canonical spec.md using /speckit.specify

**Commands**:
- Compare with canonical: See `reverse-engineered/drift-report.md`
- Merge to canonical: `/speckit.specify` (manually merge verified FRs)
- Re-extract: `/speckit.reverse-engineer --scope "{{scan_scope_patterns}}"`

---

**Extraction Manifest**: `.extraction-manifest.yaml`
**Drift Report**: `drift-report.md`
**Extraction Log**: `extraction-log.md`

---

> 🤖 Generated by Spec Kit Reverse-Engineering (v1.0.0)
> Extraction ID: {{extraction_id}}
> Generated: {{ISO_DATE}}
