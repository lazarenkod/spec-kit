# {{PLATFORM/TECHNOLOGY}} Technical Constraints

> **Purpose**: Documented technical limitations, quotas, and rate limits for {{PLATFORM/TECHNOLOGY}}. Used during planning to validate NFRs and generate constraint-driven requirements.
>
> **Evidence Standard**: [AUTHORITATIVE] tier required (official vendor documentation <90 days old).

---

## Platform Overview

**Vendor**: {{Company Name}}
**Technology**: {{Technology/Service Name}}
**Documentation**: {{Official Docs URL}}
**Last Updated**: YYYY-MM-DD
**Evidence Tier**: AUTHORITATIVE

---

## Rate Limits

| Operation | Limit | Scope | Penalty | Workaround |
|-----------|-------|-------|---------|------------|
| API requests | {{N}} req/sec | Per account | 429 Too Many Requests | Exponential backoff |
| {{Operation}} | {{Limit}} | {{Scope}} | {{Error}} | {{Solution}} |

### Rate Limit Implementation Notes

```
IF response.status == 429:
  retry_after = response.headers['Retry-After']
  sleep(retry_after)
  retry_request()
```

**Best Practice**: Implement exponential backoff with jitter

---

## Resource Quotas

| Resource | Limit | Hard/Soft | Upgrade Path |
|----------|-------|-----------|--------------|
| {{Resource}} | {{Limit}} | {{Type}} | {{How to increase}} |

### Quota Monitoring

- Alert threshold: {{X%}} of quota
- Escalation: {{Process}}
- Cost impact: {{Estimate}}

---

## Performance Constraints

| Metric | Limit | Context | Impact |
|--------|-------|---------|--------|
| Latency | {{N}} ms | {{P50/P95/P99}} | {{User-facing impact}} |
| Timeout | {{N}} sec | {{Operation}} | {{Failure mode}} |
| Payload size | {{N}} MB | {{Max request/response}} | {{413 error}} |

### Performance Optimization

{{Guidance on how to work within constraints}}

---

## Storage Limits

| Type | Limit | Retention | Cost |
|------|-------|-----------|------|
| {{Storage type}} | {{Size}} | {{Duration}} | {{$/unit}} |

---

## Auto-NFR Generation

### Performance NFRs

```markdown
NFR-PERF-{{TECH}}-001: Handle API rate limit ({{N}} req/sec) [HIGH]
- Acceptance: Exponential backoff implemented for 429 responses
- Evidence: {{TECH}} Rate Limits [AUTHORITATIVE]
- Constraint: {{N}} req/sec per {{scope}}
- Traceability: → {{Related FRs}}
```

### Reliability NFRs

```markdown
NFR-REL-{{TECH}}-001: Handle timeout gracefully ({{N}} sec limit) [MEDIUM]
- Acceptance: Timeout handling with retry logic
- Evidence: {{TECH}} Timeout Documentation [AUTHORITATIVE]
- Constraint: {{N}} second timeout
- Traceability: → {{Related FRs}}
```

---

## Known Issues & Gotchas

### Issue: {{Issue Name}}

**Description**: {{What's the problem?}}
**Workaround**: {{How to handle it?}}
**Status**: {{Open | Acknowledged | Fixed}}
**Evidence**: {{Stack Overflow link, GitHub issue, vendor docs}}

---

## Integration Checklist

When using {{TECHNOLOGY}} in architecture:

- [ ] Rate limits validated against expected load
- [ ] Retry logic implemented for 429/503 responses
- [ ] Timeout handling configured
- [ ] Monitoring alerts set at {{X%}} of limits
- [ ] Cost estimation includes {{TECH}} usage
- [ ] Fallback strategy defined for quota exhaustion

---

## Maintenance

**Last Updated**: YYYY-MM-DD
**Reviewed By**: [Agent or Human]
**Evidence Tier**: AUTHORITATIVE
**Source URL**: {{Vendor docs URL}}
**Freshness**: {{Days since last update}} days (threshold: 90 days)
