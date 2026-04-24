from flask import Flask, request, jsonify
import stripe
import os
from werkzeug.exceptions import BadRequest
from datetime import datetime

app = Flask(__name__)

# Initialize Stripe with secret key from environment
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_secret_key_replace_me')

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Create payment intent endpoint
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()

        # Extract and validate required fields
        amount = data.get('amount')
        currency = data.get('currency')
        description = data.get('description', 'Luxury restaurant payment')
        metadata = data.get('metadata', {})

        if not amount or not currency:
            raise BadRequest('Amount and currency are required')

        if not isinstance(amount, int) or amount <= 0:
            raise BadRequest('Amount must be a positive integer (cents)')

        # Create payment intent with enhanced security
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency.lower(),
            description=description,
            metadata=metadata,
            automatic_payment_methods={'enabled': True},
            setup_future_usage='off_session',  # Enable saved payment methods
            # Additional fraud prevention settings
            payment_method_options={
                'card': {
                    'request_three_d_secure': 'automatic',  # Force 3D Secure when required
                }
            }
        )

        return jsonify({'clientSecret': payment_intent.client_secret})

    except stripe.error.StripeError as e:
        app.logger.error(f'Stripe error: {e}')
        return jsonify({'error': str(e)}), 400
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'Internal server error'}), 500

# Stripe webhook verification endpoint
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret_replace_me')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        app.logger.warning('Invalid payload in webhook')
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        app.logger.warning('Invalid signature in webhook')
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    event_type = event['type']
    if event_type == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        app.logger.info(f'PaymentIntent {payment_intent.id} succeeded')
        # TODO: Update database with successful transaction
        # TODO: Send confirmation email to customer
        # TODO: Update inventory or trigger order fulfillment

    elif event_type == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        error_message = payment_intent.get('last_payment_error', {}).get('message', 'Unknown error')
        app.logger.warning(f'PaymentIntent {payment_intent.id} failed: {error_message}')
        # TODO: Handle failed payment (notify customer, log for review)

    elif event_type == 'payment_method.attached':
        payment_method = event['data']['object']
        app.logger.info(f'Payment method {payment_method.id} attached')
        # TODO: Store payment method for future use

    else:
        app.logger.info(f'Unhandled event type: {event_type}')

    return jsonify({'received': True})

# Transaction status endpoint
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
            'created': payment_intent.created,
        })
    except stripe.error.StripeError as e:
        app.logger.warning(f'Transaction {payment_intent_id} not found')
        return jsonify({'error': 'Transaction not found'}), 404

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'luxury-payment-api'
    })

if __name__ == '__main__':
    # In production, use a WSGI server like gunicorn
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 3000))
    )