# Migration Guide Template

This template generates migration documentation from system spec history, breaking changes, and version changes.

## Usage

This template is used by:
- `/speckit.merge` — generates migration guide from system spec history
- `/speckit.docs version {version}` — creates version-specific migration guide
- `/speckit.docs build --type migration` — regenerates migration documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| system specs | Version history, behavior changes, breaking changes |
| CHANGELOG.md | Version-to-version changes, deprecations |
| contracts/api.yaml | API version changes, endpoint modifications |
| plan.md | Database schema changes, infrastructure updates |
| code analysis | Deprecated functions, renamed modules |

## Template Structure

```markdown
# Migration Guide: v{old-version} to v{new-version}

> **Migration Complexity**: {Low/Medium/High}
> **Estimated Time**: {X minutes to Y hours}
> **Downtime Required**: {Yes/No/Optional}

## Overview

This guide helps you migrate from **{Project Name} v{old-version}** to **v{new-version}**.

**What's New:**
{From CHANGELOG.md}
- {Major feature 1}
- {Major feature 2}
- {Major improvement}

**Breaking Changes:** {Count}
**Deprecations:** {Count}
**Database Changes:** {Yes/No}

---

## Should You Upgrade?

### Reasons to Upgrade

✅ **You should upgrade if:**
- {Reason 1 from release notes}
- {Reason 2}
- {Reason 3}

### Reasons to Wait

⚠️ **Consider waiting if:**
- You're using deprecated features without migration plan
- You need {specific compatibility}
- Current version is working perfectly for your use case

---

## Pre-Migration Checklist

**Before starting, ensure:**
- [ ] Full backup created ([Backup Guide](../admin-guide/backup-restore.md))
- [ ] Migration tested in staging environment
- [ ] Downtime window scheduled (if required)
- [ ] Team notified of planned upgrade
- [ ] Rollback plan documented
- [ ] All dependencies compatible with new version

**Check compatibility:**
```bash
# Check current version
{version check command}

# Check dependency compatibility
{dependency check command}
```

---

## Breaking Changes

{From system spec history and CHANGELOG}

### Breaking Change 1: {Change Description}

**Impact:** {High/Medium/Low}
**Affects:** {What this breaks}

**Old Behavior** (v{old-version}):
```{language}
{Old code example}
```

**New Behavior** (v{new-version}):
```{language}
{New code example}
```

**Why Changed:** {Reason from system spec history}

**Migration Steps:**

1. **Update code:**
   ```{language}
   {Migration code}
   ```

2. **Update configuration:**
   ```yaml
   {Configuration changes}
   ```

3. **Test:**
   ```bash
   {Test commands}
   ```

**Estimated effort:** {Time estimate}

---

### Breaking Change 2: API Endpoint Changes

{From contracts/api.yaml version history}

**Removed Endpoints:**

| Old Endpoint | Replacement | Notes |
|-------------|-------------|-------|
| `{old-endpoint}` | `{new-endpoint}` | {Migration notes} |

**Changed Endpoints:**

| Endpoint | Change | Migration Required |
|----------|--------|-------------------|
| `{endpoint}` | {Change description} | {Yes/No} |

**Migration Example:**

**Before (v{old-version}):**
```bash
curl -X POST {old-api-url} \
  -H "Authorization: Bearer {token}" \
  -d '{old-payload}'
```

**After (v{new-version}):**
```bash
curl -X POST {new-api-url} \
  -H "Authorization: Bearer {token}" \
  -d '{new-payload}'
```

**Client Library Updates:**

```{language}
# Old
{old-client-code}

# New
{new-client-code}
```

---

### Breaking Change 3: Database Schema Changes

{From plan.md and database migration files}

**Schema Modifications:**

| Table | Change | Migration |
|-------|--------|-----------|
| `{table}` | {Change description} | {Migration SQL} |

**Data Migration Required:** {Yes/No}

**Automatic migrations:**
```bash
# Run migrations
{migration command}

# Verify migration
{verification command}
```

**Manual data migration:**
```sql
-- Backup data first
{backup SQL}

-- Transform data
{transformation SQL}

-- Verify
{verification SQL}
```

**Rollback procedure:**
```sql
-- Revert schema
{rollback SQL}

-- Restore data
{restore SQL}
```

---

## Deprecations

{From code analysis and CHANGELOG}

### Deprecated Feature: {Feature Name}

**Deprecated in:** v{deprecation-version}
**Removal planned:** v{removal-version}
**Reason:** {Deprecation reason}

**Old Way:**
```{language}
{Deprecated code}
```

**New Way:**
```{language}
{Replacement code}
```

**Migration Guide:**
{Step-by-step migration instructions}

**Timeline:**
- v{current}: Feature deprecated but functional (warnings logged)
- v{next}: Feature still available with deprecation notices
- v{removal}: Feature removed

---

## Configuration Changes

{From .env.example and config file changes}

### Environment Variables

**Removed:**
| Variable | Replacement | Migration |
|----------|-------------|-----------|
| `{OLD_VAR}` | `{NEW_VAR}` | {Migration notes} |

**Added:**
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{NEW_VAR}` | {Description} | Yes/No | {Default} |

**Modified:**
| Variable | Old Format | New Format | Migration |
|----------|-----------|------------|-----------|
| `{VAR}` | {Old format} | {New format} | {How to migrate} |

**Update .env:**
```bash
# Remove deprecated
# OLD_VAR=value  # Remove this

# Add new required variables
NEW_VAR=value
ANOTHER_VAR=value

# Update modified variables
# Was: CONFIG_OPTION=old_format
# Now: CONFIG_OPTION=new_format
```

---

### Configuration Files

**config.yaml changes:**

```yaml
# Old configuration (v{old-version})
old_section:
  old_option: value

# New configuration (v{new-version})
new_section:
  new_option: value
  additional_option: value
```

---

## Migration Steps

### Step 1: Backup

⚠️ **Critical: Always backup before upgrading**

```bash
# Backup database
{database backup command}

# Backup configuration
{config backup command}

# Backup application files
{file backup command}

# Verify backup
{verification command}
```

**Store backups in:** `{backup-location}`

---

### Step 2: Update Dependencies

{Language/framework-specific dependency updates}

**For {Language} projects:**

```bash
# Update package manager
{package manager update}

# Update dependencies
{dependency update command}

# Verify compatibility
{compatibility check}
```

**Dependency version requirements:**
| Dependency | Minimum Version | Recommended |
|------------|----------------|-------------|
| {Dependency 1} | {Min version} | {Rec version} |
| {Dependency 2} | {Min version} | {Rec version} |

---

### Step 3: Database Migration

{If database changes exist}

**Development/Staging:**
```bash
# Backup database
{backup command}

# Run migrations
{migration command}

# Verify schema
{schema verification}

# Test application
{test command}
```

**Production:**
```bash
# Enable maintenance mode
{maintenance mode command}

# Backup database
{backup command}

# Run migrations
{migration command}

# Verify migration
{verification command}

# Disable maintenance mode
{disable maintenance command}
```

**Expected duration:** {Time estimate}

**If migration fails:**
```bash
# Rollback migration
{rollback command}

# Restore backup
{restore command}

# Investigate logs
{log command}
```

---

### Step 4: Update Application Code

**Code changes required:**

1. **Update imports/dependencies:**
   ```{language}
   {Import updates}
   ```

2. **Replace deprecated APIs:**
   ```{language}
   {API replacement code}
   ```

3. **Update configuration:**
   ```{language}
   {Config updates}
   ```

4. **Handle breaking changes:**
   ```{language}
   {Breaking change fixes}
   ```

---

### Step 5: Update Configuration

```bash
# Update .env file
{env update steps}

# Update config files
{config update steps}

# Validate configuration
{validation command}
```

---

### Step 6: Update Application

**Docker deployment:**
```bash
# Pull new image
docker pull {image}:v{new-version}

# Stop old container
docker-compose down

# Start new container
docker-compose up -d

# Check status
docker-compose ps
```

**Native deployment:**
```bash
# Stop application
{stop command}

# Update application files
{update command}

# Start application
{start command}

# Verify status
{status command}
```

---

### Step 7: Verify Migration

**Post-migration checklist:**
- [ ] Application starts successfully
- [ ] Health checks passing
- [ ] Database migrations applied
- [ ] API endpoints responding
- [ ] Authentication working
- [ ] Key features functional
- [ ] No error logs
- [ ] Performance acceptable

**Verification commands:**
```bash
# Health check
curl {health-url}

# API test
curl {api-test-url}

# Database verification
{db verification}

# Log check
{log command}
```

---

### Step 8: Monitor

**Monitor for these issues after migration:**
- Error rate increases
- Performance degradation
- Unexpected behavior
- User complaints

**Monitoring commands:**
```bash
# Check error logs
{error log command}

# Monitor performance
{performance command}

# Check resource usage
{resource command}
```

**Monitoring dashboards:** {dashboard-links}

---

## Rollback Procedure

If migration fails, rollback to v{old-version}:

### Rollback Steps

1. **Stop application:**
   ```bash
   {stop command}
   ```

2. **Restore database backup:**
   ```bash
   {restore database command}
   ```

3. **Restore configuration:**
   ```bash
   {restore config command}
   ```

4. **Deploy previous version:**
   ```bash
   # Docker
   docker-compose down
   docker pull {image}:v{old-version}
   docker-compose up -d

   # Native
   {rollback deployment command}
   ```

5. **Verify rollback:**
   ```bash
   {verification commands}
   ```

**Rollback time estimate:** {Time estimate}

---

## Migration Strategies

### Strategy 1: Blue-Green Deployment (Zero Downtime)

**Best for:** Production systems requiring high availability

**Steps:**
1. Deploy v{new-version} to green environment
2. Run database migrations (compatible with both versions)
3. Test green environment thoroughly
4. Switch traffic to green
5. Monitor for issues
6. Decommission blue after stability confirmed

**Pros:**
- Zero downtime
- Easy rollback
- Full testing before switchover

**Cons:**
- Requires extra infrastructure
- Database migrations must be compatible with both versions

---

### Strategy 2: Rolling Update (Minimal Downtime)

**Best for:** Distributed systems with multiple instances

**Steps:**
1. Update instances one at a time
2. Verify each instance before proceeding
3. Continue until all updated

**Downtime:** {Minimal/None per instance}

---

### Strategy 3: Maintenance Window (Planned Downtime)

**Best for:** Small deployments, significant breaking changes

**Steps:**
1. Schedule maintenance window
2. Notify users
3. Enable maintenance mode
4. Perform full migration
5. Verify and test
6. Resume operations

**Downtime:** {Time estimate}

---

## Platform-Specific Notes

### AWS

{AWS-specific migration notes}

### Google Cloud Platform

{GCP-specific migration notes}

### Docker/Kubernetes

{Container-specific migration notes}

---

## Troubleshooting Migration

### Issue: Migration fails with "{Error}"

**Cause:** {Error cause}

**Solution:**
```bash
{Solution commands}
```

---

### Issue: Application won't start after migration

**Diagnosis:**
```bash
{Diagnostic commands}
```

**Common causes:**
- Configuration error: [Fix](#configuration-changes)
- Dependency version mismatch: [Fix](#step-2-update-dependencies)
- Database migration incomplete: [Fix](#step-3-database-migration)

---

### Issue: Performance degradation after migration

**Check:**
```bash
# Database query performance
{db performance command}

# Resource usage
{resource command}

# Cache status
{cache command}
```

**Optimization:** [Performance Tuning Guide](../admin-guide/performance-tuning.md)

---

## Post-Migration

### Optimize New Features

**New features to configure:**
{From CHANGELOG new features}

1. **{New Feature 1}:**
   {Configuration instructions}

2. **{New Feature 2}:**
   {Configuration instructions}

---

### Clean Up Deprecated Code

After successful migration:

```bash
# Remove deprecated configuration
{cleanup commands}

# Remove old backups (after retention period)
{backup cleanup}
```

---

### Update Documentation

- [ ] Update internal documentation
- [ ] Update team wiki
- [ ] Update API documentation
- [ ] Notify integrations/partners
- [ ] Update monitoring/alerting

---

## Getting Help

### Migration Support

**Having issues?**
- 📖 Read this guide thoroughly
- 🔍 Search [known issues]({issues-url}?q=label%3Amigration)
- 💬 Ask in [discussions]({discussions-url})
- 📧 Contact support: {support-email}

**Include in support request:**
- Migration step where failure occurred
- Error messages from logs
- Current version and target version
- Migration commands executed
- System configuration

---

## Version History

### Previous Migrations

- [v{older} to v{old}](./migration-v{older}-to-v{old}.md)
- [v{even-older} to v{older}](./migration-v{even-older}-to-v{older}.md)

### Future Versions

**Upcoming:** v{next-version} (planned for {date})
- {Planned feature 1}
- {Planned feature 2}

**Long-term:** [Roadmap]({roadmap-url})

---

*Last updated: {generation timestamp}*
*Generated from: {system specs history}, {CHANGELOG.md}, {contracts/api.yaml}*
```

## Generation Instructions for AI Agents

### Step 1: Extract Breaking Changes from System Specs

```python
breaking_changes = []

for system_spec in system_specs:
    history = system_spec.spec_history

    for version_entry in history:
        if version_entry.breaking_changes:
            for change in version_entry.breaking_changes:
                breaking_changes.append({
                    "component": system_spec.component,
                    "change": change.description,
                    "old_behavior": change.before,
                    "new_behavior": change.after,
                    "reason": change.reason,
                    "version": version_entry.version
                })
```

### Step 2: Extract API Changes from OpenAPI

```python
if exists("contracts/api.yaml"):
    api_changes = compare_openapi_versions(old_version, new_version)

    for change in api_changes:
        if change.type == "breaking":
            migration_steps.append({
                "type": "api",
                "endpoint": change.endpoint,
                "old": change.old_definition,
                "new": change.new_definition,
                "migration": generate_api_migration_example(change)
            })
```

### Step 3: Extract Database Migrations

```python
# From migration files or plan.md
db_migrations = analyze_database_migrations(old_version, new_version)

for migration in db_migrations:
    if migration.requires_manual_intervention:
        migration_guide.add_manual_step(migration)
    else:
        migration_guide.add_automatic_migration(migration)
```

### Step 4: Extract Configuration Changes

```python
old_env = parse_env_example(f".env.example.{old_version}")
new_env = parse_env_example(f".env.example.{new_version}")

config_changes = {
    "removed": old_env - new_env,
    "added": new_env - old_env,
    "modified": find_modified_vars(old_env, new_env)
}
```

### Step 5: Generate Migration Complexity Score

```python
complexity = calculate_migration_complexity({
    "breaking_changes": len(breaking_changes),
    "database_changes": len(db_migrations),
    "config_changes": len(config_changes),
    "api_changes": len(api_changes),
    "code_changes_required": estimate_code_changes()
})

# Low: < 5 changes, no manual steps
# Medium: 5-15 changes, some manual steps
# High: > 15 changes or complex manual steps
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:migration:breaking-changes -->
{Auto-generated breaking changes from system spec history}
<!-- /speckit:auto:migration:breaking-changes -->

<!-- MANUAL SECTION - Platform-specific notes -->
For our internal deployment, also run...
<!-- /MANUAL SECTION -->
```

## Quality Checks

- [ ] All breaking changes from system specs included
- [ ] Database migrations documented
- [ ] API endpoint changes documented
- [ ] Configuration changes listed
- [ ] Rollback procedure tested
- [ ] Migration tested in staging
- [ ] Time estimates realistic
- [ ] Troubleshooting section complete

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
