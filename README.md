![Payment-Gateway](https://socialify.git.ci/Nihar16/Payment-Gateway/image?custom_description=Industrial-grade+global+payment+infrastructure.%0AStripe+powered+%E2%80%A2+Multi-currency+%E2%80%A2+Wallets+%E2%80%A2+Fraud+protection.+&description=1&font=Source+Code+Pro&name=1&pattern=Circuit+Board&theme=Dark)

A secure, enterprise-grade payment processing system designed for  establishments with PCI-DSS compliance, advanced fraud prevention, multi-currency support, and integrated wallet solutions.

**[Full Architecture Documentation & API Guide Below]**

## Features

- **PCI-DSS Level 1 Compliant**: Zero card data storage using Stripe Elements tokenization
- **Advanced Fraud Detection**: Stripe Radar integration with ML-powered anomaly detection
- **Multi-Currency Support**: Real-time currency detection and dynamic conversion
- **Digital Wallets**: Apple Pay and Google Pay integration
- **Enterprise Security**: TLS 1.3, Content Security Policy, security headers, rate limiting
- **Global Infrastructure**: CDN optimization, WAF protection, multi-region availability
- **Comprehensive Logging**: Structured logging with error tracking and audit trails

---

## Architecture Overview

### System Architecture Diagram

The payment gateway follows a layered security architecture with multiple defense mechanisms:

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser (HTTPS)                   │
│              payment.html + Stripe Elements                  │
└────────────────────────┬────────────────────────────────────┘
                         │ TLS 1.3 Encrypted
                         ↓
┌─────────────────────────────────────────────────────────────┐
│           Content Delivery & Security Layer                  │
│  Cloudflare CDN + WAF (Bot Detection, DDoS Protection)       │
└────────────────────────┬────────────────────────────────────┘
                         │ Rate Limiting & Geo-blocking
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Cloud Load Balancer & API Gateway                    │
│   AWS ALB/GCP LB/Azure Front Door + API Gateway              │
│     (Authentication, Request Validation, Routing)            │
└────────────────────────┬────────────────────────────────────┘
                         │ Authenticated Requests
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend API Server                              │
│  Node.js/Python (Lambda/Cloud Functions/Azure Functions)    │
│    • Payment Intent Creation    • Webhook Handler            │
│    • Transaction Verification   • Audit Logging              │
└────────────────────────┬────────────────────────────────────┘
                         │ Secure API Call
                         ↓
┌─────────────────────────────────────────────────────────────┐
│           Payment Processor (Stripe)                         │
│  • Tokenization • 3D Secure 2 • Fraud Scoring                │
│  • Multi-currency • Wallet Support                           │
└────────────────────────┬────────────────────────────────────┘
                         │ Encrypted Payment
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Banking Network & Card Networks                      │
│  Visa/Mastercard/Amex (PCI-DSS Compliant)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ Transaction Result
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Fraud Detection & Analytics                          │
│   Stripe Radar + Custom ML Rules + Device Fingerprinting     │
└────────────────────────┬────────────────────────────────────┘
                         │ Verified Transactions
                         ↓
┌─────────────────────────────────────────────────────────────┐
│       Encrypted Database & Audit Trail                       │
│   AWS RDS/GCP Cloud SQL/Azure Database                       │
│   (Transaction logs, compliance records, audit trails)       │
└─────────────────────────────────────────────────────────────┘
```

### Payment Flow Sequence

```
Customer Initiates Payment
         ↓
    ┌────────────────────────────┐
    │  Load payment.html (HTTPS)  │
    │  - Stripe Public Key loaded │
    │  - Stripe Elements created  │
    └────────────┬───────────────┘
                 ↓
    ┌────────────────────────────┐
    │  Customer enters amount &   │
    │  currency (Geo auto-detect) │
    └────────────┬───────────────┘
                 ↓
    ┌────────────────────────────────────────┐
    │  Select payment method:                 │
    │  • Card (Stripe Elements)               │
    │  • Apple Pay / Google Pay               │
    │  • Digital Wallets                      │
    └────────────┬───────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Frontend: POST /create-payment-intent         │
    │  Pass: {amount, currency, email, metadata}     │
    └────────────┬─────────────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Backend: Create Stripe PaymentIntent          │
    │  - Validate inputs & currency                  │
    │  - Configure fraud detection                   │
    │  - Log transaction start                       │
    │  - Return client_secret                        │
    └────────────┬─────────────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Frontend: Confirm Payment with Stripe.js      │
    │  - Tokenize card/wallet (no raw card data)     │
    │  - Send payment_method token only              │
    └────────────┬─────────────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Stripe Processes Payment                      │
    │  - 3D Secure 2 Authentication                  │
    │  - Fraud Detection (Radar ML)                  │
    │  - Bank Settlement                             │
    └────────────┬─────────────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Stripe Webhook Event                          │
    │  /webhook receives payment_intent.succeeded     │
    │  - HMAC signature verification                 │
    │  - Log to database                             │
    │  - Send confirmation email                     │
    └────────────┬─────────────────────────────────┘
                 ↓
    ┌────────────────────────────────────────────────┐
    │  Frontend: Get /transaction/:id status         │
    │  - Show success confirmation                   │
    │  - Display receipt                             │
    └────────────┬─────────────────────────────────┘
                 ↓
    Payment Complete (Audit Trail Logged)

---

## Security Architecture

### Multi-Layer Defense

**Layer 1: Network & Transport** → TLS 1.3, HSTS, Cloudflare WAF, CDN caching
**Layer 2: Frontend** → CSP, Stripe Elements, anti-clickjacking, anti-XSS headers
**Layer 3: API Gateway** → Input validation, rate limiting, CORS, JWT auth
**Layer 4: Backend** → Zero card data, webhook verification, audit logging, idempotency
**Layer 5: Fraud Prevention** → ML scoring, device fingerprinting, IP geolocation, velocity checks
**Layer 6: Data Security** → Encrypted DB, KMS keys, immutable audit trail, GDPR compliance

---

## Global Payment Support

### Multi-Currency Detection & Localization

```

Customer IP → GeoIP2 Lookup → Country Code → Local Currency
   ↓
Real-time Exchange Rates (via Stripe) → Display Local Price
   ↓
Payment Processor handles multi-currency settlement

```

**Supported Currencies**: USD, EUR, GBP, JPY, CAD, AUD, CNY, INR, BRL, and 160+ others

### Wallet Integration

**Apple Pay** (iOS/Safari): Stripe PaymentRequestButton with native Face ID/Touch ID
**Google Pay** (Android/Chrome): Stripe PaymentRequestButton with native fingerprint/PIN

---

## API Endpoints

### Core Operations

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/create-payment-intent` | POST | Create payment intent | API Key |
| `/webhook` | POST | Stripe webhook handler | Signature |
| `/transaction/:id` | GET | Retrieve transaction | API Key |
| `/health` | GET | Service health | None |

### 1. Create Payment Intent

**Request:**

```bash
curl -X POST http://localhost:3000/create-payment-intent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "amount": 10000,
    "currency": "usd",
    "description": "Premium Restaurant Experience",
    "metadata": {
      "order_id": "12345",
      "customer_id": "cust_ABC",
      "restaurant_id": "rest_XYZ"
    },
    "customer_email": "customer@example.com"
  }'
```

**Response:**

```json
{
  "clientSecret": "pi_1A2B3C4D_secret_...",
  "paymentIntentId": "pi_1A2B3C4D",
  "status": "requires_payment_method",
  "amount": 10000,
  "currency": "usd"
}
```

**Node.js Implementation:**

```javascript
app.post('/create-payment-intent', async (req, res) => {
  try {
    const { amount, currency, description, metadata, customer_email } = req.body;

    // Validate inputs
    if (!amount || amount < 50) return res.status(400).json({ error: 'Min $0.50' });
    if (!currency || !['usd', 'eur', 'gbp', 'jpy'].includes(currency)) {
      return res.status(400).json({ error: 'Invalid currency' });
    }

    // Create payment intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount),
      currency: currency.toLowerCase(),
      description: description || 'Luxury service payment',
      metadata: metadata || {},
      customer_email: customer_email,
      automatic_payment_methods: { enabled: true },
      setup_future_usage: 'off_session',
      receipt_email: customer_email,
    });

    res.json({
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id,
      status: paymentIntent.status,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
    });
  } catch (error) {
    console.error('Payment intent failed:', error);
    res.status(500).json({ error: 'Failed to create payment intent' });
  }
});
```

**Python Implementation:**

```python
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')

    # Validate
    if not amount or amount < 50:
        return jsonify({'error': 'Min $0.50'}), 400
    if currency.lower() not in ['usd', 'eur', 'gbp', 'jpy']:
        return jsonify({'error': 'Invalid currency'}), 400

    # Create intent
    payment_intent = stripe.PaymentIntent.create(
        amount=int(amount),
        currency=currency.lower(),
        description=data.get('description', 'Luxury service payment'),
        metadata=data.get('metadata', {}),
        customer_email=data.get('customer_email'),
        automatic_payment_methods={'enabled': True},
        setup_future_usage='off_session',
        receipt_email=data.get('customer_email'),
    )

    return jsonify({
        'clientSecret': payment_intent.client_secret,
        'paymentIntentId': payment_intent.id,
        'status': payment_intent.status,
        'amount': payment_intent.amount,
        'currency': payment_intent.currency,
    })
```

### 2. Webhook Handler

**Request (from Stripe):**

```
POST /webhook HTTP/1.1
Stripe-Signature: t=1614556800,v1=abcdef123456...

{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_1A2B3C4D",
      "status": "succeeded",
      "amount": 10000,
      "currency": "usd"
    }
  }
}
```

**Node.js Implementation:**

```javascript
app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const secret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, secret);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  try {
    switch (event.type) {
      case 'payment_intent.succeeded': {
        const pi = event.data.object;
        console.log(`✓ Payment ${pi.id} succeeded`);
        await updateTransaction(pi.id, 'succeeded');
        await sendConfirmationEmail(pi);
        break;
      }
      case 'payment_intent.payment_failed': {
        const pi = event.data.object;
        console.log(`✗ Payment ${pi.id} failed`);
        await updateTransaction(pi.id, 'failed');
        break;
      }
      case 'charge.refunded': {
        const charge = event.data.object;
        console.log(`↩ Charge ${charge.id} refunded`);
        await processRefund(charge);
        break;
      }
    }
  } catch (error) {
    return res.status(500).json({ error: 'Webhook processing failed' });
  }

  res.json({ received: true });
});
```

**Python Implementation:**

```python
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('stripe-signature')
    secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({'error': 'Signature verification failed'}), 400

    try:
        if event['type'] == 'payment_intent.succeeded':
            pi = event['data']['object']
            app.logger.info(f'✓ Payment {pi.id} succeeded')
            update_transaction(pi.id, 'succeeded')
            send_confirmation_email(pi)

        elif event['type'] == 'payment_intent.payment_failed':
            pi = event['data']['object']
            app.logger.warning(f'✗ Payment {pi.id} failed')
            update_transaction(pi.id, 'failed')

    except Exception as e:
        app.logger.error(f'Error: {str(e)}')
        return jsonify({'error': 'Processing failed'}), 500

    return jsonify({'received': True})
```

### 3. Get Transaction Status

**Request:**

```bash
curl http://localhost:3000/transaction/pi_1A2B3C4D \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "id": "pi_1A2B3C4D",
  "status": "succeeded",
  "amount": 10000,
  "currency": "usd",
  "created": 1614556800,
  "customer_email": "customer@example.com",
  "charges": {
    "total_count": 1,
    "data": [{ "id": "ch_1A2B3C4D", "status": "succeeded" }]
  }
}
```

**Implementation:**

```javascript
app.get('/transaction/:id', async (req, res) => {
  try {
    const pi = await stripe.paymentIntents.retrieve(req.params.id);
    res.json({
      id: pi.id,
      status: pi.status,
      amount: pi.amount,
      currency: pi.currency,
      created: pi.created,
      customer_email: pi.receipt_email,
      charges: {
        total_count: pi.charges.total_count,
        data: pi.charges.data.map(c => ({ id: c.id, status: c.status })),
      },
    });
  } catch (error) {
    res.status(404).json({ error: 'Transaction not found' });
  }
});
```

### 4. Frontend Integration (payment.html)

## Deployment

### AWS Lambda (Serverless Framework)

```bash
npm install -g serverless
serverless deploy --stage prod
```

Refer to `serverless.yml` for configuration options.

### Docker Production

```bash
docker build -t luxury-payment-api:latest .
docker run -d \
  -p 3000:3000 \
  --env-file .env \
  --name payment-api \
  luxury-payment-api:latest
```

### Cloud Platforms

| Platform | Method | Notes |
|----------|--------|-------|
| **AWS** | Lambda + API Gateway | Use serverless.yml; auto-scaling included |
| **Azure** | Container Apps / Functions | Use Dockerfile or Azure Functions Runtime |
| **GCP** | Cloud Run | Containerized; billing per request |

## Security

### Best Practices Implemented

- ✅ **Zero Card Storage**: All card data tokenized via Stripe Elements
- ✅ **Encryption**: TLS 1.3 for all data in transit
- ✅ **CSP Headers**: Strict Content Security Policy to prevent XSS attacks
- ✅ **Rate Limiting**: Automatic request throttling per client
- ✅ **Webhook Verification**: Stripe signature validation on all webhooks
- ✅ **Input Validation**: Sanitization of all user inputs
- ✅ **Error Masking**: Generic error responses prevent information leakage
- ✅ **Audit Logging**: Immutable transaction history

### Security Configuration

Enable webhook verification in your handler:

```javascript
const event = stripe.webhooks.constructEvent(
  req.rawBody,
  req.headers['stripe-signature'],
  process.env.STRIPE_WEBHOOK_SECRET
);
```

## Monitoring & Observability

- **Health Checks**: Service availability monitoring every 30 seconds
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Error Tracking**: Integration-ready for Sentry or similar APM tools
- **Stripe Dashboard**: Real-time transaction monitoring and dispute management
- **Metrics**: Request latency, error rates, and success rates tracked

## Development

### Testing

Run the test suite (if configured):

```bash
npm test
```

### Code Quality

- Follow security best practices at every step
- Test all payment flows end-to-end
- Keep dependencies up to date
- Use conventional commits for clarity

### Contributing

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Commit changes with conventional commits
3. Test thoroughly before submitting PR
4. Update documentation as needed
5. Ensure all security checks pass

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Webhook signature invalid` | Verify `STRIPE_WEBHOOK_SECRET` in `.env` |
| `Port 3000 already in use` | Change `PORT` in `.env` or kill existing process |
| `CORS errors` | Check CORS headers in handler; ensure client origin is whitelisted |
| `Payment intent creation fails` | Verify Stripe API keys and network connectivity |

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

For issues, questions, or security concerns, please open an issue on the repository or contact the development team.

The application will be available at `http://localhost:3000`

## 📖 API Documentation

### Authentication

All API requests require authentication using Bearer tokens:

```http
Authorization: Bearer <your_api_token>
```

### Core Endpoints

#### Process Payment

```http
POST /api/v1/payments
Content-Type: application/json

{
  "amount": 1000,
  "currency": "USD",
  "payment_method": {
    "type": "card",
    "card": {
      "number": "4242424242424242",
      "exp_month": 12,
      "exp_year": 2025,
      "cvc": "123"
    }
  },
  "description": "Payment for Order #12345"
}
```

#### Retrieve Payment

```http
GET /api/v1/payments/{payment_id}
```

#### List Payments

```http
GET /api/v1/payments?limit=10&offset=0
```

#### Refund Payment

```http
POST /api/v1/payments/{payment_id}/refund
Content-Type: application/json

{
  "amount": 500,
  "reason": "requested_by_customer"
}
```

For complete API documentation, visit `/api/docs` when the server is running.

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Merchant      │────│  Payment        │────│  Payment        │
│   Application   │    │  Gateway API    │    │  Processors     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Database      │
                       │   & Security    │
                       └─────────────────┘
```

### Data Flow

1. **Payment Request**: Merchant sends payment request to gateway
2. **Validation**: Gateway validates request parameters and merchant credentials
3. **Processing**: Payment is processed through selected payment provider
4. **Response**: Transaction result is returned to merchant
5. **Webhook**: Status updates are sent via webhooks (if configured)

## 🔒 Security Features

- **PCI DSS Compliance**: Follows Payment Card Industry security standards
- **Data Encryption**: All sensitive data is encrypted at rest and in transit
- **Tokenization**: Card details are tokenized to prevent data exposure
- **Rate Limiting**: API rate limiting to prevent abuse
- **Fraud Detection**: Machine learning-based fraud detection algorithms
- **Audit Logging**: Comprehensive logging of all transactions and API calls

## 🧪 Testing

### Run Tests

```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run with coverage
npm run test:coverage
```

### Test Payment Cards

For testing purposes, use these card numbers:

- **Visa**: 4242424242424242
- **Mastercard**: 5555555555554444
- **American Express**: 378282246310005
- **Declined**: 4000000000000002

## 📊 Monitoring and Analytics

### Health Check

```http
GET /health
```

### Metrics Endpoint

```http
GET /metrics
```

### Dashboard

Access the admin dashboard at `/dashboard` to view:

- Transaction volume and success rates
- Revenue analytics
- Error rates and system performance
- Payment method distribution
- Geographic transaction data

## 🚀 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t payment-gateway .

# Run container
docker run -p 3000:3000 --env-file .env payment-gateway
```

### Docker Compose

```bash
docker-compose up -d
```

### Production Deployment

1. Set environment to production: `NODE_ENV=production`
2. Use production database credentials
3. Enable SSL/TLS certificates
4. Configure load balancers and scaling
5. Set up monitoring and alerting

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

### Development Guidelines

- Follow the existing code style and conventions
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting PR
- Keep commits atomic and well-documented

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🗺️ Roadmap

### Upcoming Features

- [ ] Mobile SDK development
- [ ] Cryptocurrency payment support
- [ ] Advanced fraud detection with AI/ML
- [ ] Multi-tenant architecture
- [ ] GraphQL API support
- [ ] Real-time transaction streaming
- [ ] Enhanced analytics dashboard
- [ ] International payment methods

### Version History

- **V1.0** - Initial release with core payment processing.
- **V1.1** - Multi-currency support.
- **V1.2** - Optimized for mobile phones and Tablets

**⚠️ Important**: This is a payment processing system. Always ensure compliance with local regulations and PCI DSS requirements when handling payment data.
