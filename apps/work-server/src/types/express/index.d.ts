// Express request fields used by the JWT middleware.
// Multer owns `file`/`files`; redeclaring those fields here creates a
// different Express Request shape and breaks middleware overloads.
export {};

declare global {
  namespace Express {
    interface Request {
      user?: {
        id: number;
        email: string;
        role: "student" | "business" | string;
      } | null;
      authenticated?: boolean;
    }
  }
}
