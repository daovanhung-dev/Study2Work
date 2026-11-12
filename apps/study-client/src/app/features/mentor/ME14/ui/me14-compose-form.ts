import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  CourseContentSummaryDto,
  NotificationChannelType,
} from '../models/me14-create-notification.models';

@Component({
  selector: 'app-me14-compose-form',
  imports: [FormsModule],
  templateUrl: './me14-compose-form.html',
  styleUrl: './me14-compose-form.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me14ComposeFormComponent {
  readonly title = input.required<string>();
  readonly contentIdInput = input.required<string>();
  readonly selectedChannels = input.required<ReadonlySet<NotificationChannelType>>();
  readonly contents = input.required<CourseContentSummaryDto[]>();
  readonly loadingContents = input.required<boolean>();
  readonly submitting = input.required<boolean>();
  readonly canSubmit = input.required<boolean>();

  readonly titleChange = output<string>();
  readonly contentIdChange = output<string>();
  readonly toggleChannel = output<NotificationChannelType>();
  readonly submitNotification = output<void>();

  hasChannel(ch: NotificationChannelType): boolean {
    return this.selectedChannels().has(ch);
  }

  onContentIdChange(raw: string | number | null | undefined): void {
    this.contentIdChange.emit(raw === null || raw === undefined ? '' : String(raw));
  }
}
