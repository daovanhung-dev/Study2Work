import { Component, ElementRef, OnDestroy, ViewChild, effect, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { basicSetup } from "codemirror";
import { sql } from "@codemirror/lang-sql";
import { EditorState } from "@codemirror/state";
import { EditorView, ViewUpdate, keymap, placeholder } from "@codemirror/view";

import { ApiService } from "../../core/api.service";
import { AdminStateService } from "../../core/admin-state.service";
import { AuthService } from "../../core/auth.service";
import { ApiErrorInfo, CatalogData, CatalogItem, QueryHistoryItem, SqlResult, SqlValidation } from "../../core/models";

type ObjectGroupKey = Exclude<keyof CatalogData, "schemas">;

export function quoteSqlIdentifier(value: string): string {
  return `"${value.replaceAll('"', '""')}"`;
}

export function buildObjectSql(group: ObjectGroupKey, schema: string, objectName: string): string {
  const qualified = `${quoteSqlIdentifier(schema)}.${quoteSqlIdentifier(objectName)}`;
  return group === "tables" || group === "views" ? `SELECT * FROM ${qualified} LIMIT 100;` : qualified;
}

interface ObjectGroup {
  key: ObjectGroupKey;
  label: string;
  icon: string;
}

@Component({
  standalone: true,
  imports: [
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  template: `
    <section class="workspace-heading">
      <div>
        <p class="eyebrow">SQL workspace</p>
        <h1>Inspect and run</h1>
        <p class="lede">Browse the selected schema, compose a query, and inspect results without leaving this view.</p>
      </div>
    </section>

    @if (state.errorInfo(); as error) {
      <div class="error-banner">
        <mat-icon>error_outline</mat-icon>
        <div class="error-copy"><strong>{{ error.message }}</strong><small>{{ error.businessCode || 'DB_ADMIN_ERROR' }}@if (error.traceId) {<span> · trace {{ error.traceId }}</span>}</small></div>
        <button mat-button (click)="retry()">Retry</button>
      </div>
    }

    <div class="workspace-grid">
      <aside class="object-tree panel-card">
        <div class="tree-heading">
          <div><p class="eyebrow">Catalog</p><h2>{{ state.selectedSchema() || 'Choose a schema' }}</h2></div>
          <button mat-icon-button aria-label="Refresh catalog" [disabled]="!state.selectedDatabase() || state.loading()" (click)="refreshCatalog()"><mat-icon>refresh</mat-icon></button>
        </div>
        @if (state.selectedDatabase() && state.catalog()) {
          <label class="catalog-search">
            <mat-icon>search</mat-icon>
            <input aria-label="Search catalog" placeholder="Search objects" [value]="catalogSearch()" (input)="catalogSearch.set($any($event.target).value)" />
            @if (catalogSearch()) { <button type="button" aria-label="Clear catalog search" (click)="catalogSearch.set('')"><mat-icon>close</mat-icon></button> }
          </label>
        }
        @if (!state.selectedDatabase()) {
          <div class="tree-empty"><mat-icon>storage</mat-icon><span>Choose a database to load its catalog.</span></div>
        } @else if (state.catalogLoading() && !state.catalog()) {
          <div class="tree-empty"><mat-spinner diameter="24"></mat-spinner><span>Loading catalog…</span></div>
        } @else if (!state.selectedSchema()) {
          <div class="tree-empty"><mat-icon>account_tree</mat-icon><span>Choose a schema to see its objects.</span></div>
        } @else {
          @for (group of groups; track group.key) {
            <div class="tree-group" [class.collapsed]="isGroupCollapsed(group.key)">
              <button type="button" class="tree-group-heading" [attr.aria-expanded]="!isGroupCollapsed(group.key)" (click)="toggleGroup(group.key)">
                <mat-icon>{{ isGroupCollapsed(group.key) ? 'chevron_right' : 'expand_more' }}</mat-icon><mat-icon>{{ group.icon }}</mat-icon><strong>{{ group.label }}</strong><span>{{ objectsFor(group).length }}</span>
              </button>
              @if (!isGroupCollapsed(group.key)) {
                @for (item of objectsFor(group); track objectKeyForItem(item)) {
                  <button type="button" class="tree-item" [title]="objectSubtitle(item)" (click)="insertObject(group, item)"><mat-icon>chevron_right</mat-icon><span>{{ objectName(item) }}</span><small>{{ objectSubtitle(item) }}</small></button>
                } @empty {
                  <div class="tree-none">{{ catalogSearch() ? 'No matching objects.' : 'No ' + group.label.toLowerCase() + '.' }}</div>
                }
              }
            </div>
          }
        }
      </aside>

      <main class="sql-workbench">
        @if (!auth.can('db_admin:sql')) {
          <mat-card class="panel-card workspace-empty"><mat-icon>lock</mat-icon><h2>SQL permission required</h2><p>Your account can browse the catalog but cannot run SQL.</p></mat-card>
        } @else {
          <mat-card class="panel-card editor-card">
            <div class="editor-toolbar">
              <div class="editor-tab"><mat-icon>terminal</mat-icon><span>{{ state.selectedDatabase() || 'Choose database' }} · {{ state.selectedSchema() || 'Choose schema' }}</span></div>
              <div class="editor-actions"><button mat-button (click)="useExample()">Example</button><button mat-button (click)="toggleHistory()" [attr.aria-expanded]="historyOpen()"><mat-icon>history</mat-icon> History@if (history().length) { <span class="toolbar-count">{{ history().length }}</span> }</button><button mat-button (click)="clear()">Clear</button><button mat-flat-button color="primary" (click)="run()" [disabled]="!canRun()"><mat-icon>{{ busy() ? 'hourglass_top' : 'play_arrow' }}</mat-icon>{{ busy() ? 'Running…' : 'Run SQL' }}</button></div>
            </div>
            @if (historyOpen()) {
              <div class="history-panel" aria-label="Query history">
                <div class="history-heading"><div><strong>Recent queries</strong><small>Session only · {{ history().length }}/20</small></div><button mat-button (click)="clearHistory()" [disabled]="!history().length">Clear history</button></div>
                @for (item of history(); track item.id) {
                  <div class="history-item">
                    <button type="button" class="history-load" (click)="loadHistory(item)">
                      <span class="history-status" [class.failed]="item.status === 'error'"><mat-icon>{{ item.status === 'success' ? 'check' : 'error_outline' }}</mat-icon></span>
                      <span class="history-sql">{{ item.sql }}</span>
                      <small>{{ item.database }} · {{ item.schemaName }} · {{ formatHistoryDate(item.executedAt) }}</small>
                    </button>
                    <button type="button" class="history-remove" [attr.aria-label]="'Remove query from history: ' + item.sql" (click)="removeHistory(item.id)"><mat-icon>close</mat-icon></button>
                  </div>
                } @empty { <div class="history-empty"><mat-icon>history</mat-icon><span>No queries in this session.</span></div> }
              </div>
            }
            <div #editorHost class="code-host"></div>
            <div class="editor-status"><span><mat-icon>{{ state.selectedSchema() ? 'account_tree' : 'info' }}</mat-icon> {{ state.selectedSchema() ? 'search_path: ' + state.selectedSchema() : 'Select a database and schema to enable Run SQL' }}</span><span><mat-icon>speed</mat-icon> server row limit enforced</span><span><mat-icon>lock</mat-icon> mutations require confirmation</span></div>
          </mat-card>

          @if (notice()) { <div class="workspace-notice"><mat-icon>check_circle</mat-icon>{{ notice() }}</div> }

          @if (validation(); as check) {
            @if (check.requiresConfirmation) {
              <mat-card class="panel-card validation-card"><div class="card-heading"><div><p class="eyebrow">Confirmation required</p><h2>{{ check.classification.replace('_', ' ') }}</h2></div><span class="classification mutation">{{ check.statementCount }} statement{{ check.statementCount === 1 ? '' : 's' }}</span></div><div class="warning-list">@for (warning of check.warnings; track warning) { <span><mat-icon>warning</mat-icon>{{ warning }}</span> }</div><div class="confirm-row"><span>This statement changes database state.</span><button mat-flat-button color="primary" (click)="execute(check)" [disabled]="busy()">Confirm and run</button></div></mat-card>
            }
          }

          @if (errorInfo(); as runError) {
            <div class="error-banner query-error"><mat-icon>error_outline</mat-icon><div class="error-copy"><strong>{{ runError.message }}</strong><small>{{ runError.businessCode || 'DB_ADMIN_SQL_ERROR' }}@if (runError.traceId) {<span> · trace {{ runError.traceId }}</span>}</small></div>@if (runError.traceId) { <button mat-button (click)="copyTrace(runError.traceId)">{{ copiedTrace() === runError.traceId ? 'Copied' : 'Copy trace' }}</button> }</div>
          }

          @if (result(); as output) {
            <mat-card class="panel-card result-card"><div class="card-heading"><div><p class="eyebrow">Query result</p><h2>{{ output.rowCount < 0 ? output.rows.length : output.rowCount }} rows</h2></div><div class="result-badges"><span class="classification" [class.mutation]="output.classification !== 'read_only'">{{ output.classification.replace('_', ' ') }}</span>@if (output.truncated) { <span class="warning-pill"><mat-icon>warning</mat-icon> Result truncated</span> }</div></div>@if (output.columns.length) { <div class="data-table-wrap"><table><thead><tr>@for (column of output.columns; track column) { <th>{{ column }}</th> }</tr></thead><tbody>@for (row of output.rows; track $index) { <tr>@for (column of output.columns; track column) { <td>{{ formatValue(row[column]) }}</td> }</tr> } @empty { <tr><td [attr.colspan]="output.columns.length" class="empty-table">Query returned no rows.</td></tr> }</tbody></table></div> } @else { <div class="command-result"><mat-icon>check_circle</mat-icon><span>Command completed successfully.</span></div> }</mat-card>
          }
        }
      </main>
    </div>
  `,
})
export class WorkspacePageComponent implements OnDestroy {
  @ViewChild("editorHost")
  set editorHost(element: ElementRef<HTMLDivElement> | undefined) {
    if (element && !this.editor) this.createEditor(element.nativeElement);
  }
  private readonly api = inject(ApiService);
  readonly state = inject(AdminStateService);
  readonly auth = inject(AuthService);
  private editor?: EditorView;
  readonly sql = signal("");
  readonly busy = signal(false);
  readonly errorInfo = signal<ApiErrorInfo | null>(null);
  readonly validation = signal<SqlValidation | null>(null);
  readonly result = signal<SqlResult | null>(null);
  readonly catalogSearch = signal("");
  readonly history = signal<QueryHistoryItem[]>([]);
  readonly historyOpen = signal(false);
  readonly notice = signal<string | null>(null);
  readonly copiedTrace = signal<string | null>(null);
  private readonly collapsedGroups = signal<Set<ObjectGroupKey>>(new Set());
  private previousContext = "";
  private executionVersion = 0;
  private pendingContext: { version: number; database: string; schema: string; sql: string } | null = null;
  private readonly contextWatcher = effect(() => {
    const context = `${this.state.selectedDatabase() ?? ''}:${this.state.selectedSchema() ?? ''}`;
    if (this.previousContext && context !== this.previousContext) this.resetExecution();
    this.previousContext = context;
  });
  readonly groups: ObjectGroup[] = [
    { key: "tables", label: "Tables", icon: "table_chart" },
    { key: "views", label: "Views", icon: "visibility" },
    { key: "routines", label: "Functions & procedures", icon: "functions" },
    { key: "triggers", label: "Triggers", icon: "bolt" },
    { key: "types", label: "Types", icon: "category" },
    { key: "sequences", label: "Sequences", icon: "format_list_numbered" },
    { key: "indexes", label: "Indexes", icon: "speed" },
    { key: "constraints", label: "Constraints", icon: "rule" },
    { key: "grants", label: "Grants", icon: "key" },
  ];

  private createEditor(host: HTMLDivElement): void {
    this.editor = new EditorView({
      state: EditorState.create({
        doc: this.sql(),
        extensions: [basicSetup, sql(), placeholder("Write SQL after selecting a database and schema"), keymap.of([{ key: "Mod-Enter", run: () => { this.run(); return true; } }]), EditorView.updateListener.of((update: ViewUpdate) => { if (update.docChanged) { this.sql.set(update.state.doc.toString()); this.pendingContext = null; this.validation.set(null); } })],
      }),
      parent: host,
    });
  }

  ngOnDestroy(): void { this.editor?.destroy(); }

  objectsFor(group: ObjectGroup): CatalogItem[] {
    const catalog = this.state.catalog();
    const schema = this.state.selectedSchema();
    if (!catalog || !schema) return [];
    return catalog[group.key].filter((item) => this.displaySchema(item) === schema && this.matchesSearch(item));
  }

  isGroupCollapsed(group: ObjectGroupKey): boolean { return this.collapsedGroups().has(group); }

  toggleGroup(group: ObjectGroupKey): void {
    const next = new Set(this.collapsedGroups());
    if (next.has(group)) next.delete(group); else next.add(group);
    this.collapsedGroups.set(next);
  }

  objectKeyForItem(item: CatalogItem): string { return `${this.objectName(item)}:${this.objectSubtitle(item)}`; }

  objectName(item: CatalogItem): string { return String(item.name || item.table_name || item.grantee || "Unnamed object"); }

  objectSubtitle(item: CatalogItem): string {
    const details = [this.displaySchema(item)];
    if (item.table_name) details.push(String(item.table_name));
    if (item.kind) details.push(String(item.kind));
    if (item.grantee) details.push(String(item.grantee));
    if (item.privilege_type) details.push(String(item.privilege_type));
    return details.join(" · ");
  }

  insertObject(group: ObjectGroup, item: CatalogItem): void {
    const schema = this.displaySchema(item);
    const objectName = this.objectName(item);
    const value = buildObjectSql(group.key, schema, objectName);
    this.setEditorValue(value);
    this.notice.set(`Inserted ${group.label.toLowerCase().replace(' & ', '/')}: ${schema}.${objectName}`);
    this.historyOpen.set(false);
    this.editor?.focus();
  }

  refreshCatalog(): void { this.state.load(); this.resetExecution(); }
  retry(): void {
    this.resetExecution();
    if (this.state.selectedDatabase()) this.state.load(); else this.state.loadDatabases();
  }
  clear(): void { this.setEditorValue(""); this.resetExecution(); }
  useExample(): void { this.setEditorValue("SELECT current_database(), current_schema();"); this.resetExecution(); }

  toggleHistory(): void { this.historyOpen.update((open) => !open); }

  clearHistory(): void { this.history.set([]); }

  removeHistory(id: string): void { this.history.update((items) => items.filter((item) => item.id !== id)); }

  loadHistory(item: QueryHistoryItem): void {
    this.setEditorValue(item.sql);
    this.historyOpen.set(false);
    this.resetExecution();
    this.notice.set(`Loaded query from ${item.database} · ${item.schemaName}. Select the same target before running.`);
  }

  formatHistoryDate(value: string): string {
    return new Intl.DateTimeFormat("vi-VN", { hour: "2-digit", minute: "2-digit" }).format(new Date(value));
  }

  canRun(): boolean {
    return !this.busy() && !this.state.loading() && Boolean(this.state.selectedDatabase() && this.state.selectedSchema() && this.sql().trim());
  }

  run(): void {
    const database = this.state.selectedDatabase();
    const schema = this.state.selectedSchema();
    if (!database || !schema || !this.sql().trim()) return;
    this.busy.set(true);
    const context = { version: ++this.executionVersion, database, schema, sql: this.sql() };
    this.pendingContext = context;
    this.errorInfo.set(null);
    this.notice.set(null);
    this.result.set(null);
    this.validation.set(null);
    this.api.validateSql({ database, schema_name: schema, sql: context.sql }).subscribe({
      next: (check) => {
        if (context.version !== this.executionVersion) return;
        this.validation.set(check);
        this.busy.set(false);
        if (!check.requiresConfirmation) this.execute(check, context);
      },
      error: (error: unknown) => {
        if (context.version !== this.executionVersion) return;
        this.setError(error, "SQL validation failed.");
        this.recordHistory(context, "error");
        this.busy.set(false);
      },
    });
  }

  execute(check: SqlValidation, context = this.pendingContext ?? this.currentContext()): void {
    const database = this.state.selectedDatabase();
    const schema = this.state.selectedSchema();
    if (!database || !schema || database !== context.database || schema !== context.schema) return;
    this.busy.set(true);
    this.errorInfo.set(null);
    this.api.executeSql({ database: context.database, schema_name: context.schema, sql: context.sql, confirmation_token: check.confirmationToken }).subscribe({
      next: (value) => {
        if (context.version !== this.executionVersion) return;
        this.result.set(value);
        this.busy.set(false);
        this.validation.set(null);
        this.recordHistory(context, "success", value.rowCount);
      },
      error: (error: unknown) => {
        if (context.version !== this.executionVersion) return;
        this.setError(error, "SQL execution failed.");
        this.recordHistory(context, "error");
        this.busy.set(false);
      },
    });
  }

  formatValue(value: unknown): string { return value === null ? "NULL" : typeof value === "object" ? JSON.stringify(value) : String(value); }

  copyTrace(traceId: string): void {
    void navigator.clipboard?.writeText(traceId);
    this.copiedTrace.set(traceId);
  }

  private resetExecution(): void {
    this.executionVersion += 1;
    this.pendingContext = null;
    this.errorInfo.set(null);
    this.validation.set(null);
    this.result.set(null);
    this.notice.set(null);
    this.copiedTrace.set(null);
    this.busy.set(false);
  }

  private setEditorValue(value: string): void {
    this.sql.set(value);
    this.editor?.dispatch({ changes: { from: 0, to: this.editor.state.doc.length, insert: value } });
  }

  private currentContext(): { version: number; database: string; schema: string; sql: string } {
    return {
      version: this.executionVersion,
      database: this.state.selectedDatabase() ?? "",
      schema: this.state.selectedSchema() ?? "",
      sql: this.sql(),
    };
  }

  private recordHistory(
    context: { database: string; schema: string; sql: string },
    status: QueryHistoryItem["status"],
    rowCount?: number,
  ): void {
    const item: QueryHistoryItem = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      sql: context.sql,
      database: context.database,
      schemaName: context.schema,
      executedAt: new Date().toISOString(),
      status,
      rowCount,
    };
    this.history.update((items) => [item, ...items].slice(0, 20));
  }

  private matchesSearch(item: CatalogItem): boolean {
    const query = this.catalogSearch().trim().toLowerCase();
    if (!query) return true;
    return [this.objectName(item), item.kind, item.table_name, item.grantee, item.privilege_type]
      .filter(Boolean)
      .some((value) => String(value).toLowerCase().includes(query));
  }

  private setError(error: unknown, fallback: string): void {
    if (error && typeof error === "object" && "message" in error) {
      const candidate = error as { message?: unknown; businessCode?: unknown; traceId?: unknown };
      this.errorInfo.set({
        message: typeof candidate.message === "string" && candidate.message ? candidate.message : fallback,
        businessCode: typeof candidate.businessCode === "string" ? candidate.businessCode : undefined,
        traceId: typeof candidate.traceId === "string" ? candidate.traceId : undefined,
      });
      return;
    }
    this.errorInfo.set({ message: fallback });
  }

  private displaySchema(item: CatalogItem): string { return String(item.schema_name ?? item.schemaName ?? "public"); }
}
