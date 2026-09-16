# Study2Work Web

This module is the server-rendered web application for Study2Work. It contains the Express server, EJS views, Prisma schema, Neon PostgreSQL integration, session authentication, and upload handling for student, business, and admin workflows.

## Features

- Student and business sign-in/sign-up flows.
- Role-based protected routes for students and businesses.
- Student job browsing, CV creation/update, applications, notifications, chat, interview schedule, and settings pages.
- Business job posting, job management, applicant list, CV detail, notifications, chat, and settings pages.
- Admin pages for users, jobs, majors, statistics, and settings.
- Prisma data models and migrations for Neon PostgreSQL persistence.

## Stack

- Node.js, TypeScript, Express
- EJS templates and static assets
- Passport.js and Express Session
- Prisma ORM and Neon PostgreSQL
- Multer for runtime uploads
- Supabase client configuration for existing integrations

## Structure

```text
.
+-- prisma/       # Prisma schema and migrations
+-- public/       # Static assets
+-- src/
|   +-- config/       # Prisma, Supabase, upload config
|   +-- controllers/  # Request handlers
|   +-- middleware/   # Auth and Passport setup
|   +-- routes/       # Express route definitions
|   +-- services/     # Data access and domain services
|   +-- views/        # EJS templates
+-- uploads/      # Runtime uploads, ignored except .gitkeep
```

## Setup

```bash
npm install
npm run prisma:generate
npm run prisma:migrate:deploy
npm run s2w
```

PowerShell:

```powershell
npm install
npm run prisma:generate
npm run prisma:migrate:deploy
npm run s2w
```

The server reads its runtime configuration from `src/utils/constants.ts` and
connects to Neon through the pooled URL. Prisma migration commands use the
direct Neon endpoint through the local CLI wrapper.

## Configuration

| Constant | Purpose |
| --- | --- |
| `PORT` | HTTP port for the Express server. |
| `DATABASE_URL` | Pooled Neon PostgreSQL connection string used by Prisma runtime. |
| `DIRECT_DATABASE_URL` | Direct Neon PostgreSQL connection string used by Prisma CLI. |
| `JWT_SECRET` | Secret for JWT helpers. |
| `JWT_EXPIRES` | JWT expiration value. |
| `SESSION_SECRET` | Express Session secret. |
| `SUPABASE_URL` | Supabase project URL. |
| `SUPABASE_ANON_KEY` | Supabase anonymous key. |

The project does not load `.env` files. Keep the credentials in
`src/utils/constants.ts` out of logs and rotate the Neon password if it has
been exposed.
