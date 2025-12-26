"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
E-Commerce Microservices Application with Distributed Tracing
6 Microservices: Auth, Product, Order, Payment, Loyalty, Policy
"""

import os
import json
import logging
import secrets
from datetime import datetime
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class StructuredLogger:
    """Structured logger that emits JSON logs for Splunk ingestion"""
    
    def __init__(self, service_name, splunk_url='http://localhost:8088'):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.splunk_url = splunk_url
    
    def log(self, level, message, correlation_id, user_id=None, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "level": level,
            "message": message,
            "correlation_id": correlation_id,
            "user_id": user_id,
            **kwargs
        }
        
        # Log to console
        self.logger.info(json.dumps(log_entry))
        
        # Send to Splunk
        try:
            requests.post(
                f"{self.splunk_url}/services/collector/event",
                json={'event': log_entry},
                timeout=1
            )
        except:
            pass  # Don't let logging failures break the app
        
        return log_entry

# Initialize Flask apps
auth_service = Flask('auth_service')
auth_service.secret_key = secrets.token_hex(16)
auth_logger = StructuredLogger('auth-service')

product_service = Flask('product_service')
product_logger = StructuredLogger('product-service')

order_service = Flask('order_service')
order_logger = StructuredLogger('order-service')

payment_service = Flask('payment_service')
payment_logger = StructuredLogger('payment-service')

loyalty_service = Flask('loyalty_service')
loyalty_logger = StructuredLogger('loyalty-service')

policy_service = Flask('policy_service')
policy_logger = StructuredLogger('policy-service')

# Mock databases
users_db = {
    "user1@test.com": {
        "password": generate_password_hash("password123"),
        "name": "Regular Shopper",
        "user_type": "regular"
    },
    "user2@test.com": {
        "password": generate_password_hash("password123"),
        "name": "Loyalty Member",
        "user_type": "loyalty"
    },
    "user3@test.com": {
        "password": generate_password_hash("password123"),
        "name": "Policy Reader",
        "user_type": "policy_reader"
    },
    "user4@test.com": {
        "password": generate_password_hash("password123"),
        "name": "Order Checker",
        "user_type": "order_checker"
    },
    "user5@test.com": {
        "password": generate_password_hash("password123"),
        "name": "Premium Buyer",
        "user_type": "premium"
    }
}

products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Phone", "price": 699.99, "stock": 15},
    {"id": 3, "name": "Tablet", "price": 399.99, "stock": 20}
]

orders_db = {}
loyalty_points_db = {
    "user2@test.com": 5000,
    "user5@test.com": 10000
}

# Decorator to extract correlation ID
def with_correlation_id(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
        request.correlation_id = correlation_id
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTH SERVICE ====================
@auth_service.route('/health', methods=['GET'])
def auth_health():
    return jsonify({"status": "healthy", "service": "auth"}), 200

@auth_service.route('/api/auth/login', methods=['POST'])
@with_correlation_id
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        correlation_id = request.correlation_id
        
        auth_logger.log('INFO', 'Login attempt', correlation_id, email, endpoint='/api/auth/login')
        
        if email not in users_db:
            auth_logger.log('WARN', 'Login failed - user not found', correlation_id, email)
            return jsonify({"error": "Invalid credentials"}), 401
        
        user = users_db[email]
        if not check_password_hash(user['password'], password):
            auth_logger.log('WARN', 'Login failed - invalid password', correlation_id, email)
            return jsonify({"error": "Invalid credentials"}), 401
        
        token = secrets.token_hex(16)
        
        auth_logger.log('INFO', 'Login successful', correlation_id, email, 
                       user_type=user['user_type'], token=token)
        
        return jsonify({
            "token": token,
            "user": {
                "email": email,
                "name": user['name'],
                "type": user['user_type']
            },
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        auth_logger.log('ERROR', f'Login error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

# ==================== PRODUCT SERVICE ====================
@product_service.route('/health', methods=['GET'])
def product_health():
    return jsonify({"status": "healthy", "service": "product"}), 200

@product_service.route('/api/products/search', methods=['GET'])
@with_correlation_id
def search_products():
    try:
        correlation_id = request.correlation_id
        query = request.args.get('query', '')
        
        product_logger.log('INFO', 'Product search request', correlation_id, 
                          query=query, endpoint='/api/products/search')
        
        results = [p for p in products_db if query.lower() in p['name'].lower()]
        
        product_logger.log('INFO', f'Found {len(results)} products', correlation_id, 
                          results_count=len(results))
        
        return jsonify({
            "products": results,
            "count": len(results),
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        product_logger.log('ERROR', f'Search error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

@product_service.route('/api/products/<int:product_id>', methods=['GET'])
@with_correlation_id
def get_product(product_id):
    try:
        correlation_id = request.correlation_id
        
        product_logger.log('INFO', 'Product details request', correlation_id, 
                          product_id=product_id, endpoint='/api/products/{id}')
        
        product = next((p for p in products_db if p['id'] == product_id), None)
        
        if not product:
            product_logger.log('WARN', 'Product not found', correlation_id, product_id=product_id)
            return jsonify({"error": "Product not found"}), 404
        
        product_logger.log('INFO', 'Product details retrieved', correlation_id, 
                          product_id=product_id, product_name=product['name'])
        
        return jsonify({
            "product": product,
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        product_logger.log('ERROR', f'Get product error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

# ==================== ORDER SERVICE ====================
@order_service.route('/health', methods=['GET'])
def order_health():
    return jsonify({"status": "healthy", "service": "order"}), 200

@order_service.route('/api/orders/history', methods=['GET'])
@with_correlation_id
def get_order_history():
    try:
        correlation_id = request.correlation_id
        user_email = request.headers.get('X-User-Email')
        
        order_logger.log('INFO', 'Order history request', correlation_id, 
                        user_id=user_email, endpoint='/api/orders/history')
        
        user_orders = orders_db.get(user_email, [])
        
        order_logger.log('INFO', f'Retrieved {len(user_orders)} orders', correlation_id, 
                        user_id=user_email, order_count=len(user_orders))
        
        return jsonify({
            "orders": user_orders,
            "count": len(user_orders),
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        order_logger.log('ERROR', f'Order history error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

@order_service.route('/api/orders/create', methods=['POST'])
@with_correlation_id
def create_order():
    try:
        data = request.get_json()
        correlation_id = request.correlation_id
        user_email = request.headers.get('X-User-Email')
        
        order_logger.log('INFO', 'Order creation request', correlation_id, 
                        user_id=user_email, endpoint='/api/orders/create')
        
        order_id = str(uuid.uuid4())
        order = {
            "order_id": order_id,
            "user_email": user_email,
            "items": data.get('items', []),
            "total": data.get('total', 0),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        if user_email not in orders_db:
            orders_db[user_email] = []
        orders_db[user_email].append(order)
        
        order_logger.log('INFO', 'Order created successfully', correlation_id, 
                        user_id=user_email, order_id=order_id, total=order['total'])
        
        return jsonify({
            "order": order,
            "correlation_id": correlation_id
        }), 201
    
    except Exception as e:
        order_logger.log('ERROR', f'Order creation error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

# ==================== PAYMENT SERVICE ====================
@payment_service.route('/health', methods=['GET'])
def payment_health():
    return jsonify({"status": "healthy", "service": "payment"}), 200

@payment_service.route('/api/payment/process', methods=['POST'])
@with_correlation_id
def process_payment():
    try:
        data = request.get_json()
        correlation_id = request.correlation_id
        user_email = request.headers.get('X-User-Email')
        
        payment_logger.log('INFO', 'Payment processing request', correlation_id, 
                          user_id=user_email, endpoint='/api/payment/process')
        
        order_id = data.get('order_id')
        amount = data.get('amount')
        
        payment_id = str(uuid.uuid4())
        
        payment_logger.log('INFO', 'Payment processed successfully', correlation_id, 
                          user_id=user_email, order_id=order_id, 
                          payment_id=payment_id, amount=amount)
        
        return jsonify({
            "payment_id": payment_id,
            "status": "completed",
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        payment_logger.log('ERROR', f'Payment processing error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

# ==================== LOYALTY SERVICE ====================
@loyalty_service.route('/health', methods=['GET'])
def loyalty_health():
    return jsonify({"status": "healthy", "service": "loyalty"}), 200

@loyalty_service.route('/api/loyalty/points', methods=['GET'])
@with_correlation_id
def get_loyalty_points():
    try:
        correlation_id = request.correlation_id
        user_email = request.headers.get('X-User-Email')
        
        loyalty_logger.log('INFO', 'Loyalty points request', correlation_id, 
                          user_id=user_email, endpoint='/api/loyalty/points')
        
        points = loyalty_points_db.get(user_email, 0)
        
        loyalty_logger.log('INFO', f'Loyalty points retrieved: {points}', correlation_id, 
                          user_id=user_email, points=points)
        
        return jsonify({
            "points": points,
            "tier": "Gold" if points > 5000 else "Silver",
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        loyalty_logger.log('ERROR', f'Loyalty points error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

# ==================== POLICY SERVICE ====================
@policy_service.route('/health', methods=['GET'])
def policy_health():
    return jsonify({"status": "healthy", "service": "policy"}), 200

@policy_service.route('/api/policies/<policy_type>', methods=['GET'])
@with_correlation_id
def get_policy(policy_type):
    try:
        correlation_id = request.correlation_id
        
        policy_logger.log('INFO', 'Policy retrieval request', correlation_id, 
                         policy_type=policy_type, endpoint='/api/policies/{type}')
        
        policies = {
            "return": "30-day return policy: You can return any item within 30 days...",
            "privacy": "Privacy policy: We value your privacy and protect your data...",
            "shipping": "Shipping policy: Free shipping on orders over $50..."
        }
        
        policy = policies.get(policy_type, "Policy not found")
        
        policy_logger.log('INFO', 'Policy retrieved', correlation_id, policy_type=policy_type)
        
        return jsonify({
            "policy": policy,
            "type": policy_type,
            "correlation_id": correlation_id
        }), 200
    
    except Exception as e:
        policy_logger.log('ERROR', f'Policy retrieval error: {str(e)}', request.correlation_id)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Microservices module loaded successfully")
    print("Services: Auth, Product, Order, Payment, Loyalty, Policy")