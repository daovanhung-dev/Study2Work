import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD07_API_BOUNDARY } from '../data-access/ad07-api-boundary';
import { AD07_UI } from '../ui/ad07-screen.ui';

export const AD07_SCREEN: AdminScreenDefinition = { ...AD07_UI, ...AD07_API_BOUNDARY };
