import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecipientPreviewVm } from '../models/me14-create-notification.models';

@Component({
  selector: 'app-me14-recipients-summary',
  imports: [FormsModule],
  templateUrl: './me14-recipients-summary.html',
  styleUrl: './me14-recipients-summary.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Me14RecipientsSummaryComponent {
  readonly recipientsCsv = input.required<string>();
  readonly validIds = input.required<number[]>();
  readonly invalidTokens = input.required<string[]>();
  readonly knownRecipients = input.required<RecipientPreviewVm[]>();

  readonly recipientsCsvChange = output<string>();
  readonly backToSelect = output<void>();
}
