---
name: global-payment-architecture
description: 'Create a luxury-grade global payment architecture for an existing payment page while preserving the exact UI and layout. Use for enterprise security, PCI-DSS compliance, fraud prevention, multi-currency support, wallet integration, and deployment guidance.'
argument-hint: 'Describe the current payment page and the target payment processor (Stripe, Adyen, etc.).'
user-invocable: true
disable-model-invocation: false
---

# Global Payment Architecture

## When to Use
- Upgrading an existing HTML payment page to luxury-grade, bank-grade security
- Preserving the exact front-end UI while redesigning the backend architecture
- Designing global payment support with multi-currency, wallets, fraud prevention, and bot protection
- Generating secure Stripe Elements integration and backend API examples

## Procedure
1. Review the existing `payment.html` page and preserve its exact UI/UX, layout, styling, and form fields.
2. Define the proposed system architecture:
   - Client Browser → CDN/WAF → Backend API → Payment Processor → Bank Network
   - include CDN, Web Application Firewall, API gateway, secure backend, fraud services, webhook handler, encrypted database, and monitoring
3. Document security requirements:
   - PCI-DSS compliant architecture
   - tokenized payment processing with no card data stored on our servers
   - hosted secure fields using Stripe Elements or equivalent iframe-based card entry
   - Strong Customer Authentication with 3D Secure 2
   - TLS 1.3 encryption and HTTPS-only communication
   - Content Security Policy, XSS/CSRF/clickjacking/injection protection
4. Design fraud prevention and bot protection:
   - machine-learning fraud scoring via Stripe Radar or equivalent
   - device fingerprinting, IP reputation, geo-location mismatch, velocity checks, behavioral anomaly detection
   - Web Application Firewall, bot detection, rate limiting, CAPTCHA/invisible bot protection, API gateway protection
5. Add global currency and localization support:
   - detect user location by IP and browser locale
   - display local currency dynamically
   - support all currencies enabled by the payment processor
   - perform automatic currency conversion at checkout with USD fallback
6. Add wallet and modern payment support:
   - Apple Pay, Google Pay, and digital wallets supported by the processor
   - preserve the same visual experience while adding wallet payment options
7. Provide secure integration examples:
   - frontend HTML integration with Stripe Elements while keeping the existing payment page unchanged
   - backend API examples for Node.js or Python showing payment intent creation, secure token handling, webhook verification, and transaction confirmation
8. Provide deployment and infrastructure recommendations for AWS, GCP, or Azure:
   - CDN/WAF, managed API gateway, encrypted database, secrets management, private subnets, monitoring, and logging
9. Explain how the luxury experience is maintained while implementing bank-grade security:
   - seamless UI, minimal friction, fast performance, modern wallet options, and invisible security layers

## Completion Checks
- The existing payment page UI is preserved exactly
- No raw card data is stored or handled on our servers
- Architecture includes fraud detection, bot protection, and global payment support
- Security headers and best practices are clearly specified
- Deployment options cover AWS, GCP, and Azure
- Backend examples include webhook verification and tokenized payment flow

## Notes
- Keep the skill focused on architecture and security, not on redesigning the page UI.
- If needed, add `references/` or `scripts/` in `.github/skills/global-payment-architecture/` for architecture diagrams or security checklists.
