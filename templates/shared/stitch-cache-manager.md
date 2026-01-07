# Stitch Cache Manager Module

**Version**: 1.0.0
**Purpose**: Incremental generation and session reuse for developer productivity
**Performance Target**: 80% reduction on re-runs (450s → 90s with 1 change)
**Dependencies**: `stitch-integration.md`

---

## Overview

This module enables intelligent caching and incremental generation to dramatically reduce time on re-runs by:

1. **Prompt Cache**: Save generated prompts with metadata for reuse in retry/manual mode
2. **Incremental Detection**: Skip screens where wireframes and design context haven't changed
3. **Session Reuse**: Persist browser authentication state to save ~30s per run

---

## Configuration

```javascript
CACHE_MANAGER_CONFIG = {
  // Cache directories
  paths: {
    cache_root: ".speckit/stitch/cache/",
    prompts: ".speckit/stitch/cache/prompts/",
    session: ".speckit/stitch/cache/session/",
    index: ".speckit/stitch/cache/index.json",
    session_state: ".speckit/stitch/cache/session/state.json"
  },

  // Prompt cache
  prompt_cache: {
    enabled: true,
    save_on_generate: true,
    include_metadata: true,
    compress: false  // Optional gzip compression
  },

  // Incremental generation
  incremental: {
    enabled: true,
    check_wireframe_mtime: true,
    check_design_context_mtime: true,
    check_output_exists: true,
    hash_algorithm: "sha256"  // For design context hashing
  },

  // Session reuse
  session: {
    enabled: true,
    ttl_minutes: 60,  // Session expires after 1 hour
    persist_cookies: true,
    persist_storage: true,
    cdp_endpoint_file: ".speckit/stitch/cache/session/cdp-endpoint.txt"
  }
}
```

---

## Core Functions

### 1. Prompt Cache System

```text
FUNCTION cache_prompt(wireframe, prompt, design_context_hash):
  """
  Save generated prompt to cache with metadata for reuse.

  Args:
    wireframe: Wireframe object
    prompt: Generated prompt text
    design_context_hash: SHA256 hash of design context

  Returns:
    {
      success: boolean,
      cache_file: string (path to cached prompt)
    }
  """

  cache_dir = CACHE_MANAGER_CONFIG.paths.prompts
  MKDIR cache_dir IF NOT EXISTS

  # Generate cache key
  cache_key = "{wireframe.feature}_{wireframe.screen_name}"
  cache_file = "{cache_dir}/{cache_key}.json"

  # Build cache entry with metadata
  cache_entry = {
    version: "1.0",
    cached_at: NOW_ISO(),
    screen_name: wireframe.screen_name,
    feature: wireframe.feature,
    wireframe_path: wireframe.file_path,
    wireframe_mtime: GET_FILE_MTIME(wireframe.file_path),
    design_context_hash: design_context_hash,
    prompt: prompt,
    metadata: {
      wireframe_sections: wireframe.sections OR [],
      design_tokens: design_context.tokens OR {},
      component_library: design_context.component_library OR null
    }
  }

  TRY:
    # Write cache entry
    WRITE_JSON(cache_entry, cache_file, { indent: 2 })

    # Update cache index
    update_cache_index(cache_key, {
      screen_name: wireframe.screen_name,
      feature: wireframe.feature,
      cached_at: cache_entry.cached_at,
      cache_file: cache_file
    })

    LOG "💾 Cached prompt for {wireframe.screen_name}"

    RETURN {
      success: true,
      cache_file: cache_file
    }

  CATCH error:
    LOG "⚠️  Failed to cache prompt: {error.message}"
    RETURN {
      success: false,
      error: error.message
    }


FUNCTION get_cached_prompt(wireframe, design_context_hash):
  """
  Retrieve cached prompt if valid (unchanged wireframe & design context).

  Args:
    wireframe: Wireframe object
    design_context_hash: SHA256 hash of current design context

  Returns:
    {
      found: boolean,
      valid: boolean,
      prompt: string OR null,
      reason: string (if not valid)
    }
  """

  cache_dir = CACHE_MANAGER_CONFIG.paths.prompts
  cache_key = "{wireframe.feature}_{wireframe.screen_name}"
  cache_file = "{cache_dir}/{cache_key}.json"

  # Check if cache file exists
  IF NOT FILE_EXISTS(cache_file):
    RETURN {
      found: false,
      valid: false,
      prompt: null,
      reason: "no_cache_entry"
    }

  TRY:
    # Load cache entry
    cache_entry = READ_JSON(cache_file)

    # Validate cache freshness
    wireframe_mtime = GET_FILE_MTIME(wireframe.file_path)

    # Check 1: Wireframe modified since cache?
    IF cache_entry.wireframe_mtime != wireframe_mtime:
      RETURN {
        found: true,
        valid: false,
        prompt: null,
        reason: "wireframe_modified"
      }

    # Check 2: Design context changed?
    IF cache_entry.design_context_hash != design_context_hash:
      RETURN {
        found: true,
        valid: false,
        prompt: null,
        reason: "design_context_changed"
      }

    # Cache is valid
    LOG "✅ Using cached prompt for {wireframe.screen_name}"

    RETURN {
      found: true,
      valid: true,
      prompt: cache_entry.prompt,
      reason: "valid"
    }

  CATCH error:
    LOG "⚠️  Failed to read cache: {error.message}"
    RETURN {
      found: true,
      valid: false,
      prompt: null,
      reason: "cache_read_error"
    }


FUNCTION update_cache_index(cache_key, entry):
  """
  Update the cache index file with new/updated entry.

  Args:
    cache_key: Unique cache key
    entry: Index entry metadata
  """

  index_file = CACHE_MANAGER_CONFIG.paths.index
  MKDIR DIRNAME(index_file) IF NOT EXISTS

  TRY:
    # Load existing index or create new
    IF FILE_EXISTS(index_file):
      index = READ_JSON(index_file)
    ELSE:
      index = {
        version: "1.0",
        entries: {}
      }

    # Update entry
    index.entries[cache_key] = entry
    index.last_updated = NOW_ISO()

    # Write index
    WRITE_JSON(index, index_file, { indent: 2 })

  CATCH error:
    LOG "⚠️  Failed to update cache index: {error.message}"
```

---

### 2. Incremental Generation Detector

```text
FUNCTION detect_incremental_screens(wireframes, design_context, options = {}):
  """
  Detect which screens can be skipped (unchanged) vs need regeneration.

  Args:
    wireframes: Array of wireframe objects
    design_context: Design context object
    options: {
      force: boolean (default: false) - Force regeneration of all
      incremental: boolean (default: true) - Enable incremental detection
    }

  Returns:
    {
      to_generate: Array of wireframes needing generation,
      to_skip: Array of wireframes to skip (unchanged),
      stats: {
        total: number,
        generate_count: number,
        skip_count: number,
        time_saved_est_seconds: number
      }
    }
  """

  # Force mode: regenerate all
  IF options.force:
    LOG "🔄 Force mode: regenerating all {wireframes.length} screens"
    RETURN {
      to_generate: wireframes,
      to_skip: [],
      stats: {
        total: wireframes.length,
        generate_count: wireframes.length,
        skip_count: 0,
        time_saved_est_seconds: 0
      }
    }

  # Incremental disabled: regenerate all
  IF NOT options.incremental AND NOT CACHE_MANAGER_CONFIG.incremental.enabled:
    RETURN {
      to_generate: wireframes,
      to_skip: [],
      stats: {
        total: wireframes.length,
        generate_count: wireframes.length,
        skip_count: 0,
        time_saved_est_seconds: 0
      }
    }

  # Calculate design context hash
  design_context_hash = hash_design_context(design_context)

  to_generate = []
  to_skip = []

  FOR wireframe IN wireframes:
    skip_result = should_skip_screen(wireframe, design_context_hash)

    IF skip_result.should_skip:
      to_skip.push({
        wireframe: wireframe,
        reason: skip_result.reason
      })
      LOG "⏭️  Skipping {wireframe.screen_name}: {skip_result.reason}"
    ELSE:
      to_generate.push(wireframe)

  # Calculate time savings (assuming ~45s per screen)
  AVG_SCREEN_TIME_SECONDS = 45
  time_saved = to_skip.length * AVG_SCREEN_TIME_SECONDS

  stats = {
    total: wireframes.length,
    generate_count: to_generate.length,
    skip_count: to_skip.length,
    time_saved_est_seconds: time_saved
  }

  # Display summary
  IF to_skip.length > 0:
    LOG "┌────────────────────────────────────────────────────────┐"
    LOG "│  ⚡ INCREMENTAL GENERATION                              │"
    LOG "├────────────────────────────────────────────────────────┤"
    LOG "│  Total Screens: {stats.total}                          │"
    LOG "│  To Generate: {stats.generate_count} (changed)         │"
    LOG "│  To Skip: {stats.skip_count} (unchanged)               │"
    LOG "│  Est. Time Saved: {format_duration(time_saved * 1000)} │"
    LOG "└────────────────────────────────────────────────────────┘"

  RETURN {
    to_generate: to_generate,
    to_skip: to_skip,
    stats: stats
  }


FUNCTION should_skip_screen(wireframe, design_context_hash):
  """
  Determine if a screen should be skipped (unchanged).

  Args:
    wireframe: Wireframe object
    design_context_hash: SHA256 hash of design context

  Returns:
    {
      should_skip: boolean,
      reason: string
    }
  """

  output_dir = ".preview/stitch-mockups/{wireframe.feature}/{wireframe.screen_name}"

  # Check 1: Output directory exists?
  IF NOT DIR_EXISTS(output_dir):
    RETURN {
      should_skip: false,
      reason: "no_output_directory"
    }

  # Check 2: Required output files exist?
  required_files = [
    "{output_dir}/stitch-output.html",
    "{output_dir}/screenshot-desktop.png",
    "{output_dir}/screenshot-mobile.png"
  ]

  FOR file IN required_files:
    IF NOT FILE_EXISTS(file):
      RETURN {
        should_skip: false,
        reason: "missing_output_files"
      }

  # Check 3: Wireframe modified since output generation?
  wireframe_mtime = GET_FILE_MTIME(wireframe.file_path)
  output_html_mtime = GET_FILE_MTIME("{output_dir}/stitch-output.html")

  IF wireframe_mtime > output_html_mtime:
    RETURN {
      should_skip: false,
      reason: "wireframe_modified"
    }

  # Check 4: Design context changed? (via cached prompt comparison)
  cached_prompt = get_cached_prompt(wireframe, design_context_hash)

  IF cached_prompt.found AND NOT cached_prompt.valid:
    RETURN {
      should_skip: false,
      reason: cached_prompt.reason  // "design_context_changed"
    }

  # All checks passed - safe to skip
  RETURN {
    should_skip: true,
    reason: "unchanged"
  }


FUNCTION hash_design_context(design_context):
  """
  Generate SHA256 hash of design context for change detection.

  Args:
    design_context: Design context object

  Returns:
    String (SHA256 hex digest)
  """

  # Extract relevant fields for hashing
  hash_input = {
    tokens: design_context.tokens OR {},
    component_library: design_context.component_library OR null,
    brand: design_context.brand OR {},
    style_guide: design_context.style_guide OR {}
  }

  # Serialize to canonical JSON (sorted keys)
  json_str = JSON_STRINGIFY(hash_input, { sort_keys: true })

  # Hash with SHA256
  hash = SHA256(json_str)

  RETURN hash
```

---

### 3. Browser Session Reuse

```text
FUNCTION save_browser_session(context, page):
  """
  Persist browser session state for reuse.

  Args:
    context: Browser context object
    page: Page object

  Returns:
    {
      success: boolean,
      session_id: string OR null
    }
  """

  session_dir = CACHE_MANAGER_CONFIG.paths.session
  MKDIR session_dir IF NOT EXISTS

  session_id = generate_uuid()

  TRY:
    # Save cookies
    cookies = await context.cookies()
    cookies_file = "{session_dir}/cookies.json"
    WRITE_JSON(cookies, cookies_file)

    # Save local storage (if available)
    storage_data = await page.evaluate(() => {
      RETURN {
        localStorage: Object.fromEntries(Object.entries(localStorage)),
        sessionStorage: Object.fromEntries(Object.entries(sessionStorage))
      }
    })
    storage_file = "{session_dir}/storage.json"
    WRITE_JSON(storage_data, storage_file)

    # Save CDP endpoint (if in CDP mode)
    IF context.cdpEndpoint:
      cdp_file = CACHE_MANAGER_CONFIG.paths.session.cdp_endpoint_file
      WRITE cdp_file, context.cdpEndpoint

    # Save session state
    state = {
      session_id: session_id,
      created_at: NOW_ISO(),
      expires_at: ADD_MINUTES(NOW(), CACHE_MANAGER_CONFIG.session.ttl_minutes),
      cookies_file: cookies_file,
      storage_file: storage_file,
      cdp_endpoint: context.cdpEndpoint OR null,
      mode: context._mode OR "unknown"
    }

    state_file = CACHE_MANAGER_CONFIG.paths.session_state
    WRITE_JSON(state, state_file)

    LOG "💾 Saved browser session (expires in {CACHE_MANAGER_CONFIG.session.ttl_minutes}m)"

    RETURN {
      success: true,
      session_id: session_id
    }

  CATCH error:
    LOG "⚠️  Failed to save session: {error.message}"
    RETURN {
      success: false,
      session_id: null
    }


FUNCTION load_browser_session():
  """
  Load and validate cached browser session.

  Returns:
    {
      valid: boolean,
      session_state: object OR null,
      reason: string (if not valid)
    }
  """

  state_file = CACHE_MANAGER_CONFIG.paths.session_state

  # Check if session state exists
  IF NOT FILE_EXISTS(state_file):
    RETURN {
      valid: false,
      session_state: null,
      reason: "no_session_state"
    }

  TRY:
    # Load session state
    state = READ_JSON(state_file)

    # Check expiration
    now = NOW()
    expires_at = PARSE_ISO(state.expires_at)

    IF now > expires_at:
      RETURN {
        valid: false,
        session_state: state,
        reason: "session_expired"
      }

    # Check if files still exist
    IF NOT FILE_EXISTS(state.cookies_file):
      RETURN {
        valid: false,
        session_state: state,
        reason: "cookies_file_missing"
      }

    IF NOT FILE_EXISTS(state.storage_file):
      RETURN {
        valid: false,
        session_state: state,
        reason: "storage_file_missing"
      }

    # Session is valid
    LOG "✅ Found valid cached session (expires: {format_relative_time(expires_at)})"

    RETURN {
      valid: true,
      session_state: state,
      reason: "valid"
    }

  CATCH error:
    LOG "⚠️  Failed to load session: {error.message}"
    RETURN {
      valid: false,
      session_state: null,
      reason: "load_error"
    }


FUNCTION restore_browser_session(context, page, session_state):
  """
  Restore browser session from cached state.

  Args:
    context: Browser context object
    page: Page object
    session_state: Session state object from load_browser_session()

  Returns:
    {
      success: boolean,
      authenticated: boolean
    }
  """

  TRY:
    # Restore cookies
    cookies = READ_JSON(session_state.cookies_file)
    await context.addCookies(cookies)
    LOG "✅ Restored {cookies.length} cookies"

    # Restore local/session storage
    storage_data = READ_JSON(session_state.storage_file)

    await page.evaluate((data) => {
      # Restore localStorage
      FOR key, value IN Object.entries(data.localStorage):
        localStorage.setItem(key, value)

      # Restore sessionStorage
      FOR key, value IN Object.entries(data.sessionStorage):
        sessionStorage.setItem(key, value)
    }, storage_data)

    LOG "✅ Restored storage data"

    # Navigate to Stitch to verify session
    await page.goto("https://stitch.withgoogle.com", { waitUntil: "networkidle" })

    # Wait a bit for auth check
    await wait(2000)

    # Verify authentication
    is_authenticated = await verify_stitch_authentication(page)

    IF is_authenticated:
      LOG "✅ Session restored successfully"
      RETURN {
        success: true,
        authenticated: true
      }
    ELSE:
      LOG "⚠️  Session restored but not authenticated"
      RETURN {
        success: true,
        authenticated: false
      }

  CATCH error:
    LOG "❌ Failed to restore session: {error.message}"
    RETURN {
      success: false,
      authenticated: false
    }


FUNCTION verify_stitch_authentication(page):
  """
  Verify that the user is authenticated to Stitch.

  Args:
    page: Page object

  Returns:
    boolean (true if authenticated)
  """

  TRY:
    # Check for auth indicators (adjust selectors as needed)
    # Option 1: Look for user profile element
    profile_element = await page.$('[data-testid="user-profile"]')
    IF profile_element:
      RETURN true

    # Option 2: Check for "Sign in" button (if present, not authenticated)
    signin_button = await page.$('button:has-text("Sign in")')
    IF signin_button:
      RETURN false

    # Option 3: Check URL (if redirected to login)
    url = page.url()
    IF url.includes("/login") OR url.includes("/signin"):
      RETURN false

    # Default: assume authenticated if no negative indicators
    RETURN true

  CATCH error:
    LOG "⚠️  Auth verification failed: {error.message}"
    RETURN false


FUNCTION clear_cached_session():
  """
  Clear cached session data.
  """

  session_dir = CACHE_MANAGER_CONFIG.paths.session

  IF DIR_EXISTS(session_dir):
    TRY:
      REMOVE_DIR_RECURSIVE(session_dir)
      MKDIR session_dir
      LOG "🧹 Cleared cached session"
    CATCH error:
      LOG "⚠️  Failed to clear session: {error.message}"
```

---

## Integration with Main Workflow

### Updated Workflow with Caching

```text
# Import cache manager
IMPORT * FROM templates/shared/stitch-cache-manager.md:
  - cache_prompt
  - get_cached_prompt
  - detect_incremental_screens
  - hash_design_context
  - save_browser_session
  - load_browser_session
  - restore_browser_session
  - clear_cached_session
  - CACHE_MANAGER_CONFIG

# BEFORE Phase 3: Incremental detection
IF options.incremental !== false:
  design_context_hash = hash_design_context(design_context)

  incremental_result = detect_incremental_screens(wireframes, design_context, {
    force: options.force,
    incremental: options.incremental
  })

  # Update wireframes list to only those needing generation
  wireframes = incremental_result.to_generate

  # Store skipped screens for reporting
  skipped_screens = incremental_result.to_skip
  incremental_stats = incremental_result.stats

  IF wireframes.length == 0:
    LOG "✅ All screens up-to-date. Nothing to generate!"
    RETURN {
      mode: active_mode,
      results: [],
      skipped: skipped_screens.length,
      incremental_stats: incremental_stats
    }

# DURING Phase 4: Cache prompts
FOR each wireframe:
  # Generate prompt
  prompt = stitch_generate_prompt(wireframe, design_context)

  # Cache prompt for reuse
  cache_prompt(wireframe, prompt, design_context_hash)

  # ... continue with generation ...

# AFTER Phase 9: Save session for reuse
IF options.reuse_session !== false:
  save_result = await save_browser_session(context, page)
  IF save_result.success:
    LOG "💾 Session saved for next run (~30s saved)"
```

---

## Performance Impact

### Re-run Scenarios

**Scenario 1: No changes (all screens unchanged)**
- Before: 450s (regenerate all 10 screens)
- After: ~5s (detect all unchanged, skip all)
- **Improvement: 99% faster**

**Scenario 2: 1 wireframe changed (9/10 unchanged)**
- Before: 450s (regenerate all 10 screens)
- After: ~90s (skip 9, regenerate 1, includes detection + session restore)
- **Improvement: 80% faster**

**Scenario 3: Design context changed (all screens need regeneration)**
- Before: 450s
- After: 450s (no skipping, but session reuse saves ~30s)
- **Improvement: ~7% faster**

### Session Reuse Savings

- **Browser startup**: ~10s saved
- **Authentication flow**: ~20s saved
- **Total per run**: ~30s saved

---

## Cache Management

### Cache Directory Structure

```
.speckit/stitch/cache/
├── index.json                    # Cache index
├── prompts/                      # Cached prompts
│   ├── auth_login-screen.json
│   ├── auth_signup-screen.json
│   └── dashboard_home.json
└── session/                      # Session data
    ├── state.json                # Session state
    ├── cookies.json              # Browser cookies
    ├── storage.json              # localStorage/sessionStorage
    └── cdp-endpoint.txt          # CDP endpoint (if using CDP mode)
```

### Cache Invalidation

Cache is invalidated when:
1. Wireframe file modified (mtime check)
2. Design context changed (hash mismatch)
3. Output files missing/incomplete
4. Session expired (> 1 hour)
5. User passes `--force` flag

### Manual Cache Clearing

```bash
# Clear all caches
rm -rf .speckit/stitch/cache/

# Clear only session cache
rm -rf .speckit/stitch/cache/session/

# Clear only prompt cache
rm -rf .speckit/stitch/cache/prompts/
```

---

## Utility Functions

```text
FUNCTION format_relative_time(date):
  """
  Format date as relative time (e.g., "in 45 minutes").

  Args:
    date: Date object or ISO string

  Returns:
    String
  """

  now = NOW()
  diff_ms = date - now
  diff_minutes = Math.floor(diff_ms / 60000)

  IF diff_minutes < 0:
    RETURN "expired"
  ELSE IF diff_minutes < 60:
    RETURN "in {diff_minutes}m"
  ELSE:
    hours = Math.floor(diff_minutes / 60)
    minutes = diff_minutes % 60
    RETURN "in {hours}h {minutes}m"
```

---

## Error Handling

All cache operations are non-blocking:
- Cache failures don't stop generation
- Invalid cache entries are ignored
- Session restore failures fall back to fresh authentication
- Incremental detection failures default to full regeneration

---

## Testing & Validation

### Unit Tests

```javascript
// Test incremental detection
wireframes = create_mock_wireframes(10)
design_context = create_mock_design_context()

// First run: all generated
result1 = detect_incremental_screens(wireframes, design_context)
ASSERT result1.to_generate.length == 10
ASSERT result1.to_skip.length == 0

// Create mock outputs
create_mock_outputs(wireframes)

// Second run: all skipped
result2 = detect_incremental_screens(wireframes, design_context)
ASSERT result2.to_generate.length == 0
ASSERT result2.to_skip.length == 10

// Modify one wireframe
TOUCH(wireframes[0].file_path)

// Third run: 1 generated, 9 skipped
result3 = detect_incremental_screens(wireframes, design_context)
ASSERT result3.to_generate.length == 1
ASSERT result3.to_skip.length == 9
```

---

## Backward Compatibility

✅ **Fully backward compatible**:

- Incremental detection enabled by default (`--incremental`)
- Can be disabled with `--incremental false`
- Force mode available via `--force` (ignore cache, regenerate all)
- Session reuse enabled by default (`--reuse-session`)
- Can be disabled with `--no-reuse-session`

---

## Version History

- **v1.0.0** (2026-01-06): Initial implementation
  - Prompt cache system with metadata
  - Incremental generation detector
  - Browser session reuse logic
  - 80% time savings on re-runs
