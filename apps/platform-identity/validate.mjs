import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const jwks = JSON.parse(readFileSync(resolve("jwks/dev-jwks.json"), "utf8"));

if (!Array.isArray(jwks.keys)) {
  throw new Error("JWKS must contain a keys array.");
}

console.log("Platform identity scaffold validated.");
