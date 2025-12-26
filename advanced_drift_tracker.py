"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Advanced Drift Tracker
Tracks architecture changes over time with historical analysis
"""

import json
import os
import hashlib
from datetime import datetime
from collections import defaultdict


class AdvancedDriftTracker:
    """
    Tracks architecture drift over time
    Maintains history, calculates trends, generates alerts
    """
    
    def __init__(self, history_dir='architecture_history'):
        self.history_dir = history_dir
        self.history_file = os.path.join(history_dir, 'drift_history.json')
        self.history = []
        
        # Create history directory if it doesn't exist
        os.makedirs(history_dir, exist_ok=True)
        
        # Load existing history
        self._load_history()
    
    def _load_history(self):
        """Load drift history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                print(f"✅ Loaded {len(self.history)} historical snapshots")
            except:
                print("⚠️  No previous history found - starting fresh")
                self.history = []
        else:
            print("📝 Creating new drift history")
            self.history = []
    
    def _save_history(self):
        """Save drift history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def calculate_architecture_hash(self, architecture):
        """Calculate hash of architecture for change detection"""
        # Create a stable string representation
        arch_string = json.dumps({
            'services': sorted(architecture.get('services', [])),
            'dependencies': {k: sorted(v) for k, v in architecture.get('service_dependencies', {}).items()},
            'endpoints': {k: sorted(v) for k, v in architecture.get('service_endpoints', {}).items()}
        }, sort_keys=True)
        
        return hashlib.md5(arch_string.encode()).hexdigest()
    
    def capture_snapshot(self):
        """Capture current architecture state as a snapshot"""
        
        print("\n" + "="*60)
        print("📸 CAPTURING ARCHITECTURE SNAPSHOT")
        print("="*60 + "\n")
        
        # Load current architecture
        try:
            with open('discovered_architecture.json', 'r') as f:
                current_arch = json.load(f)
            print("✅ Current architecture loaded\n")
        except FileNotFoundError:
            print("❌ Error: discovered_architecture.json not found")
            print("   Please run architecture_tracer.py first")
            return None
        
        # Calculate hash
        arch_hash = self.calculate_architecture_hash(current_arch)
        
        # Check if this is a duplicate
        if self.history and self.history[-1].get('hash') == arch_hash:
            print("✅ No changes detected - architecture is stable")
            print(f"   Hash: {arch_hash}")
            return None
        
        # Create snapshot
        snapshot = {
            'timestamp': datetime.utcnow().isoformat(),
            'hash': arch_hash,
            'architecture': current_arch,
            'metrics': current_arch.get('metrics', {})
        }
        
        # Detect changes if we have previous snapshots
        changes = {}
        if self.history:
            changes = self._detect_changes(self.history[-1]['architecture'], current_arch)
            snapshot['changes'] = changes
            snapshot['drift_score'] = self._calculate_drift_score(changes)
        else:
            snapshot['changes'] = {'initial_snapshot': True}
            snapshot['drift_score'] = 0
        
        # Add to history
        self.history.append(snapshot)
        
        # Save snapshot to individual file
        snapshot_filename = os.path.join(
            self.history_dir,
            f"snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(snapshot_filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"✅ Snapshot captured: {snapshot_filename}")
        print(f"   Hash: {arch_hash}")
        
        if changes and 'initial_snapshot' not in changes:
            print(f"   Drift Score: {snapshot['drift_score']}/100")
        
        print()
        
        # Save updated history
        self._save_history()
        
        return snapshot
    
    def _detect_changes(self, previous, current):
        """Detect changes between two architectures"""
        
        changes = {}
        
        # Services
        prev_services = set(previous.get('services', []))
        curr_services = set(current.get('services', []))
        
        changes['services_added'] = list(curr_services - prev_services)
        changes['services_removed'] = list(prev_services - curr_services)
        
        # Dependencies
        prev_deps = self._flatten_dependencies(previous.get('service_dependencies', {}))
        curr_deps = self._flatten_dependencies(current.get('service_dependencies', {}))
        
        changes['dependencies_added'] = list(curr_deps - prev_deps)
        changes['dependencies_removed'] = list(prev_deps - curr_deps)
        
        # Endpoints
        prev_endpoints = self._flatten_endpoints(previous.get('service_endpoints', {}))
        curr_endpoints = self._flatten_endpoints(current.get('service_endpoints', {}))
        
        changes['endpoints_added'] = list(curr_endpoints - prev_endpoints)
        changes['endpoints_removed'] = list(prev_endpoints - curr_endpoints)
        
        return changes
    
    def _flatten_dependencies(self, dependencies_dict):
        """Flatten dependencies into a set"""
        deps = set()
        for src, targets in dependencies_dict.items():
            for target in targets:
                deps.add(f"{src} -> {target}")
        return deps
    
    def _flatten_endpoints(self, endpoints_dict):
        """Flatten endpoints into a set"""
        eps = set()
        for service, endpoints in endpoints_dict.items():
            for endpoint in endpoints:
                eps.add(f"{service}:{endpoint}")
        return eps
    
    def _calculate_drift_score(self, changes):
        """Calculate drift score from changes"""
        score = 0
        score += len(changes.get('services_added', [])) * 15
        score += len(changes.get('services_removed', [])) * 20
        score += len(changes.get('dependencies_added', [])) * 7
        score += len(changes.get('dependencies_removed', [])) * 10
        score += len(changes.get('endpoints_added', [])) * 3
        score += len(changes.get('endpoints_removed', [])) * 5
        
        return min(score, 100)
    
    def generate_trend_report(self):
        """Generate trend analysis report"""
        
        print("\n" + "="*60)
        print("📈 DRIFT TREND ANALYSIS")
        print("="*60 + "\n")
        
        if len(self.history) < 2:
            print("⚠️  Not enough historical data for trend analysis")
            print(f"   Current snapshots: {len(self.history)}")
            print("   Need at least 2 snapshots to detect trends")
            return
        
        report = []
        report.append("="*60)
        report.append("📊 ARCHITECTURE DRIFT TRENDS")
        report.append("="*60)
        report.append("")
        
        # Timeline
        first = self.history[0]['timestamp']
        last = self.history[-1]['timestamp']
        report.append(f"Analysis Period: {first} to {last}")
        report.append(f"Total Snapshots: {len(self.history)}")
        report.append("")
        
        # Calculate change frequency
        changes_count = sum(1 for snapshot in self.history if snapshot.get('drift_score', 0) > 0)
        report.append(f"Total Architecture Changes: {changes_count}")
        report.append(f"Stability Rate: {((len(self.history) - changes_count) / len(self.history) * 100):.1f}%")
        report.append("")
        
        # Metrics over time
        report.append("="*60)
        report.append("📈 METRICS TRENDS")
        report.append("="*60)
        report.append("")
        
        first_metrics = self.history[0]['metrics']
        last_metrics = self.history[-1]['metrics']
        
        metrics_comparison = [
            ('Services', 'total_services'),
            ('Dependencies', 'total_dependencies'),
            ('Endpoints', 'total_endpoints'),
            ('Journeys', 'total_journeys')
        ]
        
        report.append("Metric Growth Analysis:")
        report.append("")
        for label, key in metrics_comparison:
            first_val = first_metrics.get(key, 0)
            last_val = last_metrics.get(key, 0)
            change = last_val - first_val
            
            if change > 0:
                report.append(f"  {label}:  {first_val} → {last_val} (+{change})")
            elif change < 0:
                report.append(f"  {label}:  {first_val} → {last_val} ({change})")
            else:
                report.append(f"  {label}:  {first_val} (no change)")
        
        report.append("")
        
        # Recent changes
        if len(self.history) >= 2:
            report.append("="*60)
            report.append("🔍 RECENT CHANGES")
            report.append("="*60)
            report.append("")
            
            recent = self.history[-1]
            if 'changes' in recent and 'initial_snapshot' not in recent['changes']:
                changes = recent['changes']
                
                if changes.get('services_added'):
                    report.append("✅ Services Added:")
                    for service in changes['services_added']:
                        report.append(f"   • {service}")
                    report.append("")
                
                if changes.get('services_removed'):
                    report.append("❌ Services Removed:")
                    for service in changes['services_removed']:
                        report.append(f"   • {service}")
                    report.append("")
                
                if changes.get('dependencies_added'):
                    report.append("✅ Dependencies Added:")
                    for dep in changes['dependencies_added']:
                        report.append(f"   • {dep}")
                    report.append("")
                
                if changes.get('dependencies_removed'):
                    report.append("❌ Dependencies Removed:")
                    for dep in changes['dependencies_removed']:
                        report.append(f"   • {dep}")
                    report.append("")
        
        report.append("="*60)
        
        report_text = "\n".join(report)
        print(report_text)
        
        # Save report
        report_filename = os.path.join(self.history_dir, 'drift_trend_report.txt')
        with open(report_filename, 'w') as f:
            f.write(report_text)
        
        print(f"\n💾 Trend report saved to: {report_filename}\n")


def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("📊 ADVANCED DRIFT TRACKER")
    print("Historical Architecture Analysis")
    print("="*60)
    
    tracker = AdvancedDriftTracker()
    
    # Capture current snapshot
    snapshot = tracker.capture_snapshot()
    
    # Generate trend report
    tracker.generate_trend_report()
    
    print("="*60)
    print("✅ DRIFT TRACKING COMPLETE")
    print("="*60)
    print(f"\n📁 History Directory: architecture_history/")
    print(f"   • drift_history.json - Complete history")
    print(f"   • snapshot_*.json - Individual snapshots")
    print(f"   • drift_trend_report.txt - Latest trends")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()