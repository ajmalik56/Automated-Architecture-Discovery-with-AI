# Getting Started

This guide will help you set up and run the Automated Architecture Discovery System.

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (Claude)
- 2GB RAM minimum
- Basic understanding of microservices

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/automated-architecture-discovery.git
cd automated-architecture-discovery
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or create a .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

## Running the System

### Quick Start (One Command)

```bash
python master_orchestrator.py
```

This will:
1. Start all microservices
2. Simulate user journeys
3. Collect logs
4. Discover architecture
5. Generate diagrams
6. Detect drift

**Runtime**: ~2 minutes

### Step-by-Step Execution

If you want to run components individually:

#### Step 1: Start Microservices

```bash
python run_services.py
```

Keep this running in one terminal.

#### Step 2: Simulate User Journeys (New Terminal)

```bash
python user_journey_simulator.py
```

#### Step 3: Run Architecture Discovery

```bash
python architecture_tracer.py
```

#### Step 4: Generate Diagrams

```bash
python enhanced_diagram_generator.py
```

#### Step 5: Check for Drift

```bash
python advanced_drift_tracker.py
```

## Viewing Results

### Main Output File

```bash
# View the complete architecture documentation
cat complete_annotated_architecture.md

# Or open in VS Code with Mermaid preview
code complete_annotated_architecture.md
# Press Ctrl+K V to see diagrams
```

### Other Output Files

- `discovered_architecture.json` - Raw architecture data
- `journey_details.json` - User journey traces
- `architecture_history/` - Historical snapshots
- `logs/` - Execution logs

## Next Steps

- Review the generated architecture diagram
- Check drift reports in `architecture_history/`
- Modify user journeys in `user_journey_simulator.py`
- Add more microservices in `ecommerce_services.py`

## Need Help?

- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system details
- Open a GitHub issue for questions

---

**Quick Reference Commands:**

```bash
# Full system run
python master_orchestrator.py

# Check logs
tail -f logs/discovery_*.log

# View architecture
cat complete_annotated_architecture.md
```