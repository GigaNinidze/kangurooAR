import { Canvas } from "@react-three/fiber";
import { Suspense, useEffect, useState, useRef } from "react";
import { Experience } from "./Experience";
import { Visualizer } from "./Visualizer";
import { Chat } from "./Chat";



export const UI = () => {
  const [currentHash, setCurrentHash] = useState(
    window.location.hash.replace("#", "")
  );
  
  // Add the missing audioRef
  const audioRef = useRef(null);
  const [userInput, setUserInput] = useState("");
  const [currentVisemes, setCurrentVisemes] = useState([]);

  useEffect(() => {
    // When hash in the url changes, update the href state
    const handleHashChange = () => {
      setCurrentHash(window.location.hash.replace("#", ""));
    };
    window.addEventListener("hashchange", handleHashChange);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener("hashchange", handleHashChange);
    };
  }, []);

  const sendMessage = async () => {
    if (!userInput) return;

    const response = await fetch("http://localhost:3001/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();

    // Play audio
    audioRef.current.src = data.audioUrl;
    audioRef.current.play();

    // Send visemes to Avatar
    setCurrentVisemes(data.visemes);
  };

  const handleVoiceStart = () => {
    console.log('Voice recording started');
  };

  const handleVoiceEnd = (audioBlob) => {
    console.log('Voice recording ended', audioBlob);
    // Process the audio blob here
  };

  return (
    <section className="flex flex-row overflow-hidden h-full w-full">
      <div className="p-10 lg:max-w-2xl overflow-y-auto">
          <a
            className="pointer-events-auto select-none opacity-0 animate-fade-in-down animation-delay-200 "
            href="https://wawasensei.dev"
            target="_blank"
          >
            <img
              src="/images/wawasensei.png"
              alt="Wawa Sensei logo"
              className="w-20 h-20 object-contain"
            />
          </a>
          <Visualizer />
      </div>
      <Chat
        audioRef={audioRef}
        onVisemesChange={(visemes) => setCurrentVisemes(visemes)}
      />
      <div className="flex-1 bg-gradient-to-b from-pink-400 to-pink-200 relative">
        <Canvas shadows camera={{ position: [12, 8, 26], fov: 30 }}>
          <Suspense>
            <Experience externalVisemes={currentVisemes} audioRef={audioRef} />
          </Suspense>
        </Canvas>
        
        {/* <div className="bg-gradient-to-b from-transparent to-black/90 absolute bottom-0 top-3/4 left-0 right-0 pointer-events-none z-10">
          <div className="bottom-4 fixed z-20 right-4 md:right-15 flex items-center gap-4 animation-delay-1500 animate-fade-in-up opacity-0 ">
            <div className="w-20 h-px bg-white/60"></div>
            <a
              href="https://lessons.wawasensei.dev/courses/react-three-fiber/"
              className="text-white/60 text-xs pointer-events-auto select-none"
            >
              Learn Three.js & React Three Fiber
            </a>
          </div>
        </div> */}
      </div>
    </section>
  );
};