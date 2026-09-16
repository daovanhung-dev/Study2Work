import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  DATABASE_URL,
  DIRECT_DATABASE_URL,
} from "../src/utils/constants.js";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const prismaBin = resolve(
  appRoot,
  "node_modules",
  ".bin",
  process.platform === "win32" ? "prisma.cmd" : "prisma"
);
const prismaEntry = resolve(appRoot, "node_modules", "prisma", "build", "index.js");
const command = existsSync(prismaBin) ? prismaBin : process.execPath;
const commandArgs = existsSync(prismaBin)
  ? process.argv.slice(2)
  : [prismaEntry, ...process.argv.slice(2)];

const child = spawn(command, commandArgs, {
  cwd: appRoot,
  env: {
    ...process.env,
    DATABASE_URL,
    DIRECT_DATABASE_URL,
  },
  shell: process.platform === "win32",
  stdio: "inherit",
});

child.on("error", (error) => {
  console.error("Không thể chạy Prisma CLI:", error.message);
  process.exit(1);
});

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }

  process.exit(code ?? 1);
});
