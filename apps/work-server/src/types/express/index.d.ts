// src/types/index.d.ts
import "express";
import { Express } from "express";

declare module "express-serve-static-core" {
  interface Request {
    file?: Express.Multer.File;
    files?: Express.Multer.File[];

    user?: {
      id: number;
      email: string;
      role: "student" | "business" | string;
    } | null;
    authenticated?: boolean;
  }
}
