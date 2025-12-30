# Smoke Test Landing Page

## Purpose

Generate conversion-optimized, premium landing pages for validating demand before building. Modern design inspired by Stripe, Linear, and Vercel with glassmorphism effects, micro-interactions, and confetti celebrations.

## Landing Page Structure

### Premium Landing Page Template

```html
<!-- smoke-test-landing.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PRODUCT_NAME}} - {{TAGLINE}}</title>

  <!-- SEO -->
  <meta name="description" content="{{META_DESCRIPTION}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{PRODUCT_NAME}} - {{TAGLINE}}">
  <meta property="og:description" content="{{META_DESCRIPTION}}">
  <meta property="og:image" content="{{OG_IMAGE_URL}}">
  <meta property="og:type" content="website">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{PRODUCT_NAME}} - {{TAGLINE}}">
  <meta name="twitter:description" content="{{META_DESCRIPTION}}">
  <meta name="twitter:image" content="{{OG_IMAGE_URL}}">

  <!-- Analytics -->
  <script defer data-domain="{{DOMAIN}}" src="https://plausible.io/js/script.js"></script>

  <style>
    /* ========================================
       CSS VARIABLES — DESIGN TOKENS
       ======================================== */
    :root {
      /* Dark mode (default) */
      --color-bg: #0a0a0f;
      --color-surface: #12121a;
      --color-surface-elevated: #1a1a24;
      --color-text: #ffffff;
      --color-text-secondary: rgba(255, 255, 255, 0.7);
      --color-text-tertiary: rgba(255, 255, 255, 0.5);
      --color-border: rgba(255, 255, 255, 0.08);
      --color-border-strong: rgba(255, 255, 255, 0.15);

      /* Primary color */
      --color-primary: {{PRIMARY_COLOR}};
      --color-primary-rgb: {{PRIMARY_COLOR_RGB}};

      /* Gradient palette */
      --gradient-1: #667eea;
      --gradient-2: #764ba2;
      --gradient-3: #f093fb;
      --gradient-4: #f5576c;

      /* Semantic colors */
      --color-success: #22c55e;
      --color-success-bg: rgba(34, 197, 94, 0.15);

      /* Typography */
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --text-display: clamp(2.5rem, 5vw, 3.5rem);
      --text-h2: 1.5rem;
      --text-body-lg: 1.25rem;
      --text-body: 1rem;
      --text-sm: 0.875rem;
      --text-xs: 0.75rem;

      /* Spacing */
      --space-1: 0.25rem;
      --space-2: 0.5rem;
      --space-3: 0.75rem;
      --space-4: 1rem;
      --space-5: 1.25rem;
      --space-6: 1.5rem;
      --space-8: 2rem;
      --space-10: 2.5rem;
      --space-12: 3rem;
      --space-16: 4rem;
      --space-20: 5rem;

      /* Border radius */
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --radius-full: 9999px;

      /* Shadows */
      --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
      --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.25);
      --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.35);
      --glass-shadow:
        0 0 0 1px var(--color-border),
        0 4px 24px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);

      /* Motion */
      --duration-fast: 100ms;
      --duration-normal: 200ms;
      --duration-slow: 300ms;
      --ease-out: cubic-bezier(0, 0, 0.2, 1);
      --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Light mode */
    @media (prefers-color-scheme: light) {
      :root {
        --color-bg: #fafafa;
        --color-surface: #ffffff;
        --color-surface-elevated: #ffffff;
        --color-text: #111827;
        --color-text-secondary: #6b7280;
        --color-text-tertiary: #9ca3af;
        --color-border: rgba(0, 0, 0, 0.08);
        --color-border-strong: rgba(0, 0, 0, 0.15);
        --glass-shadow:
          0 0 0 1px var(--color-border),
          0 4px 24px rgba(0, 0, 0, 0.1),
          inset 0 1px 0 rgba(255, 255, 255, 0.8);
      }
    }

    /* ========================================
       BASE RESET & TYPOGRAPHY
       ======================================== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: var(--font-sans);
      font-size: var(--text-body);
      line-height: 1.6;
      color: var(--color-text);
      background: var(--color-bg);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }

    /* Screen reader only */
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    /* ========================================
       HERO SECTION
       ======================================== */
    .hero {
      position: relative;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: var(--space-8) var(--space-6);
      overflow: hidden;
    }

    /* Gradient background layer */
    .hero-bg {
      position: absolute;
      inset: 0;
      overflow: hidden;
      pointer-events: none;
    }

    /* Animated gradient orbs */
    .gradient-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.5;
      animation: float 20s ease-in-out infinite;
    }

    .gradient-orb-1 {
      width: 600px;
      height: 600px;
      background: radial-gradient(circle, var(--gradient-1) 0%, transparent 70%);
      top: -200px;
      left: -150px;
    }

    .gradient-orb-2 {
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, var(--gradient-3) 0%, transparent 70%);
      bottom: -150px;
      right: -100px;
      animation-delay: -10s;
    }

    @keyframes float {
      0%, 100% { transform: translate(0, 0) scale(1); }
      25% { transform: translate(30px, -30px) scale(1.05); }
      50% { transform: translate(-20px, 20px) scale(0.95); }
      75% { transform: translate(20px, 10px) scale(1.02); }
    }

    /* Grid pattern overlay */
    .grid-pattern {
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 60px 60px;
      mask-image: radial-gradient(ellipse 80% 50% at 50% 0%, black 70%, transparent 100%);
    }

    @media (prefers-color-scheme: light) {
      .grid-pattern {
        background-image:
          linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
      }
      .gradient-orb { opacity: 0.3; }
    }

    /* Hero content */
    .hero-content {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 640px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    /* Brand / Logo */
    .brand {
      display: flex;
      align-items: center;
      gap: var(--space-3);
      margin-bottom: var(--space-10);
      animation: fade-in-down 0.6s var(--ease-out) forwards;
    }

    .logo {
      font-size: var(--text-body-lg);
      font-weight: 700;
      color: var(--color-text);
      letter-spacing: -0.02em;
    }

    .badge {
      font-size: var(--text-xs);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: var(--space-1) var(--space-3);
      background: linear-gradient(135deg, var(--gradient-1), var(--gradient-3));
      color: white;
      border-radius: var(--radius-full);
    }

    @keyframes fade-in-down {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Headline stack */
    .headline-stack {
      margin-bottom: var(--space-10);
      animation: fade-in-up 0.6s var(--ease-out) 0.1s forwards;
      opacity: 0;
    }

    @keyframes fade-in-up {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .headline {
      font-size: var(--text-display);
      font-weight: 700;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: var(--space-4);
      background: linear-gradient(135deg, var(--color-text) 0%, var(--color-text-secondary) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .subheadline {
      font-size: var(--text-body-lg);
      color: var(--color-text-secondary);
      max-width: 480px;
      margin: 0 auto;
    }

    /* ========================================
       GLASSMORPHISM SIGNUP CARD
       ======================================== */
    .signup-card {
      width: 100%;
      padding: var(--space-8);
      border-radius: var(--radius-xl);
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--color-border);
      box-shadow: var(--glass-shadow);
      margin-bottom: var(--space-6);
      animation: card-appear 0.6s var(--ease-out) 0.2s forwards;
      opacity: 0;
      transform: translateY(20px);
    }

    @media (prefers-color-scheme: light) {
      .signup-card {
        background: rgba(255, 255, 255, 0.8);
      }
    }

    @keyframes card-appear {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Inner glow on hover */
    .signup-card::before {
      content: '';
      position: absolute;
      inset: -1px;
      border-radius: inherit;
      background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.1) 0%,
        transparent 50%
      );
      opacity: 0;
      transition: opacity var(--duration-slow) var(--ease-out);
      pointer-events: none;
      z-index: -1;
    }

    .signup-card:hover::before {
      opacity: 1;
    }

    /* Form layout */
    .signup-form {
      display: flex;
      flex-direction: column;
      gap: var(--space-4);
    }

    .form-row {
      display: flex;
      gap: var(--space-3);
      flex-wrap: wrap;
    }

    @media (min-width: 480px) {
      .form-row {
        flex-wrap: nowrap;
      }
    }

    /* Input wrapper */
    .input-wrapper {
      position: relative;
      flex: 1;
      min-width: 200px;
    }

    input[type="email"] {
      width: 100%;
      padding: var(--space-4) var(--space-5);
      font-size: var(--text-body);
      font-family: inherit;
      color: var(--color-text);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      outline: none;
      transition:
        border-color var(--duration-fast) var(--ease-out),
        background var(--duration-fast) var(--ease-out),
        box-shadow var(--duration-fast) var(--ease-out);
    }

    @media (prefers-color-scheme: light) {
      input[type="email"] {
        background: rgba(0, 0, 0, 0.03);
      }
    }

    input[type="email"]::placeholder {
      color: var(--color-text-tertiary);
    }

    input[type="email"]:hover {
      border-color: var(--color-border-strong);
      background: rgba(255, 255, 255, 0.07);
    }

    input[type="email"]:focus {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
    }

    /* Focus ring animation */
    .input-focus-ring {
      position: absolute;
      inset: -4px;
      border-radius: calc(var(--radius-lg) + 4px);
      border: 2px solid var(--color-primary);
      opacity: 0;
      transform: scale(0.98);
      transition:
        opacity var(--duration-fast) var(--ease-out),
        transform var(--duration-fast) var(--ease-spring);
      pointer-events: none;
    }

    input[type="email"]:focus ~ .input-focus-ring {
      opacity: 0.5;
      transform: scale(1);
    }

    /* Hint text */
    .hint {
      font-size: var(--text-sm);
      color: var(--color-text-tertiary);
      text-align: center;
    }

    /* ========================================
       CTA BUTTON
       ======================================== */
    .cta-button {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: var(--space-4) var(--space-6);
      font-size: var(--text-body);
      font-weight: 600;
      font-family: inherit;
      color: white;
      background: linear-gradient(135deg, var(--color-primary), var(--gradient-2));
      border: none;
      border-radius: var(--radius-lg);
      cursor: pointer;
      overflow: hidden;
      min-width: 160px;
      flex-shrink: 0;
      transition:
        transform var(--duration-normal) var(--ease-out),
        box-shadow var(--duration-normal) var(--ease-out);
      box-shadow:
        0 2px 8px rgba(var(--color-primary-rgb), 0.3),
        0 0 0 0 rgba(var(--color-primary-rgb), 0);
    }

    /* Shine sweep effect */
    .cta-button::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        105deg,
        transparent 20%,
        rgba(255, 255, 255, 0.25) 50%,
        transparent 80%
      );
      transform: translateX(-100%);
      transition: transform 0.6s var(--ease-out);
    }

    .cta-button:hover {
      transform: translateY(-2px);
      box-shadow:
        0 6px 20px rgba(var(--color-primary-rgb), 0.4),
        0 0 40px rgba(var(--color-primary-rgb), 0.15);
    }

    .cta-button:hover::before {
      transform: translateX(100%);
    }

    .cta-button:active {
      transform: translateY(0) scale(0.98);
      transition-duration: var(--duration-fast);
    }

    .cta-button:focus-visible {
      outline: 2px solid var(--color-primary);
      outline-offset: 3px;
    }

    /* Loading state */
    .cta-button.loading {
      pointer-events: none;
    }

    .cta-button.loading .button-text {
      opacity: 0;
    }

    .cta-button.loading .button-spinner {
      opacity: 1;
    }

    .button-text {
      transition: opacity var(--duration-fast);
    }

    .button-spinner {
      position: absolute;
      width: 20px;
      height: 20px;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-top-color: white;
      border-radius: 50%;
      opacity: 0;
      transition: opacity var(--duration-fast);
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* ========================================
       SUCCESS STATE
       ======================================== */
    .success-state {
      display: none;
      text-align: center;
      padding: var(--space-6);
    }

    .success-state.show {
      display: block;
      animation: success-appear 0.5s var(--ease-spring) forwards;
    }

    .signup-form.hide {
      display: none;
    }

    @keyframes success-appear {
      0% { opacity: 0; transform: scale(0.9); }
      50% { transform: scale(1.02); }
      100% { opacity: 1; transform: scale(1); }
    }

    .success-icon {
      width: 64px;
      height: 64px;
      margin: 0 auto var(--space-4);
      background: var(--color-success-bg);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .success-icon svg {
      width: 32px;
      height: 32px;
      color: var(--color-success);
      stroke-dasharray: 50;
      stroke-dashoffset: 50;
      animation: checkmark-draw 0.4s var(--ease-out) 0.2s forwards;
    }

    @keyframes checkmark-draw {
      to { stroke-dashoffset: 0; }
    }

    .success-message {
      font-size: var(--text-body-lg);
      font-weight: 500;
      color: var(--color-text);
    }

    /* Confetti container */
    .confetti-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: hidden;
      z-index: 100;
    }

    .confetti {
      position: absolute;
      width: 10px;
      height: 10px;
      border-radius: 2px;
      animation: confetti-fall 2.5s var(--ease-out) forwards;
    }

    @keyframes confetti-fall {
      0% {
        opacity: 1;
        transform: translateY(0) rotate(0deg) scale(1);
      }
      100% {
        opacity: 0;
        transform: translateY(100vh) rotate(720deg) scale(0.5);
      }
    }

    /* ========================================
       SOCIAL PROOF
       ======================================== */
    .social-proof {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-3);
      margin-bottom: var(--space-16);
      animation: fade-in-up 0.6s var(--ease-out) 0.4s forwards;
      opacity: 0;
    }

    .proof-text {
      font-size: var(--text-sm);
      color: var(--color-text-tertiary);
    }

    .avatar-stack {
      display: flex;
    }

    .avatar {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 2px solid var(--color-bg);
      background: linear-gradient(135deg, var(--gradient-1), var(--gradient-3));
      margin-left: -8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: var(--text-xs);
      font-weight: 600;
      color: white;
    }

    .avatar:first-child {
      margin-left: 0;
    }

    /* ========================================
       FEATURES SECTION
       ======================================== */
    .features {
      padding: var(--space-20) var(--space-6);
      background: var(--color-bg);
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--space-6);
      max-width: 960px;
      margin: 0 auto;
    }

    .feature-card {
      padding: var(--space-6);
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      transition:
        transform var(--duration-normal) var(--ease-out),
        border-color var(--duration-normal) var(--ease-out),
        box-shadow var(--duration-normal) var(--ease-out);
      opacity: 0;
      animation: feature-appear 0.5s var(--ease-out) forwards;
    }

    .feature-card:nth-child(1) { animation-delay: 0.1s; }
    .feature-card:nth-child(2) { animation-delay: 0.2s; }
    .feature-card:nth-child(3) { animation-delay: 0.3s; }

    @keyframes feature-appear {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .feature-card:hover {
      border-color: var(--color-border-strong);
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }

    .feature-icon {
      width: 48px;
      height: 48px;
      margin-bottom: var(--space-4);
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, var(--color-primary), var(--gradient-3));
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .feature-icon svg {
      width: 24px;
      height: 24px;
      color: white;
    }

    .feature-title {
      font-size: var(--text-h2);
      font-weight: 600;
      margin-bottom: var(--space-2);
    }

    .feature-description {
      color: var(--color-text-secondary);
      line-height: 1.6;
    }

    /* ========================================
       TRUST SECTION
       ======================================== */
    .trust-section {
      padding: var(--space-12) var(--space-6);
      background: var(--color-surface);
      border-top: 1px solid var(--color-border);
      border-bottom: 1px solid var(--color-border);
    }

    .trust-badges {
      display: flex;
      justify-content: center;
      gap: var(--space-8);
      flex-wrap: wrap;
      max-width: 640px;
      margin: 0 auto;
    }

    .trust-item {
      display: flex;
      align-items: center;
      gap: var(--space-2);
      color: var(--color-text-secondary);
      font-size: var(--text-sm);
    }

    .trust-icon {
      width: 20px;
      height: 20px;
      color: var(--color-success);
    }

    /* ========================================
       FOOTER
       ======================================== */
    .footer {
      padding: var(--space-8) var(--space-6);
      text-align: center;
    }

    .footer-text {
      font-size: var(--text-sm);
      color: var(--color-text-tertiary);
      margin-bottom: var(--space-2);
    }

    .footer-links {
      display: flex;
      justify-content: center;
      gap: var(--space-4);
      font-size: var(--text-sm);
    }

    .footer-links a {
      color: var(--color-text-secondary);
      text-decoration: none;
      transition: color var(--duration-fast);
    }

    .footer-links a:hover {
      color: var(--color-text);
    }

    .footer-links span {
      color: var(--color-text-tertiary);
    }

    /* ========================================
       ACCESSIBILITY — REDUCED MOTION
       ======================================== */
    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }

      .gradient-orb {
        animation: none;
      }

      .cta-button::before {
        display: none;
      }

      .confetti-container {
        display: none;
      }

      .signup-card,
      .headline-stack,
      .brand,
      .social-proof,
      .feature-card {
        opacity: 1;
        transform: none;
      }
    }
  </style>
</head>
<body>
  <!-- Hero Section -->
  <section class="hero" role="banner">
    <!-- Background -->
    <div class="hero-bg" aria-hidden="true">
      <div class="gradient-orb gradient-orb-1"></div>
      <div class="gradient-orb gradient-orb-2"></div>
      <div class="grid-pattern"></div>
    </div>

    <!-- Content -->
    <div class="hero-content">
      <!-- Brand -->
      <header class="brand">
        <span class="logo">{{PRODUCT_NAME}}</span>
        <span class="badge">Early Access</span>
      </header>

      <!-- Headline -->
      <div class="headline-stack">
        <h1 class="headline">{{HEADLINE}}</h1>
        <p class="subheadline">{{SUBHEADLINE}}</p>
      </div>

      <!-- Signup Card -->
      <div class="signup-card">
        <form class="signup-form" id="signup-form" aria-label="Waitlist signup">
          <div class="form-row">
            <div class="input-wrapper">
              <input
                type="email"
                name="email"
                id="email"
                placeholder="Enter your email"
                required
                autocomplete="email"
                aria-describedby="email-hint"
              >
              <span class="input-focus-ring" aria-hidden="true"></span>
            </div>
            <button type="submit" class="cta-button">
              <span class="button-text">{{CTA_TEXT}}</span>
              <span class="button-spinner" aria-hidden="true"></span>
            </button>
          </div>
          <p id="email-hint" class="hint">No spam. Unsubscribe anytime.</p>
        </form>

        <div class="success-state" id="success-state" aria-live="polite">
          <div class="success-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <p class="success-message">{{SUCCESS_MESSAGE}}</p>
        </div>
      </div>

      <!-- Social Proof -->
      <div class="social-proof">
        <div class="avatar-stack" aria-label="Early adopters">
          <div class="avatar">A</div>
          <div class="avatar">B</div>
          <div class="avatar">C</div>
          <div class="avatar">+</div>
        </div>
        <span class="proof-text">{{SOCIAL_PROOF}}</span>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features" aria-labelledby="features-heading">
    <h2 id="features-heading" class="sr-only">Key Benefits</h2>
    <div class="features-grid">
      {{#each BENEFITS}}
      <article class="feature-card">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <h3 class="feature-title">{{title}}</h3>
        <p class="feature-description">{{description}}</p>
      </article>
      {{/each}}
    </div>
  </section>

  <!-- Trust Section -->
  <section class="trust-section" aria-label="Trust indicators">
    <div class="trust-badges">
      <div class="trust-item">
        <svg class="trust-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
        <span>256-bit SSL</span>
      </div>
      <div class="trust-item">
        <svg class="trust-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        <span>GDPR Ready</span>
      </div>
      <div class="trust-item">
        <svg class="trust-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 13l4 4L19 7"/>
        </svg>
        <span>No Spam</span>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer" role="contentinfo">
    <p class="footer-text">&copy; {{YEAR}} {{PRODUCT_NAME}}. All rights reserved.</p>
    <nav class="footer-links" aria-label="Legal">
      <a href="{{PRIVACY_URL}}">Privacy</a>
      <span aria-hidden="true">·</span>
      <a href="{{TERMS_URL}}">Terms</a>
    </nav>
  </footer>

  <!-- Confetti container -->
  <div class="confetti-container" id="confetti-container" aria-hidden="true"></div>

  <script>
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Form elements
    const form = document.getElementById('signup-form');
    const submitBtn = form.querySelector('.cta-button');
    const successState = document.getElementById('success-state');
    const confettiContainer = document.getElementById('confetti-container');

    // Form submission handler
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Show loading state
      submitBtn.classList.add('loading');
      submitBtn.disabled = true;

      const email = form.email.value;

      // Track conversion
      if (window.plausible) {
        plausible('Signup', { props: { email_domain: email.split('@')[1] }});
      }

      try {
        // Send to backend
        await fetch('{{SIGNUP_ENDPOINT}}', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, source: 'smoke-test' })
        });
      } catch (err) {
        console.error('Signup error:', err);
      }

      // Show success
      form.classList.add('hide');
      successState.classList.add('show');

      // Trigger confetti
      if (!prefersReducedMotion) {
        createConfetti();
      }
    });

    // Confetti animation
    function createConfetti() {
      const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#22c55e'];
      const confettiCount = 50;

      for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = '-10px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;

        confettiContainer.appendChild(confetti);

        // Remove after animation
        setTimeout(() => confetti.remove(), 3000);
      }
    }

    // Smooth scroll for keyboard focus
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.documentElement.style.scrollBehavior = prefersReducedMotion ? 'auto' : 'smooth';
      }
    });
  </script>
</body>
</html>
```

## Landing Page Variants

### A/B Test Headlines

```yaml
variant_a:
  headline: "{{PROBLEM_FOCUSED_HEADLINE}}"
  # Example: "Stop Wasting Hours on Manual Data Entry"
  hypothesis: "Problem-focused resonates with pain-aware audience"

variant_b:
  headline: "{{SOLUTION_FOCUSED_HEADLINE}}"
  # Example: "Automate Your Data Entry in Minutes"
  hypothesis: "Solution-focused works for solution-aware audience"

variant_c:
  headline: "{{OUTCOME_FOCUSED_HEADLINE}}"
  # Example: "Get 10 Hours Back Every Week"
  hypothesis: "Outcome-focused emphasizes transformation"
```

### CTA Variations

```yaml
cta_variants:
  - "Get Early Access"      # Exclusivity
  - "Join the Waitlist"     # FOMO
  - "Start Free Trial"      # Low risk
  - "See How It Works"      # Curiosity
  - "Get Started Free"      # Zero barrier
  - "Request Demo"          # High-touch for B2B
```

## Configuration Template

```yaml
# smoke-test-config.yaml

product:
  name: "{{PRODUCT_NAME}}"
  tagline: "{{SHORT_TAGLINE}}"
  domain: "example.com"

content:
  headline: "{{PRIMARY_HEADLINE}}"
  subheadline: "{{SUPPORTING_STATEMENT}}"
  cta_text: "Get Early Access"
  success_message: "You're on the list! We'll be in touch soon."
  social_proof: "Join 500+ people on the waitlist"

benefits:
  - title: "{{BENEFIT_1_TITLE}}"
    description: "{{BENEFIT_1_DESCRIPTION}}"
  - title: "{{BENEFIT_2_TITLE}}"
    description: "{{BENEFIT_2_DESCRIPTION}}"
  - title: "{{BENEFIT_3_TITLE}}"
    description: "{{BENEFIT_3_DESCRIPTION}}"

seo:
  meta_description: "{{META_DESCRIPTION_155_CHARS}}"
  og_image: "/og-image.png"

branding:
  primary_color: "#4F46E5"
  primary_color_rgb: "79, 70, 229"  # For rgba() usage
  logo_url: "/logo.svg"

tracking:
  analytics: "plausible"  # or "posthog", "google"
  domain: "example.com"

backend:
  signup_endpoint: "https://api.example.com/waitlist"
  # Or use: "https://formspree.io/f/xxxxx"
  # Or use: "https://getform.io/f/xxxxx"

legal:
  privacy_url: "/privacy"
  terms_url: "/terms"
  year: "2024"
```

## Conversion Benchmarks

```yaml
conversion_benchmarks:
  smoke_test_landing:
    excellent: ">10%"      # Strong signal
    good: "5-10%"          # Proceed with caution
    weak: "2-5%"           # Needs iteration
    fail: "<2%"            # Pivot or abort

  source_expectations:
    paid_ads: "2-5%"       # Cold traffic
    social_organic: "3-8%" # Warm audience
    email_list: "8-15%"    # Hot audience
    product_hunt: "3-7%"   # Mixed intent
```

## Validation Decision Framework

```yaml
validation_criteria:
  green_light:
    - conversion_rate: ">5%"
    - signups: ">100"
    - source_diversity: ">3 channels"
    - organic_sharing: "present"

  yellow_light:
    - conversion_rate: "2-5%"
    - signups: "50-100"
    - recommendation: "iterate messaging, retest"

  red_light:
    - conversion_rate: "<2%"
    - signups: "<50"
    - recommendation: "pivot hypothesis or kill"

decision_tree:
  IF conversion > 5% AND signups > 100:
    DECISION: "GO - Proceed to build MVP"

  ELIF conversion > 5% AND signups < 100:
    DECISION: "EXTEND - Drive more traffic, revalidate"

  ELIF conversion 2-5%:
    DECISION: "ITERATE - Test new headlines/value props"
    max_iterations: 3

  ELSE:
    DECISION: "STOP - Problem hypothesis likely wrong"
```

## Quick Deploy Options

### Option 1: Static (Recommended for speed)

```bash
# Deploy to Vercel in seconds
npx vercel deploy --prod

# Or Netlify
npx netlify deploy --prod

# Or Cloudflare Pages
npx wrangler pages publish ./dist
```

### Option 2: Form Backend Services

```yaml
no_code_backends:
  - service: "Formspree"
    signup_endpoint: "https://formspree.io/f/YOUR_FORM_ID"
    free_tier: "50 submissions/month"

  - service: "Getform"
    signup_endpoint: "https://getform.io/f/YOUR_FORM_ID"
    free_tier: "50 submissions/month"

  - service: "Basin"
    signup_endpoint: "https://usebasin.com/f/YOUR_FORM_ID"
    free_tier: "100 submissions/month"

  - service: "Formcarry"
    signup_endpoint: "https://formcarry.com/s/YOUR_FORM_ID"
    free_tier: "100 submissions/month"
```

### Option 3: Full Analytics Setup

```html
<!-- PostHog (recommended for product analytics) -->
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('{{POSTHOG_KEY}}', {api_host: 'https://app.posthog.com'})
</script>
```

## Success Metrics Dashboard

```yaml
metrics_to_track:
  traffic:
    - unique_visitors
    - page_views
    - bounce_rate
    - time_on_page

  conversion:
    - email_form_views
    - email_submissions
    - conversion_rate
    - by_source_utm

  engagement:
    - scroll_depth
    - cta_clicks
    - exit_intent_triggers

  quality:
    - email_domain_distribution
    - duplicate_submissions
    - fake_email_rate
```

## Design Features

### Visual Highlights
- **Gradient orbs** — animated floating spheres with blur effect
- **Glassmorphism** — backdrop blur card with subtle borders
- **Micro-interactions** — button hover lift, press scale, focus rings
- **Confetti** — celebration animation on successful signup
- **Light/Dark mode** — automatic via `prefers-color-scheme`

### Accessibility
- **Semantic HTML** — proper heading hierarchy, ARIA labels
- **Keyboard navigation** — focus-visible states, tab order
- **Screen reader** — sr-only labels, aria-live regions
- **Reduced motion** — respects `prefers-reduced-motion`

### Performance
- **No external dependencies** — inline CSS/JS only
- **System fonts** — no font loading delay
- **Optimized animations** — GPU-accelerated transforms
- **Target size** — under 35KB total
