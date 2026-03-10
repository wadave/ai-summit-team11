const API_BASE = import.meta.env.DEV ? "http://localhost:8000" : "";

export interface LogEntry {
  time: string;
  message: string;
  type: "agent" | "tool" | "error" | "success" | "info";
}

export async function createSession(): Promise<string> {
  const resp = await fetch(`${API_BASE}/api/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!resp.ok) throw new Error(`Failed to create session: ${resp.status}`);
  const data = await resp.json();
  return data.id;
}

export async function runAgent(
  message: string,
  onLog: (entry: LogEntry) => void,
  onResult: (text: string) => void,
  signal?: AbortSignal
): Promise<void> {
  onLog({ time: now(), message: "Creating session...", type: "info" });

  const sessionId = await createSession();
  onLog({
    time: now(),
    message: `Session ${sessionId.slice(0, 12)}... created`,
    type: "info",
  });

  onLog({
    time: now(),
    message: "Sending request to orchestrator...",
    type: "agent",
  });

  const resp = await fetch(`${API_BASE}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
    signal,
  });

  if (!resp.ok) throw new Error(`API error: ${resp.status}`);

  const reader = resp.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let lastText = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    let currentEvent = "";

    for (const line of lines) {
      if (line.startsWith("event: ")) {
        currentEvent = line.slice(7).trim();
        continue;
      }
      if (!line.startsWith("data: ")) continue;
      const raw = line.slice(6).trim();
      if (!raw) continue;

      try {
        const data = JSON.parse(raw);

        switch (currentEvent) {
          case "tool_call":
            onLog({
              time: now(),
              message: `${data.author} → ${data.tool}()`,
              type: "tool",
            });
            break;
          case "tool_result":
            onLog({
              time: now(),
              message: `${data.tool} returned`,
              type: "tool",
            });
            break;
          case "message":
            onLog({
              time: now(),
              message: `${data.author} responding...`,
              type: "agent",
            });
            lastText = data.text;
            break;
          case "done":
            break;
        }
      } catch {
        // skip malformed JSON
      }
      currentEvent = "";
    }
  }

  if (lastText) {
    onLog({ time: now(), message: "Complete!", type: "success" });
    onResult(lastText);
  } else {
    onLog({ time: now(), message: "No response received.", type: "error" });
  }
}

function now(): string {
  return new Date().toLocaleTimeString();
}
