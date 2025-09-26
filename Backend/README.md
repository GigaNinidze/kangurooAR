# Kan-Guroo AI Backend Service

This backend provides AI-powered chat functionality for the 3D Avatar application with Kan-Guroo company context.

## Features

- **Text Generation**: Google Gemini 1.5 Flash for fast responses
- **Voice Synthesis**: ElevenLabs Turbo v2.5 for high-quality audio generation
- **Company Context**: Uses Company_data.json for Kan-Guroo specific responses
- **Performance**: Target <4 seconds total response time
- **Security**: API keys stored securely on server-side

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
# Copy the example file
cp env_example.txt .env

# Edit .env with your API keys
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here
```

3. **Start the server:**
```bash
python start_server.py
```

The server will run on `http://localhost:3001`

## API Endpoints

- `POST /api/chat` - Main chat endpoint
- `GET /health` - Health check
- `GET /static/audio/<filename>` - Serve audio files

## Response Format

```json
{
  "text": "AI response text",
  "audioUrl": "/static/audio/audio_1234567890.mp3",
  "visemes": []
}
```

## Performance Targets

- **Gemini Response**: <2000ms
- **ElevenLabs Audio**: <1500ms
- **Total Response**: <4000ms

## Testing

Run the test script to verify everything works:
```bash
python test_backend.py
```

## Company Context

The AI is configured with Kan-Guroo company information:
- Company details and mission
- Available programs (exchange, summer schools, university programs)
- Team information
- Contact details
- FAQ responses

## Architecture

```
User Message → Flask API → Gemini Service → ElevenLabs Service → Frontend
```

1. **User sends message** to `/api/chat`
2. **Gemini generates response** using company context
3. **ElevenLabs creates audio** from text response
4. **Frontend receives** text + audio URL
5. **Frontend plays audio** and generates visemes with wawa-lipsync
