export interface GuestCurriculumLesson {
  id: number;
  course_id: number;
  title: string;
  content: string | null;
  video_url: string | null;
  order: number;
  status: string;
}

export interface GuestCurriculumPagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface GuestCourseCurriculumPage {
  items: GuestCurriculumLesson[];
  pagination: GuestCurriculumPagination;
}

export interface GuestCurriculumLessonSummary {
  title: string;
  order: number;
}

export type GuestCurriculumState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'empty' }
  | { status: 'ready'; lessons: GuestCurriculumLessonSummary[] }
  | { status: 'not-found' }
  | { status: 'error' };

export function toGuestCurriculumLessonSummaries(
  items: GuestCurriculumLesson[],
): GuestCurriculumLessonSummary[] {
  return items.map(({ title, order }) => ({ title, order }));
}
