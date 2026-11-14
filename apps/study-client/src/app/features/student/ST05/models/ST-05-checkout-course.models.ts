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
