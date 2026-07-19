// main.ts
import app from "./app.js";
import { env } from "./config/env.js";
import prisma from "./config/prisma.config.js";

async function bootstrap() {
  try {
    await prisma.$connect();

    app.listen(env.port, () => {
      console.log(`Server chạy http://localhost:${env.port}`);
    });
  } catch (error) {
    console.error("Failed to start work-server. Check DATABASE_URL and make sure MySQL is running.");
    console.error(error);
    await prisma.$disconnect().catch(() => undefined);
    process.exit(1);
  }
}

void bootstrap();
