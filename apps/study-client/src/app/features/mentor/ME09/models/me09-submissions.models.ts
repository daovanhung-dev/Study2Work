export interface MentorCourseOptionDto {
  readonly id: number;
  readonly title: string;
  readonly status: string;
}

export interface MentorCoursePageDto {
  readonly items: readonly MentorCourseOptionDto[];
  readonly pagination: {
    readonly page: number;
    readonly size: number;
    readonly total: number;
    readonly total_pages: number;
  };
}

export interface SubmissionUploadAssetDto {
  readonly id: number;
  readonly name: string;
  readonly url: string;
  readonly content_type: string;
  readonly size_bytes: number;
  readonly status: string;
}

export interface SubmissionItemDto {
  readonly id: number;
  readonly assignment_id: number;
  readonly user_id: number;
  readonly content?: string | null;
  readonly files: readonly SubmissionUploadAssetDto[];
  readonly status: string;
  readonly submitted_at: string;
  readonly score?: string | null;
  readonly feedback?: string | null;
}

export interface SubmissionPaginationDto {
  readonly page: number;
  readonly size: number;
  readonly total: number;
  readonly total_pages: number;
}

export interface SubmissionPageDto {
  readonly items: readonly SubmissionItemDto[];
  readonly pagination: SubmissionPaginationDto;
}

export interface Me09QueryParams {
  readonly course_id?: number | null;
  readonly status?: string | null;
  readonly page?: number;
}

const MAX_INT64 = 9223372036854775807n;
const MAX_INT32 = 2147483647;

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

export function parsePositiveInt32(raw: string | null | undefined, fallback = 1): number {
  if (!raw) {
    return fallback;
  }
  const trimmed = raw.trim();
  if (!/^[1-9]\d*$/.test(trimmed)) {
    return fallback;
  }
  const num = Number(trimmed);
  if (!Number.isSafeInteger(num) || num < 1 || num > MAX_INT32) {
    return fallback;
  }
  return num;
}

export function formatSubmissionStatus(status: string): string {
  switch (status.toUpperCase()) {
    case 'SUBMITTED':
      return 'Chờ chấm điểm (SUBMITTED)';
    case 'GRADED':
      return 'Đã chấm điểm (GRADED)';
    case 'PENDING':
      return 'Đang chờ (PENDING)';
    default:
      return status;
  }
}
