import { useState, useRef, useEffect } from "react";
import { lipsyncManager } from "../App"; // Make sure this is exported from App

export const Chat = ({ audioRef, onVisemesChange }) => {
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const chatEndRef = useRef(null);

  // Auto-scroll on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // Handle Enter key to send message
  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const startTime = Date.now();
    console.log(`👤 User sent message [${new Date().toISOString()}]`);
    
    // Add user message
    setChatMessages((prev) => [...prev, { type: "user", text: userInput }]);
    const messageToSend = userInput;
    setUserInput("");

    try {
      // Call backend API (replace URL with your endpoint)
      const response = await fetch("http://localhost:3001/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageToSend }),
      });

      const data = await response.json();

      // Add AI response
      setChatMessages((prev) => [
        ...prev,
        { type: "ai", text: data.text },
      ]);

      // Play AI audio and connect to lipsync
      if (audioRef.current) {
        // Use full URL for audio
        const fullAudioUrl = `http://localhost:3001${data.audioUrl}`;
        console.log("🎵 Setting audio source:", fullAudioUrl);
        
        // Set up audio event listeners
        const audio = audioRef.current;
        
        const handleCanPlay = () => {
          console.log("🔗 Audio ready, connecting to lipsync manager");
          console.log("🎵 Audio duration:", audio.duration);
          console.log("🎵 Audio readyState:", audio.readyState);
          
          lipsyncManager.connectAudio(audio);
          
          // Play the audio
          console.log("▶️ Playing audio");
          audio.play().then(() => {
            console.log("✅ Audio started playing successfully");
            console.log(`🎬 Animation started [${new Date().toISOString()}]`);
            const totalTime = Date.now() - startTime;
            console.log(`⏱️ Total pipeline time: ${totalTime}ms`);
          }).catch(error => {
            console.error("❌ Audio play error:", error);
          });
        };
        
        const handleError = (error) => {
          console.error("❌ Audio loading error:", error);
        };
        
        const handleLoadStart = () => {
          console.log("📥 Audio loading started");
        };
        
        const handleLoadedData = () => {
          console.log("📊 Audio data loaded");
        };
        
        const handlePlay = () => {
          console.log("▶️ Audio play event fired");
        };
        
        // Add event listeners
        audio.addEventListener('canplay', handleCanPlay);
        audio.addEventListener('error', handleError);
        audio.addEventListener('loadstart', handleLoadStart);
        audio.addEventListener('loadeddata', handleLoadedData);
        audio.addEventListener('play', handlePlay);
        
        // Set the source (this will trigger loading)
        audio.src = fullAudioUrl;
        audio.load(); // Force reload
      }

      // Note: Visemes will be generated automatically by wawa-lipsync
      // No need to pass external visemes since we're using real-time analysis
    } catch (error) {
      console.error("Error sending message:", error);
      setChatMessages((prev) => [
        ...prev,
        { type: "ai", text: "Error: Failed to get response." },
      ]);
    }
  };

  return (
    <div className="flex flex-col gap-2 w-full max-w-5xl">
      {/* Chat messages */}
      <div className="chat-container h-[48rem] overflow-y-auto border p-4 rounded-lg bg-black/50 text-white flex flex-col gap-2">
        {chatMessages.map((msg, index) => (
          <div
            key={index}
            className={`p-2 rounded ${
              msg.type === "user" ? "bg-indigo-500 self-end" : "bg-gray-700 self-start"
            } max-w-full break-words`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      {/* Input + Send */}
      <div className="flex gap-2 mt-2">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask me anything..."
          className="border p-2 rounded flex-1"
        />
        <button
          onClick={sendMessage}
          className="bg-indigo-500 text-white px-4 py-2 rounded"
        >
          Send
        </button>
      </div>

      {/* Hidden audio for AI TTS */}
      <audio 
        ref={audioRef} 
        controls 
        style={{ display: 'none' }}
        crossOrigin="anonymous"
        preload="auto"
      />
    </div>
  );
};
