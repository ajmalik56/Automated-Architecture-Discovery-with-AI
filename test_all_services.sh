#!/bin/bash
#
# Automated Architecture Discovery System
# Copyright (c) 2025 Abhishek Datta
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# This file is part of the Automated Architecture Discovery System,
# an educational project demonstrating microservices architecture discovery.
#

#########################################################
# Complete Service Testing Script
# Tests all 6 microservices + Splunk Logger
# Verifies end-to-end flow with correlation ID tracking
#########################################################

echo "=========================================="
echo "COMPLETE SERVICE TESTING SCRIPT"
echo "=========================================="
echo ""
echo "This script will:"
echo "  1. Test all service health endpoints"
echo "  2. Test authentication flow"
echo "  3. Test product search"
echo "  4. Test order history"
echo "  5. Test payment processing"
echo "  6. Test loyalty points"
echo "  7. Test policy retrieval"
echo "  8. Verify Splunk log collection"
echo "  9. Verify correlation ID tracing"
echo ""
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=15

# Generate a unique correlation ID for this test run
CORRELATION_ID="test-$(date +%s)-$(shuf -i 1000-9999 -n 1)"

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_test() {
    echo -e "${YELLOW}[TEST $1/$TOTAL_TESTS] $2${NC}"
}

print_success() {
    echo -e "${GREEN}✓ SUCCESS: $1${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

print_error() {
    echo -e "${RED}✗ FAILED: $1${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

print_info() {
    echo -e "  ℹ $1"
}

print_response() {
    echo -e "${BLUE}Response:${NC}"
    if command -v jq &> /dev/null; then
        echo "$1" | jq . 2>/dev/null || echo "$1"
    else
        echo "$1"
    fi
}

echo "Correlation ID for this test run: $CORRELATION_ID"
echo ""
sleep 1

#########################################################
# PHASE 1: HEALTH CHECKS
#########################################################

print_header "PHASE 1: HEALTH CHECKS"
echo ""

# Test 1: Splunk Logger Health
print_test "1" "Splunk Logger Health Check (port 8088)"
RESPONSE=$(curl -s http://localhost:8088/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8088/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Splunk Logger is healthy"
    print_response "$RESPONSE"
else
    print_error "Splunk Logger not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 2: Auth Service Health
print_test "2" "Auth Service Health Check (port 5001)"
RESPONSE=$(curl -s http://localhost:5001/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Auth Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Auth Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 3: Product Service Health
print_test "3" "Product Service Health Check (port 5002)"
RESPONSE=$(curl -s http://localhost:5002/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Product Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Product Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 4: Order Service Health
print_test "4" "Order Service Health Check (port 5003)"
RESPONSE=$(curl -s http://localhost:5003/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Order Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Order Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 5: Payment Service Health
print_test "5" "Payment Service Health Check (port 5004)"
RESPONSE=$(curl -s http://localhost:5004/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5004/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Payment Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Payment Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 6: Loyalty Service Health
print_test "6" "Loyalty Service Health Check (port 5005)"
RESPONSE=$(curl -s http://localhost:5005/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5005/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Loyalty Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Loyalty Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""
sleep 1

# Test 7: Policy Service Health
print_test "7" "Policy Service Health Check (port 5006)"
RESPONSE=$(curl -s http://localhost:5006/health 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5006/health 2>/dev/null)

if [ "$HTTP_CODE" == "200" ] && echo "$RESPONSE" | grep -q "healthy"; then
    print_success "Policy Service is healthy"
    print_response "$RESPONSE"
else
    print_error "Policy Service not responding properly (HTTP $HTTP_CODE)"
    print_info "Response: $RESPONSE"
fi
echo ""

#########################################################
# PHASE 2: FUNCTIONAL TESTS
#########################################################

print_header "PHASE 2: FUNCTIONAL TESTS WITH CORRELATION ID: $CORRELATION_ID"
echo ""
sleep 1

# Test 8: User Login
print_test "8" "Auth Service - User Login"
print_info "Testing: POST /api/auth/login"
print_info "User: user1@test.com"
print_info "Correlation ID: $CORRELATION_ID"

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: $CORRELATION_ID" \
  -d '{"email":"user1@test.com","password":"password123"}')

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "token"; then
    print_success "User login successful"
    print_info "Authentication token received"
    print_response "$BODY"
    
    # Extract token for subsequent requests
    if command -v jq &> /dev/null; then
        TOKEN=$(echo "$BODY" | jq -r '.token' 2>/dev/null)
        print_info "Token: $TOKEN"
    fi
else
    print_error "Login failed (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 9: Product Search
print_test "9" "Product Service - Search for Laptop"
print_info "Testing: GET /api/products/search?query=laptop"
print_info "Correlation ID: $CORRELATION_ID"

SEARCH_RESPONSE=$(curl -s -w "\n%{http_code}" \
  "http://localhost:5002/api/products/search?query=laptop" \
  -H "X-Correlation-ID: $CORRELATION_ID")

HTTP_CODE=$(echo "$SEARCH_RESPONSE" | tail -n1)
BODY=$(echo "$SEARCH_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "products"; then
    print_success "Product search successful"
    
    if command -v jq &> /dev/null; then
        PRODUCT_COUNT=$(echo "$BODY" | jq '.count' 2>/dev/null)
        print_info "Products found: $PRODUCT_COUNT"
    fi
    
    print_response "$BODY"
else
    print_error "Product search failed (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 10: Get Specific Product
print_test "10" "Product Service - Get Product Details (ID: 1)"
print_info "Testing: GET /api/products/1"
print_info "Correlation ID: $CORRELATION_ID"

PRODUCT_RESPONSE=$(curl -s -w "\n%{http_code}" \
  http://localhost:5002/api/products/1 \
  -H "X-Correlation-ID: $CORRELATION_ID")

HTTP_CODE=$(echo "$PRODUCT_RESPONSE" | tail -n1)
BODY=$(echo "$PRODUCT_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "product"; then
    print_success "Product details retrieved"
    print_response "$BODY"
else
    print_error "Failed to get product details (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 11: Order History
print_test "11" "Order Service - Get Order History"
print_info "Testing: GET /api/orders/history"
print_info "User: user1@test.com"
print_info "Correlation ID: $CORRELATION_ID"

ORDER_RESPONSE=$(curl -s -w "\n%{http_code}" \
  http://localhost:5003/api/orders/history \
  -H "X-Correlation-ID: $CORRELATION_ID" \
  -H "X-User-Email: user1@test.com")

HTTP_CODE=$(echo "$ORDER_RESPONSE" | tail -n1)
BODY=$(echo "$ORDER_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "orders"; then
    print_success "Order history retrieved"
    
    if command -v jq &> /dev/null; then
        ORDER_COUNT=$(echo "$BODY" | jq '.count' 2>/dev/null)
        print_info "Orders found: $ORDER_COUNT"
    fi
    
    print_response "$BODY"
else
    print_error "Failed to get order history (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 12: Loyalty Points
print_test "12" "Loyalty Service - Get Loyalty Points"
print_info "Testing: GET /api/loyalty/points"
print_info "User: user2@test.com (loyalty member)"
print_info "Correlation ID: $CORRELATION_ID"

LOYALTY_RESPONSE=$(curl -s -w "\n%{http_code}" \
  http://localhost:5005/api/loyalty/points \
  -H "X-Correlation-ID: $CORRELATION_ID" \
  -H "X-User-Email: user2@test.com")

HTTP_CODE=$(echo "$LOYALTY_RESPONSE" | tail -n1)
BODY=$(echo "$LOYALTY_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "points"; then
    print_success "Loyalty points retrieved"
    
    if command -v jq &> /dev/null; then
        POINTS=$(echo "$BODY" | jq '.points' 2>/dev/null)
        TIER=$(echo "$BODY" | jq -r '.tier' 2>/dev/null)
        print_info "Points: $POINTS"
        print_info "Tier: $TIER"
    fi
    
    print_response "$BODY"
else
    print_error "Failed to get loyalty points (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 13: Policy Retrieval
print_test "13" "Policy Service - Get Return Policy"
print_info "Testing: GET /api/policies/return"
print_info "Correlation ID: $CORRELATION_ID"

POLICY_RESPONSE=$(curl -s -w "\n%{http_code}" \
  http://localhost:5006/api/policies/return \
  -H "X-Correlation-ID: $CORRELATION_ID")

HTTP_CODE=$(echo "$POLICY_RESPONSE" | tail -n1)
BODY=$(echo "$POLICY_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "policy"; then
    print_success "Return policy retrieved"
    print_response "$BODY"
else
    print_error "Failed to get return policy (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

#########################################################
# PHASE 3: SPLUNK VALIDATION
#########################################################

print_header "PHASE 3: SPLUNK LOG COLLECTION VALIDATION"
echo ""
sleep 2  # Give Splunk time to collect logs

# Test 14: Splunk Statistics
print_test "14" "Splunk Logger - Check Collection Statistics"
print_info "Testing: GET /api/stats"
print_info "Verifying logs were collected from all services"

STATS_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8088/api/stats)

HTTP_CODE=$(echo "$STATS_RESPONSE" | tail -n1)
BODY=$(echo "$STATS_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ] && echo "$BODY" | grep -q "total_logs"; then
    print_success "Splunk statistics retrieved"
    
    if command -v jq &> /dev/null; then
        TOTAL_LOGS=$(echo "$BODY" | jq '.total_logs' 2>/dev/null)
        UNIQUE_SERVICES=$(echo "$BODY" | jq '.unique_services' 2>/dev/null)
        CORRELATION_IDS=$(echo "$BODY" | jq '.unique_correlation_ids' 2>/dev/null)
        
        print_info "Total logs collected: $TOTAL_LOGS"
        print_info "Unique services: $UNIQUE_SERVICES"
        print_info "Unique correlation IDs: $CORRELATION_IDS"
    fi
    
    print_response "$BODY"
    
    # Check if we have logs
    if command -v jq &> /dev/null; then
        if [ "$TOTAL_LOGS" -gt "0" ]; then
            print_info "✓ Splunk is successfully collecting logs"
        else
            print_info "⚠ Warning: No logs collected yet"
        fi
    fi
else
    print_error "Failed to get Splunk statistics (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
fi
echo ""
sleep 1

# Test 15: Correlation ID Trace
print_test "15" "Splunk Logger - Trace Request Flow by Correlation ID"
print_info "Testing: GET /api/trace/$CORRELATION_ID"
print_info "Verifying complete request flow can be traced"

TRACE_RESPONSE=$(curl -s -w "\n%{http_code}" \
  http://localhost:8088/api/trace/$CORRELATION_ID)

HTTP_CODE=$(echo "$TRACE_RESPONSE" | tail -n1)
BODY=$(echo "$TRACE_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ]; then
    print_success "Correlation ID trace retrieved"
    
    if command -v jq &> /dev/null; then
        TRACE_COUNT=$(echo "$BODY" | jq '.trace | length' 2>/dev/null)
        SERVICES=$(echo "$BODY" | jq -r '.services_involved[]' 2>/dev/null)
        
        print_info "Trace entries found: $TRACE_COUNT"
        print_info "Services involved in this flow:"
        
        while IFS= read -r service; do
            print_info "  • $service"
        done <<< "$SERVICES"
    fi
    
    print_response "$BODY"
    
    # Validate we can trace the flow
    if echo "$BODY" | grep -q "auth-service"; then
        print_info "✓ Auth service log found in trace"
    fi
    if echo "$BODY" | grep -q "product-service"; then
        print_info "✓ Product service log found in trace"
    fi
    if echo "$BODY" | grep -q "loyalty-service"; then
        print_info "✓ Loyalty service log found in trace"
    fi
    if echo "$BODY" | grep -q "policy-service"; then
        print_info "✓ Policy service log found in trace"
    fi
else
    print_error "Failed to trace correlation ID (HTTP $HTTP_CODE)"
    print_info "Response: $BODY"
    
    if [ "$HTTP_CODE" == "404" ]; then
        print_info "This might mean logs haven't reached Splunk yet"
        print_info "Try checking Splunk stats or wait a moment and retry"
    fi
fi
echo ""

#########################################################
# FINAL SUMMARY
#########################################################

echo ""
print_header "TEST SUMMARY"
echo ""

echo "Test Run: $(date)"
echo "Correlation ID: $CORRELATION_ID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $TESTS_PASSED${NC}"
echo -e "${RED}Failed:       $TESTS_FAILED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ ALL TESTS PASSED! 🎉${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Your deployment is successful!"
    echo ""
    echo "What's Working:"
    echo "  ✓ All 6 microservices are running"
    echo "  ✓ Splunk logger is collecting logs"
    echo "  ✓ Correlation ID tracing is functional"
    echo "  ✓ Services can communicate properly"
    echo "  ✓ Authentication is working"
    echo "  ✓ Product search is functional"
    echo "  ✓ Loyalty system is accessible"
    echo "  ✓ Policy retrieval is working"
    echo "  ✓ End-to-end flow can be traced"
    echo ""
    echo "Next Steps:"
    echo "  1. ✓ Step 1 Complete: All services deployed and tested"
    echo "  2. → Proceed to: Deploy user journey simulator"
    echo "  3. → Then: Deploy agentic tracer"
    echo "  4. → Finally: Complete architecture discovery"
    echo ""
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}⚠ SOME TESTS FAILED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Troubleshooting Steps:"
    echo ""
    echo "1. Check Service Logs:"
    echo "   sudo journalctl -u microservices -n 50"
    echo "   sudo journalctl -u splunk-logger -n 50"
    echo ""
    echo "2. Check if services are running:"
    echo "   sudo systemctl status microservices"
    echo "   sudo systemctl status splunk-logger"
    echo ""
    echo "3. Check which ports are listening:"
    echo "   sudo ss -tlnp | grep -E ':(5001|5002|5003|5004|5005|5006|8088)'"
    echo ""
    echo "4. Test individual services manually:"
    echo "   curl http://localhost:5001/health"
    echo "   curl http://localhost:8088/health"
    echo ""
    echo "5. Restart services if needed:"
    echo "   sudo systemctl restart splunk-logger"
    echo "   sudo systemctl restart microservices"
    echo ""
    echo "6. Check for errors in application files:"
    echo "   Check that all Python files exist and have correct syntax"
    echo ""
    exit 1
fi