#!/usr/bin/env python3
"""
Test Gemini service directly
"""
import asyncio
import os
from dotenv import load_dotenv
from gemini_service import GeminiService

async def test_gemini():
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"API Key: {api_key[:10]}..." if api_key else "No API key")
    
    try:
        service = GeminiService(api_key)
        print("✅ Gemini service initialized")
        
        # Test a simple request
        response = await service.generate_response("Hello, who are you?")
        print(f"✅ Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini())
