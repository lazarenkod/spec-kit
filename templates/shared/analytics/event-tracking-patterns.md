# Analytics Event Tracking Patterns

This document provides copy-paste code snippets for implementing analytics event tracking across different programming languages and frameworks.

## TypeScript/JavaScript (React)

### Basic Setup

```typescript
// src/lib/analytics.ts
import posthog from 'posthog-js'

type AnalyticsEvent =
  | { name: 'user_signed_up'; properties: { method: 'email' | 'oauth'; provider: string } }
  | { name: 'feature_viewed'; properties: { feature_id: string; source: string } }
  | { name: 'button_clicked'; properties: { button_id: string; page: string } }

export function trackEvent<T extends AnalyticsEvent['name']>(
  eventName: T,
  properties: Extract<AnalyticsEvent, { name: T }>['properties']
) {
  const context = {
    ...properties,
    timestamp: new Date().toISOString(),
    user_id: getCurrentUserId(),
    session_id: getSessionId(),
  }

  posthog.capture(eventName, maskPII(context))
}

function maskPII(data: any): any {
  const masked = { ...data }

  if (masked.email) {
    masked.email = maskEmail(masked.email) // "u***@example.com"
  }

  if (masked.phone) {
    masked.phone = maskPhone(masked.phone) // "***-***-1234"
  }

  return masked
}

function getCurrentUserId(): string | undefined {
  // Implement based on your auth system
  return localStorage.getItem('user_id') || undefined
}

function getSessionId(): string {
  let sessionId = sessionStorage.getItem('session_id')
  if (!sessionId) {
    sessionId = crypto.randomUUID()
    sessionStorage.setItem('session_id', sessionId)
  }
  return sessionId
}

function maskEmail(email: string): string {
  const [local, domain] = email.split('@')
  return `${local[0]}***@${domain}`
}

function maskPhone(phone: string): string {
  return phone.replace(/\d(?=\d{4})/g, '*')
}
```

### Usage in Components

```typescript
// @speckit:FR:FR-001 @speckit:AS:AS-1A User can sign up
async function handleSignup(email: string, password: string) {
  const user = await createUser(email, password)

  // [ANALYTICS:AS-1A] Track signup event
  trackEvent('user_signed_up', {
    method: 'email',
    provider: 'local'
  })

  return user
}
```

```typescript
// @speckit:FR:FR-002 @speckit:AS:AS-2B User can view dashboard
function DashboardPage() {
  useEffect(() => {
    // [ANALYTICS:AS-2B] Track feature view
    trackEvent('feature_viewed', {
      feature_id: 'dashboard',
      source: 'navigation'
    })
  }, [])

  return <div>Dashboard content</div>
}
```

## Python (Flask/Django)

### Basic Setup

```python
from posthog import Posthog
import os
import hashlib
import re
from datetime import datetime

posthog = Posthog(
    project_api_key=os.getenv('POSTHOG_API_KEY'),
    host=os.getenv('POSTHOG_HOST', 'https://app.posthog.com')
)

def track_event(event_name: str, properties: dict, user_id: str):
    """
    Track an analytics event with automatic context injection and PII masking.

    Args:
        event_name: Name of the event (e.g., 'user_signed_up')
        properties: Event properties dictionary
        user_id: User identifier
    """
    context = {
        **properties,
        'user_id': user_id,
        'session_id': get_session_id(),
        'timestamp': datetime.utcnow().isoformat()
    }

    masked_context = mask_pii(context)
    posthog.capture(user_id, event_name, masked_context)

def mask_pii(data: dict) -> dict:
    """Mask personally identifiable information in event data."""
    masked = data.copy()

    if 'email' in masked:
        masked['email'] = mask_email(masked['email'])

    if 'phone' in masked:
        masked['phone'] = mask_phone(masked['phone'])

    return masked

def mask_email(email: str) -> str:
    """Mask email address: user@example.com -> u***@example.com"""
    if '@' not in email:
        return email
    local, domain = email.split('@', 1)
    return f"{local[0]}***@{domain}"

def mask_phone(phone: str) -> str:
    """Mask phone number: keep only last 4 digits"""
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 4:
        return '***'
    return '***-***-' + digits[-4:]

def get_session_id() -> str:
    """Get or create session ID from Flask/Django session."""
    from flask import session  # or from django.contrib.sessions.models import Session
    if 'session_id' not in session:
        session['session_id'] = hashlib.sha256(os.urandom(32)).hexdigest()
    return session['session_id']
```

### Usage in Routes

```python
# @speckit:FR:FR-001 @speckit:AS:AS-1A User can sign up
@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']

    user = create_user(email, password)

    # [ANALYTICS:AS-1A] Track signup event
    track_event('user_signed_up', {
        'method': 'email',
        'provider': 'local'
    }, user_id=user.id)

    return jsonify({'user': user.to_dict()})
```

## Go (Gin/Echo)

### Basic Setup

```go
package analytics

import (
    "crypto/rand"
    "encoding/hex"
    "os"
    "regexp"
    "time"

    "github.com/posthog/posthog-go"
)

var client posthog.Client

func Init() {
    client, _ = posthog.NewWithConfig(
        os.Getenv("POSTHOG_API_KEY"),
        posthog.Config{
            Endpoint: os.Getenv("POSTHOG_HOST"),
        },
    )
}

func TrackEvent(eventName string, properties map[string]interface{}, userID string) error {
    properties["user_id"] = userID
    properties["session_id"] = getSessionID()
    properties["timestamp"] = time.Now().UTC().Format(time.RFC3339)

    maskedProps := maskPII(properties)

    return client.Enqueue(posthog.Capture{
        DistinctId: userID,
        Event:      eventName,
        Properties: maskedProps,
    })
}

func maskPII(data map[string]interface{}) map[string]interface{} {
    masked := make(map[string]interface{})
    for k, v := range data {
        if k == "email" {
            if email, ok := v.(string); ok {
                masked[k] = maskEmail(email)
                continue
            }
        }
        if k == "phone" {
            if phone, ok := v.(string); ok {
                masked[k] = maskPhone(phone)
                continue
            }
        }
        masked[k] = v
    }
    return masked
}

func maskEmail(email string) string {
    re := regexp.MustCompile(`^(.)[^@]*(@.*)$`)
    return re.ReplaceAllString(email, "$1***$2")
}

func maskPhone(phone string) string {
    re := regexp.MustCompile(`\d(?=\d{4})`)
    return re.ReplaceAllString(phone, "*")
}

func getSessionID() string {
    b := make([]byte, 16)
    rand.Read(b)
    return hex.EncodeToString(b)
}
```

### Usage in Handlers

```go
// @speckit:FR:FR-001 @speckit:AS:AS-1A User can sign up
func SignupHandler(c *gin.Context) {
    var req SignupRequest
    if err := c.BindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }

    user, err := createUser(req.Email, req.Password)
    if err != nil {
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }

    // [ANALYTICS:AS-1A] Track signup event
    analytics.TrackEvent("user_signed_up", map[string]interface{}{
        "method":   "email",
        "provider": "local",
    }, user.ID)

    c.JSON(200, gin.H{"user": user})
}
```

## Testing Analytics Events

### TypeScript/Jest

```typescript
import { trackEvent } from './analytics'

jest.mock('posthog-js')

describe('Analytics', () => {
  it('tracks signup event', () => {
    const posthog = require('posthog-js')

    trackEvent('user_signed_up', {
      method: 'email',
      provider: 'local'
    })

    expect(posthog.capture).toHaveBeenCalledWith(
      'user_signed_up',
      expect.objectContaining({
        method: 'email',
        provider: 'local',
        timestamp: expect.any(String)
      })
    )
  })
})
```

### Python/pytest

```python
from unittest.mock import patch, MagicMock

def test_track_signup_event():
    with patch('analytics.posthog') as mock_posthog:
        track_event('user_signed_up', {
            'method': 'email',
            'provider': 'local'
        }, user_id='user123')

        mock_posthog.capture.assert_called_once()
        args = mock_posthog.capture.call_args[0]
        assert args[0] == 'user123'
        assert args[1] == 'user_signed_up'
        assert args[2]['method'] == 'email'
```

## Best Practices

1. **Type Safety**: Use TypeScript types or type hints to ensure event names and properties are consistent
2. **PII Masking**: Always mask PII (emails, phone numbers) before sending to analytics
3. **Context Injection**: Automatically inject user_id, session_id, timestamp
4. **Traceability**: Add @speckit comments linking events to acceptance scenarios
5. **Testing**: Mock analytics calls in tests to avoid real API calls
6. **Privacy**: Respect user consent - check consent before tracking
7. **Error Handling**: Wrap analytics calls in try-catch to prevent tracking failures from breaking app
8. **Performance**: Use async/background tracking to avoid blocking user actions

## Provider-Specific Notes

### PostHog
- Supports session recording
- Supports feature flags
- Self-hosted or cloud options

### Mixpanel
- Strong funnel analysis
- Cohort analysis
- Cloud only

### Amplitude
- Strong retention analysis
- Behavioral cohorts
- Cloud only

### Umami (Web Analytics)
- Privacy-first (no cookies by default)
- Self-hosted
- Simple page view tracking

```html
<!-- Add to <head> -->
<script async defer data-website-id="YOUR_WEBSITE_ID" src="http://localhost:3002/umami.js"></script>
```
