Nêimport vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "127.0.0.2",
    port: 3002,
    strictPort: true,
  },
  preview: {
    host: "127.0.0.2",
    port: 3002,
    strictPort: true,
  },
});
