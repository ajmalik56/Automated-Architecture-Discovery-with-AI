"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Master Orchestrator
One-click architecture discovery pipeline execution
Coordinates all components for complete automated discovery
"""

import subprocess
import sys
import time
import json
import os
from datetime import datetime
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class MasterOrchestrator:
    """Orchestrates the complete architecture discovery pipeline"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            'health_check': False,
            'journeys': False,
            'discovery': False,
            'diagrams': False,
            'drift': False
        }
        self.errors = []
        
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
        print(f"{text}")
        print(f"{'='*60}{Colors.ENDC}\n")
        
    def print_step(self, step_num, text):
        """Print step header"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[Step {step_num}] {text}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.ENDC}")
        
    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
        
    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.RED}✗ {text}{Colors.ENDC}")
        
    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")
        
    def check_health(self):
        """Check if all services are healthy"""
        self.print_step(1, "Health Check - Verifying Services")
        
        services = [
            ('Splunk Logger', 'http://localhost:8088/health'),
            ('Auth Service', 'http://localhost:5001/health'),
            ('Product Service', 'http://localhost:5002/health'),
            ('Order Service', 'http://localhost:5003/health'),
            ('Payment Service', 'http://localhost:5004/health'),
            ('Loyalty Service', 'http://localhost:5005/health'),
            ('Policy Service', 'http://localhost:5006/health')
        ]
        
        try:
            import requests
            all_healthy = True
            
            for name, url in services:
                try:
                    response = requests.get(url, timeout=2)
                    if response.status_code == 200:
                        self.print_success(f"{name} is healthy")
                    else:
                        self.print_error(f"{name} returned status {response.status_code}")
                        all_healthy = False
                except Exception as e:
                    self.print_error(f"{name} is not responding: {str(e)}")
                    all_healthy = False
                    
            if all_healthy:
                self.print_success("All services are healthy!")
                self.results['health_check'] = True
                return True
            else:
                self.print_error("Some services are not healthy")
                self.errors.append("Health check failed")
                return False
                
        except ImportError:
            self.print_error("requests library not found")
            self.errors.append("Missing requests library")
            return False
            
    def run_user_journeys(self):
        """Execute user journey simulator"""
        self.print_step(2, "Running User Journeys")
        
        try:
            result = subprocess.run(
                ['python', 'user_journey_simulator.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.print_success("User journeys completed successfully")
                
                # Verify correlation IDs file was created
                if Path('correlation_ids.json').exists():
                    with open('correlation_ids.json', 'r') as f:
                        ids = json.load(f)
                        self.print_success(f"Generated {len(ids)} correlation IDs")
                        self.results['journeys'] = True
                        return True
                else:
                    self.print_error("correlation_ids.json not found")
                    self.errors.append("Correlation IDs file not created")
                    return False
            else:
                self.print_error("User journey simulator failed")
                self.print_error(result.stderr)
                self.errors.append(f"Journey simulator error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("User journey simulator timed out")
            self.errors.append("Journey simulator timeout")
            return False
        except Exception as e:
            self.print_error(f"Error running journeys: {str(e)}")
            self.errors.append(f"Journey execution error: {str(e)}")
            return False
            
    def run_architecture_discovery(self):
        """Execute architecture tracer for architecture discovery"""
        self.print_step(3, "Discovering Architecture with AI")
        
        try:
            result = subprocess.run(
                ['python', 'architecture_tracer.py'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.print_success("Architecture discovery completed")
                
                # Verify output files were created
                required_files = [
                    'discovered_architecture.json',
                    'journey_details.json',
                    'architecture_report.md'
                ]
                
                all_created = True
                for file in required_files:
                    if Path(file).exists():
                        self.print_success(f"Generated {file}")
                    else:
                        self.print_error(f"Missing {file}")
                        all_created = False
                        
                if all_created:
                    # Load and display summary
                    try:
                        with open('discovered_architecture.json', 'r') as f:
                            arch = json.load(f)
                            
                        total_services = arch.get('total_services', len(arch.get('services', [])))
                        
                        # Try multiple possible keys for dependencies
                        deps = arch.get('dependencies', 
                                    arch.get('service_dependencies', 
                                    arch.get('deps', {})))
                        num_deps = len(deps) if deps else 0
                        
                        total_endpoints = arch.get('total_endpoints', 
                                                len(arch.get('endpoints', [])))
                        
                        self.print_success(f"Discovered {total_services} services")
                        self.print_success(f"Mapped {num_deps} dependencies")  
                        self.print_success(f"Cataloged {total_endpoints} endpoints")
                        self.results['discovery'] = True
                        return True
                        
                    except Exception as e:
                        self.print_warning(f"Could not parse architecture details: {e}")
                        self.print_success("Architecture files generated successfully")
                        self.results['discovery'] = True
                        return True
                else:
                    self.errors.append("Architecture discovery incomplete")
                    return False
            else:
                self.print_error("Architecture discovery failed")
                self.print_error(result.stderr)
                self.errors.append(f"Discovery error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("Architecture discovery timed out")
            self.errors.append("Discovery timeout")
            return False
        except Exception as e:
            self.print_error(f"Error during discovery: {str(e)}")
            self.errors.append(f"Discovery execution error: {str(e)}")
            return False
            
    def generate_diagrams(self):
        """Generate enhanced diagrams"""
        self.print_step(4, "Generating Enhanced Diagrams")
        
        try:
            result = subprocess.run(
                ['python', 'enhanced_diagram_generator.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.print_success("Enhanced diagrams generated")
                
                # Verify diagram file was created
                if Path('complete_annotated_architecture.md').exists():
                    file_size = Path('complete_annotated_architecture.md').stat().st_size
                    self.print_success(f"Generated complete_annotated_architecture.md ({file_size} bytes)")
                    self.results['diagrams'] = True
                    return True
                else:
                    self.print_error("Diagram file not created")
                    self.errors.append("Diagram generation incomplete")
                    return False
            else:
                self.print_error("Diagram generation failed")
                self.print_error(result.stderr)
                self.errors.append(f"Diagram error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("Diagram generation timed out")
            self.errors.append("Diagram timeout")
            return False
        except Exception as e:
            self.print_error(f"Error generating diagrams: {str(e)}")
            self.errors.append(f"Diagram generation error: {str(e)}")
            return False
            
    def track_drift(self):
        """Run drift tracking"""
        self.print_step(5, "Tracking Architectural Drift")
        
        try:
            result = subprocess.run(
                ['python', 'advanced_drift_tracker.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.print_success("Drift tracking completed")
                
                # Check if drift history exists
                if Path('architecture_history').exists():
                    snapshots = list(Path('architecture_history').glob('snapshot_*.json'))
                    self.print_success(f"Total snapshots: {len(snapshots)}")
                    
                    # Check for drift report
                    if Path('architecture_history/drift_trend_report.txt').exists():
                        self.print_success("Drift trend report generated")
                        
                    self.results['drift'] = True
                    return True
                else:
                    self.print_warning("Drift history not found (first run?)")
                    self.results['drift'] = True  # Not an error on first run
                    return True
            else:
                self.print_error("Drift tracking failed")
                self.print_error(result.stderr)
                self.errors.append(f"Drift tracking error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("Drift tracking timed out")
            self.errors.append("Drift tracking timeout")
            return False
        except Exception as e:
            self.print_error(f"Error tracking drift: {str(e)}")
            self.errors.append(f"Drift tracking error: {str(e)}")
            return False
            
    def generate_final_report(self):
        """Generate comprehensive execution report"""
        self.print_header("📊 EXECUTION SUMMARY")
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print(f"{Colors.BOLD}Execution Time:{Colors.ENDC} {duration:.2f} seconds")
        print(f"{Colors.BOLD}Timestamp:{Colors.ENDC} {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Results summary
        print(f"{Colors.BOLD}Pipeline Results:{Colors.ENDC}")
        for step, success in self.results.items():
            status = f"{Colors.GREEN}✓ PASSED{Colors.ENDC}" if success else f"{Colors.RED}✗ FAILED{Colors.ENDC}"
            print(f"  {step.replace('_', ' ').title()}: {status}")
        print()
        
        # Overall status
        all_passed = all(self.results.values())
        if all_passed:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL STEPS COMPLETED SUCCESSFULLY!{Colors.ENDC}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️  PIPELINE COMPLETED WITH ERRORS{Colors.ENDC}")
            print(f"\n{Colors.RED}Errors encountered:{Colors.ENDC}")
            for error in self.errors:
                print(f"  • {error}")
        print()
        
        # Output files
        print(f"{Colors.BOLD}Generated Files:{Colors.ENDC}")
        output_files = [
            'correlation_ids.json',
            'discovered_architecture.json',
            'journey_details.json',
            'architecture_report.md',
            'complete_annotated_architecture.md'
        ]
        
        for file in output_files:
            if Path(file).exists():
                size = Path(file).stat().st_size
                print(f"  {Colors.GREEN}✓{Colors.ENDC} {file} ({size:,} bytes)")
            else:
                print(f"  {Colors.RED}✗{Colors.ENDC} {file} (not found)")
        print()
        
        # Drift snapshots
        if Path('architecture_history').exists():
            snapshots = list(Path('architecture_history').glob('snapshot_*.json'))
            print(f"{Colors.BOLD}Drift Snapshots:{Colors.ENDC} {len(snapshots)} total")
            print()
        
        # Next steps
        if all_passed:
            print(f"{Colors.BOLD}📁 Next Steps:{Colors.ENDC}")
            print(f"  • View architecture: {Colors.CYAN}cat architecture_report.md{Colors.ENDC}")
            print(f"  • View diagrams: {Colors.CYAN}cat complete_annotated_architecture.md{Colors.ENDC}")
            print(f"  • Check drift: {Colors.CYAN}cat architecture_history/drift_trend_report.txt{Colors.ENDC}")
        
        print(f"\n{Colors.BLUE}{'='*60}{Colors.ENDC}\n")
        
        return all_passed
        
    def run(self):
        """Execute complete pipeline"""
        self.print_header("🚀 MASTER ORCHESTRATOR - Architecture Discovery Pipeline")
        
        print(f"{Colors.BOLD}Starting automated architecture discovery...{Colors.ENDC}\n")
        
        # Step 1: Health Check
        if not self.check_health():
            self.print_error("Health check failed. Aborting pipeline.")
            self.generate_final_report()
            return False
            
        time.sleep(2)
        
        # Step 2: Run User Journeys
        if not self.run_user_journeys():
            self.print_error("User journeys failed. Aborting pipeline.")
            self.generate_final_report()
            return False
            
        time.sleep(2)
        
        # Step 3: Discover Architecture
        if not self.run_architecture_discovery():
            self.print_error("Architecture discovery failed. Aborting pipeline.")
            self.generate_final_report()
            return False
            
        time.sleep(2)
        
        # Step 4: Generate Diagrams
        if not self.generate_diagrams():
            self.print_warning("Diagram generation failed. Continuing...")
            
        time.sleep(2)
        
        # Step 5: Track Drift
        if not self.track_drift():
            self.print_warning("Drift tracking failed. Continuing...")
            
        # Final Report
        return self.generate_final_report()

def main():
    """Main entry point"""
    try:
        orchestrator = MasterOrchestrator()
        success = orchestrator.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Pipeline interrupted by user{Colors.ENDC}\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n{Colors.RED}✗ Fatal error: {str(e)}{Colors.ENDC}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()