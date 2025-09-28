import os
import time
import asyncio
import aiohttp
import aiofiles
from typing import Optional

class ElevenLabsService:
    def __init__(self, api_key: str, voice_id: Optional[str] = None):
        """Initialize ElevenLabs service"""
        self.api_key = api_key
        # Using a voice that works well with Georgian language
        self.voice_id = voice_id or "pNInz6obpgDQGcFmaJgB"  # Default voice if not provided
        self.base_url = "https://api.elevenlabs.io/v1"
        
        print(f"ElevenLabs service initialized with voice ID: {self.voice_id} (dynamic model selection)")
    
    async def generate_audio(self, text: str, language: str = "georgian") -> str:
        """Generate audio from text using ElevenLabs"""
        start_time = time.time()
        
        try:
            elevenlabs_start = time.time()
            print(f"🎵 ElevenLabs TTS started [{time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z]")
            
            # Select model based on language
            model_id = "eleven_v3" if language == "georgian" else "eleven_turbo_v2_5"
            print(f"🎵 Using {model_id} model for {language} language")
            print(f"🎵 Text to convert: {text[:100]}...")
            print(f"🎵 Text length: {len(text)} characters")
            
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            # Use different voice settings for Georgian vs English
            if language == "georgian":
                voice_settings = {
                    "stability": 1.0,  # Robust stability for Georgian (valid value)
                    "similarity_boost": 0.8,  # Higher similarity for Georgian
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            else:
                voice_settings = {
                    "stability": 0.5,  # Natural stability for English
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            
            data = {
                "text": text,
                "model_id": model_id,
                "voice_settings": voice_settings
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    print(f"🎵 Response status: {response.status}")
                    print(f"🎵 Response headers: {dict(response.headers)}")
                    print(f"🎵 Content-Type: {response.headers.get('Content-Type', 'Not set')}")
                    print(f"🎵 Content-Length: {response.headers.get('Content-Length', 'Not set')}")
                    if response.status == 200:
                        # Create audio directory if it doesn't exist
                        os.makedirs("static/audio", exist_ok=True)
                        
                        # Generate unique filename
                        timestamp = int(time.time() * 1000)
                        filename = f"audio_{timestamp}.mp3"
                        filepath = f"static/audio/{filename}"
                        
                        # Save audio file
                        file_size = 0
                        async with aiofiles.open(filepath, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                await f.write(chunk)
                                file_size += len(chunk)
                        
                        # Log performance
                        elapsed_time = (time.time() - start_time) * 1000
                        print(f"✅ ElevenLabs TTS completed in {elapsed_time:.3f}ms")
                        print(f"🎵 Audio file size: {file_size} bytes")
                        print(f"🎵 Audio file path: {filepath}")
                        
                        # Check if file exists and is readable
                        if os.path.exists(filepath):
                            print(f"✅ Audio file exists and is accessible")
                        else:
                            print(f"❌ Audio file does not exist at {filepath}")
                        
                        # Return relative URL for frontend
                        return f"/static/audio/{filename}"
                    else:
                        error_text = await response.text()
                        print(f"ElevenLabs API error: {response.status} - {error_text}")
                        raise Exception(f"ElevenLabs API error: {response.status}")
                        
        except Exception as e:
            print(f"Error in ElevenLabs service: {e}")
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    async def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            url = f"{self.base_url}/voices"
            headers = {"xi-api-key": self.api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("voices", [])
                    else:
                        print(f"Error fetching voices: {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []
    
    def get_voice_info(self) -> dict:
        """Get current voice information"""
        return {
            "voice_id": self.voice_id,
            "model": "eleven_v3",
            "stability": 0.5,
            "similarity_boost": 0.5
        }
