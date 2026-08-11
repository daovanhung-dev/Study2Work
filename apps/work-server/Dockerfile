FROM node:22-alpine AS build

WORKDIR /app
RUN corepack enable

# Prisma validates the datasource while generating the client. Runtime values
# are supplied by Compose/deployment and are not baked into the final image.
ENV WORK_DATABASE_URL=postgresql://study2work:study2work@localhost:5432/study2work_work

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml tsconfig.base.json ./
COPY apps/work-server/package.json apps/work-server/package.json
RUN corepack pnpm install --frozen-lockfile --filter work-api...

COPY apps/work-server apps/work-server
RUN corepack pnpm --filter work-api prisma:generate \
  && corepack pnpm --filter work-api build

FROM node:22-alpine AS runtime

WORKDIR /app
ENV NODE_ENV=production
ENV WORK_HOST=0.0.0.0
ENV WORK_PORT=8001

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/apps/work-server/package.json ./apps/work-server/package.json
COPY --from=build /app/apps/work-server/node_modules ./apps/work-server/node_modules
COPY --from=build /app/apps/work-server/dist ./apps/work-server/dist
COPY --from=build /app/apps/work-server/prisma ./apps/work-server/prisma

EXPOSE 8001
CMD ["node", "apps/work-server/dist/main.js"]
