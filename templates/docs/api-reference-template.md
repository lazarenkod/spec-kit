# API Reference Template

This template generates API reference documentation from OpenAPI specs, code analysis, and functional requirements.

## Usage

This template is used by:
- `/speckit.plan` — generates initial API docs from contracts/api.yaml
- `/speckit.implement` — enriches with implementation details and examples
- `/speckit.docs build --type api-reference` — regenerates API documentation

## Input Sources

| Source | Information Extracted |
|--------|---------------------|
| contracts/api.yaml | OpenAPI specification, endpoints, schemas |
| spec.md FR-xxx | API requirements, business rules |
| code analysis | Actual implementation, validation rules, error handling |
| system specs | Current behavior, authentication, rate limiting |
| integration tests | Request/response examples |

## Template Structure

```markdown
# API Reference

> **API Version**: {api-version}
> **Base URL**: `{base-url}`
> **Last Updated**: {generation timestamp}

## Overview

{One-paragraph API description from spec.md}

**Key Features:**
- {Feature from FR-xxx}
- {Feature from FR-xxx}
- {Feature from FR-xxx}

**API Type:** {REST/GraphQL/gRPC}
**Data Format:** {JSON/XML/Protobuf}

---

## Quick Start

### Authentication

**Method:** {auth-method from OpenAPI securitySchemes}

```bash
# Example authentication
curl {api-url}/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'

# Response
{
  "token": "{jwt-token}",
  "expiresIn": 3600
}

# Use token in requests
curl {api-url}/resource \
  -H "Authorization: Bearer {jwt-token}"
```

**Authentication Guide:** [Authentication Details](#authentication)

---

### Your First Request

```bash
# Make your first API call
curl {api-url}/example \
  -H "Authorization: Bearer {token}"

# Response
{
  "message": "Hello from {Project Name} API!",
  "version": "{api-version}"
}
```

---

### API Explorer

**Try the API interactively:**
- [Swagger UI]({swagger-ui-url}) — Interactive API documentation
- [Postman Collection]({postman-url}) — Import and test API
- [API Playground]({playground-url}) — Test API in browser

---

## Table of Contents

- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Pagination](#pagination)
- [Filtering & Sorting](#filtering--sorting)
- [Webhooks](#webhooks) (if applicable)
- [Endpoints](#endpoints)
  - [{Resource 1}](#{resource-1-endpoints})
  - [{Resource 2}](#{resource-2-endpoints})
- [Data Schemas](#data-schemas)
- [Examples](#examples)
- [SDKs](#sdks)
- [Changelog](#changelog)

---

## Authentication

{From OpenAPI securitySchemes}

### {Auth Method Name}

**Type:** {bearer/apiKey/oauth2/basic}
**Location:** {header/query/cookie}

**How to Authenticate:**

1. **Obtain credentials:**
   {Credential obtainment process}

2. **Include in requests:**
   ```http
   {auth-header}: {auth-format}
   ```

**Example:**
```bash
curl {api-url}/endpoint \
  -H "{auth-header}: {auth-example}"
```

---

### API Keys

{If API key auth is used}

**Generate API Key:**
```bash
curl {api-url}/auth/api-keys \
  -X POST \
  -H "Authorization: Bearer {jwt-token}" \
  -d '{
    "name": "My Application",
    "permissions": ["read", "write"]
  }'
```

**Use API Key:**
```bash
curl {api-url}/endpoint \
  -H "X-API-Key: {api-key}"
```

**Security Best Practices:**
- Store API keys securely (environment variables, secret managers)
- Rotate keys periodically
- Use different keys for development and production
- Revoke keys when no longer needed

---

### OAuth 2.0

{If OAuth is used}

**Grant Type:** {authorization-code/client-credentials/etc}

**Authorization Flow:**

1. **Redirect user to authorization URL:**
   ```
   {oauth-authorize-url}?
     client_id={client-id}&
     redirect_uri={redirect-uri}&
     response_type=code&
     scope={scopes}
   ```

2. **Receive authorization code at redirect URI**

3. **Exchange code for access token:**
   ```bash
   curl {oauth-token-url} \
     -X POST \
     -d "grant_type=authorization_code" \
     -d "code={authorization-code}" \
     -d "client_id={client-id}" \
     -d "client_secret={client-secret}" \
     -d "redirect_uri={redirect-uri}"
   ```

4. **Use access token:**
   ```bash
   curl {api-url}/endpoint \
     -H "Authorization: Bearer {access-token}"
   ```

**Token Refresh:**
```bash
curl {oauth-token-url} \
  -X POST \
  -d "grant_type=refresh_token" \
  -d "refresh_token={refresh-token}" \
  -d "client_id={client-id}" \
  -d "client_secret={client-secret}"
```

---

## Rate Limiting

{From system specs or spec.md}

**Rate Limits:**
| Tier | Requests per Minute | Requests per Hour | Burst |
|------|---------------------|-------------------|-------|
| Free | {limit} | {limit} | {burst} |
| Pro | {limit} | {limit} | {burst} |
| Enterprise | {limit} | {limit} | {burst} |

**Headers:**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
```

**Rate Limit Exceeded:**
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

**Best Practices:**
- Implement exponential backoff
- Cache responses when possible
- Batch requests
- Monitor `X-RateLimit-Remaining` header

---

## Error Handling

{From OpenAPI responses and error schema}

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    },
    "requestId": "req_123456789"
  }
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no content to return |
| 400 | Bad Request | Invalid request (check `details`) |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Server temporarily unavailable |

### Error Codes

{Auto-generated from code analysis}

| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| `{ERROR_CODE}` | {status} | {description} | {how to fix} |

**Example Error:**
```bash
curl {api-url}/endpoint \
  -X POST \
  -d '{"invalid": "data"}'

# Response (400 Bad Request)
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": ["Email is required", "Email must be valid"]
    },
    "requestId": "req_abc123"
  }
}
```

---

## Pagination

{If pagination is implemented}

**Pagination Method:** {cursor/offset/page-based}

### Cursor-Based Pagination

```bash
# First page
curl "{api-url}/resources"

# Response
{
  "data": [...],
  "pagination": {
    "nextCursor": "cursor_abc123",
    "hasMore": true
  }
}

# Next page
curl "{api-url}/resources?cursor=cursor_abc123"
```

### Offset-Based Pagination

```bash
# Page 1 (limit 20)
curl "{api-url}/resources?limit=20&offset=0"

# Page 2
curl "{api-url}/resources?limit=20&offset=20"

# Response
{
  "data": [...],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 20,
    "totalPages": 8
  }
}
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 20 | Items per page (max: 100) |
| `offset` | integer | 0 | Number of items to skip |
| `cursor` | string | - | Pagination cursor |

---

## Filtering & Sorting

### Filtering

**Filter Syntax:**
```bash
# Single filter
curl "{api-url}/resources?status=active"

# Multiple filters (AND)
curl "{api-url}/resources?status=active&role=admin"

# Range filter
curl "{api-url}/resources?createdAt[gte]=2024-01-01&createdAt[lte]=2024-12-31"

# Array filter (IN)
curl "{api-url}/resources?category=tech,science,art"
```

**Available Operators:**
| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals (default) | `status=active` |
| `ne` | Not equals | `status[ne]=deleted` |
| `gt` | Greater than | `price[gt]=100` |
| `gte` | Greater than or equal | `createdAt[gte]=2024-01-01` |
| `lt` | Less than | `price[lt]=1000` |
| `lte` | Less than or equal | `createdAt[lte]=2024-12-31` |
| `in` | In array | `status[in]=active,pending` |
| `contains` | String contains | `name[contains]=test` |

### Sorting

```bash
# Sort ascending
curl "{api-url}/resources?sort=createdAt"

# Sort descending
curl "{api-url}/resources?sort=-createdAt"

# Multiple sort fields
curl "{api-url}/resources?sort=-priority,createdAt"
```

---

## Webhooks

{If webhooks are implemented}

**Webhook Events:**
{From spec.md or system specs}

| Event | Description | Payload |
|-------|-------------|---------|
| `{event.name}` | {description} | [{Schema}](#{schema-anchor}) |

**Configure Webhook:**
```bash
curl {api-url}/webhooks \
  -X POST \
  -H "Authorization: Bearer {token}" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["resource.created", "resource.updated"],
    "secret": "your-webhook-secret"
  }'
```

**Verify Webhook Signature:**
```{language}
{Webhook signature verification code}
```

**Webhook Payload Example:**
```json
{
  "event": "resource.created",
  "timestamp": "2024-03-20T14:30:00Z",
  "data": {
    ...
  }
}
```

---

## Endpoints

{Auto-generated from OpenAPI paths}

### {Resource Name}

{Resource description from OpenAPI tag description or FR-xxx}

---

#### Create {Resource}

```http
POST {base-url}/{resource}
```

**Description:** {From OpenAPI operation summary}

{Extended description from FR-xxx}

**Authentication:** Required
**Rate Limit:** {rate-limit}

**Request:**

**Headers:**
```http
Content-Type: application/json
Authorization: Bearer {token}
```

**Body:**
```json
{
  "{field}": "{type}",  // {description from schema}
  "{field2}": "{type}", // {description}
  "{optional-field}": "{type}"  // Optional: {description}
}
```

**Request Schema:** [{SchemaName}](#{schema-anchor})

**Example:**
```bash
curl {base-url}/{resource} \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "{field}": "{example-value}",
    "{field2}": "{example-value}"
  }'
```

**Response:**

**Success (201 Created):**
```json
{
  "id": "{generated-id}",
  "{field}": "{value}",
  "createdAt": "2024-03-20T14:30:00Z",
  "updatedAt": "2024-03-20T14:30:00Z"
}
```

**Response Schema:** [{SchemaName}](#{schema-anchor})

**Errors:**
| Status | Code | Description |
|--------|------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request data |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 409 | `CONFLICT` | Resource already exists |
| 422 | `UNPROCESSABLE_ENTITY` | Validation failed |

---

#### Get {Resource}

```http
GET {base-url}/{resource}/{id}
```

**Description:** {From OpenAPI operation summary}

**Authentication:** Required
**Rate Limit:** {rate-limit}

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | {type} | {description from OpenAPI} |

**Example:**
```bash
curl {base-url}/{resource}/{id} \
  -H "Authorization: Bearer {token}"
```

**Response:**

**Success (200 OK):**
```json
{
  "id": "{id}",
  "{field}": "{value}",
  ...
}
```

**Errors:**
| Status | Code | Description |
|--------|------|-------------|
| 404 | `NOT_FOUND` | Resource not found |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |

---

#### Update {Resource}

```http
PUT {base-url}/{resource}/{id}
PATCH {base-url}/{resource}/{id}
```

**Description:** {From OpenAPI operation summary}

**Methods:**
- `PUT` — Full replacement (all fields required)
- `PATCH` — Partial update (only specified fields)

{Repeat similar structure for UPDATE}

---

#### Delete {Resource}

```http
DELETE {base-url}/{resource}/{id}
```

**Description:** {From OpenAPI operation summary}

{Repeat similar structure for DELETE}

---

#### List {Resources}

```http
GET {base-url}/{resource}
```

**Description:** {From OpenAPI operation summary}

**Query Parameters:**
{From OpenAPI parameters}
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `{param}` | {type} | {default} | {description} |

{Include pagination, filtering, sorting documentation}

---

## Data Schemas

{From OpenAPI components/schemas}

### {SchemaName}

**Description:** {From schema description}

**Properties:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `{field}` | `{type}` | Yes/No | {description} |

**Example:**
```json
{
  "{field}": "{example-value}",
  ...
}
```

**Validation Rules:**
- `{field}`: {validation rules from schema}
- `{field2}`: {validation rules}

**Used In:**
- [{Endpoint 1}](#{endpoint-anchor})
- [{Endpoint 2}](#{endpoint-anchor})

---

## Examples

### Complete Workflow Example

{End-to-end example from AS-xxx or integration tests}

```bash
# 1. Authenticate
TOKEN=$(curl {api-url}/auth/login \
  -X POST \
  -d '{"email":"user@example.com","password":"pass"}' \
  | jq -r '.token')

# 2. Create resource
RESOURCE_ID=$(curl {api-url}/resource \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Example"}' \
  | jq -r '.id')

# 3. Get resource
curl {api-url}/resource/$RESOURCE_ID \
  -H "Authorization: Bearer $TOKEN"

# 4. Update resource
curl {api-url}/resource/$RESOURCE_ID \
  -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"active"}'

# 5. Delete resource
curl {api-url}/resource/$RESOURCE_ID \
  -X DELETE \
  -H "Authorization: Bearer $TOKEN"
```

---

## SDKs

**Official SDKs:**

### JavaScript/TypeScript
```bash
npm install {project-name}-sdk
```

```typescript
import { Client } from '{project-name}-sdk';

const client = new Client({
  apiKey: process.env.API_KEY
});

const resource = await client.resources.create({
  name: 'Example'
});
```

**Documentation:** [JavaScript SDK Docs]({sdk-docs-url})
**Repository:** [{sdk-repo-url}]({sdk-repo-url})

### Python
```bash
pip install {project-name}
```

```python
from {project_name} import Client

client = Client(api_key=os.getenv('API_KEY'))
resource = client.resources.create(name='Example')
```

**Documentation:** [Python SDK Docs]({sdk-docs-url})

### Go
```bash
go get {sdk-module-path}
```

```go
import "{sdk-module-path}"

client := {package}.NewClient("{api-key}")
resource, err := client.Resources.Create(ctx, &{package}.ResourceCreateRequest{
  Name: "Example",
})
```

---

## Changelog

{From contracts/api.yaml version history or CHANGELOG.md}

### Version {version} ({date})

**Breaking Changes:**
- {Breaking change description}

**New Endpoints:**
- `{endpoint}` — {description}

**Modified Endpoints:**
- `{endpoint}` — {change description}

**Deprecated:**
- `{endpoint}` — Use `{replacement}` instead (removal in v{version})

**Migration Guide:** [v{old} to v{new}](../changelog/migration-v{old}-to-v{new}.md)

---

*Last updated: {generation timestamp}*
*Generated from: {contracts/api.yaml}, {spec.md FR-xxx}, {code analysis}*
```

## Generation Instructions for AI Agents

### Step 1: Parse OpenAPI Specification

```python
openapi_spec = parse_openapi("contracts/api.yaml")

api_docs = {
    "version": openapi_spec.info.version,
    "base_url": openapi_spec.servers[0].url,
    "auth": openapi_spec.components.securitySchemes,
    "endpoints": openapi_spec.paths,
    "schemas": openapi_spec.components.schemas
}
```

### Step 2: Generate Endpoint Documentation

```python
for path, methods in openapi_spec.paths.items():
    for method, operation in methods.items():
        endpoint_doc = {
            "method": method.upper(),
            "path": path,
            "summary": operation.summary,
            "description": operation.description,
            "parameters": operation.parameters,
            "requestBody": operation.requestBody,
            "responses": operation.responses,
            "security": operation.security,
            "tags": operation.tags
        }

        # Enrich with FR-xxx context
        related_frs = find_related_requirements(operation, spec.md)
        endpoint_doc["business_context"] = related_frs

        # Add code examples
        endpoint_doc["examples"] = generate_code_examples(endpoint_doc)
```

### Step 3: Generate Schema Documentation

```python
for schema_name, schema in openapi_spec.components.schemas.items():
    schema_doc = {
        "name": schema_name,
        "description": schema.description,
        "properties": format_properties(schema.properties),
        "required": schema.required,
        "validation": extract_validation_rules(schema),
        "example": generate_example_from_schema(schema),
        "used_in": find_endpoints_using_schema(schema_name)
    }
```

### Step 4: Extract from Integration Tests

```python
# Find integration tests
test_files = find_files("tests/integration/*api*.{language}")

for test_file in test_files:
    examples = extract_request_response_examples(test_file)

    # Add real-world examples to endpoint docs
    for example in examples:
        add_example_to_endpoint(example.endpoint, example)
```

### Step 5: Generate Error Documentation

```python
# Extract error codes from code
error_codes = analyze_error_handling(codebase)

error_reference = []
for code in error_codes:
    error_reference.append({
        "code": code.error_code,
        "http_status": code.http_status,
        "description": code.description,
        "resolution": infer_resolution(code)
    })
```

## Auto-Update Markers

```markdown
<!-- speckit:auto:api-reference:authentication -->
{Auto-generated authentication documentation from OpenAPI}
<!-- /speckit:auto:api-reference:authentication -->

<!-- MANUAL SECTION - Additional notes -->
For internal systems, use service accounts...
<!-- /MANUAL SECTION -->
```

## Quality Checks

- [ ] All OpenAPI endpoints documented
- [ ] Request/response schemas included
- [ ] Authentication methods documented
- [ ] Error codes documented
- [ ] Rate limiting documented
- [ ] Code examples work (tested)
- [ ] SDK examples included
- [ ] Pagination documented (if applicable)
- [ ] Webhook examples (if applicable)
- [ ] Cross-references to user guides

---

**Template Version**: 1.0.0
**Compatible with**: spec-kit v0.6.0+
**Last Updated**: 2024-03-20
