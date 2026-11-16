import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD22_API_BOUNDARY } from '../data-access/ad22-api-boundary';
import { AD22_UI } from '../ui/ad22-screen.ui';

export const AD22_SCREEN: AdminScreenDefinition = { ...AD22_UI, ...AD22_API_BOUNDARY };
