import { describe, expect, it } from "vitest";

import { getFieldErrors, isSuccessEnvelope, parseApiEnvelope, type ApiEnvelope } from "./envelope";

describe("API envelope", () => {
  it("narrows success envelopes", () => {
    const envelope: ApiEnvelope<{ status: string }> = {
      success: true,
      businessCode: "SYSTEM_HEALTH_LIVE",
      message: "Work API is live.",
      data: { status: "ok" },
      meta: {},
      traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    };

    expect(isSuccessEnvelope(envelope)).toBe(true);
  });

  it("reads canonical field errors from meta", () => {
    const envelope = parseApiEnvelope({
      success: false,
      businessCode: "PROFILE_VALIDATION_FAILED",
      message: "Please review the highlighted fields.",
      data: null,
      meta: {
        fieldErrors: [
          {
            field: "headline",
            code: "REQUIRED",
            message: "A headline is required.",
          },
        ],
      },
      traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    });

    if (isSuccessEnvelope(envelope)) {
      throw new Error("Expected an error envelope.");
    }

    expect(getFieldErrors(envelope)).toEqual([
      {
        field: "headline",
        code: "REQUIRED",
        message: "A headline is required.",
      },
    ]);
  });
});
