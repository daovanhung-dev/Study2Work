import { useEffect, type ReactNode } from "react";

import { clearPrivateWorkQueries } from "../api/query-client";
import { restoreWorkSession } from "./session-client";
import { useSessionStore } from "./store";

export function SessionBootstrap({ children }: { children: ReactNode }) {
  const setAnonymous = useSessionStore((state) => state.setAnonymous);
  const setSession = useSessionStore((state) => state.setSession);
  const subjectId = useSessionStore((state) => state.session?.identity.subjectId);

  useEffect(() => {
    let active = true;

    void restoreWorkSession().then((session) => {
      if (!active) {
        return;
      }

      if (session) {
        setSession(session);
      } else {
        setAnonymous();
      }
    });

    return () => {
      active = false;
    };
  }, [setAnonymous, setSession]);

  useEffect(() => {
    clearPrivateWorkQueries();
  }, [subjectId]);

  return <>{children}</>;
}
