import { Component, EventEmitter, Input, Output } from '@angular/core';

import type { Me08ActionIntent, Me08TargetInspectionVm } from '../models/me08-actions.models';

@Component({
  selector: 'study-me08-action-cards',
  styleUrl: './me08-action-cards.css',
  templateUrl: './me08-action-cards.html',
})
export class Me08ActionCards {
  @Input() inspection: Me08TargetInspectionVm | null = null;
  @Input() activeIntent: Me08ActionIntent = 'publish';
  @Input() processing = false;

  @Output() readonly confirmPublish = new EventEmitter<void>();
  @Output() readonly confirmUnpublish = new EventEmitter<void>();
  @Output() readonly confirmDelete = new EventEmitter<void>();
}
