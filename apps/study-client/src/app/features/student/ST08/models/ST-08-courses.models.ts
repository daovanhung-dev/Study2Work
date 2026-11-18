export interface EnrolledCourse {
  readonly course_id: number;
  readonly name: string;
  readonly description: string | null;
  readonly thumbnail_url: string | null;
  readonly enrollment_status: string;
  readonly enrolled_at: string;
}

export interface CoursePage {
  readonly items: EnrolledCourse[];
  readonly pagination: {
    readonly page: number;
    readonly size: number;
    readonly total: number;
    readonly total_pages: number;
  };
}

export type StudentCoursesState =
  | { readonly kind: 'loading' }
  | { readonly kind: 'empty' }
  | { readonly kind: 'ready'; readonly page: CoursePage }
  | { readonly kind: 'error'; readonly message: string; readonly traceId?: string };
