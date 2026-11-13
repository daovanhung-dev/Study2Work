import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';
import { StudentSummaryDto } from '../models/me13-recipients.models';

@Component({
  selector: 'app-me13-student-roster',
  imports: [],
  templateUrl: './me13-student-roster.html',
  styleUrl: './me13-student-roster.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me13StudentRosterComponent {
  readonly students = input.required<StudentSummaryDto[]>();
  readonly selectedIds = input.required<ReadonlySet<number>>();

  readonly toggleStudent = output<number>();
  readonly selectAllVisible = output<void>();
  readonly clearSelection = output<void>();

  readonly allVisibleSelected = computed(() => {
    const list = this.students();
    const set = this.selectedIds();
    return list.length > 0 && list.every((s) => set.has(s.id));
  });

  isSelected(studentId: number): boolean {
    return this.selectedIds().has(studentId);
  }

  getInitials(fullName: string): string {
    const parts = fullName.trim().split(/\s+/);
    const last = parts[parts.length - 1] ?? 'H';
    return (last[0] ?? 'H').toUpperCase();
  }
}
