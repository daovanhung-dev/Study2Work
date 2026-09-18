# Study Web API boundary

- `src/shared/api/http.ts` defines `studyApiBaseUrl` from
  `VITE_STUDY_API_URL`, falling back to `http://localhost:8000`.
- `src/shared/api/envelope.ts` defines the success/error envelope union and
  `isSuccessEnvelope` type guard.
- `src/shared/api/envelope.test.ts` verifies the type guard.
- No current caller wires the HTTP helper to a Study route.
- `contracts/openapi/study/README.md` is a placeholder, so request/response
  fields must not be inferred from Work Web or design-only DD.

Status: `CURRENT_BEHAVIOR=SOURCE_BACKED_SKELETON`,
`EXPECTED_BEHAVIOR=SOURCE_REQUIRED` for future Study API integration.
