# Work runtime and HTTP pipeline

`src/main.ts` connects the shared Prisma client before opening the Express
listener. A failed database connection terminates startup.

`src/app.ts` configures JSON/urlencoded parsers, static assets, optional JWT
parsing and the web/student/business routers. There is no Nest bootstrap,
Fastify pipeline, Passport middleware or Express session middleware.

Authentication failures are content-aware: HTML navigation is redirected to a
public sign-in page, while API-style requests receive a JSON `401` or `403`.
Protected clients send an `Authorization: Bearer <JWT>` header.
