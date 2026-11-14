export interface St04CourseSummary {
  id: number;
  title: string;
  description: string | null;
  price: string;
  status: string;
}

export interface St04CoursePage {
  items: St04CourseSummary[];
  pagination: {
    page: number;
    size: number;
    total: number;
    total_pages: number;
  };
}

export type St04CourseLoadState = 'loading' | 'ready' | 'missing' | 'error';
