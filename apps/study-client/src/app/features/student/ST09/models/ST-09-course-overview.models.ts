export interface CourseProgress {
  course_id: number;
  completed_lessons: number;
  total_lessons: number;
  progress_percent: number;
  has_content: boolean;
}

export interface CourseLesson {
  id: number;
  title: string;
  order: number;
  status: string;
}

export interface StudentCourseOverviewState {
  readonly kind: 'loading' | 'ready' | 'not-enrolled' | 'missing-context' | 'error';
  readonly title: string;
  readonly message: string;
  readonly progress?: CourseProgress;
  readonly lessons?: CourseLesson[];
}
