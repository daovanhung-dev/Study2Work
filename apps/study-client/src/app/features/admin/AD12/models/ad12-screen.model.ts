import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD12_API_BOUNDARY } from '../data-access/ad12-api-boundary';
import { AD12_UI } from '../ui/ad12-screen.ui';

export const AD12_SCREEN: AdminScreenDefinition = { ...AD12_UI, ...AD12_API_BOUNDARY };
