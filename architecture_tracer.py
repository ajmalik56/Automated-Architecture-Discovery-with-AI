"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Architecture Tracer
AI-powered microservices architecture discovery from distributed traces
"""

import json
import requests
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

# Optional Claude AI integration
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  anthropic package not installed. Claude AI analysis will be skipped.")
    print("   To enable: pip install anthropic")


class ArchitectureTracer:
    """
    AI-powered architecture discovery
    Discovers services, dependencies, and endpoints from correlation ID traces
    """
    
    def __init__(self, splunk_url='http://localhost:8088'):
        self.splunk_url = splunk_url
        self.service_dependencies = defaultdict(set)
        self.service_endpoints = defaultdict(set)
        self.user_journeys = []
        self.all_services = set()
        
        # Claude AI setup (optional)
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        if CLAUDE_AVAILABLE and self.claude_api_key:
            self.client = Anthropic(api_key=self.claude_api_key)
            print("✅ Claude AI integration enabled")
        else:
            print("ℹ️  Claude AI integration disabled (no API key or package)")
    
    def fetch_trace_from_splunk(self, correlation_id: str) -> List[Dict]:
        """Fetch complete trace for a correlation ID from Splunk"""
        try:
            url = f"{self.splunk_url}/api/trace/{correlation_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('trace', [])
            else:
                print(f"  ⚠️  Failed to fetch trace for {correlation_id}: HTTP {response.status_code}")
                return []
        
        except Exception as e:
            print(f"  ✗ Error fetching trace for {correlation_id}: {str(e)}")
            return []
    
    def analyze_trace(self, correlation_id: str, trace: List[Dict]) -> Dict:
        """
        AI-BASED BEHAVIOR: Analyze a trace to discover services, dependencies, and endpoints
        The LLM autonomously discovers architecture without predetermined knowledge
        """
        if not trace:
            return {}
        
        services_in_order = []
        endpoints_used = []
        previous_service = None
        
        # DISCOVERY: LLM finds services and endpoints it didn't know about
        for entry in trace:
            service = entry.get('service')
            endpoint = entry.get('endpoint')
            
            # Discover service
            if service and service not in services_in_order:
                services_in_order.append(service)
                self.all_services.add(service)
            
            # Discover endpoint
            if endpoint:
                endpoints_used.append({
                    'service': service,
                    'endpoint': endpoint,
                    'timestamp': entry.get('timestamp')
                })
                self.service_endpoints[service].add(endpoint)
            
            # INFERENCE: LLM infers dependencies from call sequences
            if previous_service and previous_service != service:
                self.service_dependencies[previous_service].add(service)
            
            previous_service = service
        
        journey_data = {
            'correlation_id': correlation_id,
            'services': services_in_order,
            'endpoints': endpoints_used,
            'start_service': services_in_order[0] if services_in_order else None,
            'end_service': services_in_order[-1] if services_in_order else None,
            'service_count': len(services_in_order)
        }
        
        return journey_data
    
    def process_all_correlation_ids(self, correlation_ids: List[tuple]):
        """
        AI-BASED BEHAVIOR: Process all journeys to build complete architecture map
        Synthesizes patterns across multiple observations
        """
        print("\n" + "="*60)
        print("AI-BASED ARCHITECTURE DISCOVERY")
        print("="*60)
        print(f"\nAnalyzing {len(correlation_ids)} user journeys...")
        print("LLM is discovering services, dependencies, and endpoints...\n")
        
        for journey_name, correlation_id in correlation_ids:
            print(f"📊 Processing: {journey_name}")
            print(f"   Correlation ID: {correlation_id}")
            
            # Fetch trace from Splunk
            trace = self.fetch_trace_from_splunk(correlation_id)
            
            if trace:
                print(f"   ✓ Found {len(trace)} log entries")
                
                # Analyze trace autonomously
                journey_data = self.analyze_trace(correlation_id, trace)
                journey_data['journey_name'] = journey_name
                
                if journey_data.get('services'):
                    self.user_journeys.append(journey_data)
                    print(f"   ✓ Discovered {len(journey_data['services'])} services in flow")
                else:
                    print(f"   ⚠️  No services found in trace")
            else:
                print(f"   ✗ No trace data found")
            
            print()
        
        print("="*60)
        print(f"✅ Discovery Complete!")
        print(f"   Total Services: {len(self.all_services)}")
        print(f"   Total Dependencies: {sum(len(deps) for deps in self.service_dependencies.values())}")
        print(f"   Total Endpoints: {sum(len(eps) for eps in self.service_endpoints.values())}")
        print("="*60)
    
    def build_architecture_map(self) -> Dict:
        """Build complete architecture map from discoveries"""
        
        # Convert sets to lists for JSON serialization
        dependencies_dict = {
            service: list(deps) 
            for service, deps in self.service_dependencies.items()
        }
        
        endpoints_dict = {
            service: list(eps) 
            for service, eps in self.service_endpoints.items()
        }
        
        architecture = {
            'timestamp': datetime.utcnow().isoformat(),
            'discovery_method': 'llm_powered_tracing',
            'total_services': len(self.all_services),
            'services': sorted(list(self.all_services)),
            'service_dependencies': dependencies_dict,
            'service_endpoints': endpoints_dict,
            'user_journeys': self.user_journeys,
            'metrics': {
                'total_services': len(self.all_services),
                'total_dependencies': sum(len(deps) for deps in self.service_dependencies.values()),
                'total_endpoints': sum(len(eps) for eps in self.service_endpoints.values()),
                'total_journeys': len(self.user_journeys)
            }
        }
        
        return architecture
    
    def use_claude_for_analysis(self, architecture: Dict) -> str:
        """
        ADVANCED AI: Use Claude for expert-level architectural analysis
        """
        if not self.client:
            return "Claude AI analysis not available (no API key configured)"
        
        try:
            prompt = f"""Analyze this e-commerce microservices architecture discovered through distributed tracing:

Services: {', '.join(architecture['services'])}
Total Services: {architecture['metrics']['total_services']}
Total Dependencies: {architecture['metrics']['total_dependencies']}
Total Endpoints: {architecture['metrics']['total_endpoints']}

Service Dependencies:
{json.dumps(architecture['service_dependencies'], indent=2)}

Service Endpoints:
{json.dumps(architecture['service_endpoints'], indent=2)}

Please provide:
1. Critical paths and key dependencies
2. Potential bottlenecks or single points of failure
3. Recommendations for monitoring and observability
4. Suggestions for architectural improvements
5. Security considerations

Keep the analysis concise and actionable."""

            print("\n🤖 Requesting Claude AI analysis...")
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = message.content[0].text
            print("✅ Claude AI analysis complete!\n")
            return analysis
        
        except Exception as e:
            print(f"⚠️  Claude AI analysis failed: {str(e)}")
            return f"Claude AI analysis unavailable: {str(e)}"
    
    def generate_report(self, architecture: Dict, claude_analysis: str = None):
        """Generate comprehensive architecture report"""
        
        report = []
        report.append("# 🏗️ Discovered Architecture Report")
        report.append(f"\n**Discovery Timestamp:** {architecture['timestamp']}")
        report.append(f"**Discovery Method:** AI-Based Architecture Tracing\n")
        
        # Executive Summary
        report.append("## 📊 Executive Summary\n")
        report.append(f"- **Total Services:** {architecture['metrics']['total_services']}")
        report.append(f"- **Total Dependencies:** {architecture['metrics']['total_dependencies']}")
        report.append(f"- **Total Endpoints:** {architecture['metrics']['total_endpoints']}")
        report.append(f"- **User Journeys Analyzed:** {architecture['metrics']['total_journeys']}\n")
        
        # Discovered Services
        report.append("## 🔍 Discovered Services\n")
        for i, service in enumerate(architecture['services'], 1):
            endpoint_count = len(architecture['service_endpoints'].get(service, []))
            dependency_count = len(architecture['service_dependencies'].get(service, []))
            report.append(f"{i}. **{service}**")
            report.append(f"   - Endpoints: {endpoint_count}")
            report.append(f"   - Calls to: {dependency_count} service(s)")
        
        # Dependencies
        report.append("\n## 🔗 Service Dependencies\n")
        for service, deps in sorted(architecture['service_dependencies'].items()):
            if deps:
                report.append(f"**{service}** → {', '.join(deps)}")
        
        # Endpoints
        report.append("\n## 📍 API Endpoints\n")
        for service, endpoints in sorted(architecture['service_endpoints'].items()):
            report.append(f"\n### {service}")
            for endpoint in sorted(endpoints):
                report.append(f"- `{endpoint}`")
        
        # User Journeys
        report.append("\n## 🛤️ User Journeys\n")
        for journey in architecture['user_journeys']:
            report.append(f"\n### {journey['journey_name']}")
            report.append(f"**Flow:** {' → '.join(journey['services'])}")
            report.append(f"**Correlation ID:** `{journey['correlation_id']}`")
        
        # Claude AI Analysis
        if claude_analysis and "not available" not in claude_analysis.lower():
            report.append("\n## 🤖 AI-Powered Analysis\n")
            report.append(claude_analysis)
        
        # Architecture Diagram (Basic Mermaid)
        report.append("\n## 📈 Architecture Diagram\n")
        report.append("```mermaid")
        report.append("graph TB")
        report.append('    User(["👤 User"])')
        
        # Add services
        for i, service in enumerate(architecture['services'], 1):
            service_id = f"S{i}"
            report.append(f'    {service_id}["{service}"]')
        
        # Add user to first service connection
        if architecture['services']:
            report.append('    User --> S1')
        
        # Add dependencies
        service_to_id = {svc: f"S{i+1}" for i, svc in enumerate(architecture['services'])}
        for service, deps in architecture['service_dependencies'].items():
            src_id = service_to_id.get(service)
            if src_id:
                for dep in deps:
                    dst_id = service_to_id.get(dep)
                    if dst_id:
                        report.append(f"    {src_id} --> {dst_id}")
        
        report.append("```")
        
        return "\n".join(report)
    
    def save_outputs(self, architecture: Dict, report: str):
        """Save all outputs to files"""
        
        print("\n" + "="*60)
        print("💾 SAVING OUTPUTS")
        print("="*60 + "\n")
        
        # 1. Save discovered architecture (JSON)
        with open('discovered_architecture.json', 'w') as f:
            json.dump(architecture, f, indent=2)
        print("✅ Saved: discovered_architecture.json")
        
        # 2. Save journey details (JSON)
        journey_details = {
            journey['correlation_id']: journey 
            for journey in architecture['user_journeys']
        }
        with open('journey_details.json', 'w') as f:
            json.dump(journey_details, f, indent=2)
        print("✅ Saved: journey_details.json")
        
        # 3. Save architecture report (Markdown)
        with open('architecture_report.md', 'w') as f:
            f.write(report)
        print("✅ Saved: architecture_report.md")
        
        print("\n" + "="*60)
        print("✅ ALL OUTPUTS SAVED SUCCESSFULLY")
        print("="*60)


def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("🚀 AI-BASED ARCHITECTURE TRACER")
    print("AI-Powered Microservices Discovery")
    print("="*60 + "\n")
    
    # Initialize tracer
    # tracer = AgenticArchitectureTracer()
    tracer = ArchitectureTracer()

    # Load correlation IDs
    print("📂 Loading correlation IDs from user journeys...")
    try:
        with open('correlation_ids.json', 'r') as f:
            data = json.load(f)
            journeys = data.get('journeys', [])
            correlation_ids = [(j['name'], j['correlation_id']) for j in journeys]
        print(f"✅ Loaded {len(correlation_ids)} correlation IDs\n")
    except FileNotFoundError:
        print("❌ Error: correlation_ids.json not found!")
        print("   Please run user_journey_simulator.py first.")
        return
    except Exception as e:
        print(f"❌ Error loading correlation IDs: {str(e)}")
        return
    
    # Process all journeys (autonomous discovery)
    tracer.process_all_correlation_ids(correlation_ids)
    
    # Build complete architecture map
    print("\n🗺️  Building complete architecture map...")
    architecture = tracer.build_architecture_map()
    print("✅ Architecture map built!\n")
    
    # Claude AI analysis (optional)
    claude_analysis = tracer.use_claude_for_analysis(architecture)
    
    # Generate report
    print("📝 Generating comprehensive report...")
    report = tracer.generate_report(architecture, claude_analysis)
    print("✅ Report generated!\n")
    
    # Save all outputs
    tracer.save_outputs(architecture, report)
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 ARCHITECTURE DISCOVERY COMPLETE!")
    print("="*60)
    print(f"\n📊 Discovered:")
    print(f"   • {architecture['metrics']['total_services']} Services")
    print(f"   • {architecture['metrics']['total_dependencies']} Dependencies")
    print(f"   • {architecture['metrics']['total_endpoints']} API Endpoints")
    print(f"   • {architecture['metrics']['total_journeys']} User Journeys")
    print(f"\n📁 Output Files:")
    print(f"   • discovered_architecture.json")
    print(f"   • journey_details.json")
    print(f"   • architecture_report.md")
    print(f"\n🔍 Next Steps:")
    print(f"   • View architecture: cat architecture_report.md")
    print(f"   • Generate enhanced diagrams: python enhanced_diagram_generator.py")
    print(f"   • Track drift: python advanced_drift_tracker.py")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()