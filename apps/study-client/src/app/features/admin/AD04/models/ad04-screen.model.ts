import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD04_API_BOUNDARY } from '../data-access/ad04-api-boundary';
import { AD04_UI } from '../ui/ad04-screen.ui';

export const AD04_SCREEN: AdminScreenDefinition = { ...AD04_UI, ...AD04_API_BOUNDARY };
