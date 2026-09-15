import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { basicSetup } from "codemirror";
import { EditorState } from "@codemirror/state";
import { sql } from "@codemirror/lang-sql";
import { EditorView, ViewUpdate } from "@codemirror/view";

import { ApiService } from "../../core/api.service";
import { AuthService } from "../../core/auth.service";
import { SqlResult, SqlValidation } from "../../core/models";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, MatProgressSpinnerModule],
  template: `
    <section class="page-header"><div><p class="eyebrow">Power tools</p><h1>SQL editor</h1><p class="lede">Run database-scoped SQL with a validation step, isolated transaction and visible result set.</p></div><span class="sql-mode-badge"><span class="status-dot"></span> Admin SQL enabled</span></section>
    <div class="sql-layout"><mat-card class="panel-card editor-card"><div class="editor-toolbar"><div class="editor-tab"><mat-icon>terminal</mat-icon><span>query-{{ queryNumber }}</span></div><div class="editor-actions">@if (auth.can('db_admin:sql')) { <button mat-button (click)="clear()">Clear</button><button mat-stroked-button (click)="validate()" [disabled]="busy()">Validate</button><button mat-flat-button color="primary" (click)="run()" [disabled]="busy()"><mat-icon>{{ busy() ? 'hourglass_top' : 'play_arrow' }}</mat-icon>{{ busy() ? 'Running…' : 'Run SQL' }}</button> }</div></div><div #editorHost class="code-host"></div><div class="editor-status"><span><mat-icon>lock</mat-icon> Request-isolated execution</span><span><mat-icon>speed</mat-icon> Timeout protected</span><span><mat-icon>visibility</mat-icon> Max rows enforced</span></div></mat-card>
      <mat-card class="panel-card sql-side"><p class="eyebrow">Execution notes</p><h2>Stay in control</h2><div class="note-item"><mat-icon>preview</mat-icon><div><strong>Validate first</strong><span>Mutations receive a short-lived confirmation token.</span></div></div><div class="note-item"><mat-icon>sync_lock</mat-icon><div><strong>One request, one transaction</strong><span>Read queries rollback; writes commit only after confirmation.</span></div></div><div class="note-item"><mat-icon>shield</mat-icon><div><strong>Guarded commands</strong><span>Transaction control, roles and COPY are blocked.</span></div></div><div class="example-query"><span>Try a safe query</span><button mat-button (click)="useExample()">SELECT current_database();</button></div></mat-card></div>
    @if (validation(); as check) { <mat-card class="panel-card validation-card"><div class="card-heading"><div><p class="eyebrow">Validation result</p><h2>{{ check.classification.replace('_', ' ') }}</h2></div><span class="classification" [class.mutation]="check.classification !== 'read_only'">{{ check.statementCount }} statement{{ check.statementCount === 1 ? '' : 's' }}</span></div><div class="warning-list">@for (warning of check.warnings; track warning) { <span><mat-icon>info</mat-icon>{{ warning }}</span> }</div>@if (check.requiresConfirmation) { <div class="confirm-row"><span>This statement changes database state.</span><button mat-flat-button color="primary" (click)="execute(check)">Confirm and execute</button></div> }</mat-card> }
    @if (error()) { <div class="error-banner"><mat-icon>error_outline</mat-icon><span>{{ error() }}</span></div> }
    @if (result(); as output) { <mat-card class="panel-card result-card"><div class="card-heading"><div><p class="eyebrow">Query result</p><h2>{{ output.rowCount < 0 ? output.rows.length : output.rowCount }} rows</h2></div>@if (output.truncated) { <span class="warning-pill"><mat-icon>warning</mat-icon> Result truncated</span> }</div>@if (output.columns.length) { <div class="data-table-wrap"><table><thead><tr>@for (column of output.columns; track column) { <th>{{ column }}</th> }</tr></thead><tbody>@for (row of output.rows; track $index) { <tr>@for (column of output.columns; track column) { <td>{{ formatValue(row[column]) }}</td> }</tr> } @empty { <tr><td [attr.colspan]="output.columns.length" class="empty-table">Query returned no rows.</td></tr> }</tbody></table></div> } @else { <div class="command-result"><mat-icon>check_circle</mat-icon><span>Command completed successfully.</span></div> }</mat-card> }
  `,
})
export class SqlEditorPageComponent implements AfterViewInit, OnDestroy {
  @ViewChild("editorHost", { static: true }) private readonly editorHost?: ElementRef<HTMLDivElement>;
  private readonly api = inject(ApiService);
  readonly auth = inject(AuthService);
  private editor?: EditorView;
  readonly sql = signal("SELECT table_schema, table_name\nFROM information_schema.tables\nWHERE table_schema NOT IN ('pg_catalog', 'information_schema')\nORDER BY table_schema, table_name;");
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly validation = signal<SqlValidation | null>(null);
  readonly result = signal<SqlResult | null>(null);
  queryNumber = 1;

  ngAfterViewInit(): void {
    const host = this.editorHost?.nativeElement;
    if (!host) return;
    this.editor = new EditorView({
      state: EditorState.create({
        doc: this.sql(),
        extensions: [basicSetup, sql(), EditorView.updateListener.of((update: ViewUpdate) => { if (update.docChanged) this.sql.set(update.state.doc.toString()); })],
      }),
      parent: host,
    });
  }
  ngOnDestroy(): void { this.editor?.destroy(); }
  clear(): void { this.sql.set(""); this.editor?.dispatch({ changes: { from: 0, to: this.editor.state.doc.length, insert: "" } }); this.validation.set(null); this.result.set(null); }
  useExample(): void { this.sql.set("SELECT current_database(), current_user, current_schema();"); this.editor?.dispatch({ changes: { from: 0, to: this.editor.state.doc.length, insert: this.sql() } }); }
  validate(): void {
    this.busy.set(true); this.error.set(null); this.result.set(null);
    this.api.validateSql(this.sql()).subscribe({ next: (value) => { this.validation.set(value); this.busy.set(false); }, error: (error: Error) => { this.error.set(error.message); this.busy.set(false); } });
  }
  run(): void {
    this.validateAndMaybeRun();
  }
  execute(check: SqlValidation): void {
    this.busy.set(true); this.error.set(null);
    this.api.executeSql({ sql: this.sql(), confirmation_token: check.confirmationToken }).subscribe({ next: (value) => { this.result.set(value); this.busy.set(false); this.validation.set(null); }, error: (error: Error) => { this.error.set(error.message); this.busy.set(false); } });
  }
  formatValue(value: unknown): string { return value === null ? "NULL" : typeof value === "object" ? JSON.stringify(value) : String(value); }
  private validateAndMaybeRun(): void {
    this.busy.set(true); this.error.set(null); this.result.set(null);
    this.api.validateSql(this.sql()).subscribe({ next: (check) => { this.validation.set(check); this.busy.set(false); if (!check.requiresConfirmation) this.execute(check); }, error: (error: Error) => { this.error.set(error.message); this.busy.set(false); } });
  }
}
