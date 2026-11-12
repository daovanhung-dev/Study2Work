export interface Me10UploadAssetDto {
  readonly id: number;
  readonly name: string;
  readonly url: string;
  readonly content_type: string;
  readonly size_bytes: number;
  readonly status: string;
}

export interface SubmissionDetailDto {
  readonly id: number;
  readonly assignment_id: number;
  readonly user_id: number;
  readonly content?: string | null;
  readonly files: readonly Me10UploadAssetDto[];
  readonly status: string;
  readonly submitted_at: string;
  readonly score?: string | null;
  readonly feedback?: string | null;
}

/**
 * API #56 — POST /api/v1/mentor/submissions/{submission_id}/grade
 * Pydantic model GradeSubmissionRequest(extra="forbid"):
 * - score: Int32 (strict int)
 * - rubric_items: str (strict str, nhận nhưng chưa persist trong DB)
 */
export interface GradeSubmissionRequestDto {
  readonly score: number;
  readonly rubric_items: string;
}

/**
 * API #57 — POST /api/v1/mentor/submissions/{submission_id}/feedback
 * Pydantic model FeedbackSubmissionRequest(extra="forbid"):
 * - feedback_text: str (strict str)
 * - attachments: str (strict str, nhận nhưng chưa persist trong DB)
 */
export interface FeedbackSubmissionRequestDto {
  readonly feedback_text: string;
  readonly attachments: string;
}

export type MutationStatus = 'idle' | 'dirty' | 'saving' | 'saved' | 'error';

const MAX_INT64 = 9223372036854775807n;
const MIN_INT32 = -2147483648;
const MAX_INT32 = 2147483647;

export function parseSubmissionIdParam(raw: string | null | undefined): number | null {
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

export function parseStrictInt32Score(raw: string): number | null {
  const trimmed = raw.trim();
  if (!/^-?\d+$/.test(trimmed)) {
    return null;
  }
  const num = Number(trimmed);
  if (!Number.isSafeInteger(num) || num < MIN_INT32 || num > MAX_INT32) {
    return null;
  }
  return num;
}

export function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) {
    return '0 B';
  }
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  const kb = bytes / 1024;
  if (kb < 1024) {
    return `${kb.toFixed(1)} KB`;
  }
  return `${(kb / 1024).toFixed(2)} MB`;
}
