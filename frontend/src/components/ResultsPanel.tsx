import { useState } from "react";
import ReactMarkdown from "react-markdown";
import styles from "./ResultsPanel.module.css";

interface Props {
  content: string;
}

export default function ResultsPanel({ content }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  if (!content) return null;

  return (
    <div className={styles.panel}>
      <button
        className={styles.header}
        onClick={() => setCollapsed((c) => !c)}
      >
        <span className={styles.badge}>Results</span>
        <span className={styles.toggle}>{collapsed ? "+" : "−"}</span>
      </button>
      {!collapsed && (
        <div className={styles.body}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
