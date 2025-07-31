#!/usr/bin/env python3
"""
Value Stream Mapping Generator - Demo Script
===========================================

This script demonstrates various capabilities of the VSM Generator including:
- Sample VSM generation
- Custom VSM creation
- Analysis comparison
- Multiple output formats
"""

import os
import sys
from vsm_generator import VSMGenerator, ProcessStep, ValueStreamMap
from datetime import datetime

def demo_sample_vsm():
    """Demonstrate sample VSM generation"""
    print("=" * 60)
    print("DEMO 1: Sample VSM Generation")
    print("=" * 60)
    
    generator = VSMGenerator()
    
    # Generate sample VSM
    sample_vsm = generator.create_sample_vsm()
    print(f"Generated sample VSM: {sample_vsm.name}")
    
    # Perform analysis
    generator.analyze_vsm(sample_vsm)
    
    # Export to PDF
    pdf_file = generator.export_to_pdf(sample_vsm, "demo_sample_vsm.pdf")
    json_file = generator.save_vsm_json(sample_vsm, "demo_sample_vsm.json")
    
    print(f"\nFiles created:")
    print(f"  PDF: {pdf_file}")
    print(f"  JSON: {json_file}")
    
    return sample_vsm

def demo_custom_vsm():
    """Demonstrate custom VSM creation"""
    print("\n" + "=" * 60)
    print("DEMO 2: Custom VSM Creation")
    print("=" * 60)
    
    # Create a software development value stream
    processes = [
        ProcessStep(
            name="Requirements Analysis",
            cycle_time=480.0,  # 8 hours
            lead_time=1440.0,  # 3 days
            uptime=90.0,
            changeover_time=60.0,
            batch_size=1,
            number_of_operators=2,
            available_time=480.0,
            waste_types=['waiting', 'overprocessing'],
            value_added=True,
            description="Gather and analyze customer requirements"
        ),
        ProcessStep(
            name="Design & Architecture",
            cycle_time=720.0,  # 12 hours
            lead_time=2880.0,  # 6 days
            uptime=85.0,
            changeover_time=120.0,
            batch_size=1,
            number_of_operators=3,
            available_time=480.0,
            waste_types=['waiting'],
            value_added=True,
            description="Create system design and architecture"
        ),
        ProcessStep(
            name="Development",
            cycle_time=1440.0,  # 3 days
            lead_time=7200.0,  # 15 days
            uptime=80.0,
            changeover_time=240.0,
            batch_size=1,
            number_of_operators=5,
            available_time=480.0,
            waste_types=['defects', 'waiting'],
            value_added=True,
            description="Code implementation and unit testing"
        ),
        ProcessStep(
            name="Code Review",
            cycle_time=240.0,  # 4 hours
            lead_time=960.0,   # 2 days
            uptime=95.0,
            changeover_time=30.0,
            batch_size=1,
            number_of_operators=2,
            available_time=480.0,
            waste_types=[],
            value_added=True,
            description="Peer code review and feedback"
        ),
        ProcessStep(
            name="Testing",
            cycle_time=480.0,  # 8 hours
            lead_time=1920.0,  # 4 days
            uptime=88.0,
            changeover_time=60.0,
            batch_size=1,
            number_of_operators=3,
            available_time=480.0,
            waste_types=['defects', 'waiting'],
            value_added=True,
            description="System testing and quality assurance"
        ),
        ProcessStep(
            name="Documentation",
            cycle_time=360.0,  # 6 hours
            lead_time=720.0,   # 1.5 days
            uptime=92.0,
            changeover_time=30.0,
            batch_size=1,
            number_of_operators=1,
            available_time=480.0,
            waste_types=['overprocessing'],
            value_added=False,
            description="Create user and technical documentation"
        ),
        ProcessStep(
            name="Deployment",
            cycle_time=120.0,  # 2 hours
            lead_time=480.0,   # 1 day
            uptime=75.0,
            changeover_time=180.0,
            batch_size=1,
            number_of_operators=2,
            available_time=480.0,
            waste_types=['waiting', 'motion'],
            value_added=False,
            description="Deploy to production environment"
        )
    ]
    
    custom_vsm = ValueStreamMap(
        name="Software Development Lifecycle",
        customer="Internal Business Units",
        supplier="Development Team",
        product="Custom Software Application",
        processes=processes,
        takt_time=2400.0,  # Customer expects delivery every 5 days
        created_date=datetime.now().strftime("%Y-%m-%d"),
        analyst="Demo System"
    )
    
    generator = VSMGenerator()
    
    print(f"Created custom VSM: {custom_vsm.name}")
    
    # Perform analysis
    generator.analyze_vsm(custom_vsm)
    
    # Export to PDF
    pdf_file = generator.export_to_pdf(custom_vsm, "demo_custom_vsm.pdf")
    json_file = generator.save_vsm_json(custom_vsm, "demo_custom_vsm.json")
    
    print(f"\nFiles created:")
    print(f"  PDF: {pdf_file}")
    print(f"  JSON: {json_file}")
    
    return custom_vsm

def demo_comparative_analysis(vsm1, vsm2):
    """Demonstrate comparative analysis between two VSMs"""
    print("\n" + "=" * 60)
    print("DEMO 3: Comparative Analysis")
    print("=" * 60)
    
    print(f"\nComparing:")
    print(f"  VSM 1: {vsm1.name}")
    print(f"  VSM 2: {vsm2.name}")
    
    print(f"\nKey Metrics Comparison:")
    print(f"{'Metric':<25} {'VSM 1':<20} {'VSM 2':<20}")
    print("-" * 65)
    print(f"{'Total Cycle Time':<25} {vsm1.total_cycle_time:<20.1f} {vsm2.total_cycle_time:<20.1f}")
    print(f"{'Total Lead Time':<25} {vsm1.total_lead_time:<20.1f} {vsm2.total_lead_time:<20.1f}")
    print(f"{'Process Efficiency':<25} {vsm1.process_efficiency:<20.1f}% {vsm2.process_efficiency:<20.1f}%")
    print(f"{'Takt Time':<25} {vsm1.takt_time:<20.1f} {vsm2.takt_time:<20.1f}")
    print(f"{'Number of Processes':<25} {len(vsm1.processes):<20} {len(vsm2.processes):<20}")
    
    # Identify which VSM is more efficient
    if vsm1.process_efficiency > vsm2.process_efficiency:
        print(f"\n✅ {vsm1.name} is more efficient")
    elif vsm2.process_efficiency > vsm1.process_efficiency:
        print(f"\n✅ {vsm2.name} is more efficient")
    else:
        print(f"\n🤝 Both VSMs have similar efficiency")

def demo_advanced_features():
    """Demonstrate advanced features"""
    print("\n" + "=" * 60)
    print("DEMO 4: Advanced Features")
    print("=" * 60)
    
    generator = VSMGenerator()
    
    # Create a high-efficiency process
    efficient_processes = [
        ProcessStep(
            name="Lean Process A",
            cycle_time=10.0,
            lead_time=12.0,  # Very low lead time
            uptime=98.0,
            changeover_time=1.0,
            batch_size=1,
            number_of_operators=1,
            available_time=480.0,
            waste_types=[],
            value_added=True,
            description="Optimized lean process"
        ),
        ProcessStep(
            name="Lean Process B",
            cycle_time=15.0,
            lead_time=18.0,
            uptime=97.0,
            changeover_time=2.0,
            batch_size=1,
            number_of_operators=1,
            available_time=480.0,
            waste_types=[],
            value_added=True,
            description="Optimized lean process"
        )
    ]
    
    efficient_vsm = ValueStreamMap(
        name="Optimized Lean Process",
        customer="Demanding Customer",
        supplier="Lean Supplier",
        product="High-Quality Product",
        processes=efficient_processes,
        takt_time=20.0,
        created_date=datetime.now().strftime("%Y-%m-%d"),
        analyst="Lean Expert"
    )
    
    print("Created high-efficiency VSM for demonstration")
    generator.analyze_vsm(efficient_vsm)
    
    # Export with custom filename
    pdf_file = generator.export_to_pdf(efficient_vsm, "demo_lean_process.pdf")
    print(f"\nGenerated optimized process report: {pdf_file}")
    
    return efficient_vsm

def demo_file_operations():
    """Demonstrate file loading and manipulation"""
    print("\n" + "=" * 60)
    print("DEMO 5: File Operations")
    print("=" * 60)
    
    generator = VSMGenerator()
    
    # Check if sample JSON exists and load it
    json_files = [f for f in os.listdir('.') if f.startswith('demo_sample_vsm') and f.endswith('.json')]
    
    if json_files:
        json_file = json_files[0]
        print(f"Loading VSM from file: {json_file}")
        
        loaded_vsm = generator.load_vsm_json(json_file)
        print(f"Successfully loaded: {loaded_vsm.name}")
        
        # Modify the loaded VSM
        loaded_vsm.analyst = "Modified by Demo"
        loaded_vsm.name = "Modified " + loaded_vsm.name
        
        # Save modified version
        new_json_file = generator.save_vsm_json(loaded_vsm, "demo_modified_vsm.json")
        new_pdf_file = generator.export_to_pdf(loaded_vsm, "demo_modified_vsm.pdf")
        
        print(f"Created modified versions:")
        print(f"  JSON: {new_json_file}")
        print(f"  PDF: {new_pdf_file}")
    else:
        print("No sample JSON file found. Run demo_sample_vsm() first.")

def main():
    """Run complete demonstration"""
    print("🚀 Value Stream Mapping Generator - Complete Demo")
    print("=" * 60)
    print("This demo will showcase all major features of the VSM Generator")
    print("Multiple PDF reports and JSON files will be created")
    print("=" * 60)
    
    try:
        # Demo 1: Sample VSM
        sample_vsm = demo_sample_vsm()
        
        # Demo 2: Custom VSM
        custom_vsm = demo_custom_vsm()
        
        # Demo 3: Comparative Analysis
        demo_comparative_analysis(sample_vsm, custom_vsm)
        
        # Demo 4: Advanced Features
        lean_vsm = demo_advanced_features()
        
        # Demo 5: File Operations
        demo_file_operations()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETE")
        print("=" * 60)
        print("Generated files:")
        
        # List all generated files
        demo_files = [f for f in os.listdir('.') if f.startswith('demo_')]
        for file in sorted(demo_files):
            size = os.path.getsize(file)
            print(f"  {file} ({size:,} bytes)")
        
        print(f"\nTotal files generated: {len(demo_files)}")
        print("\n🎯 You can now review the PDF reports to see the full capabilities!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()