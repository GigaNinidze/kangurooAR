#!/usr/bin/env python3
"""
Batch Processor - Processes multiple session files in batches
Useful for analyzing large numbers of sessions efficiently
"""

import os
import asyncio
from datetime import datetime
from session_analyzer import SessionAnalyzer

class BatchProcessor:
    def __init__(self, api_key: str, batch_size: int = 5):
        """Initialize batch processor"""
        self.analyzer = SessionAnalyzer(api_key)
        self.batch_size = batch_size
    
    async def process_batches(self, sessions_dir: str = "../sessions"):
        """Process sessions in batches to avoid overwhelming the API"""
        session_files = self.analyzer.get_all_session_files(sessions_dir)
        total_files = len(session_files)
        
        print(f"🔄 Processing {total_files} sessions in batches of {self.batch_size}")
        
        all_analyses = []
        
        # Process in batches
        for i in range(0, total_files, self.batch_size):
            batch_files = session_files[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_files + self.batch_size - 1) // self.batch_size
            
            print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch_files)} files)")
            
            batch_analyses = []
            for filepath in batch_files:
                print(f"  📄 Analyzing {os.path.basename(filepath)}...")
                
                # Load and analyze session
                session_data = self.analyzer.load_session_file(filepath)
                if session_data:
                    analysis = await self.analyzer.analyze_session(session_data)
                    batch_analyses.append(analysis)
                    print(f"  ✅ Completed {session_data['session_id']}")
                else:
                    print(f"  ❌ Failed to load {filepath}")
            
            all_analyses.extend(batch_analyses)
            
            # Small delay between batches to be respectful to the API
            if i + self.batch_size < total_files:
                print(f"  ⏳ Waiting 2 seconds before next batch...")
                await asyncio.sleep(2)
        
        return all_analyses

async def main():
    """Main function for batch processing"""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return
    
    # Initialize batch processor
    processor = BatchProcessor(api_key, batch_size=3)  # Small batch size for testing
    
    print("🚀 Starting batch processing...")
    
    # Process all sessions
    analyses = await processor.process_batches()
    
    if analyses:
        # Save comprehensive report
        report_path = processor.analyzer.save_analysis_report(analyses, "batch_analysis_report.json")
        
        # Print summary
        summary = processor.analyzer.generate_summary(analyses)
        print(f"\n📊 Batch Processing Summary:")
        print(f"Total Sessions Processed: {summary.get('total_sessions', 0)}")
        print(f"Resolution Rate: {summary.get('resolution_rate', '0%')}")
        print(f"Satisfaction Rate: {summary.get('satisfaction_rate', '0%')}")
        
        print(f"\n📄 Comprehensive report saved to: {report_path}")
    else:
        print("❌ No sessions were processed")

if __name__ == "__main__":
    asyncio.run(main())
