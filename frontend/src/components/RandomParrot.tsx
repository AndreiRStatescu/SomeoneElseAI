import { useState } from "react";

export function RandomParrot() {
  const [numWords, setNumWords] = useState<number>(5);
  const [parrotText, setParrotText] = useState<string>("");
  const [isParrotLoading, setIsParrotLoading] = useState(false);

  const handleRandomParrot = async () => {
    setIsParrotLoading(true);
    setParrotText("");

    try {
      const response = await fetch(`/random_parrot?num_words=${numWords}`);
      if (!response.ok) {
        throw new Error("Random parrot failed");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          setParrotText((prev) => prev + chunk);
        }
      }
    } catch (err) {
      console.error("Error fetching random parrot:", err);
    } finally {
      setIsParrotLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 mt-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">
        Random Parrot
      </h2>

      <div className="mb-4">
        <label
          htmlFor="numWords"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Number of Words
        </label>
        <input
          id="numWords"
          type="number"
          min="1"
          max="50"
          value={numWords}
          onChange={(e) => setNumWords(parseInt(e.target.value) || 1)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>

      <button
        onClick={handleRandomParrot}
        disabled={isParrotLoading}
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isParrotLoading ? "Generating..." : "Generate Random Words"}
      </button>

      {parrotText && (
        <div className="mt-4 bg-white border border-indigo-200 rounded-lg p-4">
          <p className="text-gray-800 font-mono text-sm">{parrotText}</p>
        </div>
      )}
    </div>
  );
}
