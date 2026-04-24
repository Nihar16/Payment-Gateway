# Payment Gateway

A secure, enterprise-grade payment processing system designed for luxury restaurants with PCI-DSS compliance, fraud prevention, multi-currency support, and wallet integration.

## Features

- **PCI-DSS Compliant**: Zero card data storage using Stripe Elements
- **Fraud Prevention**: Advanced fraud detection with Stripe Radar
- **Multi-Currency**: Automatic currency detection and conversion
- **Wallet Integration**: Apple Pay, Google Pay support
- **Enterprise Security**: TLS 1.3, CSP, security headers
- **Global Architecture**: CDN, WAF, API Gateway protection

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and security implementation.

## Quick Start

### Prerequisites

- Node.js 18+ or Python 3.8+
- Stripe account with API keys
- Docker (optional)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd payment-gateway
   ```

2. **Environment Setup**

   ```bash
   cp .env.example .env
   # Edit .env with your Stripe keys
   ```

3. **Choose your backend:**

   **Node.js Backend:**

   ```bash
   npm install
   npm start
   ```

   **Python Backend:**

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

   **Docker:**

   ```bash
   docker-compose up --build
   ```

### Stripe Configuration

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from the dashboard
3. Set up webhooks for payment events
4. Configure Radar for fraud prevention

### Testing

The API includes health check endpoints:

- `GET /health` - Service health status

## Deployment

### AWS Lambda (Serverless)

```bash
npm install -g serverless
serverless deploy
```

### Docker Production

```bash
docker build -t payment-api .
docker run -p 3000:3000 --env-file .env payment-api
```

### Cloud Platforms

- **AWS**: Use serverless.yml for Lambda deployment
- **GCP**: Deploy to Cloud Run with Dockerfile
- **Azure**: Use Azure Functions or Container Apps

## Security

- All card data is tokenized and never stored
- TLS 1.3 encryption for all communications
- Content Security Policy prevents XSS attacks
- Rate limiting and fraud detection enabled
- Webhook signature verification

## API Endpoints

- `POST /create-payment-intent` - Create payment intent
- `POST /webhook` - Stripe webhook handler
- `GET /transaction/:id` - Get transaction status
- `GET /health` - Health check

## Frontend Integration

The payment.html file contains the complete frontend implementation with:

- Stripe Elements for secure card input
- Multi-currency support
- Wallet payment options
- Error handling and success confirmation

## Monitoring

- Health checks every 30 seconds
- Structured logging
- Error tracking with Sentry (optional)
- Stripe dashboard monitoring

## Contributing

1. Follow security best practices
2. Test all payment flows
3. Update documentation
4. Use conventional commits

## License

MIT License - see LICENSE file for details

# For Node.js projects

npm install

# For Python projects

pip install -r requirements.txt

# For Java projects

mvn install

```

### 3. Environment Configuration

Create a `.env` file in the root directory and configure the following variables:

```env
# Database Configuration
DATABASE_URL=your_database_connection_string
DATABASE_NAME=payment_gateway_db

# Payment Provider Keys
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret

# Security
JWT_SECRET=your_jwt_secret_key
ENCRYPTION_KEY=your_encryption_key

# Server Configuration
PORT=3000
NODE_ENV=development

# Webhook Endpoints
WEBHOOK_SECRET=your_webhook_secret
```

### 4. Database Setup

```bash
# Create database tables/collections
npm run db:migrate

# Seed initial data (optional)
npm run db:seed
```

### 5. Run the Application

```bash
# Development mode
npm run dev

# Production mode
npm start
```

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
