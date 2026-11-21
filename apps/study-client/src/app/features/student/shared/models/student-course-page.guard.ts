import type { StudentCourseSummary, StudentPage } from './student-api.models';

const PAGE_SIZE = 20;

export function isStudentCoursePage(
  value: unknown,
  requestedPage: number,
  requiredEnrollmentStatus?: string,
): value is StudentPage<StudentCourseSummary> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }
  const pagination = value['pagination'];
  const total = pagination['total'];
  if (
    pagination['page'] !== requestedPage ||
    pagination['size'] !== PAGE_SIZE ||
    !isNonnegativeSafeInteger(total) ||
    pagination['total_pages'] !== Math.ceil(total / PAGE_SIZE) ||
    value['items'].length > PAGE_SIZE
  ) {
    return false;
  }

  let previousEnrolledAt = Number.POSITIVE_INFINITY;
  return value['items'].every((course: unknown) => {
    if (
      !isRecord(course) ||
      !isPositiveSafeInteger(course['course_id']) ||
      typeof course['name'] !== 'string' ||
      typeof course['enrollment_status'] !== 'string' ||
      (requiredEnrollmentStatus !== undefined &&
        course['enrollment_status'] !== requiredEnrollmentStatus) ||
      typeof course['enrolled_at'] !== 'string'
    ) {
      return false;
    }

    const enrolledAt = Date.parse(course['enrolled_at']);
    if (!Number.isFinite(enrolledAt) || enrolledAt > previousEnrolledAt) return false;
    previousEnrolledAt = enrolledAt;

    for (const field of ['description', 'thumbnail_url', 'course_status'] as const) {
      const fieldValue = course[field];
      if (fieldValue !== undefined && fieldValue !== null && typeof fieldValue !== 'string') {
        return false;
      }
    }
    return true;
  });
}

export function hasStudentCoursePageCountMismatch(
  page: StudentPage<StudentCourseSummary>,
): boolean {
  const { page: pageNumber, size, total } = page.pagination;
  const offset = (pageNumber - 1) * size;
  const expectedItems = Math.min(size, Math.max(total - offset, 0));
  return page.items.length !== expectedItems;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isPositiveSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
}
