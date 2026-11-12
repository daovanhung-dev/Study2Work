import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Me07EditorService } from '../data-access/me07-editor.service';
import {
  SUPPORTED_CONTENT_TYPES,
  type Me07ContentNodeDto,
  type Me07EditorDraftVm,
  type Me07EditorMode,
  buildPayloadFromDraft,
  extractDraftFromNode,
  isDraftDirty,
  parseMe07Int64Param,
} from '../models/me07-editor.models';
import { Me07GuidelinesAside } from '../ui/me07-guidelines-aside';
import { Me07Header } from '../ui/me07-header';

export type Me07ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'ready'
  | 'saving'
  | 'saved'
  | 'not-found'
  | 'forbidden'
  | 'unauthorized'
  | 'error';

const EMPTY_DRAFT: Me07EditorDraftVm = {
  title: '',
  contentType: 'LESSON',
  summaryText: '',
  bodyText: '',
};

@Component({
  imports: [Me07Header, Me07GuidelinesAside],
  selector: 'study-me07-page',
  styleUrl: './me07-page.css',
  templateUrl: './me07-page.html',
})
export class ME07Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly editorService = inject(Me07EditorService);

  readonly contentTypes = SUPPORTED_CONTENT_TYPES;
  readonly courseId = signal<number | null>(null);
  readonly contentId = signal<number | null>(null);
  readonly mode = signal<Me07EditorMode>('create');
  readonly screenState = signal<Me07ScreenState>('ready');

  readonly currentNode = signal<Me07ContentNodeDto | null>(null);
  readonly initialDraft = signal<Me07EditorDraftVm>(EMPTY_DRAFT);
  readonly currentDraft = signal<Me07EditorDraftVm>(EMPTY_DRAFT);

  readonly validationError = signal<string>('');
  readonly statusMessage = signal<string>('');
  readonly showCancelConfirm = signal<boolean>(false);

  readonly isDirty = computed<boolean>(() =>
    isDraftDirty(this.initialDraft(), this.currentDraft()),
  );

  ngOnInit(): void {
    const rawCourseId = this.route.snapshot.paramMap.get('courseId');
    const parsedCourseId = parseMe07Int64Param(rawCourseId);
    if (parsedCourseId === null) {
      this.screenState.set('invalid-param');
      this.statusMessage.set('Mã khóa học (courseId) không phải số nguyên int64 hợp lệ.');
      return;
    }
    this.courseId.set(parsedCourseId);

    const rawContentId = this.route.snapshot.paramMap.get('contentId');
    if (!rawContentId || rawContentId === 'new') {
      this.mode.set('create');
      this.contentId.set(null);
      this.initialDraft.set({ ...EMPTY_DRAFT });
      this.currentDraft.set({ ...EMPTY_DRAFT });
      this.screenState.set('ready');
      return;
    }

    const parsedContentId = parseMe07Int64Param(rawContentId);
    if (parsedContentId === null) {
      this.screenState.set('invalid-param');
      this.statusMessage.set('Mã nội dung (contentId) không phải số nguyên int64 hợp lệ.');
      return;
    }

    this.mode.set('edit');
    this.contentId.set(parsedContentId);
    this.loadExistingNode(parsedCourseId, parsedContentId);
  }

  onTitleInput(event: Event): void {
    const value = (event.target as HTMLInputElement | null)?.value ?? '';
    this.currentDraft.update((prev) => ({ ...prev, title: value }));
    this.validationError.set('');
  }

  onContentTypeChange(event: Event): void {
    const value = (event.target as HTMLSelectElement | null)?.value ?? 'LESSON';
    this.currentDraft.update((prev) => ({ ...prev, contentType: value }));
  }

  onSummaryInput(event: Event): void {
    const value = (event.target as HTMLTextAreaElement | null)?.value ?? '';
    this.currentDraft.update((prev) => ({ ...prev, summaryText: value }));
  }

  onBodyInput(event: Event): void {
    const value = (event.target as HTMLTextAreaElement | null)?.value ?? '';
    this.currentDraft.update((prev) => ({ ...prev, bodyText: value }));
  }

  submitForm(): void {
    const cId = this.courseId();
    if (cId === null) {
      return;
    }

    const draft = this.currentDraft();
    const trimmedTitle = draft.title.trim();
    if (!trimmedTitle) {
      this.validationError.set('Tiêu đề nội dung là trường bắt buộc.');
      return;
    }

    this.validationError.set('');
    this.statusMessage.set('');
    this.screenState.set('saving');

    const payload = buildPayloadFromDraft(draft, this.currentNode()?.payload ?? {});

    if (this.mode() === 'create') {
      this.editorService
        .createContent({
          course_id: cId,
          content_type: draft.contentType,
          title: trimmedTitle,
          payload,
        })
        .subscribe({
          next: (envelope) => {
            const created = envelope.data;
            this.currentNode.set(created);
            const updatedDraft = extractDraftFromNode(created);
            this.initialDraft.set(updatedDraft);
            this.currentDraft.set(updatedDraft);
            this.screenState.set('saved');
            this.statusMessage.set(
              `Đã tạo nội dung #${created.id} ở trạng thái ${created.status} (API #50).`,
            );
          },
          error: (err: unknown) => this.handleMutationError(err),
        });
      return;
    }

    const targetContentId = this.contentId();
    if (targetContentId === null) {
      return;
    }

    this.editorService
      .updateContent(targetContentId, {
        content_type: draft.contentType,
        title: trimmedTitle,
        payload,
      })
      .subscribe({
        next: (envelope) => {
          const updated = envelope.data;
          this.currentNode.set(updated);
          const updatedDraft = extractDraftFromNode(updated);
          this.initialDraft.set(updatedDraft);
          this.currentDraft.set(updatedDraft);
          this.screenState.set('saved');
          this.statusMessage.set(
            `Đã lưu phiên bản mới cho nội dung #${updated.id} (${updated.status}, API #51).`,
          );
        },
        error: (err: unknown) => this.handleMutationError(err),
      });
  }

  requestCancelOrBack(): void {
    if (this.isDirty()) {
      this.showCancelConfirm.set(true);
      return;
    }
    this.navigateToTree();
  }

  confirmDiscardAndLeave(): void {
    this.showCancelConfirm.set(false);
    this.navigateToTree();
  }

  dismissCancelDialog(): void {
    this.showCancelConfirm.set(false);
  }

  navigateToTree(): void {
    const cId = this.courseId();
    if (cId !== null) {
      void this.router.navigate(['/mentor/courses', cId, 'content']);
    }
  }

  openPublishOrDeleteActions(): void {
    const cId = this.courseId();
    const targetId = this.currentNode()?.id ?? this.contentId();
    if (cId === null || targetId === null) {
      return;
    }
    void this.router.navigate(['/mentor/content', targetId, 'actions'], {
      queryParams: { courseId: cId, action: 'publish' },
    });
  }

  private loadExistingNode(courseId: number, contentId: number): void {
    this.screenState.set('loading');
    this.statusMessage.set('');

    this.editorService.getCourseContents(courseId).subscribe({
      next: (envelope) => {
        const list = Array.isArray(envelope.data) ? envelope.data : [];
        const match = list.find((item) => item.id === contentId) ?? null;
        if (!match) {
          this.screenState.set('not-found');
          this.statusMessage.set(
            `Không tìm thấy nội dung #${contentId} trong cây nội dung khóa học #${courseId}.`,
          );
          return;
        }
        this.currentNode.set(match);
        const draft = extractDraftFromNode(match);
        this.initialDraft.set(draft);
        this.currentDraft.set({ ...draft });
        this.screenState.set('ready');
      },
      error: (err: unknown) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status === 401) {
            this.screenState.set('unauthorized');
            this.statusMessage.set('Phiên đăng nhập giảng viên không hợp lệ (401).');
            return;
          }
          if (err.status === 403) {
            this.screenState.set('forbidden');
            this.statusMessage.set('Bạn không có quyền truy cập khóa học này (403).');
            return;
          }
          if (err.status === 404) {
            this.screenState.set('not-found');
            this.statusMessage.set('Không tìm thấy khóa học trên máy chủ (404).');
            return;
          }
        }
        this.screenState.set('error');
        this.statusMessage.set('Không thể tải dữ liệu nội dung từ API #49.');
      },
    });
  }

  private handleMutationError(err: unknown): void {
    this.screenState.set('ready');
    if (err instanceof HttpErrorResponse) {
      const body = err.error as { message?: string } | null;
      if (err.status === 422) {
        this.validationError.set(
          body?.message ?? 'Dữ liệu gửi lên không hợp lệ (422). Bản nháp của bạn vẫn được giữ nguyên.',
        );
        return;
      }
      if (err.status === 403) {
        this.validationError.set('Bạn không có quyền ghi nội dung vào khóa học này (403).');
        return;
      }
      if (err.status === 404) {
        this.validationError.set('Không tìm thấy nội dung hoặc khóa học đích (404).');
        return;
      }
      this.validationError.set(body?.message ?? 'Lỗi máy chủ khi lưu nội dung. Bản nháp vẫn được giữ nguyên.');
      return;
    }
    this.validationError.set('Không thể kết nối máy chủ khi lưu nội dung.');
  }
}
