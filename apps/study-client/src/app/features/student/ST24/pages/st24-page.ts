import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Subject, catchError, distinctUntilChanged, map, of, switchMap, tap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import {
  hasStudentCoursePageCountMismatch,
  isStudentCoursePage,
} from '../../shared/models/student-course-page.guard';

import { ST24CreateDiscussionService } from '../data-access/st24-create-discussion.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type {
  StudentCourseSummary,
  StudentDiscussion,
  StudentPage,
  StudentPagination,
} from '../../shared/models/student-api.models';
import { toSafeStudyId, toSafeStudyNumber } from '../../shared/models/student-api.models';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'study-st24-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st24-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st24-page.html',
})
export class ST24Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST24CreateDiscussionService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly loadCourses$ = new Subject<number>();
  readonly loadingCourses = signal(true);
  readonly courseSnapshotMismatch = signal(false);
  readonly creating = signal(false);
  readonly error = signal<string | null>(null);
  readonly refreshError = signal<string | null>(null);
  readonly creationAccepted = signal(false);
  readonly outcomeUnknown = signal(false);
  readonly createdId = signal<string | null>(null);
  readonly courses = signal<StudentCourseSummary[]>([]);
  readonly coursePagination = signal<StudentPagination | null>(null);
  readonly coursePage = signal(1);
  readonly selectedCourseId = signal('');
  title = '';
  content = '';

  ngOnInit(): void {
    this.loadCourses$
      .pipe(
        tap((page) => {
          this.loadingCourses.set(true);
          this.error.set(null);
          this.courseSnapshotMismatch.set(false);
          this.coursePage.set(page);
          this.courses.set([]);
          this.coursePagination.set(null);
        }),
        switchMap((page) =>
          this.data.courses(page).pipe(
            map((response) => ({ page, response, error: null })),
            catchError((error: unknown) => of({ page, response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyCourses(result));
    this.route.queryParamMap
      .pipe(
        map((params) => params.get('courseId')),
        distinctUntilChanged(),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((courseId) => this.applyCourseQuery(courseId));
    this.loadCourses(1);
  }

  loadCourses(page: number): void {
    if (
      !Number.isSafeInteger(page) ||
      page < 1 ||
      this.creating() ||
      this.creationAccepted() ||
      this.outcomeUnknown()
    ) {
      return;
    }
    this.selectedCourseId.set('');
    this.loadCourses$.next(page);
  }

  changeCoursePage(delta: number): void {
    if (this.courseSnapshotMismatch()) return;
    const targetPage = this.coursePage() + delta;
    const totalPages = this.coursePagination()?.total_pages ?? 0;
    if (targetPage < 1 || targetPage > totalPages) return;
    this.loadCourses(targetPage);
  }

  create(): void {
    const courseId = toSafeStudyNumber(this.selectedCourseId());
    const title = this.title.trim();
    const content = this.content.trim();
    if (this.creating() || this.creationAccepted() || this.outcomeUnknown()) return;
    if (
      courseId === null ||
      !this.courses().some((course) => course.course_id === courseId && course.enrollment_status === 'ACTIVE') ||
      !title ||
      !content
    ) {
      this.error.set('Chọn khóa học đang tham gia và nhập tiêu đề cùng nội dung.');
      return;
    }
    this.creating.set(true);
    this.error.set(null);
    this.refreshError.set(null);
    this.data.create(courseId, title, content).subscribe({
      next: (response) => {
        if (!response.success) {
          const discussionId = toSafeStudyId(response.data?.items?.[0]?.id);
          if (discussionId) this.createdId.set(discussionId);
          this.outcomeUnknown.set(true);
          this.error.set('Chưa thể tạo chủ đề. Vui lòng kiểm tra nội dung và thử lại.');
          this.creating.set(false);
          return;
        }
        const created = response.data?.items?.[0];
        const discussionId = toSafeStudyId(created?.id);
        if (
          response.businessCode !== 'DESIGN_RESOURCE_CREATED' ||
          !discussionId ||
          !isCreatedDiscussionPage(response.data, courseId, title, content)
        ) {
          if (discussionId) this.createdId.set(discussionId);
          this.outcomeUnknown.set(true);
          this.error.set('Chưa thể xác nhận chủ đề đã được tạo. Nút gửi đã khóa để tránh tạo trùng.');
          this.creating.set(false);
          return;
        }
        this.createdId.set(discussionId);
        this.creationAccepted.set(true);
        this.refreshDiscussionList(courseId, discussionId);
      },
      error: (error: unknown) => {
        const knownRejection =
          error instanceof HttpErrorResponse && [401, 403, 422].includes(error.status);
        if (!knownRejection) {
          this.outcomeUnknown.set(true);
        }
        this.error.set(studentApiErrorMessage(error));
        this.creating.set(false);
      },
    });
  }

  backToList(): void {
    const courseId = toSafeStudyNumber(this.selectedCourseId());
    void this.router.navigate(['/student/discussions'], {
      queryParams: courseId ? { courseId } : {},
    });
  }

  createdIdForLink(): string | null {
    return toSafeStudyId(this.createdId());
  }

  private applyCourses(result: CourseLoad): void {
    this.loadingCourses.set(false);
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải danh sách khóa học. Vui lòng thử lại.');
      return;
    }
    if (
      response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isStudentCoursePage(response.data, result.page, 'ACTIVE')
    ) {
      this.error.set('Danh sách khóa học chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }

    const coursePage = response.data;
    const lastAvailablePage = Math.max(coursePage.pagination.total_pages, 1);
    if (coursePage.items.length === 0 && result.page > lastAvailablePage) {
      this.loadCourses(lastAvailablePage);
      return;
    }

    this.courseSnapshotMismatch.set(hasStudentCoursePageCountMismatch(coursePage));
    this.courses.set(coursePage.items);
    this.coursePagination.set(coursePage.pagination);
    this.applyCourseQuery(this.route.snapshot.queryParamMap.get('courseId'));
  }

  private applyCourseQuery(rawCourseId: string | null): void {
    const courseId = toSafeStudyNumber(rawCourseId);
    const courseIsLoaded =
      courseId !== null &&
      this.courses().some(
        (course) => course.course_id === courseId && course.enrollment_status === 'ACTIVE',
      );
    this.selectedCourseId.set(courseIsLoaded ? String(courseId) : '');
  }

  private refreshDiscussionList(courseId: number, discussionId: string): void {
    this.data.refresh(courseId).subscribe({
      next: (response) => {
        if (
          !response.success ||
          response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
          !isDiscussionPage(response.data, courseId)
        ) {
          this.refreshError.set('Chủ đề đã được tạo nhưng danh sách chưa tải lại. Vui lòng thử lại.');
          this.creating.set(false);
          return;
        }
        if (!response.data.items.some((discussion) => String(discussion.id) === discussionId)) {
          this.refreshError.set('Chủ đề đã tạo nhưng chưa xuất hiện trong trang danh sách hiện tại.');
          this.creating.set(false);
          return;
        }
        this.creating.set(false);
        if (this.destroyRef.destroyed) return;
        void this.router
          .navigate(['/student/discussions'], { queryParams: { courseId } })
          .then((navigated) => {
            if (!navigated) this.refreshError.set('Chủ đề đã tạo. Mở chi tiết bằng liên kết bên dưới.');
          })
          .catch(() => this.refreshError.set('Chủ đề đã tạo. Mở chi tiết bằng liên kết bên dưới.'));
      },
      error: (error: unknown) => {
        this.refreshError.set(studentApiErrorMessage(error));
        this.creating.set(false);
      },
    });
  }
}

interface CourseLoad {
  page: number;
  response: ApiEnvelope<StudentPage<StudentCourseSummary>> | null;
  error: unknown | null;
}

function isCreatedDiscussionPage(
  value: unknown,
  courseId: number,
  expectedTitle: string,
  expectedContent: string,
): value is StudentPage<StudentDiscussion> {
  if (typeof value !== 'object' || value === null) return false;
  const page = value as Record<string, unknown>;
  const pagination = page['pagination'];
  if (typeof pagination !== 'object' || pagination === null || !Array.isArray(page['items']))
    return false;
  const discussion = page['items'][0] as Record<string, unknown> | undefined;
  const meta = pagination as Record<string, unknown>;
  return (
    page['items'].length === 1 &&
    discussion !== undefined &&
    toSafeStudyId(discussion['id']) !== null &&
    toSafeStudyId(discussion['course_id']) === String(courseId) &&
    discussion['title'] === expectedTitle &&
    discussion['content'] === expectedContent &&
    discussion['status'] === 'ACTIVE' &&
    Array.isArray(discussion['comments']) &&
    discussion['comments'].length === 0 &&
    meta['page'] === 1 &&
    meta['size'] === 1 &&
    meta['total'] === 1 &&
    meta['total_pages'] === 1
  );
}

function isDiscussionPage(value: unknown, courseId: number): value is StudentPage<StudentDiscussion> {
  if (typeof value !== 'object' || value === null) return false;
  const page = value as Record<string, unknown>;
  const pagination = page['pagination'];
  if (typeof pagination !== 'object' || pagination === null || !Array.isArray(page['items']))
    return false;
  const meta = pagination as Record<string, unknown>;
  const total = meta['total'];
  return (
    page['items'].every((item: unknown) => {
      if (typeof item !== 'object' || item === null) return false;
      const discussion = item as Record<string, unknown>;
      return (
        toSafeStudyId(discussion['id']) !== null &&
        toSafeStudyId(discussion['course_id']) === String(courseId) &&
        typeof discussion['title'] === 'string' &&
        typeof discussion['content'] === 'string' &&
        typeof discussion['status'] === 'string' &&
        Array.isArray(discussion['comments'])
      );
    }) &&
    (page['items'] as unknown[]).length <= 20 &&
    meta['page'] === 1 &&
    meta['size'] === 20 &&
    Number.isSafeInteger(total) &&
    Number(total) >= 0 &&
    meta['total_pages'] === (Number(total) ? Math.ceil(Number(total) / 20) : 0)
  );
}
