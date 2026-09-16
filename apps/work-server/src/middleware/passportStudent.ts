// src/middleware/passportStudent.ts
import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";
import prisma from "../config/prisma.config.js";

export default function configPassportStudent() {
  passport.use(
    "student-local",
    new LocalStrategy(
      { usernameField: "email", passwordField: "matkhau" },
      async (email, matkhau, done) => {
        try {
          const student = await prisma.sinhVien.findFirst({
            where: { email, matkhau },
          });

          if (!student) return done(null, false, { message: "Sai thông tin" });

          // Only return id + role
          return done(null, { id: Number(student.id), role: "student" });
        } catch (err) {
          return done(err);
        }
      }
    )
  );
}
