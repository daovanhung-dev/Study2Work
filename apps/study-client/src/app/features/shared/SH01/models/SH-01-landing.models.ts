export type LoadState = 'loading' | 'ready' | 'empty' | 'error';

export interface Pagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface Page<T> {
  items: T[];
  pagination: Pagination;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
}

export interface Course {
  id: number;
  title: string;
  description: string | null;
  thumbnail_url: string | null;
  price: string;
  status: string;
  mentor: {
    id: number;
    full_name: string;
    avatar_url: string | null;
  };
}
