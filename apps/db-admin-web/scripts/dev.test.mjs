import assert from "node:assert/strict";
import { test } from "node:test";

import { ensureConstantsFile } from "./dev.mjs";

test("launcher reports a missing local constants file", () => {
  assert.throws(
    () => ensureConstantsFile("/tmp/db-admin-constants-that-does-not-exist.py"),
    /Thiếu .*constants\.py/u,
  );
});
