import { Component, OnInit, inject, signal } from "@angular/core";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";

import { ApiService } from "../../core/api.service";
import { AuditEntry } from "../../core/models";

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule],
  template: `
    <section class="page-header"><div><p class="eyebrow">Accountability</p><h1>Audit trail</h1><p class="lede">A local, bounded history of database administration actions. Raw SQL is represented by a hash, never logged in plain text.</p></div><button mat-flat-button color="primary" (click)="load()"><mat-icon>refresh</mat-icon> Refresh audit</button></section>
    @if (error()) { <div class="error-banner"><mat-icon>error_outline</mat-icon><span>{{ error() }}</span></div> }
    <mat-card class="panel-card audit-card"><div class="audit-head"><div><p class="eyebrow">Recent activity</p><h2>{{ entries().length }} events</h2></div><span class="retention-note"><mat-icon>info</mat-icon> In-memory local retention</span></div>@if (entries().length) { <div class="audit-list">@for (entry of entries(); track entry.timestamp + entry.traceId) { <div class="audit-row"><span class="audit-icon" [class.failed]="entry.outcome !== 'success'"><mat-icon>{{ entry.outcome === 'success' ? 'check' : 'error_outline' }}</mat-icon></span><div class="audit-main"><strong>{{ entry.action }}</strong><span>{{ entry.target }} · {{ entry.actor }}</span></div><div class="audit-meta"><span>{{ formatDate(entry.timestamp) }}</span><code>{{ entry.sqlHash ? entry.sqlHash.slice(0, 12) : entry.traceId.slice(0, 12) }}</code></div></div> }</div> } @else { <div class="empty-state small"><mat-icon>history</mat-icon><h2>No audit events yet</h2><p>DDL, row mutations and SQL executions will appear here.</p></div> }</mat-card>
  `,
})
export class AuditPageComponent implements OnInit {
  private readonly api = inject(ApiService);
  readonly entries = signal<AuditEntry[]>([]);
  readonly error = signal<string | null>(null);
  ngOnInit(): void { this.load(); }
  load(): void { this.error.set(null); this.api.getAudit().subscribe({ next: (value) => this.entries.set(value.entries), error: (error: Error) => this.error.set(error.message) }); }
  formatDate(value: string): string { return new Intl.DateTimeFormat("vi-VN", { dateStyle: "short", timeStyle: "medium" }).format(new Date(value)); }
}
