import { Component, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { Router } from "@angular/router";

import { AdminApiError } from "../../core/api.service";
import { AuthService } from "../../core/auth.service";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatIconModule, MatProgressSpinnerModule],
  template: `
    <main class="login-page">
      <section class="login-card">
        <div class="login-brand"><div class="brand-mark large"><mat-icon>data_object</mat-icon></div><span>Neon Admin</span></div>
        <p class="eyebrow">Protected workspace</p>
        @if (auth.mustChangePassword() && auth.token()) {
          <h1>Set a new password.</h1>
          <p class="login-copy">This temporary secret can only be used once. Choose a new password before opening the workspace.</p>
          <form class="login-form" (submit)="submitChangePassword($event)">
            <label><span>Current password</span><input type="password" name="currentPassword" autocomplete="current-password" [value]="currentPassword" (input)="currentPassword = inputValue($event)" /></label>
            <label><span>New password</span><input type="password" name="newPassword" autocomplete="new-password" [value]="newPassword" (input)="newPassword = inputValue($event)" /></label>
            <label><span>Confirm new password</span><input type="password" name="confirmPassword" autocomplete="new-password" [value]="confirmPassword" (input)="confirmPassword = inputValue($event)" /></label>
            @if (errorMessage()) { <div class="login-error"><mat-icon>error_outline</mat-icon><span>{{ errorMessage() }}</span></div> }
            <button mat-flat-button color="primary" class="login-action" type="submit" [disabled]="busy()">@if (busy()) { <mat-spinner diameter="17"></mat-spinner> } @else { <mat-icon>lock_reset</mat-icon> } Change password</button>
          </form>
        } @else {
          <h1>Manage your database with confidence.</h1>
          <p class="login-copy">Inspect PostgreSQL metadata and run controlled SQL from one focused control plane.</p>
          @if (auth.localAuthEnabled) {
            <form class="login-form" (submit)="submitLogin($event)">
              <label><span>Username</span><input name="username" autocomplete="username" placeholder="admin" [value]="username" (input)="username = inputValue($event)" /></label>
              <label><span>Password</span><input type="password" name="password" autocomplete="current-password" [value]="password" (input)="password = inputValue($event)" /></label>
              @if (errorMessage()) { <div class="login-error"><mat-icon>error_outline</mat-icon><span>{{ errorMessage() }}</span></div> }
              <button mat-flat-button color="primary" class="login-action" type="submit" [disabled]="busy() || !username.trim() || !password">@if (busy()) { <mat-spinner diameter="17"></mat-spinner> } @else { <mat-icon>arrow_forward</mat-icon> } Sign in</button>
            </form>
            <p class="login-hint">Local account authentication · session stays in memory for this tab.</p>
          } @else if (auth.isLocalDevAccess) {
            <div class="dev-notice"><mat-icon>construction</mat-icon><div><strong>Local development access enabled</strong><span>The bypass is intended for isolated tests only.</span></div></div>
            <button mat-flat-button color="primary" class="login-action" (click)="enter()">Enter local workspace <mat-icon>arrow_forward</mat-icon></button>
          } @else {
            <button mat-flat-button color="primary" class="login-action" (click)="auth.login()">Continue with Identity <mat-icon>arrow_forward</mat-icon></button>
          }
        }
        <div class="security-note"><mat-icon>lock</mat-icon><span>Database credentials remain on the API server.</span></div>
      </section>
      <div class="login-visual"><div class="grid-glow"></div><div class="terminal-card"><div class="terminal-head"><span></span><span></span><span></span><small>neon-prod / db_admin</small></div><div class="terminal-line"><b>SELECT</b> schema_name, table_name</div><div class="terminal-line muted">FROM information_schema.tables</div><div class="terminal-line result">✓ control plane ready for review</div></div></div>
    </main>
  `,
})
export class LoginPageComponent {
  readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  readonly busy = signal(false);
  readonly errorMessage = signal<string | null>(null);
  username = "";
  password = "";
  currentPassword = "";
  newPassword = "";
  confirmPassword = "";

  inputValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

  submitLogin(event: Event): void {
    event.preventDefault();
    if (!this.username.trim() || !this.password) return;
    this.busy.set(true);
    this.errorMessage.set(null);
    this.auth.loginLocal(this.username, this.password).subscribe({
      next: (session) => {
        this.busy.set(false);
        if (session.mustChangePassword) {
          this.currentPassword = this.password;
          this.password = "";
          return;
        }
        void this.router.navigateByUrl("/");
      },
      error: (error: unknown) => {
        this.busy.set(false);
        this.setError(error, "Sign in failed. Check the account details and try again.");
      },
    });
  }

  submitChangePassword(event: Event): void {
    event.preventDefault();
    if (!this.currentPassword || this.newPassword.length < 12) {
      this.errorMessage.set("New password must contain at least 12 characters.");
      return;
    }
    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage.set("The new password confirmation does not match.");
      return;
    }
    this.busy.set(true);
    this.errorMessage.set(null);
    this.auth.changePassword(this.currentPassword, this.newPassword).subscribe({
      next: () => { this.busy.set(false); void this.router.navigateByUrl("/"); },
      error: (error: unknown) => { this.busy.set(false); this.setError(error, "Password change failed."); },
    });
  }

  enter(): void { void this.router.navigateByUrl("/"); }

  private setError(error: unknown, fallback: string): void {
    this.errorMessage.set(error instanceof AdminApiError ? error.message || fallback : fallback);
  }
}
