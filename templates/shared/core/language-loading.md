# Language Loading

## Purpose

Unified language detection and loading for all Spec Kit commands. This module ensures consistent multi-language support across all artifact generation.

## Instructions for AI Agents

Execute these steps at the **start** of any artifact-generating command.

### Step 1: Read Constitution

```text
Read /memory/constitution.md
Search for "Project Settings" section (table format)
```

### Step 2: Extract Language Code

```text
IF "Project Settings" table exists:
  Look for row where first column = "language" (case-insensitive)
  ARTIFACT_LANGUAGE = value from second column (e.g., "ru", "en", "de")
ELSE:
  ARTIFACT_LANGUAGE = "en" (default)
```

### Step 3: Resolve Language Name

| Code | Language Name |
|------|---------------|
| `en` | English |
| `ru` | Russian |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `zh` | Chinese |
| `ja` | Japanese |
| `ko` | Korean |
| `pt` | Portuguese |
| `uk` | Ukrainian |
| `pl` | Polish |
| `ar` | Arabic |

### Step 4: Apply Language Rules

Reference `templates/shared/language-context.md` for detailed translation rules:

**Translate to ARTIFACT_LANGUAGE**:
- Section headers
- Requirement descriptions
- User stories and acceptance criteria
- Comments, notes, validation messages
- UX/UI text

**Keep in English** (never translate):
- IDs: FR-001, AS-001, T001, etc.
- Technical terms: API, REST, JWT, CRUD, HTTP
- Code snippets and variable names
- File paths and URLs
- RFC 2119 keywords: MUST, SHOULD, MAY

### Step 5: Confirm Language

Output confirmation message:

```text
"Generating {ARTIFACT_TYPE} in {LANGUAGE_NAME} ({ARTIFACT_LANGUAGE})..."
```

## Usage in Commands

Add to any command's Step 0:

```markdown
## Step 0: Load Project Language

Read `templates/shared/core/language-loading.md` and apply.
Store ARTIFACT_LANGUAGE for use throughout this command.
```

## Fallback Behavior

If constitution.md is missing or unreadable:
1. Log warning: "Constitution not found, using English as default"
2. Set ARTIFACT_LANGUAGE = "en"
3. Continue with command execution

## Caching Hint

For performance, cache the parsed constitution for the session:
- Key: `/memory/constitution.md` checksum
- Value: `{language: ARTIFACT_LANGUAGE, principles: [...], domains: [...]}`
- TTL: 1 hour or until file modification detected
