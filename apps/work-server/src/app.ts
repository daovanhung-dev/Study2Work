import express, { type NextFunction, type Request, type Response } from "express";
import { randomUUID } from "node:crypto";
import { MulterError } from "multer";
import path from "path";
import { fileURLToPath } from "url";

import api_router from "./routes/api_routes.js";

import { authenticateToken } from "./middleware/auth.middleware.js";

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));
app.use("/uploads", express.static(path.join(process.cwd(), "uploads")));
app.use(authenticateToken);

// The server is API-only. React owns all browser pages and is deployed separately.
app.use("/api/v1", api_router);

app.use((req: Request, res: Response) => {
  const traceId = req.get("X-Trace-Id") || randomUUID();
  res.setHeader("X-Trace-Id", traceId);
  res.status(404).json({
    success: false,
    businessCode: "NOT_FOUND",
    message: "Không tìm thấy tài nguyên.",
    data: null,
    meta: {},
    traceId,
  });
});

app.use((error: unknown, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) {
    next(error);
    return;
  }

  const traceId = req.get("X-Trace-Id") || randomUUID();
  const isMulterError = error instanceof MulterError;
  const isUploadFilterError = error instanceof Error && error.message === "Chỉ cho phép file ảnh (jpeg, jpg, png, gif)";
  const isJsonBodyError = error instanceof SyntaxError && "body" in error;
  const status = isMulterError && error.code === "LIMIT_FILE_SIZE" ? 413 : (isMulterError || isUploadFilterError || isJsonBodyError ? 400 : 500);
  const businessCode = status === 413 ? "PAYLOAD_TOO_LARGE" : status === 400 ? "INVALID_REQUEST" : "INTERNAL_SERVER_ERROR";
  const message = status === 413
    ? "File tải lên vượt quá kích thước cho phép."
    : status === 400
      ? "Request không hợp lệ."
      : "Lỗi máy chủ.";
  res.setHeader("X-Trace-Id", traceId);
  res.status(status).json({
    success: false,
    businessCode,
    message,
    data: null,
    meta: {},
    traceId,
  });
});

export default app;
