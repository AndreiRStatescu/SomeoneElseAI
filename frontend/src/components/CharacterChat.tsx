import { useState } from "react";

export function CharacterChat() {
  const [characterFile, setCharacterFile] = useState<string>("astra.yaml");
  const [chatMessage, setChatMessage] = useState<string>("");
  const [chatResponse, setChatResponse] = useState<string>("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleChat = async () => {
    if (!chatMessage.trim()) return;

    setIsChatLoading(true);
    setChatResponse("");

    try {
      const response = await fetch("/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          character_file: characterFile,
          message: chatMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          setChatResponse((prev) => prev + chunk);
        }
      }
    } catch (err) {
      console.error("Error fetching chat response:", err);
      setChatResponse("Error: Failed to get response");
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 mt-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">
        Character Chat
      </h2>

      <div className="mb-4">
        <label
          htmlFor="characterFile"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Select Character
        </label>
        <select
          id="characterFile"
          value={characterFile}
          onChange={(e) => setCharacterFile(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
          <option value="astra.yaml">Astra</option>
          <option value="cipher.yaml">Cipher</option>
          <option value="elara.yaml">Elara</option>
        </select>
      </div>

      <div className="mb-4">
        <label
          htmlFor="chatMessage"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Your Message
        </label>
        <textarea
          id="chatMessage"
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          rows={4}
          placeholder="Type your message here..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
        />
      </div>

      <button
        onClick={handleChat}
        disabled={isChatLoading || !chatMessage.trim()}
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isChatLoading ? "Chatting..." : "Send Message"}
      </button>

      {chatResponse && (
        <div className="mt-4 bg-white border border-indigo-200 rounded-lg p-4">
          <p className="text-gray-800 text-sm whitespace-pre-wrap">
            {chatResponse}
          </p>
        </div>
      )}
    </div>
  );
}
