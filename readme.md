# AI 3D Avatar Chat System - Complete Documentation

## 👥 Contributors
- **Frontend and lipsync** - Luka Gobechia
- **Backend and AI generation** - Giga Ninidze

## 🚀 Quick Start

### 1. Backend Setup
Add `.env` file in the backend folder with environmental variables:
```
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=fq1SdXsX6OokE10pJ4Xw
```

Then run:
```bash
cd Backend
python start_server.py
```

### 2. Frontend Setup
```bash
cd AI-3DAvatar
npm run build
```

### 3. Session Analysis (NEW!)
Analyze customer support sessions for insights:
```bash
cd Backend/analysis
python run_analysis.py
```

## 📊 Session Analysis & Insights

### 🔍 AI-Powered Session Evaluation
The system now includes comprehensive session analysis capabilities:

- **Automatic Session Saving**: All customer interactions are automatically saved with timestamps
- **AI Quality Analysis**: Each session is evaluated using Gemini AI for quality metrics
- **Performance Insights**: Track resolution rates, customer satisfaction, and communication quality
- **Improvement Recommendations**: Get actionable insights for service enhancement

### 📈 Analysis Features
- **Resolution Tracking**: Monitor which issues are successfully resolved
- **Customer Sentiment**: Analyze customer satisfaction levels
- **Communication Quality**: Evaluate response effectiveness
- **Troubleshooting Analysis**: Assess problem-solving approaches
- **Performance Metrics**: Generate comprehensive reports

### 🎯 Key Metrics Analyzed
- Overall session rating (1-10)
- Issue resolution status
- Customer satisfaction levels
- Response time quality
- Troubleshooting effectiveness
- Communication quality
- Customer sentiment analysis
- Escalation needs
- Improvement suggestions

## 🎯 Overview


This is a real-time 3D avatar chat system that combines AI responses (Gemini), text-to-speech (ElevenLabs), and real-time lip-sync animation using the `wawa-lipsync` library. The system provides a conversational AI experience with a 3D avatar that speaks and animates in real-time.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP API    ┌─────────────────┐    Real-time Audio    ┌─────────────────┐
│   Frontend      │ ──────────────► │   Backend       │ ───────────────────► │   3D Avatar     │
│   (React + R3F) │                 │   (Flask)       │                      │   (Lip-sync)    │
└─────────────────┘                 └─────────────────┘                      └─────────────────┘
         │                                   │
         │                                   │
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│   wawa-lipsync  │                 │   Gemini API   │
│   (Audio Analysis)│                │   (AI Responses)│
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │  ElevenLabs API │
                                     │  (Text-to-Speech)│
                                     └─────────────────┘
```

## 📁 Project Structure

```
lukaavatar/
├── AI-3DAvatar/                 # Frontend (React + Three.js)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Avatar.jsx       # 3D Avatar with lip-sync
│   │   │   ├── Chat.jsx         # Chat interface
│   │   │   ├── UI.jsx           # Main layout
│   │   │   └── Visualizer.jsx   # 3D scene
│   │   ├── App.jsx              # Main app with lipsync manager
│   │   └── index.js
│   ├── packages/
│   │   └── wawa-lipsync/        # Custom lip-sync library
│   └── package.json
├── Backend/                     # Backend (Flask + Python)
│   ├── app.py                   # Main Flask application
│   ├── gemini_service.py       # Gemini AI integration
│   ├── elevenlabs_service.py    # ElevenLabs TTS integration
│   ├── analysis/                # Session Analysis Module (NEW!)
│   │   ├── session_analyzer.py  # AI-powered session evaluation
│   │   ├── batch_processor.py # Batch processing for large datasets
│   │   ├── run_analysis.py      # Simple analysis runner
│   │   └── reports/             # Generated analysis reports
│   ├── sessions/                # Saved customer sessions
│   ├── requirements.txt         # Python dependencies
│   ├── start_server.py         # Server startup script
│   └── static/audio/           # Generated audio files
└── FullREADME.md               # This documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- API Keys: Gemini, ElevenLabs

### 1. Backend Setup
```bash
cd Backend
pip install -r requirements.txt
cp env_example.txt .env
# Edit .env with your API keys
python start_server.py
```

### 2. Frontend Setup
```bash
cd AI-3DAvatar
npm install
npm run dev
```

### 3. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:3001

## 🔧 Backend Components

### Flask Application (`app.py`)

**Purpose**: Main server that handles API requests and coordinates AI services.

**Key Features**:
- CORS enabled for frontend communication
- Async handling of AI and TTS services
- Static file serving for generated audio
- Performance logging and debugging

**API Endpoints**:
- `POST /api/chat` - Main chat endpoint
- `GET /static/audio/<filename>` - Serve generated audio files
- `GET /health` - Health check endpoint

**Flow**:
1. Receives user message from frontend
2. Calls Gemini service for AI response
3. Calls ElevenLabs service for audio generation
4. Returns text and audio URL to frontend

### Gemini Service (`gemini_service.py`)

**Purpose**: Handles AI text generation using Google's Gemini API.

**Key Features**:
- Custom prompt engineering with company context
- Performance timing and logging
- Error handling and fallback responses
- Async processing for better performance

**Configuration**:
- Model: `gemini-1.5-pro` (configurable)
- Context: Company data from `Company_data.json`
- Performance target: < 2 seconds

### ElevenLabs Service (`elevenlabs_service.py`)

**Purpose**: Converts AI text responses to natural speech audio.

**Key Features**:
- Fast TTS using `eleven_turbo_v2_5` model
- Audio file generation and storage
- Performance timing and logging
- Async processing with aiohttp

**Configuration**:
- Model: `eleven_turbo_v2_5` (fastest)
- Voice settings optimized for speed
- Audio format: MP3
- Performance target: < 2 seconds

### Mock Services (`mock_gemini_service.py`)

**Purpose**: Provides fallback responses when API quotas are exceeded.

**Features**:
- Predefined responses for testing
- Same interface as real services
- Enables development without API costs

### Session Analysis Module (`analysis/`)

**Purpose**: AI-powered evaluation of customer support sessions for quality insights.

**Key Features**:
- **Automatic Session Saving**: All conversations saved with timestamps
- **AI Quality Analysis**: Gemini AI evaluates session effectiveness
- **Comprehensive Metrics**: Resolution rates, satisfaction, communication quality
- **Batch Processing**: Handle large numbers of sessions efficiently
- **JSON Reports**: Detailed analysis reports with actionable insights

**Analysis Components**:
- `session_analyzer.py` - Core analysis engine with AI evaluation
- `batch_processor.py` - Efficient batch processing for large datasets
- `run_analysis.py` - Simple command-line interface
- `reports/` - Generated analysis reports and insights

**Analysis Metrics**:
- Overall session rating (1-10)
- Issue resolution status
- Customer satisfaction levels
- Response time quality
- Troubleshooting effectiveness
- Communication quality
- Customer sentiment analysis
- Escalation needs
- Improvement suggestions

**Usage**:
```bash
cd Backend/analysis
python run_analysis.py              # Single analysis
python run_analysis.py --batch      # Batch processing
python test_analysis.py             # Test functionality
```

## 🎨 Frontend Components

### Main Application (`App.jsx`)

**Purpose**: Initializes the global lipsync manager and renders the main UI.

**Key Features**:
- Global `lipsyncManager` instance
- Component composition and layout
- State management for the entire app

### Chat Interface (`Chat.jsx`)

**Purpose**: Handles user input and displays conversation history.

**Key Features**:
- Real-time message sending
- Audio playback integration
- Performance debugging timestamps
- Error handling and user feedback

**Flow**:
1. User types message and hits send
2. Sends POST request to backend
3. Receives AI response and audio URL
4. Plays audio and connects to lipsync
5. Displays response in chat

**Performance Debugging**:
- User message timestamp
- Animation start timestamp
- Total pipeline timing

### 3D Avatar (`Avatar.jsx`)

**Purpose**: Renders the 3D avatar with real-time lip-sync animation.

**Key Features**:
- Three.js/React Three Fiber integration
- Morph target animation system
- Real-time viseme detection
- Smooth animation transitions

**Animation System**:
- Uses `wawa-lipsync` for real-time audio analysis
- Applies visemes to 3D model morph targets
- Smooth interpolation between viseme states
- Blink and wink animations

### UI Layout (`UI.jsx`)

**Purpose**: Main layout component that orchestrates all UI elements.

**Components**:
- Visualizer (3D scene)
- Chat interface
- Experience (Avatar container)

## 🎵 Audio & Animation Pipeline

### Real-time Lip-sync (`wawa-lipsync`)

**Purpose**: Analyzes audio in real-time to generate viseme data for avatar animation.

**Key Features**:
- Real-time audio analysis
- Viseme detection and classification
- Smooth animation transitions
- Performance optimized

**Viseme Types**:
- `viseme_sil` - Silence
- `viseme_aa` - "ah" sound
- `viseme_ee` - "ee" sound
- `viseme_oo` - "oo" sound
- And more...

### Animation Flow

1. **Audio Generation**: ElevenLabs generates audio from text
2. **Audio Playback**: Frontend plays audio through HTML5 audio element
3. **Real-time Analysis**: `wawa-lipsync` analyzes audio stream
4. **Viseme Detection**: Library detects speech patterns and generates visemes
5. **Avatar Animation**: 3D avatar applies morph targets based on visemes
6. **Smooth Transitions**: Interpolation creates natural-looking speech

## ⚡ Performance Optimization

### Performance Targets
- **Total Pipeline**: < 4 seconds
- **Gemini Response**: < 2 seconds
- **ElevenLabs TTS**: < 2 seconds
- **Animation Start**: < 4 seconds

### Optimization Strategies

**Backend**:
- Async processing for AI and TTS
- Fast Gemini model (`gemini-1.5-pro`)
- Turbo ElevenLabs model (`eleven_turbo_v2_5`)
- Optimized voice settings

**Frontend**:
- Real-time audio analysis
- Efficient 3D rendering
- Smooth animation interpolation
- Minimal re-renders

### Performance Debugging

**Console Output**:
```
👤 User sent message [timestamp]
🤖 Gemini response started [timestamp]
✅ Gemini response completed in XXXms
🎵 ElevenLabs TTS started [timestamp]
✅ ElevenLabs TTS completed in XXXms
🎬 Animation started [timestamp]
⏱️ Total pipeline time: XXXms
```

## 🔧 Configuration

### Environment Variables (`.env`)
```
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id
```

### Company Data (`Company_data.json`)
Contains company-specific information used to contextualize AI responses:
- Company details
- Programs and services
- Team information
- Contact information

## 🐛 Troubleshooting

### Common Issues

**Audio Not Playing**:
- Check CORS settings
- Verify audio file URLs
- Check browser audio permissions

**Avatar Not Animating**:
- Verify `lipsyncManager.connectAudio()` is called
- Check audio element is properly connected
- Ensure viseme data is being generated

**Slow Performance**:
- Check API quotas and limits
- Monitor network latency
- Verify model configurations

### Debug Tools

**Backend Logs**:
- Performance timestamps
- API response times
- Error messages

**Frontend Console**:
- Audio loading events
- Lipsync connection status
- Animation state changes

## 🚀 Deployment

### Production Considerations

**Backend**:
- Use production WSGI server (Gunicorn)
- Configure proper CORS settings
- Set up API rate limiting
- Monitor performance metrics

**Frontend**:
- Build for production (`npm run build`)
- Configure CDN for static assets
- Optimize 3D models and textures
- Enable service workers for caching

### Security

**API Keys**:
- Never expose API keys in frontend
- Use environment variables
- Implement proper CORS policies
- Monitor API usage and quotas

## 📊 Monitoring

### Performance Metrics
- Response times for each service
- Audio generation time
- Animation start time
- Total pipeline duration

### Health Checks
- Backend health endpoint
- API connectivity
- Audio file generation
- Lipsync functionality

## 🔮 Future Enhancements

### Potential Improvements
- Multiple avatar models
- Custom voice training
- Emotion detection
- Multi-language support
- Real-time video streaming
- Advanced animation systems

### Scalability
- Microservices architecture
- Load balancing
- Caching strategies
- Database integration
- User management

## 📝 Development Notes

### Code Organization
- Modular service architecture
- Clear separation of concerns
- Comprehensive error handling
- Performance monitoring
- Debug logging

### Testing
- Unit tests for services
- Integration tests for API
- Performance benchmarks
- User experience testing

---

**This system represents a complete real-time AI avatar solution with optimized performance and comprehensive debugging capabilities.**


