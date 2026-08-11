import { create } from "zustand";

import type { AuthSession, SessionStatus } from "./types";

interface SessionStore {
  lastCheckedAt?: string;
  session: AuthSession | null;
  status: SessionStatus;
  setAnonymous: () => void;
  setChecking: () => void;
  setSession: (session: AuthSession) => void;
}

export const useSessionStore = create<SessionStore>((set) => ({
  lastCheckedAt: undefined,
  session: null,
  status: "checking",
  setAnonymous: () =>
    set({
      lastCheckedAt: new Date().toISOString(),
      session: null,
      status: "anonymous",
    }),
  setChecking: () => set({ status: "checking" }),
  setSession: (session) =>
    set({
      lastCheckedAt: new Date().toISOString(),
      session,
      status: "authenticated",
    }),
}));

export function getAccessToken(): string | undefined {
  return useSessionStore.getState().session?.accessToken;
}

export function clearSession(): void {
  useSessionStore.getState().setAnonymous();
}
