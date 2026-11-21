import type {
  GuestCatalogPagination,
  GuestMentorSummary,
  GuestPublicCourse,
  GuestPublicCoursePage,
} from '../../shared/models/guest-course.models';

export type GS02CourseMentor = GuestMentorSummary;
export type GS02Course = GuestPublicCourse;
export type GS02Pagination = GuestCatalogPagination;
export type GS02CourseSearchPage = GuestPublicCoursePage;

export type GS02SearchState =
  | { status: 'prompt' }
  | { status: 'loading'; query: string; page: number }
  | { status: 'ready'; query: string; result: GS02CourseSearchPage }
  | { status: 'no-results'; query: string }
  | { status: 'out-of-range'; query: string; page: number; total: number; totalPages: number }
  | { status: 'error'; query: string; page: number };

export function normalizeGS02Query(query: string): string {
  return query.trim().toLowerCase();
}
