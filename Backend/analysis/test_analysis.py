#!/usr/bin/env python3
"""
Test script for session analysis functionality
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.session_analyzer import SessionAnalyzer

async def test_analysis():
    """Test the session analysis functionality"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
        return
    
    # Initialize analyzer
    analyzer = SessionAnalyzer(api_key)
    
    print("🧪 Testing session analysis...")
    
    # Test loading a session file
    session_files = analyzer.get_all_session_files("../sessions")
    if not session_files:
        print("❌ No session files found in ../sessions")
        return
    
    print(f"📄 Found {len(session_files)} session files")
    
    # Test loading the first session
    first_file = session_files[0]
    print(f"📖 Loading session file: {os.path.basename(first_file)}")
    
    session_data = analyzer.load_session_file(first_file)
    if not session_data:
        print("❌ Failed to load session data")
        return
    
    print(f"✅ Session loaded successfully:")
    print(f"  - Session ID: {session_data['session_id']}")
    print(f"  - Language: {session_data['language']}")
    print(f"  - Duration: {session_data['duration']}")
    print(f"  - Issue Type: {session_data['issue_type']}")
    print(f"  - Messages: {len(session_data['conversation_history'])}")
    
    # Test analysis (optional - requires API call)
    print(f"\n🔍 Testing AI analysis...")
    try:
        analysis = await analyzer.analyze_session(session_data)
        print(f"✅ Analysis completed:")
        print(f"  - Session ID: {analysis.get('session_id', 'N/A')}")
        if 'analysis_error' in analysis:
            print(f"  - Error: {analysis['analysis_error']}")
        else:
            print(f"  - Overall Rating: {analysis.get('overall_rating', 'N/A')}")
            print(f"  - Issue Resolved: {analysis.get('issue_resolved', 'N/A')}")
            print(f"  - Customer Satisfaction: {analysis.get('customer_satisfaction', 'N/A')}")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    
    print(f"\n🏁 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_analysis())
