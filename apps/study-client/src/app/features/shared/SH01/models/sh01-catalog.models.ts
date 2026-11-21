export interface SH01Category {
  id: number;
  name: string;
  slug: string;
  description?: string | null;
}

export interface SH01CategoryPage {
  items: SH01Category[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export interface SH01PublicCourse {
  id: number;
  title: string;
  description?: string | null;
  thumbnail_url?: string | null;
  price: string;
  status: string;
  mentor: {
    id: number;
    full_name: string;
    avatar_url?: string | null;
  };
}

export interface SH01PublicCoursePage {
  items: SH01PublicCourse[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export function readSH01Categories(response: unknown): SH01Category[] | null {
  const data = readSuccessfulData(response);
  if (!isRecord(data) || !Array.isArray(data['items'])) {
    return null;
  }

  const rawItems = data['items'];
  const items = rawItems.filter(isCategory);
  if (
    items.length !== rawItems.length
    || !isCategoryPagination(data['pagination'], items.length)
  ) {
    return null;
  }

  return items;
}

export function readSH01PublishedCourses(response: unknown): SH01PublicCourse[] | null {
  const data = readSuccessfulData(response);
  if (!isRecord(data) || !Array.isArray(data['items'])) {
    return null;
  }

  const rawItems = data['items'];
  const courses = rawItems.filter(isPublicCourse);
  if (
    courses.length !== rawItems.length
    || !isCoursePagination(data['pagination'], courses.length)
  ) {
    return null;
  }

  return courses.filter((course) => course.status === 'PUBLISHED');
}

function readSuccessfulData(response: unknown): unknown {
  if (
    !isRecord(response)
    || response['success'] !== true
    || response['businessCode'] !== 'DESIGN_RESOURCE_RETRIEVED'
  ) {
    return null;
  }

  return response['data'];
}

function isCategory(value: unknown): value is SH01Category {
  return isRecord(value)
    && isPositiveInteger(value['id'])
    && typeof value['name'] === 'string'
    && typeof value['slug'] === 'string'
    && isOptionalNullableString(value['description']);
}

function isPublicCourse(value: unknown): value is SH01PublicCourse {
  if (!isRecord(value)) {
    return false;
  }

  const mentor = value['mentor'];
  if (!isRecord(mentor)) {
    return false;
  }

  return isPositiveInteger(value['id'])
    && typeof value['title'] === 'string'
    && isOptionalNullableString(value['description'])
    && isOptionalNullableString(value['thumbnail_url'])
    && typeof value['price'] === 'string'
    && typeof value['status'] === 'string'
    && isPositiveInteger(mentor['id'])
    && typeof mentor['full_name'] === 'string'
    && isOptionalNullableString(mentor['avatar_url']);
}

function isCategoryPagination(value: unknown, itemCount: number): boolean {
  return isRecord(value)
    && value['page'] === 1
    && value['size'] === itemCount
    && value['total'] === itemCount
    && value['total_pages'] === 1;
}

function isCoursePagination(value: unknown, itemCount: number): boolean {
  if (!isRecord(value)) {
    return false;
  }

  const total = value['total'];
  const totalPages = value['total_pages'];
  if (
    value['page'] !== 1
    || value['size'] !== 6
    || !isNonNegativeInteger(total)
    || !isNonNegativeInteger(totalPages)
    || itemCount > 6
  ) {
    return false;
  }

  const expectedTotalPages = total === 0 ? 0 : Math.ceil(total / 6);
  return totalPages === expectedTotalPages;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isOptionalNullableString(value: unknown): value is string | null | undefined {
  return value === undefined || value === null || typeof value === 'string';
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isNonNegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}
