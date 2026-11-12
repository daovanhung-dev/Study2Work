export interface Me16StudentSummaryDto {
  readonly id: number;
  readonly full_name: string;
  readonly avatar_url?: string | null;
}

export interface MentorStudentProgressDto {
  readonly student: Me16StudentSummaryDto;
  readonly completed_lessons: number;
  readonly total_lessons: number;
  readonly progress_percent: number;
}

export interface Me16ProgressPaginationDto {
  readonly page: number;
  readonly size: number;
  readonly total: number;
  readonly total_pages: number;
}

export interface MentorStudentProgressPageDto {
  readonly items: readonly MentorStudentProgressDto[];
  readonly pagination: Me16ProgressPaginationDto;
}

export interface Me16RosterKpiVm {
  readonly totalStudents: number;
  readonly completedAllCount: number;
  readonly inProgressCount: number;
  readonly notStartedCount: number;
  readonly averagePercent: number;
}

const MAX_INT64 = 9223372036854775807n;

export function parseCourseIdParam(raw: string | null | undefined): number | null {
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

export function computeRosterKpi(
  items: readonly MentorStudentProgressDto[],
): Me16RosterKpiVm {
  if (items.length === 0) {
    return {
      totalStudents: 0,
      completedAllCount: 0,
      inProgressCount: 0,
      notStartedCount: 0,
      averagePercent: 0,
    };
  }

  let completedAllCount = 0;
  let inProgressCount = 0;
  let notStartedCount = 0;
  let sumPercent = 0;

  for (const row of items) {
    sumPercent += row.progress_percent;
    if (row.progress_percent >= 100) {
      completedAllCount += 1;
    } else if (row.progress_percent > 0 || row.completed_lessons > 0) {
      inProgressCount += 1;
    } else {
      notStartedCount += 1;
    }
  }

  return {
    totalStudents: items.length,
    completedAllCount,
    inProgressCount,
    notStartedCount,
    averagePercent: Math.round(sumPercent / items.length),
  };
}
