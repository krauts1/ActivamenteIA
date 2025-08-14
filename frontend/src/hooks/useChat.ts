import { useState } from "react";

export function useChatState<T extends { role: "user" | "assistant"; content: string }>() {
  const [history, setHistory] = useState<T[]>([]);
  const push = (m: T) => setHistory((h) => [...h, m]);
  const clear = () => setHistory([]);
  return { history, push, clear };
}
