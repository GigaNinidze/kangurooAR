#!/usr/bin/env python3
"""
Test script for the backend API
"""
import requests
import json
import time

def test_backend():
    """Test the backend API"""
    base_url = "http://localhost:3001"
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Make sure the backend is running with: python app.py")
        return
    
    # Test chat endpoint
    print("\n🤖 Testing chat endpoint...")
    test_messages = [
        "Hello, who are you?",
        "What programs do you offer?",
        "Who is your CEO?",
        "Tell me about your exchange programs"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i}: {message} ---")
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                elapsed_time = (time.time() - start_time) * 1000
                
                print(f"✅ Response time: {elapsed_time:.3f}ms")
                print(f"📝 Text: {data.get('text', 'No text')}")
                print(f"🎵 Audio URL: {data.get('audioUrl', 'No audio')}")
                print(f"👄 Visemes: {data.get('visemes', [])}")
                
                # Check if response time is under 4 seconds
                if elapsed_time < 4000:
                    print("✅ Response time is under 4 seconds!")
                else:
                    print("⚠️ Response time is over 4 seconds")
                    
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing chat: {e}")
    
    print("\n🎉 Backend testing completed!")

if __name__ == "__main__":
    test_backend()
