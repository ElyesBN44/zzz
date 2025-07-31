# Value Stream Mapping (VSM) Generator

A comprehensive tool for creating, analyzing, and improving value stream maps. This AI-powered system helps businesses visualize their processes to identify waste, inefficiencies, and opportunities for improvement.

## 🎯 Features

- **Interactive Process Mapping**: Step-by-step guided creation of value stream maps
- **Comprehensive Waste Analysis**: Automatic identification of 8 types of waste (TIMWOODS)
- **Professional PDF Reports**: Multi-page detailed reports with analysis and recommendations
- **Improvement Recommendations**: AI-generated suggestions for process optimization
- **Metrics Tracking**: Real-time calculation of efficiency, cycle times, and bottlenecks
- **Data Export/Import**: Save and load VSM data in JSON format
- **Sample Data**: Built-in demonstration with realistic manufacturing process

## 📊 What is Value Stream Mapping?

Value Stream Mapping (VSM) is a lean manufacturing technique used to analyze and design the flow of materials and information required to bring a product or service to a consumer. It helps organizations:

- Visualize the entire process flow
- Identify waste and bottlenecks
- Understand cycle times and lead times
- Optimize resource allocation
- Improve overall efficiency

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Generate Sample VSM with PDF Report
```bash
python3 vsm_generator.py --sample
```

#### Interactive VSM Creation
```bash
python3 vsm_generator.py --interactive
```

#### Load Existing VSM Data
```bash
python3 vsm_generator.py --load vsm_data_file.json
```

#### Analysis Only (No PDF)
```bash
python3 vsm_generator.py --sample --analyze-only
```

## 📋 Command Line Options

| Option | Description |
|--------|-------------|
| `--sample` | Generate a sample VSM with realistic manufacturing data |
| `--interactive` | Create a custom VSM through guided input |
| `--load <file>` | Load VSM data from JSON file |
| `--output <file>` | Specify output PDF filename |
| `--analyze-only` | Perform analysis without generating PDF |

## 🔍 Understanding the Analysis

### Key Metrics

- **Total Cycle Time**: Sum of all process cycle times
- **Total Lead Time**: Sum of all process lead times  
- **Value-Added Time**: Time spent on value-adding activities
- **Process Efficiency**: (Value-Added Time / Total Cycle Time) × 100
- **Takt Time**: Customer demand rate

### Waste Types (TIMWOODS)

1. **Transportation**: Unnecessary movement of materials/information
2. **Inventory**: Excess raw materials, WIP, or finished goods
3. **Motion**: Unnecessary movement of people
4. **Waiting**: Idle time waiting for materials, information, or equipment
5. **Overproduction**: Producing more than customer demand
6. **Overprocessing**: More work than required by customer
7. **Defects**: Effort to find and correct defects
8. **Underutilized Talent**: Not fully utilizing employee skills and ideas

### Process Parameters

Each process step includes:
- **Cycle Time**: Time to complete one unit
- **Lead Time**: Total time from start to finish including waiting
- **Uptime**: Equipment/process availability percentage
- **Changeover Time**: Time to switch between products
- **Batch Size**: Number of units processed together
- **Operators**: Number of people required
- **Available Time**: Working time per day

## 📖 Interactive Mode Guide

When using `--interactive`, you'll be prompted for:

1. **Basic Information**:
   - Process name
   - Customer and supplier names
   - Product information
   - Takt time (customer demand rate)
   - Analyst name

2. **Process Steps**: For each step, provide:
   - Process name and description
   - Timing metrics (cycle time, lead time, uptime)
   - Resource requirements (operators, batch size)
   - Value-added classification
   - Known waste types

## 📊 Sample Output

The system generates two types of files:

### 1. JSON Data File (`vsm_data_YYYYMMDD_HHMMSS.json`)
Contains structured VSM data that can be reloaded for further analysis.

### 2. PDF Report (`vsm_report_YYYYMMDD_HHMMSS.pdf`)
Comprehensive multi-page report including:
- **Title Page**: VSM overview and key metrics
- **Executive Summary**: Process overview and waste analysis
- **Process Details**: Detailed table of all processes
- **Waste Analysis**: Breakdown of identified waste types
- **Recommendations**: Prioritized improvement suggestions

## 🎨 Understanding the PDF Report

### Title Page
- Process identification information
- Key metrics summary table
- Overall efficiency indicators

### Executive Summary
- Process overview narrative
- Total waste quantification
- Improvement potential assessment

### Process Details
- Comprehensive process table
- Color-coded value-added classification
- Efficiency calculations for each step

### Waste Analysis
- Detailed waste impact quantification
- Prioritized waste types by impact
- Descriptions of each waste category

### Improvement Recommendations
- Prioritized action items
- Expected impact estimates
- Specific implementation guidance

## 🔧 Customization

### Adding Custom Waste Types
Modify the `WASTE_TYPES` dictionary in the `WasteAnalyzer` class:

```python
WASTE_TYPES = {
    'custom_waste': 'Description of custom waste type',
    # ... existing waste types
}
```

### Modifying Analysis Thresholds
Adjust waste identification logic in the `identify_waste` method:

```python
# Example: Change inventory waste threshold
if process.batch_size > 100:  # Custom threshold
    identified_waste.append('inventory')
```

### Customizing PDF Styling
Modify colors and styles in the `PDFGenerator` class:

```python
# Example: Change color scheme
self.colors = {
    'value_added': Color(0.7, 1.0, 0.7),  # Light green
    'non_value_added': Color(1.0, 0.7, 0.7),  # Light red
    # ... other colors
}
```

## 📁 File Structure

```
├── vsm_generator.py          # Main application
├── requirements.txt          # Dependencies
├── README.md                # Documentation
├── vsm_data_*.json          # Generated data files
└── vsm_report_*.pdf         # Generated reports
```

## 🏭 Sample Data Overview

The built-in sample demonstrates a **Custom Widget Manufacturing Process** with 7 process steps:

1. **Order Processing** (15 min cycle, 120 min lead time)
2. **Material Preparation** (30 min cycle, 240 min lead time)
3. **Quality Check** (10 min cycle, 60 min lead time)
4. **Assembly** (45 min cycle, 180 min lead time) - *Bottleneck*
5. **Final Inspection** (20 min cycle, 90 min lead time)
6. **Packaging** (12 min cycle, 45 min lead time) - *Non-value-added*
7. **Shipping** (5 min cycle, 1440 min lead time) - *Non-value-added*

**Key Insights from Sample**:
- Process Efficiency: 87.6%
- Primary Waste: Waiting (2,038 minutes)
- Main Bottleneck: Assembly process exceeds takt time
- Improvement Potential: 90%+ lead time reduction possible

## 🎯 Best Practices

### Data Collection
1. **Accurate Timing**: Use actual measured times, not estimates
2. **Include Waiting**: Account for all delays and queues
3. **Document Waste**: Record observed waste types during analysis
4. **Validate Data**: Cross-check with multiple sources

### Process Mapping
1. **Start with Current State**: Map what actually happens, not what should happen
2. **Include All Steps**: Don't skip seemingly minor processes
3. **Measure at Process Level**: Focus on individual process performance
4. **Consider Variability**: Account for best/worst case scenarios

### Analysis Interpretation
1. **Focus on Impact**: Prioritize high-impact improvement opportunities
2. **Consider Constraints**: Evaluate feasibility of recommendations
3. **Validate Assumptions**: Test improvement theories with small experiments
4. **Monitor Progress**: Track metrics after implementing changes

## 🔄 Continuous Improvement Workflow

1. **Map Current State**: Document existing processes
2. **Analyze Waste**: Identify improvement opportunities
3. **Design Future State**: Create improved process map
4. **Implement Changes**: Execute improvement initiatives
5. **Measure Results**: Validate improvement impact
6. **Repeat Cycle**: Continuously refine processes

## 🤝 Contributing

To extend or improve the VSM Generator:

1. Fork the repository
2. Create feature branch
3. Implement changes with proper testing
4. Submit pull request with clear description

### Development Areas
- Additional waste identification algorithms
- Enhanced visualization capabilities
- Integration with other lean tools
- Industry-specific templates
- Real-time data integration

## 📞 Support

For questions, issues, or feature requests:
- Review this documentation
- Check the sample output for expected behavior
- Analyze the generated JSON data for process understanding
- Experiment with different process configurations

## 📄 License

This Value Stream Mapping Generator is provided as-is for educational and business improvement purposes. Feel free to modify and distribute according to your needs.

---

**Built with ❤️ for operational excellence and continuous improvement**