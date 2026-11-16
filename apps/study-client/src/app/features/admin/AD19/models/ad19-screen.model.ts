import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD19_API_BOUNDARY } from '../data-access/ad19-api-boundary';
import { AD19_UI } from '../ui/ad19-screen.ui';

export const AD19_SCREEN: AdminScreenDefinition = { ...AD19_UI, ...AD19_API_BOUNDARY };
