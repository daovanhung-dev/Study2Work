import { DatePipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Subject, catchError, map, of, startWith, switchMap, tap } from 'rxjs';
import { ST20ProgressService } from '../data-access/st20-progress.service';
import { isStudentAchievementPage } from '../../shared/models/student-achievement-page.guard';
import { studentApiErrorMessage, studentEnvelopeError } from '../../shared/models/student-api-errors';
import type { StudentAchievement } from '../../shared/models/student-api.models';

@Component({
  imports: [DatePipe, RouterLink],
  selector: 'study-st20-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st20-page.html',
})
export class ST20Page implements OnInit {
  private readonly data = inject(ST20ProgressService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly retryAchievements$ = new Subject<void>();
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly snapshotMismatch = signal(false);
  readonly achievements = signal<StudentAchievement[]>([]);

  ngOnInit(): void {
    this.retryAchievements$
      .pipe(
        startWith(undefined),
        tap(() => {
          this.loading.set(true);
          this.error.set(null);
          this.snapshotMismatch.set(false);
          this.achievements.set([]);
        }),
        switchMap(() =>
          this.data.achievements().pipe(
            map((response) => ({ response, error: null })),
            catchError((error: unknown) => of({ response: null, error })),
          ),
        ),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((result) => {
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
        this.snapshotMismatch.set(response.data.pagination.total !== response.data.items.length);
        this.achievements.set(response.data.items);
      });
  }

  retryAchievements(): void {
    this.retryAchievements$.next();
  }
}
