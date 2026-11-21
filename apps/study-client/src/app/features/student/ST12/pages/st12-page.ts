import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
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
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST12ResourcesService } from '../data-access/st12-resources.service';
import { studentApiErrorMessage } from '../../shared/models/student-api-errors';
import type { StudentLessonResources } from '../../shared/models/student-api.models';
import { toSafeStudyId } from '../../shared/models/student-api.models';

@Component({
  imports: [RouterLink],
  selector: 'study-st12-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-learning.css',
    './st12-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st12-page.html',
})
export class ST12Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly data = inject(ST12ResourcesService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryResources$ = new Subject<void>();
  readonly lessonId = signal(toSafeStudyId(this.route.snapshot.paramMap.get('lessonId')));
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly lesson = signal<StudentLessonResources | null>(null);

  ngOnInit(): void {
    const lessonId$ = this.route.paramMap.pipe(
      map((params) => toSafeStudyId(params.get('lessonId'))),
      distinctUntilChanged(),
      tap((lessonId) => this.lessonId.set(lessonId)),
    );

    combineLatest([lessonId$, this.retryResources$.pipe(startWith(undefined))])
      .pipe(
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.lesson.set(null);
        }),
        switchMap(([lessonId]) => this.loadResources(lessonId)),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.applyResourcesResult(result));
  }

  retryResources(): void {
    this.retryResources$.next();
  }

  private loadResources(lessonId: string | null) {
    if (!lessonId) return of({ lessonId, response: null, error: null });
    return this.data.resources(lessonId).pipe(
      map((response) => ({ lessonId, response, error: null })),
      catchError((error: unknown) => of({ lessonId, response: null, error })),
    );
  }

  private applyResourcesResult(result: ResourcesResult): void {
    this.loading.set(false);
    if (!result.lessonId) {
      this.error.set('Không tìm thấy bài học này.');
      return;
    }
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }

    const response = result.response;
    if (!response?.success) {
      this.error.set('Chưa thể tải tài liệu bài học. Vui lòng thử lại.');
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải tài liệu bài học. Vui lòng thử lại.');
      return;
    }
    if (!isStudentLessonResources(response.data, result.lessonId)) {
      this.error.set('Danh sách tài liệu chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    if (toSafeStudyId(response.data.id) !== result.lessonId) {
      this.error.set('Không tìm thấy bài học này.');
      return;
    }
    this.lesson.set(response.data);
  }
}

interface ResourcesResult {
  lessonId: string | null;
  response: ApiEnvelope<StudentLessonResources> | null;
  error: unknown | null;
}

function isStudentLessonResources(
  value: unknown,
  lessonId: string,
): value is StudentLessonResources {
  if (typeof value !== 'object' || value === null) return false;
  const lesson = value as Record<string, unknown>;
  if (
    toSafeStudyId(lesson['id']) === null ||
    toSafeStudyId(lesson['course_id']) === null ||
    typeof lesson['title'] !== 'string' ||
    typeof lesson['order'] !== 'number' ||
    !Number.isInteger(lesson['order']) ||
    lesson['status'] !== 'PUBLISHED' ||
    !Array.isArray(lesson['resources'])
  ) {
    return false;
  }

  let previousResourceId = 0;
  for (const resource of lesson['resources']) {
    if (typeof resource !== 'object' || resource === null) return false;
    const item = resource as Record<string, unknown>;
    const resourceId = item['id'];
    if (
      typeof resourceId !== 'number' ||
      toSafeStudyId(resourceId) === null ||
      resourceId <= previousResourceId ||
      toSafeStudyId(item['lesson_id']) !== lessonId ||
      typeof item['name'] !== 'string' ||
      typeof item['type'] !== 'string' ||
      item['url'] !== null
    ) {
      return false;
    }
    previousResourceId = resourceId;
  }

  return true;
}
