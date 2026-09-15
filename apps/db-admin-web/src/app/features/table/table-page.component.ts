import { Component, OnDestroy, OnInit, inject, signal } from "@angular/core";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatInputModule } from "@angular/material/input";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatSelectModule } from "@angular/material/select";
import { Subscription } from "rxjs";

import { ApiService } from "../../core/api.service";
import { AuthService } from "../../core/auth.service";
import { RowResult } from "../../core/models";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, MatInputModule, MatProgressSpinnerModule, MatSelectModule, RouterLink],
  template: `
    <section class="page-header compact"><div><a routerLink="/catalog" class="back-link"><mat-icon>arrow_back</mat-icon> Schema explorer</a><p class="eyebrow">Table data</p><h1>{{ schema }}<span class="title-separator">.</span>{{ table }}</h1><p class="lede">Browse and edit rows using primary-key-safe mutations.</p></div><button mat-flat-button color="primary" (click)="load()"><mat-icon>refresh</mat-icon> Refresh rows</button></section>
    @if (error()) { <div class="error-banner"><mat-icon>error_outline</mat-icon><span>{{ error() }}</span></div> }
    <mat-card class="panel-card table-panel"><div class="table-toolbar"><div><p class="eyebrow">Rows</p><h2>{{ rows()?.rows?.length ?? 0 }} loaded</h2></div><div class="table-tools"><span class="key-badge"><mat-icon>key</mat-icon>{{ primaryKeyLabel() }}</span>@if (auth.can('db_admin:write') && (rows()?.primaryKey?.length ?? 0) > 0) { <button mat-stroked-button (click)="startInsert()"><mat-icon>add</mat-icon> New row</button> }</div></div>
      @if (rows(); as result) { <div class="table-query-tools"><mat-form-field appearance="outline" class="compact-field"><mat-label>Filter column</mat-label><mat-select [value]="filterColumn()" (selectionChange)="filterColumn.set($event.value)">@for (column of result.columns; track column.name) { <mat-option [value]="column.name">{{ column.name }}</mat-option> }</mat-select></mat-form-field><mat-form-field appearance="outline" class="compact-field filter-value"><mat-label>Contains</mat-label><input matInput [value]="filterValue()" (input)="filterValue.set($any($event.target).value)" (keyup.enter)="applyQuery()" /></mat-form-field><button mat-stroked-button (click)="applyQuery()" [disabled]="!filterColumn() || !filterValue().trim()"><mat-icon>filter_alt</mat-icon> Filter</button><button mat-button (click)="clearQuery()" [disabled]="!filterValue() && !sortColumn()">Clear</button></div> }
      @if (loading()) { <div class="loading-state"><mat-spinner diameter="28"></mat-spinner><span>Loading rows…</span></div> } @else if (rows(); as result) { <div class="data-table-wrap"><table><thead><tr>@for (column of result.columns; track column.name) { <th><button mat-button class="sort-button" (click)="sortBy(column.name)">{{ column.name }}<mat-icon>{{ sortColumn() === column.name ? (sortDirection() === 'asc' ? 'arrow_upward' : 'arrow_downward') : 'unfold_more' }}</mat-icon></button><small>{{ column.data_type }}</small></th> }<th class="actions-col">Actions</th></tr></thead><tbody>@for (row of result.rows; track rowKey(row)) { <tr>@for (column of result.columns; track column.name) { <td>{{ formatValue(row[column.name]) }}</td> }<td class="row-actions">@if (auth.can('db_admin:write')) { <button mat-icon-button aria-label="Edit row" (click)="startEdit(row)" [disabled]="!result.primaryKey.length"><mat-icon>edit</mat-icon></button><button mat-icon-button aria-label="Delete row" (click)="remove(row)" [disabled]="!result.primaryKey.length"><mat-icon>delete_outline</mat-icon></button> }</td></tr> } @empty { <tr><td [attr.colspan]="result.columns.length + 1" class="empty-table">No rows matched this query.</td></tr> }</tbody></table></div><div class="table-footer"><span>Offset {{ result.offset }} · Limit {{ result.limit }}</span><div><button mat-button [disabled]="result.offset === 0" (click)="previous()">Previous</button><button mat-button [disabled]="result.rows.length < result.limit" (click)="next()">Next</button></div></div> } @else { <div class="empty-state small"><mat-icon>table_view</mat-icon><h2>Table unavailable</h2><p>Check the table name and API connection.</p></div> }
    </mat-card>
    @if (editorMode()) { <mat-card class="panel-card row-editor"><div class="card-heading"><div><p class="eyebrow">{{ editorMode() === 'insert' ? 'Create row' : 'Edit row' }}</p><h2>JSON values</h2></div><button mat-icon-button aria-label="Close editor" (click)="editorMode.set(null)"><mat-icon>close</mat-icon></button></div><p class="helper">Use valid JSON. Primary-key values identify the row and cannot be changed from this editor.</p><textarea class="json-editor" [value]="editorJson()" (input)="editorJson.set($any($event.target).value)"></textarea><div class="preview-actions"><button mat-button (click)="editorMode.set(null)">Cancel</button><button mat-flat-button color="primary" (click)="saveRow()">Save row</button></div></mat-card> }
  `,
})
export class TablePageComponent implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ApiService);
  readonly auth = inject(AuthService);
  private readonly subscription = new Subscription();
  readonly rows = signal<RowResult | null>(null);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly editorMode = signal<"insert" | "edit" | null>(null);
  readonly editorJson = signal("{}");
  schema = "public";
  table = "";
  private offset = 0;
  private editingPrimaryKey: Record<string, unknown> | null = null;
  readonly filterColumn = signal("");
  readonly filterValue = signal("");
  readonly sortColumn = signal("");
  readonly sortDirection = signal<"asc" | "desc">("asc");

  ngOnInit(): void {
    this.subscription.add(this.route.paramMap.subscribe((params) => {
      this.schema = params.get("schema") ?? "public";
      this.table = params.get("table") ?? "";
      this.offset = 0;
      this.filterColumn.set("");
      this.filterValue.set("");
      this.sortColumn.set("");
      this.sortDirection.set("asc");
      this.load();
    }));
  }

  ngOnDestroy(): void { this.subscription.unsubscribe(); }
  load(): void {
    this.loading.set(true); this.error.set(null);
    const filters = this.filterColumn() && this.filterValue().trim() ? [{ column: this.filterColumn(), operator: "contains", value: this.filterValue().trim() }] : [];
    this.api.getRows(this.schema, this.table, { offset: this.offset, sortColumn: this.sortColumn() || undefined, sortDirection: this.sortDirection(), filters }).subscribe({
      next: (value) => { this.rows.set(value); if (!this.filterColumn() && value.columns.length) this.filterColumn.set(value.columns[0].name); this.loading.set(false); },
      error: (error: Error) => { this.error.set(error.message); this.loading.set(false); },
    });
  }
  next(): void { this.offset += this.rows()?.limit ?? 100; this.load(); }
  previous(): void { this.offset = Math.max(0, this.offset - (this.rows()?.limit ?? 100)); this.load(); }
  applyQuery(): void { this.offset = 0; this.load(); }
  clearQuery(): void { this.filterValue.set(""); this.sortColumn.set(""); this.sortDirection.set("asc"); this.offset = 0; this.load(); }
  sortBy(column: string): void { if (this.sortColumn() === column) this.sortDirection.set(this.sortDirection() === "asc" ? "desc" : "asc"); else { this.sortColumn.set(column); this.sortDirection.set("asc"); } this.offset = 0; this.load(); }
  primaryKeyLabel(): string { const keys = this.rows()?.primaryKey.map((item) => item.name) ?? []; return keys.length ? `PK: ${keys.join(", ")}` : "Read-only · no PK"; }
  rowKey(row: Record<string, unknown>): string { const keys = this.rows()?.primaryKey.map((item) => String(row[item.name])) ?? []; return keys.join("|") || JSON.stringify(row); }
  formatValue(value: unknown): string { return value === null ? "NULL" : typeof value === "object" ? JSON.stringify(value) : String(value); }
  startInsert(): void { this.editingPrimaryKey = null; this.editorJson.set("{\n  \n}"); this.editorMode.set("insert"); }
  startEdit(row: Record<string, unknown>): void {
    const keys = this.rows()?.primaryKey ?? [];
    if (!keys.length) return;
    this.editingPrimaryKey = Object.fromEntries(keys.map((item) => [item.name, row[item.name]]));
    this.editorJson.set(JSON.stringify(row, null, 2)); this.editorMode.set("edit");
  }
  saveRow(): void {
    let values: Record<string, unknown>;
    try { values = JSON.parse(this.editorJson()) as Record<string, unknown>; } catch { window.alert("JSON không hợp lệ."); return; }
    const operation = this.editorMode() === "insert" ? "insert" : "update";
    const primaryKey = this.editingPrimaryKey ?? undefined;
    this.api.previewRowMutation(this.schema, this.table, { operation, values, primary_key: primaryKey }).subscribe({
      next: (preview) => {
        if (!window.confirm(`${preview.warnings.join("\n")}\n\n${preview.target}\n\nContinue?`)) return;
        const request = operation === "insert" ? this.api.insertRow(this.schema, this.table, values, preview.confirmationToken) : this.api.updateRow(this.schema, this.table, primaryKey ?? {}, values, preview.confirmationToken);
        request.subscribe({ next: () => { this.editorMode.set(null); this.load(); }, error: (error: Error) => window.alert(error.message) });
      },
      error: (error: Error) => window.alert(error.message),
    });
  }
  remove(row: Record<string, unknown>): void {
    const keys = this.rows()?.primaryKey ?? [];
    if (!keys.length || !window.confirm("Delete this row? This action cannot be undone.")) return;
    const primaryKey = Object.fromEntries(keys.map((item) => [item.name, row[item.name]]));
    this.api.previewRowMutation(this.schema, this.table, { operation: "delete", primary_key: primaryKey }).subscribe({
      next: (preview) => {
        if (!window.confirm(`${preview.warnings.join("\n")}\n\n${preview.target}\n\nContinue?`)) return;
        this.api.deleteRow(this.schema, this.table, primaryKey, preview.confirmationToken).subscribe({ next: () => this.load(), error: (error: Error) => window.alert(error.message) });
      },
      error: (error: Error) => window.alert(error.message),
    });
  }
}
