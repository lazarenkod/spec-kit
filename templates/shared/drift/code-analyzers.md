# Language-Specific Code Analyzers

## Purpose

Provide language-specific patterns and Serena MCP integration for extracting public APIs, annotations, and validation rules from codebases in TypeScript, Python, Go, and Java/Kotlin.

## Serena MCP Integration

All analyzers use Serena MCP tools for AST parsing and code analysis:

```text
SERENA_MCP_TOOLS = {
  list_dir: "List files and directories",
  find_file: "Find files by pattern",
  find_symbol: "Extract symbols (functions, classes, methods)",
  search_for_pattern: "Regex search for annotations",
  read_file: "Read file contents"
}
```

**LSP Symbol Kinds**:
```text
SYMBOL_KINDS = {
  1: "File",
  2: "Module",
  3: "Namespace",
  4: "Package",
  5: "Class",
  6: "Method",
  7: "Property",
  8: "Field",
  9: "Constructor",
  10: "Enum",
  11: "Interface",
  12: "Function",
  13: "Variable",
  14: "Constant"
}
```

---

## TypeScript Analyzer

### Configuration

```yaml
typescript_analyzer:
  file_patterns: ["*.ts", "*.tsx"]
  exclude_patterns: ["*.d.ts", "*.test.ts", "*.spec.ts", "node_modules/**"]
  frameworks:
    - express
    - nestjs
    - next
    - react
  validation_libraries:
    - zod
    - joi
    - yup
    - class-validator
```

### Public API Detection

```text
ANALYZE_TYPESCRIPT(scope_files):
  typescript_files = FILTER(scope_files, "*.ts", "*.tsx")
  typescript_files = EXCLUDE(typescript_files, "*.test.*", "*.spec.*", "*.d.ts")

  apis = []

  FOR file IN typescript_files:
    # Use Serena find_symbol to extract functions and methods
    symbols = find_symbol(
      name_path_pattern="*",
      relative_path=file,
      include_kinds=[12, 6],  # 12=Function, 6=Method
      include_body=true
    )

    FOR symbol IN symbols:
      # Skip private (starts with _ or #)
      IF symbol.name.startswith("_") OR symbol.name.startswith("#"):
        CONTINUE

      # Check visibility
      IF "export" IN symbol.body:
        visibility = "public"
      ELSE:
        visibility = "private"
        CONTINUE  # Skip private

      # Detect framework patterns
      api_type = DETECT_API_TYPE_TS(symbol)

      # Extract annotations
      annotations = PARSE_ANNOTATIONS_TS(symbol.body)

      # Check for @internal marker
      is_internal = "@internal" IN symbol.body OR "// @internal" IN symbol.body

      api = {
        type: api_type,
        language: "typescript",
        file: file,
        line: symbol.line,
        name: symbol.name,
        signature: symbol.signature,
        visibility: visibility,
        annotations: annotations,
        is_internal: is_internal,
        body_sample: symbol.body[:200]  # First 200 chars for context
      }

      apis.append(api)

  RETURN apis
```

### Framework Pattern Detection

```text
DETECT_API_TYPE_TS(symbol):
  body = symbol.body

  # Express routes
  IF REGEX_MATCH(r"router\.(get|post|put|delete|patch)\(", body):
    method = REGEX_EXTRACT(r"router\.(\w+)\(", body)
    route = REGEX_EXTRACT(r"router\.\w+\(['\"]([^'\"]+)['\"]", body)
    RETURN {
      category: "REST_API",
      framework: "express",
      method: method.upper(),
      endpoint: route
    }

  # NestJS decorators
  IF REGEX_MATCH(r"@(Get|Post|Put|Delete|Patch)", body):
    method = REGEX_EXTRACT(r"@(Get|Post|Put|Delete|Patch)", body)
    route = REGEX_EXTRACT(r"@\w+\(['\"]([^'\"]*)['\"]?\)", body) OR ""
    RETURN {
      category: "REST_API",
      framework: "nestjs",
      method: method.upper(),
      endpoint: route
    }

  # Next.js API routes (in pages/api/ or app/api/)
  IF "/api/" IN symbol.file:
    # File path IS the route
    route = EXTRACT_NEXTJS_ROUTE(symbol.file)
    RETURN {
      category: "REST_API",
      framework: "nextjs",
      method: "MULTI",  # Next.js handlers can be GET/POST/etc.
      endpoint: route
    }

  # React components (exported functions returning JSX)
  IF "return (" IN body OR "return <" IN body:
    IF symbol.name[0].isupper():  # React components are PascalCase
      RETURN {
        category: "COMPONENT",
        framework: "react",
        component_name: symbol.name
      }

  # Exported utility/business logic functions
  IF "export" IN body:
    RETURN {
      category: "UTILITY",
      framework: null,
      function_name: symbol.name
    }

  # Default
  RETURN {
    category: "UNKNOWN",
    framework: null
  }
```

### Annotation Extraction

```text
PARSE_ANNOTATIONS_TS(code):
  annotations = {
    FR: [],
    AS: [],
    COMP: [],
    INTERNAL: false
  }

  # @speckit:FR:FR-xxx
  fr_matches = REGEX_FINDALL(r"@speckit:FR:(FR-\d+)", code)
  annotations.FR = fr_matches

  # @speckit:AS:AS-xxx
  as_matches = REGEX_FINDALL(r"@speckit:AS:(AS-\w+)", code)
  annotations.AS = as_matches

  # [COMP:COMP-xxx]
  comp_matches = REGEX_FINDALL(r"\[COMP:(COMP-\d+)\]", code)
  annotations.COMP = comp_matches

  # @internal marker
  IF "@internal" IN code OR "// @internal" IN code OR "/* @internal */" IN code:
    annotations.INTERNAL = true

  RETURN annotations
```

### Validation Rule Detection

```text
DETECT_VALIDATION_TS(symbol):
  body = symbol.body
  rules = []

  # Zod schemas
  IF "z." IN body:
    # z.string()
    IF "z.string()" IN body:
      rules.append({type: "string", library: "zod"})

    # .email()
    IF ".email()" IN body:
      rules.append({type: "email", library: "zod"})

    # .min(N), .max(N)
    min_val = REGEX_EXTRACT(r"\.min\((\d+)\)", body)
    IF min_val:
      rules.append({type: "min_length", value: min_val, library: "zod"})

    max_val = REGEX_EXTRACT(r"\.max\((\d+)\)", body)
    IF max_val:
      rules.append({type: "max_length", value: max_val, library: "zod"})

  # Class-validator decorators
  decorators = REGEX_FINDALL(r"@(IsEmail|IsString|IsNumber|Min|Max|Length)", body)
  FOR decorator IN decorators:
    rules.append({type: decorator.lower(), library: "class-validator"})

  RETURN rules
```

---

## Python Analyzer

### Configuration

```yaml
python_analyzer:
  file_patterns: ["*.py"]
  exclude_patterns: ["test_*.py", "*_test.py", "conftest.py", "__pycache__/**"]
  frameworks:
    - fastapi
    - flask
    - django
  validation_libraries:
    - pydantic
    - marshmallow
    - django-validators
```

### Public API Detection

```text
ANALYZE_PYTHON(scope_files):
  python_files = FILTER(scope_files, "*.py")
  python_files = EXCLUDE(python_files, "test_*", "*_test.py")

  apis = []

  FOR file IN python_files:
    symbols = find_symbol(
      name_path_pattern="*",
      relative_path=file,
      include_kinds=[12, 6],  # Function, Method
      include_body=true
    )

    FOR symbol IN symbols:
      # Skip private (starts with _)
      IF symbol.name.startswith("_"):
        CONTINUE

      # All non-_ prefixed are public in Python
      visibility = "public"

      # Detect framework patterns
      api_type = DETECT_API_TYPE_PY(symbol)

      # Extract annotations
      annotations = PARSE_ANNOTATIONS_PY(symbol.body)

      # Check for @internal or # @internal
      is_internal = "@internal" IN symbol.body OR "# @internal" IN symbol.body

      api = {
        type: api_type,
        language: "python",
        file: file,
        line: symbol.line,
        name: symbol.name,
        signature: symbol.signature,
        visibility: visibility,
        annotations: annotations,
        is_internal: is_internal,
        body_sample: symbol.body[:200]
      }

      apis.append(api)

  RETURN apis
```

### Framework Pattern Detection

```text
DETECT_API_TYPE_PY(symbol):
  body = symbol.body

  # FastAPI decorators
  IF REGEX_MATCH(r"@app\.(get|post|put|delete|patch)", body):
    method = REGEX_EXTRACT(r"@app\.(\w+)", body)
    route = REGEX_EXTRACT(r"@app\.\w+\(['\"]([^'\"]+)['\"]", body)
    RETURN {
      category: "REST_API",
      framework: "fastapi",
      method: method.upper(),
      endpoint: route
    }

  # Flask decorators
  IF REGEX_MATCH(r"@app\.route\(", body):
    route = REGEX_EXTRACT(r"@app\.route\(['\"]([^'\"]+)['\"]", body)
    methods = REGEX_EXTRACT(r"methods=\[([^\]]+)\]", body) OR ["GET"]
    RETURN {
      category: "REST_API",
      framework: "flask",
      method: methods[0] IF isinstance(methods, list) ELSE "GET",
      endpoint: route
    }

  # Django view functions
  IF "HttpRequest" IN symbol.signature OR "request" IN symbol.signature:
    IF "def " + symbol.name IN body:
      RETURN {
        category: "VIEW",
        framework: "django",
        view_name: symbol.name
      }

  # Pydantic models (classes, not functions)
  IF "BaseModel" IN body:
    RETURN {
      category: "MODEL",
      framework: "pydantic",
      model_name: symbol.name
    }

  # Public function
  RETURN {
    category: "UTILITY",
    framework: null,
    function_name: symbol.name
  }
```

### Annotation Extraction

```text
PARSE_ANNOTATIONS_PY(code):
  annotations = {
    FR: [],
    AS: [],
    INTERNAL: false
  }

  # @speckit:FR:FR-xxx (in docstring or comment)
  fr_matches = REGEX_FINDALL(r"@speckit:FR:(FR-\d+)", code)
  annotations.FR = fr_matches

  # @speckit:AS:AS-xxx
  as_matches = REGEX_FINDALL(r"@speckit:AS:(AS-\w+)", code)
  annotations.AS = as_matches

  # @internal or # @internal
  IF "@internal" IN code OR "# @internal" IN code:
    annotations.INTERNAL = true

  RETURN annotations
```

### Validation Rule Detection

```text
DETECT_VALIDATION_PY(symbol):
  body = symbol.body
  rules = []

  # Pydantic Field validators
  IF "Field(" IN body:
    min_length = REGEX_EXTRACT(r"Field\(.*min_length=(\d+)", body)
    IF min_length:
      rules.append({type: "min_length", value: min_length, library: "pydantic"})

    max_length = REGEX_EXTRACT(r"Field\(.*max_length=(\d+)", body)
    IF max_length:
      rules.append({type: "max_length", value: max_length, library: "pydantic"})

  # Type hints with validation
  IF "EmailStr" IN body:
    rules.append({type: "email", library: "pydantic"})

  IF "UUID" IN body:
    rules.append({type: "uuid", library: "pydantic"})

  # Django validators
  validators = REGEX_FINDALL(r"validators=\[(MinLength|MaxLength|EmailValidator)", body)
  FOR validator IN validators:
    rules.append({type: validator.lower(), library: "django"})

  RETURN rules
```

---

## Go Analyzer

### Configuration

```yaml
go_analyzer:
  file_patterns: ["*.go"]
  exclude_patterns: ["*_test.go", "vendor/**"]
  frameworks:
    - gin
    - echo
    - chi
    - fiber
  validation_libraries:
    - validator
    - govalidator
```

### Public API Detection

```text
ANALYZE_GO(scope_files):
  go_files = FILTER(scope_files, "*.go")
  go_files = EXCLUDE(go_files, "*_test.go")

  apis = []

  FOR file IN go_files:
    symbols = find_symbol(
      name_path_pattern="*",
      relative_path=file,
      include_kinds=[12, 6],  # Function, Method
      include_body=true
    )

    FOR symbol IN symbols:
      # Go exported = capitalized first letter
      IF NOT symbol.name[0].isupper():
        CONTINUE  # Private (lowercase)

      visibility = "public"  # All uppercase = exported

      # Detect framework patterns
      api_type = DETECT_API_TYPE_GO(symbol)

      # Extract annotations
      annotations = PARSE_ANNOTATIONS_GO(symbol.body)

      # Check for @internal comment
      is_internal = "// @internal" IN symbol.body

      api = {
        type: api_type,
        language: "go",
        file: file,
        line: symbol.line,
        name: symbol.name,
        signature: symbol.signature,
        visibility: visibility,
        annotations: annotations,
        is_internal: is_internal,
        body_sample: symbol.body[:200]
      }

      apis.append(api)

  RETURN apis
```

### Framework Pattern Detection

```text
DETECT_API_TYPE_GO(symbol):
  body = symbol.body

  # Gin routes
  IF REGEX_MATCH(r"router\.(GET|POST|PUT|DELETE|PATCH)\(", body):
    method = REGEX_EXTRACT(r"router\.(\w+)\(", body)
    route = REGEX_EXTRACT(r"router\.\w+\(['\"]([^'\"]+)['\"]", body)
    RETURN {
      category: "REST_API",
      framework: "gin",
      method: method,
      endpoint: route
    }

  # Chi routes
  IF REGEX_MATCH(r"r\.(Get|Post|Put|Delete|Patch)\(", body):
    method = REGEX_EXTRACT(r"r\.(\w+)\(", body)
    route = REGEX_EXTRACT(r"r\.\w+\(['\"]([^'\"]+)['\"]", body)
    RETURN {
      category: "REST_API",
      framework: "chi",
      method: method.upper(),
      endpoint: route
    }

  # Echo routes
  IF REGEX_MATCH(r"e\.(GET|POST|PUT|DELETE|PATCH)\(", body):
    method = REGEX_EXTRACT(r"e\.(\w+)\(", body)
    route = REGEX_EXTRACT(r"e\.\w+\(['\"]([^'\"]+)['\"]", body)
    RETURN {
      category: "REST_API",
      framework: "echo",
      method: method,
      endpoint: route
    }

  # Structs (exported types)
  IF "type " + symbol.name + " struct" IN body:
    RETURN {
      category: "STRUCT",
      framework: null,
      struct_name: symbol.name
    }

  # Exported function
  RETURN {
    category: "UTILITY",
    framework: null,
    function_name: symbol.name
  }
```

### Annotation Extraction

```text
PARSE_ANNOTATIONS_GO(code):
  annotations = {
    FR: [],
    AS: [],
    INTERNAL: false
  }

  # // @speckit:FR:FR-xxx
  fr_matches = REGEX_FINDALL(r"// @speckit:FR:(FR-\d+)", code)
  annotations.FR = fr_matches

  # // @speckit:AS:AS-xxx
  as_matches = REGEX_FINDALL(r"// @speckit:AS:(AS-\w+)", code)
  annotations.AS = as_matches

  # // @internal
  IF "// @internal" IN code:
    annotations.INTERNAL = true

  RETURN annotations
```

### Validation Rule Detection

```text
DETECT_VALIDATION_GO(symbol):
  body = symbol.body
  rules = []

  # Struct tags with validation
  tag_matches = REGEX_FINDALL(r'`validate:"([^"]+)"`', body)
  FOR tag IN tag_matches:
    # Split by comma: "required,email,min=3"
    rules_list = tag.split(",")
    FOR rule IN rules_list:
      IF "=" IN rule:
        rule_type, value = rule.split("=")
        rules.append({type: rule_type, value: value, library: "validator"})
      ELSE:
        rules.append({type: rule, library: "validator"})

  # Custom validation (if checks)
  IF "if " IN body AND "== \"\"" IN body:
    rules.append({type: "required", library: "custom"})

  IF "if " IN body AND "len(" IN body:
    rules.append({type: "length_check", library: "custom"})

  RETURN rules
```

---

## Java/Kotlin Analyzer

### Configuration

```yaml
java_kotlin_analyzer:
  file_patterns: ["*.java", "*.kt"]
  exclude_patterns: ["*Test.java", "*Test.kt", "test/**"]
  frameworks:
    - spring
    - jaxrs
    - micronaut
  validation_libraries:
    - jsr303  # Bean Validation
    - hibernate-validator
```

### Public API Detection

```text
ANALYZE_JAVA_KOTLIN(scope_files):
  jvm_files = FILTER(scope_files, "*.java", "*.kt")
  jvm_files = EXCLUDE(jvm_files, "*Test.*", "test/**")

  apis = []

  FOR file IN jvm_files:
    symbols = find_symbol(
      name_path_pattern="*",
      relative_path=file,
      include_kinds=[6],  # Methods (Java/Kotlin classes analyzed separately)
      include_body=true
    )

    FOR symbol IN symbols:
      # Check visibility modifier
      IF "private" IN symbol.body:
        CONTINUE
      ELIF "protected" IN symbol.body:
        visibility = "protected"
      ELIF "public" IN symbol.body:
        visibility = "public"
      ELSE:
        visibility = "package-private"

      # Only track public
      IF visibility != "public":
        CONTINUE

      # Detect framework patterns
      api_type = DETECT_API_TYPE_JVM(symbol, file)

      # Extract annotations
      annotations = PARSE_ANNOTATIONS_JVM(symbol.body)

      # Check for @internal
      is_internal = "@internal" IN symbol.body OR "// @internal" IN symbol.body

      api = {
        type: api_type,
        language: "java" IF file.endswith(".java") ELSE "kotlin",
        file: file,
        line: symbol.line,
        name: symbol.name,
        signature: symbol.signature,
        visibility: visibility,
        annotations: annotations,
        is_internal: is_internal,
        body_sample: symbol.body[:200]
      }

      apis.append(api)

  RETURN apis
```

### Framework Pattern Detection

```text
DETECT_API_TYPE_JVM(symbol, file):
  body = symbol.body

  # Spring Boot annotations
  IF REGEX_MATCH(r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)", body):
    annotation = REGEX_EXTRACT(r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)", body)
    route = REGEX_EXTRACT(r'@\w+\(["\']([^"\']+)["\']?\)', body) OR ""

    method = annotation.replace("Mapping", "").upper()
    IF method == "REQUEST":
      method = "MULTI"  # RequestMapping can be any method

    RETURN {
      category: "REST_API",
      framework: "spring",
      method: method,
      endpoint: route
    }

  # JAX-RS annotations
  IF REGEX_MATCH(r"@(GET|POST|PUT|DELETE)", body) AND "@Path" IN body:
    method = REGEX_EXTRACT(r"@(GET|POST|PUT|DELETE)", body)
    route = REGEX_EXTRACT(r'@Path\(["\']([^"\']+)["\']?\)', body)
    RETURN {
      category: "REST_API",
      framework: "jaxrs",
      method: method,
      endpoint: route
    }

  # Micronaut annotations
  IF REGEX_MATCH(r"@(Get|Post|Put|Delete)", body) AND "io.micronaut" IN file:
    method = REGEX_EXTRACT(r"@(Get|Post|Put|Delete)", body)
    route = REGEX_EXTRACT(r'@\w+\(["\']([^"\']+)["\']?\)', body) OR ""
    RETURN {
      category: "REST_API",
      framework: "micronaut",
      method: method.upper(),
      endpoint: route
    }

  # Public method (no framework)
  RETURN {
    category: "UTILITY",
    framework: null,
    method_name: symbol.name
  }
```

### Annotation Extraction

```text
PARSE_ANNOTATIONS_JVM(code):
  annotations = {
    FR: [],
    AS: [],
    INTERNAL: false
  }

  # @speckit:FR:FR-xxx (in JavaDoc or comment)
  fr_matches = REGEX_FINDALL(r"@speckit:FR:(FR-\d+)", code)
  annotations.FR = fr_matches

  # @speckit:AS:AS-xxx
  as_matches = REGEX_FINDALL(r"@speckit:AS:(AS-\w+)", code)
  annotations.AS = as_matches

  # @internal or /* @internal */
  IF "@internal" IN code OR "// @internal" IN code OR "/* @internal */" IN code:
    annotations.INTERNAL = true

  RETURN annotations
```

### Validation Rule Detection

```text
DETECT_VALIDATION_JVM(symbol):
  body = symbol.body
  rules = []

  # JSR-303 / Bean Validation annotations
  validation_annotations = REGEX_FINDALL(r"@(NotNull|NotEmpty|Email|Size|Min|Max|Pattern)", body)
  FOR annotation IN validation_annotations:
    rules.append({type: annotation.lower(), library: "jsr303"})

  # Hibernate Validator annotations
  hibernate_annotations = REGEX_FINDALL(r"@(Length|Range|CreditCardNumber)", body)
  FOR annotation IN hibernate_annotations:
    rules.append({type: annotation.lower(), library: "hibernate-validator"})

  RETURN rules
```

---

## Cross-Language Utilities

### Extract Route from Next.js File Path

```text
EXTRACT_NEXTJS_ROUTE(file_path):
  # Examples:
  #   pages/api/users/[id].ts → /api/users/:id
  #   app/api/posts/route.ts → /api/posts

  route = file_path
  route = route.replace("pages/", "/")
  route = route.replace("app/", "/")
  route = route.replace("/route.ts", "")
  route = route.replace(".ts", "")
  route = route.replace(".tsx", "")

  # Convert [param] to :param
  route = REGEX_REPLACE(r"\[(\w+)\]", r":\1", route)

  RETURN route
```

### Infer Expected Location

```text
INFER_LOCATION(fr):
  description = fr.description.lower()

  # Keyword-based inference
  IF "authentication" IN description OR "login" IN description:
    RETURN "src/auth/"
  ELIF "user" IN description:
    RETURN "src/users/"
  ELIF "payment" IN description OR "checkout" IN description:
    RETURN "src/payments/"
  ELIF "email" IN description OR "notification" IN description:
    RETURN "src/notifications/"
  ELIF "api" IN description OR "endpoint" IN description:
    RETURN "src/api/"
  ELSE:
    RETURN "src/"  # Generic
```

---

## Usage Example (Pass AA)

```text
# In /speckit.analyze Pass AA

# Determine languages in project
languages = DETECT_LANGUAGES(PROJECT_ROOT)
# Returns: ["typescript", "python"]

drift_items = []

FOR lang IN languages:
  SWITCH lang:
    CASE "typescript":
      apis = ANALYZE_TYPESCRIPT(scope_files)
    CASE "python":
      apis = ANALYZE_PYTHON(scope_files)
    CASE "go":
      apis = ANALYZE_GO(scope_files)
    CASE "java":
      apis = ANALYZE_JAVA_KOTLIN(scope_files)
    CASE "kotlin":
      apis = ANALYZE_JAVA_KOTLIN(scope_files)

  # Detect drift for this language
  drift = DETECT_DRIFT(spec, apis)
  drift_items.extend(drift)

# Generate unified report
GENERATE_DRIFT_REPORT(drift_items)
```

---

## Performance Optimization

### Parallel Language Analysis

```text
# Launch parallel Task agents for each language
LAUNCH Task agent: typescript-analyzer
LAUNCH Task agent: python-analyzer
LAUNCH Task agent: go-analyzer
LAUNCH Task agent: java-analyzer

# Wait for all to complete
WAIT_ALL()

# Merge results
all_apis = typescript_apis + python_apis + go_apis + java_apis
```

### Caching Parsed Symbols

```yaml
# .drift-cache.yaml (gitignored)
caches:
  - file: "src/api/users.ts"
    checksum: "sha256:abc123..."
    last_parsed: "2026-01-11T10:30:00Z"
    symbols:
      - name: "createUser"
        line: 42
        type: "REST_API"
        # ... cached symbol data
```

```text
ANALYZE_WITH_CACHE(file):
  current_checksum = CALCULATE_CHECKSUM(file)
  cached_entry = LOAD_CACHE(file)

  IF cached_entry AND cached_entry.checksum == current_checksum:
    OUTPUT: "Cache hit: {file}"
    RETURN cached_entry.symbols
  ELSE:
    OUTPUT: "Cache miss: {file}"
    symbols = PARSE_FILE(file)
    SAVE_CACHE(file, symbols, current_checksum)
    RETURN symbols
```

---

## Error Handling

```text
TRY:
  symbols = find_symbol(...)
CATCH FileNotFoundError:
  OUTPUT: "Warning: File not found: {file}"
  SKIP
CATCH SyntaxError:
  OUTPUT: "Warning: Syntax error in {file}, skipping"
  SKIP
CATCH Exception as e:
  OUTPUT: "Error analyzing {file}: {e}"
  SKIP
```

---

## Testing Patterns

**Test Data**:
```typescript
// test-fixtures/typescript/sample-api.ts
// @speckit:FR:FR-001
export async function createUser(data: UserData) {
  // Implementation
}

export async function archiveUser(id: string) {
  // No annotation - should trigger drift
}
```

**Expected Output**:
```yaml
apis:
  - type: "REST_API"
    name: "createUser"
    annotations: {FR: ["FR-001"]}
    is_internal: false
  - type: "REST_API"
    name: "archiveUser"
    annotations: {FR: []}
    is_internal: false  # Triggers DRIFT-xxx
```
