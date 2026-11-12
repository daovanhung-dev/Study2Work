export type Me07EditorMode = 'create' | 'edit';

/** Khớp ContentResponse dùng chung của API #49, #50, #51 */
export interface Me07ContentNodeDto {
  id: number;
  course_id: number;
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
  status: string;
  parent_id?: number | null;
  order: number;
}

/** Khớp CreateContentRequest trong apps/study-server/app/modules/mentor/api_50_mentor_content_create/models.py */
export interface CreateContentRequestDto {
  course_id: number;
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
}

/** Khớp UpdateContentRequest trong apps/study-server/app/modules/mentor/api_51_mentor_content_update/models.py */
export interface UpdateContentRequestDto {
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
}

export interface Me07EditorDraftVm {
  title: string;
  contentType: string;
  summaryText: string;
  bodyText: string;
}

export const SUPPORTED_CONTENT_TYPES = [
  { value: 'SECTION', label: 'SECTION — Chương / học phần' },
  { value: 'LESSON', label: 'LESSON — Bài học lý thuyết' },
  { value: 'VIDEO', label: 'VIDEO — Bài giảng video' },
  { value: 'DOCUMENT', label: 'DOCUMENT — Tài liệu đọc' },
  { value: 'ASSIGNMENT', label: 'ASSIGNMENT — Bài tập thực hành / Lab' },
  { value: 'QUIZ', label: 'QUIZ — Bài kiểm tra trắc nghiệm' },
] as const;

const SIGNED_INT64_PATTERN = /^[+-]?\d+$/;
const INT64_MIN = BigInt('-9223372036854775808');
const INT64_MAX = BigInt('9223372036854775807');

export function parseMe07Int64Param(raw: string | null | undefined): number | null {
  if (!raw || raw.length > 20 || !SIGNED_INT64_PATTERN.test(raw)) {
    return null;
  }
  try {
    const big = BigInt(raw);
    if (big < INT64_MIN || big > INT64_MAX) {
      return null;
    }
    const num = Number(big);
    return Number.isSafeInteger(num) ? num : null;
  } catch {
    return null;
  }
}

export function extractDraftFromNode(node: Me07ContentNodeDto): Me07EditorDraftVm {
  const rawSummary = node.payload['summary'];
  const rawBody = node.payload['body'];
  return {
    title: node.title,
    contentType: node.content_type || 'LESSON',
    summaryText: typeof rawSummary === 'string' ? rawSummary : '',
    bodyText:
      typeof rawBody === 'string'
        ? rawBody
        : Object.keys(node.payload).length > 0
          ? JSON.stringify(node.payload)
          : '',
  };
}

export function buildPayloadFromDraft(
  draft: Me07EditorDraftVm,
  existingPayload: Record<string, unknown> = {},
): Record<string, unknown> {
  const next: Record<string, unknown> = { ...existingPayload };
  const trimmedSummary = draft.summaryText.trim();
  const trimmedBody = draft.bodyText.trim();

  if (trimmedSummary.length > 0) {
    next['summary'] = trimmedSummary;
  } else {
    delete next['summary'];
  }

  if (trimmedBody.length > 0) {
    next['body'] = trimmedBody;
  } else {
    delete next['body'];
  }

  return next;
}

export function isDraftDirty(initial: Me07EditorDraftVm, current: Me07EditorDraftVm): boolean {
  return (
    initial.title !== current.title ||
    initial.contentType !== current.contentType ||
    initial.summaryText !== current.summaryText ||
    initial.bodyText !== current.bodyText
  );
}
