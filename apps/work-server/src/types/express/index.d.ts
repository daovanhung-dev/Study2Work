// src/types/index.d.ts
import "express";
import { Express } from "express";
import { sinhVien } from "@prisma/client";

declare module "express-serve-static-core" {
  interface Request {
    file?: Express.Multer.File;
    files?: Express.Multer.File[];

    user?: 
      | {
          id: number;
          role: "student" | "business" | string;
        }
      | sinhVien      
      | null;
  }
}
