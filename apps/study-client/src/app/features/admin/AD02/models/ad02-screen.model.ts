import { AD02_API_BOUNDARY } from '../data-access/ad02-api-boundary';
import { AD02_COLUMNS } from '../ui/ad02-screen.ui';

export const AD02_SCREEN_MODEL = {
  id: 'AD02',
  title: 'Danh sách người dùng',
  columns: AD02_COLUMNS,
  ...AD02_API_BOUNDARY,
} as const;

