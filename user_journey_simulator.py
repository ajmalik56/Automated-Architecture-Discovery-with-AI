"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
User Journey Simulator
Simulates 5 different user journey types through the e-commerce system
"""

import requests
import json
import uuid
import time
from datetime import datetime

class UserJourneySimulator:
    """Simulates different user journeys through the microservices"""
    
    def __init__(self, base_url='http://localhost'):
        self.base_url = base_url
        self.services = {
            'auth': f'{base_url}:5001',
            'product': f'{base_url}:5002',
            'order': f'{base_url}:5003',
            'payment': f'{base_url}:5004',
            'loyalty': f'{base_url}:5005',
            'policy': f'{base_url}:5006'
        }
        self.session = requests.Session()
    
    def make_request(self, service, endpoint, method='GET', data=None, 
                    correlation_id=None, user_email=None):
        """Make HTTP request to a service"""
        try:
            url = f"{self.services[service]}{endpoint}"
            headers = {
                'Content-Type': 'application/json',
                'X-Correlation-ID': correlation_id or str(uuid.uuid4())
            }
            
            if user_email:
                headers['X-User-Email'] = user_email
            
            if method == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=5)
            else:
                response = self.session.get(url, headers=headers, timeout=5)
            
            print(f"  → {method} {endpoint} [{response.status_code}]")
            return response
        
        except Exception as e:
            print(f"  ✗ Error calling {service}{endpoint}: {str(e)}")
            return None
    
    def journey_regular_shopper(self, user_email='user1@test.com', password='password123'):
        """
        Journey 1: Regular Shopper
        Path: Login → Search Products → View Product → Create Order → Process Payment
        """
        correlation_id = str(uuid.uuid4())
        print(f"\n{'='*60}")
        print(f"Journey 1: Regular Shopper")
        print(f"Correlation ID: {correlation_id}")
        print(f"{'='*60}")
        
        # Step 1: Login
        print("Step 1: User Login")
        response = self.make_request('auth', '/api/auth/login', 'POST',
                                    {'email': user_email, 'password': password},
                                    correlation_id)
        if not response or response.status_code != 200:
            print("  ✗ Login failed, stopping journey")
            return None
        
        time.sleep(0.5)
        
        # Step 2: Search Products
        print("Step 2: Search for Products")
        self.make_request('product', '/api/products/search?query=laptop', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 3: View Product Details
        print("Step 3: View Product Details")
        self.make_request('product', '/api/products/1', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 4: Create Order
        print("Step 4: Create Order")
        order_data = {
            'items': [{'product_id': 1, 'quantity': 1, 'price': 999.99}],
            'total': 999.99
        }
        self.make_request('order', '/api/orders/create', 'POST', order_data,
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 5: Process Payment
        print("Step 5: Process Payment")
        payment_data = {
            'order_id': str(uuid.uuid4()),
            'amount': 999.99
        }
        self.make_request('payment', '/api/payment/process', 'POST', payment_data,
                         correlation_id=correlation_id, user_email=user_email)
        
        print(f"✓ Journey Complete: Regular Shopper")
        return correlation_id
    
    def journey_loyalty_member(self, user_email='user2@test.com', password='password123'):
        """
        Journey 2: Loyalty Member
        Path: Login → Check Loyalty Points → Browse Products
        """
        correlation_id = str(uuid.uuid4())
        print(f"\n{'='*60}")
        print(f"Journey 2: Loyalty Member")
        print(f"Correlation ID: {correlation_id}")
        print(f"{'='*60}")
        
        # Step 1: Login
        print("Step 1: User Login")
        response = self.make_request('auth', '/api/auth/login', 'POST',
                                    {'email': user_email, 'password': password},
                                    correlation_id)
        if not response or response.status_code != 200:
            print("  ✗ Login failed, stopping journey")
            return None
        
        time.sleep(0.5)
        
        # Step 2: Check Loyalty Points
        print("Step 2: Check Loyalty Points")
        self.make_request('loyalty', '/api/loyalty/points', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 3: Browse Products
        print("Step 3: Browse Products")
        self.make_request('product', '/api/products/search?query=phone', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        print(f"✓ Journey Complete: Loyalty Member")
        return correlation_id
    
    def journey_policy_reader(self, user_email='user3@test.com', password='password123'):
        """
        Journey 3: Policy Reader
        Path: Login → Read Return Policy → Read Privacy Policy → Read Shipping Policy
        """
        correlation_id = str(uuid.uuid4())
        print(f"\n{'='*60}")
        print(f"Journey 3: Policy Reader")
        print(f"Correlation ID: {correlation_id}")
        print(f"{'='*60}")
        
        # Step 1: Login
        print("Step 1: User Login")
        response = self.make_request('auth', '/api/auth/login', 'POST',
                                    {'email': user_email, 'password': password},
                                    correlation_id)
        if not response or response.status_code != 200:
            print("  ✗ Login failed, stopping journey")
            return None
        
        time.sleep(0.5)
        
        # Step 2: Read Return Policy
        print("Step 2: Read Return Policy")
        self.make_request('policy', '/api/policies/return', 'GET',
                         correlation_id=correlation_id)
        
        time.sleep(0.5)
        
        # Step 3: Read Privacy Policy
        print("Step 3: Read Privacy Policy")
        self.make_request('policy', '/api/policies/privacy', 'GET',
                         correlation_id=correlation_id)
        
        time.sleep(0.5)
        
        # Step 4: Read Shipping Policy
        print("Step 4: Read Shipping Policy")
        self.make_request('policy', '/api/policies/shipping', 'GET',
                         correlation_id=correlation_id)
        
        print(f"✓ Journey Complete: Policy Reader")
        return correlation_id
    
    def journey_order_checker(self, user_email='user4@test.com', password='password123'):
        """
        Journey 4: Order Checker
        Path: Login → Check Order History
        """
        correlation_id = str(uuid.uuid4())
        print(f"\n{'='*60}")
        print(f"Journey 4: Order Checker")
        print(f"Correlation ID: {correlation_id}")
        print(f"{'='*60}")
        
        # Step 1: Login
        print("Step 1: User Login")
        response = self.make_request('auth', '/api/auth/login', 'POST',
                                    {'email': user_email, 'password': password},
                                    correlation_id)
        if not response or response.status_code != 200:
            print("  ✗ Login failed, stopping journey")
            return None
        
        time.sleep(0.5)
        
        # Step 2: Check Order History
        print("Step 2: Check Order History")
        self.make_request('order', '/api/orders/history', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        print(f"✓ Journey Complete: Order Checker")
        return correlation_id
    
    def journey_premium_buyer(self, user_email='user5@test.com', password='password123'):
        """
        Journey 5: Premium Buyer
        Path: Login → Check Loyalty → Search → View Product → Order → Pay → Check Orders
        """
        correlation_id = str(uuid.uuid4())
        print(f"\n{'='*60}")
        print(f"Journey 5: Premium Buyer")
        print(f"Correlation ID: {correlation_id}")
        print(f"{'='*60}")
        
        # Step 1: Login
        print("Step 1: User Login")
        response = self.make_request('auth', '/api/auth/login', 'POST',
                                    {'email': user_email, 'password': password},
                                    correlation_id)
        if not response or response.status_code != 200:
            print("  ✗ Login failed, stopping journey")
            return None
        
        time.sleep(0.5)
        
        # Step 2: Check Loyalty Points
        print("Step 2: Check Loyalty Points")
        self.make_request('loyalty', '/api/loyalty/points', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 3: Search Products
        print("Step 3: Search for Products")
        self.make_request('product', '/api/products/search?query=tablet', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 4: View Product Details
        print("Step 4: View Product Details")
        self.make_request('product', '/api/products/3', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 5: Create Order
        print("Step 5: Create Order")
        order_data = {
            'items': [{'product_id': 3, 'quantity': 1, 'price': 399.99}],
            'total': 399.99
        }
        self.make_request('order', '/api/orders/create', 'POST', order_data,
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 6: Process Payment
        print("Step 6: Process Payment")
        payment_data = {
            'order_id': str(uuid.uuid4()),
            'amount': 399.99
        }
        self.make_request('payment', '/api/payment/process', 'POST', payment_data,
                         correlation_id=correlation_id, user_email=user_email)
        
        time.sleep(0.5)
        
        # Step 7: Check Order History
        print("Step 7: Check Order History")
        self.make_request('order', '/api/orders/history', 'GET',
                         correlation_id=correlation_id, user_email=user_email)
        
        print(f"✓ Journey Complete: Premium Buyer")
        return correlation_id
    
    def run_all_journeys(self):
        """Run all 5 user journeys"""
        print("\n" + "="*60)
        print("USER JOURNEY SIMULATOR")
        print("Running 5 Different User Journeys")
        print("="*60)
        
        correlation_ids = []
        
        # Journey 1: Regular Shopper
        cid1 = self.journey_regular_shopper()
        if cid1:
            correlation_ids.append(('Regular Shopper', cid1))
        
        time.sleep(1)
        
        # Journey 2: Loyalty Member
        cid2 = self.journey_loyalty_member()
        if cid2:
            correlation_ids.append(('Loyalty Member', cid2))
        
        time.sleep(1)
        
        # Journey 3: Policy Reader
        cid3 = self.journey_policy_reader()
        if cid3:
            correlation_ids.append(('Policy Reader', cid3))
        
        time.sleep(1)
        
        # Journey 4: Order Checker
        cid4 = self.journey_order_checker()
        if cid4:
            correlation_ids.append(('Order Checker', cid4))
        
        time.sleep(1)
        
        # Journey 5: Premium Buyer
        cid5 = self.journey_premium_buyer()
        if cid5:
            correlation_ids.append(('Premium Buyer', cid5))
        
        # Save correlation IDs
        output = {
            'timestamp': datetime.utcnow().isoformat(),
            'journeys': [
                {'name': name, 'correlation_id': cid} 
                for name, cid in correlation_ids
            ]
        }
        
        with open('correlation_ids.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n{'='*60}")
        print("ALL JOURNEYS COMPLETE")
        print(f"{'='*60}")
        print(f"\nTotal Journeys: {len(correlation_ids)}")
        print(f"Correlation IDs saved to: correlation_ids.json")
        print(f"\nJourneys completed:")
        for name, cid in correlation_ids:
            print(f"  • {name}: {cid}")
        print(f"\n{'='*60}\n")
        
        return correlation_ids

if __name__ == '__main__':
    simulator = UserJourneySimulator()
    simulator.run_all_journeys()