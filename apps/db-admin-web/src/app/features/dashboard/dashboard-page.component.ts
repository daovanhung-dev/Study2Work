import { Component, OnInit, inject } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { RouterLink } from "@angular/router";

import { ApiService } from "../../core/api.service";
import { AdminStateService } from "../../core/admin-state.service";
import { AuthService } from "../../core/auth.service";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule, MatProgressSpinnerModule, RouterLink],
  template: `
    <section class="page-header">
      <div><p class="eyebrow">Operations overview</p><h1>Database workspace</h1><p class="lede">A clean view of the Neon database that powers Study2Work.</p></div>
      @if (auth.can('db_admin:sql')) { <a mat-flat-button color="primary" routerLink="/sql"><mat-icon>terminal</mat-icon> Open SQL editor</a> }
    </section>
    @if (state.loading()) { <div class="loading-state"><mat-spinner diameter="32"></mat-spinner><span>Reading database catalog…</span></div> }
    @if (state.error()) { <div class="error-banner"><mat-icon>error_outline</mat-icon><span>{{ state.error() }}</span><button mat-button (click)="load()">Retry</button></div> }
    <div class="stat-grid">
      @for (stat of stats; track stat.label) { <mat-card class="stat-card"><div class="stat-icon" [class]="stat.tone"><mat-icon>{{ stat.icon }}</mat-icon></div><div><span>{{ stat.label }}</span><strong>{{ stat.value() }}</strong></div></mat-card> }
    </div>
    <div class="dashboard-grid">
      <mat-card class="panel-card connection-card"><div class="card-heading"><div><p class="eyebrow">Target connection</p><h2>Neon PostgreSQL</h2></div><span class="healthy-badge"><span class="status-dot"></span> Ready</span></div>
        @if (connection) { <div class="connection-details"><div><span>Database</span><strong>{{ connection.database }}</strong></div><div><span>Role</span><strong>{{ connection.user }}</strong></div><div><span>Schema</span><strong>{{ connection.schema }}</strong></div></div><p class="server-version">{{ connection.serverVersion }}</p> } @else { <button mat-stroked-button (click)="loadConnection()">Check connection</button> }
      </mat-card>
      <mat-card class="panel-card quick-card"><div class="card-heading"><div><p class="eyebrow">Quick actions</p><h2>Work faster</h2></div><mat-icon>bolt</mat-icon></div><div class="quick-actions"><a routerLink="/catalog"><mat-icon>account_tree</mat-icon><span><strong>Explore catalog</strong><small>Browse schemas and objects</small></span><mat-icon>arrow_forward</mat-icon></a>@if (auth.can('db_admin:sql')) { <a routerLink="/sql"><mat-icon>code</mat-icon><span><strong>Run a query</strong><small>Inspect data with SQL</small></span><mat-icon>arrow_forward</mat-icon></a> }</div></mat-card>
    </div>
    <mat-card class="panel-card principles-card"><div class="card-heading"><div><p class="eyebrow">Guardrails</p><h2>Built for safe operations</h2></div></div><div class="principles"><div><mat-icon>verified_user</mat-icon><span><strong>Server-side permissions</strong><small>RBAC is enforced before every database action.</small></span></div><div><mat-icon>preview</mat-icon><span><strong>Preview before commit</strong><small>DDL and mutation SQL require explicit confirmation.</small></span></div><div><mat-icon>history</mat-icon><span><strong>Audit visibility</strong><small>Every admin action is captured with a trace ID.</small></span></div></div></mat-card>
  `,
})
export class DashboardPageComponent implements OnInit {
  readonly state = inject(AdminStateService);
  readonly auth = inject(AuthService);
  private readonly api = inject(ApiService);
  connection?: { database: string; user: string; schema: string; serverVersion: string };
  readonly stats = [
    { label: "Schemas", icon: "account_tree", tone: "violet", value: () => this.state.catalog()?.schemas.length ?? 0 },
    { label: "Tables", icon: "table_chart", tone: "blue", value: () => this.state.catalog()?.tables.length ?? 0 },
    { label: "Views", icon: "visibility", tone: "amber", value: () => this.state.catalog()?.views.length ?? 0 },
    { label: "Routines", icon: "functions", tone: "green", value: () => this.state.catalog()?.routines.length ?? 0 },
  ];

  ngOnInit(): void { this.load(); this.loadConnection(); }
  load(): void { this.state.load(); }
  loadConnection(): void { this.api.getConnection().subscribe({ next: (value) => this.connection = value, error: () => this.connection = undefined }); }
}
