import { useEffect, useRef, useState } from "react";
import { ingestAsync, ingestStatus } from "../../services/api";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState<string>("");
  const [jobId, setJobId] = useState<string | null>(null);
  const [phase, setPhase] = useState<"idle" | "queued" | "processing" | "success" | "error">("idle");

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const aliveRef = useRef<boolean>(true);

  async function onUpload() {
    if (!file) { setMsg("Selecciona un archivo"); return; }
    setMsg("Encolando trabajo…");
    setPhase("queued");

    try {
      const { job_id } = await ingestAsync(file);
      setJobId(job_id);
      setMsg(`Job creado (${job_id.slice(0, 8)}…). Procesando…`);
      setPhase("processing");

      if (timerRef.current) clearInterval(timerRef.current);

      timerRef.current = setInterval(async () => {
        if (!aliveRef.current || !job_id) return;
        try {
          const st = await ingestStatus(job_id);
          const s = (st.status || "").toLowerCase();

          if (s === "queued") {
            setPhase("queued");
            setMsg(`En cola (${job_id.slice(0, 8)}…).`);
          } else if (s === "processing") {
            setPhase("processing");
            setMsg("Procesando e indexando…");
          } else if (s === "done") {
            clearInterval(timerRef.current!);
            timerRef.current = null;
            setPhase("success");
            setMsg("Indexación completa.");
          } else if (s === "error") {
            clearInterval(timerRef.current!);
            timerRef.current = null;
            setPhase("error");
            setMsg(`Error: ${st.detail ?? "falló la indexación"}`);
          } else if (s === "not_found") {
            clearInterval(timerRef.current!);
            timerRef.current = null;
            setPhase("error");
            setMsg("Error: job no encontrado.");
          }
        } catch (err: any) {
          clearInterval(timerRef.current!);
          timerRef.current = null;
          setPhase("error");
          setMsg(`Error consultando estado: ${err?.message ?? "desconocido"}`);
        }
      }, 5000);
    } catch (e: any) {
      setPhase("error");
      setMsg(`Error al encolar: ${e?.response?.data?.detail ?? e.message}`);
    }
  }

  useEffect(() => {
    aliveRef.current = true;
    return () => {
      aliveRef.current = false;
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const disabled = phase === "queued" || phase === "processing";

  return (
    <div className="card">
      <h3>Ingestar documento</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        accept=".pdf,.txt,.md,.csv"
        disabled={disabled}
      />

      <button onClick={onUpload} disabled={!file || disabled}>
        {phase === "queued" ? "Encolado…" :
         phase === "processing" ? "Procesando…" :
         "Subir"}
      </button>

      <p className="muted">
        {msg}{jobId ? ` ${jobId ? `(job: ${jobId.slice(0,8)}…)` : ""}` : ""}
      </p>
    </div>
  );
}
