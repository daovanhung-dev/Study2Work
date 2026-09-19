import assert from "node:assert/strict";
import { test } from "node:test";

import {
  backendHost,
  backendPort,
  ensureConstantsFile,
  frontendHost,
  frontendPort,
} from "./dev.mjs";

test("launcher uses the canonical DB Admin server and client addresses", () => {
  assert.deepEqual(
    { backendHost, backendPort, frontendHost, frontendPort },
    {
      backendHost: "127.0.0.1",
      backendPort: 3001,
      frontendHost: "127.0.0.2",
      frontendPort: 3000,
    },
  );
});

test("launcher reports a missing local constants file", () => {
  assert.throws(
    () => ensureConstantsFile("/tmp/db-admin-constants-that-does-not-exist.py"),
    /Thiếu .*constants\.py/u,
  );
});
