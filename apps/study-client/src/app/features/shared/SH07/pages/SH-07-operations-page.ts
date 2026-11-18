import { HttpErrorResponse } from '@angular/common/http';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { SystemOperationsService } from '../data-access/SH-07-operations.service';
import type { SystemOperationsState } from '../models/SH-07-operations.models';
import { SystemOperationsView } from '../ui/SH-07-operations-view';

const UUID = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

@Component({
  selector: 'study-system-operations-page',
  imports: [SystemOperationsView],
  templateUrl: './SH-07-operations-page.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SystemOperationsPage implements OnInit {
  private readonly source = inject(SystemOperationsService);
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private operationId: string | null = null;

  readonly state = signal<SystemOperationsState>({
    kind: 'missing-context',
    title: 'Thiếu thông tin trên đường dẫn',
    message: 'Vui lòng mở lại màn hình từ chức năng trước đó.',
    referenceId: null,
  });

  ngOnInit(): void {
    this.route.paramMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      this.operationId = params.get('operationId')?.trim() ?? null;
      this.load();
    });
  }

  load(): void {
    const id = this.operationId;
    if (!id) {
      this.state.set({ kind: 'missing-context', title: 'Thiếu mã tác vụ', message: 'Vui lòng mở lại màn hình từ chức năng trước đó.', referenceId: null });
      return;
    }
    if (!UUID.test(id)) {
      this.state.set({ kind: 'not-found', title: 'Không tìm thấy tác vụ', message: 'Mã tác vụ trên đường dẫn không hợp lệ.', referenceId: id.slice(0, 128) });
      return;
    }
    this.state.set({ kind: 'loading', title: 'Đang tải tác vụ', message: 'Đang xác minh trạng thái và quyền truy cập với máy chủ.', referenceId: id });
    this.source.getOperation(id).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (operation) => this.state.set({
        kind: 'ready', title: 'Trạng thái tác vụ', message: 'Trạng thái được xác nhận từ API #18.',
        referenceId: id, operation,
      }),
      error: (error: unknown) => {
        const http = error instanceof HttpErrorResponse ? error : null;
        const body = http?.error && typeof http.error === 'object' ? http.error as Record<string, unknown> : {};
        const trace = body['traceId'] ?? http?.headers.get('X-Trace-Id');
        const kind = http?.status === 404 ? 'not-found' : http?.status === 401 || http?.status === 403 ? 'unavailable' : 'error';
        this.state.set({
          kind,
          title: kind === 'not-found' ? 'Không tìm thấy tác vụ' : kind === 'unavailable' ? 'Không thể truy cập tác vụ' : 'Không tải được tác vụ',
          message: kind === 'not-found' ? 'Tác vụ không tồn tại hoặc không thuộc phạm vi được phép xem.' : kind === 'unavailable' ? 'Vui lòng kiểm tra phiên đăng nhập và quyền truy cập.' : 'Máy chủ chưa thể cung cấp trạng thái. Vui lòng thử lại.',
          referenceId: id,
          traceId: typeof trace === 'string' ? trace : null,
        });
      },
    });
  }
}
