# Work runtime and HTTP pipeline

`src/main.ts` loads typed environment config, creates injected dependencies,
connects Prisma before opening the Express listener at `127.0.0.1:3002`, and
disconnects on SIGINT/SIGTERM. A failed database connection terminates startup.

`src/app.ts` exposes `createApp(options)` for injected tests and configures trace
context, the JSON parser, public static assets, `/uploads` static assets,
optional JWT parsing, system health routes and the `/api/v1` JSON router. Async
errors are routed through `src/core/exceptions.ts`; there is no URL-encoded
parser, Nest bootstrap, Fastify pipeline, Passport middleware or Express session
middleware.

Authentication failures always receive a JSON `401` or `403`. Protected clients
send an `Authorization: Bearer <JWT>` header; browser navigation is handled by
the separate React Work Web router.
