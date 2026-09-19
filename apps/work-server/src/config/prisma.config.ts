import { loadConfig } from "../core/config.js";
import { createPrismaClient } from "../core/database.js";

const prisma = createPrismaClient(loadConfig());

export default prisma;
