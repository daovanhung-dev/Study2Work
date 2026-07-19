import { Request, Response, NextFunction } from "express";

// Kiểm tra user đã login chưa
export function ensureAuthenticated(req: any, res: Response, next: NextFunction) {
  if (req.isAuthenticated()) return next(); // đã login → cho qua
  res.redirect("/signInRole"); // chưa login → quay về login
}

// Kiểm tra role
export function checkRole(role: string) {
  return (req: any, res: Response, next: NextFunction) => {
    if (req.isAuthenticated() && req.user.role === role) {
      return next(); // đúng role → cho qua
    }
    res.status(403).redirect("/errorRole");
  };
}
