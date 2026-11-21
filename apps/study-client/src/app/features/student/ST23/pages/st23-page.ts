import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  distinctUntilChanged,
  map,
  of,
  switchMap,
  takeUntil,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST23DiscussionsService } from '../data-access/st23-discussions.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentDiscussion,
  StudentDiscussionComment,
  StudentPagination,
  StudentPage,
} from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'study-st23-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st23-page.html',
})
export class ST23Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST23DiscussionsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly request$ = new Subject<DiscussionRequest>();
  private readonly cancelRequest$ = new Subject<void>();
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly discussions = signal<StudentDiscussion[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);
  readonly snapshotMismatch = signal(false);
  readonly courseFilter = signal<number | null>(null);
  readonly page = signal(1);
  readonly invalidCourseQuery = signal(false);
  courseIdInput = '';

  ngOnInit(): void {
    this.request$
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.snapshotMismatch.set(false);
          this.discussions.set([]);
          this.pagination.set(null);
        }),
        switchMap((request) =>
          this.data.discussions(request.courseId, request.page).pipe(
            takeUntil(this.cancelRequest$),
            map((response) => ({ request, response, error: null })),
            catchError((error: unknown) => of({ request, response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResult(result));

    this.route.queryParamMap
      .pipe(
        map((params) => params.get('courseId')),
        distinctUntilChanged(),
        tap((rawCourseId) => {
          this.courseIdInput = rawCourseId ?? '';
          const courseId = rawCourseId ? toSafeStudyNumber(rawCourseId) : null;
          this.invalidCourseQuery.set(rawCourseId !== null && courseId === null);
          if (this.invalidCourseQuery()) {
            this.cancelRequest$.next();
            this.courseFilter.set(null);
            this.page.set(1);
            this.loading.set(false);
            this.snapshotMismatch.set(false);
            this.discussions.set([]);
            this.pagination.set(null);
      this.error.set('Mã khóa học chưa hợp lệ.');
            return;
          }
          this.courseFilter.set(courseId);
          this.page.set(1);
          this.load();
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe();
  }

  load(): void {
    if (this.invalidCourseQuery()) return;
    this.request$.next({ courseId: this.courseFilter(), page: this.page() });
  }

  retry(): void {
    this.load();
  }

  applyCourseFilter(): void {
    const raw = this.courseIdInput.trim();
    const courseId = raw ? toSafeStudyNumber(raw) : null;
    if (raw && courseId === null) {
      this.invalidCourseQuery.set(true);
      this.cancelRequest$.next();
      this.loading.set(false);
      this.snapshotMismatch.set(false);
      this.discussions.set([]);
      this.pagination.set(null);
      this.error.set('Mã khóa học phải là số nguyên dương an toàn.');
      return;
    }
    this.invalidCourseQuery.set(false);
    this.courseFilter.set(courseId);
    this.page.set(1);
    const current = this.route.snapshot.queryParamMap.get('courseId');
    const next = courseId === null ? null : String(courseId);
    if (current === next) this.load();
    else {
      void this.router.navigate([], {
        relativeTo: this.route,
        queryParams: { courseId: next },
        queryParamsHandling: 'merge',
      });
    }
  }

  changePage(delta: number): void {
    if (this.snapshotMismatch()) return;
    const targetPage = this.page() + delta;
    const totalPages = this.pagination()?.total_pages ?? 0;
    if (targetPage < 1 || targetPage > totalPages) return;
    this.page.set(targetPage);
    this.load();
  }

  safeId(id: unknown): string | null {
    return toSafeStudyId(id);
  }

  private applyResult(result: DiscussionResult): void {
    this.loading.set(false);
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải danh sách thảo luận. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isDiscussionPage(response.data, result.request.page)
    ) {
      this.error.set('Danh sách thảo luận chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }

    const pageData = response.data;
    const lastAvailablePage = Math.max(pageData.pagination.total_pages, 1);
    if (pageData.items.length === 0 && result.request.page > lastAvailablePage) {
      this.page.set(lastAvailablePage);
      this.load();
      return;
    }

    this.snapshotMismatch.set(hasDiscussionPageCountMismatch(pageData));
    this.discussions.set(pageData.items);
    this.pagination.set(pageData.pagination);
  }
}

interface DiscussionRequest {
  courseId: number | null;
  page: number;
}

interface DiscussionResult {
  request: DiscussionRequest;
  response: ApiEnvelope<StudentPage<StudentDiscussion>> | null;
  error: unknown | null;
}

function isDiscussionPage(value: unknown, expectedPage: number): value is StudentPage<StudentDiscussion> {
  if (typeof value !== 'object' || value === null) return false;
  const page = value as Record<string, unknown>;
  const pagination = page['pagination'];
  if (typeof pagination !== 'object' || pagination === null || !Array.isArray(page['items']))
    return false;
  const meta = pagination as Record<string, unknown>;
  const total = meta['total'];
  return (
    page['items'].every((item: unknown) => isDiscussion(item)) &&
    (page['items'] as unknown[]).length <= 20 &&
    meta['page'] === expectedPage &&
    meta['size'] === 20 &&
    Number.isSafeInteger(total) &&
    Number(total) >= 0 &&
    meta['total_pages'] === (Number(total) ? Math.ceil(Number(total) / 20) : 0)
  );
}

function hasDiscussionPageCountMismatch(page: StudentPage<StudentDiscussion>): boolean {
  const { page: pageNumber, size, total } = page.pagination;
  const offset = (pageNumber - 1) * size;
  const expectedItems = Math.min(size, Math.max(total - offset, 0));
  return page.items.length !== expectedItems;
}

function isDiscussion(value: unknown): value is StudentDiscussion {
  if (typeof value !== 'object' || value === null) return false;
  const discussion = value as Record<string, unknown>;
  const author = discussion['author'];
  return (
    toSafeStudyId(discussion['id']) !== null &&
    toSafeStudyId(discussion['course_id']) !== null &&
    typeof discussion['title'] === 'string' &&
    typeof discussion['content'] === 'string' &&
    discussion['status'] === 'ACTIVE' &&
    isAuthor(author) &&
    Array.isArray(discussion['comments']) &&
    discussion['comments'].every((comment: unknown) => isComment(comment))
  );
}

function isAuthor(value: unknown): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const author = value as Record<string, unknown>;
  return (
    toSafeStudyId(author['id']) !== null &&
    typeof author['full_name'] === 'string' &&
    (author['avatar_url'] === undefined ||
      author['avatar_url'] === null ||
      typeof author['avatar_url'] === 'string')
  );
}

function isComment(value: unknown): value is StudentDiscussionComment {
  if (typeof value !== 'object' || value === null) return false;
  const comment = value as Record<string, unknown>;
  return (
    toSafeStudyId(comment['id']) !== null &&
    toSafeStudyId(comment['discussion_id']) !== null &&
    typeof comment['content'] === 'string' &&
    typeof comment['created_at'] === 'string' &&
    isAuthor(comment['author'])
  );
}
