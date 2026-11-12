import { Component, EventEmitter, Input, Output } from '@angular/core';

import {
  type ThreadActionStatus,
  canResolveSupportStatus,
} from '../models/me12-thread.models';

@Component({
  selector: 'study-me12-composer-resolve',
  styleUrl: './me12-composer-resolve.css',
  templateUrl: './me12-composer-resolve.html',
})
export class Me12ComposerResolve {
  @Input() requestStatus = 'OPEN';
  @Input() replyDraft = '';
  @Input() replyStatus: ThreadActionStatus = 'idle';
  @Input() replyMessage = '';

  @Input() confirmResolvedChecked = false;
  @Input() resolveStatus: ThreadActionStatus = 'idle';
  @Input() resolveMessage = '';

  @Output() readonly replyDraftChange = new EventEmitter<string>();
  @Output() readonly submitReply = new EventEmitter<void>();
  @Output() readonly confirmResolveChange = new EventEmitter<boolean>();
  @Output() readonly submitResolve = new EventEmitter<void>();

  get canResolve(): boolean {
    return canResolveSupportStatus(this.requestStatus);
  }

  onTextareaInput(event: Event): void {
    const val = (event.target as HTMLTextAreaElement | null)?.value ?? '';
    this.replyDraftChange.emit(val);
  }

  onConfirmToggle(event: Event): void {
    const checked = (event.target as HTMLInputElement | null)?.checked ?? false;
    this.confirmResolveChange.emit(checked);
  }
}
