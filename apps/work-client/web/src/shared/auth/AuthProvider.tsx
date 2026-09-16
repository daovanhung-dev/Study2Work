import { createContext, useContext, useEffect, type ReactNode } from "react";

import { useAuthStore } from "./store";

const AuthContext = createContext(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const restore = useAuthStore((state) => state.restore);
  useEffect(() => restore(), [restore]);
  return <AuthContext.Provider value={null}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  useContext(AuthContext);
  return useAuthStore();
}
