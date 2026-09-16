import { Component, OnInit, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatSelectModule } from "@angular/material/select";
import { MatToolbarModule } from "@angular/material/toolbar";
import { Router, RouterOutlet } from "@angular/router";

import { AdminStateService } from "./admin-state.service";
import { AuthService } from "./auth.service";
import { AccessDrawerComponent } from "../features/access/access-drawer.component";

@Component({
  selector: "db-shell",
  standalone: true,
  imports: [
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatToolbarModule,
    RouterOutlet,
    AccessDrawerComponent,
  ],
  template: `
    <mat-toolbar class="topbar">
      <div class="shell-brand">
        <span class="brand-mark"><mat-icon>data_object</mat-icon></span>
        <div><strong>DB Admin</strong><span>test · debug · coding</span></div>
      </div>
      <div class="topbar-context" aria-label="Database context">
        <mat-form-field class="topbar-select" appearance="outline" subscriptSizing="dynamic">
          <mat-label>Database</mat-label>
          <mat-select [value]="state.selectedDatabase() ?? ''" (valueChange)="chooseDatabase($event)">
            <mat-option value="">Choose database</mat-option>
            @for (database of state.databases(); track database.id) {
              <mat-option [value]="database.id">{{ database.label }}</mat-option>
            }
          </mat-select>
        </mat-form-field>
        <mat-form-field class="topbar-select" appearance="outline" subscriptSizing="dynamic">
          <mat-label>Schema</mat-label>
          <mat-select [value]="state.selectedSchema() ?? ''" [disabled]="!state.catalog()" (valueChange)="chooseSchema($event)">
            <mat-option value="">Choose schema</mat-option>
            @for (schema of schemaNames(); track schema) {
              <mat-option [value]="schema">{{ schema }}</mat-option>
            }
          </mat-select>
        </mat-form-field>
      </div>
      <span class="toolbar-spacer"></span>
      <span class="topbar-status" [class.ready]="state.selectedSchema()" [class.loading]="state.loading()">
        @if (state.loading()) { <mat-spinner diameter="14"></mat-spinner> }
        @else { <span class="status-dot"></span> }
        {{ statusLabel() }}
      </span>
      @if (auth.isRoot()) { <button mat-stroked-button class="manage-button" (click)="accessOpen.set(true)"><mat-icon>admin_panel_settings</mat-icon> Manage access</button> }
      <span class="role-pill"><mat-icon>shield</mat-icon>{{ auth.isRoot() ? 'ROOT' : 'DEVELOPER' }}</span>
      <button mat-icon-button aria-label="Refresh catalog" [disabled]="state.loading()" (click)="refresh()"><mat-icon>refresh</mat-icon></button>
      <button mat-stroked-button class="logout-button" (click)="logout()"><mat-icon>logout</mat-icon> Sign out</button>
    </mat-toolbar>
    <main class="page-canvas"><router-outlet /></main>
    <db-access-drawer [open]="accessOpen()" (closed)="accessOpen.set(false)" />
  `,
})
export class ShellComponent implements OnInit {
  readonly auth = inject(AuthService);
  readonly state = inject(AdminStateService);
  private readonly router = inject(Router);
  readonly accessOpen = signal(false);

  ngOnInit(): void { this.state.loadDatabases(); }

  schemaNames(): string[] {
    return (this.state.catalog()?.schemas ?? [])
      .map((schema) => schema.name)
      .filter((name): name is string => typeof name === "string");
  }

  chooseDatabase(database: string): void { this.state.selectDatabase(database || null); }
  chooseSchema(schema: string): void { this.state.selectSchema(schema || null); }

  statusLabel(): string {
    if (this.state.databasesLoading()) return "Loading targets";
    if (this.state.catalogLoading()) return "Loading catalog";
    if (this.state.selectedSchema()) return "Ready";
    if (this.state.selectedDatabase()) return "Choose schema";
    return "No target selected";
  }

  logout(): void {
    this.auth.logout();
    void this.router.navigateByUrl("/login");
  }

  refresh(): void {
    if (this.state.selectedDatabase()) this.state.load();
    else this.state.loadDatabases();
  }
}
