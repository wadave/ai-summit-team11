import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    watch: {
      usePolling: true,
      interval: 1000,
    },
    proxy: {
      "/apps": "http://localhost:8000",
      "/run_sse": "http://localhost:8000",
      "/run": "http://localhost:8000",
      "/list-apps": "http://localhost:8000",
    },
  },
  build: {
    outDir: "dist",
  },
});
