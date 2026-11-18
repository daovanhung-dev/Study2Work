export interface EnrolledCourse {
  course_id: number;
  name: string;
  enrollment_status: string;
  enrolled_at: string;
  description?: string | null;
}

export interface Achievement {
  id: number;
  code: string;
  title: string;
  awarded_at: string;
  course_id?: number | null;
}

export interface StudentNotification {
  id: number;
  title: string;
  content: string;
  is_read: boolean;
  created_at: string;
}

export type OverviewWidget<T> =
  | { readonly kind: 'loading' }
  | { readonly kind: 'ready'; readonly items: T[]; readonly total: number }
  | { readonly kind: 'empty' }
  | { readonly kind: 'contract-gap'; readonly message: string }
  | { readonly kind: 'error'; readonly message: string; readonly traceId?: string };

export type OverviewWidgetKey = 'courses' | 'progress' | 'achievements' | 'notifications';
