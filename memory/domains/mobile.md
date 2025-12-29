# Domain Extension: Mobile Applications (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: App Store Guidelines (Apple), Play Store Policies (Google), GDPR, COPPA
**Typical Projects**: iOS apps, Android apps, React Native, Flutter, cross-platform mobile

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Platform Guidelines** | Apple Human Interface Guidelines (HIG) / Material Design 3 / store requirements |
| **Offline-First** | Apps must provide core functionality without network connection |
| **Battery Efficiency** | Minimize CPU, GPU, network, and location resource consumption |
| **Deep Linking** | Universal Links (iOS) / App Links (Android) for web-to-app navigation |
| **Push Notifications** | APNs (Apple) / FCM (Google) for async user engagement |
| **App Lifecycle** | Background/foreground state management, app suspension handling |
| **Secure Enclave** | Keychain (iOS) / Keystore (Android) for credential storage |

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated from SHOULD to MUST for mobile applications:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| PERF-001 | SHOULD | MUST | Mobile users expect instant response (<100ms touch feedback) |
| SEC-002 | SHOULD | MUST | Device-based credential storage requires secure enclave usage |
| ERR-001 | SHOULD | MUST | Graceful degradation critical for offline/poor connectivity scenarios |
| API-003 | SHOULD | MUST | Rate limiting essential for battery and cellular data preservation |

---

## Additional Principles

### MOB-001: Offline Capability

**Level**: MUST
**Applies to**: All mobile applications

**Description**: Core features must function without network connectivity. Actions taken offline must be queued and synchronized when connectivity is restored.

**Implementation**:
- Implement local data caching with SQLite, Realm, or Core Data
- Queue mutations for background sync (e.g., WorkManager, BGTaskScheduler)
- Show clear offline state indicators
- Handle sync conflicts with last-write-wins or user resolution

**Validation**: Test all user flows in airplane mode
**Violations**: HIGH - App unusable without network = store rejection risk

---

### MOB-002: Platform Compliance

**Level**: MUST
**Applies to**: All mobile applications

**Description**: Applications must follow platform-specific design guidelines (Apple HIG, Material Design) and comply with store review guidelines.

**Implementation**:
- Use native UI components or high-fidelity equivalents
- Follow platform navigation patterns (back button, swipe gestures)
- Implement required privacy disclosures (ATT, permissions)
- Avoid private APIs and store policy violations

**Validation**: Pre-submission checklist against store guidelines
**Violations**: CRITICAL - Store rejection or removal

---

### MOB-003: Battery Efficiency

**Level**: MUST
**Applies to**: All mobile applications

**Description**: Applications must minimize battery drain through efficient use of CPU, GPU, network, and location services.

**Implementation**:
- Batch network requests; avoid polling (use push/WebSocket)
- Minimize background processing; use efficient scheduling
- Reduce location accuracy when high precision not needed
- Profile with Xcode Instruments / Android Profiler

**Validation**: Battery profiling shows < 5% drain per hour of active use
**Violations**: MEDIUM - Poor app store ratings, user uninstalls

---

### MOB-004: Responsive Touch

**Level**: MUST
**Applies to**: All mobile applications

**Description**: Touch interactions must provide immediate visual feedback (<100ms) and maintain 60fps during animations.

**Implementation**:
- Highlight/ripple effect on touch-down, not touch-up
- Avoid main thread blocking during UI interactions
- Use hardware-accelerated animations
- Debounce rapid taps; prevent double-submission

**Validation**: Measure touch-to-render latency with profiling tools
**Violations**: MEDIUM - Perceived sluggishness, poor user experience

---

### MOB-005: Secure Storage

**Level**: MUST
**Applies to**: All mobile applications handling credentials or sensitive data

**Description**: Sensitive data must be stored using platform secure storage (Keychain/Keystore). Local databases containing user data must be encrypted.

**Implementation**:
- Store tokens, passwords, keys in Keychain (iOS) / Keystore (Android)
- Enable file-level encryption or use encrypted database (SQLCipher)
- Never log sensitive data; use redaction
- Implement biometric authentication for sensitive operations

**Validation**: Security audit; no plaintext secrets in storage
**Violations**: CRITICAL - Data breach, compliance failure

---

### MOB-006: Deep Linking

**Level**: SHOULD
**Applies to**: Applications with web presence or app-to-app navigation

**Description**: Support Universal Links (iOS) and App Links (Android) for seamless web-to-app and app-to-app navigation.

**Implementation**:
- Configure apple-app-site-association / assetlinks.json
- Handle all link parameters gracefully (missing, malformed)
- Preserve deep link across app install (deferred deep linking)
- Test links from email, SMS, web, and other apps

**Validation**: All defined routes open correct screens with correct data
**Violations**: LOW - Reduced engagement, poor marketing attribution

---

### MOB-007: Accessibility

**Level**: MUST
**Applies to**: All mobile applications

**Description**: Applications must be fully usable with screen readers (VoiceOver/TalkBack) and support dynamic type / text scaling.

**Implementation**:
- Add accessibility labels to all interactive elements
- Support Dynamic Type (iOS) / font scaling (Android)
- Ensure minimum 44pt touch targets
- Test with screen reader enabled
- Support reduce motion preference

**Validation**: Complete user flows with VoiceOver/TalkBack enabled
**Violations**: HIGH - Excludes users with disabilities, legal risk

---

### MOB-008: Graceful Updates

**Level**: SHOULD
**Applies to**: Applications with breaking API changes or critical security updates

**Description**: Support forced update mechanism for critical versions and handle API version skew gracefully.

**Implementation**:
- Check minimum supported version on app launch
- Show blocking update screen for critical updates
- Handle deprecated API responses without crashing
- Provide clear update messaging with store link

**Validation**: Test update flow from N-2 version
**Violations**: LOW - Users stuck on broken versions

---

## Platform-Specific Considerations

### iOS-Specific

| Concern | Requirement |
|---------|-------------|
| App Transport Security | HTTPS required for all network calls |
| Privacy Manifest | Declare API usage reasons (iOS 17+) |
| App Tracking Transparency | Prompt before IDFA access |
| Background Modes | Declare only modes actually used |
| Notarization | Required for macOS Catalyst apps |

### Android-Specific

| Concern | Requirement |
|---------|-------------|
| Target SDK | Must target recent API level per Play Store policy |
| Permissions | Request at point of use, not on launch |
| Doze/App Standby | Handle battery optimization restrictions |
| Scoped Storage | Use SAF for external file access (Android 10+) |
| Foreground Services | Declare type and show notification |

---

## Performance Thresholds

| Metric | Target | Lovable |
|--------|--------|---------|
| Cold Start | < 2s | < 1s |
| Warm Start | < 500ms | < 200ms |
| Touch Response | < 100ms | < 50ms |
| Frame Rate | 60 fps | 120 fps (ProMotion) |
| App Size (iOS) | < 200MB | < 50MB |
| App Size (Android) | < 150MB | < 30MB |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 4 |
| New MUST principles | 6 |
| New SHOULD principles | 2 |
| **Total additional requirements** | **12** |

---

## When to Use

Apply this domain extension when building:
- Native iOS applications (Swift, Objective-C)
- Native Android applications (Kotlin, Java)
- Cross-platform apps (React Native, Flutter, Xamarin)
- Progressive Web Apps targeting mobile installation

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **SaaS** | Multi-tenant mobile apps: combine MOB + SAS principles |
| **E-Commerce** | Shopping apps: add ECM checkout/payment principles |
| **Healthcare** | Health apps: add HIP compliance (HIPAA, HealthKit) |
| **FinTech** | Banking apps: add FIN security and audit requirements |
| **Gaming** | Mobile games: add GAM performance and monetization principles |
| **UX Quality** | Consumer apps: add UXQ delight and polish principles |

---

## Usage

```bash
cp memory/domains/mobile.md memory/constitution.domain.md
```

Then customize the `constitution.domain.md` for your specific mobile project, adjusting principles as needed while respecting the MUST/SHOULD hierarchy.
