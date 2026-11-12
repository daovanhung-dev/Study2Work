import { Component, EventEmitter, Input, Output } from '@angular/core';

import { type MentorStudentProgressDto } from '../models/me16-progress.models';

@Component({
  selector: 'study-me16-roster-table',
  styleUrl: './me16-roster-table.css',
  templateUrl: './me16-roster-table.html',
})
export class Me16RosterTable {
  @Input() items: readonly MentorStudentProgressDto[] = [];

  @Output() readonly openStudentProgress = new EventEmitter<number>();
}
