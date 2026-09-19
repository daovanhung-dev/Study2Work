import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // Work Web has no environment-driven runtime configuration. Keep Vite from
  // loading repository `.env` files even if one exists in the workspace.
  envDir: "./.vite-empty-env",
  plugins: [react()],
  server: {
    host: "127.0.0.2",
    port: 3001,
    strictPort: true,
    proxy: {
      "/api": "http://127.0.0.1:3002",
      "/uploads": "http://127.0.0.1:3002",
      "/img": "http://127.0.0.1:3002",
    },
  },
  preview: {
    host: "127.0.0.2",
    port: 3001,
    strictPort: true,
  },
});
