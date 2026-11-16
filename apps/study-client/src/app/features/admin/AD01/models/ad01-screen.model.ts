import { AD01_API_BOUNDARY } from '../data-access/ad01-api-boundary';

export const AD01_SCREEN_MODEL = {
  id: 'AD01',
  title: 'Bảng điều khiển quản trị hệ thống',
  ...AD01_API_BOUNDARY,
} as const;

