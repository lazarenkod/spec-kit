# OpenAPI Generation Guide

This document provides context for AI agents performing API contract generation from FR-xxx requirements via the `/speckit.plan` command.

## Overview

The OpenAPI generation step (4.5) parses functional requirements from `spec.md` and generates `contracts/api.yaml` in OpenAPI 3.0.3 format.

## FR-to-Endpoint Detection

### API Keywords

Scan FR-xxx requirements for these keywords to identify API-related requirements:

| Keyword Category | Keywords |
|-----------------|----------|
| HTTP Methods | `POST`, `GET`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` |
| API Terms | `API`, `endpoint`, `route`, `REST`, `GraphQL`, `webhook` |
| Request/Response | `request`, `response`, `payload`, `body`, `query`, `params` |
| Actions | `fetch`, `submit`, `send`, `receive`, `call` |

### Detection Example

```markdown
FR-001: User can create a new account with email and password
        ^^^^   ^^^^^^
        (action) (resource)

→ Detected: API requirement
→ Method: POST (create action)
→ Resource: accounts
→ Path: /api/v1/accounts
```

## FR-to-Endpoint Mapping Rules

### Action Verb Mapping

| FR Action Pattern | HTTP Method | Path Pattern | Notes |
|-------------------|-------------|--------------|-------|
| create/add/register {X} | POST | /api/v1/{x}s | Pluralized resource |
| get/fetch/retrieve {X} | GET | /api/v1/{x}s/{id} | Singular with ID |
| list/show all {X} | GET | /api/v1/{x}s | Collection endpoint |
| update/modify/edit {X} | PUT | /api/v1/{x}s/{id} | Full replacement |
| patch/change {field} of {X} | PATCH | /api/v1/{x}s/{id} | Partial update |
| delete/remove {X} | DELETE | /api/v1/{x}s/{id} | Resource deletion |
| search/find {X} by {criteria} | GET | /api/v1/{x}s?{criteria}= | Query params |
| upload/attach {X} to {Y} | POST | /api/v1/{y}s/{id}/{x}s | Nested resource |
| authenticate/login | POST | /api/v1/auth/login | Auth endpoint |
| logout/sign out | POST | /api/v1/auth/logout | Auth endpoint |

### Resource Naming

| FR Reference | API Resource | Example Path |
|--------------|--------------|--------------|
| user/account | users | /api/v1/users |
| order/purchase | orders | /api/v1/orders |
| product/item | products | /api/v1/products |
| comment/review | comments | /api/v1/comments |
| file/document | files | /api/v1/files |

**Pluralization Rules**:
- Standard: add 's' (user → users)
- -y ending: change to 'ies' (category → categories)
- -s/-x/-ch/-sh: add 'es' (status → statuses)

## Schema Inference

### From FR Descriptions

| FR Pattern | Inferred Schema |
|------------|-----------------|
| "user with email and password" | `{ email: string, password: string }` |
| "returns user profile with name and avatar" | `{ id, name: string, avatar: string }` |
| "paginated list of orders" | `{ items: Order[], page: number, totalPages: number }` |
| "upload image file (max 5MB)" | `multipart/form-data, maxSize: 5242880` |
| "optional description field" | `description: { type: string, nullable: true }` |

### Data Type Inference

| FR Hint | OpenAPI Type | Format |
|---------|--------------|--------|
| email | string | email |
| password | string | password |
| date/when/time | string | date-time |
| URL/link | string | uri |
| ID/identifier | string | uuid (or integer) |
| amount/price | number | decimal |
| count/quantity | integer | int32 |
| yes/no/enabled | boolean | - |
| file/image/document | string | binary |

### Required vs Optional

| FR Signal | Field Requirement |
|-----------|-------------------|
| "must provide", "required" | required: true |
| "can optionally", "may include" | required: false |
| "if provided", "when specified" | required: false |
| No qualifier | required: true (default) |

## OpenAPI Output Structure

### Base Template

```yaml
openapi: 3.0.3
info:
  title: "{PROJECT_NAME} API"
  version: "1.0.0"
  description: "Auto-generated from spec.md FR-xxx requirements"
  contact:
    name: "API Support"
servers:
  - url: /api/v1
    description: "API v1"
tags:
  - name: "{domain}"
    description: "Operations for {domain}"
paths:
  # Generated from FR-xxx
components:
  schemas:
    # Inferred from FR descriptions
  securitySchemes:
    # From spec.md Security Considerations
```

### Path Entry Template

```yaml
/api/v1/{resource}:
  {method}:
    operationId: "{action}{Resource}"
    summary: "{FR-xxx description}"
    description: "Source: FR-xxx"
    tags:
      - "{domain}"
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/{Resource}Input'
    responses:
      '200':
        description: "Success"
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{Resource}'
      '400':
        $ref: '#/components/responses/BadRequest'
      '401':
        $ref: '#/components/responses/Unauthorized'
      '404':
        $ref: '#/components/responses/NotFound'
      '500':
        $ref: '#/components/responses/InternalError'
```

### Standard Response Components

```yaml
components:
  responses:
    BadRequest:
      description: "Invalid request parameters"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: "Authentication required"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: "Resource not found"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    InternalError:
      description: "Internal server error"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: "Error code"
        message:
          type: string
          description: "Human-readable error message"
        details:
          type: object
          description: "Additional error context"
```

## Authentication Inference

From `spec.md` Security Considerations section:

| Spec Pattern | Security Scheme |
|--------------|-----------------|
| "JWT authentication" | bearerAuth (JWT) |
| "API key" | apiKeyAuth (header) |
| "OAuth 2.0" | oauth2 (authorization code) |
| "session-based" | cookieAuth |
| "basic auth" | basicAuth |

### Security Scheme Templates

```yaml
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
  apiKeyAuth:
    type: apiKey
    in: header
    name: X-API-Key
  oauth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: /oauth/authorize
        tokenUrl: /oauth/token
        scopes:
          read: "Read access"
          write: "Write access"
```

## Validation Rules

Before writing `contracts/api.yaml`:

| Rule | Check | Severity |
|------|-------|----------|
| All API FRs covered | Each FR-xxx with API keywords has path | ERROR |
| Unique operationIds | No duplicate operationId values | ERROR |
| Valid HTTP methods | Only GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS | ERROR |
| Schema references exist | All $ref targets defined | ERROR |
| Response codes documented | At least 200 and one 4xx | WARNING |
| Auth requirements explicit | Security defined if auth mentioned in spec | WARNING |

## Integration with Dependency Registry

Link external APIs from `plan.md` Dependency Registry:

```yaml
# If API-001 is Stripe in Dependency Registry:
paths:
  /api/v1/payments:
    post:
      operationId: createPayment
      description: |
        Creates payment via Stripe API.
        External dependency: [API-001]
      x-external-api: "API-001"  # Cross-reference
```

## Generation Report Format

After successful generation:

```text
CONTRACTS_GENERATED_REPORT:
  Output: contracts/api.yaml
  OpenAPI Version: 3.0.3

  Source FRs:
    - FR-001: createUser (POST /api/v1/users)
    - FR-003: getUser (GET /api/v1/users/{id})
    - FR-007: listOrders (GET /api/v1/orders)

  Generated:
    - Paths: {count}
    - Schemas: {count}
    - Security Schemes: {count}

  Validation:
    - All API FRs covered: PASS
    - Unique operationIds: PASS
    - Schema integrity: PASS

  External References:
    - [API-001]: Stripe endpoints documented
    - [API-002]: SendGrid webhooks documented
```

## Skip Conditions

Do not generate OpenAPI if:

1. `--no-contracts` flag is set
2. No FR-xxx contains API keywords
3. `openapi_generation.enabled: false` in command YAML
4. Spec is purely CLI/desktop application (no HTTP API)

In these cases, set API Contracts section status to `N/A`:

```markdown
### API Contracts

| Contract | Path | Source FRs | Status |
|----------|------|------------|--------|
| Main API | - | - | N/A (no API endpoints in spec) |
```
