import { Component, inject } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { Router } from "@angular/router";

import { AuthService } from "../../core/auth.service";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
  template: `
    <main class="login-page">
      <section class="login-card">
        <div class="login-brand"><div class="brand-mark large"><mat-icon>data_object</mat-icon></div><span>Neon Admin</span></div>
        <p class="eyebrow">Protected workspace</p>
        <h1>Manage your database with confidence.</h1>
        <p class="login-copy">Inspect PostgreSQL metadata, edit table data, and run controlled SQL from one focused control plane.</p>
        @if (auth.isLocalDevAccess) {
          <div class="dev-notice"><mat-icon>construction</mat-icon><div><strong>Local development access enabled</strong><span>The local UI bypass is enabled; configure the API with DB_ADMIN_DEV_AUTH too. No login token is stored.</span></div></div>
          <button mat-flat-button color="primary" class="login-action" (click)="enter()">Enter local workspace <mat-icon>arrow_forward</mat-icon></button>
        } @else {
          <button mat-flat-button color="primary" class="login-action" (click)="auth.login()">Continue with Identity <mat-icon>arrow_forward</mat-icon></button>
        }
        <div class="security-note"><mat-icon>lock</mat-icon><span>Database credentials remain on the API server.</span></div>
      </section>
      <div class="login-visual"><div class="grid-glow"></div><div class="terminal-card"><div class="terminal-head"><span></span><span></span><span></span><small>neon-prod / public</small></div><div class="terminal-line"><b>SELECT</b> schema_name, table_name</div><div class="terminal-line muted">FROM information_schema.tables</div><div class="terminal-line result">✓ 16 objects loaded in 42ms</div></div></div>
    </main>
  `,
})
export class LoginPageComponent {
  readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  enter(): void {
    void this.router.navigateByUrl("/dashboard");
  }
}
