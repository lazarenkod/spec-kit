# Contract Testing Strategy

## Purpose

Replace slow E2E tests with fast contract verification where appropriate, reducing test execution time by 80-90% while maintaining confidence in API compatibility and integration correctness.

## Performance Impact

| Test Type | Time | Coverage | When to Use |
|-----------|------|----------|-------------|
| Full E2E | 30-60s per flow | Complete | Major releases, nightly |
| Contract tests | 2-5s | API contracts | Every deploy |
| Unit + Contract | 3-8s | Logic + API | Default for CI |

## Configuration

```yaml
optimization:
  verify:
    contract_testing:
      enabled: true
      skip_flag: "--full-e2e"
      provider: pact              # pact | openapi | custom
      contracts_dir: "contracts/"
      verify_on_deploy: true
      e2e_triggers:
        - first_deploy_to_env
        - major_version_change
        - explicit_flag
        - nightly_schedule
```

## Contract vs E2E Decision Matrix

```text
DECISION_MATRIX:

  USE_CONTRACT_TESTS:
    - API schema validation
    - Request/response format verification
    - Error response formats
    - Pagination contracts
    - Authentication token formats
    - Rate limiting headers
    - CORS configuration

  USE_E2E_TESTS:
    - Complete user journeys
    - Multi-service transactions
    - Browser-specific behavior
    - Visual regression
    - Performance under load
    - Security penetration
    - Third-party integrations

  HYBRID (Contract + Targeted E2E):
    - Payment flows (contract for API, E2E for actual payment)
    - User registration (contract for API, E2E for email verification)
    - File uploads (contract for API, E2E for actual file processing)


FUNCTION decide_test_strategy(test_scenario):
  # Check explicit markers
  IF "[E2E-REQUIRED]" IN test_scenario.markers:
    RETURN "e2e"

  IF "[CONTRACT-ONLY]" IN test_scenario.markers:
    RETURN "contract"

  # Auto-detect based on scenario characteristics
  IF test_scenario.involves_browser:
    RETURN "e2e"

  IF test_scenario.involves_external_service:
    RETURN "hybrid"

  IF test_scenario.is_api_only:
    RETURN "contract"

  # Default to contract for speed
  RETURN "contract"
```

## Pact Contract Testing

```text
PACT_CONFIG:
  broker_url: "${PACT_BROKER_URL}"
  publish_verification: true
  provider_version: "${GIT_SHA}"
  consumer_version_selectors:
    - { mainBranch: true }
    - { deployedOrReleased: true }


FUNCTION setup_pact_contracts():
  contracts_dir = "contracts/"
  mkdir -p $contracts_dir

  # Structure
  # contracts/
  # ├── consumer-provider.pact.json
  # ├── frontend-api.pact.json
  # ├── api-payment.pact.json
  # └── api-notification.pact.json

  RETURN contracts_dir


FUNCTION generate_consumer_contract(consumer, provider, interactions):
  contract = {
    consumer: {name: consumer},
    provider: {name: provider},
    interactions: [],
    metadata: {
      pactSpecification: {version: "4.0"}
    }
  }

  FOR interaction IN interactions:
    contract.interactions.append({
      description: interaction.description,
      providerState: interaction.provider_state,
      request: {
        method: interaction.request.method,
        path: interaction.request.path,
        headers: interaction.request.headers,
        body: interaction.request.body,
        matchingRules: generate_matching_rules(interaction.request)
      },
      response: {
        status: interaction.response.status,
        headers: interaction.response.headers,
        body: interaction.response.body,
        matchingRules: generate_matching_rules(interaction.response)
      }
    })

  RETURN contract


FUNCTION verify_provider_contract(provider_name, contracts_dir):
  LOG f"Verifying contracts for provider: {provider_name}"

  # Find all contracts where this service is the provider
  contracts = glob(f"{contracts_dir}/*-{provider_name}.pact.json")

  results = []
  FOR contract_file IN contracts:
    contract = json.load(contract_file)
    consumer_name = contract.consumer.name

    LOG f"  Verifying against consumer: {consumer_name}"

    # Start provider (or use running instance)
    provider_url = get_provider_url(provider_name)

    # Verify each interaction
    FOR interaction IN contract.interactions:
      result = verify_interaction(provider_url, interaction)
      results.append(result)

      IF result.passed:
        LOG f"    ✓ {interaction.description}"
      ELSE:
        LOG f"    ✗ {interaction.description}: {result.error}"

  passed = all(r.passed FOR r IN results)
  RETURN ContractResult(passed=passed, results=results)


FUNCTION verify_interaction(provider_url, interaction):
  # Set up provider state
  IF interaction.providerState:
    setup_provider_state(provider_url, interaction.providerState)

  # Make request
  response = http_request(
    method=interaction.request.method,
    url=f"{provider_url}{interaction.request.path}",
    headers=interaction.request.headers,
    body=interaction.request.body
  )

  # Verify response
  expected = interaction.response

  # Status check
  IF response.status != expected.status:
    RETURN VerifyResult(passed=False, error=f"Status mismatch: {response.status} != {expected.status}")

  # Body matching
  IF NOT matches_with_rules(response.body, expected.body, expected.matchingRules):
    RETURN VerifyResult(passed=False, error="Body mismatch")

  RETURN VerifyResult(passed=True)
```

## OpenAPI Contract Testing

```text
OPENAPI_CONFIG:
  spec_path: "api/openapi.yaml"
  validate_requests: true
  validate_responses: true
  strict_mode: false          # Allow additional properties


FUNCTION verify_openapi_contract(spec_path, api_url):
  LOG f"Verifying OpenAPI contract: {spec_path}"

  spec = load_openapi_spec(spec_path)

  results = []

  FOR path, methods IN spec.paths:
    FOR method, operation IN methods:
      # Generate test request from spec
      test_request = generate_request_from_spec(path, method, operation)

      # Execute request
      response = execute_request(api_url, test_request)

      # Validate response against spec
      validation = validate_response(response, operation.responses, spec)

      result = {
        endpoint: f"{method.upper()} {path}",
        passed: validation.valid,
        errors: validation.errors
      }
      results.append(result)

      IF validation.valid:
        LOG f"  ✓ {method.upper()} {path}"
      ELSE:
        LOG f"  ✗ {method.upper()} {path}: {validation.errors}"

  passed = all(r["passed"] FOR r IN results)
  RETURN OpenAPIResult(passed=passed, results=results)


FUNCTION generate_request_from_spec(path, method, operation):
  request = {
    method: method.upper(),
    path: path,
    headers: {},
    query: {},
    body: None
  }

  # Generate path parameters
  FOR param IN operation.parameters:
    IF param.in == "path":
      value = generate_example_value(param.schema)
      request.path = request.path.replace(f"{{{param.name}}}", str(value))
    ELIF param.in == "query":
      IF param.required:
        request.query[param.name] = generate_example_value(param.schema)
    ELIF param.in == "header":
      IF param.required:
        request.headers[param.name] = generate_example_value(param.schema)

  # Generate request body
  IF operation.requestBody:
    content_type = list(operation.requestBody.content.keys())[0]
    schema = operation.requestBody.content[content_type].schema
    request.headers["Content-Type"] = content_type
    request.body = generate_example_from_schema(schema)

  RETURN request
```

## E2E Trigger Conditions

```text
E2E_TRIGGER_CONDITIONS:

  first_deploy_to_env:
    check: |
      deployed_version = get_deployed_version(environment)
      RETURN deployed_version IS None

  major_version_change:
    check: |
      current = parse_semver(new_version)
      deployed = parse_semver(get_deployed_version(environment))
      RETURN current.major != deployed.major

  schema_breaking_change:
    check: |
      diff = openapi_diff(old_spec, new_spec)
      RETURN diff.has_breaking_changes

  explicit_flag:
    check: |
      RETURN "--full-e2e" IN cli_flags

  nightly_schedule:
    check: |
      RETURN is_nightly_run()

  dependency_update:
    check: |
      changes = git_diff_files()
      RETURN any(f IN ["package-lock.json", "go.sum", "Cargo.lock"] FOR f IN changes)


FUNCTION should_run_full_e2e(environment, config):
  FOR trigger_name, trigger IN E2E_TRIGGER_CONDITIONS:
    IF trigger.check():
      LOG f"E2E triggered by: {trigger_name}"
      RETURN true

  LOG "No E2E triggers matched, using contract tests"
  RETURN false
```

## Contract Generation from Tests

```text
FUNCTION generate_contracts_from_e2e(e2e_test_file):
  # Parse E2E test to extract API interactions
  interactions = []

  test_content = read_file(e2e_test_file)
  api_calls = extract_api_calls(test_content)

  FOR call IN api_calls:
    interaction = {
      description: call.context,
      request: {
        method: call.method,
        path: call.path,
        headers: call.headers,
        body: call.body
      },
      response: {
        status: call.expected_status,
        body: call.expected_body
      }
    }
    interactions.append(interaction)

  # Group by provider
  grouped = group_by_provider(interactions)

  # Generate contracts
  FOR provider, provider_interactions IN grouped:
    contract = generate_consumer_contract(
      consumer="e2e-tests",
      provider=provider,
      interactions=provider_interactions
    )
    save_contract(contract, f"contracts/e2e-{provider}.pact.json")

  LOG f"Generated {len(grouped)} contracts from E2E tests"


FUNCTION extract_api_calls(test_content):
  # Pattern matching for common test frameworks
  patterns = [
    # Playwright
    r'page\.request\.(get|post|put|delete)\(["\']([^"\']+)["\']',
    # Cypress
    r'cy\.request\(\{.*method:\s*["\'](\w+)["\'].*url:\s*["\']([^"\']+)["\']',
    # Jest/SuperTest
    r'request\(app\)\.(get|post|put|delete)\(["\']([^"\']+)["\']',
  ]

  calls = []
  FOR pattern IN patterns:
    matches = regex.findall(pattern, test_content)
    FOR match IN matches:
      calls.append(parse_api_call(match))

  RETURN calls
```

## Hybrid Test Strategy

```text
HYBRID_STRATEGY:

  payment_flow:
    contract_tests:
      - verify_create_payment_request_format
      - verify_payment_response_schema
      - verify_webhook_payload_format
    e2e_tests:
      - complete_payment_with_test_card
      - verify_payment_appears_in_dashboard

  user_registration:
    contract_tests:
      - verify_registration_request_format
      - verify_registration_response_schema
      - verify_email_api_contract
    e2e_tests:
      - complete_registration_with_email_verification

  file_upload:
    contract_tests:
      - verify_upload_endpoint_accepts_multipart
      - verify_upload_response_includes_file_url
    e2e_tests:
      - upload_large_file_and_verify_processing


FUNCTION execute_hybrid_tests(scenario):
  results = []

  # Always run contract tests first (fast)
  contract_results = run_contract_tests(scenario.contract_tests)
  results.extend(contract_results)

  IF any(r.failed FOR r IN contract_results):
    LOG "Contract tests failed, skipping E2E"
    RETURN TestResults(results, skipped_e2e=True)

  # Run E2E only if contracts pass
  IF should_run_e2e(scenario):
    e2e_results = run_e2e_tests(scenario.e2e_tests)
    results.extend(e2e_results)

  RETURN TestResults(results)
```

## Contract Verification Pipeline

```text
FUNCTION contract_verification_pipeline(services, environment):
  LOG "📋 Contract Verification"

  all_results = []

  # 1. Verify all consumers have published contracts
  FOR service IN services:
    IF service.type == "consumer":
      contracts = find_contracts(consumer=service.name)
      IF NOT contracts:
        LOG f"⚠ Warning: No contracts published by {service.name}"

  # 2. Verify each provider against its contracts
  FOR service IN services:
    IF service.type == "provider":
      LOG f"\nVerifying provider: {service.name}"

      contracts = find_contracts(provider=service.name)
      FOR contract IN contracts:
        result = verify_provider_contract(service.name, contract)
        all_results.append(result)

        IF result.passed:
          LOG f"  ✓ Contract with {contract.consumer}: PASSED"
        ELSE:
          LOG f"  ✗ Contract with {contract.consumer}: FAILED"

  # 3. Summary
  passed = sum(1 FOR r IN all_results IF r.passed)
  failed = len(all_results) - passed

  RETURN ContractSummary(
    total=len(all_results),
    passed=passed,
    failed=failed,
    results=all_results
  )
```

## Integration with ship.md

```text
# At verify phase:
Read `templates/shared/ship/contract-testing.md` and apply.

# Replace full E2E with contract-first:
INSTEAD OF:
  run_all_e2e_tests()

USE:
  IF should_run_full_e2e(environment, config):
    run_all_e2e_tests()
  ELSE:
    contract_result = contract_verification_pipeline(services, environment)
    IF contract_result.passed:
      run_smoke_tests_only()  # Minimal E2E for sanity
```

## Output Format

```text
📋 Contract Verification
├── Strategy: Contract-first (no E2E triggers matched)
├── Contracts Found:
│   ├── frontend-api.pact.json (12 interactions)
│   ├── api-payment.pact.json (8 interactions)
│   └── api-notification.pact.json (5 interactions)
├── Provider Verification:
│   ├── api-server:
│   │   ├── ✓ frontend-api: 12/12 passed
│   │   └── Total: 12 interactions verified
│   ├── payment-service:
│   │   ├── ✓ api-payment: 8/8 passed
│   │   └── Total: 8 interactions verified
│   └── notification-service:
│       ├── ✓ api-notification: 5/5 passed
│       └── Total: 5 interactions verified
├── Smoke Tests: 3/3 passed (sanity check)
├── Timing:
│   ├── Contract verification: 4.2s
│   ├── Smoke tests: 8.1s
│   └── Total: 12.3s (vs ~120s full E2E)
└── Result: SUCCESS ✓
```

## CLI Flags

```bash
# Force full E2E
speckit ship --full-e2e

# Contract verification only (no E2E)
speckit ship --contracts-only

# Skip contract verification
speckit ship --skip-contracts

# Regenerate contracts from E2E
speckit ship --generate-contracts

# Publish contracts to broker
speckit ship --publish-contracts
```

## Contract Evolution

```text
FUNCTION handle_contract_evolution(old_contract, new_contract):
  diff = contract_diff(old_contract, new_contract)

  IF diff.is_backward_compatible:
    LOG "Contract change is backward compatible"
    RETURN ALLOW

  IF diff.is_breaking:
    LOG "⚠ Breaking contract change detected!"

    changes = []
    FOR change IN diff.breaking_changes:
      changes.append(f"  - {change.type}: {change.description}")

    LOG "\n".join(changes)

    # Options
    IF config.strict_contracts:
      RETURN DENY
    ELSE:
      LOG "Warning: Breaking change allowed (strict mode disabled)"
      RETURN ALLOW_WITH_WARNING

  RETURN ALLOW


FUNCTION contract_diff(old_contract, new_contract):
  diff = ContractDiff()

  # Check for removed interactions
  old_interactions = {i.description FOR i IN old_contract.interactions}
  new_interactions = {i.description FOR i IN new_contract.interactions}

  removed = old_interactions - new_interactions
  IF removed:
    diff.breaking_changes.append(
      BreakingChange(type="removed_interaction", items=removed)
    )

  # Check for changed request schemas
  FOR old_int IN old_contract.interactions:
    new_int = find_interaction(new_contract, old_int.description)
    IF new_int:
      request_diff = schema_diff(old_int.request, new_int.request)
      IF request_diff.is_breaking:
        diff.breaking_changes.append(
          BreakingChange(type="request_change", interaction=old_int.description)
        )

  RETURN diff
```
