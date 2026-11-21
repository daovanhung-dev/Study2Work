export interface GuestCategory {
  id: number;
  name: string;
  slug: string;
  description?: string | null;
}

export interface GuestMentorSummary {
  id: number;
  full_name: string;
  avatar_url?: string | null;
}

export interface GuestPublicCourse {
  id: number;
  title: string;
  description?: string | null;
  thumbnail_url?: string | null;
  price: string;
  status: string;
  mentor: GuestMentorSummary;
}

export interface GuestCatalogPagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface GuestCategoryPage {
  items: GuestCategory[];
  pagination: GuestCatalogPagination;
}

export interface GuestPublicCoursePage {
  items: GuestPublicCourse[];
  pagination: GuestCatalogPagination;
}

export function isGuestResourceSuccessEnvelope(
  value: unknown,
): value is { success: true; businessCode: string; data: unknown } {
  return (
    isRecord(value) &&
    value['success'] === true &&
    typeof value['businessCode'] === 'string' &&
    'data' in value
  );
}

export function isGuestCategoryPage(value: unknown): value is GuestCategoryPage {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isCatalogPagination(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  return (
    items.every(isGuestCategory) &&
    pagination.page === 1 &&
    pagination.size === items.length &&
    pagination.total === items.length &&
    pagination.total_pages === 1
  );
}

export function isGuestPublicCoursePage(value: unknown): value is GuestPublicCoursePage {
  if (!isRecord(value) || !Array.isArray(value['items']) || !isCatalogPagination(value['pagination'])) {
    return false;
  }

  const items = value['items'];
  const pagination = value['pagination'];
  const expectedTotalPages =
    pagination.total === 0 ? 0 : Math.ceil(pagination.total / pagination.size);
  return (
    items.every(isGuestPublicCourse) &&
    pagination.size > 0 &&
    items.length <= pagination.size &&
    pagination.total_pages === expectedTotalPages
  );
}

export function hasGuestPublicCoursePageCountMismatch(page: GuestPublicCoursePage): boolean {
  const { page: pageNumber, size, total } = page.pagination;
  const offset = (pageNumber - 1) * size;
  const expectedItems = Math.min(size, Math.max(total - offset, 0));
  return page.items.length !== expectedItems;
}

function isGuestCategory(value: unknown): value is GuestCategory {
  if (!isRecord(value)) return false;
  return (
    isPositiveInteger(value['id']) &&
    typeof value['name'] === 'string' &&
    typeof value['slug'] === 'string' &&
    isOptionalNullableString(value['description'])
  );
}

function isGuestPublicCourse(value: unknown): value is GuestPublicCourse {
  if (!isRecord(value) || !isRecord(value['mentor'])) return false;
  const mentor = value['mentor'];
  return (
    isPositiveInteger(value['id']) &&
    typeof value['title'] === 'string' &&
    isOptionalNullableString(value['description']) &&
    isOptionalNullableString(value['thumbnail_url']) &&
    typeof value['price'] === 'string' &&
    typeof value['status'] === 'string' &&
    isPositiveInteger(mentor['id']) &&
    typeof mentor['full_name'] === 'string' &&
    isOptionalNullableString(mentor['avatar_url'])
  );
}

function isCatalogPagination(
  value: unknown,
): value is GuestCatalogPagination {
  if (!isRecord(value)) return false;
  return (
    isPositiveInteger(value['page']) &&
    isNonnegativeInteger(value['size']) &&
    isNonnegativeInteger(value['total']) &&
    isNonnegativeInteger(value['total_pages'])
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}

function isNonnegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

function isOptionalNullableString(value: unknown): value is string | null | undefined {
  return value === undefined || value === null || typeof value === 'string';
}
