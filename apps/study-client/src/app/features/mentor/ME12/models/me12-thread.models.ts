export interface Me12UserSummaryDto {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export interface Me12UploadAssetDto {
  readonly id: number;
  readonly name: string;
  readonly url: string;
  readonly content_type: string;
  readonly size_bytes: number;
  readonly status: string;
}

export interface Me12SupportMessageDto {
  readonly id: number;
  readonly author: Me12UserSummaryDto;
  readonly content: string;
  readonly attachments: readonly Me12UploadAssetDto[];
  readonly created_at: string;
}

export interface SupportRequestDetailDto {
  readonly id: number;
  readonly course_id: number;
  readonly student: Me12UserSummaryDto;
  readonly status: string;
  readonly messages: readonly Me12SupportMessageDto[];
  readonly created_at: string;
  readonly resolved_at?: string | null;
}

/**
 * API #60 — POST /api/v1/mentor/support/{request_id}/reply
 * ReplyToMentorSupportRequest(extra="forbid"):
 * - message: str (strict=True, không chấp nhận chuỗi rỗng/chỉ khoảng trắng)
 * - attachment_refs: str (strict=True, chuỗi JSON mảng ID int64 duy nhất, mặc định "[]")
 */
export interface ReplySupportRequestDto {
  readonly message: string;
  readonly attachment_refs: string;
}

export type ThreadActionStatus = 'idle' | 'saving' | 'saved' | 'error';

const MAX_INT64 = 9223372036854775807n;
const RESOLVABLE_STATUSES = new Set(['OPEN', 'IN_PROGRESS', 'WAITING_LEARNER', 'RESOLVED']);

export function parseSupportRequestId(raw: string | null | undefined): number | null {
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

export function canResolveSupportStatus(status: string | undefined | null): boolean {
  if (!status) {
    return false;
  }
  return RESOLVABLE_STATUSES.has(status.toUpperCase());
}
