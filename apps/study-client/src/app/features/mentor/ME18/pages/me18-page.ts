import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Me18AnalyticsService } from '../data-access/me18-analytics.service';
import {
  MentorCourseActivityAnalyticsDto,
  parseCourseIdParam,
} from '../models/me18-analytics.models';
import { Me18MetricsCardsComponent } from '../ui/me18-metrics-cards';

@Component({
  selector: 'app-me18-page',
  imports: [Me18MetricsCardsComponent],
  templateUrl: './me18-page.html',
  styleUrl: './me18-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ME18Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly analyticsService = inject(Me18AnalyticsService);

  readonly courseId = signal<number | null>(null);
  readonly loading = signal<boolean>(false);
  readonly errorMessage = signal<string | null>(null);
  readonly errorCode = signal<string | null>(null);
  readonly analytics = signal<MentorCourseActivityAnalyticsDto | null>(null);

  readonly hasActivity = computed(() => {
    const data = this.analytics();
    return Boolean(
      data && (data.tracked_lesson_accesses > 0 || data.students_with_activity > 0),
    );
  });

  ngOnInit(): void {
    const rawCourseId = this.route.snapshot.paramMap.get('courseId');
    const parsed = parseCourseIdParam(rawCourseId);
    if (!parsed) {
      this.errorCode.set('INVALID_COURSE_ID');
      this.errorMessage.set('Mã khóa học trên đường dẫn không hợp lệ (cần số nguyên dương).');
      return;
    }
    this.courseId.set(parsed);
    this.loadAnalytics();
  }

  loadAnalytics(): void {
    const id = this.courseId();
    if (!id) {
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.errorCode.set(null);

    this.analyticsService.getCourseAnalytics(id).subscribe({
      next: (data) => {
        this.analytics.set(data);
        this.loading.set(false);
      },
      error: (err: unknown) => {
        this.loading.set(false);
        if (err instanceof HttpErrorResponse) {
          const apiCode =
            (err.error as { error?: { code?: string } } | null)?.error?.code ??
            `HTTP_${err.status}`;
          const apiMsg =
            (err.error as { error?: { message?: string } } | null)?.error?.message ??
            err.message;
          this.errorCode.set(apiCode);
          this.errorMessage.set(apiMsg);
        } else {
          this.errorCode.set('UNKNOWN_ERROR');
          this.errorMessage.set('Không thể tải dữ liệu analytics khóa học.');
        }
      },
    });
  }

  backToProgress(): void {
    const id = this.courseId();
    if (id) {
      void this.router.navigate(['/mentor/courses', id, 'progress']);
    } else {
      void this.router.navigate(['/mentor/courses']);
    }
  }
}
