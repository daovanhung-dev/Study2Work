import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD11_API_BOUNDARY } from '../data-access/ad11-api-boundary';
import { AD11_UI } from '../ui/ad11-screen.ui';

export const AD11_SCREEN: AdminScreenDefinition = { ...AD11_UI, ...AD11_API_BOUNDARY };
