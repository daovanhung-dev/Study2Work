import { Component, inject } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatListModule } from "@angular/material/list";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatToolbarModule } from "@angular/material/toolbar";
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from "@angular/router";

import { AuthService } from "./auth.service";
import { Permission } from "./models";

interface NavItem {
  label: string;
  icon: string;
  route: string;
  permission: Permission;
}

@Component({
  selector: "db-shell",
  standalone: true,
  imports: [
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatSidenavModule,
    MatToolbarModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
  ],
  template: `
    <mat-sidenav-container class="shell-container">
      <mat-sidenav #drawer class="shell-sidenav" mode="side" opened>
        <div class="brand-lockup">
          <div class="brand-mark"><mat-icon>data_object</mat-icon></div>
          <div>
            <strong>Neon Admin</strong>
            <span>Database control plane</span>
          </div>
        </div>
        <div class="nav-section-label">Workspace</div>
        <mat-nav-list>
          @for (item of visibleNavItems; track item.route) {
            <a mat-list-item [routerLink]="item.route" routerLinkActive="nav-active" #active="routerLinkActive" [activated]="active.isActive">
              <mat-icon matListItemIcon>{{ item.icon }}</mat-icon>
              <span matListItemTitle>{{ item.label }}</span>
            </a>
          }
        </mat-nav-list>
        <div class="sidenav-bottom">
          <div class="connection-mini"><span class="status-dot"></span><span>Neon target</span><small>configured server-side</small></div>
          <button mat-stroked-button class="logout-button" (click)="logout()"><mat-icon>logout</mat-icon> Sign out</button>
        </div>
      </mat-sidenav>
      <mat-sidenav-content>
        <mat-toolbar class="topbar">
          <button mat-icon-button class="mobile-menu" (click)="drawer.toggle()" aria-label="Open navigation"><mat-icon>menu</mat-icon></button>
          <div class="breadcrumb"><span>Control plane</span><mat-icon>chevron_right</mat-icon><strong>Database</strong></div>
          <span class="toolbar-spacer"></span>
          <span class="role-pill"><mat-icon>shield</mat-icon>{{ auth.isLocalDevAccess ? 'LOCAL ADMIN' : 'DB ADMIN' }}</span>
          <button mat-icon-button aria-label="Refresh workspace" (click)="refresh()"><mat-icon>refresh</mat-icon></button>
        </mat-toolbar>
        <main class="page-canvas"><router-outlet /></main>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
})
export class ShellComponent {
  readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  readonly navItems: NavItem[] = [
    { label: "Overview", icon: "dashboard", route: "/dashboard", permission: "db_admin:read" },
    { label: "Schema explorer", icon: "account_tree", route: "/catalog", permission: "db_admin:read" },
    { label: "SQL editor", icon: "terminal", route: "/sql", permission: "db_admin:sql" },
    { label: "Audit trail", icon: "history", route: "/audit", permission: "db_admin:read" },
  ];
  get visibleNavItems(): NavItem[] { return this.navItems.filter((item) => this.auth.can(item.permission)); }

  logout(): void {
    this.auth.logout();
    void this.router.navigateByUrl("/login");
  }

  refresh(): void {
    window.location.reload();
  }
}
