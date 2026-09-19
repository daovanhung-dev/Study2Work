import { beforeEach, describe, expect, it, vi } from "vitest";

import { apiRequest } from "./work";
import { TOKEN_KEY, useAuthStore } from "../auth/store";

function installBrowserStubs() {
  const values = new Map<string, string>();
  Object.defineProperty(globalThis, "localStorage", {
    configurable: true,
    value: {
      getItem: (key: string) => values.get(key) ?? null,
      setItem: (key: string, value: string) => values.set(key, value),
      removeItem: (key: string) => values.delete(key),
    },
  });
  Object.defineProperty(globalThis, "window", {
    configurable: true,
    value: { location: { origin: "http://127.0.0.2:3001" } },
  });
}

describe("Work API boundary", () => {
  beforeEach(() => {
    installBrowserStubs();
    useAuthStore.setState({ token: null, user: null, hydrated: true });
    vi.restoreAllMocks();
  });

  it("sends one Bearer header and never opts into cookies", async () => {
    const token = "header.payload.signature";
    useAuthStore.getState().setAuth({
      token,
      user: { id: 7, email: "student@example.test", role: "student" },
    });
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({
        success: true,
        businessCode: "ME_LOADED",
        message: "ok",
        data: { id: 7, email: "student@example.test", role: "student" },
        meta: {},
        traceId: "trace-1",
      }), { status: 200, headers: { "Content-Type": "application/json" } }),
    );

    await apiRequest("/me");

    const [, init] = fetchMock.mock.calls[0];
    const headers = new Headers(init?.headers);
    expect(headers.get("Authorization")).toBe(`Bearer ${token}`);
    expect(headers.get("Cookie")).toBeNull();
    expect(init?.credentials).toBe("omit");
    expect(localStorage.getItem(TOKEN_KEY)).toBe(token);
  });

  it("clears the local token on a 401 response", async () => {
    useAuthStore.getState().setAuth({
      token: "expired.token.signature",
      user: { id: 7, email: "student@example.test", role: "student" },
    });
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({
        success: false,
        businessCode: "UNAUTHORIZED",
        message: "Unauthorized",
        data: null,
        meta: {},
        traceId: "trace-2",
      }), { status: 401, headers: { "Content-Type": "application/json" } }),
    );

    await expect(apiRequest("/me")).rejects.toMatchObject({ status: 401 });
    expect(localStorage.getItem(TOKEN_KEY)).toBeNull();
    expect(useAuthStore.getState().token).toBeNull();
  });
});
