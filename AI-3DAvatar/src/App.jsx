import { Loader } from "@react-three/drei";
import { Lipsync } from "../packages/wawa-lipsync/src/lipsync";
import { UI } from "./components/UI";

export const lipsyncManager = new Lipsync({});

function App() {
  return (
    <>
      <Loader />
      <UI />
    </>
  );
}

export default App;
