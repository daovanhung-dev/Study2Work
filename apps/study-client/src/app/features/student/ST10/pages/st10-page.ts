import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import {
  Subject,
  catchError,
  combineLatest,
  distinctUntilChanged,
  map,
  of,
  startWith,
  switchMap,
  tap,
} from 'rxjs';
import type { Observable } from 'rxjs';

import { ST10LessonAccessService } from '../data-access/st10-lesson-access.service';
import {
  studentApiErrorMessage,
  studentEnvelopeError,
} from '../../shared/models/student-api-errors';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';
import type { StudentLesson } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';
import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [RouterLink, StudentPublicFrame],
  selector: 'study-st10-page',
  styleUrls: ['./st10-page.css', '../../shared/ui/student-api-page.css'],
  templateUrl: './st10-page.html',
})
export class ST10Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly data = inject(ST10LessonAccessService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryAccess$ = new Subject<void>();
  readonly lessonId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('lessonId')));
  readonly accessLoading = signal(true);
  readonly accessError = signal<string | null>(null);
  readonly lesson = signal<StudentLessonPreview | null>(null);
  readonly starting = signal(false);
  readonly started = signal(false);
  readonly startError = signal<string | null>(null);
  readonly canStart = computed(
    () => this.lesson()?.status === 'PUBLISHED' && !this.starting() && !this.started(),
  );

  ngOnInit(): void {
    const lessonId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('lessonId'))),
      distinctUntilChanged(),
      tap((lessonId) => {
        this.lessonId.set(lessonId);
        this.started.set(false);
        this.starting.set(false);
        this.startError.set(null);
      }),
    );

    combineLatest([lessonId$, this.retryAccess$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.accessLoading.set(true);
          this.accessError.set(null);
          this.lesson.set(null);
        }),
        switchMap(([lessonId]) => this.loadAccess(lessonId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyAccessResult(result));
  }

  checkAccess(): void {
    this.retryAccess$.next();
  }

  startLesson(): void {
    const lessonId = this.lessonId();
    if (!lessonId || !this.canStart()) return;
    this.starting.set(true);
    this.startError.set(null);
    this.data
      .start(lessonId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          if (this.lessonId() !== lessonId) return;
          const issue = studentEnvelopeError(response.success, response.message);
          if (issue || response.businessCode !== 'DESIGN_RESOURCE_CREATED') {
            this.startError.set(
              issue || 'Chưa thể bắt đầu bài học. Vui lòng thử lại.',
            );
            this.starting.set(false);
            return;
          }
          if (
            !isStudentLesson(response.data) ||
            toSafeStudyId(response.data.id) !== lessonId ||
            response.data.status !== 'PUBLISHED'
          ) {
            this.startError.set('Bài học chưa sẵn sàng để bắt đầu.');
            this.starting.set(false);
            return;
          }

          this.started.set(true);
          this.router.navigate(['/student/lessons', lessonId]).then((navigated) => {
            if (this.lessonId() !== lessonId) return;
            this.starting.set(false);
            if (!navigated) {
              this.startError.set(
                'Bài học đã được ghi nhận bắt đầu. Hãy mở ST-11 để tải nội dung.',
              );
            }
          });
        },
        error: (error: unknown) => {
          if (this.lessonId() !== lessonId) return;
          this.startError.set(studentApiErrorMessage(error));
          this.starting.set(false);
        },
      });
  }

  private loadAccess(lessonId: string | null): Observable<AccessResult> {
    if (!lessonId) return of({ lessonId, response: null, error: null });
    return this.data.access(lessonId).pipe(
      map((response) => ({ lessonId, response, error: null })),
      catchError((error: unknown) => of({ lessonId, response: null, error })),
    );
  }

  private applyAccessResult(result: AccessResult): void {
    this.accessLoading.set(false);
    if (!result.lessonId) {
      this.accessError.set('Không tìm thấy bài học này.');
      return;
    }
    if (result.error !== null) {
      this.accessError.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.accessError.set(
        'Chưa thể xác nhận quyền truy cập bài học.',
      );
      return;
    }
    if (!isStudentLesson(response.data)) {
      this.accessError.set('Thông tin bài học chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    if (toSafeStudyId(response.data.id) !== result.lessonId) {
      this.accessError.set('Không tìm thấy bài học này.');
      return;
    }
    this.lesson.set(toLessonPreview(response.data));
  }
}

interface AccessResult {
  lessonId: string | null;
  response: ApiEnvelope<StudentLesson> | null;
  error: unknown | null;
}

interface StudentLessonPreview {
  id: number;
  course_id: number;
  title: string;
  order: number;
  status: string;
}

function toLessonPreview(lesson: StudentLesson): StudentLessonPreview {
  return {
    id: lesson.id,
    course_id: lesson.course_id,
    title: lesson.title,
    order: lesson.order,
    status: lesson.status,
  };
}

function isStudentLesson(value: unknown): value is StudentLesson {
  if (typeof value !== 'object' || value === null) return false;
  const lesson = value as Record<string, unknown>;
  return (
    toSafeStudyId(lesson['id']) !== null &&
    toSafeStudyId(lesson['course_id']) !== null &&
    typeof lesson['title'] === 'string' &&
    typeof lesson['order'] === 'number' &&
    Number.isInteger(lesson['order']) &&
    typeof lesson['status'] === 'string'
  );
}
