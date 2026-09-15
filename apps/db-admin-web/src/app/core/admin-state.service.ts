import { Injectable, signal } from "@angular/core";

import { ApiService } from "./api.service";
import { CatalogData } from "./models";

@Injectable({ providedIn: "root" })
export class AdminStateService {
  readonly catalog = signal<CatalogData | null>(null);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  constructor(private readonly api: ApiService) {}

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.api.getCatalog().subscribe({
      next: (catalog) => { this.catalog.set(catalog); this.loading.set(false); },
      error: (error: Error) => { this.error.set(error.message || "Không thể tải database catalog."); this.loading.set(false); },
    });
  }
}
