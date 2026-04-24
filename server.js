const express = require('express');
const stripe = require('stripe')('sk_test_your_secret_key_replace_me');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Security headers middleware
app.use((req, res, next) => {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    next();
});

// Create payment intent endpoint
app.post('/create-payment-intent', async (req, res) => {
    try {
        const { amount, currency, description, metadata } = req.body;

        // Input validation
        if (!amount || !currency) {
            return res.status(400).json({ error: 'Amount and currency required' });
        }

        if (typeof amount !== 'number' || amount <= 0) {
            return res.status(400).json({ error: 'Invalid amount' });
        }

        // Create payment intent with fraud detection enabled
        const paymentIntent = await stripe.paymentIntents.create({
            amount: amount,
            currency: currency.toLowerCase(),
            description: description || 'Luxury restaurant payment',
            metadata: metadata || {},
            automatic_payment_methods: {
                enabled: true,
            },
            setup_future_usage: 'off_session', // Enable future payments for returning customers
        });

        res.json({ clientSecret: paymentIntent.client_secret });
    } catch (error) {
        console.error('Payment intent creation failed:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Stripe webhook verification endpoint
app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = 'whsec_your_webhook_secret_replace_me'; // Replace with your webhook secret

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
            // TODO: Update your database, send confirmation email, etc.
            // Store transaction details securely
            break;
        case 'payment_intent.payment_failed':
            const failedPayment = event.data.object;
            console.log('PaymentIntent failed:', failedPayment.last_payment_error?.message);
            // TODO: Handle failed payment (notify customer, log for review)
            break;
        case 'payment_method.attached':
            // Handle payment method attachment for future use
            break;
        default:
            console.log(`Unhandled event type ${event.type}`);
    }

    res.json({ received: true });
});

// Transaction status endpoint (for confirmation)
app.get('/transaction/:id', async (req, res) => {
    try {
        const paymentIntent = await stripe.paymentIntents.retrieve(req.params.id);
        res.json({
            id: paymentIntent.id,
            status: paymentIntent.status,
            amount: paymentIntent.amount,
            currency: paymentIntent.currency,
            description: paymentIntent.description,
            created: paymentIntent.created,
        });
    } catch (error) {
        res.status(404).json({ error: 'Transaction not found' });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;
