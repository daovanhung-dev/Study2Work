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

function assertWorkOpenApiBaseline() {
  const specification = readJson("contracts/openapi/work/openapi.json");

  if (specification.openapi !== "3.1.0") {
    throw new Error("Work OpenAPI must use OpenAPI 3.1.0.");
  }

  const expectedBaselineOperations = {
    "/api/v1": {
      businessCode: "SYSTEM_ROOT_LOADED",
      schema: "#/components/schemas/RootEnvelope",
    },
    "/health/live": {
      businessCode: "SYSTEM_HEALTH_LIVE",
      schema: "#/components/schemas/LiveHealthEnvelope",
    },
    "/health/ready": {
      businessCode: "SYSTEM_HEALTH_READY",
      schema: "#/components/schemas/ReadyHealthEnvelope",
    },
  };

  for (const [path, expected] of Object.entries(expectedBaselineOperations)) {
    const operation = specification.paths?.[path]?.get;
    const response = operation?.responses?.["200"];
    const schema = response?.content?.["application/json"]?.schema;
    const traceHeader = response?.headers?.["X-Trace-Id"]?.$ref;
    const traceParameter = operation?.parameters?.find(
      (parameter) => parameter?.$ref === "#/components/parameters/IncomingTraceId",
    );
    const envelope = specification.components?.schemas?.[
      expected.schema.split("/").at(-1)
    ];
    const envelopeProperties = envelope?.allOf?.[1]?.properties;

    if (schema?.$ref !== expected.schema) {
      throw new Error(`Work OpenAPI ${path} must return ${expected.schema}.`);
    }
    if (traceHeader !== "#/components/headers/TraceId") {
      throw new Error(`Work OpenAPI ${path} must return the X-Trace-Id header.`);
    }
    if (!traceParameter) {
      throw new Error(`Work OpenAPI ${path} must accept the X-Trace-Id header.`);
    }
    if (envelopeProperties?.businessCode?.const !== expected.businessCode) {
      throw new Error(`Work OpenAPI ${path} must use ${expected.businessCode}.`);
    }
  }

  const unavailableResponse = specification.paths?.["/health/ready"]?.get?.responses?.["503"];
  const unavailableSchema = unavailableResponse?.content?.["application/json"]?.schema?.$ref;
  const unavailableTraceHeader = unavailableResponse?.headers?.["X-Trace-Id"]?.$ref;
  const unavailableEnvelope = specification.components?.schemas?.ReadyUnavailableEnvelope;
  const unavailableProperties = unavailableEnvelope?.allOf?.[1]?.properties;

  if (unavailableSchema !== "#/components/schemas/ReadyUnavailableEnvelope") {
    throw new Error("Work OpenAPI /health/ready must document its 503 readiness response.");
  }
  if (unavailableTraceHeader !== "#/components/headers/TraceId") {
    throw new Error("Work OpenAPI /health/ready 503 must return the X-Trace-Id header.");
  }
  if (unavailableProperties?.businessCode?.const !== "DEPENDENCY_UNAVAILABLE") {
    throw new Error("Work OpenAPI /health/ready 503 must use DEPENDENCY_UNAVAILABLE.");
  }

  const errorEnvelope = specification.components?.schemas?.ApiErrorEnvelope;
  const errorRequired = errorEnvelope?.required ?? [];
  const errorProperties = errorEnvelope?.properties;
  const fieldErrors = specification.components?.schemas?.ApiMeta?.properties?.fieldErrors;

  if (errorProperties?.data?.type !== "null" || !errorRequired.includes("meta")) {
    throw new Error("Work OpenAPI errors must return data:null and a meta object.");
  }
  if (fieldErrors?.items?.$ref !== "#/components/schemas/ApiErrorDetail") {
    throw new Error("Work OpenAPI errors must expose safe details through meta.fieldErrors.");
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

assertWorkOpenApiBaseline();

console.log("Contract validation passed.");
