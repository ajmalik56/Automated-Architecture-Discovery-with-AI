"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Enhanced Diagram Generator
Generates comprehensive annotated architecture diagrams with:
- Call frequencies
- Endpoint details
- Critical path highlighting
- Dependency matrix
- Complete API catalog
"""

import json
from collections import defaultdict, Counter
from datetime import datetime


class ComprehensiveArchitectureDiagramGenerator:
    """
    Generates complete annotated architecture diagrams with all flows and metrics
    """
    
    def __init__(self):
        self.architecture = {}
        self.journey_details = {}
        self.service_call_counts = Counter()
        self.endpoint_call_counts = Counter()
        self.dependency_call_counts = Counter()
        self.http_methods = {}
        
    def load_data(self):
        """Load discovered architecture and journey details"""
        print("\n" + "="*60)
        print("📂 LOADING ARCHITECTURE DATA")
        print("="*60 + "\n")
        
        # Load discovered architecture
        try:
            with open('discovered_architecture.json', 'r') as f:
                self.architecture = json.load(f)
            print("✅ Loaded: discovered_architecture.json")
        except FileNotFoundError:
            print("❌ Error: discovered_architecture.json not found!")
            print("   Please run architecture_tracer.py first.")
            return False
        
        # Load journey details
        try:
            with open('journey_details.json', 'r') as f:
                self.journey_details = json.load(f)
            print("✅ Loaded: journey_details.json")
        except FileNotFoundError:
            print("⚠️  Warning: journey_details.json not found!")
            print("   Some detailed metrics will be unavailable.")
        
        print()
        return True
    
    def analyze_flows(self):
        """Analyze all flows to count calls and dependencies"""
        print("="*60)
        print("🔍 ANALYZING FLOWS AND METRICS")
        print("="*60 + "\n")
        
        # Process each journey to count calls
        for correlation_id, journey_data in self.journey_details.items():
            journey_name = journey_data.get('journey_name', 'Unknown')
            print(f"📊 Analyzing: {journey_name}")
            
            # Count service calls
            services_in_journey = journey_data.get('services', [])
            for service in services_in_journey:
                self.service_call_counts[service] += 1
            
            # Count endpoint calls and extract HTTP methods
            endpoints = journey_data.get('endpoints', [])
            for endpoint_info in endpoints:
                service = endpoint_info.get('service')
                endpoint = endpoint_info.get('endpoint')
                
                if service and endpoint:
                    key = f"{service}:{endpoint}"
                    self.endpoint_call_counts[key] += 1
                    
                    # Infer HTTP method from endpoint path
                    if 'login' in endpoint or 'create' in endpoint or 'process' in endpoint:
                        self.http_methods[key] = 'POST'
                    else:
                        self.http_methods[key] = 'GET'
            
            # Count dependencies
            for i in range(len(services_in_journey) - 1):
                src = services_in_journey[i]
                dst = services_in_journey[i + 1]
                dep_key = f"{src} -> {dst}"
                self.dependency_call_counts[dep_key] += 1
        
        print(f"\n✅ Analysis complete!")
        print(f"   • Service calls tracked: {len(self.service_call_counts)}")
        print(f"   • Endpoint calls tracked: {len(self.endpoint_call_counts)}")
        print(f"   • Dependencies tracked: {len(self.dependency_call_counts)}")
        print()
    
    def generate_complete_annotated_diagram(self):
        """Generate the master annotated architecture diagram"""
        
        mermaid = []
        mermaid.append("# 🏗️ Complete Annotated Architecture")
        mermaid.append(f"\n**Generated:** {datetime.utcnow().isoformat()}")
        mermaid.append(f"**Discovery Method:** AI-Based Tracing with Complete Annotations\n")
        
        # Statistics
        mermaid.append("## 📊 Architecture Statistics\n")
        mermaid.append(f"- **Total Services:** {self.architecture['metrics']['total_services']}")
        mermaid.append(f"- **Total Dependencies:** {self.architecture['metrics']['total_dependencies']}")
        mermaid.append(f"- **Total Endpoints:** {self.architecture['metrics']['total_endpoints']}")
        mermaid.append(f"- **Total User Journeys:** {self.architecture['metrics']['total_journeys']}")
        mermaid.append(f"- **Total Service Calls:** {sum(self.service_call_counts.values())}")
        mermaid.append(f"- **Total Endpoint Calls:** {sum(self.endpoint_call_counts.values())}\n")
        
        # Complete Architecture Diagram
        mermaid.append("## 🎨 Complete Architecture Diagram\n")
        mermaid.append("**Legend:**")
        mermaid.append("- `==>` Critical path (3+ calls)")
        mermaid.append("- `-->` Frequent path (2 calls)")
        mermaid.append("- `-.->` Normal path (1 call)")
        mermaid.append("- `📊 X calls` Service call count")
        mermaid.append("- `🔗 X endpoints` Number of endpoints\n")
        
        mermaid.append("```mermaid")
        mermaid.append("graph TB")
        
        # User node
        mermaid.append('    User(["👤 User/Browser<br/>Entry Point"])')
        
        # Service nodes with annotations
        services = self.architecture.get('services', [])
        service_to_id = {}
        
        for i, service in enumerate(services, 1):
            service_id = f"S{i}"
            service_to_id[service] = service_id
            
            # Get metrics
            call_count = self.service_call_counts.get(service, 0)
            endpoint_count = len(self.architecture.get('service_endpoints', {}).get(service, []))
            
            # Create annotated label
            display_name = service.replace('-service', '').title()
            mermaid.append(f'    {service_id}["{display_name} Service<br/>━━━━━━━━<br/>📊 {call_count} calls<br/>🔗 {endpoint_count} endpoints"]')
        
        # User to first service (always auth)
        if 'auth-service' in service_to_id:
            mermaid.append(f'    User ==>|"All journeys<br/>start here"| {service_to_id["auth-service"]}')
        
        # Dependencies with frequency annotations
        dependencies = self.architecture.get('service_dependencies', {})
        
        for src_service, dest_services in dependencies.items():
            src_id = service_to_id.get(src_service)
            if not src_id:
                continue
            
            for dest_service in dest_services:
                dst_id = service_to_id.get(dest_service)
                if not dst_id:
                    continue
                
                # Count calls for this dependency
                dep_key = f"{src_service} -> {dest_service}"
                call_count = self.dependency_call_counts.get(dep_key, 0)
                
                # Choose arrow style based on frequency
                if call_count >= 3:
                    arrow = "==>"
                    label = f"{call_count} calls<br/>(critical)"
                    style_class = "critical"
                elif call_count >= 2:
                    arrow = "-->"
                    label = f"{call_count} calls<br/>(frequent)"
                    style_class = "frequent"
                else:
                    arrow = ".->"
                    label = f"{call_count} call"
                    style_class = "normal"
                
                mermaid.append(f'    {src_id} {arrow}|"{label}"| {dst_id}')
        
        # Endpoint subgraphs
        mermaid.append("\n    %% Endpoint Details")
        
        for service in services:
            endpoints = self.architecture.get('service_endpoints', {}).get(service, [])
            if endpoints:
                service_id = service_to_id[service]
                display_name = service.replace('-service', '').title()
                
                mermaid.append(f'\n    subgraph {service_id}_endpoints["{display_name} Endpoints"]')
                
                for j, endpoint in enumerate(sorted(endpoints), 1):
                    endpoint_key = f"{service}:{endpoint}"
                    call_count = self.endpoint_call_counts.get(endpoint_key, 0)
                    http_method = self.http_methods.get(endpoint_key, 'GET')
                    
                    endpoint_id = f"{service_id}_E{j}"
                    endpoint_display = endpoint.replace('/api/', '').replace('{', '').replace('}', '')
                    
                    mermaid.append(f'        {endpoint_id}["{http_method} {endpoint}<br/>📈 {call_count} calls"]')
                
                mermaid.append("    end")
                mermaid.append(f"    {service_id} -.-> {service_id}_endpoints")
        
        # Styles
        mermaid.append("\n    %% Styling")
        mermaid.append("    classDef authStyle fill:#e1f5ff,stroke:#01579b,stroke-width:3px")
        mermaid.append("    classDef productStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px")
        mermaid.append("    classDef orderStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px")
        mermaid.append("    classDef paymentStyle fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px")
        mermaid.append("    classDef loyaltyStyle fill:#fce4ec,stroke:#880e4f,stroke-width:2px")
        mermaid.append("    classDef policyStyle fill:#f1f8e9,stroke:#33691e,stroke-width:2px")
        mermaid.append("    classDef endpointStyle fill:#fffde7,stroke:#f57f17,stroke-width:1px")
        
        # Apply styles
        for service, service_id in service_to_id.items():
            if 'auth' in service:
                mermaid.append(f"    class {service_id} authStyle")
            elif 'product' in service:
                mermaid.append(f"    class {service_id} productStyle")
            elif 'order' in service:
                mermaid.append(f"    class {service_id} orderStyle")
            elif 'payment' in service:
                mermaid.append(f"    class {service_id} paymentStyle")
            elif 'loyalty' in service:
                mermaid.append(f"    class {service_id} loyaltyStyle")
            elif 'policy' in service:
                mermaid.append(f"    class {service_id} policyStyle")
        
        mermaid.append("```\n")
        
        return "\n".join(mermaid)
    
    def generate_dependency_matrix(self):
        """Generate dependency matrix table"""
        
        matrix = []
        matrix.append("## 📋 Dependency Matrix\n")
        matrix.append("**Legend:** 🔴 Critical (3+ calls) | 🟡 Frequent (2 calls) | 🟢 Normal (1 call) | - No dependency\n")
        
        services = sorted(self.architecture.get('services', []))
        dependencies = self.architecture.get('service_dependencies', {})
        
        # Header
        header = "| From / To |"
        for service in services:
            display = service.replace('-service', '').title()[:8]  # Truncate for table
            header += f" {display} |"
        matrix.append(header)
        
        # Separator
        separator = "|-----------|"
        for _ in services:
            separator += "---------|"
        matrix.append(separator)
        
        # Rows
        for src_service in services:
            src_display = src_service.replace('-service', '').title()
            row = f"| **{src_display}** |"
            
            for dst_service in services:
                if src_service == dst_service:
                    row += " - |"
                    continue
                
                # Check if dependency exists
                dest_services = dependencies.get(src_service, [])
                if dst_service in dest_services:
                    # Count calls
                    dep_key = f"{src_service} -> {dst_service}"
                    call_count = self.dependency_call_counts.get(dep_key, 0)
                    
                    if call_count >= 3:
                        row += f" 🔴 {call_count} |"
                    elif call_count >= 2:
                        row += f" 🟡 {call_count} |"
                    else:
                        row += f" 🟢 {call_count} |"
                else:
                    row += " - |"
            
            matrix.append(row)
        
        matrix.append("")
        return "\n".join(matrix)
    
    def generate_api_catalog(self):
        """Generate complete API catalog"""
        
        catalog = []
        catalog.append("## 📚 Complete API Catalog\n")
        
        service_endpoints = self.architecture.get('service_endpoints', {})
        
        for service in sorted(service_endpoints.keys()):
            display_name = service.replace('-service', '').title()
            catalog.append(f"\n### {display_name} Service\n")
            
            endpoints = sorted(service_endpoints[service])
            
            # Table header
            catalog.append("| HTTP Method | Endpoint | Calls | Description |")
            catalog.append("|-------------|----------|-------|-------------|")
            
            for endpoint in endpoints:
                endpoint_key = f"{service}:{endpoint}"
                call_count = self.endpoint_call_counts.get(endpoint_key, 0)
                http_method = self.http_methods.get(endpoint_key, 'GET')
                
                # Generate description
                if 'login' in endpoint:
                    description = "User authentication"
                elif 'search' in endpoint:
                    description = "Search resources"
                elif 'create' in endpoint:
                    description = "Create new resource"
                elif 'history' in endpoint:
                    description = "Retrieve history"
                elif 'process' in endpoint:
                    description = "Process transaction"
                elif 'points' in endpoint:
                    description = "Get loyalty points"
                elif 'policies' in endpoint:
                    description = "Retrieve policy document"
                elif '{id}' in endpoint or '{type}' in endpoint:
                    description = "Get specific resource"
                else:
                    description = "API endpoint"
                
                catalog.append(f"| `{http_method}` | `{endpoint}` | {call_count} | {description} |")
            
            catalog.append("")
        
        return "\n".join(catalog)
    
    def generate_sequence_diagrams(self):
        """Generate detailed sequence diagrams for each journey"""
        
        diagrams = []
        diagrams.append("## 🔄 User Journey Sequence Diagrams\n")
        
        for correlation_id, journey_data in self.journey_details.items():
            journey_name = journey_data.get('journey_name', 'Unknown Journey')
            services = journey_data.get('services', [])
            endpoints = journey_data.get('endpoints', [])
            
            diagrams.append(f"\n### {journey_name}\n")
            diagrams.append(f"**Correlation ID:** `{correlation_id}`")
            diagrams.append(f"**Flow:** {' → '.join([s.replace('-service', '').title() for s in services])}\n")
            
            diagrams.append("```mermaid")
            diagrams.append("sequenceDiagram")
            diagrams.append("    participant User")
            
            # Add participants
            unique_services = []
            for service in services:
                if service not in unique_services:
                    unique_services.append(service)
                    display = service.replace('-service', '').title()
                    diagrams.append(f"    participant {display}")
            
            # Add sequence
            current_service = None
            for i, endpoint_info in enumerate(endpoints, 1):
                service = endpoint_info.get('service')
                endpoint = endpoint_info.get('endpoint')
                
                if not service or not endpoint:
                    continue
                
                service_display = service.replace('-service', '').title()
                endpoint_key = f"{service}:{endpoint}"
                http_method = self.http_methods.get(endpoint_key, 'GET')
                
                if i == 1:
                    # First call from user
                    diagrams.append(f'    User->>+{service_display}: {http_method} {endpoint}')
                    diagrams.append(f'    {service_display}-->>-User: 200 OK')
                else:
                    # Subsequent calls
                    if current_service and current_service != service:
                        current_display = current_service.replace('-service', '').title()
                        diagrams.append(f'    {current_display}->>+{service_display}: {http_method} {endpoint}')
                        diagrams.append(f'    {service_display}-->>-{current_display}: 200 OK')
                    else:
                        diagrams.append(f'    User->>+{service_display}: {http_method} {endpoint}')
                        diagrams.append(f'    {service_display}-->>-User: 200 OK')
                
                current_service = service
            
            diagrams.append("```\n")
        
        return "\n".join(diagrams)
    
    def generate_critical_paths(self):
        """Identify and document critical paths"""
        
        critical = []
        critical.append("## ⚠️ Critical Paths Analysis\n")
        
        # Find most called services
        if self.service_call_counts:
            most_called = self.service_call_counts.most_common(3)
            critical.append("### Most Called Services\n")
            for service, count in most_called:
                display = service.replace('-service', '').title()
                critical.append(f"- **{display} Service**: {count} calls across all journeys")
            critical.append("")
        
        # Find most used endpoints
        if self.endpoint_call_counts:
            most_used = self.endpoint_call_counts.most_common(5)
            critical.append("### Most Used Endpoints\n")
            for endpoint_key, count in most_used:
                service, endpoint = endpoint_key.split(':', 1)
                http_method = self.http_methods.get(endpoint_key, 'GET')
                display = service.replace('-service', '').title()
                critical.append(f"- **{display}**: `{http_method} {endpoint}` - {count} calls")
            critical.append("")
        
        # Find critical dependencies
        if self.dependency_call_counts:
            critical_deps = [(k, v) for k, v in self.dependency_call_counts.items() if v >= 3]
            if critical_deps:
                critical.append("### Critical Dependencies (3+ calls)\n")
                for dep, count in sorted(critical_deps, key=lambda x: x[1], reverse=True):
                    src, dst = dep.split(' -> ')
                    src_display = src.replace('-service', '').title()
                    dst_display = dst.replace('-service', '').title()
                    critical.append(f"- **{src_display} → {dst_display}**: {count} calls")
                critical.append("")
        
        return "\n".join(critical)
    
    def generate_complete_report(self):
        """Generate the complete annotated architecture report"""
        
        print("="*60)
        print("📝 GENERATING COMPLETE ANNOTATED REPORT")
        print("="*60 + "\n")
        
        report_sections = []
        
        # Title and stats
        print("• Generating architecture diagram...")
        report_sections.append(self.generate_complete_annotated_diagram())
        
        # Critical paths
        print("• Analyzing critical paths...")
        report_sections.append(self.generate_critical_paths())
        
        # Dependency matrix
        print("• Creating dependency matrix...")
        report_sections.append(self.generate_dependency_matrix())
        
        # API catalog
        print("• Compiling API catalog...")
        report_sections.append(self.generate_api_catalog())
        
        # Sequence diagrams
        print("• Generating sequence diagrams...")
        report_sections.append(self.generate_sequence_diagrams())
        
        print("\n✅ All sections generated!\n")
        
        return "\n".join(report_sections)
    
    def save_report(self, report):
        """Save the complete annotated report"""
        
        print("="*60)
        print("💾 SAVING COMPLETE ANNOTATED ARCHITECTURE")
        print("="*60 + "\n")
        
        with open('complete_annotated_architecture.md', 'w') as f:
            f.write(report)
        
        print("✅ Saved: complete_annotated_architecture.md\n")
        
        # Print file info
        import os
        file_size = os.path.getsize('complete_annotated_architecture.md')
        print(f"📊 File size: {file_size:,} bytes")
        print(f"📄 Location: {os.path.abspath('complete_annotated_architecture.md')}")
        print()


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("🎨 ENHANCED DIAGRAM GENERATOR")
    print("Complete Annotated Architecture with All Flows")
    print("="*60)
    
    generator = ComprehensiveArchitectureDiagramGenerator()
    
    # Load data
    if not generator.load_data():
        return
    
    # Analyze flows
    generator.analyze_flows()
    
    # Generate complete report
    report = generator.generate_complete_report()
    
    # Save report
    generator.save_report(report)
    
    # Final summary
    print("="*60)
    print("🎉 COMPLETE ANNOTATED ARCHITECTURE GENERATED!")
    print("="*60)
    print("\n📁 Output File:")
    print("   • complete_annotated_architecture.md")
    print("\n📊 Includes:")
    print("   • Complete architecture diagram with annotations")
    print("   • Call frequencies per service and endpoint")
    print("   • Critical paths highlighted (⇒ arrows)")
    print("   • Dependency matrix table")
    print("   • Complete API catalog with HTTP methods")
    print("   • Detailed sequence diagrams for all journeys")
    print("   • Critical paths analysis")
    print("\n🔍 View the complete diagram:")
    print("   cat complete_annotated_architecture.md")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()