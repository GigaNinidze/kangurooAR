#!/usr/bin/env python3
"""
Startup script for the backend server
"""
import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import flask
        import google.generativeai
        import aiohttp
        import aiofiles
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Please create .env file with your API keys")
        return False
    
    # Check if required keys are in .env
    with open('.env', 'r') as f:
        content = f.read()
        required_keys = ['GEMINI_API_KEY', 'ELEVENLABS_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            if key not in content:
                missing_keys.append(key)
            elif f"{key}=" in content and not content.split(f"{key}=")[1].split('\n')[0].strip():
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Missing API keys in .env: {missing_keys}")
            return False
    
    print("✅ .env file is properly configured")
    return True

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Kan-Guroo AI Backend Server...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check environment
    if not check_env_file():
        return False
    
    # Create static directories
    os.makedirs("static/audio", exist_ok=True)
    print("✅ Static directories created")
    
    print("\n🎯 Server Configuration:")
    print("- Port: 3001")
    print("- CORS: Enabled")
    print("- Services: Gemini + ElevenLabs")
    print("- Target Response Time: <4 seconds")
    
    print("\n🚀 Starting server...")
    print("=" * 50)
    
    try:
        # Start the server
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()
