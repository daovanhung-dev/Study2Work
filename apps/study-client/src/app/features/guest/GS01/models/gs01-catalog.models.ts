export const GS01_SORT_OPTIONS = [
  { label: 'Mới nhất', value: '' },
  { label: 'Cũ nhất', value: 'created_at:asc' },
  { label: 'Tên A–Z', value: 'name:asc' },
] as const;

export type GS01Sort = (typeof GS01_SORT_OPTIONS)[number]['value'];
