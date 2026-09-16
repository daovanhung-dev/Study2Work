export type Permission = "db_admin:read" | "db_admin:write" | "db_admin:sql" | "db_admin:manage";

export interface DatabaseTarget {
  id: string;
  label: string;
}

export interface DatabaseTargetResult {
  databases: DatabaseTarget[];
}

export interface ApiErrorInfo {
  message: string;
  businessCode?: string;
  traceId?: string;
}

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
  grantee?: string;
  privilege_type?: string;
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
  database?: string;
  schemaName?: string;
  classification: "read_only" | "mutation" | "blocked" | "unknown";
  statementCount: number;
  requiresConfirmation: boolean;
  warnings: string[];
  confirmationToken: string | null;
}

export interface SqlRequest {
  database: string;
  schema_name: string;
  sql: string;
}

export interface SqlResult {
  classification: string;
  columns: string[];
  rows: Array<Record<string, unknown>>;
  rowCount: number;
  truncated: boolean;
}

export interface QueryHistoryItem {
  id: string;
  sql: string;
  database: string;
  schemaName: string;
  executedAt: string;
  status: "success" | "error";
  rowCount?: number;
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

export interface SchemaBinding {
  database: string;
  schema: string;
  postgresRole?: string;
  accessLevel?: string;
  active?: boolean;
}

export interface AdminUserProfile {
  id: string;
  username?: string | null;
  displayName?: string;
  isRoot: boolean;
  status?: string;
}

export interface AdminAuthSession {
  accessToken: string;
  user: AdminUserProfile;
  permissions: string[];
  roles: string[];
  targets: string[];
  schemaBindings: SchemaBinding[];
  mustChangePassword: boolean;
  traceId?: string;
}

export interface AccessAccount extends AdminUserProfile {
  status: "active" | "disabled";
  mustChangePassword: boolean;
  failedLoginAttempts?: number;
  lockedUntil?: string | null;
  lastLoginAt?: string | null;
  createdAt?: string | null;
  bindings: SchemaBinding[];
  secret?: string;
}

export interface AccessAccountsResult {
  accounts: AccessAccount[];
}

export interface AccessAuditResult {
  entries: AuditEntry[];
}
