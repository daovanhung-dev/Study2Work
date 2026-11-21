import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  Component,
  DestroyRef,
  ElementRef,
  OnInit,
  ViewChild,
  inject,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import type { CanDeactivateFn } from '@angular/router';
import {
  EMPTY,
  Observable,
  Subject,
  catchError,
  distinctUntilChanged,
  finalize,
  filter,
  map,
  merge,
  of,
  switchMap,
  tap,
} from 'rxjs';
import type { ApiEnvelope } from '../../../../core/http/api-envelope';

import { ME04LectureCreateService } from '../data-access/me04-lecture-create.service';
import type {
  MentorCourse,
  MentorLecture,
  MentorPage,
  MentorUploadAsset,
} from '../../shared/models/mentor-api.models';
import { toSafeMentorId } from '../../shared/models/mentor-api.models';
import { mentorApiErrorMessage } from '../../shared/models/mentor-api-errors';
import { MentorPageHeader } from '../../shared/ui/mentor-page-header';

interface SelectedLectureFile {
  key: number;
  file: File;
  asset: MentorUploadAsset | null;
  error: string | null;
  retryBlocked: boolean;
}

@Component({
  imports: [FormsModule, RouterLink, MentorPageHeader],
  selector: 'study-me04-page',
  styleUrls: ['./me04-page.css', '../../shared/ui/mentor-pages.css'],
  templateUrl: './me04-page.html',
})
export class ME04Page implements OnInit {
  private readonly data = inject(ME04LectureCreateService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly retryCourses$ = new Subject<void>();
  private nextFileKey = 0;
  private courseRouteInitialized = false;

  @ViewChild('contentEditor') private contentEditor?: ElementRef<HTMLTextAreaElement>;

  readonly courseId = signal('');
  readonly courses = signal<MentorCourse[]>([]);
  readonly title = signal('');
  readonly content = signal('');
  readonly order = signal('0');
  readonly selectedFiles = signal<SelectedLectureFile[]>([]);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly formError = signal<string | null>(null);
  readonly createError = signal<string | null>(null);
  readonly createMessage = signal<string | null>(null);
  readonly navigationError = signal(false);
  readonly invalidId = signal(false);
  readonly uploadingKey = signal<number | null>(null);
  readonly creating = signal(false);
  readonly createOutcomeUnknown = signal(false);
  readonly createdLectureId = signal<string | null>(null);

  ngOnInit(): void {
    const routeCourseIds$ = this.route.paramMap.pipe(
      map((params) => toSafeMentorId(params.get('courseId'))),
      distinctUntilChanged(),
      filter((id) => this.acceptCourseRoute(id)),
      tap((id) => this.resetForCourse(id)),
    );
    const retryCourseIds$ = this.retryCourses$.pipe(
      map(() => toSafeMentorId(this.courseId())),
      tap((id) => {
        if (id) {
          this.loading.set(true);
          this.error.set(null);
        }
      }),
    );

    merge(routeCourseIds$, retryCourseIds$)
      .pipe(
        switchMap((id) => {
          if (!id) return EMPTY;
          return capture(this.data.courses()).pipe(map((result) => ({ id, result })));
        }),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(({ id, result }) => {
        if (id !== this.courseId()) return;
        this.loading.set(false);
        if (!result.ok) {
          this.error.set(mentorApiErrorMessage(result.error));
          return;
        }
        const response = result.response;
        if (
          !response.success ||
          response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED' ||
          !isCoursePage(response.data)
        ) {
          this.error.set(response.message || 'Study Server trả về danh sách khóa học không hợp lệ.');
          return;
        }
        this.courses.set(response.data.items);
      });
  }

  load(): void {
    if (this.courseId()) this.retryCourses$.next();
  }

  selectCourse(event: Event): void {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement)) return;
    const value = target.value;
    const id = toSafeMentorId(value);
    if (!id || id === this.courseId() || !this.courses().some((course) => toSafeMentorId(course.id) === id)) {
      return;
    }
    void this.router.navigate(['/mentor/courses', id, 'lectures', 'new']);
  }

  courseListed(): boolean {
    const selectedId = this.courseId();
    return this.courses().some((course) => toSafeMentorId(course.id) === selectedId);
  }

  setOrder(value: number | null): void {
    this.order.set(value === null ? '' : String(value));
  }

  applyInlineMarkdown(prefix: string, suffix: string, placeholder: string): void {
    const editor = this.contentEditor?.nativeElement;
    if (!editor || this.creating() || this.createdLectureId()) return;

    const source = editor.value;
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const selected = source.slice(start, end);
    const body = selected || placeholder;
    const replacement = `${prefix}${body}${suffix}`;
    const nextValue = `${source.slice(0, start)}${replacement}${source.slice(end)}`;
    this.content.set(nextValue);
    this.restoreEditorSelection(nextValue, start + prefix.length, start + prefix.length + body.length);
  }

  applyMarkdownLinePrefix(prefix: string, placeholder: string): void {
    const editor = this.contentEditor?.nativeElement;
    if (!editor || this.creating() || this.createdLectureId()) return;

    const source = editor.value;
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const blockStart = start === 0 ? 0 : source.lastIndexOf('\n', start - 1) + 1;
    const nextBreak = source.indexOf('\n', end);
    const blockEnd = nextBreak === -1 ? source.length : nextBreak;
    const block = source.slice(blockStart, blockEnd) || placeholder;
    const replacement = block
      .split('\n')
      .map((line) => `${prefix}${line}`)
      .join('\n');
    const nextValue = `${source.slice(0, blockStart)}${replacement}${source.slice(blockEnd)}`;
    this.content.set(nextValue);
    this.restoreEditorSelection(nextValue, blockStart + prefix.length, blockStart + replacement.length);
  }

  backToWorkspace(): void {
    if (this.creating() || this.uploadingKey() !== null) return;
    void this.router.navigate(['/mentor/courses', this.courseId()]);
  }

  canDeactivate(): boolean {
    if (!this.hasPendingWrite()) return true;
    this.formError.set('Đang ghi dữ liệu lên máy chủ. Hãy chờ request hoàn tất trước khi rời màn hình.');
    return false;
  }

  addFiles(event: Event): void {
    const input = event.target;
    if (!(input instanceof HTMLInputElement)) return;
    const files = Array.from(input.files ?? []);
    input.value = '';
    if (!files.length) return;

    const next = this.nextFileKey;
    this.nextFileKey += files.length;
    this.selectedFiles.update((current) => [
      ...current,
      ...files.map((file, index) => ({
        key: next + index,
        file,
        asset: null,
        error: null,
        retryBlocked: false,
      })),
    ]);
    this.formError.set(null);
  }

  uploadFile(key: number): void {
    const fileEntry = this.selectedFiles().find((item) => item.key === key);
    const courseId = this.courseId();
    if (
      !fileEntry ||
      fileEntry.asset ||
      fileEntry.retryBlocked ||
      !courseId ||
      this.uploadingKey() !== null ||
      this.creating() ||
      this.createdLectureId()
    ) {
      return;
    }

    this.uploadingKey.set(key);
    this.formError.set(null);
    this.updateFile(key, (item) => ({ ...item, error: null }));
    this.data
      .upload(fileEntry.file, courseId)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => {
          if (this.uploadingKey() === key) this.uploadingKey.set(null);
        }),
      )
      .subscribe({
        next: (response) => {
          if (this.courseId() !== courseId) return;
          if (
            response.success &&
            response.businessCode === 'DESIGN_RESOURCE_CREATED' &&
            isUploadAsset(response.data)
          ) {
            this.updateFile(key, (item) => ({ ...item, asset: response.data, error: null }));
            return;
          }
          this.updateFile(key, (item) => ({
            ...item,
            error: response.message || 'Study Server chưa xác nhận file đã tải lên.',
            retryBlocked: response.success,
          }));
        },
        error: (error: unknown) => {
          if (this.courseId() !== courseId) return;
          this.updateFile(key, (item) => ({
            ...item,
            error: mentorApiErrorMessage(error),
            retryBlocked: isAmbiguousWriteFailure(error),
          }));
        },
      });
  }

  removeFile(key: number): void {
    if (this.uploadingKey() === key || this.creating() || this.createdLectureId()) return;
    const removed = this.selectedFiles().find((item) => item.key === key);
    this.selectedFiles.update((items) => items.filter((item) => item.key !== key));
    if (removed?.asset) {
      this.formError.set('File đã tải lên vẫn được lưu trên máy chủ; thao tác này chỉ bỏ file khỏi lecture mới.');
    }
  }

  createLecture(): void {
    if (this.creating()) return;

    const courseId = this.courseId();
    const title = this.title();
    const content = this.content();
    const order = parseInt32(this.order());
    const files = this.selectedFiles();

    this.formError.set(null);
    this.createError.set(null);
    if (!courseId) {
      this.formError.set('Không có course ID hợp lệ trên đường dẫn.');
      return;
    }
    if (!title.trim() || title.length > 200) {
      this.formError.set('Nhập tiêu đề bài giảng tối đa 200 ký tự.');
      return;
    }
    if (!content.trim()) {
      this.formError.set('Nhập nội dung Markdown cho bài giảng.');
      return;
    }
    if (order === null) {
      this.formError.set('Thứ tự phải là số nguyên trong giới hạn int32.');
      return;
    }
    if (this.uploadingKey() !== null || files.some((item) => item.asset === null)) {
      this.formError.set('Tải lên hoặc bỏ khỏi danh sách các file đã chọn trước khi tạo lecture.');
      return;
    }
    if (this.createOutcomeUnknown() || this.createdLectureId()) {
      this.formError.set('Không thể gửi lại yêu cầu tạo lecture chưa xác định kết quả.');
      return;
    }

    const assetIds = files.map((item) => toSafeMentorId(item.asset?.id));
    if (assetIds.some((id) => id === null) || new Set(assetIds).size !== assetIds.length) {
      this.formError.set('Study Server trả về ID file không hợp lệ hoặc bị trùng.');
      return;
    }
    const assetRefs = `[${assetIds.join(',')}]`;
    const payload = { title, content, asset_refs: assetRefs, order };
    this.creating.set(true);
    this.data
      .create(courseId, payload)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        finalize(() => this.creating.set(false)),
      )
      .subscribe({
        next: (response) => {
          if (this.courseId() !== courseId) return;
          if (
            response.success &&
            response.businessCode === 'DESIGN_RESOURCE_CREATED' &&
            isCreatedLecture(response.data, courseId, payload, files)
          ) {
            const lectureId = toSafeMentorId(response.data.id);
            if (!lectureId) {
              this.createOutcomeUnknown.set(true);
              this.createError.set('Lecture đã được tạo nhưng ID phản hồi không thể dùng an toàn.');
              return;
            }
            this.createdLectureId.set(lectureId);
            this.createMessage.set('Bài giảng đã được tạo và xuất bản.');
            this.openLecture(lectureId);
            return;
          }

          if (response.success) {
            this.createOutcomeUnknown.set(true);
            const returnedId = response.data && toSafeMentorId(response.data.id);
            if (returnedId) this.createdLectureId.set(returnedId);
            this.createError.set(
              response.message || 'Study Server đã nhận yêu cầu nhưng phản hồi chưa thể xác nhận lecture.',
            );
            return;
          }
          this.createError.set(response.message || 'Study Server chưa tạo lecture.');
        },
        error: (error: unknown) => {
          if (this.courseId() !== courseId) return;
          this.createError.set(mentorApiErrorMessage(error));
          this.createOutcomeUnknown.set(isAmbiguousWriteFailure(error));
        },
      });
  }

  private resetForCourse(id: string | null): void {
    this.courseId.set(id ?? '');
    this.courses.set([]);
    this.loading.set(id !== null);
    this.error.set(null);
    this.invalidId.set(id === null);
    this.title.set('');
    this.content.set('');
    this.order.set('0');
    this.selectedFiles.set([]);
    this.uploadingKey.set(null);
    this.creating.set(false);
    this.createError.set(null);
    this.createMessage.set(null);
    this.navigationError.set(false);
    this.createOutcomeUnknown.set(false);
    this.createdLectureId.set(null);
    this.formError.set(null);
  }

  private acceptCourseRoute(id: string | null): boolean {
    if (!this.courseRouteInitialized) {
      this.courseRouteInitialized = true;
      return true;
    }
    if ((id ?? '') === this.courseId()) return false;
    if (!this.hasPendingWrite()) return true;

    this.formError.set('Đang ghi dữ liệu lên máy chủ. Hãy chờ request hoàn tất trước khi đổi khóa học.');
    void this.router.navigate(['/mentor/courses', this.courseId(), 'lectures', 'new']);
    return false;
  }

  private hasPendingWrite(): boolean {
    return this.uploadingKey() !== null || (this.creating() && !this.createdLectureId());
  }

  private updateFile(key: number, update: (item: SelectedLectureFile) => SelectedLectureFile): void {
    this.selectedFiles.update((items) =>
      items.map((item) => (item.key === key ? update(item) : item)),
    );
  }

  private openLecture(lectureId: string): void {
    void this.router.navigate(['/mentor/lectures', lectureId]).then(
      (navigated) => this.navigationError.set(!navigated),
      () => this.navigationError.set(true),
    );
  }

  private restoreEditorSelection(value: string, start: number, end: number): void {
    requestAnimationFrame(() => {
      const editor = this.contentEditor?.nativeElement;
      if (!editor || this.content() !== value) return;
      editor.focus();
      editor.setSelectionRange(start, end);
    });
  }
}

export const blockME04DepartureDuringWrite: CanDeactivateFn<ME04Page> = (page) =>
  page.canDeactivate();

type RequestResult<T> =
  | { ok: true; response: ApiEnvelope<T> }
  | { ok: false; error: unknown };

function capture<T>(request: Observable<ApiEnvelope<T>>): Observable<RequestResult<T>> {
  return request.pipe(
    map((response): RequestResult<T> => ({ ok: true, response })),
    catchError((error: unknown) => of<RequestResult<T>>({ ok: false, error })),
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isCoursePage(value: unknown): value is MentorPage<MentorCourse> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }
  const pagination = value['pagination'];
  const total = pagination['total'];
  return (
    pagination['page'] === 1 &&
    pagination['size'] === 100 &&
    value['items'].length <= 100 &&
    Number.isSafeInteger(total) &&
    Number(total) >= 0 &&
    pagination['total_pages'] === (Number(total) > 0 ? Math.ceil(Number(total) / 100) : 0) &&
    value['items'].every(
      (item) =>
        isRecord(item) &&
        toSafeMentorId(item['id']) !== null &&
        typeof item['title'] === 'string' &&
        typeof item['status'] === 'string',
    )
  );
}

function isUploadAsset(value: unknown): value is MentorUploadAsset {
  return (
    isRecord(value) &&
    toSafeMentorId(value['id']) !== null &&
    typeof value['name'] === 'string' &&
    typeof value['url'] === 'string' &&
    typeof value['content_type'] === 'string' &&
    Number.isSafeInteger(value['size_bytes']) &&
    Number(value['size_bytes']) >= 0 &&
    value['status'] === 'UPLOADED'
  );
}

function isCreatedLecture(
  value: unknown,
  courseId: string,
  payload: { title: string; content: string; asset_refs: string; order: number },
  files: SelectedLectureFile[],
): value is MentorLecture {
  if (
    !isRecord(value) ||
    toSafeMentorId(value['id']) === null ||
    toSafeMentorId(value['course_id']) !== courseId ||
    value['title'] !== payload.title ||
    value['content'] !== payload.content ||
    value['order'] !== payload.order ||
    value['status'] !== 'PUBLISHED' ||
    !Array.isArray(value['assets']) ||
    value['assets'].length !== files.length ||
    !value['assets'].every(isUploadAsset)
  ) {
    return false;
  }
  return value['assets'].every((asset, index) => {
    const expectedId = toSafeMentorId(files[index].asset?.id);
    return expectedId !== null && toSafeMentorId(asset.id) === expectedId;
  });
}

function parseInt32(value: string): number | null {
  if (!/^-?\d+$/.test(value)) return null;
  try {
    const parsed = BigInt(value);
    if (parsed < -(2n ** 31n) || parsed > 2n ** 31n - 1n) return null;
    return Number(parsed);
  } catch {
    return null;
  }
}

function isAmbiguousWriteFailure(error: unknown): boolean {
  return error instanceof HttpErrorResponse && (error.status === 0 || error.status >= 500);
}
