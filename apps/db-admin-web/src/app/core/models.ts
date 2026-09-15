export type Permission = "db_admin:read" | "db_admin:write" | "db_admin:sql";

export interface ApiEnvelope<T> {
  success: boolean;
  businessCode: string;
  message: string;
  data: T;
  meta: Record<string, unknown>;
  traceId: string;
}

export interface ConnectionInfo {
  database: string;
  user: string;
  schema: string;
  serverVersion: string;
}

export interface CatalogItem {
  name: string;
  schema_name?: string;
  schemaName?: string;
  kind?: string;
  table_name?: string;
  definition?: string;
  [key: string]: unknown;
}

export interface CatalogData {
  schemas: CatalogItem[];
  tables: CatalogItem[];
  views: CatalogItem[];
  routines: CatalogItem[];
  triggers: CatalogItem[];
  types: CatalogItem[];
  sequences: CatalogItem[];
  indexes: CatalogItem[];
  constraints: CatalogItem[];
  grants: CatalogItem[];
}

export interface ColumnMetadata {
  name: string;
  position: number;
  data_type: string;
  udt_name: string;
  is_nullable: string;
  column_default: string | null;
  is_identity: string;
  identity_generation: string | null;
  is_generated: string;
  generation_expression: string | null;
}

export interface RowResult {
  columns: ColumnMetadata[];
  primaryKey: Array<{ name: string; position: number }>;
  rows: Array<Record<string, unknown>>;
  limit: number;
  offset: number;
}

export interface RowPreview {
  operation: "insert" | "update" | "delete";
  target: string;
  warnings: string[];
  confirmationToken: string;
}

export interface SqlValidation {
  classification: "read_only" | "mutation" | "blocked" | "unknown";
  statementCount: number;
  requiresConfirmation: boolean;
  warnings: string[];
  confirmationToken: string | null;
}

export interface SqlResult {
  classification: string;
  columns: string[];
  rows: Array<Record<string, unknown>>;
  rowCount: number;
  truncated: boolean;
}

export interface AuditEntry {
  timestamp: string;
  actor: string;
  action: string;
  target: string;
  outcome: string;
  traceId: string;
  sqlHash: string | null;
  details: Record<string, unknown>;
}

export interface AuditResult {
  entries: AuditEntry[];
}
