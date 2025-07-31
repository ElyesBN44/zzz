#!/usr/bin/env python3
"""
Value Stream Mapping (VSM) Generator
=====================================

A comprehensive tool for creating, analyzing, and improving value stream maps.
Helps visualize business processes to identify waste, inefficiencies, and 
opportunities for improvement.

Features:
- Interactive process mapping
- Waste identification and analysis
- Improvement recommendations
- Professional PDF export
- Comprehensive metrics tracking
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import argparse

# PDF and visualization imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.colors import Color, black, white, red, green, blue, orange, yellow
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.platypus.flowables import Flowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
    from reportlab.graphics import renderPDF
except ImportError:
    print("Installing required dependencies...")
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.colors import Color, black, white, red, green, blue, orange, yellow
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.platypus.flowables import Flowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
    from reportlab.graphics import renderPDF


@dataclass
class ProcessStep:
    """Represents a single step in the value stream"""
    name: str
    cycle_time: float  # minutes
    lead_time: float   # minutes
    uptime: float      # percentage
    changeover_time: float  # minutes
    batch_size: int
    number_of_operators: int
    available_time: float  # minutes per day
    waste_types: List[str]
    value_added: bool
    description: str = ""
    
    @property
    def efficiency(self) -> float:
        """Calculate process efficiency"""
        return (self.cycle_time / self.lead_time) * 100 if self.lead_time > 0 else 0
    
    @property
    def capacity(self) -> float:
        """Calculate daily capacity"""
        effective_time = self.available_time * (self.uptime / 100)
        return effective_time / self.cycle_time if self.cycle_time > 0 else 0


@dataclass
class ValueStreamMap:
    """Complete value stream map representation"""
    name: str
    customer: str
    supplier: str
    product: str
    processes: List[ProcessStep]
    takt_time: float  # minutes
    created_date: str
    analyst: str
    
    @property
    def total_cycle_time(self) -> float:
        """Sum of all cycle times"""
        return sum(p.cycle_time for p in self.processes)
    
    @property
    def total_lead_time(self) -> float:
        """Sum of all lead times"""
        return sum(p.lead_time for p in self.processes)
    
    @property
    def value_added_time(self) -> float:
        """Sum of value-added cycle times"""
        return sum(p.cycle_time for p in self.processes if p.value_added)
    
    @property
    def non_value_added_time(self) -> float:
        """Sum of non-value-added cycle times"""
        return sum(p.cycle_time for p in self.processes if not p.value_added)
    
    @property
    def process_efficiency(self) -> float:
        """Overall process efficiency"""
        return (self.value_added_time / self.total_cycle_time) * 100 if self.total_cycle_time > 0 else 0


class WasteAnalyzer:
    """Analyzes processes for waste identification"""
    
    WASTE_TYPES = {
        'transportation': 'Unnecessary movement of materials or information',
        'inventory': 'Excess raw materials, WIP, or finished goods',
        'motion': 'Unnecessary movement of people',
        'waiting': 'Idle time waiting for materials, information, or equipment',
        'overproduction': 'Producing more than customer demand',
        'overprocessing': 'More work than required by customer',
        'defects': 'Effort to find and correct defects',
        'underutilized_talent': 'Not fully utilizing employee skills and ideas'
    }
    
    @classmethod
    def identify_waste(cls, process: ProcessStep) -> List[str]:
        """Identify potential waste in a process step"""
        identified_waste = []
        
        # Check for waiting waste
        if process.lead_time > process.cycle_time * 2:
            identified_waste.append('waiting')
        
        # Check for inventory waste
        if process.batch_size > 50:  # Arbitrary threshold
            identified_waste.append('inventory')
        
        # Check for underutilized talent
        if process.uptime < 80:
            identified_waste.append('underutilized_talent')
        
        # Check for overprocessing
        if process.changeover_time > process.cycle_time:
            identified_waste.append('overprocessing')
        
        # Add any explicitly defined waste types
        identified_waste.extend(process.waste_types)
        
        return list(set(identified_waste))  # Remove duplicates
    
    @classmethod
    def calculate_waste_impact(cls, vsm: ValueStreamMap) -> Dict[str, float]:
        """Calculate the impact of different waste types"""
        waste_impact = {waste: 0.0 for waste in cls.WASTE_TYPES.keys()}
        
        for process in vsm.processes:
            process_waste = cls.identify_waste(process)
            for waste_type in process_waste:
                if waste_type in waste_impact:
                    waste_impact[waste_type] += process.lead_time - process.cycle_time
        
        return waste_impact


class ImprovementEngine:
    """Generates improvement recommendations"""
    
    @classmethod
    def generate_recommendations(cls, vsm: ValueStreamMap) -> List[Dict[str, str]]:
        """Generate improvement recommendations based on VSM analysis"""
        recommendations = []
        waste_analyzer = WasteAnalyzer()
        waste_impact = waste_analyzer.calculate_waste_impact(vsm)
        
        # Efficiency recommendations
        if vsm.process_efficiency < 50:
            recommendations.append({
                'category': 'Process Efficiency',
                'priority': 'High',
                'description': 'Focus on eliminating non-value-added activities',
                'action': 'Conduct kaizen events to streamline processes',
                'expected_impact': 'Reduce lead time by 20-30%'
            })
        
        # Takt time balance
        bottleneck_processes = [p for p in vsm.processes if p.cycle_time > vsm.takt_time]
        if bottleneck_processes:
            recommendations.append({
                'category': 'Flow Balance',
                'priority': 'High',
                'description': f'Balance line to takt time ({vsm.takt_time:.1f} min)',
                'action': 'Add capacity to bottleneck processes or redistribute work',
                'expected_impact': 'Improve flow and reduce waiting'
            })
        
        # Waste-specific recommendations
        for waste_type, impact in waste_impact.items():
            if impact > 60:  # Significant waste impact
                recommendations.append({
                    'category': 'Waste Elimination',
                    'priority': 'Medium',
                    'description': f'Reduce {waste_type} waste',
                    'action': waste_analyzer.WASTE_TYPES[waste_type],
                    'expected_impact': f'Potential {impact:.1f} min reduction in lead time'
                })
        
        # Uptime improvements
        low_uptime_processes = [p for p in vsm.processes if p.uptime < 85]
        if low_uptime_processes:
            recommendations.append({
                'category': 'Equipment Reliability',
                'priority': 'Medium',
                'description': 'Improve equipment uptime',
                'action': 'Implement TPM (Total Productive Maintenance)',
                'expected_impact': 'Increase overall capacity and reduce variability'
            })
        
        return recommendations


class VSMVisualizer:
    """Creates visual representation of the value stream map"""
    
    def __init__(self):
        self.colors = {
            'process': Color(0.8, 0.9, 1.0),
            'value_added': Color(0.8, 1.0, 0.8),
            'non_value_added': Color(1.0, 0.8, 0.8),
            'waste': Color(1.0, 0.6, 0.6),
            'flow': Color(0.2, 0.2, 0.8),
            'info': Color(0.9, 0.9, 0.9)
        }
    
    def create_process_box(self, x: float, y: float, width: float, height: float, 
                          process: ProcessStep) -> Drawing:
        """Create a visual process box"""
        d = Drawing(width, height)
        
        # Choose color based on value-added status
        box_color = self.colors['value_added'] if process.value_added else self.colors['non_value_added']
        
        # Main process box
        d.add(Rect(0, 0, width, height, fillColor=box_color, strokeColor=black))
        
        # Process name
        d.add(String(width/2, height-15, process.name, 
                    fontSize=10, textAnchor='middle', fontName='Helvetica-Bold'))
        
        # Metrics
        metrics_text = [
            f"C/T: {process.cycle_time:.1f} min",
            f"L/T: {process.lead_time:.1f} min",
            f"Uptime: {process.uptime:.0f}%",
            f"Operators: {process.number_of_operators}"
        ]
        
        for i, metric in enumerate(metrics_text):
            d.add(String(5, height-30-i*12, metric, fontSize=8, fontName='Helvetica'))
        
        return d
    
    def create_flow_arrow(self, x: float, y: float, width: float) -> Drawing:
        """Create a flow arrow between processes"""
        d = Drawing(width, 20)
        
        # Arrow line
        d.add(Line(0, 10, width-10, 10, strokeColor=self.colors['flow'], strokeWidth=2))
        
        # Arrow head
        d.add(Line(width-10, 10, width-15, 5, strokeColor=self.colors['flow'], strokeWidth=2))
        d.add(Line(width-10, 10, width-15, 15, strokeColor=self.colors['flow'], strokeWidth=2))
        
        return d


class PDFGenerator:
    """Generates comprehensive PDF reports for value stream maps"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10
        )
    
    def generate_report(self, vsm: ValueStreamMap, filename: str) -> str:
        """Generate comprehensive VSM PDF report"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title page
        story.extend(self._create_title_page(vsm))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(vsm))
        story.append(PageBreak())
        
        # Process details
        story.extend(self._create_process_details(vsm))
        story.append(PageBreak())
        
        # Waste analysis
        story.extend(self._create_waste_analysis(vsm))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(vsm))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def _create_title_page(self, vsm: ValueStreamMap) -> List:
        """Create title page content"""
        content = []
        
        content.append(Paragraph("Value Stream Mapping Report", self.title_style))
        content.append(Spacer(1, 20))
        
        # VSM information table
        vsm_info = [
            ['Process Name:', vsm.name],
            ['Customer:', vsm.customer],
            ['Supplier:', vsm.supplier],
            ['Product:', vsm.product],
            ['Analysis Date:', vsm.created_date],
            ['Analyst:', vsm.analyst]
        ]
        
        info_table = Table(vsm_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        content.append(info_table)
        
        content.append(Spacer(1, 40))
        
        # Key metrics summary
        content.append(Paragraph("Key Metrics Summary", self.heading_style))
        
        metrics = [
            ['Total Cycle Time:', f"{vsm.total_cycle_time:.1f} minutes"],
            ['Total Lead Time:', f"{vsm.total_lead_time:.1f} minutes"],
            ['Value-Added Time:', f"{vsm.value_added_time:.1f} minutes"],
            ['Process Efficiency:', f"{vsm.process_efficiency:.1f}%"],
            ['Takt Time:', f"{vsm.takt_time:.1f} minutes"],
            ['Number of Processes:', str(len(vsm.processes))]
        ]
        
        metrics_table = Table(metrics, colWidths=[2.5*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('BACKGROUND', (0, 0), (0, -1), Color(0.9, 0.9, 0.9)),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        content.append(metrics_table)
        
        return content
    
    def _create_executive_summary(self, vsm: ValueStreamMap) -> List:
        """Create executive summary"""
        content = []
        content.append(Paragraph("Executive Summary", self.title_style))
        
        # Process overview
        overview_text = f"""
        This value stream analysis examines the {vsm.name} process serving customer {vsm.customer}. 
        The analysis identified {len(vsm.processes)} key process steps with a total cycle time of 
        {vsm.total_cycle_time:.1f} minutes and lead time of {vsm.total_lead_time:.1f} minutes.
        
        The current process efficiency is {vsm.process_efficiency:.1f}%, indicating significant 
        opportunities for improvement through waste elimination and process optimization.
        """
        content.append(Paragraph(overview_text, self.styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Waste summary
        waste_analyzer = WasteAnalyzer()
        waste_impact = waste_analyzer.calculate_waste_impact(vsm)
        total_waste = sum(waste_impact.values())
        
        waste_text = f"""
        <b>Waste Analysis Summary:</b><br/>
        Total identified waste: {total_waste:.1f} minutes<br/>
        Primary waste sources: {', '.join([k for k, v in waste_impact.items() if v > 30])}<br/>
        Improvement potential: {(total_waste/vsm.total_lead_time)*100:.1f}% lead time reduction
        """
        content.append(Paragraph(waste_text, self.styles['Normal']))
        
        return content
    
    def _create_process_details(self, vsm: ValueStreamMap) -> List:
        """Create detailed process analysis"""
        content = []
        content.append(Paragraph("Process Details", self.title_style))
        
        # Process table
        headers = ['Process', 'Cycle Time', 'Lead Time', 'Uptime', 'Operators', 'Efficiency', 'Value Added']
        data = [headers]
        
        for process in vsm.processes:
            row = [
                process.name,
                f"{process.cycle_time:.1f} min",
                f"{process.lead_time:.1f} min",
                f"{process.uptime:.0f}%",
                str(process.number_of_operators),
                f"{process.efficiency:.1f}%",
                "Yes" if process.value_added else "No"
            ]
            data.append(row)
        
        process_table = Table(data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.7*inch])
        process_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.8, 0.8, 0.8)),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, Color(0.95, 0.95, 0.95)]),
        ]))
        content.append(process_table)
        
        return content
    
    def _create_waste_analysis(self, vsm: ValueStreamMap) -> List:
        """Create waste analysis section"""
        content = []
        content.append(Paragraph("Waste Analysis", self.title_style))
        
        waste_analyzer = WasteAnalyzer()
        waste_impact = waste_analyzer.calculate_waste_impact(vsm)
        
        # Waste impact table
        headers = ['Waste Type', 'Impact (minutes)', 'Description']
        data = [headers]
        
        for waste_type, impact in sorted(waste_impact.items(), key=lambda x: x[1], reverse=True):
            if impact > 0:
                row = [
                    waste_type.replace('_', ' ').title(),
                    f"{impact:.1f}",
                    waste_analyzer.WASTE_TYPES[waste_type]
                ]
                data.append(row)
        
        if len(data) > 1:  # If there's waste data
            waste_table = Table(data, colWidths=[1.5*inch, 1.2*inch, 3.5*inch])
            waste_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), Color(0.8, 0.8, 0.8)),
                ('TEXTCOLOR', (0, 0), (-1, 0), black),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, Color(0.95, 0.95, 0.95)]),
            ]))
            content.append(waste_table)
        else:
            content.append(Paragraph("No significant waste identified in current analysis.", self.styles['Normal']))
        
        return content
    
    def _create_recommendations(self, vsm: ValueStreamMap) -> List:
        """Create recommendations section"""
        content = []
        content.append(Paragraph("Improvement Recommendations", self.title_style))
        
        improvement_engine = ImprovementEngine()
        recommendations = improvement_engine.generate_recommendations(vsm)
        
        for i, rec in enumerate(recommendations, 1):
            content.append(Paragraph(f"Recommendation {i}: {rec['category']}", self.heading_style))
            
            rec_details = f"""
            <b>Priority:</b> {rec['priority']}<br/>
            <b>Description:</b> {rec['description']}<br/>
            <b>Action:</b> {rec['action']}<br/>
            <b>Expected Impact:</b> {rec['expected_impact']}
            """
            content.append(Paragraph(rec_details, self.styles['Normal']))
            content.append(Spacer(1, 15))
        
        return content


class VSMGenerator:
    """Main application class for VSM generation"""
    
    def __init__(self):
        self.current_vsm: Optional[ValueStreamMap] = None
        self.visualizer = VSMVisualizer()
        self.pdf_generator = PDFGenerator()
    
    def create_sample_vsm(self) -> ValueStreamMap:
        """Create a sample value stream map for demonstration"""
        processes = [
            ProcessStep(
                name="Order Processing",
                cycle_time=15.0,
                lead_time=120.0,
                uptime=95.0,
                changeover_time=5.0,
                batch_size=1,
                number_of_operators=2,
                available_time=480.0,
                waste_types=['waiting'],
                value_added=True,
                description="Process customer orders and validate requirements"
            ),
            ProcessStep(
                name="Material Preparation",
                cycle_time=30.0,
                lead_time=240.0,
                uptime=85.0,
                changeover_time=20.0,
                batch_size=10,
                number_of_operators=3,
                available_time=480.0,
                waste_types=['inventory', 'transportation'],
                value_added=True,
                description="Gather and prepare materials for production"
            ),
            ProcessStep(
                name="Quality Check",
                cycle_time=10.0,
                lead_time=60.0,
                uptime=98.0,
                changeover_time=2.0,
                batch_size=1,
                number_of_operators=1,
                available_time=480.0,
                waste_types=[],
                value_added=True,
                description="Inspect materials for quality standards"
            ),
            ProcessStep(
                name="Assembly",
                cycle_time=45.0,
                lead_time=180.0,
                uptime=90.0,
                changeover_time=15.0,
                batch_size=5,
                number_of_operators=4,
                available_time=480.0,
                waste_types=['motion', 'waiting'],
                value_added=True,
                description="Assemble components into final product"
            ),
            ProcessStep(
                name="Final Inspection",
                cycle_time=20.0,
                lead_time=90.0,
                uptime=95.0,
                changeover_time=5.0,
                batch_size=1,
                number_of_operators=2,
                available_time=480.0,
                waste_types=[],
                value_added=True,
                description="Final quality inspection and testing"
            ),
            ProcessStep(
                name="Packaging",
                cycle_time=12.0,
                lead_time=45.0,
                uptime=92.0,
                changeover_time=8.0,
                batch_size=10,
                number_of_operators=2,
                available_time=480.0,
                waste_types=['overprocessing'],
                value_added=False,
                description="Package product for shipping"
            ),
            ProcessStep(
                name="Shipping",
                cycle_time=5.0,
                lead_time=1440.0,  # 24 hours
                uptime=80.0,
                changeover_time=30.0,
                batch_size=20,
                number_of_operators=1,
                available_time=480.0,
                waste_types=['transportation', 'waiting'],
                value_added=False,
                description="Ship product to customer"
            )
        ]
        
        return ValueStreamMap(
            name="Custom Widget Manufacturing Process",
            customer="ABC Manufacturing Corp",
            supplier="XYZ Components Ltd",
            product="Custom Industrial Widget",
            processes=processes,
            takt_time=30.0,  # Customer demand: one unit every 30 minutes
            created_date=datetime.now().strftime("%Y-%m-%d"),
            analyst="VSM Generator System"
        )
    
    def interactive_vsm_creation(self) -> ValueStreamMap:
        """Interactive VSM creation through CLI"""
        print("\n=== Value Stream Mapping Generator ===")
        print("Let's create your value stream map step by step.\n")
        
        # Basic VSM information
        name = input("Enter process name: ").strip() or "Manufacturing Process"
        customer = input("Enter customer name: ").strip() or "Customer"
        supplier = input("Enter supplier name: ").strip() or "Supplier"
        product = input("Enter product name: ").strip() or "Product"
        
        takt_time_input = input("Enter takt time (minutes) [30]: ").strip()
        takt_time = float(takt_time_input) if takt_time_input else 30.0
        
        analyst = input("Enter analyst name: ").strip() or "Anonymous"
        
        print(f"\nHow many process steps are in your value stream? ", end="")
        num_processes = int(input().strip() or "3")
        
        processes = []
        for i in range(num_processes):
            print(f"\n--- Process Step {i+1} ---")
            process = self._create_process_step_interactive()
            processes.append(process)
        
        return ValueStreamMap(
            name=name,
            customer=customer,
            supplier=supplier,
            product=product,
            processes=processes,
            takt_time=takt_time,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            analyst=analyst
        )
    
    def _create_process_step_interactive(self) -> ProcessStep:
        """Create a process step through interactive input"""
        name = input("Process name: ").strip() or "Process Step"
        
        cycle_time = float(input("Cycle time (minutes) [15]: ").strip() or "15")
        lead_time = float(input("Lead time (minutes) [60]: ").strip() or "60")
        uptime = float(input("Uptime percentage [90]: ").strip() or "90")
        changeover_time = float(input("Changeover time (minutes) [5]: ").strip() or "5")
        batch_size = int(input("Batch size [1]: ").strip() or "1")
        operators = int(input("Number of operators [1]: ").strip() or "1")
        available_time = float(input("Available time per day (minutes) [480]: ").strip() or "480")
        
        value_added_input = input("Is this process value-added? (y/n) [y]: ").strip().lower()
        value_added = value_added_input != 'n'
        
        waste_input = input("Enter waste types (comma-separated, optional): ").strip()
        waste_types = [w.strip() for w in waste_input.split(',') if w.strip()]
        
        description = input("Process description (optional): ").strip()
        
        return ProcessStep(
            name=name,
            cycle_time=cycle_time,
            lead_time=lead_time,
            uptime=uptime,
            changeover_time=changeover_time,
            batch_size=batch_size,
            number_of_operators=operators,
            available_time=available_time,
            waste_types=waste_types,
            value_added=value_added,
            description=description
        )
    
    def analyze_vsm(self, vsm: ValueStreamMap) -> None:
        """Perform comprehensive VSM analysis"""
        print(f"\n=== Analysis Results for {vsm.name} ===")
        
        # Basic metrics
        print(f"\nKey Metrics:")
        print(f"  Total Cycle Time: {vsm.total_cycle_time:.1f} minutes")
        print(f"  Total Lead Time: {vsm.total_lead_time:.1f} minutes")
        print(f"  Value-Added Time: {vsm.value_added_time:.1f} minutes")
        print(f"  Process Efficiency: {vsm.process_efficiency:.1f}%")
        print(f"  Takt Time: {vsm.takt_time:.1f} minutes")
        
        # Waste analysis
        waste_analyzer = WasteAnalyzer()
        waste_impact = waste_analyzer.calculate_waste_impact(vsm)
        
        print(f"\nWaste Analysis:")
        for waste_type, impact in sorted(waste_impact.items(), key=lambda x: x[1], reverse=True):
            if impact > 0:
                print(f"  {waste_type.replace('_', ' ').title()}: {impact:.1f} minutes")
        
        # Bottleneck analysis
        bottlenecks = [p for p in vsm.processes if p.cycle_time > vsm.takt_time]
        if bottlenecks:
            print(f"\nBottleneck Processes (exceed takt time):")
            for process in bottlenecks:
                print(f"  {process.name}: {process.cycle_time:.1f} min (vs {vsm.takt_time:.1f} min takt)")
        
        # Improvement recommendations
        improvement_engine = ImprovementEngine()
        recommendations = improvement_engine.generate_recommendations(vsm)
        
        print(f"\nImprovement Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
            print(f"  {i}. {rec['category']}: {rec['description']}")
    
    def export_to_pdf(self, vsm: ValueStreamMap, filename: str = None) -> str:
        """Export VSM to PDF"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vsm_report_{timestamp}.pdf"
        
        print(f"Generating PDF report: {filename}")
        self.pdf_generator.generate_report(vsm, filename)
        print(f"PDF report generated successfully: {filename}")
        return filename
    
    def save_vsm_json(self, vsm: ValueStreamMap, filename: str = None) -> str:
        """Save VSM data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vsm_data_{timestamp}.json"
        
        # Convert dataclass to dictionary
        vsm_dict = asdict(vsm)
        
        with open(filename, 'w') as f:
            json.dump(vsm_dict, f, indent=2)
        
        print(f"VSM data saved to: {filename}")
        return filename
    
    def load_vsm_json(self, filename: str) -> ValueStreamMap:
        """Load VSM data from JSON file"""
        with open(filename, 'r') as f:
            vsm_dict = json.load(f)
        
        # Convert processes back to ProcessStep objects
        processes = [ProcessStep(**p) for p in vsm_dict['processes']]
        vsm_dict['processes'] = processes
        
        return ValueStreamMap(**vsm_dict)


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Value Stream Mapping Generator")
    parser.add_argument('--sample', action='store_true', help='Generate sample VSM')
    parser.add_argument('--interactive', action='store_true', help='Interactive VSM creation')
    parser.add_argument('--load', type=str, help='Load VSM from JSON file')
    parser.add_argument('--output', type=str, help='Output PDF filename')
    parser.add_argument('--analyze-only', action='store_true', help='Only perform analysis, no PDF')
    
    args = parser.parse_args()
    
    generator = VSMGenerator()
    
    # Determine VSM source
    if args.load:
        if not os.path.exists(args.load):
            print(f"Error: File {args.load} not found")
            return
        vsm = generator.load_vsm_json(args.load)
        print(f"Loaded VSM from {args.load}")
    elif args.interactive:
        vsm = generator.interactive_vsm_creation()
    else:
        # Default to sample VSM
        vsm = generator.create_sample_vsm()
        print("Generated sample VSM (use --interactive for custom VSM)")
    
    # Perform analysis
    generator.analyze_vsm(vsm)
    
    # Save data
    json_file = generator.save_vsm_json(vsm)
    
    # Generate PDF unless analyze-only
    if not args.analyze_only:
        pdf_file = generator.export_to_pdf(vsm, args.output)
        
        print(f"\n=== Files Generated ===")
        print(f"Data file: {json_file}")
        print(f"PDF report: {pdf_file}")
    else:
        print(f"\nData file: {json_file}")
    
    print(f"\nAnalysis complete for: {vsm.name}")


if __name__ == "__main__":
    main()