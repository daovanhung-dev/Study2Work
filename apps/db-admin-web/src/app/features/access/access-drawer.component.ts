import { Component, EventEmitter, Input, Output, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { Observable } from "rxjs";

import { AdminApiError, ApiService } from "../../core/api.service";
import { AuthService } from "../../core/auth.service";
import { AccessAccount, AccessAuditResult, DatabaseTarget } from "../../core/models";

@Component({
  selector: "db-access-drawer",
  standalone: true,
  imports: [MatButtonModule, MatIconModule, MatProgressSpinnerModule],
  template: `
    @if (open) {
      <div class="access-scrim" (click)="closed.emit()"></div>
      <aside class="access-drawer" role="dialog" aria-modal="true" aria-labelledby="access-title">
        <header class="access-header">
          <div><p class="eyebrow">Root only</p><h2 id="access-title">Manage access</h2><p>Accounts, isolated schemas and DB Admin audit.</p></div>
          <button mat-icon-button aria-label="Close access management" (click)="closed.emit()"><mat-icon>close</mat-icon></button>
        </header>
        <div class="access-body">
          @if (errorMessage()) { <div class="error-banner access-error"><mat-icon>error_outline</mat-icon><div class="error-copy"><strong>{{ errorMessage() }}</strong></div><button mat-button (click)="errorMessage.set(null)">Dismiss</button></div> }
          <section class="access-section create-account">
            <div class="access-section-heading"><div><p class="eyebrow">Provision</p><h3>Create developer account</h3></div><mat-icon>person_add</mat-icon></div>
            <div class="access-form-grid">
              <label><span>Database</span><select [value]="newDatabase" (change)="newDatabase = inputValue($event)"><option value="">Choose target</option>@for (database of databases(); track database.id) { <option [value]="database.id">{{ database.label }}</option> }</select></label>
              <label><span>Username</span><input autocomplete="off" placeholder="dev_name" [value]="newUsername" (input)="newUsername = inputValue($event)" /></label>
              <label><span>Display name</span><input autocomplete="off" placeholder="Developer" [value]="newDisplayName" (input)="newDisplayName = inputValue($event)" /></label>
              <label><span>Schema</span><input autocomplete="off" placeholder="dev_name" [value]="newSchema" (input)="newSchema = inputValue($event)" /></label>
            </div>
            <button mat-flat-button color="primary" (click)="createAccount()" [disabled]="busy() || !newDatabase || !newUsername.trim() || !newDisplayName.trim() || !newSchema.trim()"><mat-icon>add</mat-icon> Create account</button>
          </section>

          <section class="access-section">
            <div class="access-section-heading"><div><p class="eyebrow">Accounts</p><h3>{{ accounts().length }} account{{ accounts().length === 1 ? '' : 's' }}</h3></div><button mat-icon-button aria-label="Refresh access accounts" (click)="load()" [disabled]="busy()"><mat-icon>refresh</mat-icon></button></div>
            @if (loadingAccounts()) { <div class="access-loading"><mat-spinner diameter="22"></mat-spinner><span>Loading accounts…</span></div> }
            @else { @for (account of accounts(); track account.id) {
              <article class="account-card">
                <div class="account-card-header"><div class="account-identity"><span class="account-avatar"><mat-icon>{{ account.isRoot ? 'shield' : 'person' }}</mat-icon></span><div><strong>{{ account.username }}</strong><small>{{ account.displayName }} · {{ account.isRoot ? 'Root' : 'Developer' }}</small></div></div><span class="account-status" [class.disabled]="account.status === 'disabled'">{{ account.status }}</span></div>
                <div class="account-binding-list">@for (binding of account.bindings; track binding.database + binding.schema) { <div class="account-binding"><span><mat-icon>database</mat-icon>{{ binding.database }} <b>/</b> {{ binding.schema }}</span>@if (!account.isRoot) { <div class="binding-edit"><input [attr.aria-label]="'New schema for ' + account.username" [value]="schemaDraft(account.id, binding.schema)" (input)="setSchemaDraft(account.id, inputValue($event))" /><button mat-button (click)="changeSchema(account, binding.database)" [disabled]="busy()">Reassign</button></div> }</div> } @empty { <span class="binding-empty">No developer schema binding.</span> }</div>
                <div class="account-actions">@if (!account.isRoot) { <input class="display-edit" [attr.aria-label]="'Display name for ' + account.username" [value]="displayDraft(account)" (input)="setDisplayDraft(account.id, inputValue($event))" /><button mat-button (click)="saveDisplayName(account)" [disabled]="busy()">Save name</button><button mat-button (click)="toggleAccount(account)" [disabled]="busy()">{{ account.status === 'active' ? 'Disable' : 'Enable' }}</button><button mat-stroked-button (click)="rotatePassword(account)" [disabled]="busy()"><mat-icon>key</mat-icon> Rotate secret</button> }</div>
              </article>
            } @empty { <div class="access-empty"><mat-icon>group_off</mat-icon><span>No accounts found.</span></div> } }
          </section>

          <section class="access-section audit-section">
            <div class="access-section-heading"><div><p class="eyebrow">Audit</p><h3>Recent control-plane events</h3></div><button mat-icon-button aria-label="Refresh access audit" (click)="loadAudit()" [disabled]="busy()"><mat-icon>history</mat-icon></button></div>
            @if (loadingAudit()) { <div class="access-loading"><mat-spinner diameter="22"></mat-spinner><span>Loading audit…</span></div> } @else { @for (entry of audit().entries; track entry.traceId + entry.timestamp) { <div class="audit-row"><span class="audit-outcome" [class.failed]="entry.outcome !== 'success'"><mat-icon>{{ entry.outcome === 'success' ? 'check_circle' : 'error_outline' }}</mat-icon></span><div><strong>{{ entry.action }}</strong><small>{{ entry.actor }} · {{ entry.target }} · {{ formatDate(entry.timestamp) }}</small><small class="trace-line">trace {{ entry.traceId }}</small></div></div> } @empty { <div class="access-empty"><mat-icon>history_toggle_off</mat-icon><span>No audit events yet.</span></div> } }
          </section>
        </div>
        @if (secret()) { <div class="secret-modal" role="alertdialog" aria-labelledby="secret-title"><div class="secret-modal-card"><mat-icon>warning</mat-icon><h3 id="secret-title">Save this secret now</h3><p>It is shown once and cannot be recovered from DB Admin.</p><code>{{ secret() }}</code><div><button mat-stroked-button (click)="copySecret()"><mat-icon>content_copy</mat-icon>{{ copied() ? 'Copied' : 'Copy secret' }}</button><button mat-flat-button color="primary" (click)="secret.set(null); copied.set(false)">Done</button></div></div></div> }
      </aside>
    }
  `,
})
export class AccessDrawerComponent {
  @Input() open = false;
  @Output() readonly closed = new EventEmitter<void>();
  readonly auth = inject(AuthService);
  private readonly api = inject(ApiService);
  readonly accounts = signal<AccessAccount[]>([]);
  readonly databases = signal<DatabaseTarget[]>([]);
  readonly audit = signal<AccessAuditResult>({ entries: [] });
  readonly loadingAccounts = signal(false);
  readonly loadingAudit = signal(false);
  readonly busy = signal(false);
  readonly errorMessage = signal<string | null>(null);
  readonly secret = signal<string | null>(null);
  readonly copied = signal(false);
  newDatabase = "";
  newUsername = "";
  newDisplayName = "";
  newSchema = "";
  private readonly schemaDrafts = new Map<string, string>();
  private readonly displayDrafts = new Map<string, string>();

  ngOnChanges(): void {
    if (this.open && !this.accounts().length && !this.loadingAccounts()) this.load();
  }

  inputValue(event: Event): string { return (event.target as HTMLInputElement).value; }

  load(): void {
    this.loadingAccounts.set(true);
    this.errorMessage.set(null);
    this.api.getDatabases().subscribe({
      next: (value) => this.databases.set(value.databases),
      error: (error: unknown) => this.setError(error, "Unable to load database targets."),
    });
    this.api.getAccessAccounts().subscribe({
      next: (value) => { this.accounts.set(value.accounts); this.loadingAccounts.set(false); },
      error: (error: unknown) => { this.loadingAccounts.set(false); this.setError(error, "Unable to load access accounts."); },
    });
    this.loadAudit();
  }

  loadAudit(): void {
    this.loadingAudit.set(true);
    this.api.getAccessAudit({ limit: 80 }).subscribe({
      next: (value) => { this.audit.set(value); this.loadingAudit.set(false); },
      error: (error: unknown) => { this.loadingAudit.set(false); this.setError(error, "Unable to load access audit."); },
    });
  }

  createAccount(): void {
    this.runAction(() => this.api.createAccessAccount({ database: this.newDatabase, username: this.newUsername.trim(), display_name: this.newDisplayName.trim(), schema_name: this.newSchema.trim() }), (account) => {
      this.showSecret(account.secret);
      this.newUsername = ""; this.newDisplayName = ""; this.newSchema = "";
    });
  }

  toggleAccount(account: AccessAccount): void {
    this.runAction(() => this.api.updateAccessAccount(account.id, { status: account.status === "active" ? "disabled" : "active" }));
  }

  saveDisplayName(account: AccessAccount): void {
    const displayName = this.displayDraft(account).trim();
    if (!displayName) return;
    this.runAction(() => this.api.updateAccessAccount(account.id, { display_name: displayName }));
  }

  rotatePassword(account: AccessAccount): void {
    this.runAction(() => this.api.rotateAccessPassword(account.id), (updated) => this.showSecret(updated.secret));
  }

  changeSchema(account: AccessAccount, database: string): void {
    const current = account.bindings.find((binding) => binding.database === database);
    const schema = this.schemaDraft(account.id, current?.schema ?? "").trim();
    if (!schema || schema === current?.schema) return;
    this.runAction(() => this.api.changeAccessSchema(account.id, { database, schema_name: schema }));
  }

  schemaDraft(accountId: string, fallback: string): string {
    return this.schemaDrafts.get(accountId) ?? fallback;
  }

  setSchemaDraft(accountId: string, value: string): void { this.schemaDrafts.set(accountId, value); }

  displayDraft(account: AccessAccount): string { return this.displayDrafts.get(account.id) ?? account.displayName ?? ""; }

  setDisplayDraft(accountId: string, value: string): void { this.displayDrafts.set(accountId, value); }

  formatDate(value: string): string {
    return new Intl.DateTimeFormat("vi-VN", { dateStyle: "short", timeStyle: "short" }).format(new Date(value));
  }

  copySecret(): void {
    if (!this.secret()) return;
    void navigator.clipboard?.writeText(this.secret() ?? "");
    this.copied.set(true);
  }

  private showSecret(value: string | undefined): void {
    this.secret.set(value ?? null);
    this.copied.set(false);
  }

  private runAction(
    action: () => Observable<AccessAccount>,
    after?: (value: AccessAccount) => void,
  ): void {
    this.busy.set(true);
    this.errorMessage.set(null);
    action().subscribe({
      next: (value) => { after?.(value); this.busy.set(false); this.load(); },
      error: (error: unknown) => { this.busy.set(false); this.setError(error, "Access operation failed."); },
    });
  }

  private setError(error: unknown, fallback: string): void {
    this.errorMessage.set(error instanceof AdminApiError ? error.message || fallback : fallback);
  }
}
