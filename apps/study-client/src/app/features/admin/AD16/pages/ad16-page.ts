import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed, toObservable, toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';

import { AdminSessionError } from '../../../../core/auth/admin-session.service';
import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD16ApiService } from '../data-access/ad16-api.service';
import { AD16_SCREEN } from '../models/ad16-screen.model';
import type { AdminCourse, AdminPage } from '../../admin-api.models';
import { hasAdminPageCountMismatch, isAdminCoursePage } from '../../admin-api-guards';
import { adminDataError } from '../../admin-screen-state';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

type DraftField = 'titleDraft' | 'durationDraft' | 'passingScoreDraft';
type QuizQuestionType = 'SINGLE_CHOICE' | 'MULTIPLE_CHOICE' | 'TRUE_FALSE';

interface QuizChoiceDraft {
  readonly id: number;
  readonly text: string;
  readonly isCorrect: boolean;
}

interface QuizQuestionDraft {
  readonly id: number;
  readonly text: string;
  readonly type: QuizQuestionType;
  readonly choices: readonly QuizChoiceDraft[];
}

interface CourseOption {
  readonly id: string;
  readonly title: string;
  readonly status: string;
}

type CoursePageState =
  | { readonly status: 'loading' }
  | { readonly status: 'error'; readonly message: string }
  | {
      readonly status: 'loaded';
      readonly options: readonly CourseOption[];
      readonly page: number;
      readonly totalPages: number;
      readonly hasUnrepresentableIds: boolean;
    };

type SaveStatus = 'idle' | 'saving' | 'success' | 'error' | 'unconfirmed';

const COURSE_LOADING: CoursePageState = { status: 'loading' };
const QUESTION_TYPES: readonly QuizQuestionType[] = [
  'SINGLE_CHOICE',
  'MULTIPLE_CHOICE',
  'TRUE_FALSE',
];

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad16-page',
  templateUrl: './ad16-page.html',
})
export class AD16Page {
  readonly definition = AD16_SCREEN;
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly api = inject(AD16ApiService);
  readonly quizId = signal(this.route.snapshot.paramMap.get('quizId'));
  readonly courseQuery = signal({ page: 1, refresh: 0 });
  readonly courseState = toSignal(
    toObservable(this.courseQuery).pipe(
      switchMap(({ page }) => this.isEditMode
        ? of<CoursePageState>({ status: 'error', message: 'Chế độ chỉnh sửa đang khóa.' })
        : this.api.getCourses(page).pipe(
            map((envelope) => coursePageState(envelope, page)),
            startWith(COURSE_LOADING),
            catchError((error: unknown) => of<CoursePageState>({
              status: 'error',
              message: adminDataError(error).message ?? 'Không thể tải danh sách khóa học.',
            })),
          )),
    ),
    { initialValue: COURSE_LOADING },
  );

  readonly selectedCourse = signal<CourseOption | null>(null);
  readonly questions = signal<readonly QuizQuestionDraft[]>([]);
  readonly saveStatus = signal<SaveStatus>('idle');
  readonly saveMessage = signal('');

  titleDraft = '';
  durationDraft = '';
  passingScoreDraft = '';

  private nextQuestionId = 1;
  private nextChoiceId = 1;

  get isEditMode(): boolean {
    return this.quizId() !== null;
  }

  get isQuizIdValid(): boolean {
    const quizId = this.quizId();
    return quizId === null || isPositiveSignedInt64(quizId);
  }

  get isDraftLocked(): boolean {
    return this.isEditMode || this.saveStatus() === 'saving'
      || this.saveStatus() === 'success' || this.saveStatus() === 'unconfirmed';
  }

  get canSaveQuiz(): boolean {
    return !this.isDraftLocked && this.courseState().status === 'loaded'
      && this.selectedCourse() !== null;
  }

  get isSelectedCourseOnCurrentPage(): boolean {
    const selected = this.selectedCourse();
    const state = this.courseState();
    return selected !== null && state.status === 'loaded'
      && state.options.some((course) => course.id === selected.id);
  }

  get needsCoursePageRecovery(): boolean {
    const state = this.courseState();
    return state.status === 'loaded' && state.page > Math.max(1, state.totalPages);
  }

  get titleLength(): number {
    return Array.from(this.titleDraft).length;
  }

  updateDraft(field: DraftField, event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLInputElement)) return;
    this[field] = event.target.value;
    this.clearSaveError();
  }

  updateCourse(event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLSelectElement)) return;
    const id = event.target.value;
    const state = this.courseState();
    this.selectedCourse.set(state.status === 'loaded'
      ? state.options.find((course) => course.id === id) ?? null
      : null);
    this.clearSaveError();
  }

  refreshCourses(): void {
    this.courseQuery.update((query) => ({ ...query, refresh: query.refresh + 1 }));
  }

  changeCoursePage(page: number): void {
    const state = this.courseState();
    if (state.status !== 'loaded' || !Number.isSafeInteger(page)
      || page < 1 || page > Math.max(1, state.totalPages)) {
      return;
    }
    this.courseQuery.update((query) => ({ ...query, page }));
  }

  recoverCoursePage(): void {
    const state = this.courseState();
    if (state.status === 'loaded' && this.needsCoursePageRecovery) {
      this.changeCoursePage(Math.max(1, state.totalPages));
    }
  }

  addQuestion(): void {
    if (this.isDraftLocked) return;
    const id = this.nextQuestionId++;
    this.questions.update((questions) => [...questions, {
      id,
      text: '',
      type: 'SINGLE_CHOICE',
      choices: [],
    }]);
    this.clearSaveError();
  }

  removeQuestion(questionId: number): void {
    if (this.isDraftLocked) return;
    this.questions.update((questions) => questions.filter((question) => question.id !== questionId));
    this.clearSaveError();
  }

  updateQuestionText(questionId: number, event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLInputElement)) return;
    const text = event.target.value;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? { ...question, text }
      : question));
    this.clearSaveError();
  }

  updateQuestionType(questionId: number, event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLSelectElement)) return;
    const value = event.target.value;
    if (!QUESTION_TYPES.includes(value as QuizQuestionType)) return;
    const type = value as QuizQuestionType;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? { ...question, type }
      : question));
    this.clearSaveError();
  }

  addChoice(questionId: number): void {
    if (this.isDraftLocked) return;
    const id = this.nextChoiceId++;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? { ...question, choices: [...question.choices, { id, text: '', isCorrect: false }] }
      : question));
    this.clearSaveError();
  }

  removeChoice(questionId: number, choiceId: number): void {
    if (this.isDraftLocked) return;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? { ...question, choices: question.choices.filter((choice) => choice.id !== choiceId) }
      : question));
    this.clearSaveError();
  }

  updateChoiceText(questionId: number, choiceId: number, event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLInputElement)) return;
    const text = event.target.value;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? {
          ...question,
          choices: question.choices.map((choice) => choice.id === choiceId
            ? { ...choice, text }
            : choice),
        }
      : question));
    this.clearSaveError();
  }

  updateChoiceCorrect(questionId: number, choiceId: number, event: Event): void {
    if (this.isDraftLocked || !(event.target instanceof HTMLInputElement)) return;
    const isCorrect = event.target.checked;
    this.questions.update((questions) => questions.map((question) => question.id === questionId
      ? {
          ...question,
          choices: question.choices.map((choice) => choice.id === choiceId
            ? { ...choice, isCorrect }
            : choice),
        }
      : question));
    this.clearSaveError();
  }

  saveQuiz(event: Event): void {
    event.preventDefault();
    if (!this.canSaveQuiz) return;

    const course = this.selectedCourse();
    const courseId = course ? normalizeSignedInt64(course.id) : null;
    if (courseId === null) {
      this.showSaveError('Hãy chọn khóa học có mã số biểu diễn chính xác.');
      return;
    }
    if (!this.titleDraft.trim()) {
      this.showSaveError('Hãy nhập tên bài kiểm tra.');
      return;
    }
    if (this.titleLength > 200) {
      this.showSaveError('Tên bài kiểm tra vượt quá 200 ký tự theo giới hạn của máy chủ.');
      return;
    }

    const duration = this.durationDraft === ''
      ? null
      : normalizeSignedInt32(this.durationDraft);
    if (this.durationDraft !== '' && duration === null) {
      this.showSaveError('Thời lượng phải là số nguyên signed 32-bit hoặc để trống.');
      return;
    }
    if (!isPassingScore(this.passingScoreDraft)) {
      this.showSaveError('Điểm đạt phải là chuỗi số thập phân tối đa hai chữ số lẻ và biểu diễn được bằng NUMERIC(5,2).');
      return;
    }

    const config = `{"course_id":${courseId},"title":${JSON.stringify(this.titleDraft)},"duration_minutes":${duration === null ? 'null' : duration},"passing_score":${JSON.stringify(this.passingScoreDraft)}}`;
    const questions = JSON.stringify(this.questions().map((question) => ({
      text: question.text,
      type: question.type,
      choices: question.choices.map((choice) => ({
        text: choice.text,
        is_correct: choice.isCorrect,
      })),
    })));

    this.saveStatus.set('saving');
    this.saveMessage.set('');
    this.api.createQuiz({ config, questions }).pipe(
      takeUntilDestroyed(this.destroyRef),
    ).subscribe({
      next: (response) => {
        const envelope = response.body;
        if (response.status !== 201 || !envelope) {
          this.saveStatus.set('unconfirmed');
          this.saveMessage.set('Phản hồi không xác nhận đúng HTTP 201 của API #88. Hãy kiểm tra AD-15 trước khi gửi lại để tránh tạo trùng.');
          return;
        }
        if (envelope.success === true && envelope.businessCode === 'DESIGN_RESOURCE_CREATED'
          && isCreatedQuiz(envelope.data)) {
          this.saveStatus.set('success');
          this.saveMessage.set('Bài kiểm tra đã được tạo. Mở danh sách AD-15 để xem dữ liệu đã lưu.');
          return;
        }
        if (envelope.success === true) {
          this.saveStatus.set('unconfirmed');
          this.saveMessage.set('Yêu cầu đã được chấp nhận nhưng phản hồi không khớp contract #88. Hãy kiểm tra AD-15 trước khi gửi lại để tránh tạo trùng.');
          return;
        }
        this.showSaveError('Study Server không xác nhận việc tạo bài kiểm tra.');
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 0) {
          this.saveStatus.set('unconfirmed');
          this.saveMessage.set('Không xác định được máy chủ đã nhận yêu cầu hay chưa. Hãy kiểm tra AD-15 trước khi gửi lại.');
          return;
        }
        this.showSaveError(createErrorMessage(error));
      },
    });
  }

  constructor() {
    const routeParamMap = this.route.paramMap;
    routeParamMap?.pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => {
        const quizId = params.get('quizId');
        if (this.quizId() === quizId) return;
        this.quizId.set(quizId);
        this.courseQuery.update((query) => ({ ...query, refresh: query.refresh + 1 }));
      });
  }

  private clearSaveError(): void {
    if (this.saveStatus() === 'error') {
      this.saveStatus.set('idle');
      this.saveMessage.set('');
    }
  }

  private showSaveError(message: string): void {
    this.saveStatus.set('error');
    this.saveMessage.set(message);
  }
}

function coursePageState(
  envelope: ApiEnvelope<AdminPage<AdminCourse>>,
  requestedPage: number,
): CoursePageState {
  if (envelope.success !== true || envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
    return { status: 'error', message: 'Study Server không thể tải danh sách khóa học.' };
  }

  const page = envelope.data;
  if (!isAdminCoursePage(page, requestedPage) || hasAdminPageCountMismatch(page)) {
    return { status: 'error', message: 'Phản hồi danh sách khóa học không khớp contract #73.' };
  }

  const pagination = page.pagination;
  const exactCourses = page.items.filter((course) => Number.isSafeInteger(course.id));
  return {
    status: 'loaded',
    options: exactCourses.map((course) => ({
      id: String(course.id),
      title: course.title,
      status: course.status,
    })),
    page: pagination.page,
    totalPages: pagination.total_pages,
    hasUnrepresentableIds: exactCourses.length !== page.items.length,
  };
}

function isCreatedQuiz(value: unknown): boolean {
  if (!isRecord(value)) return false;
  const duration = value['duration_minutes'];
  const questions = value['questions'];
  return Number.isInteger(value['id'])
    && Number.isInteger(value['course_id'])
    && typeof value['title'] === 'string'
    && (duration === undefined || duration === null || Number.isInteger(duration))
    && typeof value['passing_score'] === 'string'
    && Array.isArray(questions)
    && questions.every(isRecord);
}

function createErrorMessage(error: unknown): string {
  if (error instanceof AdminSessionError && error.code === 'LOGIN_REQUIRED') {
    return 'Phiên Admin không còn hiệu lực. Hãy đăng nhập lại.';
  }
  if (error instanceof HttpErrorResponse) {
    if (error.status === 401) return 'Phiên Admin đã hết hiệu lực. Hãy đăng nhập lại.';
    if (error.status === 403) return 'Tài khoản không được phép tạo bài kiểm tra.';
    if (error.status === 422) return 'Study Server từ chối dữ liệu. Kiểm tra khóa học, cấu hình và cấu trúc câu hỏi.';
    return 'Không thể tạo bài kiểm tra lúc này. Hãy thử lại sau.';
  }
  return 'Không thể tạo bài kiểm tra lúc này. Hãy thử lại sau.';
}

function normalizeSignedInt64(value: string): string | null {
  const match = /^([+-]?)([0-9]+)$/.exec(value);
  if (match?.[0] !== value) return null;
  return normalizeSignedInteger(match[1], match[2], '9223372036854775807', '9223372036854775808');
}

function normalizeSignedInt32(value: string): number | null {
  const match = /^([+-]?)([0-9]+)$/.exec(value);
  if (match?.[0] !== value) return null;
  const normalized = normalizeSignedInteger(match[1], match[2], '2147483647', '2147483648');
  return normalized === null ? null : Number(normalized);
}

function normalizeSignedInteger(
  sign: string,
  rawDigits: string,
  maxPositive: string,
  maxNegative: string,
): string | null {
  const digits = rawDigits.replace(/^0+/, '') || '0';
  const negative = sign === '-';
  const max = negative ? maxNegative : maxPositive;
  if (digits.length > max.length || (digits.length === max.length && digits > max)) {
    return null;
  }
  return digits === '0' ? '0' : `${negative ? '-' : ''}${digits}`;
}

function isPassingScore(value: string): boolean {
  const match = /^[+-]?[0-9]+(?:\.[0-9]{1,2})?$/.exec(value);
  if (match?.[0] !== value) return false;
  const parsed = Number(value);
  return Number.isFinite(parsed) && Math.abs(parsed) <= 999.99;
}

function isPositiveSignedInt64(value: string): boolean {
  const match = /^[0-9]+$/.exec(value);
  if (match?.[0] !== value || value.length > 19 || !/[1-9]/.test(value)) {
    return false;
  }

  const max = '9223372036854775807';
  return value.length < max.length || (value.length === max.length && value <= max);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
