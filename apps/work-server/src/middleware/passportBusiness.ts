// src/middleware/passportBusiness.ts
import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";
import prisma from "../config/prisma.config.js";

export default function configPassportBusiness() {
  passport.use(
    "business-local",
    new LocalStrategy(
      { usernameField: "email", passwordField: "matkhau" },
      async (email, matkhau, done) => {
        try {
          const business = await prisma.doanhNghiep.findFirst({
            where: { email, matkhau },
          });

          if (!business) return done(null, false, { message: "Sai thông tin" });

          return done(null, { id: Number(business.id), role: "business" });
        } catch (err) {
          return done(err);
        }
      }
    )
  );
}
