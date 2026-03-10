import { useState, useCallback } from "react";
import { runAgent, type LogEntry } from "../api";
import InputField from "./InputField";
import LogPanel from "./LogPanel";
import ResultsPanel from "./ResultsPanel";
import styles from "./Phase.module.css";

export default function Phase2() {
  const [blogUrl, setBlogUrl] = useState("");
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [result, setResult] = useState("");
  const [running, setRunning] = useState(false);

  const handleRun = useCallback(async () => {
    if (!blogUrl) {
      alert("Please enter a blog post URL.");
      return;
    }

    setRunning(true);
    setLogs([]);
    setResult("");

    const message = [
      "Run Phase 2: Campaign Generation.",
      `Blog Post URL: ${blogUrl}`,
    ].join("\n");

    try {
      await runAgent(
        message,
        (entry) => setLogs((prev) => [...prev, entry]),
        (text) => setResult(text)
      );
    } catch (err) {
      setLogs((prev) => [
        ...prev,
        {
          time: new Date().toLocaleTimeString(),
          message: `Error: ${err instanceof Error ? err.message : String(err)}`,
          type: "error",
        },
      ]);
    } finally {
      setRunning(false);
    }
  }, [blogUrl]);

  return (
    <div>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <h2 className={styles.cardTitle}>Generate Campaign-in-a-Box</h2>
          <p className={styles.cardDesc}>
            Paste a blog post URL to generate a complete multi-channel campaign
            — social posts, email, ads, and visuals — with a single click.
          </p>
        </div>

        <div className={styles.cardBody}>
          <InputField
            label="Blog Post URL"
            hint="The URL of the new blog post to promote"
            value={blogUrl}
            onChange={setBlogUrl}
            placeholder="https://your-blog.com/your-new-post"
            type="url"
          />

          <button
            className={styles.button}
            onClick={handleRun}
            disabled={running}
          >
            {running ? (
              <>
                <span className={styles.spinner} />
                Generating Campaign...
              </>
            ) : (
              "Generate Campaign-in-a-Box"
            )}
          </button>
        </div>
      </div>

      <LogPanel logs={logs} />
      <ResultsPanel content={result} />
    </div>
  );
}
