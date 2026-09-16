import app from "./app.js"; // vẫn giữ .js
import prisma from "./config/prisma.config.js";
import { PORT } from "./utils/constants.js";

const bootstrap = async () => {
  await prisma.$connect();
  app.listen(PORT, () => {
    console.log(`Server chạy http://localhost:${PORT}`);
  });
};

bootstrap().catch((error) => {
  console.error("Không thể kết nối Neon PostgreSQL:", error);
  process.exit(1);
});
