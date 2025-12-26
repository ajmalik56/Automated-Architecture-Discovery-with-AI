"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Drift Detector
Compares two architecture snapshots to detect changes
"""

import json
import sys
from datetime import datetime


class ArchitectureDriftDetector:
    """
    Detects drift between two architecture snapshots
    Calculates severity and generates change reports
    """
    
    def __init__(self):
        self.changes = {
            'services_added': [],
            'services_removed': [],
            'dependencies_added': [],
            'dependencies_removed': [],
            'endpoints_added': [],
            'endpoints_removed': []
        }
        self.drift_score = 0
        self.severity = 'NO_CHANGE'
    
    def load_architecture(self, filepath):
        """Load an architecture snapshot"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File not found: {filepath}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in file: {filepath}")
            return None
    
    def compare_architectures(self, baseline, current):
        """Compare two architecture snapshots"""
        
        print("\n" + "="*60)
        print("🔍 DRIFT DETECTION ANALYSIS")
        print("="*60 + "\n")
        
        # Compare services
        baseline_services = set(baseline.get('services', []))
        current_services = set(current.get('services', []))
        
        self.changes['services_added'] = list(current_services - baseline_services)
        self.changes['services_removed'] = list(baseline_services - current_services)
        
        # Compare dependencies
        baseline_deps = self._flatten_dependencies(baseline.get('service_dependencies', {}))
        current_deps = self._flatten_dependencies(current.get('service_dependencies', {}))
        
        self.changes['dependencies_added'] = list(current_deps - baseline_deps)
        self.changes['dependencies_removed'] = list(baseline_deps - current_deps)
        
        # Compare endpoints
        baseline_endpoints = self._flatten_endpoints(baseline.get('service_endpoints', {}))
        current_endpoints = self._flatten_endpoints(current.get('service_endpoints', {}))
        
        self.changes['endpoints_added'] = list(current_endpoints - baseline_endpoints)
        self.changes['endpoints_removed'] = list(baseline_endpoints - current_endpoints)
        
        # Calculate drift score
        self._calculate_drift_score()
        
        return self.changes
    
    def _flatten_dependencies(self, dependencies_dict):
        """Flatten dependencies into a set of strings"""
        deps = set()
        for src, targets in dependencies_dict.items():
            for target in targets:
                deps.add(f"{src} -> {target}")
        return deps
    
    def _flatten_endpoints(self, endpoints_dict):
        """Flatten endpoints into a set of strings"""
        eps = set()
        for service, endpoints in endpoints_dict.items():
            for endpoint in endpoints:
                eps.add(f"{service}:{endpoint}")
        return eps
    
    def _calculate_drift_score(self):
        """
        Calculate drift score (0-100)
        Higher score = more severe changes
        """
        
        # Weighted scoring
        score = 0
        score += len(self.changes['services_added']) * 15        # New services are significant
        score += len(self.changes['services_removed']) * 20      # Removed services are critical
        score += len(self.changes['dependencies_added']) * 7     # New dependencies matter
        score += len(self.changes['dependencies_removed']) * 10  # Broken deps are concerning
        score += len(self.changes['endpoints_added']) * 3        # New APIs are minor
        score += len(self.changes['endpoints_removed']) * 5      # Removed APIs need attention
        
        self.drift_score = min(score, 100)  # Cap at 100
        
        # Determine severity
        if self.drift_score == 0:
            self.severity = 'NO_CHANGE'
        elif self.drift_score < 20:
            self.severity = 'LOW'
        elif self.drift_score < 50:
            self.severity = 'MEDIUM'
        elif self.drift_score < 80:
            self.severity = 'HIGH'
        else:
            self.severity = 'CRITICAL'
    
    def generate_report(self, baseline_path, current_path):
        """Generate a comprehensive drift report"""
        
        report = []
        report.append("="*60)
        report.append("📊 ARCHITECTURE DRIFT REPORT")
        report.append("="*60)
        report.append("")
        report.append(f"Baseline:  {baseline_path}")
        report.append(f"Current:   {current_path}")
        report.append(f"Timestamp: {datetime.utcnow().isoformat()}")
        report.append("")
        
        # Drift Score
        report.append("="*60)
        report.append("🎯 DRIFT SCORE & SEVERITY")
        report.append("="*60)
        report.append("")
        report.append(f"Drift Score: {self.drift_score}/100")
        report.append(f"Severity:    {self.severity}")
        report.append("")
        
        severity_descriptions = {
            'NO_CHANGE': '✅ No changes detected',
            'LOW': '🟢 Minor changes - Document for reference',
            'MEDIUM': '🟡 Moderate changes - Review recommended',
            'HIGH': '🟠 Significant changes - Action required',
            'CRITICAL': '🔴 Critical changes - Immediate review needed'
        }
        
        report.append(f"Impact: {severity_descriptions.get(self.severity, 'Unknown')}")
        report.append("")
        
        # Services Changes
        if self.changes['services_added'] or self.changes['services_removed']:
            report.append("="*60)
            report.append("🔧 SERVICE CHANGES")
            report.append("="*60)
            report.append("")
            
            if self.changes['services_added']:
                report.append("✅ Services Added:")
                for service in self.changes['services_added']:
                    report.append(f"   • {service}")
                report.append("")
            
            if self.changes['services_removed']:
                report.append("❌ Services Removed:")
                for service in self.changes['services_removed']:
                    report.append(f"   • {service}")
                report.append("")
        
        # Dependencies Changes
        if self.changes['dependencies_added'] or self.changes['dependencies_removed']:
            report.append("="*60)
            report.append("🔗 DEPENDENCY CHANGES")
            report.append("="*60)
            report.append("")
            
            if self.changes['dependencies_added']:
                report.append("✅ Dependencies Added:")
                for dep in self.changes['dependencies_added']:
                    report.append(f"   • {dep}")
                report.append("")
            
            if self.changes['dependencies_removed']:
                report.append("❌ Dependencies Removed:")
                for dep in self.changes['dependencies_removed']:
                    report.append(f"   • {dep}")
                report.append("")
        
        # Endpoints Changes
        if self.changes['endpoints_added'] or self.changes['endpoints_removed']:
            report.append("="*60)
            report.append("📍 ENDPOINT CHANGES")
            report.append("="*60)
            report.append("")
            
            if self.changes['endpoints_added']:
                report.append("✅ Endpoints Added:")
                for endpoint in self.changes['endpoints_added']:
                    report.append(f"   • {endpoint}")
                report.append("")
            
            if self.changes['endpoints_removed']:
                report.append("❌ Endpoints Removed:")
                for endpoint in self.changes['endpoints_removed']:
                    report.append(f"   • {endpoint}")
                report.append("")
        
        # No Changes
        if self.drift_score == 0:
            report.append("="*60)
            report.append("✅ NO CHANGES DETECTED")
            report.append("="*60)
            report.append("")
            report.append("Architecture is stable - no drift from baseline.")
            report.append("")
        
        # Recommendations
        report.append("="*60)
        report.append("💡 RECOMMENDATIONS")
        report.append("="*60)
        report.append("")
        
        if self.severity == 'NO_CHANGE':
            report.append("• No action required")
        elif self.severity == 'LOW':
            report.append("• Document changes in architecture notes")
            report.append("• Update diagrams if needed")
        elif self.severity == 'MEDIUM':
            report.append("• Review changes with team")
            report.append("• Update documentation")
            report.append("• Verify intended changes")
        elif self.severity == 'HIGH':
            report.append("• Immediate team review required")
            report.append("• Validate all changes are authorized")
            report.append("• Update monitoring and alerts")
            report.append("• Brief stakeholders")
        else:  # CRITICAL
            report.append("• 🚨 URGENT: Immediate review required")
            report.append("• Validate changes are intentional")
            report.append("• Check for security implications")
            report.append("• Update all documentation")
            report.append("• Alert stakeholders immediately")
        
        report.append("")
        report.append("="*60)
        
        return "\n".join(report)


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("🔍 ARCHITECTURE DRIFT DETECTOR")
    print("="*60 + "\n")
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python drift_detector.py <baseline.json> <current.json>")
        print("")
        print("Example:")
        print("  python drift_detector.py baseline_architecture.json discovered_architecture.json")
        print("")
        print("This will compare two architecture snapshots and detect drift.")
        print("")
        return
    
    baseline_path = sys.argv[1]
    current_path = sys.argv[2]
    
    print(f"📂 Loading architectures...")
    print(f"   Baseline: {baseline_path}")
    print(f"   Current:  {current_path}")
    print("")
    
    # Initialize detector
    detector = ArchitectureDriftDetector()
    
    # Load architectures
    baseline = detector.load_architecture(baseline_path)
    current = detector.load_architecture(current_path)
    
    if not baseline or not current:
        print("❌ Failed to load architecture files")
        return
    
    print("✅ Architectures loaded successfully\n")
    
    # Compare
    detector.compare_architectures(baseline, current)
    
    # Generate report
    report = detector.generate_report(baseline_path, current_path)
    
    # Print report
    print(report)
    
    # Save report to file
    report_filename = f"drift_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"\n💾 Report saved to: {report_filename}\n")
    
    # Exit with appropriate code
    if detector.severity in ['HIGH', 'CRITICAL']:
        sys.exit(1)  # Non-zero exit for CI/CD integration
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()