export interface GuestCategory {
  id: number;
  name: string;
  slug: string;
  description?: string | null;
}

export interface GuestMentorSummary {
  id: number;
  full_name: string;
  avatar_url?: string | null;
}

export interface GuestPublicCourse {
  id: number;
  title: string;
  description?: string | null;
  thumbnail_url?: string | null;
  price: string;
  status: string;
  mentor: GuestMentorSummary;
}

export interface GuestCatalogPagination {
  page: number;
  size: number;
  total: number;
  total_pages: number;
}

export interface GuestCategoryPage {
  items: GuestCategory[];
  pagination: GuestCatalogPagination;
}

export interface GuestPublicCoursePage {
  items: GuestPublicCourse[];
  pagination: GuestCatalogPagination;
}
