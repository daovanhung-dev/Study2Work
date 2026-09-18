import multer from "multer";
import path from "path";
import fs from "fs";

// Thư mục lưu file
const uploadDir = path.join(process.cwd(), "uploads");
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    const filename = `${Date.now()}-${Math.round(Math.random() * 1e9)}${ext}`;
    cb(null, filename);
  },
});

export const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowed = new Set([".jpeg", ".jpg", ".png", ".gif"]);
    const ext = path.extname(file.originalname).toLowerCase();
    const mimeAllowed = new Set(["image/jpeg", "image/png", "image/gif"]);
    if (allowed.has(ext) && mimeAllowed.has(file.mimetype)) cb(null, true);
    else cb(new Error("Chỉ cho phép file ảnh (jpeg, jpg, png, gif)"));
  },
});
