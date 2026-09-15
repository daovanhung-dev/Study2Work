import { Component, OnInit, inject } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatIconModule } from "@angular/material/icon";
import { MatInputModule } from "@angular/material/input";
import { MatSelectModule } from "@angular/material/select";
import { RouterLink } from "@angular/router";

import { ApiService } from "../../core/api.service";
import { AdminStateService } from "../../core/admin-state.service";
import { AuthService } from "../../core/auth.service";
import { CatalogData, CatalogItem } from "../../core/models";

interface ObjectGroup {
  key: keyof CatalogData;
  label: string;
  icon: string;
  kind: string;
}

interface DdlPreview {
  sql: string;
  warnings: string[];
  confirmationToken: string;
  target: string;
  impact?: Array<{ schema_name?: string; name: string; kind?: string }>;
}

interface AdvancedKindOption {
  value: string;
  label: string;
}

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSelectModule, ReactiveFormsModule, RouterLink],
  template: `
    <section class="page-header"><div><p class="eyebrow">Database intelligence</p><h1>Schema explorer</h1><p class="lede">Inspect every object in the connected PostgreSQL database and make changes with a visible DDL preview.</p></div><button mat-flat-button color="primary" (click)="state.load()"><mat-icon>sync</mat-icon> Refresh catalog</button></section>
    @if (state.error()) { <div class="error-banner"><mat-icon>error_outline</mat-icon><span>{{ state.error() }}</span></div> }
    @if (pendingPreview) { <mat-card class="preview-card"><div class="preview-heading"><div><p class="eyebrow">Pending operation</p><h2>{{ pendingPreview.target }}</h2></div><button mat-icon-button aria-label="Close preview" (click)="pendingPreview = undefined"><mat-icon>close</mat-icon></button></div><pre>{{ pendingPreview.sql }}</pre><div class="warning-list">@for (warning of pendingPreview.warnings; track warning) { <span><mat-icon>warning</mat-icon>{{ warning }}</span> }</div>@if (pendingPreview.impact?.length) { <div class="impact-list"><strong>Dependencies / impact</strong>@for (item of pendingPreview.impact; track item.schema_name + item.name + item.kind) { <span><mat-icon>link</mat-icon>{{ item.schema_name }}.{{ item.name }} · {{ item.kind }}</span> }</div> }<div class="preview-actions"><button mat-button (click)="pendingPreview = undefined">Cancel</button><button mat-flat-button color="primary" (click)="applyPreview()">Confirm and apply</button></div></mat-card> }
    <div class="catalog-layout">
      <div class="catalog-main">
        @if (state.catalog(); as catalog) {
          @for (group of groups; track group.key) {
            <mat-card class="panel-card object-card"><div class="card-heading"><div class="object-title"><span class="object-icon"><mat-icon>{{ group.icon }}</mat-icon></span><div><h2>{{ group.label }}</h2><span>{{ catalog[group.key].length }} objects</span></div></div><span class="section-count">{{ catalog[group.key].length }}</span></div>
              @if (catalog[group.key].length) { <div class="object-list">@for (item of catalog[group.key]; track item.name + displaySchema(item)) { <div class="object-row"><div class="object-name"><mat-icon>chevron_right</mat-icon><span><strong>{{ item.name }}</strong><small>{{ displaySchema(item) }}{{ item.kind ? ' · ' + item.kind : '' }}</small></span></div><div class="object-actions">@if (group.key === 'tables') { <a mat-stroked-button [routerLink]="['/tables', displaySchema(item), item.name]"><mat-icon>table_view</mat-icon> Browse</a> } @if (auth.can('db_admin:write') && (group.key === 'schemas' || group.key === 'tables')) { <button mat-icon-button aria-label="Rename object" (click)="requestRename(group.kind, item)"><mat-icon>drive_file_rename_outline</mat-icon></button> } @if (auth.can('db_admin:write') && group.key !== 'grants') { <button mat-icon-button aria-label="Delete object" (click)="requestDelete(group.kind, item)"><mat-icon>delete_outline</mat-icon></button> }</div></div> }</div> } @else { <div class="empty-inline"><mat-icon>inbox</mat-icon><span>No {{ group.label.toLowerCase() }} found.</span></div> }
            </mat-card>
          }
        } @else if (!state.loading()) { <div class="empty-state"><mat-icon>cloud_off</mat-icon><h2>Catalog not loaded</h2><p>Connect the DB Admin API to inspect this Neon target.</p><button mat-flat-button color="primary" (click)="state.load()">Load catalog</button></div> }
      </div>
      <aside class="catalog-side">
        @if (auth.can('db_admin:write')) { <mat-card class="panel-card builder-card"><div class="card-heading"><div><p class="eyebrow">DDL builder</p><h2>Create schema</h2></div><mat-icon>add_box</mat-icon></div><p class="helper">Generate a quoted CREATE SCHEMA statement and preview it before commit.</p><mat-form-field appearance="outline"><mat-label>Schema name</mat-label><input matInput [formControl]="schemaForm.controls.name" placeholder="analytics" /><mat-error>Use a valid PostgreSQL identifier.</mat-error></mat-form-field><button mat-flat-button color="primary" [disabled]="schemaForm.invalid" (click)="createSchema()">Preview schema DDL</button></mat-card>
        <mat-card class="panel-card builder-card"><div class="card-heading"><div><p class="eyebrow">Table builder</p><h2>Create table</h2></div><mat-icon>table_chart</mat-icon></div><p class="helper">One column per line: <code>name | type | nullable</code>. Primary keys are comma-separated.</p><mat-form-field appearance="outline"><mat-label>Schema</mat-label><input matInput [formControl]="tableForm.controls.schema" /></mat-form-field><mat-form-field appearance="outline"><mat-label>Table name</mat-label><input matInput [formControl]="tableForm.controls.name" placeholder="events" /></mat-form-field><mat-form-field appearance="outline"><mat-label>Columns</mat-label><textarea matInput rows="6" [formControl]="tableForm.controls.columns" placeholder="id | bigint | no&#10;created_at | timestamptz | no&#10;payload | jsonb | yes"></textarea></mat-form-field><mat-form-field appearance="outline"><mat-label>Primary key</mat-label><input matInput [formControl]="tableForm.controls.primaryKey" placeholder="id" /></mat-form-field><button mat-flat-button color="primary" [disabled]="tableForm.invalid" (click)="createTable()">Preview table DDL</button></mat-card>
        <mat-card class="panel-card builder-card"><div class="card-heading"><div><p class="eyebrow">Advanced DDL</p><h2>Common object builder</h2></div><mat-icon>architecture</mat-icon></div><p class="helper">Use a complete PostgreSQL definition for views, routines, triggers, types, indexes, constraints and grants.</p><mat-form-field appearance="outline"><mat-label>Object kind</mat-label><mat-select [formControl]="advancedForm.controls.kind">@for (kind of advancedKinds; track kind.value) { <mat-option [value]="kind.value">{{ kind.label }}</mat-option> }</mat-select></mat-form-field><mat-form-field appearance="outline"><mat-label>Operation</mat-label><mat-select [formControl]="advancedForm.controls.operation"><mat-option value="create">Create</mat-option><mat-option value="alter">Alter</mat-option><mat-option value="drop">Drop</mat-option></mat-select></mat-form-field><mat-form-field appearance="outline"><mat-label>Schema</mat-label><input matInput [formControl]="advancedForm.controls.schema" /></mat-form-field><mat-form-field appearance="outline"><mat-label>Object name</mat-label><input matInput [formControl]="advancedForm.controls.name" placeholder="active_users" /></mat-form-field><mat-form-field appearance="outline"><mat-label>Parent table (trigger/constraint)</mat-label><input matInput [formControl]="advancedForm.controls.parent" placeholder="users" /></mat-form-field><mat-form-field appearance="outline"><mat-label>SQL definition</mat-label><textarea matInput rows="7" [formControl]="advancedForm.controls.definition" placeholder="CREATE VIEW public.active_users AS SELECT ...;"></textarea></mat-form-field><label class="checkbox-line"><input type="checkbox" [formControl]="advancedForm.controls.cascade" /> <span>Allow CASCADE for generated DROP</span></label><button mat-flat-button color="primary" [disabled]="advancedForm.invalid" (click)="previewAdvanced()">Preview advanced DDL</button></mat-card> }
        <mat-card class="panel-card scope-card"><div class="card-heading"><div><p class="eyebrow">Coverage</p><h2>Common objects</h2></div><mat-icon>layers</mat-icon></div><div class="scope-tags"><span>schemas</span><span>tables</span><span>views</span><span>routines</span><span>triggers</span><span>types</span><span>indexes</span><span>grants</span></div><a routerLink="/sql" class="text-link">Need something more advanced? Use SQL editor <mat-icon>arrow_forward</mat-icon></a></mat-card>
      </aside>
    </div>
  `,
})
export class CatalogPageComponent implements OnInit {
  readonly state = inject(AdminStateService);
  readonly auth = inject(AuthService);
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);
  pendingPreview?: DdlPreview & { payload: Record<string, unknown> };
  readonly schemaForm = this.fb.nonNullable.group({ name: ["", [Validators.required, Validators.pattern(/^[A-Za-z_][A-Za-z0-9_$]{0,62}$/)]] });
  readonly tableForm = this.fb.nonNullable.group({
    schema: ["public", [Validators.required]],
    name: ["", [Validators.required, Validators.pattern(/^[A-Za-z_][A-Za-z0-9_$]{0,62}$/)]],
    columns: ["", [Validators.required]],
    primaryKey: [""],
  });
  readonly advancedForm = this.fb.nonNullable.group({
    kind: ["view", [Validators.required]],
    operation: ["create", [Validators.required]],
    schema: ["public", [Validators.required]],
    name: ["", [Validators.required, Validators.pattern(/^[A-Za-z_][A-Za-z0-9_$]{0,62}$/)]],
    parent: [""],
    definition: [""],
    cascade: [false],
  });
  readonly advancedKinds: AdvancedKindOption[] = [
    { value: "view", label: "View" },
    { value: "materialized_view", label: "Materialized view" },
    { value: "function", label: "Function" },
    { value: "procedure", label: "Procedure" },
    { value: "trigger", label: "Trigger" },
    { value: "type", label: "Type / enum" },
    { value: "sequence", label: "Sequence" },
    { value: "index", label: "Index" },
    { value: "constraint", label: "Constraint" },
    { value: "grant", label: "Grant" },
  ];
  readonly groups: ObjectGroup[] = [
    { key: "schemas", label: "Schemas", icon: "account_tree", kind: "schema" },
    { key: "tables", label: "Tables", icon: "table_chart", kind: "table" },
    { key: "views", label: "Views & materialized views", icon: "visibility", kind: "view" },
    { key: "routines", label: "Functions & procedures", icon: "functions", kind: "function" },
    { key: "triggers", label: "Triggers", icon: "bolt", kind: "trigger" },
    { key: "types", label: "Types & enums", icon: "category", kind: "type" },
    { key: "sequences", label: "Sequences", icon: "format_list_numbered", kind: "sequence" },
    { key: "indexes", label: "Indexes", icon: "speed", kind: "index" },
    { key: "constraints", label: "Constraints", icon: "rule", kind: "constraint" },
    { key: "grants", label: "Grants", icon: "key", kind: "grant" },
  ];

  ngOnInit(): void { if (!this.state.catalog()) this.state.load(); }
  displaySchema(item: CatalogItem): string { return String(item.schema_name ?? item.schemaName ?? item.table_name ?? "public"); }

  createSchema(): void {
    this.preview({ kind: "schema", operation: "create", object_name: this.schemaForm.controls.name.value });
  }

  createTable(): void {
    const columns = this.tableForm.controls.columns.value.split("\n").map((line) => line.trim()).filter(Boolean).map((line) => {
      const [name, dataType, nullable = "yes"] = line.split("|").map((value) => value.trim());
      return { name, data_type: dataType, nullable: nullable.toLowerCase() !== "no" };
    });
    this.preview({
      kind: "table", operation: "create", schema_name: this.tableForm.controls.schema.value,
      object_name: this.tableForm.controls.name.value, columns,
      primary_key: this.tableForm.controls.primaryKey.value.split(",").map((value) => value.trim()).filter(Boolean),
    });
  }

  previewAdvanced(): void {
    const value = this.advancedForm.getRawValue();
    if (value.operation !== "drop" && !value.definition.trim()) {
      window.alert("SQL definition is required for create and alter operations.");
      return;
    }
    this.preview({
      kind: value.kind,
      operation: value.operation,
      schema_name: value.schema,
      object_name: value.name,
      parent_name: value.parent || undefined,
      definition_sql: value.definition || undefined,
      cascade: value.cascade,
    });
  }

  requestDelete(kind: string, item: CatalogItem): void {
    const objectKind = this.catalogObjectKind(item, kind);
    this.preview({ kind: objectKind, operation: "drop", schema_name: this.displaySchema(item), object_name: item.name, parent_name: item.table_name, arguments: item["arguments"], cascade: false });
  }

  requestRename(kind: string, item: CatalogItem): void {
    const newName = window.prompt(`Rename ${item.name} to:`)?.trim();
    if (!newName || newName === item.name) return;
    const objectKind = this.catalogObjectKind(item, kind);
    this.preview({ kind: objectKind, operation: "alter", schema_name: this.displaySchema(item), object_name: item.name, new_name: newName });
  }

  private catalogObjectKind(item: CatalogItem, fallback: string): string {
    const candidate = String(item.kind ?? "");
    const allowed = new Set(["schema", "table", "view", "materialized_view", "function", "procedure", "trigger", "type", "sequence", "index", "constraint", "grant"]);
    return allowed.has(candidate) ? candidate : fallback;
  }

  private preview(payload: Record<string, unknown>): void {
    this.api.previewDdl(payload).subscribe({ next: (preview) => { const value = preview as DdlPreview; this.pendingPreview = { ...value, payload: { ...payload, confirmation_token: value.confirmationToken } }; }, error: (error: Error) => window.alert(error.message) });
  }

  applyPreview(): void {
    const pending = this.pendingPreview;
    if (!pending) return;
    this.api.applyDdl(pending.payload).subscribe({ next: () => { this.pendingPreview = undefined; this.state.load(); }, error: (error: Error) => window.alert(error.message) });
  }
}
