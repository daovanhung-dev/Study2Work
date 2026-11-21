import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { EMPTY, Subject, catchError, map, of, switchMap, tap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME13RecipientsService } from '../data-access/me13-recipients.service';
import type { MentorCourse, MentorPage, MentorStudentSummary } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

type ME13CourseResult =
  | { page: number; response: ApiEnvelope<MentorPage<MentorCourse>> }
  | { page: number; error: unknown };
type ME13StudentResult =
  | { courseId: string; response: ApiEnvelope<MentorStudentSummary[]> }
  | { courseId: string; error: unknown };

@Component({
  imports: [MentorPageHeader],
  selector: 'study-me13-page',
  styleUrls: ['./me13-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me13-page.html',
})
export class ME13Page implements OnInit {
  private readonly data = inject(ME13RecipientsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly router = inject(Router);
  private readonly coursePage$ = new Subject<number>();
  private readonly rosterCourse$ = new Subject<string>();

  readonly courses = signal<MentorCourse[]>([]);
  readonly coursePage = signal(1);
  readonly courseTotalPages = signal(1);
  readonly courseId = signal('');
  readonly students = signal<MentorStudentSummary[]>([]);
  readonly selectedIds = signal<Set<string>>(new Set());
  readonly failedStudentAvatarIds = signal<ReadonlySet<string>>(new Set());
  readonly coursesLoading = signal(true);
  readonly studentsLoading = signal(false);
  readonly error = signal<string | null>(null);
  readonly studentError = signal<string | null>(null);
  readonly studentForbidden = signal(false);

  ngOnInit(): void {
    this.coursePage$
      .pipe(
        tap((page) => this.resetCourseRead(page)),
        switchMap((page) =>
          this.data.courses(page).pipe(
            map((response): ME13CourseResult => ({ page, response })),
            catchError((error: unknown) => of<ME13CourseResult>({ page, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyCourseResult(result));

    this.rosterCourse$
      .pipe(
        tap((courseId) => this.resetRosterRead(Boolean(courseId))),
        switchMap((courseId) => {
          if (toSafeMentorId(courseId) !== courseId || !courseId) return EMPTY;
          return this.data.students(courseId).pipe(
            map((response): ME13StudentResult => ({ courseId, response })),
            catchError((error: unknown) => of<ME13StudentResult>({ courseId, error })),
          );
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyStudentResult(result));

    this.loadCourses();
  }

  loadCourses(page = this.coursePage()): void {
    if (!Number.isInteger(page) || page < 1 || page > 2 ** 31 - 1) {
      this.coursesLoading.set(false);
      this.error.set('Số trang khóa học cần là số nguyên dương trong giới hạn API.');
      return;
    }
    this.coursePage$.next(page);
  }

  loadStudents(): void {
    const courseId = this.courseId();
    if (courseId) this.rosterCourse$.next(courseId);
  }

  chooseCourse(id: string): void {
    const safeId = toSafeMentorId(id);
    this.courseId.set(safeId ?? '');
    this.students.set([]);
    this.selectedIds.set(new Set());
    this.failedStudentAvatarIds.set(new Set<string>());
    this.studentError.set(null);
    this.studentForbidden.set(false);
    this.rosterCourse$.next(safeId ?? '');
  }

  toggleStudent(id: string, checked: boolean): void {
    const safeId = toSafeMentorId(id);
    if (!safeId || !this.students().some((student) => toSafeMentorId(student.id) === safeId)) return;
    this.selectedIds.update((current) => {
      const next = new Set(current);
      if (checked) next.add(safeId);
      else next.delete(safeId);
      return next;
    });
  }

  selectAll(checked: boolean): void {
    this.selectedIds.set(
      checked
        ? new Set(this.students().map((student) => toSafeMentorId(student.id)).filter((id): id is string => id !== null))
        : new Set(),
    );
  }

  safeId(value: unknown): string | null {
    return toSafeMentorId(value);
  }

  studentAvatarUrl(student: MentorStudentSummary): string | null {
    const id = toSafeMentorId(student.id);
    return id && !this.failedStudentAvatarIds().has(id)
      ? safeMentorAvatarUrl(student.avatar_url)
      : null;
  }

  studentInitials(student: MentorStudentSummary): string {
    const parts = student.full_name.trim().split(/\s+/).filter(Boolean);
    return parts.slice(-2).map((part) => Array.from(part)[0]?.toUpperCase() ?? '').join('') || '?';
  }

  markStudentAvatarFailed(studentId: unknown): void {
    const id = toSafeMentorId(studentId);
    if (!id) return;
    this.failedStudentAvatarIds.update((current) => new Set(current).add(id));
  }

  selectedStudents(): Array<{ id: string; full_name: string }> {
    const ids = this.selectedIds();
    return this.students().flatMap((student) => {
      const id = toSafeMentorId(student.id);
      return id && ids.has(id) ? [{ id, full_name: student.full_name }] : [];
    });
  }

  canContinue(): boolean {
    const courseId = toSafeMentorId(this.courseId());
    const recipients = this.selectedStudents();
    return Boolean(
      courseId &&
      !this.coursesLoading() &&
      !this.studentsLoading() &&
      !this.studentError() &&
      !this.studentForbidden() &&
      this.courses().some((course) => toSafeMentorId(course.id) === courseId) &&
      recipients.length > 0 &&
      recipients.length === this.selectedIds().size,
    );
  }

  continueToCompose(): void {
    if (!this.canContinue()) return;
    const courseId = this.courseId();
    const recipients = this.selectedStudents();
    if (!courseId || !recipients.length || recipients.some((item) => !toSafeMentorId(item.id))) return;
    void this.router.navigate(['/mentor/notifications/new'], {
      state: { courseId, recipients },
    });
  }

  private resetCourseRead(page: number): void {
    if (this.coursePage() !== page) {
      this.courseId.set('');
      this.students.set([]);
      this.selectedIds.set(new Set());
      this.rosterCourse$.next('');
    }
    this.coursePage.set(page);
    this.courses.set([]);
    this.courseTotalPages.set(1);
    this.coursesLoading.set(true);
    this.error.set(null);
  }

  private applyCourseResult(result: ME13CourseResult): void {
    if (this.coursePage() !== result.page) return;
    this.coursesLoading.set(false);
    if ('error' in result) {
      this.error.set(mentorApiErrorMessage(result.error));
      return;
    }
    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.error.set('Study Server trả về phản hồi khóa học không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.error.set(envelope.message || 'Study Server không xác nhận danh sách khóa học.');
      return;
    }
    if (
      envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
      !isCoursePage(envelope.data, result.page)
    ) {
      this.error.set('Study Server trả về danh sách khóa học không hợp lệ.');
      return;
    }
    this.courses.set(envelope.data.items);
    this.coursePage.set(envelope.data.pagination.page);
    this.courseTotalPages.set(envelope.data.pagination.total_pages);
  }

  private resetRosterRead(hasCourse: boolean): void {
    this.students.set([]);
    this.selectedIds.set(new Set());
    this.failedStudentAvatarIds.set(new Set<string>());
    this.studentsLoading.set(hasCourse);
    this.studentError.set(null);
    this.studentForbidden.set(false);
  }

  private applyStudentResult(result: ME13StudentResult): void {
    if (this.courseId() !== result.courseId) return;
    this.studentsLoading.set(false);
    if ('error' in result) {
      this.studentForbidden.set(hasHttpStatus(result.error, 403));
      if (!this.studentForbidden()) this.studentError.set(mentorApiErrorMessage(result.error));
      return;
    }
    const envelope: unknown = result.response;
    if (!isApiEnvelope(envelope)) {
      this.studentError.set('Study Server trả về roster không hợp lệ.');
      return;
    }
    if (!envelope.success) {
      this.studentForbidden.set(envelope.businessCode === 'DESIGN_ACCESS_DENIED');
      if (!this.studentForbidden()) this.studentError.set(envelope.message || 'Study Server không xác nhận roster.');
      return;
    }
    if (envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' || !isStudentList(envelope.data)) {
      this.studentError.set('Study Server trả về roster không hợp lệ.');
      return;
    }
    this.students.set(envelope.data);
    const ids = new Set(envelope.data.map((student) => toSafeMentorId(student.id)).filter((id): id is string => id !== null));
    this.selectedIds.update((selected) => new Set([...selected].filter((id) => ids.has(id))));
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isApiEnvelope(value: unknown): value is ApiEnvelope<unknown> {
  return (
    isRecord(value) &&
    typeof value['success'] === 'boolean' &&
    typeof value['businessCode'] === 'string' &&
    typeof value['message'] === 'string' &&
    isRecord(value['meta']) &&
    typeof value['traceId'] === 'string'
  );
}

function isCoursePage(value: unknown, requestedPage: number): value is MentorPage<MentorCourse> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) return false;
  const pagination = value['pagination'];
  const { page, size, total, total_pages: totalPages } = pagination;
  if (
    !isNonNegativeInt(page) || page !== requestedPage ||
    !isNonNegativeInt(size) || size !== 100 ||
    !isNonNegativeInt(total) ||
    !isNonNegativeInt(totalPages) ||
    totalPages !== (total === 0 ? 0 : Math.ceil(total / size)) ||
    value['items'].length > size
  ) {
    return false;
  }
  const ids = new Set<string>();
  for (const course of value['items']) {
    if (
      !isRecord(course) ||
      toSafeMentorId(course['id']) === null ||
      typeof course['title'] !== 'string' ||
      (course['status'] !== 'DRAFT' && course['status'] !== 'PUBLISHED') ||
      typeof course['price'] !== 'string' ||
      !isOptionalString(course['description']) ||
      !isOptionalString(course['thumbnail_url']) ||
      !isRecord(course['mentor']) ||
      toSafeMentorId(course['mentor']['id']) === null ||
      typeof course['mentor']['full_name'] !== 'string' ||
      !isOptionalString(course['mentor']['avatar_url'])
    ) {
      return false;
    }
    const id = toSafeMentorId(course['id']);
    if (id === null || ids.has(id)) return false;
    ids.add(id);
  }
  return true;
}

function isStudentList(value: unknown): value is MentorStudentSummary[] {
  if (!Array.isArray(value)) return false;
  const ids = new Set<string>();
  for (const student of value) {
    if (
      !isRecord(student) ||
      toSafeMentorId(student['id']) === null ||
      typeof student['full_name'] !== 'string' ||
      (student['avatar_url'] !== undefined && student['avatar_url'] !== null && typeof student['avatar_url'] !== 'string')
    ) {
      return false;
    }
    const id = toSafeMentorId(student['id']);
    if (id === null || ids.has(id)) return false;
    ids.add(id);
  }
  return true;
}

function isNonNegativeInt(value: unknown): value is number {
  return Number.isSafeInteger(value) && Number(value) >= 0;
}

function isOptionalString(value: unknown): boolean {
  return value === undefined || value === null || typeof value === 'string';
}

function hasHttpStatus(error: unknown, status: number): boolean {
  return isRecord(error) && error['status'] === status;
}

function safeMentorAvatarUrl(value: unknown): string | null {
  if (typeof value !== 'string' || !value.trim() || typeof globalThis.location === 'undefined') {
    return null;
  }
  try {
    const origin = globalThis.location.origin;
    const url = new URL(value, origin);
    return url.protocol === 'https:' || (url.protocol === 'http:' && url.origin === origin)
      ? url.href
      : null;
  } catch {
    return null;
  }
}
