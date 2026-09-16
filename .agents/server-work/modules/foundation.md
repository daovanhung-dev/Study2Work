# Work route modules

The current foundation is Express, not Nest/Fastify. `src/app.ts` mounts only
`src/routes/api_routes.ts` under `/api/v1`; browser pages are owned by the
separate React Work Web package.

`api_routes.ts` owns the JSON adapter around the existing student, business, CV,
JD, and application services. It centralizes the response envelope, safe
BigInt/Date serialization, numeric path validation, and owner/role checks. Chat,
notification, interview, and Admin remain unwired because no current service
provides those API operations.
