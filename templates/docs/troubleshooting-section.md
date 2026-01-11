# Troubleshooting Section Template

This template generates troubleshooting documentation from error scenarios, acceptance tests, and common failure patterns.

## Usage

This template is used by:
- `/speckit.implement` — generates troubleshooting guide from error handling code
- `/speckit.docs build --type troubleshooting` — regenerates troubleshooting documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| spec.md AS-xxx | Error scenarios, edge cases, validation failures |
| code analysis | Error handling patterns, exception types, error messages |
| test files | Failed test scenarios, boundary conditions |
| logs | Common error patterns, stack traces |
| monitoring | Alert patterns, incident history |

## Template Structure

```markdown
# Troubleshooting Guide

> **Target Audience**: All users (end-users, administrators, developers)
> **When to Use**: When encountering errors or unexpected behavior

## Overview

This guide helps you diagnose and resolve common issues with {application-name}.

**Quick Links:**
- [Common Errors](#common-errors) — Frequently encountered issues
- [Diagnostic Tools](#diagnostic-tools) — How to gather information
- [Error Reference](#error-reference) — Complete error code list
- [Getting Help](#getting-help) — When to escalate

---

## Quick Diagnostics

### Is the System Running?

```bash
# Check service status
{status command}

# Expected output
{expected status}
```

**If not running:**
- [Service Won't Start](#service-wont-start)

### Can You Connect?

```bash
# Test connectivity
{connectivity test command}
```

**If cannot connect:**
- [Connection Issues](#connection-issues)

### Are Dependencies Available?

```bash
# Check database
{database check command}

# Check cache
{cache check command}

# Check external APIs
{API check command}
```

**If dependencies unavailable:**
- [Dependency Failures](#dependency-failures)

---

## Common Errors

### Error: {Error Code/Message}

**Error Code**: `{ERROR-CODE}`
**Severity**: {High/Medium/Low}
**Source**: {AS-xxx or code location}

**What This Means:**
{Plain-language explanation of the error}

**Common Causes:**
1. {Cause from AS-xxx edge case}
2. {Cause from code analysis}
3. {Cause from incident history}

**How to Fix:**

#### Solution 1: {Most Common Fix}

{Step-by-step instructions}

```bash
{fix commands}
```

**Verify fix:**
```bash
{verification command}
```

**Why this works:** {Technical explanation}

#### Solution 2: {Alternative Fix}

{Alternative solution if Solution 1 doesn't work}

**Related Errors:**
- [{Related Error Code}](#error-code-2)
- [{Related Issue}](#related-issue)

**Prevention:**
To avoid this error in the future:
- {Preventive measure 1}
- {Preventive measure 2}

---

### Service Won't Start

**Symptoms:**
- Service fails to start
- Process exits immediately
- {Specific symptoms from logs}

**Diagnostic Steps:**

1. **Check logs**
   ```bash
   {log viewing command}
   ```

2. **Look for these patterns:**
   - `{error pattern 1}` → [Port Already in Use](#port-already-in-use)
   - `{error pattern 2}` → [Configuration Error](#configuration-error)
   - `{error pattern 3}` → [Missing Dependency](#missing-dependency)

3. **Verify configuration**
   ```bash
   {config verification command}
   ```

**Common Solutions:**

#### Port Already in Use

**Find process using port:**
```bash
# Find process
{port check command}

# Kill process
{kill command}

# Or change port
{port configuration}
```

#### Configuration Error

**Validate configuration:**
```bash
{config validation command}
```

**Common config issues:**
- Missing required environment variable: {fix}
- Invalid value in config file: {fix}
- Typo in configuration: {fix}

**Fix configuration:**
```bash
{config fix commands}
```

#### Missing Dependency

**Check dependencies:**
```bash
{dependency check command}
```

**Install missing dependencies:**
```bash
{dependency install command}
```

---

### Connection Issues

**Symptoms:**
- Cannot reach application
- Timeout errors
- Connection refused

**Diagnostic Flowchart:**

```
1. Can you ping the server?
   ├─ No → Check network, firewall
   └─ Yes → Continue to step 2

2. Is the port open?
   ├─ No → Service not running or firewall blocking
   └─ Yes → Continue to step 3

3. Does curl/wget work?
   ├─ No → SSL/TLS issue
   └─ Yes → Client configuration issue
```

**Step-by-Step Diagnosis:**

#### Step 1: Check Network Connectivity

```bash
# Ping server
ping {server-address}

# Check DNS resolution
nslookup {domain-name}
```

**If ping fails:**
- Check network connection
- Verify VPN connection (if required)
- Check firewall rules

#### Step 2: Check Port Accessibility

```bash
# Test port connectivity
telnet {server-address} {port}
# or
nc -zv {server-address} {port}
```

**If port not accessible:**
- Service may not be running: [Service Won't Start](#service-wont-start)
- Firewall may be blocking: [Firewall Issues](#firewall-issues)

#### Step 3: Test HTTP/HTTPS

```bash
# Test HTTP connection
curl -v {application-url}

# Test HTTPS with detailed SSL info
curl -vvv https://{application-url}
```

**Common SSL/TLS errors:**
- `SSL certificate problem`: [Certificate Issues](#certificate-issues)
- `SSL handshake failed`: [SSL Handshake Issues](#ssl-handshake-issues)

---

### Authentication Failures

**Error Messages:**
- "Invalid credentials"
- "Authentication failed"
- "Unauthorized"
- "Token expired"

{From AS-xxx authentication scenarios}

**Common Causes:**

#### Wrong Credentials

**Verify credentials:**
- Check username/email spelling
- Verify password (case-sensitive)
- Check for extra spaces

**Reset password:**
```bash
{password reset command}
```

#### Expired Session/Token

**Symptoms:**
- Worked previously, now fails
- "Token expired" message

**Solution:**
```bash
# Clear local storage/cookies
{clear session command}

# Login again
{login command}
```

#### Account Locked

**Check account status:**
```bash
{account check command}
```

**Unlock account:**
```bash
{unlock command}
```

---

### Performance Issues

**Symptoms:**
- Slow response times
- Timeouts
- High resource usage

**Quick Diagnosis:**

```bash
# Check response time
time curl {application-url}

# Check resource usage
{resource monitoring command}
```

**Performance Checklist:**

- [ ] Database queries optimized
- [ ] Cache enabled and working
- [ ] Sufficient system resources
- [ ] No memory leaks
- [ ] Network latency acceptable

**Diagnostic Commands:**

```bash
# Database query performance
{db performance command}

# Cache hit rate
{cache stats command}

# Memory usage
{memory command}

# CPU usage
{cpu command}

# Network latency
{network latency command}
```

**Common Fixes:**

#### Slow Database Queries

```sql
-- Identify slow queries
{slow query command}

-- Add missing indexes
{index creation}
```

#### Cache Not Working

```bash
# Check cache status
{cache status command}

# Clear and rebuild cache
{cache rebuild command}
```

#### Insufficient Resources

```bash
# Check resource limits
{resource limit command}

# Increase limits
{increase limits command}
```

---

### Data Validation Errors

{From AS-xxx validation scenarios}

**Common Validation Errors:**

| Error Message | Cause | Fix |
|--------------|-------|-----|
| {validation error} | {cause from AS-xxx} | {fix} |

**Example: Email Validation Error**

**Error:** "Invalid email format"

**Valid formats:**
- ✅ `user@example.com`
- ✅ `user.name@example.co.uk`
- ❌ `user@example` (missing TLD)
- ❌ `user @example.com` (space in username)

**Solution:** Ensure email matches pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

---

## Diagnostic Tools

### Log Analysis

**Log Locations:**
- Application logs: `{app log path}`
- System logs: `{system log path}`
- Error logs: `{error log path}`

**View logs:**
```bash
# Real-time logs
tail -f {log path}

# Last 100 lines
tail -n 100 {log path}

# Search for errors
grep -i "error" {log path}

# Filter by time
{time-filtered log command}
```

**Log Levels:**
- `ERROR` — Application errors (investigate immediately)
- `WARN` — Potential issues (monitor)
- `INFO` — Normal operations
- `DEBUG` — Detailed diagnostics

### Health Checks

```bash
# Application health
curl {health-check-url}

# Expected response
{health check response format}

# Database health
{db health check}

# Cache health
{cache health check}
```

### Configuration Validation

```bash
# Validate configuration syntax
{config validation command}

# Test configuration
{config test command}

# Display current configuration (redacted)
{config display command}
```

### Network Diagnostics

```bash
# DNS lookup
nslookup {domain}

# Trace route
traceroute {server}

# Port scan
nmap -p {port} {server}

# Packet capture (advanced)
tcpdump -i any port {port}
```

---

## Error Reference

Complete list of error codes and messages.

### Error Codes

| Code | Message | Severity | Cause | Fix Link |
|------|---------|----------|-------|----------|
| {ERROR-001} | {message} | {severity} | {cause} | [Fix](#error-001) |

{Auto-generated from code analysis and AS-xxx}

### HTTP Status Codes

| Code | Meaning | Common Cause | Fix |
|------|---------|--------------|-----|
| 400 | Bad Request | Invalid input | Validate request data |
| 401 | Unauthorized | Missing/invalid auth | Check credentials |
| 403 | Forbidden | Insufficient permissions | Check user roles |
| 404 | Not Found | Resource doesn't exist | Verify resource ID |
| 500 | Server Error | Application error | Check server logs |
| 503 | Service Unavailable | Service down | Check service status |

---

## Advanced Troubleshooting

### Enable Debug Mode

⚠️ **Only in development/staging**

```bash
# Enable debug logging
{debug mode command}

# Restart service
{restart command}

# View debug logs
{debug log command}
```

**Remember to disable in production!**

### Trace Requests

```bash
# Enable request tracing
{tracing command}

# Make request
{request command}

# View trace
{trace view command}
```

### Profiling

{Performance profiling instructions}

### Database Debugging

```sql
-- Explain query plan
EXPLAIN ANALYZE {query};

-- Check locks
{lock check query};

-- View active connections
{connections query};
```

---

## Prevention

### Monitoring Setup

{Link to monitoring documentation}

**Key Metrics to Monitor:**
- Response time
- Error rate
- Resource usage
- Dependency availability

### Automated Alerts

{Link to alerting configuration}

**Recommended Alerts:**
- Error rate > {threshold}
- Response time > {threshold}ms
- CPU usage > {threshold}%
- Disk space < {threshold}%

### Regular Maintenance

**Daily:**
- Check error logs
- Verify backup success
- Monitor resource usage

**Weekly:**
- Review performance metrics
- Check for security updates
- Validate backup restoration

**Monthly:**
- Audit user accounts
- Review and rotate credentials
- Performance testing

---

## Getting Help

### Self-Service Resources

1. **Search this guide** — Use Ctrl+F to search for error messages
2. **Check FAQ** — [Frequently Asked Questions](./faq.md)
3. **Community Forum** — {forum-url}
4. **Documentation** — {docs-url}

### Reporting Issues

**Before reporting:**
- [ ] Searched this troubleshooting guide
- [ ] Checked FAQ
- [ ] Searched existing issues
- [ ] Tried basic diagnostic steps

**Include in report:**
```bash
# System information
{system info command}

# Application version
{version command}

# Recent logs (last 50 lines)
tail -n 50 {log path}

# Configuration (redact secrets!)
{config command}
```

**Where to report:**
- **Bugs**: {bug-report-url}
- **Questions**: {questions-url}
- **Security issues**: {security-email}

### Emergency Contact

**For production emergencies:**
- On-call: {oncall-contact}
- Escalation: {escalation-process}
- Incident management: {incident-process}

---

## Appendix

### Diagnostic Script

Download and run comprehensive diagnostic script:

```bash
# Download diagnostic script
{download command}

# Run diagnostics
{run diagnostic command}

# View report
cat diagnostic-report.txt
```

### Common Log Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| {log pattern 1} | {meaning} | {action} |
| {log pattern 2} | {meaning} | {action} |

### Useful Commands Reference

```bash
# Service management
{service commands}

# Log viewing
{log commands}

# Network diagnostics
{network commands}

# Resource monitoring
{monitoring commands}
```

---

*Last updated: {generation timestamp}*
*Generated from: {spec.md AS-xxx}, {error handling code}, {incident logs}*
```

## Generation Instructions for AI Agents

### Step 1: Extract Error Scenarios from AS-xxx

```python
error_scenarios = []

for scenario in spec.md.acceptance_scenarios:
    if "error" in scenario.then.lower() or "invalid" in scenario.when.lower():
        error_scenarios.append({
            "id": scenario.id,
            "error_message": extract_error_message(scenario.then),
            "cause": scenario.when,
            "expected_behavior": scenario.then,
            "prevention": scenario.given  # Conditions to avoid error
        })
```

### Step 2: Analyze Error Handling Code

```python
# Scan code for error handling patterns
error_handlers = analyze_error_handling(codebase)

for handler in error_handlers:
    troubleshooting_entry = {
        "error_type": handler.exception_type,
        "error_message": handler.error_message,
        "location": handler.file_location,
        "diagnostic_steps": infer_diagnostic_steps(handler),
        "resolution": handler.recovery_logic
    }
```

### Step 3: Extract from Test Failures

```python
# Analyze test files for failure scenarios
test_failures = analyze_test_files("tests/")

for failure in test_failures:
    if failure.is_edge_case:
        troubleshooting_entry = {
            "symptom": failure.test_description,
            "cause": failure.failure_reason,
            "fix": failure.resolution_notes
        }
```

### Step 4: Generate Error Reference Table

```python
error_codes = extract_error_codes(codebase)

error_reference = []
for code in error_codes:
    error_reference.append({
        "code": code.error_code,
        "message": code.error_message,
        "severity": infer_severity(code),
        "cause": find_cause_in_as_xxx(code) or infer_from_code(code),
        "fix_link": generate_fix_anchor(code)
    })
```

### Step 5: Generate Diagnostic Flowcharts

```python
# Create decision tree from common errors
common_errors = get_most_frequent_errors(incident_log)

flowchart = generate_diagnostic_flowchart(common_errors)
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:troubleshooting:authentication -->
{Auto-generated authentication troubleshooting}
<!-- /speckit:auto:troubleshooting:authentication -->

<!-- MANUAL SECTION - Team-specific troubleshooting -->
Known issue with LDAP integration: ...
<!-- /MANUAL SECTION -->
```

## Quality Checks

- [ ] All AS-xxx error scenarios documented
- [ ] Top 10 error patterns from logs included
- [ ] Diagnostic steps testable
- [ ] Solutions verified
- [ ] Error reference table complete
- [ ] Cross-references to related docs
- [ ] Emergency contact info current

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
