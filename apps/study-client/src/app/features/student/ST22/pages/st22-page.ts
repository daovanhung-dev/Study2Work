import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Subject, catchError, map, of, startWith, switchMap, tap } from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ST22AchievementsService } from '../data-access/st22-achievements.service';
import { isStudentAchievementPage } from '../../shared/models/student-achievement-page.guard';
import { studentApiErrorMessage, studentEnvelopeError } from '../../shared/models/student-api-errors';
import type { StudentAchievement, StudentPage, StudentPagination } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st22-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st22-page.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st22-page.html',
})
export class ST22Page implements OnInit {
  private readonly data = inject(ST22AchievementsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retry$ = new Subject<void>();
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly items = signal<StudentAchievement[]>([]);
  readonly pagination = signal<StudentPagination | null>(null);
  readonly hasSnapshotCountMismatch = computed(() => {
    const page = this.pagination();
    return page !== null && page.total !== this.items().length;
  });

  ngOnInit(): void {
    this.retry$
      .pipe(
        startWith(undefined),
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.items.set([]);
          this.pagination.set(null);
        }),
        switchMap(() =>
          this.data.achievements().pipe(
            map((response) => ({ response, error: null })),
            catchError((error: unknown) => of({ response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => this.apply(result));
  }

  retry(): void {
    this.retry$.next();
  }

  private apply(result: AchievementLoad): void {
    this.loading.set(false);
    if (result.error !== null) {
      this.error.set(studentApiErrorMessage(result.error));
      return;
    }
    const response = result.response;
    if (!response) {
      this.error.set('Chưa thể tải thành tích. Vui lòng thử lại.');
      return;
    }
    const envelopeIssue = studentEnvelopeError(response.success, response.message);
    if (envelopeIssue) {
      this.error.set(envelopeIssue);
      return;
    }
    if (response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
      this.error.set('Chưa thể tải thành tích. Vui lòng thử lại.');
      return;
    }
    if (!isStudentAchievementPage(response.data)) {
      this.error.set('Danh sách thành tích chưa đúng định dạng. Hãy tải lại trang.');
      return;
    }
    this.items.set(response.data.items);
    this.pagination.set(response.data.pagination);
  }
}

interface AchievementLoad {
  response: ApiEnvelope<StudentPage<StudentAchievement>> | null;
  error: unknown | null;
}
