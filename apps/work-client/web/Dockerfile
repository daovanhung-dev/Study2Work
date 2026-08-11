FROM node:22-alpine AS build

WORKDIR /workspace

RUN corepack enable

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/work-client/web/package.json apps/work-client/web/package.json

RUN corepack pnpm install --frozen-lockfile --filter work-web

COPY apps/work-client/web apps/work-client/web

ARG VITE_WORK_API_URL=http://localhost:8001/api/v1
ARG VITE_IDENTITY_API_URL=
ARG VITE_IDENTITY_LOGIN_URL=https://identity.study2work.vn/login
ENV VITE_WORK_API_URL=${VITE_WORK_API_URL}
ENV VITE_IDENTITY_API_URL=${VITE_IDENTITY_API_URL}
ENV VITE_IDENTITY_LOGIN_URL=${VITE_IDENTITY_LOGIN_URL}

RUN corepack pnpm --filter work-web build

FROM nginx:1.27-alpine AS runtime

COPY apps/work-client/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /workspace/apps/work-client/web/dist /usr/share/nginx/html

EXPOSE 80
