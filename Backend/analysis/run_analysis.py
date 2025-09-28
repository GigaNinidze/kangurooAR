#!/usr/bin/env python3
"""
Simple runner script for session analysis
Usage: python run_analysis.py [--batch] [--sessions-dir ../sessions]
"""

import argparse
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.session_analyzer import SessionAnalyzer
from analysis.batch_processor import BatchProcessor

async def run_single_analysis(sessions_dir: str):
    """Run single session analysis"""
    print("🔍 Running single session analysis...")
    
    analyzer = SessionAnalyzer(os.getenv('GEMINI_API_KEY'))
    analyses = await analyzer.analyze_all_sessions(sessions_dir)
    
    if analyses:
        report_path = analyzer.save_analysis_report(analyses)
        print(f"📄 Report saved to: {report_path}")
    else:
        print("❌ No sessions found to analyze")

async def run_batch_analysis(sessions_dir: str):
    """Run batch session analysis"""
    print("🔄 Running batch session analysis...")
    
    processor = BatchProcessor(os.getenv('GEMINI_API_KEY'), batch_size=3)
    analyses = await processor.process_batches(sessions_dir)
    
    if analyses:
        report_path = processor.analyzer.save_analysis_report(analyses, "batch_analysis_report.json")
        print(f"📄 Batch report saved to: {report_path}")
    else:
        print("❌ No sessions found to analyze")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Analyze customer support sessions')
    parser.add_argument('--batch', action='store_true', help='Use batch processing')
    parser.add_argument('--sessions-dir', default='../sessions', help='Sessions directory path')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
        return
    
    # Run analysis
    if args.batch:
        asyncio.run(run_batch_analysis(args.sessions_dir))
    else:
        asyncio.run(run_single_analysis(args.sessions_dir))

if __name__ == "__main__":
    main()
