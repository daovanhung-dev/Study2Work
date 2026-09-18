import { createApp } from "./app.js";
import { loadConfig } from "./core/config.js";
import { createDependencies } from "./core/dependencies.js";

const config = loadConfig();
const dependencies = createDependencies(config);
const app = createApp({ config, dependencies });

async function bootstrap(): Promise<void> {
  await dependencies.prisma.$connect();
  const server = app.listen(config.port, () => {
    console.log(`Server chạy http://localhost:${config.port}`);
  });

  const shutdown = async () => {
    server.close(async () => {
      await dependencies.prisma.$disconnect();
      process.exit(0);
    });
  };

  process.once("SIGINT", shutdown);
  process.once("SIGTERM", shutdown);
}

bootstrap().catch(async () => {
  console.error("Không thể khởi động Work API hoặc kết nối Neon PostgreSQL.");
  await dependencies.prisma.$disconnect().catch(() => undefined);
  process.exit(1);
});
