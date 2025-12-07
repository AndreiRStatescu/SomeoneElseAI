import { useEffect, useState } from "react";

interface HealthStatus {
  status: string;
}

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch("/healthz");
        if (!response.ok) {
          throw new Error("Health check failed");
        }
        const data = await response.json();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
        setHealth(null);
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          SomeoneElseAI
        </h1>

        <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            Health Status
          </h2>

          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700 font-medium">Error</p>
              <p className="text-red-600 text-sm mt-1">{error}</p>
            </div>
          ) : health ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-3 animate-pulse"></div>
                <p className="text-green-700 font-medium">
                  Status:{" "}
                  <span className="text-green-800">{health.status}</span>
                </p>
              </div>
            </div>
          ) : null}

          <p className="text-gray-500 text-xs mt-4 text-center">
            Auto-refreshes every 10 seconds
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
