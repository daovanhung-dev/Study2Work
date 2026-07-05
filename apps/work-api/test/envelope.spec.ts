import { describe, expect, it } from "vitest";

import { createErrorEnvelope, createSuccessEnvelope } from "../src/common/api/envelope";

describe("API envelope", () => {
  it("creates success envelopes", () => {
    expect(
      createSuccessEnvelope(
        {
          businessCode: "SYSTEM_HEALTH_LIVE",
          message: "Work API is live.",
          data: { status: "ok" },
        },
        "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
      ),
    ).toEqual({
      success: true,
      businessCode: "SYSTEM_HEALTH_LIVE",
      message: "Work API is live.",
      data: { status: "ok" },
      meta: {},
      traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    });
  });

  it("creates error envelopes", () => {
    expect(
      createErrorEnvelope({
        businessCode: "SYSTEM_INTERNAL_ERROR",
        message: "Internal server error.",
        errors: [{ code: "INTERNAL_SERVER_ERROR", message: "Internal server error." }],
        traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
      }),
    ).toEqual({
      success: false,
      businessCode: "SYSTEM_INTERNAL_ERROR",
      message: "Internal server error.",
      errors: [{ code: "INTERNAL_SERVER_ERROR", message: "Internal server error." }],
      traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    });
  });
});
