import { Component, EventEmitter, Input, Output, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { StudyIcon } from './study-icon';
import type { AdminScreenDefinition, AdminScreenViewState } from './admin-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-admin-screen-surface',
  templateUrl: './admin-screen-surface.html',
})
export class AdminScreenSurface {
  @Input({ required: true }) definition!: AdminScreenDefinition;
  @Input() viewState: AdminScreenViewState | null = null;
  @Output() readonly filterChange = new EventEmitter<Readonly<Record<string, string>>>();
  @Output() readonly pageChange = new EventEmitter<number>();

  private readonly route = inject(ActivatedRoute);
  filterValues: Record<string, string> = {};
  readonly draftTitle = signal('');
  readonly draftContent = signal('');

  setDraftTitle(value: string): void {
    this.draftTitle.set(value);
  }

  setDraftContent(value: string): void {
    this.draftContent.set(value);
  }

  get referenceId(): string | null {
    const params = this.route.snapshot.paramMap;

    return params.get('userId')
      ?? params.get('courseId')
      ?? params.get('contentId')
      ?? params.get('lessonId')
      ?? params.get('quizId')
      ?? params.get('notificationId')
      ?? params.get('discussionId');
  }

  get connectionTitle(): string {
    if (this.viewState?.status === 'loading') {
      return 'Đang tải dữ liệu';
    }
    if (this.viewState?.status === 'error') {
      return 'Không thể tải dữ liệu';
    }
    if (this.viewState?.status === 'loaded') {
      return 'Dữ liệu đã tải từ Study Server';
    }
    switch (this.definition.sourceState) {
      case 'session-unavailable':
        return 'Chưa có dữ liệu được tải';
      case 'contract-blocked':
        return 'Chức năng đang chờ xác nhận hợp đồng';
      case 'api-absent':
        return 'Nguồn dữ liệu chưa được triển khai';
      case 'data-backed':
        return 'Chưa có dữ liệu được tải';
    }
  }

  get connectionMessage(): string {
    if (this.viewState?.status === 'loading') {
      return 'Đang gửi yêu cầu tới API đã xác minh.';
    }
    if (this.viewState?.status === 'error') {
      return this.viewState.message ?? 'Yêu cầu chưa hoàn tất.';
    }
    if (this.viewState?.status === 'loaded') {
      return this.definition.sourceNote;
    }
    return this.definition.sourceNote;
  }

  get unavailableText(): string {
    if (this.viewState?.status === 'loading') {
      return 'Đang tải dữ liệu';
    }
    if (this.viewState?.status === 'error') {
      return this.viewState.message ?? 'Không thể tải dữ liệu';
    }
    if (this.viewState?.status === 'loaded') {
      return 'API hiện tại không cung cấp dữ liệu này';
    }
    return this.definition.sourceState === 'api-absent'
      ? 'Chưa có nguồn dữ liệu'
      : 'Chưa thể tải dữ liệu';
  }

  setFilter(key: string, value: string): void {
    this.filterValues = { ...this.filterValues, [key]: value };
  }

  applyFilters(event: Event): void {
    event.preventDefault();
    this.filterChange.emit({ ...this.filterValues });
  }

  clearFilters(): void {
    this.filterValues = {};
    this.filterChange.emit({});
  }

  fieldValue(label: string): string {
    return this.viewState?.fields?.find((field) => field.label === label)?.value ?? '';
  }

  resolveRoute(route: string): string {
    return route.replace(/:([A-Za-z][A-Za-z0-9]*)/g, (_placeholder, key: string) =>
      encodeURIComponent(this.route.snapshot.paramMap.get(key) ?? ''),
    );
  }
}

