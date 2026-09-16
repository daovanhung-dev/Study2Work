import { describe, expect, it } from "vitest";

import { canAccessRole } from "./router";

describe("role route guard", () => {
  it("requires a token", () => {
    expect(canAccessRole(null, null, "student")).toBe(false);
  });

  it("allows the matching role and blocks a different role", () => {
    expect(canAccessRole("token", { role: "student" }, "student")).toBe(true);
    expect(canAccessRole("token", { role: "business" }, "student")).toBe(false);
  });

  it("rejects a token without a usable JWT principal", () => {
    expect(canAccessRole("token", null, "business")).toBe(false);
  });
});
