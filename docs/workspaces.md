# Multi-Repository Workspaces

Spec Kit supports multi-repository workspaces for organizations where projects span multiple Git repositories. This guide covers workspace setup, management, and CI/CD integration.

## Overview

Modern applications often span multiple repositories:
- Multiple backend services (microservices)
- Frontend applications (web, mobile)
- Shared libraries
- Infrastructure configurations

Spec Kit workspaces provide a lightweight coordination layer that enables:
- **Cross-repository feature specifications** with traceability
- **Unified feature manifests** across repos
- **Dependency tracking** between features in different repos

## Quick Start

```bash
# Create a workspace in your projects directory
cd ~/projects
specify workspace create --name my-platform

# Add repositories to the workspace
specify workspace add ./backend-api --alias api --role backend
specify workspace add ./web-frontend --alias web --role frontend
specify workspace add ./mobile-app --alias mobile --role mobile

# List workspace repositories
specify workspace list

# Synchronize workspace (generate manifest, validate links)
specify workspace sync
```

## Workspace Structure

After creating a workspace, the following structure is created:

```
my-workspace/                    # Workspace root
├── .speckit-workspace           # YAML configuration file
├── .speckit/
│   ├── links/repos/             # Symlinks to repositories
│   │   ├── api -> ../../../backend-api
│   │   └── web -> ../../../web-frontend
│   └── cache/
│       └── unified-manifest.json  # Auto-generated manifest
├── backend-api/                 # Git repository 1
│   ├── .git/
│   └── specs/features/
└── web-frontend/                # Git repository 2
    ├── .git/
    └── specs/features/
```

## Configuration File

The `.speckit-workspace` file uses YAML format:

```yaml
version: "1.0"
name: "my-platform"
link_strategy: auto  # auto | symlink | junction | path_ref

repositories:
  api:
    path: "./backend-api"
    role: backend
    domain: e-commerce
  web:
    path: "./web-frontend"
    role: frontend
    domain: e-commerce
  mobile:
    path: "./mobile-app"
    role: mobile

cross_dependencies:
  - source: "web:005-checkout"
    target: "api:002-payment-api"
    type: REQUIRES
```

## Repository Roles

When adding repositories, you can specify their role:

| Role | Description |
|------|-------------|
| `backend` | Backend services, APIs |
| `frontend` | Web frontend applications |
| `mobile` | Mobile applications |
| `shared` | Shared libraries, common code |
| `infrastructure` | IaC, deployment configs |
| `docs` | Documentation |
| `other` | Other repository types |

Roles help with automatic dependency suggestions (e.g., frontend typically REQUIRES backend APIs).

## Cross-Repository Dependencies

Features can reference dependencies across repositories using the `repo-alias:feature-id` format:

```markdown
## Cross-Repository Dependencies

### Dependencies on Other Repositories

| This Feature | Depends On | Dependency Type | Reason |
|--------------|------------|-----------------|--------|
| web:005-checkout | api:002-payment-api | REQUIRES | Needs payment processing |
| web:005-checkout | api:003-inventory | USES | Checks stock availability |

### Features Depending on This

| External Feature | Dependency Type | Notes |
|------------------|-----------------|-------|
| mobile:008-checkout | REQUIRES | Shares same API contract |
```

### Dependency Types

| Type | Description |
|------|-------------|
| `REQUIRES` | Hard dependency - target must be implemented first |
| `BLOCKS` | This feature blocks the target from completion |
| `EXTENDS` | Extends functionality of the target feature |
| `IMPLEMENTS` | Implements a contract/interface defined by target |
| `USES` | Soft dependency - uses target but doesn't strictly require it |

## Link Strategies

Workspaces support multiple linking strategies for different environments:

| Strategy | Platform | Description |
|----------|----------|-------------|
| `symlink` | Unix/macOS | Standard symbolic links (default) |
| `junction` | Windows | Directory junctions (no admin required) |
| `path_ref` | Any | Path reference files (`.path` files) |
| `auto` | Any | Auto-detect best strategy for platform |

For CI/CD environments, use `path_ref` which doesn't require filesystem symlink support.

---

## CI/CD Integration

### Environment Variables

Configure workspace behavior through environment variables:

```bash
# Set workspace root (useful when not running from workspace directory)
export SPECKIT_WORKSPACE="/path/to/workspace"

# Force link strategy (useful in containers)
export SPECKIT_LINK_STRATEGY="path_ref"
```

### GitHub Actions Example

```yaml
# .github/workflows/spec-validation.yml
name: Validate Specifications

on:
  pull_request:
    paths:
      - 'specs/**'
      - '.speckit-workspace'

env:
  SPECKIT_WORKSPACE: ${{ github.workspace }}
  SPECKIT_LINK_STRATEGY: path_ref

jobs:
  validate-specs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main repository
        uses: actions/checkout@v4
        with:
          path: backend-api

      - name: Checkout frontend repository
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository_owner }}/web-frontend
          path: web-frontend

      - name: Checkout mobile repository
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository_owner }}/mobile-app
          path: mobile-app

      - name: Install Specify CLI
        run: pipx install specify-cli

      - name: Create CI workspace
        run: |
          specify workspace create --name ci-workspace --link-strategy path_ref
          specify workspace add ./backend-api --alias api --role backend
          specify workspace add ./web-frontend --alias web --role frontend
          specify workspace add ./mobile-app --alias mobile --role mobile

      - name: Sync and validate workspace
        run: |
          specify workspace sync
          cat .speckit/cache/unified-manifest.json

      - name: Run spec analysis (when available)
        run: |
          # Future: specify analyze --workspace
          echo "Workspace validated successfully"
```

### Multi-Repository PR Validation

For validating changes across dependent repositories:

```yaml
# .github/workflows/cross-repo-validation.yml
name: Cross-Repository Validation

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  check-dependencies:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout all repos
        run: |
          gh repo clone ${{ github.repository_owner }}/backend-api
          gh repo clone ${{ github.repository_owner }}/web-frontend
          gh repo clone ${{ github.repository_owner }}/mobile-app
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup workspace
        run: |
          pipx install specify-cli
          specify workspace create --name validation-workspace
          specify workspace add ./backend-api --alias api
          specify workspace add ./web-frontend --alias web
          specify workspace add ./mobile-app --alias mobile
          specify workspace sync

      - name: Check cross-repo dependencies
        run: |
          # Parse unified manifest and check for broken dependencies
          jq '.cross_dependencies' .speckit/cache/unified-manifest.json
```

### GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - setup
  - validate

variables:
  SPECKIT_LINK_STRATEGY: path_ref

setup-workspace:
  stage: setup
  script:
    - pip install specify-cli
    - git clone https://${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD}@gitlab.com/org/backend-api.git
    - git clone https://${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD}@gitlab.com/org/web-frontend.git
    - specify workspace create --name gitlab-workspace
    - specify workspace add ./backend-api --alias api --role backend
    - specify workspace add ./web-frontend --alias web --role frontend
    - specify workspace sync
  artifacts:
    paths:
      - .speckit-workspace
      - .speckit/

validate-specs:
  stage: validate
  needs: [setup-workspace]
  script:
    - pip install specify-cli
    - specify workspace list --verbose
    - cat .speckit/cache/unified-manifest.json
```

---

## Docker Compose Example

For local development with multiple repositories:

```yaml
# docker-compose.workspace.yml
version: '3.8'

services:
  spec-workspace:
    image: python:3.11-slim
    working_dir: /workspace
    volumes:
      # Mount all repositories
      - ./backend-api:/workspace/backend-api:ro
      - ./web-frontend:/workspace/web-frontend:ro
      - ./mobile-app:/workspace/mobile-app:ro
      # Mount workspace config
      - ./.speckit-workspace:/workspace/.speckit-workspace
      - ./.speckit:/workspace/.speckit
    environment:
      - SPECKIT_LINK_STRATEGY=path_ref
    command: |
      bash -c "
        pip install specify-cli &&
        specify workspace sync &&
        specify workspace list --verbose
      "

  # Development service that needs workspace context
  dev-shell:
    image: python:3.11-slim
    working_dir: /workspace/backend-api
    volumes:
      - ./backend-api:/workspace/backend-api
      - ./web-frontend:/workspace/web-frontend:ro
      - ./.speckit-workspace:/workspace/.speckit-workspace:ro
      - ./.speckit:/workspace/.speckit:ro
    environment:
      - SPECKIT_WORKSPACE=/workspace
      - SPECKIT_LINK_STRATEGY=path_ref
    stdin_open: true
    tty: true
```

Usage:

```bash
# Validate workspace in container
docker-compose -f docker-compose.workspace.yml run spec-workspace

# Start development shell with workspace context
docker-compose -f docker-compose.workspace.yml run dev-shell bash
```

---

## Best Practices

### 1. Workspace Location

Keep the workspace root **outside** of any individual repository:

```
~/projects/                  # Workspace root here
├── .speckit-workspace
├── backend-api/             # Git repo (not nested)
├── web-frontend/            # Git repo (not nested)
└── mobile-app/              # Git repo (not nested)
```

### 2. Version Control

The `.speckit-workspace` file can be:
- **Ignored** if each developer creates their own workspace
- **Committed** to a dedicated "workspace" repo for team consistency

The `.speckit/` directory should generally be **ignored** (contains cache and links).

### 3. Cross-Repository Dependencies

- Document dependencies **in the consuming feature's spec**, not the provider
- Use REQUIRES for hard dependencies, USES for soft dependencies
- Run `specify workspace sync` after adding dependencies to update the manifest

### 4. CI/CD Considerations

- Always use `--link-strategy path_ref` in containers
- Set `SPECKIT_WORKSPACE` environment variable for non-interactive contexts
- Cache the workspace setup step when possible

---

## Troubleshooting

### Symlinks Not Working

**Problem**: Symlink creation fails on the platform.

**Solution**: Use path references instead:

```bash
specify workspace create --name my-workspace --link-strategy path_ref
# Or for existing workspace, recreate links:
specify workspace sync --force
```

### Repository Not Found

**Problem**: `specify workspace add` says repository doesn't exist.

**Solution**: Verify the path is correct and the directory contains a `.git` folder:

```bash
ls -la ./my-repo/.git
# Should show git directory
```

### Workspace Not Detected

**Problem**: Commands say "Not inside a workspace".

**Solution**: Ensure you're running from within the workspace directory tree, or set the environment variable:

```bash
export SPECKIT_WORKSPACE=/path/to/workspace
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `specify workspace create` | Create a new workspace in current directory |
| `specify workspace add <path>` | Add a repository to the workspace |
| `specify workspace remove <alias>` | Remove a repository from the workspace |
| `specify workspace list` | List all repositories in the workspace |
| `specify workspace sync` | Synchronize links and generate manifest |

See `specify workspace --help` for full option details.
