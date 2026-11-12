import { Component, Input } from '@angular/core';

import type { Me07ContentNodeDto, Me07EditorMode } from '../models/me07-editor.models';

@Component({
  selector: 'study-me07-guidelines-aside',
  styleUrl: './me07-guidelines-aside.css',
  templateUrl: './me07-guidelines-aside.html',
})
export class Me07GuidelinesAside {
  @Input() mode: Me07EditorMode = 'create';
  @Input() currentNode: Me07ContentNodeDto | null = null;
  @Input() isDirty = false;
}
