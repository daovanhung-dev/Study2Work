// src/middleware/passport.ts
import passport from "passport";

export default function configPassport() {
  passport.serializeUser((user: any, done) => {
    done(null, user); 
  });

  passport.deserializeUser((user: any, done) => {
    done(null, user); 
  });
}
