import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD16_API_BOUNDARY } from '../data-access/ad16-api-boundary';
import { AD16_UI } from '../ui/ad16-screen.ui';

export const AD16_SCREEN: AdminScreenDefinition = { ...AD16_UI, ...AD16_API_BOUNDARY };
