import Ajv2020 from "ajv/dist/2020.js";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import process from "node:process";

const root = process.cwd();
const ajv = new Ajv2020({ allErrors: true, strict: false });

function readJson(path) {
  return JSON.parse(readFileSync(resolve(root, path), "utf8"));
}

function assertSchema(schemaPath, validPath, invalidPath) {
  const schema = readJson(schemaPath);
  const validate = ajv.compile(schema);
  const validPayload = readJson(validPath);
  if (!validate(validPayload)) {
    throw new Error(`${validPath} should be valid: ${ajv.errorsText(validate.errors)}`);
  }

  if (invalidPath) {
    const invalidPayload = readJson(invalidPath);
    if (validate(invalidPayload)) {
      throw new Error(`${invalidPath} should be invalid.`);
    }
  }
}

assertSchema(
  "contracts/events/study-work/study.evidence.upserted.v1.schema.json",
  "contracts/events/study-work/examples/study.evidence.upserted.valid.json",
  "contracts/events/study-work/examples/study.evidence.upserted.invalid.json",
);

assertSchema(
  "contracts/events/study-work/study.evidence.revoked.v1.schema.json",
  "contracts/events/study-work/examples/study.evidence.revoked.valid.json",
  "contracts/events/study-work/examples/study.evidence.revoked.invalid.json",
);

assertSchema(
  "contracts/skill-taxonomy/skill-taxonomy.v1.schema.json",
  "contracts/skill-taxonomy/skill-taxonomy.v1.json",
);

console.log("Contract validation passed.");
