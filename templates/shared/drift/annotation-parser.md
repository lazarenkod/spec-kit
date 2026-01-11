# Annotation Parser

## Purpose

Parse @speckit annotations from code comments and docstrings to enable bidirectional traceability between specifications and implementation.

## Supported Annotation Types

```yaml
annotations:
  FR:
    pattern: "@speckit:FR:(FR-\\d+)"
    description: "Links code to functional requirement"
    example: "// @speckit:FR:FR-001 User authentication"

  AS:
    pattern: "@speckit:AS:(AS-\\w+)"
    description: "Links code to acceptance scenario"
    example: "// @speckit:AS:AS-1A Login success case"

  COMP:
    pattern: "\\[COMP:(COMP-\\d+)\\]"
    description: "Marks component creation/usage"
    example: "// [COMP:COMP-001] LoginButton component"

  WIRE:
    pattern: "\\[WIRE:(COMP-\\d+)→(SCR-\\d+)\\]"
    description: "Links component to screen"
    example: "// [WIRE:COMP-001→SCR-01] Wire button to login screen"

  TEST:
    pattern: "\\[TEST:(AS-\\w+)\\]"
    description: "Links test to acceptance scenario"
    example: "// [TEST:AS-1A] Test for login success"

  INTERNAL:
    pattern: "@internal"
    description: "Marks function as internal-only (not public API)"
    example: "// @internal - helper function"
```

---

## Core Algorithm

```text
PARSE_ANNOTATIONS(file_path):
  content = read_file(file_path)

  annotations = {
    FR: [],
    AS: [],
    COMP: [],
    WIRE: [],
    TEST: [],
    INTERNAL: false
  }

  # Parse each annotation type
  FOR annotation_type, pattern IN ANNOTATION_PATTERNS:
    matches = REGEX_FINDALL(pattern, content)

    FOR match IN matches:
      line_number = GET_LINE_NUMBER(content, match)
      context = GET_SURROUNDING_LINES(content, line_number, before=2, after=2)

      annotation_entry = {
        type: annotation_type,
        id: match.group(1) IF annotation_type != "INTERNAL" ELSE null,
        file: file_path,
        line: line_number,
        context: context,
        raw_match: match
      }

      IF annotation_type == "INTERNAL":
        annotations.INTERNAL = true
      ELSE:
        annotations[annotation_type].append(annotation_entry)

  RETURN annotations
```

---

## Language-Specific Extraction

### TypeScript

```text
PARSE_ANNOTATIONS_TS(file_content):
  annotations = DEFAULT_ANNOTATIONS()

  # Single-line comments: // @speckit:FR:FR-001
  single_line = REGEX_FINDALL(r"//\s*@speckit:(FR|AS):([\w-]+)", file_content)
  FOR type, id IN single_line:
    annotations[type].append(id)

  # Multi-line comments: /* @speckit:FR:FR-001 */
  multi_line = REGEX_FINDALL(r"/\*.*?@speckit:(FR|AS):([\w-]+).*?\*/", file_content, DOTALL)
  FOR type, id IN multi_line:
    annotations[type].append(id)

  # JSDoc comments: /** @speckit:FR:FR-001 */
  jsdoc = REGEX_FINDALL(r"/\*\*.*?@speckit:(FR|AS):([\w-]+).*?\*/", file_content, DOTALL)
  FOR type, id IN jsdoc:
    annotations[type].append(id)

  # Task markers in code: [TEST:AS-1A], [COMP:COMP-001]
  task_markers = REGEX_FINDALL(r"\[(TEST|COMP|WIRE):([^\]]+)\]", file_content)
  FOR type, id IN task_markers:
    annotations[type].append(id)

  # @internal marker
  IF "@internal" IN file_content OR "// @internal" IN file_content:
    annotations.INTERNAL = true

  RETURN annotations
```

**Example Input**:
```typescript
/**
 * @speckit:FR:FR-001 User registration endpoint
 * Handles new user creation with email/password
 */
export async function createUser(data: UserData) {
  // @speckit:AS:AS-1A Validate email format
  if (!validateEmail(data.email)) {
    throw new ValidationError("Invalid email");
  }
  // Implementation...
}

// @internal - Helper function (not public API)
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

**Extracted**:
```yaml
annotations:
  FR: ["FR-001"]
  AS: ["AS-1A"]
  INTERNAL: true  # For validateEmail
```

---

### Python

```text
PARSE_ANNOTATIONS_PY(file_content):
  annotations = DEFAULT_ANNOTATIONS()

  # Inline comments: # @speckit:FR:FR-001
  inline = REGEX_FINDALL(r"#\s*@speckit:(FR|AS):([\w-]+)", file_content)
  FOR type, id IN inline:
    annotations[type].append(id)

  # Docstrings (triple-quoted): """@speckit:FR:FR-001"""
  docstrings = REGEX_FINDALL(r'""".*?@speckit:(FR|AS):([\w-]+).*?"""', file_content, DOTALL)
  FOR type, id IN docstrings:
    annotations[type].append(id)

  # Single-quoted docstrings: '''@speckit:FR:FR-001'''
  single_docstrings = REGEX_FINDALL(r"'''.*?@speckit:(FR|AS):([\w-]+).*?'''", file_content, DOTALL)
  FOR type, id IN single_docstrings:
    annotations[type].append(id)

  # Task markers: [TEST:AS-1A]
  task_markers = REGEX_FINDALL(r"\[(TEST|COMP):([^\]]+)\]", file_content)
  FOR type, id IN task_markers:
    annotations[type].append(id)

  # @internal or # @internal
  IF "@internal" IN file_content OR "# @internal" IN file_content:
    annotations.INTERNAL = true

  RETURN annotations
```

**Example Input**:
```python
@app.post("/api/v1/users")
async def create_user(data: UserData):
    """
    @speckit:FR:FR-001 User registration endpoint
    Handles new user creation with email/password
    """
    # @speckit:AS:AS-1A Validate email format
    if not validate_email(data.email):
        raise ValidationError("Invalid email")
    # Implementation...

# @internal - Helper function
def validate_email(email: str) -> bool:
    return "@" in email and "." in email
```

**Extracted**:
```yaml
annotations:
  FR: ["FR-001"]
  AS: ["AS-1A"]
  INTERNAL: true  # For validate_email
```

---

### Go

```text
PARSE_ANNOTATIONS_GO(file_content):
  annotations = DEFAULT_ANNOTATIONS()

  # Single-line comments: // @speckit:FR:FR-001
  single_line = REGEX_FINDALL(r"//\s*@speckit:(FR|AS):([\w-]+)", file_content)
  FOR type, id IN single_line:
    annotations[type].append(id)

  # Multi-line comments: /* @speckit:FR:FR-001 */
  multi_line = REGEX_FINDALL(r"/\*.*?@speckit:(FR|AS):([\w-]+).*?\*/", file_content, DOTALL)
  FOR type, id IN multi_line:
    annotations[type].append(id)

  # Task markers: [TEST:AS-1A]
  task_markers = REGEX_FINDALL(r"\[(TEST|COMP):([^\]]+)\]", file_content)
  FOR type, id IN task_markers:
    annotations[type].append(id)

  # @internal
  IF "// @internal" IN file_content:
    annotations.INTERNAL = true

  RETURN annotations
```

**Example Input**:
```go
// @speckit:FR:FR-001 User registration endpoint
// Handles new user creation with email/password
func CreateUser(c *gin.Context) {
    var user UserData
    // @speckit:AS:AS-1A Validate email format
    if !validateEmail(user.Email) {
        c.JSON(400, gin.H{"error": "Invalid email"})
        return
    }
    // Implementation...
}

// @internal
// validateEmail is a helper function (not exported)
func validateEmail(email string) bool {
    return strings.Contains(email, "@")
}
```

**Extracted**:
```yaml
annotations:
  FR: ["FR-001"]
  AS: ["AS-1A"]
  INTERNAL: true  # For validateEmail
```

---

### Java/Kotlin

```text
PARSE_ANNOTATIONS_JVM(file_content):
  annotations = DEFAULT_ANNOTATIONS()

  # Single-line comments: // @speckit:FR:FR-001
  single_line = REGEX_FINDALL(r"//\s*@speckit:(FR|AS):([\w-]+)", file_content)
  FOR type, id IN single_line:
    annotations[type].append(id)

  # Multi-line comments: /* @speckit:FR:FR-001 */
  multi_line = REGEX_FINDALL(r"/\*.*?@speckit:(FR|AS):([\w-]+).*?\*/", file_content, DOTALL)
  FOR type, id IN multi_line:
    annotations[type].append(id)

  # JavaDoc comments: /** @speckit:FR:FR-001 */
  javadoc = REGEX_FINDALL(r"/\*\*.*?@speckit:(FR|AS):([\w-]+).*?\*/", file_content, DOTALL)
  FOR type, id IN javadoc:
    annotations[type].append(id)

  # Task markers: [TEST:AS-1A]
  task_markers = REGEX_FINDALL(r"\[(TEST|COMP):([^\]]+)\]", file_content)
  FOR type, id IN task_markers:
    annotations[type].append(id)

  # @internal
  IF "@internal" IN file_content OR "// @internal" IN file_content:
    annotations.INTERNAL = true

  RETURN annotations
```

**Example Input (Java)**:
```java
/**
 * @speckit:FR:FR-001 User registration endpoint
 * Handles new user creation with email/password
 */
@PostMapping("/api/v1/users")
public ResponseEntity<User> createUser(@RequestBody UserData data) {
    // @speckit:AS:AS-1A Validate email format
    if (!validateEmail(data.getEmail())) {
        return ResponseEntity.badRequest().build();
    }
    // Implementation...
}

// @internal
private boolean validateEmail(String email) {
    return email.contains("@");
}
```

**Extracted**:
```yaml
annotations:
  FR: ["FR-001"]
  AS: ["AS-1A"]
  INTERNAL: true  # For validateEmail
```

---

## Utility Functions

### Get Line Number

```text
GET_LINE_NUMBER(content, match_text):
  lines = content.split("\n")
  FOR i, line IN enumerate(lines):
    IF match_text IN line:
      RETURN i + 1  # 1-indexed
  RETURN null
```

### Get Surrounding Lines

```text
GET_SURROUNDING_LINES(content, line_number, before=2, after=2):
  lines = content.split("\n")
  start = max(0, line_number - 1 - before)  # 0-indexed
  end = min(len(lines), line_number + after)

  context_lines = lines[start:end]
  context = "\n".join(context_lines)

  RETURN context
```

### Extract All Annotations from Codebase

```text
EXTRACT_ALL_ANNOTATIONS(scope_files):
  all_annotations = {
    FR: {},     # FR-001: [{file, line, context}, ...]
    AS: {},     # AS-1A: [{file, line, context}, ...]
    COMP: {},
    WIRE: {},
    TEST: {},
    INTERNAL: []  # [{file, line, function_name}, ...]
  }

  FOR file IN scope_files:
    file_annotations = PARSE_ANNOTATIONS(file)

    # Group by ID
    FOR fr IN file_annotations.FR:
      IF fr.id NOT IN all_annotations.FR:
        all_annotations.FR[fr.id] = []
      all_annotations.FR[fr.id].append({
        file: file,
        line: fr.line,
        context: fr.context
      })

    FOR as IN file_annotations.AS:
      IF as.id NOT IN all_annotations.AS:
        all_annotations.AS[as.id] = []
      all_annotations.AS[as.id].append({
        file: file,
        line: as.line,
        context: as.context
      })

    # Track internal functions
    IF file_annotations.INTERNAL:
      all_annotations.INTERNAL.append({
        file: file,
        # Extract function name from context
        function_name: EXTRACT_FUNCTION_NAME(file)
      })

  RETURN all_annotations
```

---

## Validation

### Validate Annotation Format

```text
VALIDATE_ANNOTATION(annotation):
  # Check FR format: FR-001, FR-123, etc.
  IF annotation.type == "FR":
    IF NOT REGEX_MATCH(r"^FR-\d{3}$", annotation.id):
      OUTPUT: "Warning: FR annotation format mismatch: {annotation.id}"
      RETURN false

  # Check AS format: AS-1A, AS-2B, etc.
  IF annotation.type == "AS":
    IF NOT REGEX_MATCH(r"^AS-\d+[A-Z]$", annotation.id):
      OUTPUT: "Warning: AS annotation format mismatch: {annotation.id}"
      RETURN false

  # Check COMP format: COMP-001, COMP-123
  IF annotation.type == "COMP":
    IF NOT REGEX_MATCH(r"^COMP-\d{3}$", annotation.id):
      OUTPUT: "Warning: COMP annotation format mismatch: {annotation.id}"
      RETURN false

  RETURN true
```

### Detect Orphan Annotations

```text
DETECT_ORPHAN_ANNOTATIONS(code_annotations, spec):
  orphans = []

  # Check if annotated FRs exist in spec
  spec_frs = EXTRACT_FRS(spec)

  FOR fr_id, locations IN code_annotations.FR:
    IF fr_id NOT IN spec_frs:
      orphans.append({
        type: "orphan_annotation",
        annotation: fr_id,
        locations: locations,
        recommendation: "Add {fr_id} to spec.md or remove annotation"
      })

  # Check if annotated ASs exist in spec
  spec_ass = EXTRACT_ASS(spec)

  FOR as_id, locations IN code_annotations.AS:
    IF as_id NOT IN spec_ass:
      orphans.append({
        type: "orphan_annotation",
        annotation: as_id,
        locations: locations,
        recommendation: "Add {as_id} to spec.md or remove annotation"
      })

  RETURN orphans
```

---

## Integration with Drift Detection

```text
# In Pass AA

# Step 1: Extract annotations from codebase
code_annotations = EXTRACT_ALL_ANNOTATIONS(scope_files)

# Step 2: Extract requirements from spec
spec_frs = EXTRACT_FRS(spec.md)
spec_ass = EXTRACT_ASS(spec.md)

# Step 3: Detect forward drift (spec → code)
forward_drift = []
FOR fr IN spec_frs:
  IF fr.id NOT IN code_annotations.FR:
    forward_drift.append({
      type: "unimplemented_requirement",
      fr: fr.id,
      description: fr.description
    })

# Step 4: Detect reverse drift (code → spec)
reverse_drift = []
FOR fr_id IN code_annotations.FR.keys():
  IF fr_id NOT IN spec_frs:
    reverse_drift.append({
      type: "orphan_annotation",
      annotation: fr_id,
      locations: code_annotations.FR[fr_id]
    })

# Step 5: Generate drift report
GENERATE_DRIFT_REPORT(forward_drift, reverse_drift)
```

---

## Output Format

### Annotation Registry

```yaml
# .annotation-registry.yaml (for caching)
version: "1.0"
last_scanned: "2026-01-11T10:30:00Z"
annotations:
  FR:
    FR-001:
      - file: "src/api/users.ts"
        line: 42
        context: "export async function createUser..."
      - file: "src/services/user-service.ts"
        line: 15
        context: "class UserService implements..."
    FR-002:
      - file: "src/api/auth.ts"
        line: 28
        context: "export async function login..."

  AS:
    AS-1A:
      - file: "tests/e2e/login.test.ts"
        line: 10
        context: "// [TEST:AS-1A]"
    AS-1B:
      - file: "tests/e2e/login.test.ts"
        line: 25
        context: "// [TEST:AS-1B]"

  INTERNAL:
    - file: "src/utils/helpers.ts"
      function: "validateEmail"
      line: 50
    - file: "src/utils/crypto.ts"
      function: "hashPassword"
      line: 12

stats:
  total_fr_annotations: 15
  total_as_annotations: 20
  total_internal_markers: 8
  files_with_annotations: 12
```

### Annotation Coverage Report

```markdown
# Annotation Coverage Report

## FR Coverage

| FR | Annotated | Files | Lines |
|----|-----------|-------|-------|
| FR-001 | ✅ Yes | 2 | users.ts:42, user-service.ts:15 |
| FR-002 | ✅ Yes | 1 | auth.ts:28 |
| FR-003 | ❌ No | 0 | - |

**FR Coverage**: 67% (2/3 FRs annotated)

## AS Coverage

| AS | Annotated | Test Files | Lines |
|----|-----------|-----------|-------|
| AS-1A | ✅ Yes | 1 | login.test.ts:10 |
| AS-1B | ✅ Yes | 1 | login.test.ts:25 |
| AS-2A | ❌ No | 0 | - |

**AS Coverage**: 67% (2/3 ASs annotated)

## Internal Functions

| File | Function | Line | Purpose |
|------|----------|------|---------|
| utils/helpers.ts | validateEmail | 50 | Email validation |
| utils/crypto.ts | hashPassword | 12 | Password hashing |

**Total Internal**: 8 functions

---

## Recommendations

1. **Missing Annotations**: Add @speckit:FR:FR-003 to codebase
2. **Missing Tests**: Create test with [TEST:AS-2A] marker
3. **Orphan Annotations**: None found ✅
```

---

## Error Handling

```text
TRY:
  annotations = PARSE_ANNOTATIONS(file)
CATCH FileNotFoundError:
  OUTPUT: "Warning: File not found: {file}"
  RETURN DEFAULT_ANNOTATIONS()
CATCH UnicodeDecodeError:
  OUTPUT: "Warning: Cannot decode {file} (binary file?)"
  RETURN DEFAULT_ANNOTATIONS()
CATCH Exception as e:
  OUTPUT: "Error parsing {file}: {e}"
  RETURN DEFAULT_ANNOTATIONS()
```

---

## Performance Optimization

### Use Serena MCP search_for_pattern

```text
# Instead of reading each file individually:
FOR file IN files:
  content = read_file(file)
  annotations = PARSE_ANNOTATIONS(content)

# Use Serena search across all files at once:
fr_matches = search_for_pattern(
  substring_pattern=r"@speckit:FR:(FR-\d+)",
  relative_path="src/",
  output_mode="content",
  context_lines_before=2,
  context_lines_after=2
)

# Returns all matches with context, much faster
```

### Cache Results

```yaml
# .annotation-cache.yaml
caches:
  - file: "src/api/users.ts"
    checksum: "sha256:abc123..."
    annotations:
      FR: ["FR-001"]
      AS: ["AS-1A"]
      INTERNAL: false
```

```text
PARSE_WITH_CACHE(file):
  current_checksum = CALCULATE_CHECKSUM(file)
  cached = LOAD_CACHE(file)

  IF cached AND cached.checksum == current_checksum:
    RETURN cached.annotations  # Cache hit
  ELSE:
    annotations = PARSE_ANNOTATIONS(file)  # Cache miss
    SAVE_CACHE(file, annotations, current_checksum)
    RETURN annotations
```

---

## Testing

**Test Fixture**:
```typescript
// test-fixtures/annotated-code.ts

// @speckit:FR:FR-001 User registration
export async function createUser(data: UserData) {
  // @speckit:AS:AS-1A Validate email
  if (!data.email.includes("@")) {
    throw new Error("Invalid email");
  }
}

// @internal
function helper() {
  // Internal utility
}
```

**Expected Output**:
```yaml
annotations:
  FR: ["FR-001"]
  AS: ["AS-1A"]
  INTERNAL: true
```
