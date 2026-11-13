import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Me08ActionsService } from '../data-access/me08-actions.service';
import {
  type DeleteResultDto,
  type Me08ActionIntent,
  type Me08ContentNodeDto,
  type Me08TargetInspectionVm,
  inspectTargetContent,
  parseMe08Int64Param,
} from '../models/me08-actions.models';
import { Me08ActionCards } from '../ui/me08-action-cards';
import { Me08TargetSummary } from '../ui/me08-target-summary';

export type Me08ScreenState =
  | 'invalid-param'
  | 'missing-course-context'
  | 'loading'
  | 'ready'
  | 'processing'
  | 'mutation-success'
  | 'refresh-error'
  | 'not-found'
  | 'forbidden'
  | 'unauthorized'
  | 'error';

@Component({
  imports: [Me08TargetSummary, Me08ActionCards],
  selector: 'study-me08-page',
  styleUrl: './me08-page.css',
  templateUrl: './me08-page.html',
})
export class ME08Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly actionsService = inject(Me08ActionsService);

  readonly contentId = signal<number | null>(null);
  readonly courseId = signal<number | null>(null);
  readonly activeIntent = signal<Me08ActionIntent>('publish');
  readonly isDialogMode = signal<boolean>(false);

  readonly screenState = signal<Me08ScreenState>('loading');
  readonly courseNodes = signal<readonly Me08ContentNodeDto[]>([]);
  readonly targetNode = signal<Me08ContentNodeDto | null>(null);
  readonly deleteReceipt = signal<DeleteResultDto | null>(null);

  readonly outcomeMessage = signal<string>('');
  readonly errorMessage = signal<string>('');

  readonly inspection = computed<Me08TargetInspectionVm | null>(() => {
    const node = this.targetNode();
    if (!node) {
      return null;
    }
    return inspectTargetContent(node, this.courseNodes());
  });

  ngOnInit(): void {
    const rawContentId = this.route.snapshot.paramMap.get('contentId');
    const parsedContentId = parseMe08Int64Param(rawContentId);
    if (parsedContentId === null) {
      this.screenState.set('invalid-param');
      this.errorMessage.set('Mã nội dung (contentId) trên đường dẫn không phải số nguyên int64 hợp lệ.');
      return;
    }
    this.contentId.set(parsedContentId);

    const queryMap = this.route.snapshot.queryParamMap;
    const rawAction = queryMap.get('action');
    if (rawAction === 'unpublish' || rawAction === 'delete' || rawAction === 'publish') {
      this.activeIntent.set(rawAction);
    }
    this.isDialogMode.set(queryMap.get('dialog') === '1');

    const rawCourseId = queryMap.get('courseId');
    const parsedCourseId = parseMe08Int64Param(rawCourseId);
    if (parsedCourseId === null) {
      this.screenState.set('missing-course-context');
      this.errorMessage.set(
        'Chưa có tham số ?courseId= hợp lệ để tải cây nội dung từ API #49. Không tự ý suy đoán dữ liệu.',
      );
      return;
    }

    this.courseId.set(parsedCourseId);
    this.hydrateFromCourseTree(parsedCourseId, parsedContentId);
  }

  executePublishState(published: boolean): void {
    const id = this.contentId();
    const cId = this.courseId();
    if (id === null || cId === null) {
      return;
    }

    this.screenState.set('processing');
    this.errorMessage.set('');
    this.outcomeMessage.set('');

    this.actionsService.setPublishState(id, { published }).subscribe({
      next: (envelope) => {
        const updatedNode = envelope.data;
        this.targetNode.set(updatedNode);
        this.outcomeMessage.set(
          published
            ? `Đã xuất bản nội dung #${updatedNode.id} (status = ${updatedNode.status}, PATCH #52).`
            : `Đã gỡ xuất bản nội dung #${updatedNode.id} về trạng thái ${updatedNode.status} (PATCH #52).`,
        );
        this.refreshCourseTreeAfterMutation(cId, id, false);
      },
      error: (err: unknown) => this.handleActionError(err),
    });
  }

  executeDelete(): void {
    const id = this.contentId();
    const cId = this.courseId();
    if (id === null || cId === null) {
      return;
    }

    this.screenState.set('processing');
    this.errorMessage.set('');
    this.outcomeMessage.set('');

    this.actionsService.deleteContent(id).subscribe({
      next: (envelope) => {
        this.deleteReceipt.set(envelope.data);
        this.targetNode.set(null);
        this.outcomeMessage.set(
          `Đã xóa mềm nội dung #${envelope.data.id} lúc ${envelope.data.deleted_at} (DELETE #53).`,
        );
        this.refreshCourseTreeAfterMutation(cId, id, true);
      },
      error: (err: unknown) => this.handleActionError(err),
    });
  }

  returnToTree(): void {
    const cId = this.courseId();
    if (cId !== null) {
      void this.router.navigate(['/mentor/courses', cId, 'content']);
    }
  }

  private hydrateFromCourseTree(courseId: number, contentId: number): void {
    this.screenState.set('loading');
    this.errorMessage.set('');

    this.actionsService.getCourseContents(courseId).subscribe({
      next: (envelope) => {
        const list = Array.isArray(envelope.data) ? envelope.data : [];
        this.courseNodes.set(list);
        const match = list.find((item) => item.id === contentId) ?? null;
        if (!match) {
          this.targetNode.set(null);
          this.screenState.set('not-found');
          this.errorMessage.set(
            `Không tìm thấy nội dung #${contentId} trong danh sách hoạt động của khóa học #${courseId} (#49).`,
          );
          return;
        }
        this.targetNode.set(match);
        this.screenState.set('ready');
      },
      error: (err: unknown) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status === 401) {
            this.screenState.set('unauthorized');
            this.errorMessage.set('Phiên đăng nhập giảng viên chưa xác thực (401).');
            return;
          }
          if (err.status === 403) {
            this.screenState.set('forbidden');
            this.errorMessage.set('Bạn không có quyền truy cập khóa học này (403).');
            return;
          }
          if (err.status === 404) {
            this.screenState.set('not-found');
            this.errorMessage.set('Không tìm thấy khóa học trên máy chủ (404).');
            return;
          }
        }
        this.screenState.set('error');
        this.errorMessage.set('Không thể tải dữ liệu cây nội dung từ API #49.');
      },
    });
  }

  /**
   * Theo AC của ME-08: sau khi PATCH #52 hoặc DELETE #53 thành công,
   * phải gọi lại GET #49 với courseId đã lưu và tách biệt trạng thái
   * mutation-success với refresh-error.
   */
  private refreshCourseTreeAfterMutation(
    courseId: number,
    contentId: number,
    wasDeleted: boolean,
  ): void {
    this.actionsService.getCourseContents(courseId).subscribe({
      next: (envelope) => {
        const list = Array.isArray(envelope.data) ? envelope.data : [];
        this.courseNodes.set(list);
        if (!wasDeleted) {
          const refreshed = list.find((item) => item.id === contentId) ?? this.targetNode();
          this.targetNode.set(refreshed);
        }
        this.screenState.set('mutation-success');
      },
      error: () => {
        this.screenState.set('refresh-error');
        this.errorMessage.set(
          'Thao tác cập nhật đã được máy chủ ghi nhận, nhưng việc tải lại cây nội dung (#49) bị lỗi.',
        );
      },
    });
  }

  private handleActionError(err: unknown): void {
    this.screenState.set('ready');
    if (err instanceof HttpErrorResponse) {
      const body = err.error as { message?: string } | null;
      if (err.status === 422) {
        this.errorMessage.set(
          body?.message ??
            'Nội dung chưa đáp ứng điều kiện chuyển trạng thái hoặc xóa (422 DESIGN_VALIDATION_ERROR).',
        );
        return;
      }
      if (err.status === 403) {
        this.errorMessage.set('Bạn không sở hữu khóa học chứa nội dung này (403).');
        return;
      }
      if (err.status === 404) {
        this.errorMessage.set('Nội dung không tồn tại hoặc đã bị xóa trước đó (404).');
        return;
      }
      this.errorMessage.set(body?.message ?? 'Lỗi máy chủ khi thực hiện thao tác (#52/#53).');
      return;
    }
    this.errorMessage.set('Lỗi kết nối khi gọi API #52/#53.');
  }
}
