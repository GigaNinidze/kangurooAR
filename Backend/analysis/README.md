# Session Analysis Module

This module analyzes customer support sessions saved as text files and generates insights using AI.

## Files

- `session_analyzer.py` - Main analyzer class with AI-powered session evaluation
- `batch_processor.py` - Batch processing for large numbers of sessions
- `run_analysis.py` - Simple runner script
- `reports/` - Directory for generated analysis reports

## Usage

### Basic Analysis
```bash
cd Backend/analysis
python run_analysis.py
```

### Batch Analysis
```bash
cd Backend/analysis
python run_analysis.py --batch
```

### Custom Sessions Directory
```bash
cd Backend/analysis
python run_analysis.py --sessions-dir /path/to/sessions
```

## Features

- **AI-Powered Analysis**: Uses Gemini AI to evaluate session quality
- **Comprehensive Metrics**: Analyzes resolution rate, customer satisfaction, communication quality
- **Batch Processing**: Handles large numbers of sessions efficiently
- **JSON Reports**: Generates detailed reports in JSON format
- **Summary Statistics**: Provides overall performance metrics

## Analysis Metrics

Each session is evaluated on:

- **Overall Rating** (1-10)
- **Issue Resolution** (true/false)
- **Customer Satisfaction** (high/medium/low)
- **Response Time Quality** (fast/medium/slow)
- **Troubleshooting Effectiveness** (effective/partially_effective/ineffective)
- **Communication Quality** (excellent/good/fair/poor)
- **Customer Sentiment** (positive/neutral/negative)
- **Escalation Needed** (true/false)
- **Improvement Suggestions**

## Output

Analysis reports are saved to the `reports/` directory with:
- Individual session analyses
- Summary statistics
- Resolution rates
- Satisfaction metrics
- Improvement recommendations

## Requirements

- Python 3.7+
- google-generativeai
- python-dotenv
- Valid GEMINI_API_KEY in .env file
