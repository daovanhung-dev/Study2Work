import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Me14CreateNotificationService } from '../data-access/me14-create-notification.service';
import {
  CourseContentSummaryDto,
  NotificationChannelType,
  parsePositiveInt,
  parseRecipientsCsvStrict,
  RecipientPreviewVm,
} from '../models/me14-create-notification.models';
import { Me14ComposeFormComponent } from '../ui/me14-compose-form';
import { Me14RecipientsSummaryComponent } from '../ui/me14-recipients-summary';

@Component({
  selector: 'app-me14-page',
  imports: [Me14RecipientsSummaryComponent, Me14ComposeFormComponent],
  templateUrl: './me14-page.html',
  styleUrl: './me14-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ME14Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly service = inject(Me14CreateNotificationService);

  readonly courseId = signal<number | null>(null);
  readonly recipientsCsv = signal<string>('');
  readonly knownRecipients = signal<RecipientPreviewVm[]>([]);
  readonly contents = signal<CourseContentSummaryDto[]>([]);
  readonly title = signal<string>('');
  readonly contentIdInput = signal<string>('');
  readonly selectedChannels = signal<Set<NotificationChannelType>>(
    new Set<NotificationChannelType>(['PUSH']),
  );

  readonly loadingContents = signal<boolean>(false);
  readonly submitting = signal<boolean>(false);
  readonly errorCode = signal<string | null>(null);
  readonly errorMessage = signal<string | null>(null);

  readonly parsedRecipients = computed(() => parseRecipientsCsvStrict(this.recipientsCsv()));
  readonly parsedContentId = computed(() => parsePositiveInt(this.contentIdInput()));

  readonly canSubmit = computed(() => {
    const rec = this.parsedRecipients();
    const trimmedTitle = this.title().trim();
    const contentId = this.parsedContentId();
    const channels = this.selectedChannels();
    return (
      rec.validIds.length > 0 &&
      rec.invalidTokens.length === 0 &&
      trimmedTitle.length > 0 &&
      trimmedTitle.length <= 200 &&
      contentId !== null &&
      channels.size > 0
    );
  });

  ngOnInit(): void {
    const qCourseId = parsePositiveInt(this.route.snapshot.queryParamMap.get('courseId'));
    const qRecipients = this.route.snapshot.queryParamMap.get('recipients') ?? '';
    if (qRecipients) {
      this.recipientsCsv.set(qRecipients);
    }

    const navState = history.state as
      | { courseId?: number; recipients?: RecipientPreviewVm[] }
      | undefined;
    if (Array.isArray(navState?.recipients)) {
      this.knownRecipients.set(navState.recipients);
      if (!qRecipients && navState.recipients.length > 0) {
        this.recipientsCsv.set(navState.recipients.map((r) => r.id).join(','));
      }
    }

    const resolvedCourseId = qCourseId ?? parsePositiveInt(navState?.courseId);
    if (resolvedCourseId) {
      this.courseId.set(resolvedCourseId);
      this.loadCourseContents(resolvedCourseId);
    }
  }

  loadCourseContents(courseId: number): void {
    this.loadingContents.set(true);
    this.service.getCourseContents(courseId).subscribe({
      next: (items) => {
        this.contents.set(items);
        this.loadingContents.set(false);
        if (!this.contentIdInput() && items[0]?.id) {
          this.contentIdInput.set(String(items[0].id));
        }
      },
      error: () => {
        this.loadingContents.set(false);
      },
    });
  }

  onToggleChannel(channel: NotificationChannelType): void {
    const next = new Set(this.selectedChannels());
    if (next.has(channel)) {
      next.delete(channel);
    } else {
      next.add(channel);
    }
    this.selectedChannels.set(next);
  }

  backToRecipients(): void {
    const validIds = this.parsedRecipients().validIds;
    void this.router.navigate(['/mentor/notifications/recipients'], {
      queryParams: {
        courseId: this.courseId() ?? undefined,
        recipients: validIds.length > 0 ? validIds.join(',') : undefined,
      },
    });
  }

  submitNotification(): void {
    if (!this.canSubmit() || this.submitting()) {
      return;
    }
    const recipients = this.parsedRecipients().validIds.join(',');
    const content = this.parsedContentId()!;
    const title = this.title().trim();
    const channels = Array.from(this.selectedChannels()).join(',');

    this.submitting.set(true);
    this.errorCode.set(null);
    this.errorMessage.set(null);

    this.service
      .createNotification({
        recipients,
        title,
        content,
        channels,
      })
      .subscribe({
        next: (result) => {
          this.submitting.set(false);
          const ids = result.notificationIds;
          void this.router.navigate(['/mentor/notifications/status'], {
            queryParams: {
              ids: ids.length > 0 ? ids.join(',') : undefined,
              op: result.operation.operation_id,
              courseId: this.courseId() ?? undefined,
            },
            state: {
              operation: result.operation,
              notificationIds: ids,
              courseId: this.courseId(),
              title,
            },
          });
        },
        error: (err: unknown) => {
          this.submitting.set(false);
          if (err instanceof HttpErrorResponse) {
            const apiCode =
              (err.error as { error?: { code?: string } } | null)?.error?.code ??
              `HTTP_${err.status}`;
            const apiMsg =
              (err.error as { error?: { message?: string } } | null)?.error?.message ?? err.message;
            this.errorCode.set(apiCode);
            this.errorMessage.set(apiMsg);
          } else {
            this.errorCode.set('UNKNOWN_ERROR');
            this.errorMessage.set('Không thể gửi thông báo.');
          }
        },
      });
  }
}
