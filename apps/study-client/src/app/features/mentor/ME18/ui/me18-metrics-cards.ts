import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { DatePipe } from '@angular/common';
import { MentorCourseActivityAnalyticsDto } from '../models/me18-analytics.models';

@Component({
  selector: 'app-me18-metrics-cards',
  imports: [DatePipe],
  templateUrl: './me18-metrics-cards.html',
  styleUrl: './me18-metrics-cards.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me18MetricsCardsComponent {
  readonly analytics = input<MentorCourseActivityAnalyticsDto | null>(null);
}
