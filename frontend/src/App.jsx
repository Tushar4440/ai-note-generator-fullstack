import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [page, setPage] = useState("login"); // login | app
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [content, setContent] = useState("");
  const [notes, setNotes] = useState([]);
  const [token, setToken] = useState("");
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    if (token) {
      getNotes();
    }
  }, [token]);
  // ---------------- AUTH ----------------
  const register = async () => {
    await axios.post(`${API}/register`, null, { params: { email, password } });
    alert("Registered!");
  };

  const login = async () => {
    const res = await axios.post(`${API}/login`, null, {
      params: { email, password },
    });

    setToken(res.data.access_token);
    setPage("app");
    alert("Logged in!");
  };

  const logout = () => {
    setToken("");
    setPage("login");
  };

  // ---------------- NOTES ----------------
  const generateNotes = async () => {
    try {
      setLoading(true);

      await axios.post(`${API}/generate-notes`, null, {
        params: { content },
        headers: { Authorization: `Bearer ${token}` },
      });

      setContent("");
      await getNotes();
    } finally {
      setLoading(false);
    }
  };

  const getNotes = async () => {
    const res = await axios.get(`${API}/notes`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setNotes(res.data);
  };

  const deleteNote = async (id) => {
    await axios.delete(`${API}/notes/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    getNotes();
  };

  // ================= LOGIN PAGE =================
  if (page === "login") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-500 to-purple-600">
        <div className="bg-white p-8 rounded-xl shadow-lg w-80">
          <h2 className="text-2xl font-bold mb-4 text-center">
            🔐 Login
          </h2>

          <input
            className="w-full border p-2 mb-3 rounded"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="w-full border p-2 mb-4 rounded"
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={login}
            className="w-full bg-blue-500 text-white py-2 rounded mb-2 hover:bg-blue-600"
          >
            Login
          </button>

          <button
            onClick={register}
            className="w-full bg-gray-500 text-white py-2 rounded hover:bg-gray-600"
          >
            Register
          </button>
        </div>
      </div>
    );
  }

  // ================= APP DASHBOARD =================
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">📝 AI Notes</h1>
        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>

      {/* Input */}
      <div className="bg-white shadow-md rounded-xl p-4 max-w-2xl mx-auto mb-6">
        <textarea
          className="w-full border p-3 rounded mb-3"
          placeholder="Enter topic..."
          value={content}
          disabled={loading}
          onChange={(e) => setContent(e.target.value)}
        />

        <div className="flex items-center justify-between gap 5">
          <button
            onClick={generateNotes}
            disabled={loading}
            className={`px-4 py-2 rounded text-white ${loading
              ? "bg-purple-300"
              : "bg-purple-500 hover:bg-purple-600"
              }`}
          >
            {loading ? "Generating..." : "Generate Notes"}
          </button>

          {loading && (
            <div className="flex justify-center mt-3">
              <div className="w-6 h-6 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
          <button
            onClick={getNotes}
            className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
          >
            Refresh
          </button>

        </div>
      </div>

      {/* Notes */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
        {notes.map((n) => (
          <div key={n.id} className="bg-white p-4 rounded-xl shadow relative">
            <p className="text-gray-700 whitespace-pre-line">
              {n.content}
            </p>

            <button
              onClick={() => deleteNote(n.id)}
              className="absolute top-2 right-2 text-red-500"
            >
              ❌
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}