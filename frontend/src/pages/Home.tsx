import { useEffect, useState } from "react";
import Upload from "../components/Upload/Upload";
import Chat from "../components/Chat/Chat";
import { health } from "../services/api";

export default function Home() {
  const [status, setStatus] = useState<string>("…");
  const [indexSize, setIndexSize] = useState<number>(0);
  const base = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  useEffect(() => {
    (async () => {
      try {
        const h = await health();
        setStatus(h.status);
        setIndexSize(h.index_size);
      } catch {
        setStatus("error");
      }
    })();
  }, []);

  return (
    <div className="container">
      <header className="header">
        <h1>ActivaMente — RAG Client</h1>
        <div className="env">
          <span>API: {base}</span>
          <span>health: {status}</span>
          <span>index: {indexSize}</span>
        </div>
      </header>

      <main className="grid">
        <Upload />
        <Chat />
      </main>
    </div>
  );
}
