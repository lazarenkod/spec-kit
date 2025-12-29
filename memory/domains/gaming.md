# Domain Extension: Gaming (Layer 1)

**Extends**: constitution.base.md v1.0
**Regulatory Context**: PEGI/ESRB/CERO ratings, COPPA (children), Loot box regulations (Belgium, Netherlands), Platform TOS (Sony TRC, Microsoft TCR, Nintendo Lotcheck)
**Typical Projects**: Mobile games, PC games, console games, multiplayer backends, game engines

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Game Loop** | Core update-render cycle (fixed timestep for physics, variable for rendering) |
| **Frame Rate** | Consistent 30/60/120 FPS targets based on platform and genre |
| **Input Latency** | Time from player input to visible response (critical for competitive games) |
| **State Synchronization** | Keeping game state consistent across clients in multiplayer |
| **Determinism** | Identical inputs produce identical outputs (required for replays, netcode) |
| **Monetization** | In-app purchases, battle passes, subscriptions, ads, loot boxes |
| **Anti-Cheat** | Mechanisms to detect and prevent unfair play in multiplayer |
| **Platform Certification** | Sony TRC, Microsoft TCR, Nintendo Lotcheck requirements |

---

## Strengthened Principles

These principles from `constitution.base.md` are elevated from SHOULD to MUST for games:

| Base ID | Original | New Level | Rationale |
|---------|----------|-----------|-----------|
| PERF-001 | SHOULD | MUST | Frame rate drops directly ruin gameplay experience |
| PERF-002 | SHOULD | MUST | Memory leaks cause crashes mid-session, losing progress |
| LOG-001 | SHOULD | MUST | Telemetry critical for balancing, debugging, and analytics |
| SEC-003 | SHOULD | MUST | Cheating destroys multiplayer experience and economy |

---

## Additional Principles

### GAM-001: Frame Rate Stability

**Level**: MUST
**Applies to**: All games

**Description**: Games must maintain their target frame rate (30/60/120 FPS) consistently without drops during active gameplay.

**Implementation**:
- Profile with platform tools (RenderDoc, PIX, Instruments)
- Implement dynamic quality scaling (resolution, effects)
- Use object pooling to avoid GC spikes
- Budget frame time: 16.67ms for 60fps, 33.33ms for 30fps

**Validation**: Frame time profiling across representative gameplay scenarios
**Violations**: HIGH - Unplayable feel, motion sickness, negative reviews

---

### GAM-002: Input Latency

**Level**: MUST
**Applies to**: All games

**Description**: Input-to-visual-response must be under 50ms for action games, under 100ms for casual games. Input handling must be predictable and consistent.

**Implementation**:
- Process input at start of frame, not end
- Minimize render pipeline latency
- Support high refresh rate displays (120Hz+)
- Implement input buffering for fighting/rhythm games

**Validation**: Measure with high-speed camera or specialized hardware
**Violations**: HIGH - Poor game feel, competitive disadvantage

---

### GAM-003: State Persistence

**Level**: MUST
**Applies to**: All games

**Description**: Player progress must be saved reliably. The game must handle interruptions (alt-tab, phone call, system suspend) without losing progress.

**Implementation**:
- Auto-save at meaningful checkpoints
- Save on app backgrounding/suspension
- Validate save data integrity (checksums)
- Support cloud save synchronization where available

**Validation**: Kill-app testing at various points; verify progress preserved
**Violations**: CRITICAL - Lost progress = angry players, refund requests

---

### GAM-004: Fair Monetization

**Level**: MUST
**Applies to**: All games with purchases

**Description**: Pricing must be clear and not deceptive. Monetization must comply with platform policies and regional regulations (loot box disclosure, COPPA).

**Implementation**:
- Show real currency prices, not just virtual currency
- Disclose drop rates for random items (gacha/loot boxes)
- No pay-to-win in competitive modes
- Implement parental controls and spending limits
- Comply with regional regulations (Belgium, Netherlands loot box bans)

**Validation**: Policy compliance review; age gate testing
**Violations**: CRITICAL - Platform removal, legal action, player backlash

---

### GAM-005: Age-Appropriate Content

**Level**: MUST
**Applies to**: All games

**Description**: Games must have accurate age ratings (ESRB, PEGI, CERO) and implement parental controls where required. COPPA compliance for games targeting children.

**Implementation**:
- Submit accurate rating questionnaires
- Implement age gates for mature content
- COPPA: no personal data collection from under-13 without parental consent
- Filter/disable chat and UGC for younger audiences

**Validation**: Rating board guidelines; COPPA compliance audit
**Violations**: CRITICAL - Legal liability, platform removal

---

### GAM-006: Multiplayer Integrity

**Level**: MUST
**Applies to**: Multiplayer games

**Description**: Multiplayer games must implement anti-cheat measures and use server-authoritative architecture to prevent cheating.

**Implementation**:
- Server validates all game state; never trust client
- Implement anti-cheat (EasyAntiCheat, BattlEye, or custom)
- Detect and ban speed hacks, aimbots, wallhacks
- Rate-limit actions; detect impossible inputs
- Maintain ban lists; support appeals

**Validation**: Penetration testing; cheat detection rate monitoring
**Violations**: CRITICAL - Economy destruction, player exodus

---

### GAM-007: Network Resilience

**Level**: MUST
**Applies to**: Online games

**Description**: Games must handle network disconnections gracefully and allow reconnection without losing progress or match state.

**Implementation**:
- Implement reconnection within timeout window
- Buffer inputs during brief disconnects
- Show clear connection status indicators
- Support varied network conditions (WiFi, cellular, high latency)
- Use reliable UDP (RUDP) or similar for game state

**Validation**: Network condition simulation testing (packet loss, latency spikes)
**Violations**: HIGH - Lost matches, frustration, churn

---

### GAM-008: Asset Loading

**Level**: SHOULD
**Applies to**: All games

**Description**: Asset loading should be asynchronous and show progress indication. Cold start and level transitions should not freeze the application.

**Implementation**:
- Stream assets asynchronously; prioritize visible content
- Show loading progress or engaging loading screens
- Use asset bundles for on-demand download
- Preload anticipated assets during idle time

**Validation**: Cold start profiling; no ANR/freeze during loads
**Violations**: MEDIUM - Poor first impression, store rating impact

---

### GAM-009: Platform Certification

**Level**: MUST
**Applies to**: Console games (PlayStation, Xbox, Nintendo Switch)

**Description**: Games must meet platform Technical Requirement Checklists (TRC/TCR/Lotcheck) including suspend/resume, achievements, and controller requirements.

**Implementation**:
- Handle system suspend/resume correctly
- Support all required controller configurations
- Implement platform-specific features (achievements/trophies)
- Handle network sign-out gracefully
- Meet memory and performance budgets

**Validation**: Pre-certification testing against full TRC/TCR/Lotcheck
**Violations**: CRITICAL - Certification failure, delayed release

---

## Game Type Considerations

### Real-Time Multiplayer (FPS, Fighting, Racing)

| Concern | Requirement |
|---------|-------------|
| Tick Rate | 30-128 ticks/second depending on genre |
| Netcode | Rollback or delay-based with lag compensation |
| Matchmaking | Skill-based (ELO/Glicko) with latency consideration |
| Anti-Cheat | Kernel-level or server-side detection required |

### Turn-Based / Casual

| Concern | Requirement |
|---------|-------------|
| Async Multiplayer | Support play-by-mail style matches |
| Session Length | Save state for short mobile sessions |
| Notifications | Push notifications for opponent turns |

### Live Service Games

| Concern | Requirement |
|---------|-------------|
| Hot Updates | Content updates without full app update |
| Server Downtime | Graceful maintenance mode with ETA |
| Economy | Balanced virtual economy, no hyperinflation |
| Events | Time-limited events with clear end dates |

---

## Performance Thresholds

| Metric | Mobile | PC | Console |
|--------|--------|-----|---------|
| Target FPS | 60 | 60-144 | 30/60 |
| Input Latency | < 80ms | < 50ms | < 50ms |
| Load Time | < 5s | < 10s | < 15s |
| Memory Budget | < 2GB | < 8GB | Platform-specific |
| Draw Calls | < 200 | < 3000 | < 2000 |

---

## Summary

| Type | Count |
|------|-------|
| Strengthened from base | 4 |
| New MUST principles | 7 |
| New SHOULD principles | 2 |
| **Total additional requirements** | **13** |

---

## When to Use

Apply this domain extension when building:
- Mobile games (iOS, Android)
- PC games (Steam, Epic, direct distribution)
- Console games (PlayStation, Xbox, Nintendo Switch)
- Multiplayer backends and game servers
- Game engines and middleware

## Combining with Other Domains

| Combined With | Notes |
|---------------|-------|
| **Mobile** | Mobile games: combine GAM + MOB for battery, offline, store compliance |
| **SaaS** | Game backends: add SAS multi-tenancy if serving multiple game clients |
| **E-Commerce** | In-game stores: add ECM payment and checkout principles |
| **UX Quality** | Premium games: add UXQ polish and delight principles |
| **FinTech** | Real-money gaming: add FIN compliance for gambling regulations |

---

## Usage

```bash
cp memory/domains/gaming.md memory/constitution.domain.md
```

Then customize the `constitution.domain.md` for your specific game project, adjusting principles based on game type (mobile vs console, single-player vs multiplayer).
