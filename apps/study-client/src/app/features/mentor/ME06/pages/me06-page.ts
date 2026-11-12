import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Me06ContentService } from '../data-access/me06-content.service';
import {
  type ContentKpiSummaryVm,
  type ContentNodeDto,
  type ContentStatusFilter,
  type ContentTreeItemVm,
  buildContentTree,
  computeContentKpi,
  filterContentTree,
  parseSignedInt64Param,
} from '../models/me06-content.models';
import { Me06Header } from '../ui/me06-header';
import { Me06KpiStrip } from '../ui/me06-kpi-strip';
import { Me06TreeList, type Me06NodeActionEvent } from '../ui/me06-tree-list';

export type Me06ScreenState =
  | 'invalid-param'
  | 'loading'
  | 'empty'
  | 'ready'
  | 'unauthorized'
  | 'forbidden'
  | 'not-found'
  | 'error';

@Component({
  imports: [Me06Header, Me06KpiStrip, Me06TreeList],
  selector: 'study-me06-page',
  styleUrl: './me06-page.css',
  templateUrl: './me06-page.html',
})
export class ME06Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly contentService = inject(Me06ContentService);

  readonly courseId = signal<number | null>(null);
  readonly screenState = signal<Me06ScreenState>('loading');
  readonly errorMessage = signal<string>('');
  readonly traceId = signal<string>('');

  readonly rawNodes = signal<readonly ContentNodeDto[]>([]);
  readonly statusFilter = signal<ContentStatusFilter>('ALL');
  readonly searchKeyword = signal<string>('');
  readonly collapsedIds = signal<ReadonlySet<number>>(new Set<number>());

  readonly kpiSummary = computed<ContentKpiSummaryVm>(() => computeContentKpi(this.rawNodes()));
  readonly fullTree = computed<ContentTreeItemVm[]>(() => buildContentTree(this.rawNodes()));
  readonly visibleTree = computed<ContentTreeItemVm[]>(() =>
    filterContentTree(this.fullTree(), this.statusFilter(), this.searchKeyword()),
  );

  ngOnInit(): void {
    const rawCourseId = this.route.snapshot.paramMap.get('courseId');
    const parsedId = parseSignedInt64Param(rawCourseId);
    if (parsedId === null) {
      this.courseId.set(null);
      this.screenState.set('invalid-param');
      this.errorMessage.set('Mã khóa học trên đường dẫn không phải số nguyên int64 hợp lệ.');
      return;
    }

    this.courseId.set(parsedId);
    this.loadCourseTree(parsedId);
  }

  reloadTree(): void {
    const id = this.courseId();
    if (id !== null) {
      this.loadCourseTree(id);
    }
  }

  setStatusFilter(filter: ContentStatusFilter): void {
    this.statusFilter.set(filter);
  }

  onSearchInput(event: Event): void {
    const target = event.target as HTMLInputElement | null;
    this.searchKeyword.set(target?.value ?? '');
  }

  expandAll(): void {
    this.collapsedIds.set(new Set<number>());
  }

  collapseAll(): void {
    const ids = new Set<number>();
    for (const item of this.rawNodes()) {
      ids.add(item.id);
    }
    this.collapsedIds.set(ids);
  }

  onToggleNodeCollapse(nodeId: number): void {
    const next = new Set(this.collapsedIds());
    if (next.has(nodeId)) {
      next.delete(nodeId);
    } else {
      next.add(nodeId);
    }
    this.collapsedIds.set(next);
  }

  openCreateContent(): void {
    const id = this.courseId();
    if (id === null) {
      return;
    }
    void this.router.navigate(['/mentor/courses', id, 'content', 'new']);
  }

  onNodeAction(event: Me06NodeActionEvent): void {
    const id = this.courseId();
    if (id === null) {
      return;
    }

    if (event.action === 'edit') {
      void this.router.navigate(['/mentor/courses', id, 'content', event.node.id]);
      return;
    }

    const mode = event.action === 'quick-dialog' ? 'publish' : event.action;
    const dialogFlag = event.action === 'quick-dialog' ? '1' : undefined;

    void this.router.navigate(['/mentor/content', event.node.id, 'actions'], {
      queryParams: {
        courseId: id,
        action: mode,
        ...(dialogFlag ? { dialog: dialogFlag } : {}),
      },
    });
  }

  private loadCourseTree(courseId: number): void {
    this.screenState.set('loading');
    this.errorMessage.set('');
    this.traceId.set('');

    this.contentService.getCourseContents(courseId).subscribe({
      next: (envelope) => {
        const nodes = Array.isArray(envelope.data) ? envelope.data : [];
        this.rawNodes.set(nodes);
        this.traceId.set(envelope.traceId ?? '');
        this.screenState.set(nodes.length === 0 ? 'empty' : 'ready');
      },
      error: (err: unknown) => {
        this.rawNodes.set([]);
        if (err instanceof HttpErrorResponse) {
          const body = err.error as { message?: string; traceId?: string } | null;
          this.traceId.set(body?.traceId ?? '');
          if (err.status === 401) {
            this.screenState.set('unauthorized');
            this.errorMessage.set('Phiên đăng nhập giảng viên chưa xác thực hoặc đã hết hạn (401).');
            return;
          }
          if (err.status === 403) {
            this.screenState.set('forbidden');
            this.errorMessage.set('Bạn không có quyền truy cập cây nội dung của khóa học này (403).');
            return;
          }
          if (err.status === 404) {
            this.screenState.set('not-found');
            this.errorMessage.set('Không tìm thấy khóa học theo mã đã cung cấp (404).');
            return;
          }
          this.errorMessage.set(body?.message ?? 'Không thể tải cây nội dung khóa học.');
        } else {
          this.errorMessage.set('Lỗi kết nối tới máy chủ Study API.');
        }
        this.screenState.set('error');
      },
    });
  }
}
