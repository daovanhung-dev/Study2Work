import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD23_API_BOUNDARY } from '../data-access/ad23-api-boundary';
import { AD23_UI } from '../ui/ad23-screen.ui';

export const AD23_SCREEN: AdminScreenDefinition = { ...AD23_UI, ...AD23_API_BOUNDARY };
