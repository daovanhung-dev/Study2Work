# Learn2Earn Web

This module is the server-rendered web application for Learn2Earn. It contains the Express server, EJS views, Prisma schema, MySQL integration, session authentication, and upload handling for student, business, and admin workflows.

## Features

- Student and business sign-in/sign-up flows.
- Role-based protected routes for students and businesses.
- Student job browsing, CV creation/update, applications, notifications, chat, interview schedule, and settings pages.
- Business job posting, job management, applicant list, CV detail, notifications, chat, and settings pages.
- Admin pages for users, jobs, majors, statistics, and settings.
- Prisma data models and migrations for MySQL persistence.

## Stack

- Node.js, TypeScript, Express
- EJS templates and static assets
- Passport.js and Express Session
- Prisma ORM and MySQL
- Multer for runtime uploads
- Supabase client configuration for existing integrations

## Structure

```text
.
+-- prisma/       # Prisma schema and migrations
+-- public/       # Static assets
+-- src/
|   +-- config/       # Database, Prisma, Supabase, upload config
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
cp .env.example .env
npm exec prisma generate
npm exec prisma migrate dev
npm run l2e
```

PowerShell:

```powershell
npm install
Copy-Item .env.example .env
npm exec prisma generate
npm exec prisma migrate dev
npm run l2e
```

The server reads `PORT` from `.env`.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `PORT` | HTTP port for the Express server. |
| `DATABASE_URL` | MySQL connection string used by Prisma and the MySQL client. |
| `JWT_SECRET` | Secret for JWT helpers. |
| `JWT_EXPIRES` | JWT expiration value. |
| `SESSION_SECRET` | Express Session secret. Falls back to `JWT_SECRET` if not set. |
| `SUPABASE_URL` | Supabase project URL. |
| `SUPABASE_ANON_KEY` | Supabase anonymous key. |

Do not commit `.env` or runtime upload files.
