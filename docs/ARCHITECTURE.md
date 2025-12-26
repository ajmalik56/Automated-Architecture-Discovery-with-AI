# System Architecture

This document explains the architecture of the Automated Architecture Discovery System.

## Overview

The system automatically discovers and documents microservices architecture by tracing real user flows through applications.

## High-Level Architecture

```
┌─────────────────┐
│  User Journey   │
│   Simulator     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  Microservices  │────▶│    Splunk    │
│   (6 services)  │     │ Log Collector│
└────────┬────────┘     └──────┬───────┘
         │                     │
         │                     │
         ▼                     ▼
┌─────────────────────────────────┐
│  AI-Powered Architecture Tracer │
│      (Claude AI Integration)    │
└────────┬────────────────────────┘
         │
         ├──────────────────┬────────────────┐
         ▼                  ▼                ▼
┌─────────────────┐  ┌──────────┐  ┌────────────┐
│Diagram Generator│  │  Drift   │  │  History   │
│                 │  │ Detector │  │  Tracker   │
└─────────────────┘  └──────────┘  └────────────┘
```

## Components

### 1. Microservices Layer

**File**: `ecommerce_services.py`

Six Flask-based microservices:

- **auth_service** (Port 5001) - User authentication
- **product_service** (Port 5002) - Product catalog
- **order_service** (Port 5003) - Order management
- **payment_service** (Port 5004) - Payment processing
- **loyalty_service** (Port 5005) - Loyalty program
- **policy_service** (Port 5006) - Policy documents

**Key Features:**
- Correlation ID propagation
- Structured logging (JSON format)
- Health check endpoints
- Service-to-service communication

### 2. User Journey Simulator

**File**: `user_journey_simulator.py`

Simulates 5 different user personas:

1. **Regular Shopper** - Browse → View → Purchase
2. **Loyalty Member** - Login → Loyalty Check → Purchase
3. **Policy Reader** - Browse → View Policy
4. **Order Checker** - Login → Check Orders
5. **Premium Buyer** - Full journey with all services

**Purpose**: Generate realistic traffic patterns for discovery.

### 3. Log Collection

**File**: `splunk_logger.py`

Mock Splunk log aggregation system:

- Collects structured logs from all services
- Stores in JSONL format
- Provides query interface
- Validates correlation IDs

### 4. Architecture Tracer (Core AI Component)

**File**: `architecture_tracer.py`

AI-powered architecture discovery:

- Analyzes traces from user journeys
- Cross-references with Splunk logs
- Uses Claude AI for intelligent insights
- Identifies services, dependencies, endpoints
- Detects patterns and anomalies

**AI Integration:**
```python
# Claude AI analyzes architecture
response = anthropic.messages.create(
    model="claude-sonnet-4-5",
    messages=[{
        "role": "user",
        "content": f"Analyze this architecture: {traces}"
    }]
)
```

### 5. Diagram Generator

**File**: `enhanced_diagram_generator.py`

Creates visual documentation:

- **Architecture diagrams** - Service dependencies
- **Sequence diagrams** - User journey flows
- **Dependency matrix** - Service relationships
- **API catalog** - Complete endpoint listing

**Output Format**: Markdown with Mermaid diagrams

### 6. Drift Detection

**Files**: 
- `drift_detector.py` - Basic drift detection
- `advanced_drift_tracker.py` - Historical tracking

Tracks architectural changes:

- Compares current vs baseline architecture
- Calculates drift score (0-100)
- Assigns severity (LOW/MEDIUM/HIGH/CRITICAL)
- Maintains historical snapshots
- Generates trend reports

### 7. Master Orchestrator

**File**: `master_orchestrator.py`

One-click execution:

1. Starts all microservices
2. Waits for services to be healthy
3. Simulates user journeys
4. Collects and validates logs
5. Discovers architecture with AI
6. Generates diagrams
7. Detects drift
8. Creates comprehensive report

## Data Flow

### 1. Request Flow

```
User Journey Simulator
    │
    ├─ GET /health → auth_service
    ├─ POST /login → auth_service
    ├─ GET /products → product_service
    │       │
    │       └─ GET /orders → order_service
    │               │
    │               └─ POST /process → payment_service
    │
    └─ Correlation ID: tracked across all calls
```

### 2. Log Flow

```
Microservices
    │
    ├─ Structured JSON logs
    │
    ▼
Splunk Logger
    │
    ├─ Aggregates logs
    ├─ Validates correlation IDs
    │
    ▼
Architecture Tracer
    │
    ├─ Reads logs
    ├─ Validates flows
    │
    ▼
Claude AI Analysis
```

### 3. Discovery Flow

```
Traces + Logs
    │
    ▼
Claude AI Analysis
    │
    ├─ Identifies services
    ├─ Maps dependencies
    ├─ Catalogs endpoints
    ├─ Detects patterns
    │
    ▼
Discovered Architecture (JSON)
    │
    ├─ Services list
    ├─ Dependencies map
    ├─ Endpoints catalog
    ├─ Journey flows
    │
    ▼
Diagram Generator
    │
    ├─ Architecture diagram
    ├─ Sequence diagrams
    ├─ Dependency matrix
    │
    ▼
Complete Documentation (Markdown)
```

## Key Design Decisions

### 1. Correlation ID Pattern

Every request gets a unique correlation ID that propagates through all services:

```python
correlation_id = request.headers.get('X-Correlation-ID')
# Pass to downstream services
headers = {'X-Correlation-ID': correlation_id}
```

**Why**: Enables end-to-end request tracing across microservices.

### 2. AI-Powered Discovery

Uses Claude AI instead of rule-based parsing:

**Advantages:**
- Handles unexpected patterns
- Provides intelligent insights
- Adapts to new architectures
- Generates human-readable analysis

### 3. Dual Validation

Validates flows in two ways:

1. **Direct tracing** - HTTP calls from simulator
2. **Log validation** - Cross-reference with Splunk

**Why**: Ensures accuracy and catches missed calls.

### 4. Drift Tracking

Maintains historical baselines:

```
architecture_history/
    ├─ baseline_architecture.json
    ├─ snapshot_20251014_120000.json
    ├─ snapshot_20251014_130000.json
    └─ drift_trend_report.txt
```

**Why**: Track architectural evolution over time.

## Scalability Considerations

### Current Design (Demo)

- Single-node deployment
- In-memory log storage
- Sequential processing
- ~6 services, ~5 journeys

### Production Scaling (Future)

- **Microservices**: Containerize with Docker/Kubernetes
- **Log Storage**: Real Splunk/ELK/CloudWatch
- **Processing**: Parallel journey execution
- **Storage**: PostgreSQL for history, Redis for cache
- **Discovery**: Scheduled batch processing
- **AI**: Request batching for Claude API

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Services | Flask | Lightweight HTTP services |
| Logging | Python logging | Structured JSON logs |
| AI | Claude API | Architecture analysis |
| Diagrams | Mermaid | Visual documentation |
| Storage | JSON files | Demo data persistence |
| Orchestration | Python multiprocessing | Service management |

## Security Considerations

⚠️ **This is a demonstration project** - Production use requires:

- Authentication/Authorization
- HTTPS/TLS
- Secrets management
- Input validation
- Rate limiting
- API key rotation
- Audit logging

## Performance Characteristics

**Current Performance:**
- Startup time: ~10 seconds (all services)
- Journey execution: ~30 seconds (5 journeys)
- AI analysis: ~30-60 seconds (depending on architecture complexity)
- Diagram generation: ~5 seconds
- Total runtime: ~2 minutes

**Optimization Opportunities:**
- Parallel journey execution
- Claude API request batching
- Cached AI responses
- Incremental diagram updates

## Extension Points

### Adding New Services

1. Add service definition to `ecommerce_services.py`
2. Update port assignments
3. Add to service runner
4. Discovery happens automatically!

### Adding New Journeys

1. Add journey function to `user_journey_simulator.py`
2. Include in journey list
3. Run system - new flows discovered automatically

### Custom Analysis

1. Modify Claude AI prompt in `architecture_tracer.py`
2. Add custom metrics/insights
3. Update diagram generator for new visualizations

## Further Reading

- [Getting Started Guide](GETTING_STARTED.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

*This architecture enables automatic, AI-powered discovery of microservices systems with minimal manual intervention.*