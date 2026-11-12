export interface Me11CourseOptionDto {
  readonly id: number;
  readonly title: string;
  readonly status: string;
}

export interface Me11CoursePageDto {
  readonly items: readonly Me11CourseOptionDto[];
  readonly pagination: {
    readonly page: number;
    readonly size: number;
    readonly total: number;
    readonly total_pages: number;
  };
}

export interface SupportUserSummaryDto {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export interface SupportUploadAssetDto {
  readonly id: number;
  readonly name: string;
  readonly url: string;
  readonly content_type: string;
  readonly size_bytes: number;
  readonly status: string;
}

export interface SupportMessageDto {
  readonly id: number;
  readonly author: SupportUserSummaryDto;
  readonly content: string;
  readonly attachments: readonly SupportUploadAssetDto[];
  readonly created_at: string;
}

export interface SupportRequestItemDto {
  readonly id: number;
  readonly course_id: number;
  readonly student: SupportUserSummaryDto;
  readonly status: string;
  readonly messages: readonly SupportMessageDto[];
  readonly created_at: string;
  readonly resolved_at?: string | null;
}

export interface Me11QueryParams {
  readonly course_id?: number | null;
  readonly status?: string | null;
}

export interface SupportStatusCountsVm {
  readonly total: number;
  readonly openCount: number;
  readonly resolvedCount: number;
}

const MAX_INT64 = 9223372036854775807n;

export function parsePositiveInt64(raw: string | null | undefined): number | null {
  if (!raw) {
    return null;
  }
  const trimmed = raw.trim();
  if (!/^[1-9]\d*$/.test(trimmed)) {
    return null;
  }
  try {
    const big = BigInt(trimmed);
    if (big < 1n || big > MAX_INT64) {
      return null;
    }
    return Number(big);
  } catch {
    return null;
  }
}

export function computeSupportCounts(
  items: readonly SupportRequestItemDto[],
): SupportStatusCountsVm {
  let openCount = 0;
  let resolvedCount = 0;
  for (const item of items) {
    const upper = item.status.toUpperCase();
    if (upper === 'RESOLVED') {
      resolvedCount += 1;
    } else if (upper === 'OPEN' || upper === 'IN_PROGRESS' || upper === 'WAITING_LEARNER') {
      openCount += 1;
    }
  }
  return {
    total: items.length,
    openCount,
    resolvedCount,
  };
}
