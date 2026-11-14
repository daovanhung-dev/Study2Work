import type { StudentOverviewState } from '../models/ST-01-overview.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-overview-view',
  imports: [CommonModule],
  templateUrl: './ST-01-overview-view.html',
  styleUrl: './ST-01-overview-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentOverviewView {
  @Input({ required: true }) state!: StudentOverviewState;
}
