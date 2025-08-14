import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 300_000,
});

export async function ingestAsync(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/ingest_async", form, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 60_000,
  });
  return data as { job_id: string; status: string };
}

export async function ingestStatus(job_id: string) {
  const { data } = await api.get(`/ingest_status/${job_id}`, {
    timeout: 60_000,
  });
  return data as Record<string, any>;
}

export async function ingestFile(
  file: File,
  onProgress?: (pct: number) => void
) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/ingest", form, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress: (evt) => {
      if (!evt.total) return;
      const pct = Math.round((evt.loaded * 100) / evt.total);
      onProgress?.(pct);
    },
    timeout: 300_000,
  });
  return data;
}

export async function askQuery(question: string, top_k = 6, structured = false) {
  const { data } = await api.post("/query", { question, top_k, structured });
  return data as {
    answer: string;
    sources: Array<any>;
    sql: Array<Record<string, any>> | null;
  };
}

export async function health() {
  const { data } = await api.get("/health");
  return data as { status: string; index_size: number };
}

export default api;
