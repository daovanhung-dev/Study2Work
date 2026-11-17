import { Component, OnInit, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { ME13RecipientsService } from '../data-access/me13-recipients.service';
import type { MentorCourse, MentorPage, MentorStudentSummary } from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage, mentorEnvelopeError } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

@Component({ imports: [MentorPageHeader], selector: 'study-me13-page', styleUrls: ['./me13-page.css', '../../shared/ui/mentor-pages.css'], templateUrl: './me13-page.html' })
export class ME13Page implements OnInit {
  private readonly data = inject(ME13RecipientsService);
  private readonly router = inject(Router);
  readonly courses = signal<MentorCourse[]>([]);
  readonly coursePage = signal(1);
  readonly courseTotalPages = signal(1);
  readonly courseId = signal('');
  readonly students = signal<MentorStudentSummary[]>([]);
  readonly selectedIds = signal<Set<string>>(new Set());
  readonly coursesLoading = signal(true);
  readonly studentsLoading = signal(false);
  readonly error = signal<string | null>(null);
  readonly studentError = signal<string | null>(null);
  ngOnInit(): void { this.loadCourses(); }
  loadCourses(page = this.coursePage()): void {
    this.coursesLoading.set(true); this.error.set(null);
    this.data.courses(page).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.error.set(issue); else { const result = response.data as MentorPage<MentorCourse>; this.courses.set(result.items); this.coursePage.set(result.pagination.page); this.courseTotalPages.set(result.pagination.total_pages); } this.coursesLoading.set(false); }, error: (error: unknown) => { this.error.set(mentorApiErrorMessage(error)); this.coursesLoading.set(false); } });
  }
  chooseCourse(id: string): void {
    const safeId = toSafeMentorId(id);
    this.courseId.set(safeId ?? ''); this.students.set([]); this.selectedIds.set(new Set()); this.studentError.set(null);
    if (!safeId) return;
    this.studentsLoading.set(true);
    this.data.students(safeId).subscribe({ next: (response) => { const issue = mentorEnvelopeError(response.success, response.message); if (issue) this.studentError.set(issue); else this.students.set(response.data); this.studentsLoading.set(false); }, error: (error: unknown) => { this.studentError.set(mentorApiErrorMessage(error)); this.studentsLoading.set(false); } });
  }
  toggleStudent(id: string, checked: boolean): void {
    this.selectedIds.update((current) => { const next = new Set(current); if (checked) next.add(id); else next.delete(id); return next; });
  }
  selectAll(checked: boolean): void {
    this.selectedIds.set(checked ? new Set(this.students().map((student) => toSafeMentorId(student.id)).filter((id): id is string => id !== null)) : new Set());
  }
  safeId(value: unknown): string | null { return toSafeMentorId(value); }
  selectedStudents(): Array<{ id: string; full_name: string }> {
    const ids = this.selectedIds();
    return this.students().flatMap((student) => { const id = toSafeMentorId(student.id); return id && ids.has(id) ? [{ id, full_name: student.full_name }] : []; });
  }
  continueToCompose(): void {
    if (!this.courseId() || !this.selectedIds().size) return;
    void this.router.navigate(['/mentor/notifications/new'], { state: { courseId: this.courseId(), recipients: this.selectedStudents() } });
  }
}
