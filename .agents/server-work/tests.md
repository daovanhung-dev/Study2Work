# Work server tests

There is no checked-in test runner for the current Express application. Use
the following verified checks for changes:

```bash
./node_modules/.bin/tsc --noEmit
npm run prisma:validate
npm run prisma:generate
node --check public/js/jwt-client.js
npm run s2w
```

JWT auth checks must cover successful student/business login, JSON `401` for
missing or invalid Bearer tokens, JSON `403` for a wrong role, rejection of
expired tokens, protected HTML redirect behavior, logout without
`Set-Cookie`, and absence of server-side session state.

Login smoke tests may create a uniquely named temporary Neon row, verify the
response contains a token and the correct role, and delete the row in a
`finally` block. Never print tokens, passwords or connection strings.
