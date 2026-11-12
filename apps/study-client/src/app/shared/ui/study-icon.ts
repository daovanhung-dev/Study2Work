import { Component, Input } from '@angular/core';

export type StudyIconName =
  | 'activity'
  | 'arrow'
  | 'bell'
  | 'book'
  | 'brand'
  | 'calendar'
  | 'chart'
  | 'checklist'
  | 'chevron'
  | 'dashboard'
  | 'database'
  | 'file'
  | 'filter'
  | 'info'
  | 'layers'
  | 'lock'
  | 'person'
  | 'refresh'
  | 'search'
  | 'server'
  | 'shield'
  | 'users';

@Component({
  selector: 'study-icon',
  styleUrl: './study-icon.css',
  templateUrl: './study-icon.html',
})
export class StudyIcon {
  @Input({ required: true }) name!: StudyIconName;
}
