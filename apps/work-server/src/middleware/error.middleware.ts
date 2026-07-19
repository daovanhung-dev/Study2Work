import type { ErrorRequestHandler } from "express";

export const errorHandler: ErrorRequestHandler = (error, req, res, next) => {
  console.error("Unhandled request error:", error);

  if (res.headersSent) {
    return next(error);
  }

  if (req.accepts("html")) {
    return res.status(500).send("Internal server error");
  }

  return res.status(500).json({ error: "Internal server error" });
};
