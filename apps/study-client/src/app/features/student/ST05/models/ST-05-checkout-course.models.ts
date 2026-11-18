export interface St05CourseSummary {
  id: number;
  title: string;
  description: string | null;
  price: string;
  status: string;
}

export interface St05CoursePage {
  items: St05CourseSummary[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export type St05CourseLoadState = 'loading' | 'ready' | 'missing' | 'error';

/** Backend API #16 returns this Order only after explicit creation. */
export interface St05Order {
  id: number;
  course_id: number;
  user_id: number;
  amount: string;
  currency: 'VND';
  status: string;
  created_at: string;
}
