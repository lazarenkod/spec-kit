# OWASP Top 10 (2021) Security Checklist

This checklist provides actionable security guidance based on the OWASP Top 10 2021. Use this during specification, planning, and implementation phases to ensure comprehensive security coverage.

**Related Spec Requirements**: Each item should map to `SEC-xxx` requirements in your specification.

---

## A01:2021 - Broken Access Control

### Description
Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of data.

### Detection Methods
- Review authorization checks in code
- Test different user roles and permission levels
- Check for direct object reference vulnerabilities (IDOR)
- Verify horizontal and vertical privilege escalation protection
- Test API endpoints with unauthorized tokens/sessions

### Prevention Patterns

```python
# BAD: No authorization check
@app.route('/user/<user_id>/profile')
def get_profile(user_id):
    user = User.get(user_id)
    return jsonify(user.to_dict())

# GOOD: Proper authorization check
@app.route('/user/<user_id>/profile')
@login_required
def get_profile(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403, "Access denied")
    user = User.get(user_id)
    return jsonify(user.to_dict())
```

```javascript
// BAD: Client-side only permission check
if (user.role === 'admin') {
    <AdminPanel />
}

// GOOD: Server validates permissions
async function getAdminData() {
    const response = await fetch('/api/admin/data', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.status === 403) throw new Error('Access denied');
    return response.json();
}
```

### Checklist

- [ ] **SEC-001**: All API endpoints have authentication checks (`@login_required`, middleware)
- [ ] **SEC-002**: Authorization checks verify user permissions before data access
- [ ] **SEC-003**: Direct object references use unpredictable identifiers (UUIDs, not sequential IDs)
- [ ] **SEC-004**: Authorization logic is centralized and reusable (decorators, middleware)
- [ ] **SEC-005**: Default deny policy implemented (explicit allow lists, not deny lists)
- [ ] **SEC-006**: CORS policy restricts allowed origins (no `*` wildcards in production)
- [ ] **SEC-007**: Rate limiting implemented on sensitive endpoints
- [ ] **SEC-008**: Log all access control failures for monitoring
- [ ] **SEC-009**: Disable directory listing on web servers
- [ ] **SEC-010**: JWT/session tokens invalidated on logout

---

## A02:2021 - Cryptographic Failures

### Description
Previously known as "Sensitive Data Exposure," this focuses on failures related to cryptography which often lead to exposure of sensitive data.

### Detection Methods
- Scan for hardcoded secrets in code/config
- Check TLS/SSL configuration (use SSL Labs, testssl.sh)
- Review encryption algorithms and key management
- Verify secure storage of passwords and sensitive data
- Check for data transmitted over unencrypted channels

### Prevention Patterns

```python
# BAD: Weak password hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD: Strong password hashing with bcrypt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verification
if bcrypt.checkpw(password.encode(), stored_hash):
    # Password correct
```

```python
# BAD: Hardcoded secret
SECRET_KEY = "my-secret-key-12345"

# GOOD: Environment-based secrets
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
```

```python
# GOOD: Encrypt sensitive data at rest
from cryptography.fernet import Fernet

key = os.environ.get('ENCRYPTION_KEY').encode()
cipher = Fernet(key)

# Encrypt
encrypted_data = cipher.encrypt(sensitive_data.encode())

# Decrypt
decrypted_data = cipher.decrypt(encrypted_data).decode()
```

### Checklist

- [ ] **SEC-011**: All data in transit uses TLS 1.2+ (no HTTP, only HTTPS)
- [ ] **SEC-012**: Passwords hashed with bcrypt, scrypt, or Argon2 (min 10 rounds)
- [ ] **SEC-013**: No secrets hardcoded in source code or configuration files
- [ ] **SEC-014**: Secrets managed via environment variables or secure vaults (AWS Secrets Manager, HashiCorp Vault)
- [ ] **SEC-015**: Sensitive data encrypted at rest (database encryption, file encryption)
- [ ] **SEC-016**: Strong encryption algorithms used (AES-256, RSA-2048+)
- [ ] **SEC-017**: Cryptographic keys rotated regularly and stored securely
- [ ] **SEC-018**: No sensitive data in URLs, logs, or error messages
- [ ] **SEC-019**: HTTP Strict Transport Security (HSTS) headers configured
- [ ] **SEC-020**: PII and financial data classified and protected accordingly

---

## A03:2021 - Injection

### Description
Injection flaws, such as SQL, NoSQL, OS command, and LDAP injection occur when untrusted data is sent to an interpreter as part of a command or query.

### Detection Methods
- Static analysis tools (Bandit, SonarQube, Semgrep)
- Dynamic testing with injection payloads
- Code review for parameterized queries
- Test with fuzzing and special characters
- Review all data inputs (forms, APIs, file uploads)

### Prevention Patterns

```python
# BAD: SQL Injection vulnerable
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# GOOD: Parameterized query
user_id = request.args.get('id')
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

```python
# BAD: Command injection vulnerable
filename = request.args.get('file')
os.system(f"cat {filename}")

# GOOD: Use safe alternatives
import subprocess
filename = request.args.get('file')
# Validate and sanitize
if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
    raise ValueError("Invalid filename")
result = subprocess.run(['cat', filename], capture_output=True, check=True)
```

```javascript
// BAD: NoSQL injection vulnerable
db.users.find({ username: req.body.username, password: req.body.password })

// GOOD: Validate input types
const { username, password } = req.body;
if (typeof username !== 'string' || typeof password !== 'string') {
    throw new Error('Invalid input');
}
db.users.find({ username: username, password: password })
```

```python
# GOOD: ORM usage (prevents SQL injection)
from sqlalchemy import select
stmt = select(User).where(User.id == user_id)
user = session.execute(stmt).scalar_one()
```

### Checklist

- [ ] **SEC-021**: All SQL queries use parameterized statements or prepared statements
- [ ] **SEC-022**: ORM frameworks used where possible (SQLAlchemy, Django ORM)
- [ ] **SEC-023**: Input validation applied to all user inputs (allowlist preferred)
- [ ] **SEC-024**: No direct OS command execution with user input
- [ ] **SEC-025**: LDAP, XML, and NoSQL queries properly sanitized
- [ ] **SEC-026**: Template engines auto-escape output (Jinja2 autoescape)
- [ ] **SEC-027**: Static analysis tools integrated into CI/CD pipeline
- [ ] **SEC-028**: Web Application Firewall (WAF) configured for injection protection
- [ ] **SEC-029**: Database accounts use least privilege principle
- [ ] **SEC-030**: Server-side input validation (never trust client-side only)

---

## A04:2021 - Insecure Design

### Description
A new category focusing on risks related to design and architectural flaws. Requires more use of threat modeling, secure design patterns, and reference architectures.

### Detection Methods
- Threat modeling sessions (STRIDE, PASTA)
- Architecture security review
- Design pattern analysis
- Abuse case development
- Security requirements review

### Prevention Patterns

```python
# BAD: No rate limiting or account lockout
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_username(request.form['username'])
    if user and user.check_password(request.form['password']):
        login_user(user)
        return redirect('/dashboard')
    return "Invalid credentials", 401

# GOOD: Rate limiting and account lockout
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    username = request.form['username']
    user = User.get_by_username(username)

    # Check account lockout
    if user and user.is_locked():
        return "Account locked. Try again later.", 403

    if user and user.check_password(request.form['password']):
        user.reset_failed_attempts()
        login_user(user)
        return redirect('/dashboard')

    if user:
        user.increment_failed_attempts()
    return "Invalid credentials", 401
```

```python
# GOOD: Secure password reset flow
import secrets
from datetime import datetime, timedelta

def request_password_reset(email):
    user = User.get_by_email(email)
    if not user:
        # Don't reveal if user exists
        return "If email exists, reset link sent"

    # Generate secure token
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)

    user.set_reset_token(token, expiry)
    send_reset_email(user.email, token)

    return "If email exists, reset link sent"

def reset_password(token, new_password):
    user = User.get_by_reset_token(token)
    if not user or user.reset_token_expired():
        return "Invalid or expired token", 400

    user.set_password(new_password)
    user.clear_reset_token()
    user.invalidate_all_sessions()  # Log out all devices
    return "Password reset successful"
```

### Checklist

- [ ] **SEC-031**: Threat modeling conducted for critical features
- [ ] **SEC-032**: Security requirements defined in specification phase
- [ ] **SEC-033**: Defense in depth strategy implemented (multiple layers)
- [ ] **SEC-034**: Secure design patterns used (least privilege, fail secure, separation of duties)
- [ ] **SEC-035**: Rate limiting on authentication, registration, password reset
- [ ] **SEC-036**: Account lockout policy after failed login attempts
- [ ] **SEC-037**: Password reset tokens single-use and time-limited (1 hour max)
- [ ] **SEC-038**: Critical operations require re-authentication
- [ ] **SEC-039**: Business logic abuse cases identified and mitigated
- [ ] **SEC-040**: Security reviewed in design phase (not just implementation)

---

## A05:2021 - Security Misconfiguration

### Description
Security misconfiguration is the most commonly seen issue, often resulting from insecure default configurations, incomplete setups, or verbose error messages.

### Detection Methods
- Security scanning tools (Nessus, OpenVAS)
- Configuration review checklists
- Automated compliance scanning
- Penetration testing
- Review error handling and logging

### Prevention Patterns

```python
# BAD: Debug mode in production
app = Flask(__name__)
app.config['DEBUG'] = True  # Never in production!

# GOOD: Environment-aware configuration
import os
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
app.config['TESTING'] = False
```

```python
# BAD: Verbose error messages
@app.errorhandler(500)
def internal_error(error):
    return str(error), 500  # Exposes stack traces

# GOOD: Generic error messages
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}", exc_info=True)
    return "An internal error occurred. Please try again later.", 500
```

```yaml
# GOOD: Docker security configuration
# docker-compose.yml
services:
  app:
    image: myapp:latest
    read_only: true  # Read-only filesystem
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    user: "1000:1000"  # Non-root user
```

```nginx
# GOOD: Secure Nginx configuration
# Remove server version
server_tokens off;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;

# TLS configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
```

### Checklist

- [ ] **SEC-041**: Debug mode disabled in production environments
- [ ] **SEC-042**: Default credentials changed on all systems and services
- [ ] **SEC-043**: Unnecessary features, ports, and services disabled
- [ ] **SEC-044**: Error messages don't reveal sensitive information (stack traces, paths)
- [ ] **SEC-045**: Security headers configured (CSP, X-Frame-Options, HSTS)
- [ ] **SEC-046**: Server version information hidden (Server header removed)
- [ ] **SEC-047**: File upload directories have execution disabled
- [ ] **SEC-048**: Automated security scanning in CI/CD pipeline
- [ ] **SEC-049**: Cloud storage buckets not publicly accessible (S3, GCS)
- [ ] **SEC-050**: Regular dependency and configuration audits performed

---

## A06:2021 - Vulnerable and Outdated Components

### Description
Using components with known vulnerabilities can undermine application defenses and enable attacks. This includes libraries, frameworks, and other software modules.

### Detection Methods
- Dependency scanning (npm audit, pip-audit, Snyk, Dependabot)
- SBOM (Software Bill of Materials) generation
- CVE database monitoring
- Version tracking
- License compliance checks

### Prevention Patterns

```json
// GOOD: Package.json with specific versions
{
  "dependencies": {
    "express": "4.18.2",
    "helmet": "7.0.0"
  },
  "devDependencies": {
    "eslint": "8.45.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

```python
# GOOD: requirements.txt with version pinning
Flask==2.3.2
SQLAlchemy==2.0.19
cryptography==41.0.3
requests==2.31.0
```

```yaml
# GOOD: Dependabot configuration
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

```bash
# GOOD: Regular security audits in CI/CD
#!/bin/bash
# In CI pipeline

# Python dependencies
pip-audit --requirement requirements.txt

# Node dependencies
npm audit --audit-level=high

# Container scanning
trivy image myapp:latest
```

### Checklist

- [ ] **SEC-051**: Dependency inventory maintained (SBOM generated)
- [ ] **SEC-052**: All dependencies from official, trusted sources only
- [ ] **SEC-053**: Automated vulnerability scanning (Dependabot, Snyk, pip-audit)
- [ ] **SEC-054**: Security advisories monitored for used components
- [ ] **SEC-055**: Dependencies updated regularly (monthly at minimum)
- [ ] **SEC-056**: Unused dependencies removed from project
- [ ] **SEC-057**: Version pinning used in production dependencies
- [ ] **SEC-058**: Security patches applied within SLA (critical: 7 days, high: 30 days)
- [ ] **SEC-059**: Container base images updated regularly
- [ ] **SEC-060**: End-of-life (EOL) components identified and replaced

---

## A07:2021 - Identification and Authentication Failures

### Description
Previously known as "Broken Authentication," this category includes confirmation of user identity, authentication, and session management failures.

### Detection Methods
- Authentication flow testing
- Session management review
- Password policy verification
- Brute force attack testing
- Session fixation testing

### Prevention Patterns

```python
# GOOD: Secure session configuration
from flask import Flask, session
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Session(app)
```

```python
# GOOD: Multi-factor authentication
import pyotp

def enable_2fa(user):
    secret = pyotp.random_base32()
    user.set_2fa_secret(secret)
    totp = pyotp.TOTP(secret)
    qr_uri = totp.provisioning_uri(user.email, issuer_name="MyApp")
    return qr_uri

def verify_2fa(user, token):
    if not user.has_2fa_enabled():
        return False
    totp = pyotp.TOTP(user.get_2fa_secret())
    return totp.verify(token, valid_window=1)

@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user and user.has_2fa_enabled():
        session['pending_2fa_user_id'] = user.id
        return redirect('/verify-2fa')
    elif user:
        login_user(user)
        return redirect('/dashboard')
    return "Invalid credentials", 401
```

```python
# GOOD: Password strength validation
import re

def validate_password(password):
    """
    Enforce NIST 800-63B password guidelines
    """
    errors = []

    # Minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    # Maximum length (prevent DoS)
    if len(password) > 128:
        errors.append("Password must be less than 128 characters")

    # Check against common passwords
    if password.lower() in load_common_passwords():
        errors.append("Password is too common")

    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        errors.append("Password contains too many repeated characters")

    return len(errors) == 0, errors
```

```python
# GOOD: Secure session regeneration
from flask import session
import secrets

@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        # Regenerate session ID to prevent fixation
        old_session_data = dict(session)
        session.clear()
        session.update(old_session_data)
        session['user_id'] = user.id
        session['csrf_token'] = secrets.token_hex(32)
        session.permanent = True

        login_user(user)
        return redirect('/dashboard')
    return "Invalid credentials", 401
```

### Checklist

- [ ] **SEC-061**: Multi-factor authentication (MFA) available for sensitive accounts
- [ ] **SEC-062**: Password complexity requirements enforced (min 8 chars, no common passwords)
- [ ] **SEC-063**: Credential stuffing protection (rate limiting, CAPTCHA)
- [ ] **SEC-064**: Session IDs regenerated on login/privilege change
- [ ] **SEC-065**: Session timeout implemented (idle: 30 min, absolute: 8 hours)
- [ ] **SEC-066**: Secure session cookies (Secure, HttpOnly, SameSite flags)
- [ ] **SEC-067**: No session IDs in URLs
- [ ] **SEC-068**: Password reset flow secure (token-based, time-limited)
- [ ] **SEC-069**: Account enumeration prevented (generic error messages)
- [ ] **SEC-070**: Authentication logs monitored for suspicious activity

---

## A08:2021 - Software and Data Integrity Failures

### Description
This focuses on code and infrastructure that does not protect against integrity violations, such as using plugins from untrusted sources or insecure CI/CD pipelines.

### Detection Methods
- Code signing verification
- Dependency integrity checks (SRI, checksums)
- CI/CD pipeline security audit
- Supply chain analysis
- Update mechanism review

### Prevention Patterns

```html
<!-- GOOD: Subresource Integrity (SRI) for CDN resources -->
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous">
</script>
```

```python
# GOOD: Verify package integrity
import hashlib

def verify_package_integrity(package_path, expected_hash):
    """Verify downloaded package matches expected hash"""
    sha256_hash = hashlib.sha256()
    with open(package_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    actual_hash = sha256_hash.hexdigest()
    if actual_hash != expected_hash:
        raise ValueError(f"Package integrity check failed: {actual_hash} != {expected_hash}")
    return True
```

```yaml
# GOOD: Signed commits enforcement
# .github/workflows/verify-commits.yml
name: Verify Signed Commits
on: [pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Verify all commits are signed
        run: |
          for commit in $(git rev-list ${{ github.event.pull_request.base.sha }}..${{ github.sha }}); do
            if ! git verify-commit $commit; then
              echo "Commit $commit is not signed"
              exit 1
            fi
          done
```

```python
# GOOD: Secure deserialization
import json

# BAD: Using pickle with untrusted data
# data = pickle.loads(untrusted_input)  # NEVER DO THIS

# GOOD: Use JSON for untrusted data
def safe_deserialize(untrusted_input):
    try:
        data = json.loads(untrusted_input)
        # Validate structure
        if not isinstance(data, dict):
            raise ValueError("Expected dict")
        return data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")
```

```yaml
# GOOD: CI/CD pipeline security
# .github/workflows/secure-pipeline.yml
name: Secure Build Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v3

      - name: Verify dependencies
        run: |
          pip-audit --requirement requirements.txt
          npm audit --audit-level=high

      - name: SAST scan
        uses: github/codeql-action/analyze@v2

      - name: Build with verification
        run: |
          python -m build
          # Verify build artifacts
          sha256sum dist/*
```

### Checklist

- [ ] **SEC-071**: Digital signatures verified for software updates
- [ ] **SEC-072**: Dependencies downloaded from trusted repositories only
- [ ] **SEC-073**: Subresource Integrity (SRI) used for CDN resources
- [ ] **SEC-074**: CI/CD pipeline secured (signed commits, protected branches)
- [ ] **SEC-075**: No deserialization of untrusted data (avoid pickle, use JSON)
- [ ] **SEC-076**: Code signing implemented for releases
- [ ] **SEC-077**: Supply chain security tools integrated (SLSA, Sigstore)
- [ ] **SEC-078**: Auto-update mechanisms use secure channels (HTTPS, signed)
- [ ] **SEC-079**: Build reproducibility verified
- [ ] **SEC-080**: Artifact integrity checksums published and verified

---

## A09:2021 - Security Logging and Monitoring Failures

### Description
Insufficient logging and monitoring, coupled with missing or ineffective integration with incident response, allows attackers to persist and pivot to more systems.

### Detection Methods
- Log coverage analysis
- SIEM integration testing
- Alert validation
- Log retention verification
- Incident response drills

### Prevention Patterns

```python
# GOOD: Comprehensive security logging
import logging
from datetime import datetime

# Configure security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Log to file and SIEM
file_handler = logging.FileHandler('/var/log/app/security.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
))
security_logger.addHandler(file_handler)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    user = User.get_by_username(username)

    if user and user.check_password(request.form['password']):
        security_logger.info(
            f"AUTHENTICATION_SUCCESS | user={username} | ip={ip_address} | "
            f"user_agent={user_agent}"
        )
        login_user(user)
        return redirect('/dashboard')

    security_logger.warning(
        f"AUTHENTICATION_FAILURE | user={username} | ip={ip_address} | "
        f"user_agent={user_agent} | reason=invalid_credentials"
    )
    return "Invalid credentials", 401
```

```python
# GOOD: Log critical security events
def log_security_event(event_type, details):
    """Log security-relevant events"""
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': getattr(current_user, 'id', None),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'details': details
    }
    security_logger.info(json.dumps(event))

# Usage examples
log_security_event('PRIVILEGE_ESCALATION_ATTEMPT', {
    'target_role': 'admin',
    'current_role': current_user.role
})

log_security_event('PASSWORD_CHANGE', {
    'user_id': user.id,
    'method': '2fa_verified'
})

log_security_event('SUSPICIOUS_ACTIVITY', {
    'activity': 'multiple_failed_2fa',
    'count': 5,
    'timeframe': '5_minutes'
})
```

```python
# GOOD: Sanitize logs to prevent injection
import re

def sanitize_log_input(value):
    """Prevent log injection attacks"""
    if not isinstance(value, str):
        value = str(value)
    # Remove newlines and control characters
    value = re.sub(r'[\n\r\t]', '', value)
    # Truncate long values
    return value[:200]

def safe_log(message, **kwargs):
    sanitized_kwargs = {
        k: sanitize_log_input(v) for k, v in kwargs.items()
    }
    security_logger.info(message, extra=sanitized_kwargs)
```

```python
# GOOD: Monitoring and alerting
from prometheus_client import Counter, Histogram

# Metrics
login_attempts = Counter('login_attempts_total', 'Total login attempts', ['status'])
auth_duration = Histogram('auth_duration_seconds', 'Authentication duration')

@app.route('/login', methods=['POST'])
@auth_duration.time()
def login():
    username = request.form.get('username')
    user = User.get_by_username(username)

    if user and user.check_password(request.form['password']):
        login_attempts.labels(status='success').inc()
        login_user(user)
        return redirect('/dashboard')

    login_attempts.labels(status='failure').inc()
    return "Invalid credentials", 401
```

### Checklist

- [ ] **SEC-081**: All authentication events logged (success and failure)
- [ ] **SEC-082**: Authorization failures logged with context
- [ ] **SEC-083**: Input validation failures logged
- [ ] **SEC-084**: Security-relevant events logged (password change, privilege escalation)
- [ ] **SEC-085**: Logs include sufficient context (timestamp, user, IP, action)
- [ ] **SEC-086**: Logs protected from tampering (write-only, integrity checks)
- [ ] **SEC-087**: Log retention policy defined and enforced (min 90 days)
- [ ] **SEC-088**: Automated alerts for suspicious patterns
- [ ] **SEC-089**: Integration with SIEM or centralized logging
- [ ] **SEC-090**: No sensitive data in logs (passwords, tokens, PII)

---

## A10:2021 - Server-Side Request Forgery (SSRF)

### Description
SSRF flaws occur when a web application fetches a remote resource without validating the user-supplied URL. It allows an attacker to coerce the application to send requests to unexpected destinations.

### Detection Methods
- URL validation testing
- Internal network scanning attempts
- Cloud metadata endpoint testing
- DNS rebinding tests
- Protocol handler enumeration

### Prevention Patterns

```python
# BAD: No URL validation
import requests

@app.route('/fetch-url')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # DANGEROUS!
    return response.content

# GOOD: Strict URL validation
import requests
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = ['http', 'https']
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
BLOCKED_IPS = [
    ipaddress.ip_network('10.0.0.0/8'),      # Private
    ipaddress.ip_network('172.16.0.0/12'),   # Private
    ipaddress.ip_network('192.168.0.0/16'),  # Private
    ipaddress.ip_network('127.0.0.0/8'),     # Loopback
    ipaddress.ip_network('169.254.0.0/16'),  # Link-local
]

def is_safe_url(url):
    """Validate URL to prevent SSRF"""
    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ALLOWED_SCHEMES:
            return False, "Invalid scheme"

        # Check domain allowlist
        if parsed.hostname not in ALLOWED_DOMAINS:
            return False, "Domain not allowed"

        # Resolve and check IP
        import socket
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))

        for blocked_network in BLOCKED_IPS:
            if ip in blocked_network:
                return False, "IP address not allowed"

        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/fetch-url')
def fetch_url():
    url = request.args.get('url')
    is_safe, error = is_safe_url(url)

    if not is_safe:
        security_logger.warning(f"SSRF_ATTEMPT | url={url} | error={error}")
        return "Invalid URL", 400

    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        return response.content
    except requests.RequestException as e:
        return "Failed to fetch URL", 500
```

```python
# GOOD: Cloud metadata protection
import requests

# Block cloud metadata endpoints
METADATA_ENDPOINTS = [
    '169.254.169.254',  # AWS, Azure, GCP
    'metadata.google.internal',
    '100.100.100.200',  # Alibaba Cloud
]

def fetch_external_resource(url):
    parsed = urlparse(url)

    # Block metadata endpoints
    if parsed.hostname in METADATA_ENDPOINTS:
        raise ValueError("Access to metadata endpoint blocked")

    # Use network isolation
    response = requests.get(
        url,
        timeout=5,
        allow_redirects=False,
        # Add custom DNS resolver that blocks private IPs
    )
    return response
```

```python
# GOOD: Webhook URL validation
def validate_webhook_url(url):
    """Validate webhook URLs before using"""
    is_safe, error = is_safe_url(url)
    if not is_safe:
        raise ValueError(f"Invalid webhook URL: {error}")

    # Test the webhook
    try:
        response = requests.post(
            url,
            json={'test': True},
            timeout=5,
            allow_redirects=False,
            headers={'User-Agent': 'MyApp-Webhook/1.0'}
        )

        if response.status_code not in [200, 201, 204]:
            raise ValueError(f"Webhook test failed: {response.status_code}")

        return True
    except requests.RequestException as e:
        raise ValueError(f"Webhook test failed: {e}")
```

```dockerfile
# GOOD: Network isolation with Docker
# docker-compose.yml
services:
  web:
    image: myapp:latest
    networks:
      - public
      - internal

  worker:
    image: myapp-worker:latest
    networks:
      - internal  # No public network access
    environment:
      - ALLOWED_HOSTS=api.example.com

networks:
  public:
    driver: bridge
  internal:
    driver: bridge
    internal: true  # No external connectivity
```

### Checklist

- [ ] **SEC-091**: URL allowlist enforced for external requests
- [ ] **SEC-092**: Private IP addresses blocked (RFC 1918, loopback, link-local)
- [ ] **SEC-093**: Cloud metadata endpoints blocked (169.254.169.254)
- [ ] **SEC-094**: URL scheme restricted (only http/https, no file://, gopher://)
- [ ] **SEC-095**: DNS rebinding protection implemented
- [ ] **SEC-096**: HTTP redirects disabled or validated
- [ ] **SEC-097**: Network segmentation isolates external request functionality
- [ ] **SEC-098**: Request timeouts enforced (max 5-10 seconds)
- [ ] **SEC-099**: Response size limits enforced
- [ ] **SEC-100**: SSRF attempts logged and monitored

---

## Security Testing Checklist

### Pre-Deployment Security Verification

- [ ] All SEC-001 through SEC-100 items reviewed and addressed
- [ ] SAST (Static Analysis) tools run and issues resolved
- [ ] DAST (Dynamic Analysis) performed on staging environment
- [ ] Dependency vulnerabilities scanned and patched
- [ ] Penetration testing completed for critical features
- [ ] Security code review conducted by security team
- [ ] Threat model updated and validated
- [ ] Security documentation complete and up-to-date

### Continuous Security Practices

- [ ] Automated security testing in CI/CD pipeline
- [ ] Security metrics tracked and reported
- [ ] Incident response plan tested quarterly
- [ ] Security training completed by development team
- [ ] Third-party security audit scheduled annually
- [ ] Bug bounty program or responsible disclosure policy active

---

## Usage Guidelines

### During Specification Phase
1. Review relevant OWASP categories for your feature
2. Add security requirements to spec using SEC-xxx IDs
3. Document threat model and security assumptions
4. Define security acceptance criteria

### During Planning Phase
1. Map implementation tasks to SEC-xxx requirements
2. Identify security testing needs
3. Plan security code review touchpoints
4. Allocate time for security hardening

### During Implementation Phase
1. Use code examples from this checklist
2. Check off completed items as you implement
3. Write security tests for each requirement
4. Document security decisions and trade-offs

### During Review Phase
1. Verify all SEC-xxx requirements tested
2. Ensure security logging implemented
3. Validate no sensitive data exposure
4. Confirm configuration hardening complete

---

## Additional Resources

- **OWASP Top 10**: <https://owasp.org/www-project-top-ten/>
- **OWASP Cheat Sheets**: <https://cheatsheetseries.owasp.org/>
- **CWE Top 25**: <https://cwe.mitre.org/top25/>
- **NIST Cybersecurity Framework**: <https://www.nist.gov/cyberframework>
- **SANS Top 25**: <https://www.sans.org/top25-software-errors/>

---

**Version**: 1.0
**Last Updated**: 2025-01-03
**Based on**: OWASP Top 10 2021
