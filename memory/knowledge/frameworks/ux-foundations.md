# UX Foundation Patterns

> Reference catalog for required UX foundations by project type.
> Used by `/speckit.concept` for automatic foundation detection and wave-based ordering.

## Project Type Detection

Detect project type from codebase indicators to determine required foundations.

| Indicator | Project Type | Required Foundations |
|-----------|--------------|---------------------|
| `package.json` with React/Vue/Angular/Svelte | Web SPA | AUTH, NAV, ERROR, FTUE, LAYOUT, ADMIN |
| `package.json` with Next.js/Nuxt/SvelteKit | Web SSR | AUTH, NAV, ERROR, FTUE, LAYOUT, ADMIN |
| `ios/` or `android/` directories | Mobile | AUTH, NAV, ERROR, FTUE, LAYOUT, OFFLINE, ADMIN |
| `--help` flag, `cli.py`, `argparse` | CLI Tool | ERROR, HELP, CONFIG |
| `openapi.yaml`, `api/`, swagger | API | AUTH, ERROR, RATE_LIMIT, ADMIN |
| `Dockerfile`, `docker-compose.yml` only | Service | AUTH, ERROR, HEALTH, ADMIN |
| Electron, Tauri indicators | Desktop | AUTH, NAV, ERROR, FTUE, LAYOUT, OFFLINE, ADMIN |

### Detection Priority

When multiple indicators match, use this priority:
1. Mobile (if `ios/` or `android/` present)
2. Web SSR (if SSR framework detected)
3. Web SPA (if SPA framework detected)
4. Desktop (if Electron/Tauri detected)
5. CLI Tool (if CLI indicators present)
6. API (if OpenAPI/swagger present)
7. Service (fallback for backend-only)

---

## Foundation Categories

### Wave 1: Core Infrastructure (Must implement first)

These foundations block ALL other features. Nothing is testable without them.

#### AUTH: Authentication & Authorization

Required for any system with user identity.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-AUTH-001 | User signs up | Given guest → When provides credentials → Then account created | All authenticated features |
| UXF-AUTH-002 | User signs in | Given registered user → When provides credentials → Then session created | All authenticated features |
| UXF-AUTH-003 | User signs out | Given authenticated → When clicks logout → Then session ended | Session management |
| UXF-AUTH-004 | Password reset | Given user forgot password → When requests reset → Then reset link sent | Account recovery |
| UXF-AUTH-005 | Session timeout | Given inactive session → When timeout reached → Then redirect to login | Session management |
| UXF-AUTH-006 | Permission denied | Given unauthorized user → When attempts protected action → Then shows error | Role-based access |

**Default Epic mapping**: EPIC-001 User Access
- F01: User Registration (UXF-AUTH-001)
- F02: Authentication (UXF-AUTH-002, UXF-AUTH-003)
- F03: Account Recovery (UXF-AUTH-004)
- F04: Session Management (UXF-AUTH-005, UXF-AUTH-006)

#### ERROR: Error Handling

Required for any system that can fail (all systems).

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-ERR-001 | Network failure | Given user action → When network unavailable → Then shows offline state | All network-dependent features |
| UXF-ERR-002 | Validation error | Given user input → When invalid data → Then shows field-level errors | All forms |
| UXF-ERR-003 | Server error (5xx) | Given system failure → When request fails → Then shows friendly error | All server interactions |
| UXF-ERR-004 | Not found (404) | Given invalid resource → When accessed → Then shows not found | All navigation |
| UXF-ERR-005 | Rate limited | Given excessive requests → When limit hit → Then shows retry message | All API consumers |

**Default mapping**: Cross-cutting concern, implemented in infrastructure layer.

#### LAYOUT: Core Layout & Shell

Required for any visual application.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-LAYOUT-001 | App shell renders | Given app start → When loaded → Then shows consistent layout | All UI features |
| UXF-LAYOUT-002 | Responsive breakpoints | Given any viewport → When resized → Then layout adapts | Mobile usage |
| UXF-LAYOUT-003 | Loading states | Given pending action → When waiting → Then shows loading indicator | Perceived performance |
| UXF-LAYOUT-004 | Skeleton screens | Given data loading → When content pending → Then shows placeholder | Perceived performance |

**Default mapping**: Infrastructure layer, design system.

---

### Wave 2: User Experience (Enable testable journeys)

These foundations make user journeys complete and testable.

#### NAV: Navigation & Routing

Required for multi-page/multi-screen applications.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-NAV-001 | Main navigation | Given any page → When clicks nav → Then navigates to section | Cross-feature navigation |
| UXF-NAV-002 | Breadcrumbs/back | Given nested page → When needs context → Then shows path | Deep navigation |
| UXF-NAV-003 | Deep linking | Given shared URL → When opened → Then shows specific state | Sharing, bookmarks |
| UXF-NAV-004 | Protected routes | Given unauthenticated → When accesses protected → Then redirects to login | AUTH integration |

**Default mapping**: Cross-cutting concern, routing layer.

#### FTUE: First-Time User Experience

Required for any product that needs user activation.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-FTUE-001 | Empty state | Given no data → When first views → Then shows guidance | User activation |
| UXF-FTUE-002 | Onboarding wizard | Given new user → When first login → Then shows setup steps | Feature discovery |
| UXF-FTUE-003 | First meaningful action | Given onboarded → When completes first action → Then shows success | User retention |
| UXF-FTUE-004 | Feature discovery | Given new feature → When available → Then shows tooltip/hint | Feature adoption |

**Default mapping**: EPIC for User Onboarding.

#### FEEDBACK: User Feedback & Confirmation

Required for any interactive application.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-FEED-001 | Success confirmation | Given action complete → When success → Then shows confirmation | All CRUD operations |
| UXF-FEED-002 | Destructive action confirmation | Given delete/irreversible → When initiated → Then shows warning | Data safety |
| UXF-FEED-003 | Progress indication | Given long operation → When in progress → Then shows progress | User patience |
| UXF-FEED-004 | Undo capability | Given reversible action → When completed → Then offers undo | Error recovery |

**Default mapping**: Cross-cutting concern, component library.

#### ADMIN: Administrative Interface

Required for any system that needs admin management capabilities.
**Trigger**: Automatically included when AUTH foundation is present.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-ADMIN-001 | Admin accesses dashboard | Given admin role → When navigates to /admin → Then shows admin dashboard | All admin features |
| UXF-ADMIN-002 | Admin lists users | Given admin dashboard → When views users → Then shows paginated user list | User management |
| UXF-ADMIN-003 | Admin edits user | Given user list → When edits user → Then updates user data | User management |
| UXF-ADMIN-004 | Admin changes user role | Given user details → When changes role → Then role updated | Role management |
| UXF-ADMIN-005 | Admin views audit log | Given admin dashboard → When views audit → Then shows action history | Audit trail |
| UXF-ADMIN-006 | Non-admin denied access | Given regular user → When accesses /admin → Then shows 403 | Security |

**Default Epic mapping**: EPIC for Admin Interface
- F01: Admin Dashboard (UXF-ADMIN-001, UXF-ADMIN-006)
- F02: User Management (UXF-ADMIN-002, UXF-ADMIN-003)
- F03: Role Management (UXF-ADMIN-004)
- F04: Audit Log (UXF-ADMIN-005)

#### INTEGRATION: Third-Party Integrations

Required for systems that connect with external services.

| ID | Scenario | Given-When-Then | Blocks |
|----|----------|-----------------|--------|
| UXF-INTEG-001 | Connect to external service | Given API credentials → When establishing connection → Then connection verified | All integration features |
| UXF-INTEG-002 | Handle API errors | Given API failure → When request fails → Then logs error and retries | Integration reliability |
| UXF-INTEG-003 | Rate limit handling | Given API rate limit → When limit reached → Then queues requests | Integration stability |
| UXF-INTEG-004 | Webhook handling | Given external event → When webhook received → Then processes event | Real-time integrations |
| UXF-INTEG-005 | OAuth flow | Given OAuth provider → When user authorizes → Then receives token | Secure integrations |
| UXF-INTEG-006 | Sync status | Given integration active → When syncing → Then shows sync progress | Integration transparency |

**Default mapping**: Infrastructure layer or EPIC for Integrations
**Wave assignment**: Wave 2 (enables business features)
**Auto-included when**: API keys, webhooks, or OAuth mentioned in requirements

---

### Wave 3+: Business Features

After Waves 1-2, business features can be built in priority order (P1a, P1b, P2, etc.).

---

## Specialized Foundations (by project type)

### OFFLINE: Offline Capability (Mobile, Desktop, PWA)

| ID | Scenario | Given-When-Then |
|----|----------|-----------------|
| UXF-OFF-001 | Offline indicator | Given no network → When detected → Then shows offline banner |
| UXF-OFF-002 | Queue operations | Given offline → When user acts → Then queues for sync |
| UXF-OFF-003 | Sync on reconnect | Given pending changes → When online → Then syncs automatically |
| UXF-OFF-004 | Conflict resolution | Given conflicting changes → When syncing → Then resolves/prompts |

### HELP: Help & Documentation (CLI)

| ID | Scenario | Given-When-Then |
|----|----------|-----------------|
| UXF-HELP-001 | Command help | Given any command → When --help → Then shows usage |
| UXF-HELP-002 | Error guidance | Given failed command → When error → Then suggests fix |
| UXF-HELP-003 | Interactive mode | Given complex input → When needed → Then prompts user |

### CONFIG: Configuration Management (CLI, Service)

| ID | Scenario | Given-When-Then |
|----|----------|-----------------|
| UXF-CFG-001 | Default config | Given fresh install → When run → Then uses sensible defaults |
| UXF-CFG-002 | Config file | Given config exists → When run → Then reads config |
| UXF-CFG-003 | Environment override | Given env vars → When run → Then env takes precedence |
| UXF-CFG-004 | Config validation | Given invalid config → When loading → Then shows validation errors |

### RATE_LIMIT: Rate Limiting (API)

| ID | Scenario | Given-When-Then |
|----|----------|-----------------|
| UXF-RATE-001 | Rate limit headers | Given any request → When responded → Then includes rate headers |
| UXF-RATE-002 | Limit exceeded | Given too many requests → When limit hit → Then returns 429 |
| UXF-RATE-003 | Retry guidance | Given rate limited → When 429 → Then includes retry-after |

### HEALTH: Health Checks (Service, API)

| ID | Scenario | Given-When-Then |
|----|----------|-----------------|
| UXF-HLTH-001 | Liveness probe | Given running service → When /health → Then returns 200 |
| UXF-HLTH-002 | Readiness probe | Given dependencies → When /ready → Then checks all deps |
| UXF-HLTH-003 | Dependency health | Given external service → When checking → Then reports status |

---

## Wave Assignment Rules

```text
WAVE_RULES = {
  "Wave 1": ["AUTH", "ERROR", "LAYOUT", "CONFIG", "HEALTH"],
  "Wave 2": ["NAV", "FTUE", "FEEDBACK", "HELP", "ADMIN", "INTEGRATION"],
  "Wave 3+": All business features
}

FOR EACH foundation in REQUIRED_FOUNDATIONS:
  IF foundation in WAVE_RULES["Wave 1"]:
    ASSIGN Wave = 1
    ASSIGN Priority = P1a (auto-elevate)
  ELSE IF foundation in WAVE_RULES["Wave 2"]:
    ASSIGN Wave = 2
    ASSIGN Priority = P1b (auto-elevate)
  ELSE:
    ASSIGN Wave = 3
    # Keep user-defined priority
```

---

## Foundation Pattern Detection

Patterns to detect if a feature IS a foundation (vs a business feature):

```text
FOUNDATION_PATTERNS = {
  "AUTH": ["auth*", "login*", "signin*", "signup*", "register*", "session*", "oauth*", "sso*"],
  "USER_MGMT": ["user*", "account*", "profile*", "permission*", "role*", "member*"],
  "ERROR": ["error*", "exception*", "fault*", "*handler", "fallback*"],
  "NAV": ["nav*", "route*", "router*", "breadcrumb*", "menu*", "sidebar*"],
  "LAYOUT": ["layout*", "shell*", "frame*", "container*", "wrapper*"],
  "FTUE": ["onboard*", "welcome*", "wizard*", "setup*", "intro*", "tour*"],
  "FEEDBACK": ["toast*", "notification*", "alert*", "confirm*", "modal*", "dialog*"],
  "CONFIG": ["config*", "setting*", "preference*", "option*"],
  "OFFLINE": ["offline*", "sync*", "cache*", "queue*"],
  "HEALTH": ["health*", "status*", "ping*", "ready*", "live*"],
  "ADMIN": ["admin*", "dashboard*", "backoffice*", "management*", "panel*", "console*"],
  "INTEGRATION": ["integrat*", "webhook*", "api*client*", "connector*", "sync*", "oauth*", "provider*"]
}

# Usage in /speckit.concept step 8b
FOR EACH feature in Feature Hierarchy:
  feature_name_lower = lowercase(feature.name)
  FOR EACH (foundation_type, patterns) in FOUNDATION_PATTERNS:
    FOR EACH pattern in patterns:
      IF feature_name_lower MATCHES pattern:
        MARK feature.is_foundation = true
        MARK feature.foundation_type = foundation_type
        SET feature.wave = WAVE_RULES[foundation_type]
        IF feature.wave == 1:
          SET feature.priority = "P1a"
        BREAK
```

---

## Golden Path Definition

A **Golden Path** is the minimum viable user journey that exercises all Wave 1-2 foundations.

### Template Golden Path (Web SPA)

```text
Journey: J000 Golden Path - New User Activation

1. [Guest] → Lands on home page [LAYOUT]
2. [Guest] → Clicks "Sign Up" [NAV]
3. [Guest] → Fills registration form [AUTH: signup]
4. [Guest] → Submits with invalid data [ERROR: validation]
5. [Guest] → Corrects and submits [AUTH: signup]
6. [User] → Sees onboarding wizard [FTUE: wizard]
7. [User] → Completes first action [FTUE: first action]
8. [User] → Sees success confirmation [FEEDBACK: success]
9. [User] → Navigates to main feature [NAV]
10. [User] → Logs out [AUTH: signout]

STATUS: Golden Path testable when ALL steps have implementing features.
```

---

## Integration with /speckit.concept

1. **Project Type Detection** (Step 2b): Use indicators table above
2. **UX Foundation Extraction** (Step 5b): Generate Epic/Feature/Story from scenarios
3. **Scenario Completeness Check** (Step 7b): Validate using Given-When-Then
4. **Foundation Layer Detection** (Step 8b): Use FOUNDATION_PATTERNS
5. **Golden Path Generation**: Create J000 from required foundations

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-27 | Initial catalog with Wave-based ordering |
| 1.1 | 2025-12-27 | Added ADMIN foundation (Wave 2) for projects with AUTH |
| 1.2 | 2026-01-13 | Added INTEGRATION foundation (Wave 2) for third-party services |
