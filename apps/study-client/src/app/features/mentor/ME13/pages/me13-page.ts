import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Me13RecipientsService } from '../data-access/me13-recipients.service';
import {
  MentorCourseItemDto,
  parsePositiveInt,
  parseRecipientsCsv,
  StudentSummaryDto,
} from '../models/me13-recipients.models';
import { Me13CourseSelectorComponent } from '../ui/me13-course-selector';
import { Me13StudentRosterComponent } from '../ui/me13-student-roster';

@Component({
  selector: 'app-me13-page',
  imports: [Me13CourseSelectorComponent, Me13StudentRosterComponent],
  templateUrl: './me13-page.html',
  styleUrl: './me13-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ME13Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(Me13RecipientsService);

  readonly courses = signal<MentorCourseItemDto[]>([]);
  readonly selectedCourseId = signal<number | null>(null);
  readonly students = signal<StudentSummaryDto[]>([]);
  readonly selectedIds = signal<Set<number>>(new Set<number>());
  readonly searchKeyword = signal<string>('');

  readonly loadingCourses = signal<boolean>(false);
  readonly loadingStudents = signal<boolean>(false);
  readonly errorCode = signal<string | null>(null);
  readonly errorMessage = signal<string | null>(null);

  readonly filteredStudents = computed(() => {
    const keyword = this.searchKeyword().trim().toLowerCase();
    const list = this.students();
    if (!keyword) {
      return list;
    }
    return list.filter(
      (s) =>
        s.full_name.toLowerCase().includes(keyword) ||
        String(s.id).includes(keyword.replace(/^#/, '')),
    );
  });

  ngOnInit(): void {
    const queryCourseId = parsePositiveInt(this.route.snapshot.queryParamMap.get('courseId'));
    const queryRecipients = parseRecipientsCsv(this.route.snapshot.queryParamMap.get('recipients'));
    if (queryRecipients.length > 0) {
      this.selectedIds.set(new Set(queryRecipients));
    }

    this.loadCourses(queryCourseId);
  }

  loadCourses(initialCourseId: number | null = null): void {
    this.loadingCourses.set(true);
    this.errorMessage.set(null);
    this.errorCode.set(null);

    this.service.getMentorCourses().subscribe({
      next: (list) => {
        this.courses.set(list);
        this.loadingCourses.set(false);
        const targetId = initialCourseId ?? (list[0]?.id ?? null);
        if (targetId) {
          this.onCourseChange(targetId, initialCourseId !== null);
        }
      },
      error: (err: unknown) => {
        this.loadingCourses.set(false);
        this.applyError(err, 'Không thể tải danh sách khóa học của Mentor.');
        if (initialCourseId) {
          this.onCourseChange(initialCourseId, true);
        }
      },
    });
  }

  onCourseChange(courseId: number, keepPreselectedIds = false): void {
    this.selectedCourseId.set(courseId);
    if (!keepPreselectedIds) {
      this.selectedIds.set(new Set<number>());
    }
    this.loadStudentsForCourse(courseId);
  }

  loadStudentsForCourse(courseId: number): void {
    this.loadingStudents.set(true);
    this.errorMessage.set(null);
    this.errorCode.set(null);

    this.service.getCourseStudents(courseId).subscribe({
      next: (roster) => {
        this.students.set(roster);
        this.loadingStudents.set(false);
      },
      error: (err: unknown) => {
        this.loadingStudents.set(false);
        this.applyError(err, 'Không thể tải danh sách học viên của khóa học.');
      },
    });
  }

  onToggleStudent(studentId: number): void {
    const next = new Set(this.selectedIds());
    if (next.has(studentId)) {
      next.delete(studentId);
    } else {
      next.add(studentId);
    }
    this.selectedIds.set(next);
  }

  onSelectAllVisible(): void {
    const next = new Set(this.selectedIds());
    for (const student of this.filteredStudents()) {
      next.add(student.id);
    }
    this.selectedIds.set(next);
  }

  onClearSelection(): void {
    this.selectedIds.set(new Set<number>());
  }

  proceedToCompose(): void {
    const ids = Array.from(this.selectedIds());
    const courseId = this.selectedCourseId();
    if (ids.length === 0) {
      return;
    }
    const selectedObjects = this.students().filter((s) => this.selectedIds().has(s.id));
    void this.router.navigate(['/mentor/notifications/create'], {
      queryParams: {
        courseId: courseId ?? undefined,
        recipients: ids.join(','),
      },
      state: {
        courseId,
        recipients: selectedObjects,
      },
    });
  }

  private applyError(err: unknown, fallbackMessage: string): void {
    if (err instanceof HttpErrorResponse) {
      const apiCode =
        (err.error as { error?: { code?: string } } | null)?.error?.code ?? `HTTP_${err.status}`;
      const apiMsg =
        (err.error as { error?: { message?: string } } | null)?.error?.message ?? err.message;
      this.errorCode.set(apiCode);
      this.errorMessage.set(apiMsg);
    } else {
      this.errorCode.set('UNKNOWN_ERROR');
      this.errorMessage.set(fallbackMessage);
    }
  }
}
