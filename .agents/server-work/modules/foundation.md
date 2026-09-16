# Work route modules

The current foundation is Express, not Nest/Fastify. `src/app.ts` mounts only
`src/routes/api_routes.ts` under `/api/v1`; browser pages are owned by the
separate React Work Web package.

`api_routes.ts` owns the JSON adapter around the wired student, business, CV, JD,
and application services. It centralizes the response envelope, safe
BigInt/Date serialization, numeric path validation, multipart upload handling,
and owner/role checks.

Wired services are `StudentService`, `BusinessService` (login/read), `CVService`,
`JDService`, and `CandidateService`. `auth.sevice.ts` is a legacy callback helper
not imported by the router. `chat_services.ts`, `messagers_services.ts`,
`notification_*`, `topcv_services.ts`, and `topjd_services.ts` are empty and
unwired. Business creation/update/delete service methods exist, but only the
job routes are currently exposed.
