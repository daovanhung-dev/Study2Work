import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type MutationStatus } from '../models/me10-grading.models';

@Component({
  selector: 'study-me10-evaluation-panel',
  styleUrl: './me10-evaluation-panel.css',
  templateUrl: './me10-evaluation-panel.html',
})
export class Me10EvaluationPanel {
  @Input() scoreDraft = '';
  @Input() feedbackDraft = '';
  @Input() gradeStatus: MutationStatus = 'idle';
  @Input() feedbackStatus: MutationStatus = 'idle';
  @Input() gradeMessage = '';
  @Input() feedbackMessage = '';

  @Output() readonly scoreInputChange = new EventEmitter<string>();
  @Output() readonly feedbackInputChange = new EventEmitter<string>();
  @Output() readonly submitGrade = new EventEmitter<void>();
  @Output() readonly submitFeedback = new EventEmitter<void>();

  onScoreInput(event: Event): void {
    const val = (event.target as HTMLInputElement | null)?.value ?? '';
    this.scoreInputChange.emit(val);
  }

  onFeedbackInput(event: Event): void {
    const val = (event.target as HTMLTextAreaElement | null)?.value ?? '';
    this.feedbackInputChange.emit(val);
  }
}
