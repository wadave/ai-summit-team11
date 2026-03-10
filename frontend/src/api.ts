const API_BASE = "";
const APP_NAME = "backend";
const USER_ID = "web-user";

export interface LogEntry {
  time: string;
  message: string;
  type: "agent" | "tool" | "error" | "success" | "info";
}

export async function createSession(): Promise<string> {
  const sessionId = `session-${Date.now()}`;
  const resp = await fetch(
    `${API_BASE}/apps/${APP_NAME}/users/${USER_ID}/sessions`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: sessionId }),
    }
  );
  if (!resp.ok) throw new Error(`Failed to create session: ${resp.status}`);
  return sessionId;
}

export async function runAgent(
  message: string,
  onLog: (entry: LogEntry) => void,
  onResult: (text: string) => void,
  signal?: AbortSignal
): Promise<void> {
  onLog({
    time: now(),
    message: "Creating session...",
    type: "info",
  });

  const sessionId = await createSession();

  onLog({
    time: now(),
    message: `Session ${sessionId.slice(0, 16)}... created`,
    type: "info",
  });

  onLog({
    time: now(),
    message: "Sending request to orchestrator...",
    type: "agent",
  });

  const resp = await fetch(`${API_BASE}/run_sse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_name: APP_NAME,
      user_id: USER_ID,
      session_id: sessionId,
      new_message: {
        role: "user",
        parts: [{ text: message }],
      },
      streaming: false,
    }),
    signal,
  });

  if (!resp.ok) throw new Error(`API error: ${resp.status}`);

  const reader = resp.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalText = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const data = line.slice(6).trim();
      if (!data || data === "[DONE]") continue;

      try {
        const event = JSON.parse(data);
        const author: string = event.author || "system";
        const parts = event.content?.parts || [];

        for (const part of parts) {
          if (part.function_call) {
            onLog({
              time: now(),
              message: `${author} → ${part.function_call.name}()`,
              type: "tool",
            });
          } else if (part.function_response) {
            onLog({
              time: now(),
              message: `${part.function_response.name} returned`,
              type: "tool",
            });
          } else if (part.text) {
            onLog({
              time: now(),
              message: `${author} responding...`,
              type: "agent",
            });
            finalText = part.text;
          }
        }
      } catch {
        // skip malformed JSON
      }
    }
  }

  if (finalText) {
    onLog({ time: now(), message: "Complete!", type: "success" });
    onResult(finalText);
  } else {
    onLog({ time: now(), message: "No response received.", type: "error" });
  }
}

function now(): string {
  return new Date().toLocaleTimeString();
}
