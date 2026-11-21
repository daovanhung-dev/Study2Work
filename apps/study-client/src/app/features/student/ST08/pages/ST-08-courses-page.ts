import { StudentCoursesService } from '../data-access/ST-08-courses.service';
import type { StudentCoursesState } from '../models/ST-08-courses.models';
import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { StudentCoursesView } from '../ui/ST-08-courses-view';

@Component({
  selector: 'study-student-courses-page',
  imports: [StudentCoursesView],
  templateUrl: './ST-08-courses-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentCoursesPage implements OnInit {
  private readonly source = inject(StudentCoursesService);
  private readonly destroyRef = inject(DestroyRef);

  readonly state = signal<StudentCoursesState>({kind: 'loading', title: 'Đang tải khóa học của bạn.', message: '', items: []});

  ngOnInit(): void {
    this.loadPage(1);
  }

  loadPage(page: number): void {
    if (!Number.isSafeInteger(page) || page < 1) return;
    this.state.set({kind: 'loading', title: 'Đang tải khóa học của bạn.', message: '', items: []});
    this.source.getCourses(page).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (response) => {
        const items = response.data?.items;
        if (!response.success || !Array.isArray(items)) return this.setError();
        this.state.set(items.length
          ? {kind: 'ready', title: 'Khóa học đang học', message: '', items, pagination: response.data.pagination}
          : {kind: 'empty', title: 'Bạn chưa ghi danh khóa học nào.', message: 'Khám phá khóa học để bắt đầu học.', items: []});
      },
      error: () => this.setError(),
    });
  }

  private setError(): void {
    this.state.set({kind: 'error', title: 'Chưa thể tải khóa học của bạn.', message: 'Vui lòng thử lại sau.', items: []});
  }
}
