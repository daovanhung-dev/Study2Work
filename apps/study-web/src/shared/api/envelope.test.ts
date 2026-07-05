import { describe, expect, it } from "vitest";

import { isSuccessEnvelope, type ApiEnvelope } from "./envelope";

describe("API envelope", () => {
  it("narrows success envelopes", () => {
    const envelope: ApiEnvelope<{ status: string }> = {
      success: true,
      businessCode: "SYSTEM_HEALTH_LIVE",
      message: "Study API is live.",
      data: { status: "ok" },
      meta: {},
      traceId: "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    };

    expect(isSuccessEnvelope(envelope)).toBe(true);
  });
});
