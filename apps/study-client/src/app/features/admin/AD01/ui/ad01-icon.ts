import { Component, Input } from '@angular/core';

export type AD01IconName =
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
  | 'info'
  | 'layers'
  | 'lock'
  | 'person'
  | 'refresh'
  | 'server'
  | 'shield'
  | 'users';

@Component({
  selector: 'study-ad01-icon',
  styleUrl: './ad01-icon.css',
  templateUrl: './ad01-icon.html',
})
export class AD01Icon {
  @Input({ required: true }) name!: AD01IconName;
}
