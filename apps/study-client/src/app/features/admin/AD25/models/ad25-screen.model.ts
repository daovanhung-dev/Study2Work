import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD25_API_BOUNDARY } from '../data-access/ad25-api-boundary';
import { AD25_UI } from '../ui/ad25-screen.ui';

export const AD25_SCREEN: AdminScreenDefinition = { ...AD25_UI, ...AD25_API_BOUNDARY };
