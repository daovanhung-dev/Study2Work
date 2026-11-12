import { Component, EventEmitter, Input, Output } from '@angular/core';

import type { Me07EditorMode } from '../models/me07-editor.models';

@Component({
  selector: 'study-me07-header',
  styleUrl: './me07-header.css',
  templateUrl: './me07-header.html',
})
export class Me07Header {
  @Input() courseId: number | null = null;
  @Input() contentId: number | null = null;
  @Input() mode: Me07EditorMode = 'create';

  @Output() readonly backToTree = new EventEmitter<void>();
}
