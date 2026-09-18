import { loadConfig } from "../core/config.js";

const config = loadConfig();

export const DATABASE_URL = config.databaseUrl;
export const DIRECT_DATABASE_URL = config.directDatabaseUrl;
export const PORT = config.port;
export const JWT_SECRET = config.jwtSecret;
export const JWT_EXPIRES = config.jwtExpires;
export const JWT_STORAGE_KEY = "access_token";

// Supabase is retained only for legacy, currently unwired modules.
export const SUPABASE_URL = config.supabaseUrl;
export const SUPABASE_ANON_KEY = config.supabaseAnonKey;
