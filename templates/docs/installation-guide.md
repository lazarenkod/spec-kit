# Installation Guide Template

This template generates comprehensive installation documentation from system requirements, dependencies, and configuration.

## Usage

This template is used by:
- `/speckit.implement` — generates installation guide from RUNNING.md + constitution
- `/speckit.docs build --type installation` — regenerates installation documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| RUNNING.md | Installation commands, prerequisites, configuration |
| constitution.md | System requirements, constraints, deployment philosophy |
| plan.md | Dependencies, tech stack, environment requirements |
| .env.example | Environment variables, configuration options |
| docker-compose.yml | Container-based installation |

## Template Structure

```markdown
# Installation Guide

> **Estimated Time**: {X minutes for quick start, Y minutes for full setup}
> **Difficulty**: {Beginner/Intermediate/Advanced}

## Overview

{One-paragraph description of what will be installed and system architecture}

This guide covers three installation methods:
1. **Quick Start** — Get up and running in 5 minutes (Docker)
2. **Development Setup** — Full local development environment
3. **Production Deployment** — Secure, scalable production installation

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|------------|
| **Operating System** | {OS from constitution} |
| **RAM** | {memory from plan.md} |
| **CPU** | {CPU from plan.md} |
| **Disk Space** | {storage from plan.md} |
| **Network** | {network requirements} |

### Recommended Requirements (Production)

| Component | Requirement |
|-----------|------------|
| **RAM** | {recommended memory} |
| **CPU** | {recommended CPU} |
| **Disk Space** | {recommended storage} |

### Software Dependencies

{Auto-extracted from plan.md and package files}

| Software | Version | Purpose |
|----------|---------|---------|
| {dependency} | {version} | {purpose} |

## Quick Start (5 Minutes)

The fastest way to get started using Docker Compose.

### Prerequisites

- Docker (≥ {version})
- Docker Compose (≥ {version})

**Check if installed:**
```bash
docker --version
docker-compose --version
```

**Install Docker:**
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

### Step 1: Download

```bash
# Clone repository
git clone {repository-url}
cd {project-name}
```

### Step 2: Configure

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional for quick start)
nano .env
```

**Minimum Required Configuration:**
```bash
{Essential env vars only}
```

### Step 3: Start

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

**Expected Output:**
```
NAME                COMMAND             STATUS
{service-1}        ...                 Up (healthy)
{service-2}        ...                 Up (healthy)
```

### Step 4: Verify

Open your browser to **{application-url}**

You should see: {expected landing page}

**Default Credentials** (development only):
- Username: `{default-user}`
- Password: `{default-password}`

⚠️ **Change these immediately in production!**

### What's Next

- [Complete Development Setup](#development-setup) for contributing
- [Production Deployment](#production-deployment) for live systems
- [Configuration Guide](../admin-guide/configuration.md) for advanced options

---

## Development Setup

Full local development environment for contributing to the project.

### Prerequisites

#### Required Software

{Auto-extracted from package.json, pyproject.toml, go.mod, etc.}

**For {language} projects:**

| Tool | Version | Install Command |
|------|---------|----------------|
| {tool} | {version} | {install command} |

**Verify installation:**
```bash
{verification commands}
```

#### Development Tools (Recommended)

| Tool | Purpose | Install |
|------|---------|---------|
| {tool} | {purpose} | {install command} |

### Step 1: Clone Repository

```bash
# Clone repository
git clone {repository-url}
cd {project-name}

# Checkout development branch (if applicable)
git checkout develop
```

### Step 2: Install Dependencies

{Language/framework-specific instructions}

**For Node.js:**
```bash
npm install
# or
yarn install
# or
pnpm install
```

**For Python:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
# or
uv sync
```

**For Go:**
```bash
go mod download
```

**For Rust:**
```bash
cargo build
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env
```

**Development Configuration:**
```bash
{Dev-specific env vars with explanations}
```

**External Services Setup:**

{For each external service dependency}

#### {Service Name} (e.g., PostgreSQL)

**Option 1: Docker (Recommended)**
```bash
docker-compose up -d {service-name}
```

**Option 2: Native Installation**

{Platform-specific installation}

**Connection String:**
```bash
{service-name}_URL={connection-string}
```

### Step 4: Database Setup

```bash
# Run migrations
{migration command}

# Seed development data (optional)
{seed command}
```

**Verify database:**
```bash
{database verification command}
```

### Step 5: Start Development Server

```bash
# Start application in development mode
{dev server command}
```

**Expected Output:**
```
{Sample dev server output}
```

**Access application:**
- Main app: {dev-url}
- API docs: {api-docs-url} (if applicable)
- Admin panel: {admin-url} (if applicable)

### Step 6: Verify Development Environment

```bash
# Run tests
{test command}

# Run linter
{lint command}

# Check code formatting
{format check command}
```

**All checks should pass:**
- ✅ Tests passing
- ✅ No lint errors
- ✅ Code formatted correctly

### Development Workflow

**File Watching:**
```bash
{watch command if applicable}
```

**Hot Reload:**
{Hot reload information}

**Debugging:**
- [VS Code Launch Configuration](.vscode/launch.json)
- [Debugging Guide](../developer-guide/debugging.md)

### Common Development Issues

#### Issue: Dependencies Won't Install

**macOS/Linux:**
```bash
# Clear cache
{cache clear command}

# Reinstall
{reinstall command}
```

**Windows:**
```bash
{Windows-specific solutions}
```

#### Issue: Port Already in Use

```bash
# Find process using port
{port check command}

# Kill process
{kill process command}

# Or change port in configuration
{port configuration}
```

---

## Production Deployment

Secure, scalable production installation guide.

⚠️ **Production Checklist**

Before deploying to production:
- [ ] Security audit completed
- [ ] Secrets configured (not committed to repo)
- [ ] SSL certificates obtained
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Disaster recovery plan documented
- [ ] Load testing completed

### Deployment Options

1. [Docker Swarm](#docker-swarm)
2. [Kubernetes](#kubernetes)
3. [Traditional Server](#traditional-server)
4. [Cloud Platforms](#cloud-platforms) (AWS, GCP, Azure)

### Docker Swarm

{Docker Swarm deployment instructions}

### Kubernetes

{Kubernetes deployment instructions}

**Prerequisites:**
- Kubernetes cluster (≥ v{version})
- kubectl configured
- {persistent storage class}

```bash
# Create namespace
kubectl create namespace {app-namespace}

# Apply configurations
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n {app-namespace}
```

### Traditional Server

{Traditional server deployment}

### Cloud Platforms

#### AWS Deployment

{AWS-specific deployment instructions}

#### Google Cloud Platform

{GCP-specific deployment instructions}

#### Microsoft Azure

{Azure-specific deployment instructions}

### Post-Deployment Steps

#### 1. Verify Deployment

```bash
# Health check
curl {production-url}/health

# Expected response
{health check response}
```

#### 2. Configure Monitoring

{Link to monitoring setup guide}

#### 3. Setup Backups

{Link to backup configuration}

#### 4. Configure SSL/TLS

```bash
{SSL setup commands}
```

#### 5. Configure Firewall

{Firewall configuration instructions}

#### 6. Initial Admin Setup

```bash
# Create admin user
{admin creation command}

# Verify admin access
{verification command}
```

### Security Hardening

{Security hardening checklist}

- [ ] Change default credentials
- [ ] Configure HTTPS
- [ ] Enable firewall
- [ ] Setup fail2ban
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Restrict SSH access
- [ ] Setup automated updates

**Security Configuration:**
```bash
{Security hardening commands}
```

---

## Updating

### Update Strategy

{From constitution/plan}

- **Minor updates**: {update frequency} with {testing requirements}
- **Major upgrades**: {upgrade process}

### Backup Before Update

⚠️ **Always backup before updating!**

```bash
# Backup database
{backup command}

# Backup configuration
{config backup command}

# Verify backup
{backup verification}
```

### Update Process

#### Docker Deployment

```bash
# Pull new images
docker-compose pull

# Stop services
docker-compose down

# Start with new images
docker-compose up -d

# Verify update
docker-compose ps
```

#### Native Installation

```bash
# Backup current version
{backup command}

# Pull updates
git pull origin main

# Update dependencies
{dependency update command}

# Run migrations
{migration command}

# Restart services
{restart command}
```

### Rollback Procedure

If update fails:

```bash
# Stop services
{stop command}

# Restore backup
{restore command}

# Restart with previous version
{restart command}

# Verify rollback
{verification command}
```

---

## Uninstallation

### Remove Application

```bash
# Stop services
{stop command}

# Remove application files
{removal command}

# Clean up configuration (optional)
{config cleanup command}
```

### Remove Docker Installation

```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Remove volumes (⚠️ data loss)
docker volume rm {volume-names}
```

### Remove Database

⚠️ **Warning**: This will delete all data

```bash
# Backup first!
{backup command}

# Remove database
{database removal command}
```

---

## Troubleshooting Installation

### Installation Fails

#### Symptom: Package installation errors

**Diagnosis:**
```bash
{diagnostic commands}
```

**Resolution:**
{Resolution steps}

#### Symptom: Port conflicts

**Diagnosis:**
```bash
# Check port usage
{port check command}
```

**Resolution:**
```bash
# Change port in configuration
{port configuration}
```

### Service Won't Start

{Troubleshooting steps}

### Connection Errors

{Connection troubleshooting}

---

## Getting Help

### Community Support

- **Documentation**: {docs-url}
- **GitHub Issues**: {issues-url}
- **Discussions**: {discussions-url}
- **Discord/Slack**: {community-chat-url}

### Commercial Support

{Commercial support information if applicable}

### Reporting Installation Issues

When reporting installation problems, include:

```bash
# System information
{system info command}

# Installation logs
{log command}

# Configuration (redact secrets)
{config command}
```

---

## Reference

### Directory Structure

After installation, you'll have:

```
{project-name}/
├── {directory structure}
```

### Environment Variables Reference

{Complete list of environment variables from .env.example}

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| {var} | {description} | {default} | Yes/No |

### Port Reference

| Port | Service | Protocol |
|------|---------|----------|
| {port} | {service} | {protocol} |

---

*Last updated: {generation timestamp}*
*Generated from: {RUNNING.md path}, {constitution.md path}, {plan.md path}*
```

## Generation Instructions for AI Agents

### Step 1: Extract System Requirements

```python
# From constitution.md and plan.md
system_requirements = {
    "os": extract_os_requirements(constitution.md),
    "ram": extract_memory_requirements(plan.md),
    "cpu": extract_cpu_requirements(plan.md),
    "disk": extract_storage_requirements(plan.md),
    "network": extract_network_requirements(plan.md)
}
```

### Step 2: Detect Tech Stack

```python
# Auto-detect from project files
if exists("package.json"):
    tech_stack = "node"
    install_cmd = detect_package_manager()  # npm/yarn/pnpm
elif exists("pyproject.toml"):
    tech_stack = "python"
    install_cmd = "uv sync" if uses_uv() else "pip install"
elif exists("go.mod"):
    tech_stack = "go"
elif exists("Cargo.toml"):
    tech_stack = "rust"
```

### Step 3: Generate Docker Instructions

```python
if exists("docker-compose.yml"):
    generate_docker_compose_instructions()
    include_docker_quickstart()
if exists("Dockerfile"):
    generate_docker_build_instructions()
```

### Step 4: Extract Environment Variables

```python
env_vars = parse_env_example(".env.example")

# Categorize by importance
essential_vars = [v for v in env_vars if v.required]
optional_vars = [v for v in env_vars if not v.required]

# Generate configuration sections
generate_env_config_section(essential_vars, "Quick Start")
generate_env_config_section(all_vars, "Development Setup")
```

### Step 5: Platform-Specific Instructions

```python
for platform in ["macos", "linux", "windows"]:
    generate_platform_instructions(platform, tech_stack)
```

## Quality Checks

- [ ] All prerequisites listed
- [ ] Quick start tested (< 10 minutes)
- [ ] Development setup tested on all platforms
- [ ] Production deployment tested
- [ ] All dependencies have versions specified
- [ ] Environment variables documented
- [ ] Troubleshooting covers common issues
- [ ] Update and rollback procedures tested

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
