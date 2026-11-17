import type { ApiEnvelope } from '../../../../core/http/api-envelope';

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

export function readSH01Categories(
  response: ApiEnvelope<SH01CategoryPage>,
): SH01Category[] | null {
  if (
    !response.success
    || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
    || !Array.isArray(response.data?.items)
  ) {
    return null;
  }

  return response.data.items;
}

export function readSH01PublishedCourses(
  response: ApiEnvelope<SH01PublicCoursePage>,
): SH01PublicCourse[] | null {
  if (
    !response.success
    || response.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
    || !Array.isArray(response.data?.items)
  ) {
    return null;
  }

  return response.data.items.filter((course) => course.status === 'PUBLISHED');
}
