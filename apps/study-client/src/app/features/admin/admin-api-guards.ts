import type {
  AdminContent,
  AdminCourse,
  AdminLesson,
  AdminPage,
  AdminQuiz,
  AdminUserProfile,
} from './admin-api.models';

export function isAdminUserProfile(value: unknown): value is AdminUserProfile {
  if (!isRecord(value)) {
    return false;
  }

  // Keep int64 IDs as response data only; route navigation must use the raw route string.
  return Number.isInteger(value['id'])
    && typeof value['full_name'] === 'string'
    && typeof value['email'] === 'string'
    && typeof value['role'] === 'string'
    && typeof value['status'] === 'string'
    && (value['phone'] === null || typeof value['phone'] === 'string')
    && (value['avatar_url'] === null || typeof value['avatar_url'] === 'string')
    && typeof value['created_at'] === 'string'
    && typeof value['updated_at'] === 'string';
}

export function isAdminCourse(value: unknown): value is AdminCourse {
  if (!isRecord(value)) {
    return false;
  }

  const mentor = value['mentor'];
  if (!isRecord(mentor)) {
    return false;
  }

  return Number.isInteger(value['id'])
    && typeof value['title'] === 'string'
    && (value['description'] === null || typeof value['description'] === 'string')
    && (value['thumbnail_url'] === null || typeof value['thumbnail_url'] === 'string')
    && typeof value['price'] === 'string'
    && typeof value['status'] === 'string'
    && Number.isInteger(mentor['id'])
    && typeof mentor['full_name'] === 'string'
    && (mentor['avatar_url'] === undefined
      || mentor['avatar_url'] === null
      || typeof mentor['avatar_url'] === 'string');
}

export function isAdminUserPage(value: unknown, requestedPage: number): value is AdminPage<AdminUserProfile> {
  return isFixedAdminPage(value, requestedPage, isAdminUserProfile);
}

export function isAdminCoursePage(value: unknown, requestedPage: number): value is AdminPage<AdminCourse> {
  return isFixedAdminPage(value, requestedPage, isAdminCourse);
}

/** Validate #74's locally implemented singleton Page<Course> response. */
export function isAdminCourseDetailPage(
  value: unknown,
): value is AdminPage<AdminCourse> & { readonly items: readonly [AdminCourse] } {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  return items.length === 1
    && isAdminCourse(items[0])
    && pagination['page'] === 1
    && pagination['size'] === 1
    && pagination['total'] === 1
    && pagination['total_pages'] === 1;
}

export function isAdminContentPage(value: unknown, requestedPage: number): value is AdminPage<AdminContent> {
  return isFixedAdminPage(value, requestedPage, isAdminContent);
}

export function isAdminQuizPage(value: unknown, requestedPage: number): value is AdminPage<AdminQuiz> {
  return isFixedAdminPage(value, requestedPage, isAdminQuiz);
}

export function hasAdminPageCountMismatch(page: AdminPage<unknown>): boolean {
  const { page: pageNumber, size, total } = page.pagination;
  if (!Number.isSafeInteger(total)) return true;

  const offset = (pageNumber - 1) * size;
  const expectedItems = Math.min(size, Math.max(total - offset, 0));
  return page.items.length !== expectedItems;
}

export function isAdminLesson(value: unknown): value is AdminLesson {
  return isRecord(value)
    && Number.isInteger(value['id'])
    && Number.isInteger(value['course_id'])
    && typeof value['title'] === 'string'
    && (value['content'] === null || typeof value['content'] === 'string')
    && (value['video_url'] === null || typeof value['video_url'] === 'string')
    && Number.isInteger(value['order'])
    && typeof value['status'] === 'string';
}

export function isAdminLessonList(value: unknown): value is readonly AdminLesson[] {
  return Array.isArray(value) && value.every(isAdminLesson);
}

function isAdminContent(value: unknown): value is AdminContent {
  return isRecord(value)
    && Number.isInteger(value['id'])
    && Number.isInteger(value['course_id'])
    && typeof value['content_type'] === 'string'
    && typeof value['title'] === 'string'
    && isRecord(value['payload'])
    && value['status'] === 'PENDING_REVIEW'
    && (value['parent_id'] === undefined || value['parent_id'] === null || Number.isInteger(value['parent_id']))
    && Number.isInteger(value['order']);
}

function isAdminQuiz(value: unknown): value is AdminQuiz {
  return isRecord(value)
    && Number.isInteger(value['id'])
    && Number.isInteger(value['course_id'])
    && typeof value['title'] === 'string'
    && (value['duration_minutes'] === undefined
      || value['duration_minutes'] === null
      || Number.isInteger(value['duration_minutes']))
    && typeof value['passing_score'] === 'string'
    && Array.isArray(value['questions'])
    && value['questions'].every(isRecord);
}

function isFixedAdminPage<T>(
  value: unknown,
  requestedPage: number,
  isItem: (item: unknown) => item is T,
): value is AdminPage<T> {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isRecord(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  if (
    pagination['page'] !== requestedPage ||
    pagination['size'] !== 20 ||
    !isNonnegativeInteger(pagination['total']) ||
    !isNonnegativeSafeInteger(pagination['total_pages']) ||
    items.length > 20 ||
    !items.every(isItem)
  ) {
    return false;
  }

  if (Number.isSafeInteger(pagination['total'])) {
    const expectedPages = pagination['total'] === 0
      ? 0
      : Math.ceil(pagination['total'] / 20);
    return pagination['total_pages'] === expectedPages;
  }

  return true;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function isNonnegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

function isNonnegativeSafeInteger(value: unknown): value is number {
  return Number.isSafeInteger(value) && (value as number) >= 0;
}
