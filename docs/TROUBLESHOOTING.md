# Troubleshooting Guide

Common issues and their solutions when running the Automated Architecture Discovery System.

## Quick Diagnostics

```bash
# Check Python version
python --version  # Should be 3.8+

# Check if virtual environment is activated
which python  # Should point to venv/bin/python

# Check API key
echo $ANTHROPIC_API_KEY  # Should show your key

# Check port availability
netstat -an | grep 500  # Check if ports 5001-5006 are free
```

---

## Installation Issues

### Issue: `ModuleNotFoundError: No module named 'anthropic'`

**Problem**: Dependencies not installed or virtual environment not activated.

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep anthropic
```

### Issue: `pip install` fails with permission error

**Problem**: Trying to install globally without sudo, or not in virtual environment.

**Solution**:
```bash
# Make sure you're in virtual environment
python -m venv venv
source venv/bin/activate

# Now install (no sudo needed)
pip install -r requirements.txt
```

### Issue: Python version too old

**Problem**: System has Python 2.7 or Python < 3.8.

**Solution**:
```bash
# Check available Python versions
python3 --version
python3.8 --version
python3.9 --version

# Use specific version for venv
python3.9 -m venv venv
source venv/bin/activate
```

---

## Service Startup Issues

### Issue: `OSError: [Errno 48] Address already in use`

**Problem**: Port already in use by another process.

**Solution**:
```bash
# Find what's using the port
lsof -i :5001  # Check each port 5001-5006
# or
netstat -an | grep 5001

# Kill the process
kill -9 <PID>

# Or use different ports in ecommerce_services.py
```

### Issue: Services start but immediately crash

**Problem**: Missing dependencies or import errors.

**Solution**:
```bash
# Check logs
tail -f logs/discovery_*.log

# Test services individually
python ecommerce_services.py

# Check for detailed error
python -c "import flask; print(flask.__version__)"
```

### Issue: `ModuleNotFoundError: No module named 'flask'`

**Problem**: Flask not installed.

**Solution**:
```bash
pip install flask==3.0.0
# or
pip install -r requirements.txt
```

---

## API Key Issues

### Issue: `AuthenticationError: Invalid API key`

**Problem**: API key not set, incorrect, or expired.

**Solution**:
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set it properly (replace with your actual key)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Verify in Python
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Issue: API key set but still not working

**Problem**: Environment variable not loaded in current shell.

**Solution**:
```bash
# Re-export in current shell
export ANTHROPIC_API_KEY="your-key-here"

# Or source your .bashrc/.zshrc
source ~/.bashrc

# Or use .env file and python-dotenv
pip install python-dotenv
```

---

## Runtime Issues

### Issue: Master orchestrator times out waiting for services

**Problem**: Services taking too long to start or not starting at all.

**Solution**:
```bash
# Check if services are actually running
ps aux | grep python | grep ecommerce_services

# Check health manually
curl http://localhost:5001/health
curl http://localhost:5002/health

# Increase timeout in master_orchestrator.py
# Change: timeout=30  →  timeout=60
```

### Issue: User journeys fail with connection errors

**Problem**: Services not ready or network issues.

**Solution**:
```bash
# Test each service manually
curl http://localhost:5001/health
curl http://localhost:5002/products

# Check firewall
# Linux
sudo ufw status
# Mac
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Wait longer between steps
# Add sleep in user_journey_simulator.py
```

### Issue: No logs in splunk_logs.jsonl

**Problem**: Services not logging or log file permissions.

**Solution**:
```bash
# Check if file exists and is writable
ls -la splunk_logs.jsonl

# Check if services are logging
tail -f splunk_logs.jsonl

# Verify logging in services
# Add this to test:
python -c "from splunk_logger import SplunkLogger; logger = SplunkLogger(); logger.log('test', 'TEST', {'msg': 'test'})"
```

---

## AI/Claude Issues

### Issue: Claude API rate limit exceeded

**Problem**: Too many requests too quickly.

**Solution**:
```bash
# Wait a few minutes and retry

# Or add delays in agentic_architecture_tracer.py
import time
time.sleep(2)  # Between requests

# Use fewer journeys for testing
# Edit user_journey_simulator.py - comment out some journeys
```

### Issue: Claude API returns empty or error response

**Problem**: Invalid prompt format or API issue.

**Solution**:
```bash
# Check API status
# Visit: https://status.anthropic.com

# Test API manually
python -c "
import anthropic
client = anthropic.Anthropic(api_key='your-key')
response = client.messages.create(
    model='claude-sonnet-4-5',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Test'}]
)
print(response)
"

# Check your API usage limits
# Visit: https://console.anthropic.com
```

### Issue: Discovered architecture is incomplete

**Problem**: Not enough data or AI didn't capture all services.

**Solution**:
```bash
# Run more journeys
# Increase iterations in user_journey_simulator.py

# Check splunk_logs.jsonl has data
wc -l splunk_logs.jsonl

# Verify all services were called
grep -o '"service":"[^"]*"' splunk_logs.jsonl | sort | uniq -c

# Re-run with verbose logging
# Add print statements in agentic_architecture_tracer.py
```

---

## Diagram Generation Issues

### Issue: Mermaid diagrams not rendering

**Problem**: VS Code extension not installed or file not recognized.

**Solution**:
```bash
# Install VS Code extension
# Open VS Code → Extensions → Search "Markdown Preview Mermaid"

# Or use online viewer
# Copy diagram code to https://mermaid.live

# Check diagram syntax
python enhanced_diagram_generator.py
```

### Issue: Diagrams are empty or malformed

**Problem**: No data in discovered_architecture.json or generation error.

**Solution**:
```bash
# Check discovered_architecture.json exists and has data
cat discovered_architecture.json | jq .

# Manually run diagram generator
python enhanced_diagram_generator.py

# Check for errors in logs
tail -f logs/discovery_*.log
```

---

## Drift Detection Issues

### Issue: "No baseline found" error

**Problem**: First run, no baseline exists yet.

**Solution**:
```bash
# Create baseline manually
cp discovered_architecture.json baseline_architecture.json

# Or run twice
python master_orchestrator.py  # First run creates baseline
python master_orchestrator.py  # Second run detects drift
```

### Issue: Drift always shows 0%

**Problem**: Architecture hasn't changed or comparison logic issue.

**Solution**:
```bash
# Make a change to test
# Add a new service or modify a journey

# Check baseline vs current
diff baseline_architecture.json discovered_architecture.json

# Manually run drift detector
python advanced_drift_tracker.py
```

---

## Performance Issues

### Issue: System is very slow

**Problem**: API calls are synchronous or too much data.

**Solution**:
```bash
# Reduce number of journeys for testing
# Edit user_journey_simulator.py

# Use simpler architecture
# Comment out some services in ecommerce_services.py

# Check system resources
top  # or htop
free -h  # Check memory
```

### Issue: Out of memory errors

**Problem**: Too many logs in memory or large data structures.

**Solution**:
```bash
# Clear old logs
rm splunk_logs.jsonl

# Reduce journey iterations
# Edit JOURNEY_ITERATIONS in user_journey_simulator.py

# Increase system swap
# (OS-specific)
```

---

## AWS Deployment Issues

### Issue: Can't connect to EC2 instance

**Problem**: Security group rules or SSH key issues.

**Solution**:
```bash
# Check security group allows SSH (port 22)
# AWS Console → EC2 → Security Groups

# Check SSH key permissions
chmod 400 your-key.pem

# Try with verbose SSH
ssh -v -i your-key.pem ec2-user@your-ip
```

### Issue: Services won't start on EC2

**Problem**: Firewall or port restrictions.

**Solution**:
```bash
# Check if ports are listening
sudo netstat -tlnp | grep 500

# Check firewall
sudo iptables -L

# Make sure security group allows ports 5001-5006
```

---

## Getting Help

### Before Opening an Issue

1. ✅ Check this troubleshooting guide
2. ✅ Review error messages carefully
3. ✅ Check logs: `tail -f logs/discovery_*.log`
4. ✅ Verify basic setup (Python version, API key, ports)
5. ✅ Try the minimal reproduction case

### Opening a GitHub Issue

Include:

```markdown
## Environment
- OS: [Ubuntu 22.04]
- Python Version: [3.9.5]
- Installation Method: [pip/venv]

## Steps to Reproduce
1. Run command X
2. Observe error Y
3. Expected behavior Z

## Error Message
```
[Paste full error message]
```

## Logs
```
[Paste relevant logs]
```

## What I've Tried
- [List what you've already attempted]
```

### Community Resources

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check `/docs` folder for guides

---

## Quick Reference: Common Commands

```bash
# Full diagnostics
python --version
pip list
echo $ANTHROPIC_API_KEY
netstat -an | grep 500
ps aux | grep python

# Fresh start
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Clean slate
rm discovered_architecture.json journey_details.json
rm splunk_logs.jsonl
rm -rf logs/ architecture_history/

# Test individual components
python ecommerce_services.py
python user_journey_simulator.py
python agentic_architecture_tracer.py

# Check outputs
cat discovered_architecture.json | jq .
cat complete_annotated_architecture.md
ls -la architecture_history/
```

---

*Still stuck? Open a GitHub issue with detailed information about your problem!*