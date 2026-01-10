---
description: Mobile performance optimization techniques and profiling strategies
---

## User Input
$ARGUMENTS

## Purpose

Provides performance optimization guidance for mobile applications. Covers startup optimization, rendering performance, memory management, battery efficiency, and platform-specific profiling tools.

## When to Use

- During `/speckit.implement` for performance-critical features
- During `/speckit.analyze` for performance validation
- When app performance metrics are below thresholds
- Before release to validate performance requirements

## Key Metrics

| Metric | Target | Critical | Measurement |
|--------|--------|----------|-------------|
| Cold start | < 2s | < 3s | Time from tap to interactive |
| Warm start | < 500ms | < 1s | Time from background to usable |
| Frame rate | 60 FPS | 30 FPS | During scroll/animation |
| Jank | 0 frames | < 5% | Dropped frames in sequence |
| Memory peak | < 150MB | < 250MB | Maximum heap usage |
| Memory leak | 0 | 0 | Objects not freed after screen exit |
| Battery | < 5%/hr | < 10%/hr | Active usage drain |
| Network | < 1MB | < 5MB | Initial data fetch |

## Execution Steps

### 1. Startup Optimization

```text
COLD START PHASES:

┌──────────────────────────────────────────────────────────────┐
│ Phase 1: Process Creation (OS)     │ ~100-300ms             │
│ - Fork process                     │ Cannot optimize        │
│ - Load runtime (ART/iOS runtime)   │                        │
├──────────────────────────────────────────────────────────────┤
│ Phase 2: App Initialization        │ ~200-500ms             │
│ - Load classes/modules             │ ⬅ Optimize: lazy load │
│ - Initialize dependencies          │ ⬅ Optimize: defer DI  │
│ - Set up crash reporting, analytics│ ⬅ Optimize: async init│
├──────────────────────────────────────────────────────────────┤
│ Phase 3: UI Creation               │ ~100-300ms             │
│ - Inflate layouts                  │ ⬅ Optimize: simpler UI│
│ - Create ViewModels                │ ⬅ Optimize: lazy data │
│ - Initial render                   │ ⬅ Optimize: skeleton  │
├──────────────────────────────────────────────────────────────┤
│ Phase 4: Data Loading              │ ~200-1000ms            │
│ - API calls                        │ ⬅ Optimize: cache     │
│ - Database queries                 │ ⬅ Optimize: prefetch  │
│ - Image loading                    │ ⬅ Optimize: lazy load │
└──────────────────────────────────────────────────────────────┘

OPTIMIZATION STRATEGIES:

1. LAZY MODULE LOADING:
   // KMP
   val heavyModule by lazy { HeavyModule() }

   // Flutter
   import 'package:heavy_feature/heavy.dart' deferred as heavy;
   await heavy.loadLibrary();

   // React Native
   const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

2. ASYNC INITIALIZATION:
   // Initialize non-critical services after first frame
   WidgetsBinding.instance.addPostFrameCallback((_) {
     initAnalytics();
     initCrashReporting();
     prefetchData();
   });

3. SPLASH SCREEN WITH CONTENT:
   - Show branded splash immediately
   - Render skeleton UI
   - Replace with real content when ready

4. CACHE FIRST LOAD:
   - Store last known state
   - Display cached data immediately
   - Refresh in background
```

### 2. Rendering Performance

```text
60 FPS REQUIREMENTS:
- Each frame: 16.67ms budget
- UI thread work: < 10ms
- GPU work: < 6ms

OPTIMIZATION CHECKLIST:

1. LIST VIRTUALIZATION:
   ✅ Use:
   - LazyColumn/LazyRow (Compose)
   - UICollectionView/UITableView (iOS)
   - FlatList/SectionList (React Native)
   - ListView.builder (Flutter)

   ❌ Avoid:
   - Column with many children
   - ScrollView with all items rendered

2. ITEM RECYCLING:
   // Compose
   LazyColumn {
       items(books, key = { it.id }) { book ->
           BookRow(book)
       }
   }

   // React Native
   <FlatList
       data={books}
       keyExtractor={(item) => item.id}
       getItemLayout={(data, index) => ({
           length: ITEM_HEIGHT,
           offset: ITEM_HEIGHT * index,
           index,
       })}
   />

3. MEMOIZATION:
   // React/RN
   const BookCard = React.memo(({ book }) => <View>...</View>);

   // Compose
   @Composable
   fun BookCard(book: Book) {
       val stableBook = remember(book.id) { book }
       // Use stableBook
   }

   // Flutter
   const BookCard({super.key, required this.book});

4. REDUCE OVERDRAW:
   - Avoid stacked opaque backgrounds
   - Use clipToBounds/clipChildren carefully
   - Debug with GPU overdraw visualization

5. IMAGE OPTIMIZATION:
   - Resize to display size
   - Use WebP format
   - Implement progressive loading
   - Cache aggressively
```

### 3. Memory Management

```text
MEMORY OPTIMIZATION:

1. IMAGE MEMORY:
   // Calculate memory: width * height * 4 bytes (RGBA)
   // 1080x1920 image = 8.3MB in memory

   SOLUTIONS:
   - Downscale to display size
   - Use RGB_565 (2 bytes) for non-transparent
   - Implement LRU cache with size limit
   - Release off-screen images

   // React Native
   <Image
       source={{ uri }}
       resizeMode="cover"
       style={{ width: 100, height: 100 }}
   />

   // Flutter
   Image.network(
       url,
       cacheWidth: 200,
       cacheHeight: 200,
   )

2. LEAK PREVENTION:
   Common leaks:
   - Retained listeners/observers
   - Closure capturing context
   - Static references to Activities/ViewControllers

   Prevention:
   - Use weak references for callbacks
   - Unsubscribe in onCleared/deinit
   - Avoid static context references

   // Kotlin
   class MyViewModel : ViewModel() {
       private val job = SupervisorJob()
       override fun onCleared() {
           job.cancel()
           super.onCleared()
       }
   }

   // Swift
   deinit {
       cancellables.forEach { $0.cancel() }
   }

3. MEMORY PROFILING:
   iOS: Instruments → Allocations, Leaks
   Android: Android Studio → Memory Profiler
   Flutter: DevTools → Memory tab
   React Native: Flipper → Memory plugin

4. OBJECT POOLING:
   - Reuse expensive objects
   - Pool RecyclerView.ViewHolders
   - Pool bitmap/canvas objects for drawing
```

### 4. Network Optimization

```text
NETWORK PERFORMANCE:

1. REQUEST COALESCING:
   // Instead of multiple requests:
   GET /books/1
   GET /books/2
   GET /books/3

   // Single batch request:
   POST /books/batch
   { "ids": [1, 2, 3] }

2. RESPONSE COMPRESSION:
   - Enable gzip/brotli on server
   - Use binary formats (protobuf) for large data
   - Paginate large lists

3. CACHING STRATEGY:
   Headers:
   - Cache-Control: max-age=3600
   - ETag for conditional requests
   - Last-Modified for validation

   Client:
   - Disk cache for images
   - Memory cache for frequent data
   - Stale-while-revalidate pattern

4. CONNECTION OPTIMIZATION:
   - HTTP/2 multiplexing
   - Connection pooling (max 6 per host)
   - Preconnect to known hosts
   - DNS prefetch

5. PREFETCHING:
   // Prefetch next screen data
   fun onListItemVisible(index: Int) {
       if (index == items.size - 5) {
           prefetchNextPage()
       }
   }

   // Prefetch likely navigation targets
   fun onBookSelected(book: Book) {
       prefetchBookDetails(book.id)
       prefetchBookCover(book.coverUrl)
   }
```

### 5. Battery Optimization

```text
BATTERY IMPACT FACTORS:

| Factor           | Impact | Mitigation                          |
|------------------|--------|-------------------------------------|
| Screen on time   | HIGH   | Dark mode, reduce brightness calls  |
| CPU wake         | HIGH   | Batch work, reduce polling          |
| Network          | MEDIUM | Coalesce requests, use push         |
| GPS              | HIGH   | Reduce accuracy when possible       |
| Sensors          | MEDIUM | Unregister when not needed          |
| Background work  | HIGH   | Use WorkManager/BGTaskScheduler     |

OPTIMIZATION STRATEGIES:

1. REDUCE POLLING:
   // Instead of polling every 10 seconds
   while (true) {
       fetchUpdates()
       delay(10_000)
   }

   // Use push notifications or WebSocket
   socket.onMessage { update ->
       handleUpdate(update)
   }

2. BATCH OPERATIONS:
   // Android WorkManager
   val constraints = Constraints.Builder()
       .setRequiredNetworkType(NetworkType.CONNECTED)
       .setRequiresBatteryNotLow(true)
       .build()

   // iOS BGTaskScheduler
   BGTaskScheduler.shared.register(forTaskWithIdentifier: "sync") { task in
       performSync()
   }

3. DEFER NON-CRITICAL WORK:
   - Analytics: batch and send on app backgrounding
   - Image prefetch: only on WiFi
   - Database maintenance: when charging

4. LOCATION OPTIMIZATION:
   // Use significant location changes instead of continuous
   locationManager.startMonitoringSignificantLocationChanges()

   // Reduce accuracy when approximate is sufficient
   locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters
```

### 6. Platform-Specific Profiling

```text
PROFILING TOOLS:

iOS:
┌─────────────────────────────────────────────────────────────┐
│ Instruments (Xcode)                                          │
├─────────────────────────────────────────────────────────────┤
│ • Time Profiler     → CPU usage, hot paths                  │
│ • Allocations       → Memory usage, object counts           │
│ • Leaks             → Memory leak detection                 │
│ • Core Animation    → Rendering performance, FPS            │
│ • Network           → Request timing, payload sizes         │
│ • Energy Log        → Battery impact analysis               │
└─────────────────────────────────────────────────────────────┘

Android:
┌─────────────────────────────────────────────────────────────┐
│ Android Studio Profiler                                      │
├─────────────────────────────────────────────────────────────┤
│ • CPU Profiler      → Method traces, flame graphs           │
│ • Memory Profiler   → Heap dumps, allocation tracking       │
│ • Network Profiler  → Request inspection, timing            │
│ • Energy Profiler   → Battery impact estimation             │
├─────────────────────────────────────────────────────────────┤
│ Additional Tools                                             │
├─────────────────────────────────────────────────────────────┤
│ • Perfetto          → System-wide tracing                   │
│ • GPU Inspector     → Rendering analysis                    │
│ • Layout Inspector  → View hierarchy analysis               │
└─────────────────────────────────────────────────────────────┘

Flutter:
┌─────────────────────────────────────────────────────────────┐
│ Flutter DevTools                                             │
├─────────────────────────────────────────────────────────────┤
│ • Performance       → Frame rendering, jank detection       │
│ • Memory            → Heap snapshots, allocation tracking   │
│ • CPU Profiler      → Dart VM profiling                     │
│ • Network           → HTTP inspection                       │
│ • Widget Inspector  → Widget tree, rebuild tracking         │
└─────────────────────────────────────────────────────────────┘

React Native:
┌─────────────────────────────────────────────────────────────┐
│ Flipper                                                      │
├─────────────────────────────────────────────────────────────┤
│ • Hermes Debugger   → JS debugging, profiling               │
│ • Layout Inspector  → Component tree                        │
│ • Network           → Request inspection                    │
│ • Databases         → SQLite, AsyncStorage inspection       │
│ • React DevTools    → Component profiling                   │
└─────────────────────────────────────────────────────────────┘
```

## Quality Gates

| Gate ID | Purpose | Threshold |
|---------|---------|-----------|
| QG-PERF-001 | Cold start time | < 2000ms |
| QG-PERF-002 | Frame rate | 60 FPS (95th percentile) |
| QG-PERF-003 | Memory peak | < 150MB |
| QG-PERF-004 | Memory leaks | 0 detected |
| QG-PERF-005 | Battery drain | < 5%/hour active |

## Output

This skill produces:
- Performance audit report
- Optimization recommendations
- Profiling instructions per platform
- Before/after metrics comparison
- Regression test suite

## Integration with Spec Kit

- **`/speckit.implement`**: Apply optimization patterns during development
- **`/speckit.analyze`**: Validate performance metrics before release
- **MQS calculation**: Performance contributes 20 points to MQS
