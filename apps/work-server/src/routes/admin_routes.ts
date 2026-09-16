import { Router } from "express";
import * as adminController from "../controllers/admin_ctrl.js";

const admin_router = Router();

admin_router.get("/home", adminController.admin_home);
admin_router.get("/users", adminController.admin_users);
admin_router.get("/jobs", adminController.admin_jobs);
admin_router.get("/majors", adminController.admin_majors);
admin_router.get("/stats", adminController.admin_stats);
admin_router.get("/settings", adminController.admin_settings);

export default admin_router;
