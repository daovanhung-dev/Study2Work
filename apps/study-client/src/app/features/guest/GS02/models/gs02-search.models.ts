export interface GS02CourseMentor {
  id: number;
  full_name: string;
  avatar_url?: string | null;
}

export interface GS02Course {
  id: number;
  title: string;
  description?: string | null;
  thumbnail_url?: string | null;
  price: string;
  status: string;
  mentor: GS02CourseMentor;
}

export interface GS02Pagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface GS02CourseSearchPage {
  items: GS02Course[];
  pagination: GS02Pagination;
}

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
