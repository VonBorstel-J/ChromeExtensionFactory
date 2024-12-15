# /backend/routes/payments_routes.py
from flask import Blueprint, request, jsonify
from auth import token_required
from models import User, db
from config import Config
import stripe

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/subscribe', methods=['POST'])
@token_required
def subscribe(current_user):
    data = request.get_json()
    tier = data.get("tier")
    payment_confirmation = data.get("payment_confirmation")

    if tier not in ["pro", "enterprise"]:
        return jsonify({"error": "Invalid tier selected"}), 400

    if not payment_confirmation:
        return jsonify({"error": "Payment confirmation is required"}), 400

    # Here you would verify the payment with Stripe or another payment gateway.
    # Assuming success for demonstration:
    payment_valid = True

    if payment_valid:
        current_user.subscription_tier = tier
        db.session.commit()
        return jsonify({"message": "Subscription updated successfully", "tier": tier}), 200
    else:
        return jsonify({"error": "Payment validation failed"}), 402
