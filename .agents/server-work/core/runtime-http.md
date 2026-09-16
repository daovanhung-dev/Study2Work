# Work runtime and HTTP pipeline

`src/main.ts` connects the shared Prisma client before opening the Express
listener. A failed database connection terminates startup.

`src/app.ts` configures the JSON parser, public static assets, `/uploads` static
assets, optional JWT parsing and the single `/api/v1` JSON router. It also owns
JSON 404/500 envelope handlers. There is no URL-encoded parser, Nest bootstrap,
Fastify pipeline, Passport middleware or Express session middleware.

Authentication failures always receive a JSON `401` or `403`. Protected clients
send an `Authorization: Bearer <JWT>` header; browser navigation is handled by
the separate React Work Web router.
