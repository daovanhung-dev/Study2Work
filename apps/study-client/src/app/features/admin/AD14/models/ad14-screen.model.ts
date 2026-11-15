import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD14_API_BOUNDARY } from '../data-access/ad14-api-boundary';
import { AD14_UI } from '../ui/ad14-screen.ui';

export const AD14_SCREEN: AdminScreenDefinition = { ...AD14_UI, ...AD14_API_BOUNDARY };
