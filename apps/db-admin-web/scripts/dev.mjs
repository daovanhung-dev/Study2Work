import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const webRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const serverRoot = resolve(webRoot, "../db-admin-server");
const constantsPath = resolve(serverRoot, "app/core/constants.py");
const backendHost = "127.0.0.1";
const backendPort = 8010;
const frontendHost = "127.0.0.1";
const frontendPort = 5175;
const startupTimeoutMs = 60_000;

function ensureConstantsFile(path = constantsPath) {
  if (!existsSync(path)) {
    throw new Error(
      `Thiếu ${path}. Hãy copy constants.example.py thành constants.py và điền cấu hình local.`,
    );
  }
}

function waitForBackend(child, url) {
  return new Promise((resolvePromise, rejectPromise) => {
    const deadline = Date.now() + startupTimeoutMs;
    let timer;

    const cleanup = () => {
      if (timer) clearTimeout(timer);
      child.off("exit", onExit);
    };

    const onExit = (code, signal) => {
      cleanup();
      rejectPromise(
        new Error(
          `FastAPI dừng trước khi sẵn sàng (code=${code ?? "-"}, signal=${signal ?? "-"}).`,
        ),
      );
    };

    const poll = async () => {
      try {
        const response = await fetch(url);
        if (response.ok) {
          cleanup();
          resolvePromise();
          return;
        }
      } catch {
        // The server can need a few seconds to bind its loopback port.
      }

      if (Date.now() >= deadline) {
        cleanup();
        rejectPromise(new Error("FastAPI không sẵn sàng trong thời gian chờ 60 giây."));
        return;
      }
      timer = setTimeout(poll, 250);
    };

    child.once("exit", onExit);
    void poll();
  });
}

function terminate(child) {
  if (child && child.exitCode === null && !child.killed) child.kill("SIGTERM");
}

function stopChildren(children, exitCode) {
  for (const child of children) terminate(child);

  const active = children.filter((child) => child && child.exitCode === null);
  if (!active.length) {
    process.exit(exitCode);
  }

  let remaining = active.length;
  const finish = () => {
    remaining -= 1;
    if (remaining === 0) process.exit(exitCode);
  };
  for (const child of active) child.once("close", finish);
  setTimeout(() => process.exit(exitCode), 5_000).unref();
}

let backend;
let frontend;
let shuttingDown = false;

function shutdown(exitCode = 0) {
  if (shuttingDown) return;
  shuttingDown = true;
  stopChildren([frontend, backend].filter(Boolean), exitCode);
}

process.once("SIGINT", () => shutdown(130));
process.once("SIGTERM", () => shutdown(143));

async function main() {
  try {
    ensureConstantsFile();
  } catch (error) {
    console.error(`[db-admin] ${error.message}`);
    process.exitCode = 1;
    return;
  }

  backend = spawn(
    "uv",
    ["run", "--no-env-file", "--no-dev", "uvicorn", "app.main:app", "--host", backendHost, "--port", String(backendPort)],
    { cwd: serverRoot, env: process.env, stdio: "inherit" },
  );
  backend.once("error", (error) => {
    if (!shuttingDown) {
      console.error(`[db-admin] Không thể khởi động FastAPI: ${error.message}`);
      shutdown(1);
    }
  });

  try {
    await waitForBackend(backend, `http://${backendHost}:${backendPort}/health/live`);
  } catch (error) {
    console.error(`[db-admin] ${error.message}`);
    shutdown(1);
    return;
  }

  console.log(`[db-admin] FastAPI sẵn sàng tại http://${backendHost}:${backendPort}`);
  frontend = spawn(
    process.execPath,
    [resolve(webRoot, "node_modules/@angular/cli/bin/ng.js"), "serve", "--host", frontendHost, "--port", String(frontendPort)],
    { cwd: webRoot, env: process.env, stdio: "inherit" },
  );
  frontend.once("error", (error) => {
    if (!shuttingDown) {
      console.error(`[db-admin] Không thể khởi động Angular: ${error.message}`);
      shutdown(1);
    }
  });
  frontend.once("close", (code, signal) => {
    if (!shuttingDown) {
      console.log(`[db-admin] Angular đã dừng (code=${code ?? "-"}, signal=${signal ?? "-"}).`);
      shutdown(code ?? 1);
    }
  });
  backend.once("close", (code, signal) => {
    if (!shuttingDown) {
      console.error(`[db-admin] FastAPI đã dừng (code=${code ?? "-"}, signal=${signal ?? "-"}).`);
      shutdown(1);
    }
  });
  console.log(`[db-admin] Mở http://${frontendHost}:${frontendPort}`);
}

const isMainModule = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMainModule) void main();

export { ensureConstantsFile };
