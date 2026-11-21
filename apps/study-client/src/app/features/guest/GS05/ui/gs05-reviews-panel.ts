import { Component, EventEmitter, Input, Output } from '@angular/core';

import type { GS05ReviewsState } from '../models/gs05-reviews.models';

@Component({
  selector: 'study-gs05-reviews-panel',
  styleUrl: './gs05-reviews-panel.css',
  templateUrl: './gs05-reviews-panel.html',
})
export class GS05ReviewsPanel {
  @Input({ required: true }) state!: GS05ReviewsState;
  @Output() readonly pageChange = new EventEmitter<number>();
  @Output() readonly retry = new EventEmitter<void>();
  @Output() readonly loadFirstPage = new EventEmitter<void>();
}
