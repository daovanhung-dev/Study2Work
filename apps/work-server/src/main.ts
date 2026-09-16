// main.ts
import dotenv from "dotenv";
dotenv.config();

import app from "./app.js"; // vẫn giữ .js
import prisma  from "./config/prisma.config.js"; // nếu cần DB



const port = process.env.PORT!;
app.listen(port, () => {
  console.log(`Server chạy http://localhost:${port}`);
});
