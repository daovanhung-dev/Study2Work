import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type SupportRequestItemDto } from '../models/me11-support.models';

@Component({
  selector: 'study-me11-request-list',
  styleUrl: './me11-request-list.css',
  templateUrl: './me11-request-list.html',
})
export class Me11RequestList {
  @Input() items: readonly SupportRequestItemDto[] = [];

  @Output() readonly selectRequest = new EventEmitter<number>();

  latestPreview(item: SupportRequestItemDto): string {
    if (item.messages.length === 0) {
      return 'Chưa có tin nhắn trong luồng trao đổi.';
    }
    const last = item.messages[item.messages.length - 1];
    return `${last.author.full_name}: ${last.content}`;
  }

  isResolved(status: string): boolean {
    return status.toUpperCase() === 'RESOLVED';
  }
}
