FROM node:22-alpine AS base

WORKDIR /workspace
RUN corepack enable

COPY package.json pnpm-workspace.yaml ./
COPY apps/work-api/package.json apps/work-api/package.json
RUN pnpm install --filter work-api --prod=false

COPY apps/work-api apps/work-api
WORKDIR /workspace/apps/work-api
RUN pnpm build

EXPOSE 8001
CMD ["pnpm", "start"]
