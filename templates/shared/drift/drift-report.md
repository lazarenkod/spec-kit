# Drift Detection Report

**Feature**: {{FEATURE_ID}}-{{feature_name}}
**Generated**: {{ISO_DATE}}
**Scope**: {{language}} files in {{scan_scope.patterns}}
**Analyzer**: Pass AA (Spec-Code Drift Detection)

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Drift Items** | {{total_drift_items}} |
| **Forward Drift (Spec → Code)** | {{forward_drift_count}} |
| **Reverse Drift (Code → Spec)** | {{reverse_drift_count}} |
| **Behavioral Drift** | {{behavioral_drift_count}} |

### Severity Breakdown

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | {{critical_count}} | {{critical_status}} |
| HIGH | {{high_count}} | {{high_status}} |
| MEDIUM | {{medium_count}} | {{medium_status}} |
| LOW | {{low_count}} | {{low_status}} |

**Overall Status**: {{overall_status}}
{{#if critical_count > 0}}🔴 **FAIL** - Critical drift must be resolved{{/if}}
{{#if critical_count == 0 && high_count > 5}}🟡 **WARN** - High drift items require attention{{/if}}
{{#if critical_count == 0 && high_count <= 5}}🟢 **PASS** - Drift within acceptable limits{{/if}}

---

## Coverage Metrics

| Metric | Percentage | Target | Status |
|--------|------------|--------|--------|
| **FR → Code Coverage** | {{fr_to_code_percentage}}% | ≥ 80% | {{fr_coverage_status}} |
| **Code → Spec Coverage** | {{code_to_spec_percentage}}% | ≥ 70% | {{code_coverage_status}} |
| **Annotation Coverage** | {{annotation_coverage}}% | ≥ 60% | {{annotation_status}} |

### Coverage Breakdown

**FR → Code Coverage**: {{implemented_frs}}/{{total_frs}} functional requirements have implementation
**Code → Spec Coverage**: {{documented_apis}}/{{total_public_apis}} public APIs have spec coverage
**Annotation Coverage**: {{annotated_implementations}}/{{total_implementations}} implementations have @speckit annotations

---

## Drift Items

{{#each drift_items}}
### DRIFT-{{@index+1}}: {{this.message}} ({{this.severity}})

**Type**: {{this.type}} ({{this.direction}} drift)
**Location**: {{this.location}}
{{#if this.requirement}}**Requirement**: {{this.requirement}}{{/if}}
{{#if this.signature}}**API Signature**: `{{this.signature}}`{{/if}}
{{#if this.scenario}}**Scenario**: {{this.scenario}}{{/if}}

**Current State**:
{{#if this.direction == "forward"}}
- ✅ Defined in spec.md
- ❌ Not found in codebase
- ❌ No @speckit annotation
{{/if}}
{{#if this.direction == "reverse"}}
- ❌ Not in spec.md
- ✅ Implementation exists
- {{#if this.annotations}}✅{{else}}❌{{/if}} @speckit annotation present
{{/if}}
{{#if this.direction == "bidirectional"}}
- ⚠️ Spec and code exist but semantics may differ
- 🔍 LLM confidence: {{this.confidence}}
{{/if}}

**Recommendation**: {{this.recommendation}}

{{#if this.auto_fix.available}}
**Auto-fix Available**: ✅ Yes - {{this.auto_fix.action}}
```diff
{{this.auto_fix.preview}}
```
{{/if}}
{{#if this.auto_fix.manual_action}}
**Manual Action Required**: {{this.auto_fix.manual_action}}
{{/if}}

{{#if this.details}}
**Details**: {{this.details}}
{{/if}}

---

{{/each}}

## Drift by Type

| Type | Count | Severity | Direction |
|------|-------|----------|-----------|
| Unimplemented Requirement | {{count_type "unimplemented_requirement"}} | HIGH | Forward (Spec → Code) |
| Undocumented API | {{count_type "undocumented_api"}} | HIGH | Reverse (Code → Spec) |
| Orphan Annotation | {{count_type "orphan_annotation"}} | MEDIUM | Reverse (Code → Spec) |
| Missing Test | {{count_type "missing_test"}} | MEDIUM | Forward (Spec → Code) |
| Behavioral Drift | {{count_type "behavioral_drift"}} | MEDIUM | Bidirectional |
| Orphan Test Annotation | {{count_type "orphan_test_annotation"}} | LOW | Reverse (Code → Spec) |

---

## Recommendations

### Immediate Actions (CRITICAL + HIGH)

{{#each critical_high_items}}
{{@index+1}}. **{{this.type}}**: {{this.message}}
   - Location: {{this.location}}
   - Action: {{this.recommendation}}
{{/each}}

{{#if critical_high_items.length == 0}}
✅ No critical or high severity drift items
{{/if}}

### Medium Priority

{{#each medium_items}}
{{@index+1}}. **{{this.type}}**: {{this.message}}
   - Location: {{this.location}}
   - Action: {{this.recommendation}}
{{/each}}

{{#if medium_items.length == 0}}
✅ No medium severity drift items
{{/if}}

### Low Priority (Informational)

{{#if low_items.length > 0}}
- {{low_items.length}} low severity items detected
- Review when time permits
- See individual DRIFT-xxx items above for details
{{else}}
✅ No low severity drift items
{{/if}}

---

## Coverage Improvement Plan

{{#if fr_to_code_percentage < 80}}
### FR → Code Coverage ({{fr_to_code_percentage}}% → 80%)

**Gap**: {{80 - fr_to_code_percentage}}% improvement needed

**Missing FRs** (no implementation):
{{#each unimplemented_frs}}
- **{{this.id}}**: {{this.description}}
  - Recommendation: {{this.recommendation}}
{{/each}}

**Action**: Implement missing FRs or move to "Out of Scope" section in spec.md
{{/if}}

{{#if code_to_spec_percentage < 70}}
### Code → Spec Coverage ({{code_to_spec_percentage}}% → 70%)

**Gap**: {{70 - code_to_spec_percentage}}% improvement needed

**Undocumented APIs** (no spec):
{{#each undocumented_apis}}
- **{{this.signature}}** ({{this.file}}:{{this.line}})
  - Recommendation: {{this.recommendation}}
{{/each}}

**Action**: Add FR-xxx entries to spec.md or mark internal with @internal comment
{{/if}}

{{#if annotation_coverage < 60}}
### Annotation Coverage ({{annotation_coverage}}% → 60%)

**Gap**: {{60 - annotation_coverage}}% improvement needed

**Action**: Add @speckit:FR:FR-xxx annotations to implementations
- Target files: {{low_annotation_files}}
- Estimated effort: {{annotation_gap_count}} annotations to add
{{/if}}

{{#if fr_to_code_percentage >= 80 && code_to_spec_percentage >= 70 && annotation_coverage >= 60}}
✅ **All coverage targets met** - traceability is strong
{{/if}}

---

## Traceability Matrix

### FR → Code Mapping

| FR ID | Description | Implementation | Test | Status |
|-------|-------------|----------------|------|--------|
{{#each fr_traceability}}
| {{this.fr_id}} | {{truncate this.description 50}} | {{this.file}}:{{this.line}} | {{this.test_file}} | {{this.status}} |
{{/each}}

### Public API → Spec Mapping

| API | File:Line | FR Mapping | Status |
|-----|-----------|------------|--------|
{{#each api_traceability}}
| `{{truncate this.signature 60}}` | {{this.file}}:{{this.line}} | {{this.fr_id}} | {{this.status}} |
{{/each}}

---

## Scan Details

**Scan Scope**:
```yaml
patterns:
{{#each scan_scope.patterns}}
  - {{this}}
{{/each}}

exclude:
{{#each scan_scope.exclude}}
  - {{this}}
{{/each}}
```

**Discovered**:
- {{discovered_files}} files scanned
- {{discovered_apis}} public APIs found
- {{discovered_annotations}} @speckit annotations parsed
- {{discovered_tests}} test files analyzed

**Language-Specific Settings**:
- Primary language: {{language}}
- Analyzer: {{analyzer_name}}
- Framework detection: {{detected_frameworks}}

---

## Quality Gates

{{#if critical_count == 0}}
✅ **QG-DRIFT-001 (CRITICAL)**: No critical drift items
{{else}}
❌ **QG-DRIFT-001 (CRITICAL)**: {{critical_count}} critical drift items - **BLOCKS PROCEED**
{{/if}}

{{#if high_count <= 5}}
✅ **QG-DRIFT-002 (HIGH)**: High drift items within acceptable range ({{high_count}}/5)
{{else}}
⚠️ **QG-DRIFT-002 (HIGH)**: {{high_count}} high drift items - review recommended
{{/if}}

{{#if fr_to_code_percentage >= 80}}
✅ **QG-DRIFT-003 (HIGH)**: FR → Code coverage meets threshold ({{fr_to_code_percentage}}% ≥ 80%)
{{else}}
❌ **QG-DRIFT-003 (HIGH)**: FR → Code coverage below threshold ({{fr_to_code_percentage}}% < 80%)
{{/if}}

{{#if code_to_spec_percentage >= 70}}
✅ **QG-DRIFT-004 (HIGH)**: Code → Spec coverage meets threshold ({{code_to_spec_percentage}}% ≥ 70%)
{{else}}
⚠️ **QG-DRIFT-004 (HIGH)**: Code → Spec coverage below threshold ({{code_to_spec_percentage}}% < 70%)
{{/if}}

---

## Next Steps

{{#if critical_count > 0}}
1. **IMMEDIATE**: Resolve {{critical_count}} critical drift items
2. Address {{high_count}} high severity items before merge
3. Plan medium priority items for next sprint
{{else if high_count > 5}}
1. Address {{high_count}} high severity items (target: ≤ 5)
2. Improve coverage metrics to meet thresholds
3. Review medium priority items
{{else}}
1. ✅ Drift within acceptable limits
2. Monitor coverage metrics over time
3. Address low priority items opportunistically
{{/if}}

**Commands**:
- Re-run drift detection: `/speckit.analyze --profile drift`
- Full QA verification: `/speckit.analyze --profile qa`
- Update spec: `/speckit.specify`

---

**Report Generated**: {{ISO_DATE}}
**Spec Kit Version**: {{speckit_version}}
**Drift Detection Version**: v1.0.0
