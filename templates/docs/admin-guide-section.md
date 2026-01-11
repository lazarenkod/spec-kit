# Admin Guide Section Template

This template generates system administrator documentation from Infrastructure Dependencies, deployment configurations, and operational requirements.

## Usage

This template is used by:
- `/speckit.plan` — generates initial deployment docs from Infrastructure Dependencies
- `/speckit.monitor` — adds monitoring and alerting documentation
- `/speckit.docs build --type admin-guide` — regenerates admin documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| plan.md Infrastructure Dependencies | Database, cache, external services configuration |
| constitution.md | System requirements, constraints, principles |
| contracts/api.yaml | Service endpoints, auth requirements |
| monitoring docs | Alert rules, runbooks, SLOs |
| tasks.md INFRA-xxx | Infrastructure setup tasks |

## Template Structure

```markdown
# {Component Name} Administration

> **Target Audience**: System administrators, DevOps engineers
> **Skill Level**: Intermediate to Advanced
> **Estimated Time**: {X minutes for setup}

## Overview

{One-paragraph description of the component's role in the system architecture}

## Prerequisites

**System Requirements:**
- {OS requirements from constitution}
- {Memory/CPU from plan.md}
- {Network requirements}

**Required Access:**
- {Admin privileges needed}
- {Cloud provider access}
- {Credentials/API keys}

**Dependencies:**
- {List from plan.md INFRA-xxx}

## Installation

### Option 1: Docker Compose (Recommended)

{Auto-generated from docker-compose.yml or staging config}

```yaml
version: '3.8'
services:
  {service-name}:
    image: {image}:{version}
    ports:
      - "{port}:{port}"
    environment:
      - {ENV_VAR}={value}
```

**Steps:**
1. Create `docker-compose.yml` with the configuration above
2. Run `docker-compose up -d`
3. Verify service is running: `docker-compose ps`

### Option 2: Native Installation

{OS-specific instructions}

**For Ubuntu/Debian:**
```bash
{installation commands}
```

**For macOS:**
```bash
{installation commands}
```

**For Windows:**
```powershell
{installation commands}
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| {ENV_VAR} | {Description from plan.md} | {default} | Yes/No |

**Example .env configuration:**
```bash
{Auto-generated from .env.example}
```

### Configuration Files

#### {config-file-name}

**Location**: `{path}`
**Purpose**: {Description}

```yaml
{Sample configuration with comments}
```

**Key Settings:**

| Setting | Description | Recommended Value |
|---------|-------------|-------------------|
| {setting} | {description} | {value} |

## Deployment

### Development Environment

```bash
{Commands for local deployment}
```

### Staging Environment

```bash
{Commands for staging deployment}
```

**Pre-deployment Checklist:**
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Monitoring enabled

### Production Environment

⚠️ **Production Deployment Requires:**
- [ ] Approval from {stakeholder}
- [ ] Backup created
- [ ] Rollback plan documented
- [ ] Monitoring dashboards ready

```bash
{Commands for production deployment}
```

**Post-deployment Verification:**
```bash
# Check service status
{health check command}

# Verify database connectivity
{database check command}

# Test authentication
{auth test command}
```

## Monitoring

### Health Checks

**Endpoint**: `{health-check-url}`
**Expected Response**: `{response format}`

```bash
# Check service health
curl {health-check-url}
```

**Response Codes:**
- `200 OK` — Service healthy
- `503 Service Unavailable` — Service degraded (check logs)

### Key Metrics

Monitor these metrics (from monitoring docs):

| Metric | Alert Threshold | Action |
|--------|----------------|---------|
| {metric-name} | {threshold} | {runbook link} |

### Logs

**Log Location**: `{log-path}`

**Key Log Patterns to Monitor:**
- `ERROR` — Application errors (runbook: {link})
- `WARN` — Potential issues
- `{custom-pattern}` — {description}

**View logs:**
```bash
# Real-time logs
{log command}

# Filter by level
{filtered log command}

# Search for errors
{search command}
```

## Maintenance

### Backup and Restore

#### Database Backup

**Schedule**: {backup frequency from plan}

```bash
# Manual backup
{backup command}

# Verify backup
{verify command}
```

**Backup Location**: `{backup-path}`
**Retention Policy**: {retention from constitution}

#### Restore from Backup

⚠️ **Warning**: This will overwrite current data

```bash
# Stop services
{stop command}

# Restore database
{restore command}

# Restart services
{start command}

# Verify restoration
{verify command}
```

### Scaling

#### Horizontal Scaling

{Instructions for adding instances}

**When to Scale:**
- CPU usage consistently > {threshold}%
- Response time > {threshold}ms
- Request queue length > {threshold}

```bash
# Add instance
{scale-up command}

# Verify new instance
{verify command}
```

#### Vertical Scaling

{Instructions for increasing resources}

```bash
# Update resource limits
{resource update command}

# Apply changes
{apply command}
```

### Updates and Patches

**Update Schedule**: {from constitution}

#### Minor Updates

```bash
# Check current version
{version command}

# Pull new version
{update command}

# Restart with new version
{restart command}

# Verify update
{verify command}
```

#### Major Upgrades

⚠️ **Major upgrades may include breaking changes**

**Before upgrading:**
1. Read release notes: {link}
2. Review migration guide: {link}
3. Create full backup
4. Test in staging environment
5. Schedule maintenance window

```bash
# Upgrade process
{upgrade commands}
```

## Troubleshooting

### Common Issues

#### Issue 1: {Common problem}

**Symptoms:**
- {Symptom description}

**Diagnosis:**
```bash
{Diagnostic commands}
```

**Resolution:**
```bash
{Fix commands}
```

**Root Cause:** {Explanation}

#### Issue 2: Service Won't Start

**Symptoms:**
- Service fails to start
- Health check returns 503

**Diagnosis:**
```bash
# Check service status
{status command}

# View recent logs
{log command}

# Check port availability
{port check command}
```

**Common Causes:**
1. **Port already in use**
   ```bash
   # Find process using port
   {find process command}

   # Kill process
   {kill command}
   ```

2. **Missing configuration**
   ```bash
   # Verify config file exists
   {check config command}

   # Validate configuration
   {validate command}
   ```

3. **Database connectivity**
   ```bash
   # Test database connection
   {db test command}
   ```

### Diagnostic Commands

```bash
# System resource usage
{resource command}

# Service status
{status command}

# Network connectivity
{network test command}

# Configuration validation
{config validate command}
```

### Getting Help

If troubleshooting doesn't resolve the issue:

1. **Collect diagnostic information:**
   ```bash
   {diagnostic script command}
   ```

2. **Check runbooks:** {runbooks directory}

3. **Contact support:**
   - Email: {support email}
   - Slack: {slack channel}
   - Escalation: {escalation process}

**Include in support request:**
- Service version: `{version command}`
- Error logs: Last 100 lines from `{log path}`
- Configuration (redact sensitive data)
- Steps to reproduce

## Security

### Authentication and Authorization

{From plan.md Security Considerations}

**Authentication Method**: {JWT/API Key/OAuth}

**Credentials Storage:**
- Location: `{credentials path}`
- Encryption: {encryption method}
- Rotation schedule: {rotation frequency}

### Firewall Configuration

**Required Ports:**

| Port | Protocol | Purpose | Allowed IPs |
|------|----------|---------|-------------|
| {port} | {protocol} | {purpose} | {IP range} |

**Firewall Rules:**
```bash
{firewall configuration commands}
```

### SSL/TLS Configuration

**Certificate Location**: `{cert path}`
**Renewal**: {auto/manual} every {period}

```bash
# Verify certificate
{cert check command}

# Renew certificate (if manual)
{renew command}
```

### Security Best Practices

- ✅ **Do**: Rotate credentials every {period}
- ✅ **Do**: Enable audit logging
- ✅ **Do**: Use principle of least privilege
- ✅ **Do**: Keep system updated
- ❌ **Don't**: Store credentials in plaintext
- ❌ **Don't**: Use default passwords
- ❌ **Don't**: Expose admin interfaces to public internet

## Performance Tuning

### Resource Optimization

**Recommended Settings** (from load testing):

| Resource | Setting | Value | Impact |
|----------|---------|-------|--------|
| {resource} | {setting} | {value} | {description} |

**Configuration:**
```yaml
{Optimized configuration}
```

### Database Optimization

{From plan.md database configuration}

```sql
-- Recommended indexes
{Index creation SQL}

-- Query optimization
{Optimization suggestions}
```

### Caching Strategy

{From plan.md caching layer}

**Cache Hit Rate Target**: > {threshold}%

```bash
# Check cache statistics
{cache stats command}
```

## Disaster Recovery

### Recovery Time Objective (RTO)

**Target**: {RTO from constitution}

### Recovery Point Objective (RPO)

**Target**: {RPO from constitution}

### Disaster Recovery Plan

1. **Declare incident**: {escalation process}
2. **Assess impact**: {assessment checklist}
3. **Execute recovery**: {recovery runbook}
4. **Verify restoration**: {verification checklist}
5. **Post-mortem**: {post-mortem template}

**Recovery Runbook**: {link to detailed runbook}

## Reference

### Useful Commands

```bash
# Service management
{start/stop/restart commands}

# Status checks
{status check commands}

# Log viewing
{log commands}

# Configuration validation
{validation commands}
```

### Configuration File Locations

| File | Location | Purpose |
|------|----------|---------|
| {file} | {path} | {description} |

### Related Documentation

- [Architecture Overview](../developer-guide/architecture/overview.md)
- [API Reference](../developer-guide/api-reference/index.md)
- [Monitoring Runbooks](../troubleshooting/runbooks/)
- [Security Policies](./security-policies.md)

---

*Last updated: {generation timestamp}*
*Generated from: {plan.md path}, {monitoring docs path}*
```

## Generation Instructions for AI Agents

### Step 1: Extract Infrastructure Dependencies

```python
# From plan.md Infrastructure Dependencies section
for dependency in plan.md.infrastructure_dependencies:
    if dependency.type == "INFRA":
        component = {
            "name": dependency.name,
            "version": dependency.version,
            "purpose": dependency.purpose,
            "configuration": dependency.configuration_requirements,
            "monitoring": dependency.monitoring_requirements
        }
```

### Step 2: Generate Installation Instructions

```python
# Auto-detect installation method from project structure
if exists("docker-compose.yml"):
    generate_docker_installation()
if exists("Dockerfile"):
    generate_docker_single_container()
if exists("k8s/"):
    generate_kubernetes_deployment()

# Platform-specific instructions
for platform in ["ubuntu", "macos", "windows"]:
    generate_native_installation(platform, component)
```

### Step 3: Extract Configuration from .env.example

```python
env_vars = parse_env_example(".env.example")

for var in env_vars:
    table_row = {
        "variable": var.name,
        "description": var.comment or infer_purpose(var.name),
        "default": var.default_value,
        "required": var.is_required()
    }
```

### Step 4: Generate Monitoring Section

```python
# From monitoring docs (if exists)
if exists("docs/monitor.md"):
    metrics = extract_metrics("docs/monitor.md")
    alerts = extract_alert_rules("infra/observability/rules/")

    for metric in metrics:
        monitoring_table_row = {
            "metric": metric.name,
            "threshold": metric.alert_threshold,
            "runbook": f"runbooks/{metric.runbook_id}.md"
        }
```

### Step 5: Generate Troubleshooting from Error Patterns

```python
# Analyze logs and error handling code
error_patterns = analyze_error_handling(codebase)

for pattern in error_patterns:
    if pattern.frequency > threshold:
        troubleshooting_entry = {
            "issue": pattern.error_message,
            "diagnosis": pattern.diagnostic_steps,
            "resolution": pattern.resolution_steps,
            "root_cause": pattern.root_cause_analysis
        }
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:admin-guide:database -->
{Auto-generated database administration content}
<!-- /speckit:auto:admin-guide:database -->

<!-- MANUAL SECTION - Infrastructure-specific notes -->
Our production database uses RDS with automated backups...
<!-- /MANUAL SECTION -->
```

## Quality Checks

- [ ] All INFRA-xxx dependencies documented
- [ ] Installation instructions tested on all platforms
- [ ] All environment variables from .env.example included
- [ ] Monitoring metrics aligned with alert rules
- [ ] Troubleshooting covers top 10 error patterns
- [ ] Security best practices included
- [ ] Disaster recovery RTO/RPO specified
- [ ] Backup/restore procedures tested

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
