import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD10_API_BOUNDARY } from '../data-access/ad10-api-boundary';
import { AD10_UI } from '../ui/ad10-screen.ui';

export const AD10_SCREEN: AdminScreenDefinition = { ...AD10_UI, ...AD10_API_BOUNDARY };
