export interface MentorCourseItemDto {
  readonly id: number;
  readonly title: string;
  readonly category: string;
  readonly price: number;
  readonly status: string;
  readonly created_at: string;
}

export interface StudentSummaryDto {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export function parsePositiveInt(raw: string | null | undefined): number | null {
  if (!raw) {
    return null;
  }
  const trimmed = raw.trim();
  if (!/^[1-9]\d*$/.test(trimmed)) {
    return null;
  }
  const num = Number(trimmed);
  return Number.isSafeInteger(num) && num > 0 ? num : null;
}

export function parseRecipientsCsv(raw: string | null | undefined): number[] {
  if (!raw) {
    return [];
  }
  const seen = new Set<number>();
  for (const part of raw.split(',')) {
    const id = parsePositiveInt(part);
    if (id) {
      seen.add(id);
    }
  }
  return Array.from(seen);
}
