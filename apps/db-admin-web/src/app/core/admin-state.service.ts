import { Injectable, signal } from "@angular/core";

import { AdminApiError, ApiService } from "./api.service";
import { ApiErrorInfo, CatalogData, DatabaseTarget } from "./models";

@Injectable({ providedIn: "root" })
export class AdminStateService {
  readonly databases = signal<DatabaseTarget[]>([]);
  readonly selectedDatabase = signal<string | null>(null);
  readonly selectedSchema = signal<string | null>(null);
  readonly catalog = signal<CatalogData | null>(null);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly errorInfo = signal<ApiErrorInfo | null>(null);
  readonly databasesLoading = signal(false);
  readonly catalogLoading = signal(false);
  private loadVersion = 0;

  constructor(private readonly api: ApiService) {}

  loadDatabases(): void {
    this.databasesLoading.set(true);
    this.loading.set(true);
    this.clearError();
    this.api.getDatabases().subscribe({
      next: (result) => {
        this.databases.set(result.databases);
        this.databasesLoading.set(false);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.setError(error, "Không thể tải danh sách database.");
        this.databasesLoading.set(false);
        this.loading.set(false);
      },
    });
  }

  selectDatabase(database: string | null): void {
    this.loadVersion += 1;
    this.selectedDatabase.set(database);
    this.selectedSchema.set(null);
    this.catalog.set(null);
    this.clearError();
    this.loading.set(false);
    this.catalogLoading.set(false);
    if (database) this.load(database);
  }

  selectSchema(schema: string | null): void {
    this.selectedSchema.set(schema);
  }

  load(database = this.selectedDatabase()): void {
    if (!database) return;
    const version = ++this.loadVersion;
    this.catalogLoading.set(true);
    this.loading.set(true);
    this.clearError();
    this.api.getCatalog(database).subscribe({
      next: (catalog) => {
        if (version !== this.loadVersion || this.selectedDatabase() !== database) return;
        this.catalog.set(catalog);
        this.catalogLoading.set(false);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        if (version !== this.loadVersion || this.selectedDatabase() !== database) return;
        this.setError(error, "Không thể tải database catalog.");
        this.catalogLoading.set(false);
        this.loading.set(false);
      },
    });
  }

  private clearError(): void {
    this.error.set(null);
    this.errorInfo.set(null);
  }

  private setError(error: unknown, fallback: string): void {
    const info: ApiErrorInfo = error instanceof AdminApiError
      ? { message: error.message || fallback, businessCode: error.businessCode, traceId: error.traceId }
      : { message: error instanceof Error ? error.message || fallback : fallback };
    this.error.set(info.message);
    this.errorInfo.set(info);
  }
}
