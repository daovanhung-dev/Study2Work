# Work route modules

The current foundation is Express, not Nest/Fastify. `src/app.ts` mounts
`src/api/v1.ts` under `/api/v1`; browser pages are owned by the separate React
Work Web package. `src/routes/api_routes.ts` is a compatibility re-export.

Each wired domain has `models.ts`, `validate.ts`, `view.ts`, `query.ts` and a
route adapter. Models use Zod, validation is side-effect free, views own
permission/business rules and transaction boundaries, and query modules are the
only Prisma callers. `src/core/responses.ts`, `trace.ts`, `middleware.ts` and
`exceptions.ts` centralize the envelope, BigInt/Date serialization, trace ID,
async errors, parser and Multer failures.

Wired modules cover auth, students, businesses, jobs, CV and applications.
Legacy services remain available for compatibility but are not imported by the
new route graph. `auth.sevice.ts` is a legacy callback helper. `chat_services.ts`, `messagers_services.ts`,
`notification_*`, `topcv_services.ts`, and `topjd_services.ts` are empty and
unwired. Business creation/update/delete service methods exist, but only the
job routes are currently exposed. Student/business public selects and relation
selects exclude `matkhau`.
