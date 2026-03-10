import { useState, useCallback } from "react";
import { runAgent, type LogEntry } from "../api";
import InputField from "./InputField";
import LogPanel from "./LogPanel";
import ResultsPanel from "./ResultsPanel";
import styles from "./Phase.module.css";

export default function Phase1() {
  const [sitemapUrl, setSitemapUrl] = useState("");
  const [industry, setIndustry] = useState("");
  const [keywords, setKeywords] = useState("");
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [result, setResult] = useState("");
  const [running, setRunning] = useState(false);

  const handleRun = useCallback(async () => {
    if (!sitemapUrl || !industry || !keywords) {
      alert("Please fill in all fields.");
      return;
    }

    setRunning(true);
    setLogs([]);
    setResult("");

    const message = [
      "Run Phase 1: Opportunity Discovery.",
      `Sitemap URL: ${sitemapUrl}`,
      `Industry: ${industry}`,
      `Seed Keywords: ${keywords}`,
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
  }, [sitemapUrl, industry, keywords]);

  return (
    <div>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <h2 className={styles.cardTitle}>Discover Content Opportunities</h2>
          <p className={styles.cardDesc}>
            Audit your blog and analyze the market to find high-value content
            gaps your competitors are capturing.
          </p>
        </div>

        <div className={styles.cardBody}>
          <InputField
            label="Company Sitemap URL"
            hint="e.g. https://your-blog.com/sitemap.xml"
            value={sitemapUrl}
            onChange={setSitemapUrl}
            placeholder="https://example.com/sitemap.xml"
            type="url"
          />
          <InputField
            label="Industry / Niche"
            hint="e.g. cloud computing, fintech, healthcare IT"
            value={industry}
            onChange={setIndustry}
            placeholder="cloud computing"
          />
          <InputField
            label="Seed Keywords"
            hint="Comma-separated keywords to research"
            value={keywords}
            onChange={setKeywords}
            placeholder="serverless, kubernetes, AI ops"
          />

          <button
            className={styles.button}
            onClick={handleRun}
            disabled={running}
          >
            {running ? (
              <>
                <span className={styles.spinner} />
                Discovering...
              </>
            ) : (
              "Discover Opportunities"
            )}
          </button>
        </div>
      </div>

      <LogPanel logs={logs} />
      <ResultsPanel content={result} />
    </div>
  );
}
