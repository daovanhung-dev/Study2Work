import { QueryClientProvider, QueryErrorResetBoundary } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";

import { router } from "./app/router";
import { workQueryClient } from "./shared/api/query-client";
import { GlobalErrorBoundary } from "./shared/ui/GlobalErrorBoundary";
import { SessionBootstrap } from "./shared/session/SessionBootstrap";

export function App() {
  return (
    <QueryClientProvider client={workQueryClient}>
      <QueryErrorResetBoundary>
        {({ reset }) => (
          <GlobalErrorBoundary onReset={reset}>
            <SessionBootstrap>
              <RouterProvider router={router} />
            </SessionBootstrap>
          </GlobalErrorBoundary>
        )}
      </QueryErrorResetBoundary>
    </QueryClientProvider>
  );
}
