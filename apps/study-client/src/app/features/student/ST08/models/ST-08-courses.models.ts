export interface StudentCourse {
  course_id: number;
  name: string;
  description: string | null;
  thumbnail_url: string | null;
  price: string | null;
  course_status: string | null;
  enrollment_status: string;
  enrolled_at: string;
}

export interface StudentCoursesPageData {
  items: StudentCourse[];
  pagination: { page: number; size: number; total: number; total_pages: number };
}

export interface StudentCoursesState {
  readonly kind: 'loading' | 'ready' | 'empty' | 'error';
  readonly title: string;
  readonly message: string;
  readonly items: StudentCourse[];
  readonly pagination?: StudentCoursesPageData['pagination'];
}
