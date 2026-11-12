import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  type ContentNodeDto,
  type ContentTreeItemVm,
  formatStatusLabel,
} from '../models/me06-content.models';

export interface Me06NodeActionEvent {
  node: ContentNodeDto;
  action: 'edit' | 'publish' | 'unpublish' | 'delete' | 'quick-dialog';
}

@Component({
  selector: 'study-me06-tree-list',
  styleUrl: './me06-tree-list.css',
  templateUrl: './me06-tree-list.html',
})
export class Me06TreeList {
  @Input({ required: true }) items: readonly ContentTreeItemVm[] = [];
  @Input() collapsedIds: ReadonlySet<number> = new Set<number>();

  @Output() readonly toggleCollapse = new EventEmitter<number>();
  @Output() readonly nodeAction = new EventEmitter<Me06NodeActionEvent>();

  statusLabel(status: string): string {
    return formatStatusLabel(status);
  }

  isPublished(status: string): boolean {
    return status === 'PUBLISHED';
  }

  isCollapsed(id: number): boolean {
    return this.collapsedIds.has(id);
  }

  onToggle(id: number): void {
    this.toggleCollapse.emit(id);
  }

  onAction(node: ContentNodeDto, action: Me06NodeActionEvent['action']): void {
    this.nodeAction.emit({ node, action });
  }
}
