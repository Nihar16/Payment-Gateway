# Global Payment Architecture for Luxury Restaurant Website

## System Architecture Diagram

```
Client Browser (HTTPS/TLS 1.3)
    ↓ (CDN/WAF Protection)
Cloudflare CDN + WAF
    ↓ (Rate Limiting, Bot Detection)
Load Balancer (AWS ALB/GCP LB/Azure Front Door)
    ↓ (API Gateway Protection)
API Gateway (AWS API Gateway/GCP API Gateway/Azure API Management)
    ↓ (Authentication & Authorization)
Backend API Server (Node.js/Python on AWS Lambda/GCP Cloud Functions/Azure Functions)
    ↓ (Payment Intent Creation)
Stripe/Payment Processor
    ↓ (Tokenized Processing, 3D Secure 2)
Bank Network (PCI-DSS Compliant)
    ↓ (Fraud Detection)
Stripe Radar + Custom Rules
    ↓ (Transaction Logging)
Encrypted Database (AWS RDS/GCP Cloud SQL/Azure Database)
```

## Security Layers

### Frontend Security

- **Content Security Policy**: Implemented in meta tag
- **HTTPS Only**: Enforced via HSTS headers
- **XSS Protection**: CSP prevents inline scripts, external domains
- **CSRF Protection**: Stripe Elements handle secure tokenization
- **Clickjacking Protection**: X-Frame-Options headers

### Backend Security

- **PCI-DSS Compliance**: No card data stored, tokenized processing
- **3D Secure 2**: Strong Customer Authentication
- **Webhook Verification**: HMAC signature validation
- **Rate Limiting**: API Gateway and application-level limits
- **Input Validation**: Sanitize all inputs, prevent injection

### Fraud Prevention

- **Stripe Radar**: ML-based fraud detection
- **Device Fingerprinting**: Browser and device analysis
- **IP Reputation**: Geo-location and IP analysis
- **Velocity Checks**: Prevent card testing attacks
- **Behavioral Analysis**: Transaction pattern monitoring

### Bot & Attack Protection

- **Cloudflare WAF**: Web Application Firewall rules
- **Bot Detection**: Challenge suspicious traffic
- **Rate Limiting**: Per-IP and per-endpoint limits
- **CAPTCHA**: Invisible reCAPTCHA for high-risk actions

## Global Currency & Localization

### Implementation

- **IP Geolocation**: Use MaxMind GeoIP2 or Cloudflare headers
- **Browser Locale**: Fallback to navigator.language
- **Currency Detection**: Map country to local currency
- **Dynamic Display**: Update prices via JavaScript
- **Conversion**: Real-time rates via Stripe or external API
- **Fallback**: Default to USD if detection fails

### Supported Currencies

All Stripe-supported currencies: USD, EUR, GBP, JPY, CAD, AUD, CNY, INR, BRL, RUB, ZAR, SGD, MXN, etc.

## Wallet & Modern Payment Support

### Apple Pay & Google Pay

- **Stripe Payment Request API**: Native wallet integration
- **Secure Elements**: No card data exposure
- **Cross-Platform**: Works on iOS, Android, web

### Implementation

```javascript
// Add to payment.html JavaScript
const paymentRequest = stripe.paymentRequest({
  country: 'US',
  currency: 'usd',
  total: {
    label: 'Premium Product',
    amount: getTotalAmountCents(),
  },
  requestPayerName: true,
  requestPayerEmail: true,
});

const elements = stripe.elements();
const prButton = elements.create('paymentRequestButton', {
  paymentRequest: paymentRequest,
});

paymentRequest.canMakePayment().then(function(result) {
  if (result) {
    prButton.mount('#payment-request-button-element');
    document.getElementById('payment-request-button-element').classList.remove('hidden');
    document.getElementById('wallet-fallback-button').classList.add('hidden');
  }
});
```

## Backend API Examples

### Node.js Backend (server.js)

```javascript
const express = require('express');
const stripe = require('stripe')('sk_test_your_secret_key');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Security headers
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  next();
});

// Create payment intent
app.post('/create-payment-intent', async (req, res) => {
  try {
    const { amount, currency, description, metadata } = req.body;

    // Validate input
    if (!amount || !currency) {
      return res.status(400).json({ error: 'Amount and currency required' });
    }

    // Create payment intent with fraud detection
    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount,
      currency: currency.toLowerCase(),
      description: description,
      metadata: metadata,
      automatic_payment_methods: {
        enabled: true,
      },
      setup_future_usage: 'off_session',
    });

    res.json({ clientSecret: paymentIntent.client_secret });
  } catch (error) {
    console.error('Payment intent creation failed:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Webhook verification
app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = 'whsec_your_webhook_secret';

  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.log(`Webhook signature verification failed.`, err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      console.log('PaymentIntent was successful!');
      // Update database, send confirmation email, etc.
      break;
    case 'payment_method.attached':
      // Handle payment method attachment
      break;
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({ received: true });
});

// Transaction confirmation endpoint
app.get('/transaction/:id', async (req, res) => {
  try {
    const paymentIntent = await stripe.paymentIntents.retrieve(req.params.id);
    res.json({
      id: paymentIntent.id,
      status: paymentIntent.status,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
      description: paymentIntent.description,
    });
  } catch (error) {
    res.status(404).json({ error: 'Transaction not found' });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Python Backend (app.py)

```python
from flask import Flask, request, jsonify
import stripe
import os
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_secret_key')

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Create payment intent
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get('amount')
        currency = data.get('currency')
        description = data.get('description', '')
        metadata = data.get('metadata', {})

        if not amount or not currency:
            raise BadRequest('Amount and currency required')

        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency.lower(),
            description=description,
            metadata=metadata,
            automatic_payment_methods={'enabled': True},
            setup_future_usage='off_session',
        )

        return jsonify({'clientSecret': payment_intent.client_secret})

    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Webhook verification
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print('PaymentIntent was successful!')
        # Update database, send confirmation email, etc.

    return jsonify({'received': True})

# Transaction confirmation
@app.route('/transaction/<payment_intent_id>', methods=['GET'])
def get_transaction(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return jsonify({
            'id': payment_intent.id,
            'status': payment_intent.status,
            'amount': payment_intent.amount,
            'currency': payment_intent.currency,
            'description': payment_intent.description,
        })
    except stripe.error.StripeError:
        return jsonify({'error': 'Transaction not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)
```

## Security Headers & Best Practices

### Server Configuration

- **TLS 1.3**: Enforce modern encryption
- **HSTS**: Force HTTPS connections
- **CSP**: As implemented in HTML meta tag
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.

### Database Security

- **Encryption at Rest**: Use AWS KMS, GCP Cloud KMS, or Azure Key Vault
- **Encryption in Transit**: TLS for all connections
- **Access Control**: Least privilege IAM roles
- **Audit Logging**: Enable database audit logs

## Deployment Recommendations

### AWS Deployment

1. **Frontend**: CloudFront CDN + S3 static hosting
2. **Backend**: API Gateway + Lambda functions
3. **Database**: RDS with encryption
4. **Security**: WAF, Shield, GuardDuty
5. **Monitoring**: CloudWatch, X-Ray

### GCP Deployment

1. **Frontend**: Cloud CDN + Cloud Storage
2. **Backend**: API Gateway + Cloud Functions
3. **Database**: Cloud SQL with CMEK
4. **Security**: Cloud Armor, Security Command Center
5. **Monitoring**: Cloud Monitoring, Cloud Trace

### Azure Deployment

1. **Frontend**: Front Door + Blob Storage
2. **Backend**: API Management + Functions
3. **Database**: Azure Database with TDE
4. **Security**: WAF, Azure Security Center
5. **Monitoring**: Application Insights, Log Analytics

## Luxury User Experience with Bank-Grade Security

### Seamless Experience

- **Zero Friction**: Stripe Elements provide native-feeling inputs
- **Fast Loading**: CDN ensures global low-latency delivery
- **Mobile Optimized**: Responsive design works on all devices
- **Progressive Enhancement**: Wallets appear when supported

### Invisible Security

- **Background Processing**: Fraud detection happens server-side
- **Minimal UI Changes**: Security doesn't alter the visual experience
- **Trust Signals**: Secure badges and SSL indicators
- **Error Handling**: User-friendly error messages without exposing internals

### Performance & Reliability

- **Global CDN**: Content delivered from edge locations
- **Auto-scaling**: Backend scales with demand
- **Failover**: Multi-region deployment for high availability
- **Monitoring**: Real-time alerts for issues

This architecture provides enterprise-grade security while maintaining the luxury user experience through invisible security layers, fast performance, and seamless payment flows.
