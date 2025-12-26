"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Service Runner - Starts all 6 microservices
"""

import sys
import os
from multiprocessing import Process
import importlib.util
import time

def load_module_from_file(file_path, module_name):
    """Dynamically load a Python module from file"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run_service(app, port, service_name):
    """Run a Flask service on specified port"""
    print(f"Starting {service_name} on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    print("\n" + "="*60)
    print("MICROSERVICES LAUNCHER")
    print("="*60 + "\n")
    
    # Load services module
    print("Loading microservices module...")
    services_module = load_module_from_file('ecommerce_services.py', 'ecommerce_services')
    print("✓ Microservices module loaded\n")
    
    # Define services
    services = [
        (services_module.auth_service, 5001, 'Auth Service'),
        (services_module.product_service, 5002, 'Product Service'),
        (services_module.order_service, 5003, 'Order Service'),
        (services_module.payment_service, 5004, 'Payment Service'),
        (services_module.loyalty_service, 5005, 'Loyalty Service'),
        (services_module.policy_service, 5006, 'Policy Service'),
    ]
    
    # Start all services
    processes = []
    for app, port, name in services:
        p = Process(target=run_service, args=(app, port, name))
        p.start()
        processes.append(p)
        print(f"✓ {name} started on port {port}")
        time.sleep(0.5)  # Stagger startup
    
    print("\n" + "="*60)
    print("ALL SERVICES RUNNING")
    print("="*60)
    print("\nService Endpoints:")
    print("  • Auth Service:    http://0.0.0.0:5001")
    print("  • Product Service: http://0.0.0.0:5002")
    print("  • Order Service:   http://0.0.0.0:5003")
    print("  • Payment Service: http://0.0.0.0:5004")
    print("  • Loyalty Service: http://0.0.0.0:5005")
    print("  • Policy Service:  http://0.0.0.0:5006")
    print("\nHealth Checks:")
    print("  • curl http://localhost:5001/health")
    print("  • curl http://localhost:5002/health")
    print("  • (etc for all services)")
    print("\nPress Ctrl+C to stop all services\n")
    
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("SHUTTING DOWN SERVICES")
        print("="*60 + "\n")
        for p in processes:
            p.terminate()
            p.join()
        print("✓ All services stopped cleanly\n")

if __name__ == '__main__':
    main()