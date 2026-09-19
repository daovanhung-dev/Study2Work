# Study Web tests and verification

The package provides `vitest run`, `vue-tsc --noEmit` and `vite build` scripts.
The checked-in unit test covers the envelope guard. There is no verified
request integration test because the HTTP helper has no current caller.

Required verification for a Study Web change:

1. Run the focused Vitest test.
2. Run `vue-tsc --noEmit` and the package build when the toolchain is available.
3. Record unavailable Node/package-manager tooling as
   `DECLARED_NOT_RUNNABLE`, not as a pass.
4. Update the Study Web worklog and this page when route/API wiring changes.
