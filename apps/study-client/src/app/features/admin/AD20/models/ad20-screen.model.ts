import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD20_API_BOUNDARY } from '../data-access/ad20-api-boundary';
import { AD20_UI } from '../ui/ad20-screen.ui';

export const AD20_SCREEN: AdminScreenDefinition = { ...AD20_UI, ...AD20_API_BOUNDARY };
