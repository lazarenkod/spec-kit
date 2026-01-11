# Analytics Privacy & Compliance

This document provides guidance on implementing privacy-compliant analytics that meets GDPR, CCPA, and other data protection regulations.

## GDPR Compliance Checklist

- [ ] **Cookie consent banner** displayed before tracking starts
- [ ] **IP anonymization** enabled in analytics provider
- [ ] **PII masking** implemented (emails, phone numbers, addresses)
- [ ] **Data retention policy** documented and enforced (default: 90 days)
- [ ] **Right to access**: API endpoint to export user's analytics data
- [ ] **Right to erasure**: API endpoint to delete user's analytics data
- [ ] **Right to opt-out**: `/analytics/opt-out` page implemented
- [ ] **Privacy policy** updated with analytics disclosure
- [ ] **Data processing agreement** (DPA) signed with analytics provider
- [ ] **Legitimate interest** or **explicit consent** basis documented

## CCPA Compliance Checklist

- [ ] **"Do Not Sell My Personal Information"** link in footer
- [ ] **Opt-out mechanism** honors CCPA requests within 15 days
- [ ] **Privacy notice** discloses what data is collected and why
- [ ] **User data download** available on request
- [ ] **Third-party disclosure** documented in privacy policy

## IP Anonymization

### PostHog

```typescript
posthog.init('API_KEY', {
  api_host: 'https://app.posthog.com',
  property_blacklist: ['$ip'], // Don't capture IP
})
```

### Mixpanel

```javascript
mixpanel.init('API_KEY', {
  ip: false, // Disable IP tracking
})
```

### Amplitude

```javascript
amplitude.getInstance().init('API_KEY', null, {
  trackingOptions: {
    ipAddress: false, // Disable IP tracking
  }
})
```

### Umami (Self-Hosted)

IP anonymization is **enabled by default** in Umami. No configuration needed.

### Google Analytics 4

```javascript
gtag('config', 'GA_MEASUREMENT_ID', {
  anonymize_ip: true
})
```

## PII Masking Implementation

### Email Masking

```typescript
function maskEmail(email: string): string {
  const [local, domain] = email.split('@')
  if (local.length <= 1) return '***@' + domain
  return `${local[0]}***@${domain}`
}

// user@example.com → u***@example.com
```

### Phone Masking

```typescript
function maskPhone(phone: string): string {
  const digits = phone.replace(/\D/g, '')
  if (digits.length < 4) return '***'
  return '***-***-' + digits.slice(-4)
}

// +1-555-123-4567 → ***-***-4567
```

### Full Name Masking

```typescript
function maskName(name: string): string {
  const parts = name.split(' ')
  if (parts.length === 1) return parts[0][0] + '***'
  return parts[0][0] + '*** ' + parts[parts.length - 1][0] + '***'
}

// John Smith → J*** S***
```

### Address Masking

```typescript
function maskAddress(address: string): string {
  // Keep only city and state/country
  const parts = address.split(',').map(p => p.trim())
  if (parts.length >= 2) {
    return `***${parts[parts.length - 2]}, ${parts[parts.length - 1]}`
  }
  return '***'
}

// 123 Main St, San Francisco, CA → *** San Francisco, CA
```

## Cookie Consent Banner

### Using CookieConsent Library

```html
<!-- Add to <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css">
<script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js"></script>

<script>
window.addEventListener('load', function() {
  window.cookieconsent.initialise({
    palette: {
      popup: { background: "#000" },
      button: { background: "#f1d600" }
    },
    type: "opt-in", // GDPR requires opt-in
    content: {
      message: "This website uses cookies and analytics to improve your experience.",
      dismiss: "Decline",
      allow: "Accept",
      link: "Learn more",
      href: "/privacy-policy"
    },
    onStatusChange: function(status) {
      if (this.hasConsented()) {
        // Initialize analytics only after consent
        initializeAnalytics()
      }
    }
  })
})

function initializeAnalytics() {
  // PostHog
  posthog.init('API_KEY', { /* config */ })

  // Umami
  // No action needed - script already loaded
}
</script>
```

### React Cookie Consent

```typescript
import CookieConsent from 'react-cookie-consent'

function App() {
  const [analyticsEnabled, setAnalyticsEnabled] = useState(false)

  return (
    <>
      <CookieConsent
        enableDeclineButton
        onAccept={() => {
          setAnalyticsEnabled(true)
          initializeAnalytics()
        }}
        onDecline={() => {
          setAnalyticsEnabled(false)
        }}
      >
        This website uses cookies and analytics to improve your experience.
      </CookieConsent>

      {/* Rest of app */}
    </>
  )
}
```

## Opt-Out Page Implementation

### `/analytics/opt-out` Route

```typescript
// Next.js example
export default function OptOutPage() {
  const [optedOut, setOptedOut] = useState(false)

  const handleOptOut = () => {
    // Store opt-out preference
    localStorage.setItem('analytics-opt-out', 'true')

    // Disable PostHog
    posthog.opt_out_capturing()

    setOptedOut(true)
  }

  return (
    <div>
      <h1>Analytics Opt-Out</h1>
      {!optedOut ? (
        <>
          <p>Click below to opt out of analytics tracking.</p>
          <button onClick={handleOptOut}>Opt Out</button>
        </>
      ) : (
        <p>You have successfully opted out of analytics tracking.</p>
      )}
    </div>
  )
}
```

### Checking Opt-Out Preference

```typescript
function isAnalyticsOptedOut(): boolean {
  // Check localStorage
  if (localStorage.getItem('analytics-opt-out') === 'true') {
    return true
  }

  // Check Do Not Track (DNT) header
  if (navigator.doNotTrack === '1') {
    return true
  }

  return false
}

// In analytics initialization
if (!isAnalyticsOptedOut()) {
  posthog.init('API_KEY', { /* config */ })
}
```

## Data Retention Policy

### PostHog Configuration

```yaml
# docker-compose.yml or posthog config
environment:
  - RETENTION_PERIOD_DAYS=90
```

### Automated Data Deletion (Backend)

```python
# Scheduled job (runs daily)
from datetime import datetime, timedelta

def purge_old_analytics_data():
    retention_days = 90
    cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

    # Delete events older than retention period
    db.execute("""
        DELETE FROM analytics_events
        WHERE timestamp < %s
    """, (cutoff_date,))

    print(f"Purged analytics data older than {retention_days} days")
```

## Right to Access (Data Export)

### API Endpoint

```python
@app.route('/api/user/analytics-data', methods=['GET'])
@login_required
def export_analytics_data():
    user_id = current_user.id

    # Fetch all analytics events for user
    events = db.query("""
        SELECT event_name, properties, timestamp
        FROM analytics_events
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """, (user_id,))

    # Return as JSON
    return jsonify({
        'user_id': user_id,
        'events': [dict(e) for e in events]
    })
```

## Right to Erasure (Data Deletion)

### API Endpoint

```python
@app.route('/api/user/analytics-data', methods=['DELETE'])
@login_required
def delete_analytics_data():
    user_id = current_user.id

    # Delete all analytics events for user
    db.execute("""
        DELETE FROM analytics_events
        WHERE user_id = %s
    """, (user_id,))

    # Also delete from analytics provider
    posthog.delete_user(user_id)

    return jsonify({'message': 'Analytics data deleted'})
```

## Privacy Policy Template

Add this section to your privacy policy:

```markdown
## Analytics and Cookies

### What We Track
We use analytics tools to understand how users interact with our application. We track:
- Page views and navigation patterns
- Button clicks and feature usage
- Session duration and frequency
- Device type, browser, and operating system

### What We Don't Track
We do NOT track:
- Personal identification information (PII) without explicit consent
- Full IP addresses (IP anonymization is enabled)
- Sensitive personal data

### Analytics Providers
We use the following analytics providers:
- **Umami** (self-hosted) - Web analytics for page views
- **PostHog** (self-hosted) - Product analytics for user behavior

### Your Rights
You have the right to:
- **Opt out** of analytics tracking at any time: [/analytics/opt-out](/analytics/opt-out)
- **Access** your analytics data: [Request data export](/account/export-data)
- **Delete** your analytics data: [Request data deletion](/account/delete-data)

### Cookie Consent
We use cookies only with your explicit consent. You can manage your cookie preferences at any time.

### Data Retention
Analytics data is retained for 90 days, after which it is automatically deleted.

### Contact
For privacy-related questions, contact: privacy@example.com
```

## Do Not Track (DNT) Support

```typescript
function respectDNT() {
  if (navigator.doNotTrack === '1') {
    console.log('Do Not Track enabled - analytics disabled')
    return false
  }
  return true
}

if (respectDNT()) {
  posthog.init('API_KEY', { /* config */ })
}
```

## Testing Compliance

### Manual Testing Checklist

- [ ] Cookie banner appears on first visit
- [ ] Analytics does NOT fire before consent
- [ ] Opt-out page works and persists preference
- [ ] DNT header is respected
- [ ] IP address is anonymized in analytics dashboard
- [ ] PII is masked in event properties
- [ ] Data export API returns user's analytics data
- [ ] Data deletion API removes user's analytics data

### Automated Tests

```typescript
describe('Analytics Privacy Compliance', () => {
  it('should not track before consent', () => {
    render(<App />)
    expect(posthog.capture).not.toHaveBeenCalled()
  })

  it('should mask email in event properties', () => {
    const event = {
      name: 'user_signed_up',
      properties: { email: 'user@example.com' }
    }

    const masked = maskPII(event.properties)
    expect(masked.email).toBe('u***@example.com')
  })

  it('should respect DNT header', () => {
    Object.defineProperty(navigator, 'doNotTrack', { value: '1' })
    expect(respectDNT()).toBe(false)
  })
})
```

## Resources

- [GDPR Official Text](https://gdpr-info.eu/)
- [CCPA Official Text](https://oag.ca.gov/privacy/ccpa)
- [PostHog Privacy Docs](https://posthog.com/docs/privacy)
- [Mixpanel GDPR Compliance](https://mixpanel.com/legal/gdpr-compliance/)
- [Amplitude Privacy](https://amplitude.com/privacy)
- [Cookie Consent Library](https://www.cookieconsent.com/)
