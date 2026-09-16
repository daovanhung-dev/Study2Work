import { create } from "zustand";

import type { AuthResponse, User } from "../api/work";

export const TOKEN_KEY = "access_token";

interface AuthState {
  token: string | null;
  user: User | null;
  hydrated: boolean;
  setAuth: (auth: AuthResponse) => void;
  restore: () => void;
  clear: () => void;
}

function decodeUser(token: string): User | null {
  try {
    const encoded = token.split(".")[1];
    if (!encoded) return null;
    const json = atob(encoded.replace(/-/g, "+").replace(/_/g, "/"));
    const payload = JSON.parse(json) as Partial<User>;
    if (typeof payload.id !== "number" || typeof payload.email !== "string" || typeof payload.role !== "string") return null;
    return { id: payload.id, email: payload.email, role: payload.role };
  } catch {
    return null;
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  hydrated: false,
  setAuth: (auth) => {
    localStorage.setItem(TOKEN_KEY, auth.token);
    set({ token: auth.token, user: auth.user, hydrated: true });
  },
  restore: () => {
    const token = localStorage.getItem(TOKEN_KEY);
    set({ token, user: token ? decodeUser(token) : null, hydrated: true });
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    set({ token: null, user: null, hydrated: true });
  },
}));

export function getAccessToken(): string | null {
  return useAuthStore.getState().token || localStorage.getItem(TOKEN_KEY);
}

export function clearAuthToken(): void {
  useAuthStore.getState().clear();
}
