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
# AWS Deployment Script for Architecture Discovery
# Amazon Linux 2023 Version
# Deploys 6 Microservices + Splunk Logger
#########################################################

echo "=========================================="
echo "ARCHITECTURE DISCOVERY - AWS DEPLOYMENT"
echo "Amazon Linux 2023"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Detect OS
print_info "Detecting Operating System..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "OS: $NAME $VERSION"
fi
echo ""

# Step 1: System Update
echo "Step 1: Updating system packages..."
sudo dnf update -y
if [ $? -eq 0 ]; then
    print_success "System packages updated"
else
    print_error "Failed to update system packages"
    exit 1
fi
echo ""

# Step 2: Install Python and dependencies
echo "Step 2: Installing Python 3 and pip..."
sudo dnf install -y python3 python3-pip
if [ $? -eq 0 ]; then
    print_success "Python 3 installed"
    python3 --version
    pip3 --version
else
    print_error "Failed to install Python 3"
    exit 1
fi
echo ""

# Step 3: Create project directory
echo "Step 3: Creating project directory..."
PROJECT_DIR="/home/ec2-user/architecture-discovery"
# PROJECT_DIR="/home/ec2-user/architecture-discovery-aws"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
print_success "Project directory created: $PROJECT_DIR"
echo ""

# Step 4: Create virtual environment
echo "Step 4: Creating Python virtual environment..."
# python3 -m venv aads-venv
python3 -m venv venv


# if [ -d "venv" ]; then      
#    rm -rf venv
# fi

if [ $? -eq 0 ]; then
    print_success "Virtual environment created"
else
    print_error "Failed to create virtual environment"
    exit 1
fi
echo ""

# Step 5: Activate virtual environment
echo "Step 5: Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"
echo ""

# Step 6: Upgrade pip
echo "Step 6: Upgrading pip..."
pip install --upgrade pip
print_success "Pip upgraded"
echo ""

# Step 7: Install Python packages
echo "Step 7: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed from requirements.txt"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
else
    print_info "requirements.txt not found, installing manually..."
    pip install Flask==3.0.0 Werkzeug==3.0.1 requests==2.31.0 python-dotenv==1.0.0 anthropic==0.40.0
    print_success "Dependencies installed manually"
fi
echo ""

# Step 8: Create systemd service files
echo "Step 8: Creating systemd service files..."

# Splunk Logger Service
sudo tee /etc/systemd/system/splunk-logger.service > /dev/null <<EOF
[Unit]
Description=Splunk Log Collector
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python3 splunk_logger.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=splunk-logger

[Install]
WantedBy=multi-user.target
EOF

print_success "Splunk Logger service file created"

# Microservices Service
sudo tee /etc/systemd/system/microservices.service > /dev/null <<EOF
[Unit]
Description=E-Commerce Microservices (6 services)
After=network.target splunk-logger.service
Requires=splunk-logger.service

[Service]
Type=simple
User=ec2-user
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python3 run_services.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

print_success "Microservices service file created"
echo ""

# Step 9: Reload systemd
echo "Step 9: Reloading systemd daemon..."
sudo systemctl daemon-reload
print_success "Systemd daemon reloaded"
echo ""

# Step 10: Enable services
echo "Step 10: Enabling services to start on boot..."
sudo systemctl enable splunk-logger.service
sudo systemctl enable microservices.service
print_success "Services enabled"
echo ""

# Step 11: Start Splunk Logger first
echo "Step 11: Starting Splunk Logger..."
sudo systemctl start splunk-logger.service
sleep 3

# Check if Splunk started
if sudo systemctl is-active --quiet splunk-logger.service; then
    print_success "Splunk Logger is running"
else
    print_error "Splunk Logger failed to start"
    echo "Checking logs..."
    sudo journalctl -u splunk-logger.service -n 20 --no-pager
    exit 1
fi
echo ""

# Step 12: Start Microservices
echo "Step 12: Starting Microservices..."
sudo systemctl start microservices.service
sleep 5

# Check if Microservices started
if sudo systemctl is-active --quiet microservices.service; then
    print_success "Microservices are running"
else
    print_error "Microservices failed to start"
    echo "Checking logs..."
    sudo journalctl -u microservices.service -n 20 --no-pager
    exit 1
fi
echo ""

# Step 13: Verify services
echo "Step 13: Verifying all services..."
echo ""

# Wait a moment for services to fully initialize
sleep 3

# Check Splunk
echo "Checking Splunk Logger (port 8088)..."
SPLUNK_CHECK=$(curl -s http://localhost:8088/health 2>/dev/null)
if echo "$SPLUNK_CHECK" | grep -q "healthy"; then
    print_success "Splunk Logger: HEALTHY"
else
    print_error "Splunk Logger: NOT RESPONDING"
    echo "Response: $SPLUNK_CHECK"
fi

# Check each microservice
services=(
    "5001:Auth"
    "5002:Product"
    "5003:Order"
    "5004:Payment"
    "5005:Loyalty"
    "5006:Policy"
)

echo ""
for service in "${services[@]}"; do
    IFS=':' read -r port name <<< "$service"
    echo "Checking $name Service (port $port)..."
    SERVICE_CHECK=$(curl -s http://localhost:$port/health 2>/dev/null)
    if echo "$SERVICE_CHECK" | grep -q "healthy"; then
        print_success "$name Service: HEALTHY"
    else
        print_error "$name Service: NOT RESPONDING"
        echo "Response: $SERVICE_CHECK"
    fi
done
echo ""

# Step 14: Install additional utilities
echo "Step 14: Installing additional utilities..."
sudo dnf install -y net-tools curl jq
print_success "Utilities installed"
echo ""

# Step 15: Display summary
echo "=========================================="
echo "DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""

# Display service status
echo "Services Status:"
echo "----------------"
sudo systemctl status splunk-logger.service --no-pager -l | head -n 5
echo ""
sudo systemctl status microservices.service --no-pager -l | head -n 5
echo ""

# Get IP addresses
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)

echo "Instance Information:"
echo "====================="
echo ""
echo "Public IP:  $PUBLIC_IP"
echo "Private IP: $PRIVATE_IP"
echo ""

echo "Service Endpoints (External Access):"
echo "======================================"
echo ""
echo "Health Checks:"
echo "  • Splunk Logger:   http://$PUBLIC_IP:8088/health"
echo "  • Auth Service:    http://$PUBLIC_IP:5001/health"
echo "  • Product Service: http://$PUBLIC_IP:5002/health"
echo "  • Order Service:   http://$PUBLIC_IP:5003/health"
echo "  • Payment Service: http://$PUBLIC_IP:5004/health"
echo "  • Loyalty Service: http://$PUBLIC_IP:5005/health"
echo "  • Policy Service:  http://$PUBLIC_IP:5006/health"
echo ""

echo "API Endpoints:"
echo "  • Login:           POST http://$PUBLIC_IP:5001/api/auth/login"
echo "  • Search Products: GET  http://$PUBLIC_IP:5002/api/products/search?query=laptop"
echo "  • Loyalty Points:  GET  http://$PUBLIC_IP:5005/api/loyalty/points"
echo "  • Policies:        GET  http://$PUBLIC_IP:5006/api/policies/return"
echo "  • Splunk Stats:    GET  http://$PUBLIC_IP:8088/api/stats"
echo ""

echo "Useful Commands:"
echo "================"
echo ""
echo "View Logs:"
echo "  • Splunk logs:      sudo journalctl -u splunk-logger -f"
echo "  • Services logs:    sudo journalctl -u microservices -f"
echo "  • Both logs:        sudo journalctl -u splunk-logger -u microservices -f"
echo "  • Last 50 lines:    sudo journalctl -u microservices -n 50"
echo ""
echo "Service Management:"
echo "  • Restart Splunk:   sudo systemctl restart splunk-logger"
echo "  • Restart Services: sudo systemctl restart microservices"
echo "  • Stop all:         sudo systemctl stop splunk-logger microservices"
echo "  • Start all:        sudo systemctl start splunk-logger microservices"
echo "  • Check status:     sudo systemctl status splunk-logger microservices"
echo ""
echo "Check Network:"
echo "  • Open ports:       sudo netstat -tlnp | grep -E ':(5001|5002|5003|5004|5005|5006|8088)'"
echo "  • Or use ss:        sudo ss -tlnp | grep -E ':(5001|5002|5003|5004|5005|5006|8088)'"
echo ""
echo "File Locations:"
echo "  • Project dir:      $PROJECT_DIR"
echo "  • Logs file:        $PROJECT_DIR/splunk_logs.jsonl"
echo "  • Virtual env:      $PROJECT_DIR/venv"
echo "  • Service files:    /etc/systemd/system/splunk-logger.service"
echo "                      /etc/systemd/system/microservices.service"
echo ""

echo "Test Commands (run from EC2):"
echo "=============================="
echo ""
echo "# Test health endpoints"
echo "curl http://localhost:8088/health"
echo "curl http://localhost:5001/health"
echo ""
echo "# Test login"
echo 'curl -X POST http://localhost:5001/api/auth/login \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"email":"user1@test.com","password":"password123"}'"'"
echo ""
echo "# Test product search"
echo "curl http://localhost:5002/api/products/search?query=laptop"
echo ""
echo "# Check Splunk stats"
echo "curl http://localhost:8088/api/stats"
echo ""

echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo ""
echo "1. Test services from this EC2 instance (use commands above)"
echo "2. Test from your local machine using public IP"
echo "3. Verify Security Group allows inbound on ports 5001-5006, 8088"
echo "4. Run test_services.sh from your local machine"
echo "5. If all tests pass, proceed to deploy user journey simulator"
echo ""
echo "Troubleshooting:"
echo "  • If services not accessible externally, check Security Group"
echo "  • If services crash, check logs: sudo journalctl -u microservices -n 100"
echo "  • If port conflicts, check: sudo netstat -tlnp | grep :5001"
echo ""
echo "=========================================="
echo "Deployment script completed successfully!"
echo "=========================================="
echo ""