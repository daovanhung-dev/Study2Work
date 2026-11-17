import type { StudentEnrollResultState } from '../models/ST-07-enroll-result.models';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'study-student-enroll-result-view',
  imports: [CommonModule],
  templateUrl: './ST-07-enroll-result-view.html',
  styleUrl: './ST-07-enroll-result-view.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentEnrollResultView {
  @Input({ required: true }) state!: StudentEnrollResultState;
}
