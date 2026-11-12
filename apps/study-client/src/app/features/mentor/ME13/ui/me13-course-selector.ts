import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MentorCourseItemDto } from '../models/me13-recipients.models';

@Component({
  selector: 'app-me13-course-selector',
  imports: [FormsModule],
  templateUrl: './me13-course-selector.html',
  styleUrl: './me13-course-selector.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me13CourseSelectorComponent {
  readonly courses = input.required<MentorCourseItemDto[]>();
  readonly selectedCourseId = input.required<number | null>();
  readonly searchKeyword = input.required<string>();
  readonly loadingCourses = input.required<boolean>();

  readonly courseChange = output<number>();
  readonly searchChange = output<string>();

  onSelectCourse(rawValue: string): void {
    const parsed = Number(rawValue);
    if (Number.isSafeInteger(parsed) && parsed > 0) {
      this.courseChange.emit(parsed);
    }
  }
}
