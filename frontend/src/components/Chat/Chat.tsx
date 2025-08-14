import { useState } from "react";
import { askQuery } from "../../services/api";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import "./Chat.css";

type Msg = { role: "user" | "assistant"; content: string; sources?: any[] };

export default function Chat() {
  const [q, setQ] = useState("");
  const [structured, setStructured] = useState(false);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<Msg[]>([]);

  async function send(message?: string) {
    const text = (message ?? q).trim();
    if (!text) return;

    const user: Msg = { role: "user", content: text };
    setHistory((h) => [...h, user]);
    setLoading(true);

    try {
      const res = await askQuery(text, 6, structured);
      const assistant: Msg = {
        role: "assistant",
        content: res.answer,
        sources: res.sources,
      };
      setHistory((h) => [...h, assistant]);
    } catch (e: any) {
      setHistory((h) => [
        ...h,
        { role: "assistant", content: `Error: ${e?.response?.data?.detail ?? e.message}` },
      ]);
    } finally {
      setLoading(false);
      setQ("");
    }
  }

  return (
    <div className="card">
      <h3>Chat RAG</h3>

      <div className="chat-list">
        {history.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} sources={m.sources} />
        ))}
      </div>

      <div className="chat-actions">
        <label className="structured-toggle">
          <input
            type="checkbox"
            checked={structured}
            onChange={(e) => setStructured(e.target.checked)}
          />
          <span>structured</span>
        </label>

        <ChatInput
          value={q}
          onChange={setQ}
          onSend={() => send()}
          disabled={loading}
        />
      </div>
    </div>
  );
}
