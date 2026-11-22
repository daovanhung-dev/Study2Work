import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink, type ParamMap } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { take } from 'rxjs';

import { AD02ApiService } from '../data-access/ad02-api.service';
import { AD02CreateUserDialog } from '../ui/ad02-create-user-dialog';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD02_SCREEN_MODEL } from '../models/ad02-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAdminPageCountMismatch, isAdminUserPage, isAdminUserProfile } from '../../admin-api-guards';
import { renderUserRow } from '../../admin-screen-renderers';
import type { AdminCreateUserRequest } from '../../admin-api.models';

interface AD02UsersQuery {
  keyword: string;
  role: string;
  status: string;
  page: number;
}

@Component({
  imports: [AD02CreateUserDialog, RouterLink, StudyIcon],
  selector: 'study-ad02-page',
  styleUrl: './ad02-page.css',
  templateUrl: './ad02-page.html',
})
export class AD02Page {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(AD02ApiService);
  @ViewChild('addUserButton') private addUserButton?: ElementRef<HTMLButtonElement>;
  readonly screenModel = AD02_SCREEN_MODEL;
  readonly columns = AD02_SCREEN_MODEL.columns;
  readonly query = signal<AD02UsersQuery>(queryFromParamMap(this.route.snapshot.queryParamMap));
  readonly snapshotMismatch = signal(false);
  readonly pageOutOfRange = signal(false);
  readonly createDialogOpen = signal(false);
  readonly createPending = signal(false);
  readonly createError = signal('');
  readonly createSuccess = signal('');
  readonly filters = signal(filtersFromQuery(this.query()));
  readonly activeFilters = computed(() => {
    const query = this.query();
    return [
      { label: 'Từ khóa', value: query.keyword },
      { label: 'Vai trò', value: query.role },
      { label: 'Trạng thái', value: query.status },
    ].filter((filter) => filter.value !== '');
  });
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getUsers(query),
    (page) => {
      if (!isAdminUserPage(page, this.query().page)) {
        this.clearPageFlags();
        return { status: 'error', message: 'API #68 trả về trang người dùng không hợp lệ.' };
      }

      const isOutOfRange = page.items.length === 0
        && page.pagination.page > Math.max(page.pagination.total_pages, 1);
      this.pageOutOfRange.set(isOutOfRange);
      this.snapshotMismatch.set(!isOutOfRange && hasAdminPageCountMismatch(page));
      return loadedRows(page.items.map(renderUserRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );
  readonly isFilterError = computed(() => {
    const state = this.viewState();
    return state.status === 'error' && state.httpStatus === 422;
  });

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      const nextQuery = queryFromParamMap(params);
      if (sameQuery(this.query(), nextQuery)) {
        return;
      }
      this.clearPageFlags();
      this.filters.set(filtersFromQuery(nextQuery));
      this.query.set(nextQuery);
    });
  }

  setFilter(key: 'keyword' | 'role' | 'status', value: string): void {
    this.filters.update((current) => ({ ...current, [key]: value }));
  }

  applyFilters(event: Event): void {
    event.preventDefault();
    this.navigateQuery({ ...this.filters(), page: 1 });
  }

  clearFilters(): void {
    this.navigateQuery({ keyword: '', role: '', status: '', page: 1 });
  }

  openCreateDialog(): void {
    if (this.createPending()) return;
    this.createError.set('');
    this.createSuccess.set('');
    this.createDialogOpen.set(true);
  }

  closeCreateDialog(): void {
    if (this.createPending()) return;
    this.createDialogOpen.set(false);
    queueMicrotask(() => this.addUserButton?.nativeElement.focus());
  }

  clearCreateError(): void {
    if (this.createError()) this.createError.set('');
  }

  createUser(request: AdminCreateUserRequest): void {
    if (this.createPending()) return;
    this.createError.set('');
    this.createPending.set(true);
    this.api.createUser(request).pipe(take(1)).subscribe({
      next: (envelope) => {
        const user = envelope.data;
        if (
          envelope.success !== true
          || envelope.businessCode !== 'DESIGN_RESOURCE_CREATED'
          || !isAdminUserProfile(user)
          || user.full_name !== request.full_name.trim()
          || user.role !== request.role
          || user.status !== 'ACTIVE'
        ) {
          this.createPending.set(false);
          this.createError.set(
            'Study Server đã phản hồi nhưng hồ sơ tài khoản không hợp lệ. Hãy tải lại danh sách trước khi gửi lại.',
          );
          return;
        }

        this.createPending.set(false);
        this.createDialogOpen.set(false);
        this.createSuccess.set('Tài khoản đã được tạo. Danh sách đang được cập nhật.');
        this.clearPageFlags();
        this.query.update((current) => ({ ...current }));
        queueMicrotask(() => this.addUserButton?.nativeElement.focus());
      },
      error: (error: unknown) => {
        this.createPending.set(false);
        this.createError.set(createUserErrorMessage(error));
      },
    });
  }

  refreshList(): void {
    if (this.viewState().status === 'loading') {
      return;
    }
    this.clearPageFlags();
    this.query.update((current) => ({ ...current }));
  }

  changePage(page: number): void {
    if (this.snapshotMismatch() || this.pageOutOfRange()) return;
    const pagination = this.viewState().pagination;
    if (!pagination || !Number.isSafeInteger(page) || page < 1 || page > pagination.totalPages) return;
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { page },
      queryParamsHandling: 'merge',
    });
  }

  resetPageToFirst(): void {
    this.navigateQuery({ ...this.query(), page: 1 });
  }

  private navigateQuery(query: AD02UsersQuery): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        keyword: query.keyword || null,
        role: query.role || null,
        status: query.status || null,
        page: query.page,
      },
      queryParamsHandling: 'merge',
    });
  }

  returnToFirstPage(): void {
    if (!this.pageOutOfRange() && !this.snapshotMismatch()) return;
    this.navigateQuery({ ...this.query(), page: 1 });
  }

  private clearPageFlags(): void {
    this.snapshotMismatch.set(false);
    this.pageOutOfRange.set(false);
  }

  get queryStateMessage(): string {
    const state = this.viewState();
    if (state.status === 'loading') {
      return 'Đang tải danh sách người dùng.';
    }
    if (state.status === 'error') {
      if (state.httpStatus === 422) {
        return 'Tham số trang không hợp lệ. Hãy đưa danh sách về trang 1 để tiếp tục.';
      }
      return state.message ?? 'Không thể tải danh sách người dùng.';
    }
    return 'Danh sách người dùng đã được tải.';
  }
}

function createUserErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) {
    return 'Không thể tạo tài khoản lúc này. Vui lòng thử lại.';
  }
  if (error.status === 401) return 'Phiên Admin không còn hiệu lực. Hãy đăng nhập lại.';
  if (error.status === 403) return 'Tài khoản hiện tại không được phép tạo người dùng.';
  if (error.status === 409) return 'Email này đã được sử dụng. Hãy nhập email khác.';
  if (error.status === 422) {
    return 'Thông tin chưa hợp lệ. Hãy kiểm tra họ tên, email, mật khẩu và vai trò.';
  }
  return 'Không thể tạo tài khoản lúc này. Vui lòng thử lại.';
}

function queryFromParamMap(params: ParamMap): AD02UsersQuery {
  return {
    keyword: params.get('keyword') ?? '',
    role: params.get('role') ?? '',
    status: params.get('status') ?? '',
    page: params.has('page') ? Number(params.get('page')) : 1,
  };
}

function filtersFromQuery(query: AD02UsersQuery): Omit<AD02UsersQuery, 'page'> {
  return { keyword: query.keyword, role: query.role, status: query.status };
}

function sameQuery(first: AD02UsersQuery, second: AD02UsersQuery): boolean {
  return (
    first.keyword === second.keyword &&
    first.role === second.role &&
    first.status === second.status &&
    Object.is(first.page, second.page)
  );
}
