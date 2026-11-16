import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD13_API_BOUNDARY } from '../data-access/ad13-api-boundary';
import { AD13_UI } from '../ui/ad13-screen.ui';

export const AD13_SCREEN: AdminScreenDefinition = { ...AD13_UI, ...AD13_API_BOUNDARY };
