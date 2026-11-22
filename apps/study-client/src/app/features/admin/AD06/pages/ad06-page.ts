import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { take } from 'rxjs';

import { AD06ApiService } from '../data-access/ad06-api.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD06_SCREEN } from '../models/ad06-screen.model';
import { adminQueryState, loadedRows } from '../../admin-screen-state';
import { hasAdminPageCountMismatch, isAdminCourse, isAdminCoursePage, isAdminUserPage } from '../../admin-api-guards';
import { renderCourseRow } from '../../admin-screen-renderers';
import type { AdminCourseCreateRequest, AdminUserProfile } from '../../admin-api.models';

interface AD06Query {
  page: number;
}

@Component({
  imports: [FormsModule, RouterLink, StudyIcon],
  selector: 'study-ad06-page',
  templateUrl: './ad06-page.html',
})
export class AD06Page {
  readonly definition = AD06_SCREEN;
  private readonly api = inject(AD06ApiService);
  private readonly router = inject(Router);
  @ViewChild('createDialog') private createDialog?: ElementRef<HTMLDialogElement>;
  @ViewChild('createCourseFormElement') private createCourseFormElement?: ElementRef<HTMLFormElement>;
  @ViewChild('createTitle') private createTitle?: ElementRef<HTMLInputElement>;
  @ViewChild('addCourseButton') private addCourseButton?: ElementRef<HTMLButtonElement>;
  readonly query = signal<AD06Query>({ page: 1 });
  readonly snapshotMismatch = signal(false);
  readonly mentors = signal<readonly AdminUserProfile[]>([]);
  readonly mentorsLoading = signal(false);
  readonly mentorsError = signal('');
  readonly mentorPage = signal(0);
  readonly mentorTotalPages = signal(0);
  readonly createPending = signal(false);
  readonly createError = signal('');
  readonly createSuccess = signal('');
  createForm = emptyCreateForm();
  readonly viewState = adminQueryState(
    this.query,
    (query) => this.api.getCourses(query),
    (page) => {
      if (!isAdminCoursePage(page, this.query().page)) {
        this.snapshotMismatch.set(false);
        return { status: 'error', message: 'API #73 trả về trang khóa học không hợp lệ.' };
      }

      this.snapshotMismatch.set(hasAdminPageCountMismatch(page));
      return loadedRows(page.items.map(renderCourseRow), {
        page: page.pagination.page,
        total: page.pagination.total,
        totalPages: page.pagination.total_pages,
        size: page.pagination.size,
      });
    },
    'DESIGN_RESOURCE_RETRIEVED',
  );

  get totalCount(): string {
    if (this.snapshotMismatch() || this.isOutOfRange) return '—';
    const total = this.viewState().pagination?.total;
    if (total === undefined) {
      return '—';
    }
    return Number.isSafeInteger(total) && total >= 0
      ? total.toLocaleString('vi-VN')
      : 'Không thể hiển thị chính xác';
  }

  get pageCount(): string {
    if (this.snapshotMismatch() || this.isOutOfRange) return '—';
    const pagination = this.viewState().pagination;
    if (!pagination || pagination.totalPages <= 0) {
      return '—';
    }
    if (!Number.isSafeInteger(pagination.page) || pagination.page < 1) {
      return 'Không thể hiển thị chính xác';
    }
    return Number.isSafeInteger(pagination.totalPages)
      ? `${pagination.page} / ${pagination.totalPages}`
      : `${pagination.page} / Không thể hiển thị chính xác`;
  }

  get currentResultCount(): string {
    return this.viewState().status === 'loaded'
      ? String(this.viewState().rows?.length ?? 0)
      : '—';
  }

  get pageSize(): string {
    const pagination = this.viewState().pagination;
    return pagination ? String(pagination.size ?? '—') : '—';
  }

  get isOutOfRange(): boolean {
    const state = this.viewState();
    const pagination = state.pagination;
    return state.status === 'loaded'
      && (state.rows?.length ?? 0) === 0
      && !!pagination
      && Number.isSafeInteger(pagination.total)
      && pagination.page > Math.max(pagination.totalPages, 1);
  }

  get isEmpty(): boolean {
    const state = this.viewState();
    return state.status === 'loaded'
      && !this.snapshotMismatch()
      && !this.isOutOfRange
      && (state.rows?.length ?? 0) === 0
      && (state.pagination?.total ?? 0) === 0;
  }

  get hasMoreMentors(): boolean {
    return this.mentorPage() > 0 && this.mentorPage() < this.mentorTotalPages();
  }

  get previousDisabled(): boolean {
    const state = this.viewState();
    return this.snapshotMismatch() || this.isOutOfRange
      || state.status !== 'loaded' || !state.pagination || state.pagination.page <= 1;
  }

  get nextDisabled(): boolean {
    const state = this.viewState();
    return this.snapshotMismatch() || this.isOutOfRange
      || state.status !== 'loaded' || !state.pagination
      || state.pagination.totalPages === 0
      || state.pagination.page >= state.pagination.totalPages;
  }

  changePage(page: number): void {
    if (this.snapshotMismatch() || this.isOutOfRange) return;
    const pagination = this.viewState().pagination;
    if (this.viewState().status !== 'loaded' || !pagination || !Number.isSafeInteger(page)
      || page < 1 || page > pagination.totalPages) {
      return;
    }
    this.snapshotMismatch.set(false);
    this.query.set({ page });
  }

  refreshCourses(): void {
    this.snapshotMismatch.set(false);
    this.query.update((query) => ({ ...query }));
  }

  returnToFirstPage(): void {
    if (!this.isOutOfRange) return;
    this.snapshotMismatch.set(false);
    this.query.set({ page: 1 });
  }

  openCreateDialog(): void {
    if (this.createPending()) return;
    this.createForm = emptyCreateForm();
    this.createError.set('');
    this.createSuccess.set('');
    const dialog = this.createDialog?.nativeElement;
    if (!dialog) return;
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
    } else {
      dialog.setAttribute('open', '');
    }
    this.loadMentors(1);
    queueMicrotask(() => this.createTitle?.nativeElement.focus());
  }

  closeCreateDialog(): void {
    if (this.createPending()) return;
    const dialog = this.createDialog?.nativeElement;
    if (dialog?.open) {
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
    }
    this.restoreCreateButtonFocus();
  }

  handleCreateDialogCancel(event: Event): void {
    if (this.createPending()) event.preventDefault();
  }

  handleCreateDialogClosed(): void {
    this.createError.set('');
    this.restoreCreateButtonFocus();
  }

  loadMoreMentors(): void {
    if (!this.hasMoreMentors || this.mentorsLoading()) return;
    this.loadMentors(this.mentorPage() + 1);
  }

  submitCreateCourse(): void {
    if (this.createPending()) return;
    if (this.createCourseFormElement && !this.createCourseFormElement.nativeElement.checkValidity()) {
      this.createCourseFormElement.nativeElement.reportValidity();
      return;
    }

    const title = this.createForm.title.trim();
    const price = this.createForm.price.trim();
    const mentorId = Number(this.createForm.mentorId);
    if (!title || !price || !Number.isSafeInteger(mentorId) || mentorId <= 0
      || !this.mentors().some((mentor) => mentor.id === mentorId)) {
      this.createError.set('Nhập tên, học phí và chọn một giảng viên đang hoạt động.');
      return;
    }

    const request: AdminCourseCreateRequest = {
      title,
      description: this.createForm.description.trim() || null,
      thumbnail_url: this.createForm.thumbnailUrl.trim() || null,
      price,
      mentor_id: mentorId,
    };
    this.createError.set('');
    this.createPending.set(true);
    this.api.createCourse(request).pipe(take(1)).subscribe({
      next: (envelope) => {
        const course = envelope.data;
        if (envelope.success !== true || envelope.businessCode !== 'DESIGN_RESOURCE_CREATED'
          || !isAdminCourse(course) || course.status !== 'DRAFT'
          || course.title !== request.title || course.mentor.id !== request.mentor_id) {
          this.createPending.set(false);
          this.createError.set('Study Server đã phản hồi nhưng dữ liệu khóa học không hợp lệ. Hãy tải lại danh sách trước khi gửi lại.');
          return;
        }
        this.createPending.set(false);
        this.createSuccess.set('Khóa học đã được tạo ở trạng thái Nháp.');
        this.closeCreateDialog();
        if (Number.isSafeInteger(course.id) && course.id > 0) {
          void this.router.navigate(['/admin/courses', course.id], { state: { courseCreated: true } });
        } else {
          this.refreshCourses();
        }
      },
      error: (error: unknown) => {
        this.createPending.set(false);
        this.createError.set(this.createRequestError(error, true));
      },
    });
  }

  private loadMentors(page: number): void {
    if (this.mentorsLoading()) return;
    this.mentorsLoading.set(true);
    this.mentorsError.set('');
    this.api.getActiveMentors(page).pipe(take(1)).subscribe({
      next: (envelope) => {
        this.mentorsLoading.set(false);
        if (envelope.success !== true || envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
          || !isAdminUserPage(envelope.data, page)) {
          this.mentorsError.set('Study Server trả về danh sách Mentor không hợp lệ.');
          return;
        }
        const activeMentors = envelope.data.items.filter((user) =>
          user.role === 'MENTOR' && user.status === 'ACTIVE'
          && Number.isSafeInteger(user.id) && user.id > 0,
        );
        this.mentors.update((current) => page === 1
          ? activeMentors
          : [...current, ...activeMentors.filter((mentor) => !current.some((item) => item.id === mentor.id))]);
        this.mentorPage.set(page);
        this.mentorTotalPages.set(envelope.data.pagination.total_pages);
      },
      error: (error: unknown) => {
        this.mentorsLoading.set(false);
        this.mentorsError.set(this.createRequestError(error, false));
      },
    });
  }

  private restoreCreateButtonFocus(): void {
    queueMicrotask(() => this.addCourseButton?.nativeElement.focus());
  }

  private createRequestError(error: unknown, isCreate: boolean): string {
    if (error instanceof HttpErrorResponse) {
      if (error.status === 401) return 'Phiên Admin đã hết hiệu lực. Hãy đăng nhập lại.';
      if (error.status === 403) return 'Tài khoản không được phép thực hiện thao tác này.';
      if (error.status === 422 && isCreate) return 'Study Server từ chối một hoặc nhiều thông tin. Hãy kiểm tra tên, học phí và giảng viên.';
      if (error.status === 0) return 'Không thể kết nối tới Study Server.';
    }
    return isCreate
      ? 'Không thể tạo khóa học lúc này. Thông tin bạn đã nhập vẫn được giữ lại.'
      : 'Không thể tải danh sách giảng viên. Hãy thử tải lại.';
  }
}

function emptyCreateForm(): { title: string; description: string; thumbnailUrl: string; price: string; mentorId: string } {
  return { title: '', description: '', thumbnailUrl: '', price: '', mentorId: '' };
}
