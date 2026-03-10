import { useState } from "react";
import Phase1 from "./components/Phase1";
import Phase2 from "./components/Phase2";
import styles from "./App.module.css";

type Tab = "phase1" | "phase2";

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>("phase1");

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>CE</div>
            <div>
              <h1 className={styles.title}>Content Engine</h1>
              <p className={styles.subtitle}>
                AI-powered SEO strategy &amp; campaign generation
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className={styles.main}>
        <nav className={styles.tabs}>
          <button
            className={`${styles.tab} ${activeTab === "phase1" ? styles.active : ""}`}
            onClick={() => setActiveTab("phase1")}
          >
            <span className={styles.tabIcon}>1</span>
            Opportunity Discovery
          </button>
          <button
            className={`${styles.tab} ${activeTab === "phase2" ? styles.active : ""}`}
            onClick={() => setActiveTab("phase2")}
          >
            <span className={styles.tabIcon}>2</span>
            Campaign Generation
          </button>
        </nav>

        <div className={styles.content}>
          {activeTab === "phase1" ? <Phase1 /> : <Phase2 />}
        </div>
      </main>

      <footer className={styles.footer}>
        Powered by Google ADK &amp; Gemini 2.5 Flash
      </footer>
    </div>
  );
}
