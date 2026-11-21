# SPEC — Study login session (temporary implementation)

## Metadata

- Task: `2026-11-17-study-fe-auth-session`
- Scope owner: Study Web + Study Server
- User request: temporarily implement the approved production-cookie direction for Study login.
- Approval state: `PENDING_APPROVAL`
- Current source: SH-02 login, Study API #03, source-only refresh route R-X01, Study API #04, Student route group.
- Unrelated working-tree changes: preserve; do not edit or stage them.

## Scope

### In scope

- SH-02 login opens a Student session after API #03 succeeds and API #04 returns the current Student profile.
- Store access JWT only in an in-memory Angular auth/session service. Do not persist access or refresh tokens in `localStorage`, `sessionStorage`, IndexedDB, URL, logs, or analytics.
- Attach `Authorization: Bearer <access_token>` through shared HTTP infrastructure for Study API calls; components and feature services do not read or copy tokens.
- Restore a session when entering the protected `/student` route by calling R-X01 with the browser-managed refresh cookie.
- Treat one browser profile and Study origin as one active account across tabs. Broadcast successful login/account replacement and logout to sibling tabs without including tokens or profile data; sibling tabs clear in-memory auth and reload their current route to re-resolve the session from the shared cookie.
- On a protected request's first 401, perform at most one shared refresh operation, then retry that request at most once. Never recurse on login, refresh, or logout requests. If refresh fails, clear in-memory state and return to `/login`.
- Add a Student route guard. The backend remains authoritative for authentication and authorization.
- BE login and refresh set/rotate an opaque refresh token in an `HttpOnly` cookie. BE continues returning only the access token and public profile fields in the JSON envelope.
- Add a bodyless `POST /api/v1/auth/logout` route (source-only `R-X02`, with no numeric catalog API ID assigned in this task) that revokes the refresh token represented by the cookie and clears that cookie. FE clears in-memory state immediately on logout.
- Reconcile the SH-02 DD, API #03 auth DD, API catalog, and FE API registry with the approved implemented contract. Keep R-X01/R-X02 status and contract traceable; do not invent a numeric API ID.

### Out of scope

- Login/session routing for Mentor or Admin. The existing API #04 contract is Student-only; reject other roles from this Student session flow and do not navigate them into `/student`.
- Remember-me or persistence across browser restarts; no browser-readable refresh token.
- New database tables, columns, migrations, or live DB changes. Reuse current `refresh_tokens` persistence and rotation.
- Production deployment, live API/DB checks, CORS-origin deployment changes, or publishing.
- Changes to unrelated files already modified/untracked in the worktree.
- Tests/build execution or test-file changes unless the user separately asks for verification; this follows the active developer instruction.

## Approved design decisions

| Decision | Selected behavior | Basis |
|---|---|---|
| Browser token storage | Access token in FE memory only; opaque refresh token in server-set cookie with `HttpOnly`. | User approved the proposed direction on 2026-11-17. |
| Login success | Keep current source/AC-02 HTTP 200 semantics; update catalog/DD from the conflicting 201 `Resource Created` entry. | User approved the proposal to align login with its current successful authentication semantics. |
| Refresh transport | R-X01 becomes a bodyless POST using the cookie; rotate the refresh token atomically and return the new access token in JSON. | User approved cookie-managed refresh. |
| Cookie attributes | `HttpOnly`, `SameSite=Lax`, host-only (no `Domain`); `Path=/api/v1/auth`; `Secure` in HTTPS deployments and disabled only by explicit local-development configuration. | User approved the proposed cookie defaults; deployment configuration remains unverified. |
| Role | This session implementation completes the Student flow only. | API #04 is Student-only and SH-02 DD marks other role handoff blocked. |
| Logout | Revoke the current refresh token server-side and expire the cookie; clear FE memory immediately. | User approved adding BE logout support in the proposed scope. |
| Multiple tabs | One active account per browser profile/origin. A login or logout in one tab invalidates sibling-tab in-memory auth and causes those tabs to reload/re-resolve session state. | Required to prevent a tab's stale access token from being paired with another account's shared refresh cookie. |

## Expected behavior and current behavior

| Area | Expected after implementation | Current source |
|---|---|---|
| SH-02 login | On valid Student login, accept access token in memory, request API #04, then navigate to `/student`; failures remain on the login flow. | API #03 is called, but token/session is deliberately discarded and no navigation occurs. |
| Protected API calls | Shared interceptor adds Bearer token; feature code does not handle token values. | API #04 caller sends no Authorization header; no auth interceptor is configured. |
| Page reload / protected route | `/student` guard obtains a fresh access token through R-X01 cookie before allowing navigation. | No session guard/restore path is implemented. |
| Refresh | R-X01 receives the HttpOnly cookie, rotates it, and returns an access token. | R-X01 currently requires `{"refresh_token": "..."}` in JSON and returns both tokens in JSON. |
| Logout | R-X02 revokes current refresh token and expires the cookie; FE session is cleared. | No logout route/client flow was found in current source. |
| Contract | API #03 remains HTTP 200 and documents its access-token response/cookie; R-X01/R-X02 contracts are explicit source-only routes. | Catalog says API #03 is HTTP 201 `ApiEnvelope<UserProfile>`; DD is Draft and has open token/session/refresh/logout questions. |

## Requirements and acceptance criteria

### REQ-AUTH-01 — Login establishes only a Student session

- API #03 success sets the refresh cookie and returns the approved access-token/profile response.
- FE rejects non-Student roles from this flow, does not retain an access token for them, and does not navigate to `/student`.
- For Student, FE holds the access token in memory, calls API #04 with Bearer authorization, and navigates to `/student` only after a valid Student profile response.
- Login errors preserve current credential/validation messaging. No password or token is logged or persisted.

### REQ-AUTH-02 — Access token is owned by shared FE auth infrastructure

- One Angular auth/session service owns the in-memory access token and authenticated state.
- The HTTP interceptor attaches one Bearer header to Study API calls when a token exists; it does not overwrite caller-provided Authorization headers.
- Feature pages/services do not read Web Storage or construct Bearer headers themselves.
- No authenticated state is inferred from client-decoded JWT claims; the server validates token and role.

### REQ-AUTH-03 — Session restore and bounded refresh

- Entering `/student` without an in-memory token attempts R-X01 using browser credentials; a valid result restores memory state before route activation.
- A protected API request is retried no more than once after one successful refresh; concurrent 401 responses share one refresh request.
- Login/refresh/logout requests are excluded from interceptor refresh/retry to prevent loops.
- Failed refresh clears FE session and redirects to `/login`; 403 never triggers refresh.

### REQ-AUTH-04 — Refresh cookie contract

- API #03 and R-X01 set the opaque refresh token only in `Set-Cookie`; response JSON never includes `refresh_token` or its raw value.
- R-X01 has no request body, validates/rotates the cookie token using the existing token-hash table/transaction, and returns the new access token.
- Cookie attributes match the approved table above. Cookie expiry follows the configured refresh-token lifetime.
- Credentialed FE calls are limited to login/refresh/logout; server CORS continues to use explicit configured origins with credentials enabled.
- Login, R-X01, and R-X02 require an `Origin` header exactly matching one configured `CORS_ORIGINS` value; reject missing or unlisted origins before DB access. Do not use wildcard origins with credentials.

### REQ-AUTH-05 — Logout revokes and clears

- R-X02 reads the refresh cookie, revokes its matching active refresh-token row, and clears the cookie with the same Path/SameSite/Secure attributes.
- FE clears the access token immediately and calls R-X02; no tokens are included in request bodies, query strings, or logs.
- The route has no numeric API ID assigned in this change; its source-only marker and contract are recorded as R-X02 until the catalog owner assigns an API ID.

### REQ-AUTH-06 — Keep sibling tabs on the same account

- Publish a cross-tab session-change event after successful login/account replacement and successful logout. Use `BroadcastChannel` or a notification-only fallback; the message must not contain an access token, refresh token, credentials, or profile data.
- On receiving the event, sibling tabs clear their in-memory access token and user-specific in-memory state, then reload the current route. Protected Student routes must re-resolve identity via R-X01 and API #04; if no session remains, they return to `/login`.
- A new login replaces the active browser-profile session. Concurrent use of different accounts in tabs of the same profile is not supported. Separate browser profiles have separate cookie jars and can hold separate sessions.

### REQ-AUTH-07 — Contract and documentation traceability

- Update API #03 DD/catalog success status and response to the selected HTTP 200 access-token response.
- Document R-X01 request/response/cookie/error behavior and R-X02 logout behavior without conflating either route with API #03's login operation.
- Update SH-02 data flow/API integration to reflect the implemented Student-only flow and bounded refresh.
- Update FE registry metadata for R-X01/R-X02 and the current auth requirements; do not claim runtime/deployment verification.

## Security constraints and known limits

- HTTPS is required outside explicit local development; production refresh cookies must set `Secure`.
- `SameSite=Lax` is defense in depth, not a complete CSRF defense. The temporary implementation uses strict Origin allowlisting on all cookie-setting/using auth routes; the FE/API deployment must remain same-site for this cookie policy. A cross-site deployment needs a separately approved cookie/CSRF design.
- XSS can still perform actions as the user even when refresh-token contents are HttpOnly. Existing FE XSS prevention remains required.
- Runtime CORS origins, HTTPS termination, and deployment topology are not verified by this source review. Do not loosen CORS to `*` with credentials.
- API #04's current 401 does not distinguish every invalid/missing-user case from expiry; the refresh/retry limit prevents loops, but precise reason codes remain outside this temporary implementation unless required by source verification.

## Files expected to change after PLAN approval

- Study FE: shared auth/session service and interceptor/guard wiring; SH-02 login handoff; API request credential support; auth DTOs; API registry; focused auth documentation.
- Study BE: API #03 login/refresh response headers and request contract; R-X02 logout route/view/query as needed; cookie settings/config; API #03 DD and canonical API catalog contract.
- SH-02 screen DD: only flow, API integration, and test-case sections affected by the approved behavior.
- No unrelated screen, database schema, migration, or worktree changes.

## Approval

- Status: `PENDING_APPROVAL`
- Approver: pending
- Approved revision SHA256: pending
- Decision date: pending
