import { useEffect, useRef } from "react";
import type { LogEntry } from "../api";
import styles from "./LogPanel.module.css";

interface Props {
  logs: LogEntry[];
}

const typeColors: Record<LogEntry["type"], string> = {
  agent: "#89b4fa",
  tool: "#a6e3a1",
  error: "#f38ba8",
  success: "#a6e3a1",
  info: "#94a3b8",
};

const typeLabels: Record<LogEntry["type"], string> = {
  agent: "AGENT",
  tool: "TOOL",
  error: "ERROR",
  success: "DONE",
  info: "INFO",
};

export default function LogPanel({ logs }: Props) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  if (logs.length === 0) return null;

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <span className={styles.dot} />
        Agent Activity
      </div>
      <div className={styles.body}>
        {logs.map((entry, i) => (
          <div key={i} className={styles.entry}>
            <span className={styles.time}>{entry.time}</span>
            <span
              className={styles.badge}
              style={{ color: typeColors[entry.type] }}
            >
              [{typeLabels[entry.type]}]
            </span>
            <span
              className={styles.message}
              style={{
                color: entry.type === "error" ? typeColors.error : undefined,
                fontWeight: entry.type === "success" ? 600 : undefined,
              }}
            >
              {entry.message}
            </span>
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}
