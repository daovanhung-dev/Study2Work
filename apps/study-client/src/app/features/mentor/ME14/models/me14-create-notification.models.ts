export type NotificationChannelType = 'PUSH' | 'EMAIL';

export interface CourseContentSummaryDto {
  readonly id: number;
  readonly course_id: number;
  readonly title: string;
  readonly content_type: string;
  readonly order: number;
}

export interface CreateNotificationRequestDto {
  readonly recipients: string;
  readonly title: string;
  readonly content: number;
  readonly channels: string;
}

export interface OperationResponseDto {
  readonly operation_id: string;
  readonly status: string;
}

export interface CreateNotificationResultDto {
  readonly operation: OperationResponseDto;
  readonly notificationIds: number[];
}

export interface RecipientPreviewVm {
  readonly id: number;
  readonly full_name?: string;
}

export function parsePositiveInt(raw: string | number | null | undefined): number | null {
  if (raw === null || raw === undefined) {
    return null;
  }
  const str = String(raw).trim();
  if (!/^[1-9]\d*$/.test(str)) {
    return null;
  }
  const num = Number(str);
  return Number.isSafeInteger(num) && num > 0 ? num : null;
}

export function parseRecipientsCsvStrict(raw: string | null | undefined): {
  readonly validIds: number[];
  readonly invalidTokens: string[];
} {
  if (!raw || !raw.trim()) {
    return { validIds: [], invalidTokens: [] };
  }
  const validSet = new Set<number>();
  const invalidTokens: string[] = [];

  for (const token of raw.split(',')) {
    const trimmed = token.trim();
    if (!trimmed) {
      continue;
    }
    const parsed = parsePositiveInt(trimmed);
    if (parsed) {
      validSet.add(parsed);
    } else {
      invalidTokens.push(trimmed);
    }
  }

  return {
    validIds: Array.from(validSet),
    invalidTokens,
  };
}
