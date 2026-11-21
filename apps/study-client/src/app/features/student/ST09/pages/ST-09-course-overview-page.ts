import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, map, of, switchMap } from 'rxjs';
import { StudentCourseOverviewService } from '../data-access/ST-09-course-overview.service';
import type { StudentCourseOverviewState } from '../models/ST-09-course-overview.models';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { StudentCourseOverviewView } from '../ui/ST-09-course-overview-view';

@Component({
  selector: 'study-student-course-overview-page',
  imports: [StudentCourseOverviewView],
  templateUrl: './ST-09-course-overview-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCourseOverviewPage implements OnInit {
  private readonly source = inject(StudentCourseOverviewService);
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  readonly state = signal<StudentCourseOverviewState>({kind: 'loading', title: 'Đang tải khóa học', message: ''});

  ngOnInit(): void {
    this.route.paramMap.pipe(
      switchMap((params) => {
        const courseId = params.get('courseId');
        if (!courseId || !/^[1-9]\d*$/.test(courseId)) {
          return of<StudentCourseOverviewState>({kind: 'missing-context', title: 'Thiếu thông tin trên đường dẫn', message: 'Vui lòng mở lại màn hình từ chức năng trước đó.'});
        }
        this.state.set({kind: 'loading', title: 'Đang tải khóa học', message: ''});
        // API #37 joins an ACTIVE enrollment before returning progress, so it gates private learning.
        return this.source.getProgress(courseId).pipe(
          switchMap((progress) => {
            if (!progress.success || !progress.data) throw new Error('Invalid progress response');
            return this.source.getCurriculum(courseId).pipe(map((curriculum): StudentCourseOverviewState => {
              if (!curriculum.success || !Array.isArray(curriculum.data?.items)) throw new Error('Invalid curriculum response');
              return {kind: 'ready', title: 'Nội dung khóa học', message: '', progress: progress.data, lessons: curriculum.data.items};
            }));
          }),
          catchError((error: unknown) => of<StudentCourseOverviewState>(error instanceof HttpErrorResponse && error.status === 404
            ? {kind: 'not-enrolled', title: 'Bạn chưa ghi danh khóa học này', message: 'Hãy ghi danh trước khi mở nội dung học.'}
            : {kind: 'error', title: 'Chưa thể tải khóa học', message: 'Vui lòng thử lại sau.'})),
        );
      }),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe((state) => this.state.set(state));
  }
}
