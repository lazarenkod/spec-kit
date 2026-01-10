---
description: Cross-platform mobile architecture patterns and decision frameworks
---

## User Input
$ARGUMENTS

## Purpose

Provides architectural guidance for mobile applications regardless of framework. Covers layer separation, dependency injection, offline-first patterns, navigation architecture, and platform selection decisions.

## When to Use

- During `/speckit.plan` for any mobile platform
- When making architectural decisions for new mobile features
- When evaluating cross-platform vs native approaches
- When designing offline-first or sync-heavy features

## Execution Steps

### 1. Platform Selection Framework

```text
DECISION MATRIX:

| Factor              | KMP      | Flutter  | React Native | Native    |
|---------------------|----------|----------|--------------|-----------|
| Team has Kotlin     | ✅ Best  | ⚠️ Learn | ⚠️ Different | ✅ Android|
| Team has Swift      | ✅ iOS OK| ⚠️ Learn | ⚠️ Different | ✅ iOS    |
| Team has JS/TS      | ⚠️ Learn | ⚠️ Learn | ✅ Best      | ❌ No     |
| Performance critical| ✅ Native| ⚠️ Good  | ⚠️ Good      | ✅ Best   |
| Complex animations  | ⚠️ Manual| ✅ Best  | ⚠️ Bridge    | ✅ Full   |
| Code sharing goal   | 70-90%   | 95%      | 90%          | 0%        |
| Native API access   | ✅ Full  | ⚠️ Plugin| ⚠️ Bridge    | ✅ Full   |
| Hot reload          | ⚠️ Partial| ✅ Best | ✅ Good      | ⚠️ SwiftUI|
| Hiring pool         | ⚠️ Small | ⚠️ Growing| ✅ Large    | ✅ Large  |

RECOMMENDATIONS:
- Fintech/Healthcare → KMP or Native (security, performance)
- Consumer social → Flutter or React Native (fast iteration)
- Enterprise → KMP (existing backend Kotlin, strict typing)
- Startup MVP → Flutter or React Native (speed to market)
- Games/3D → Native with Unity/Unreal
```

### 2. Layer Architecture

```text
CLEAN ARCHITECTURE FOR MOBILE:

┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  SwiftUI View   │  │  Compose Screen │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
│           │                    │                             │
│  ┌────────▼────────────────────▼────────┐                   │
│  │           ViewModel / BLoC            │                   │
│  │  (UI State, Actions, Side Effects)    │                   │
│  └────────────────┬─────────────────────┘                   │
├───────────────────┼─────────────────────────────────────────┤
│                   │      DOMAIN LAYER                        │
│  ┌────────────────▼─────────────────────┐                   │
│  │            Use Cases                  │                   │
│  │  (Business rules, orchestration)      │                   │
│  └────────────────┬─────────────────────┘                   │
│                   │                                          │
│  ┌────────────────▼─────────────────────┐                   │
│  │           Entities                    │                   │
│  │  (Core business objects)              │                   │
│  └──────────────────────────────────────┘                   │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                                │
│  ┌──────────────────────────────────────┐                   │
│  │           Repository                  │                   │
│  │  (Data coordination, caching)         │                   │
│  └─────────┬────────────────┬───────────┘                   │
│            │                │                                │
│  ┌─────────▼──────┐ ┌───────▼────────┐                      │
│  │  Remote Source │ │  Local Source  │                      │
│  │  (API client)  │ │  (Database)    │                      │
│  └────────────────┘ └────────────────┘                      │
└─────────────────────────────────────────────────────────────┘

RULES:
1. Dependencies point INWARD (Presentation → Domain → Data)
2. Domain layer has NO framework dependencies
3. Repository abstracts data source selection
4. ViewModels contain UI logic, not business logic
5. Use Cases contain business logic, not UI logic
```

### 3. Dependency Injection

```text
DI RECOMMENDATIONS BY PLATFORM:

| Platform       | Recommended DI    | Alternative       |
|----------------|-------------------|-------------------|
| KMP            | Koin              | Kodein            |
| Flutter        | GetIt + Injectable| Riverpod          |
| React Native   | InversifyJS       | Custom context    |
| Native iOS     | Factory/Swinject  | Manual DI         |
| Native Android | Hilt (Dagger)     | Koin              |

PRINCIPLES:
1. Constructor injection preferred over field injection
2. Singletons for stateless services (API client, analytics)
3. Factory for stateful objects (ViewModels)
4. Lazy initialization for expensive objects
5. Scope to lifecycle (app, feature, screen)

EXAMPLE STRUCTURE:
AppScope/
├── NetworkModule (Singleton)
│   ├── HttpClient
│   ├── ApiService
│   └── AuthInterceptor
├── StorageModule (Singleton)
│   ├── Database
│   ├── KeyValueStore
│   └── SecureStorage
└── FeatureModules (Factory)
    ├── LibraryModule
    │   ├── BookRepository
    │   └── LibraryViewModel
    └── ReaderModule
        ├── ReaderRepository
        └── ReaderViewModel
```

### 4. Offline-First Architecture

```text
OFFLINE-FIRST PATTERN:

┌────────────────────────────────────────────────────────────┐
│                    READ PATH                                │
│                                                             │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│  │    UI     │───▶│Repository │───▶│  Local    │          │
│  │           │◀───│           │◀───│  Cache    │          │
│  └───────────┘    └─────┬─────┘    └───────────┘          │
│                         │                                   │
│                         │ Background                        │
│                         ▼                                   │
│                   ┌───────────┐    ┌───────────┐          │
│                   │  Remote   │───▶│  Local    │          │
│                   │   API     │    │  Update   │          │
│                   └───────────┘    └───────────┘          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                    WRITE PATH                               │
│                                                             │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│  │    UI     │───▶│Repository │───▶│  Local    │          │
│  │  Action   │    │           │    │  Write    │          │
│  └───────────┘    └─────┬─────┘    └───────────┘          │
│                         │                                   │
│                         │ Enqueue                           │
│                         ▼                                   │
│                   ┌───────────┐    ┌───────────┐          │
│                   │   Sync    │───▶│  Remote   │          │
│                   │   Queue   │    │   API     │          │
│                   └───────────┘    └───────────┘          │
└────────────────────────────────────────────────────────────┘

IMPLEMENTATION STRATEGIES:

1. CACHE-FIRST (Read-heavy):
   - Read from cache immediately
   - Fetch from network in background
   - Update cache on response
   - Good for: feeds, catalogs, settings

2. NETWORK-FIRST (Fresh-data critical):
   - Try network first
   - Fall back to cache on error
   - Good for: payments, real-time data

3. STALE-WHILE-REVALIDATE:
   - Return cache immediately
   - Fetch fresh data in background
   - Update UI when fresh data arrives
   - Good for: profiles, dashboards

4. WRITE-THROUGH:
   - Write to cache and queue sync
   - Sync when online
   - Handle conflicts on sync
   - Good for: user content, forms
```

### 5. Navigation Patterns

```text
NAVIGATION ARCHITECTURE:

┌─────────────────────────────────────────────────────────────┐
│                    APP NAVIGATOR                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Root Stack                          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │  Auth   │  │  Main   │  │  Modal  │  │ Deeplink│  │  │
│  │  │  Flow   │  │  Tabs   │  │  Stack  │  │ Handler │  │  │
│  │  └─────────┘  └────┬────┘  └─────────┘  └─────────┘  │  │
│  └────────────────────┼─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │                  Tab Navigator                        │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │ Library │  │ Search  │  │ Profile │  │Settings │  │  │
│  │  │  Stack  │  │  Stack  │  │  Stack  │  │  Stack  │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

PATTERNS:

1. COORDINATOR PATTERN (iOS/KMP):
   - Separate navigation from ViewModels
   - Coordinators handle flow between screens
   - ViewModels emit navigation events

2. DEEP LINKING:
   - Universal links (iOS) / App Links (Android)
   - Single source of truth for URL → Screen mapping
   - Handle auth state before navigation

3. STATE RESTORATION:
   - Persist navigation state
   - Restore on app restart
   - Handle back stack correctly

DEEPLINK STRUCTURE:
  app://library                    → LibraryScreen
  app://library/{bookId}           → BookDetailScreen
  app://reader/{bookId}            → ReaderScreen
  app://reader/{bookId}/chapter/{n}→ ReaderScreen(chapter)
  app://settings                   → SettingsScreen
  app://settings/account           → AccountScreen
```

### 6. State Management Patterns

```text
STATE MANAGEMENT DECISION:

| Complexity    | Recommended                  | Examples           |
|---------------|------------------------------|--------------------|
| Simple screen | Local state (useState/State) | Form inputs        |
| Feature state | ViewModel/BLoC/Zustand       | List + CRUD        |
| Cross-feature | Global store (Redux/Koin)    | User session       |
| Server state  | React Query/TanStack         | API data           |

UNIDIRECTIONAL DATA FLOW:

    ┌────────────┐
    │   State    │──────────────┐
    └────────────┘              │
          ▲                     ▼
          │              ┌────────────┐
          │              │    View    │
          │              └────────────┘
          │                     │
    ┌─────┴──────┐              │
    │  Reducer   │◀─────────────┘
    │  (Update)  │        User Action
    └────────────┘

RULES:
1. State flows DOWN (parent → child)
2. Events flow UP (child → parent)
3. Single source of truth per domain
4. Immutable state updates
5. Side effects isolated (middleware/effects)
```

### 7. Security Architecture

```text
MOBILE SECURITY LAYERS:

1. TRANSPORT SECURITY
   - HTTPS only (certificate pinning for sensitive apps)
   - TLS 1.3 preferred
   - No sensitive data in URLs

2. DATA AT REST
   - Keychain (iOS) / Keystore (Android) for secrets
   - Encrypted database for sensitive user data
   - No secrets in code or assets

3. AUTHENTICATION
   - OAuth 2.0 / OIDC for login
   - Biometric for re-auth
   - Short-lived access tokens
   - Secure token refresh

4. CODE PROTECTION
   - Obfuscation (ProGuard/R8 for Android)
   - No debug logs in release
   - Root/jailbreak detection (if required)

SECURE STORAGE HIERARCHY:
┌─────────────────────────────────────────┐
│ Level 1: Keychain/Keystore              │ ← API keys, tokens
│   - Hardware-backed when available      │
│   - Biometric protection option         │
├─────────────────────────────────────────┤
│ Level 2: Encrypted SQLite/Realm         │ ← User data, PII
│   - SQLCipher, Encrypted Realm          │
│   - Key derived from Keychain           │
├─────────────────────────────────────────┤
│ Level 3: Standard Preferences           │ ← Non-sensitive settings
│   - UserDefaults, SharedPreferences     │
│   - Feature flags, UI preferences       │
└─────────────────────────────────────────┘
```

## Quality Checklist

- [ ] Clean layer separation verified (no cross-layer imports)
- [ ] DI configured for all dependencies
- [ ] Repository pattern for all data access
- [ ] Offline-first strategy defined for user content
- [ ] Navigation structure documented
- [ ] Deep linking implemented and tested
- [ ] State management consistent across features
- [ ] Security requirements met (encryption, secure storage)

## Output

This skill produces:
- Architecture decision record (ADR)
- Layer structure documentation
- DI configuration guide
- Offline-first implementation plan
- Navigation flow diagram
- Security checklist

## Integration with Spec Kit

- **`/speckit.plan`**: Provides architecture recommendations
- **`/speckit.tasks`**: Generates architecture setup tasks
- **`/speckit.analyze`**: Validates architecture compliance
