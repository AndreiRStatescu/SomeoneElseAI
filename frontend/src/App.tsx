import { CharacterChat } from "./components/CharacterChat";
import { HealthStatus } from "./components/HealthStatus";
import { RandomParrot } from "./components/RandomParrot";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          SomeoneElseAI
        </h1>

        <HealthStatus />
        <CharacterChat />
        <RandomParrot />
      </div>
    </div>
  );
}

export default App;
