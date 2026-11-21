import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD09_API_BOUNDARY } from '../data-access/ad09-api-boundary';
import { AD09_UI } from '../ui/ad09-screen.ui';

export const AD09_SCREEN: AdminScreenDefinition = { ...AD09_UI, ...AD09_API_BOUNDARY };
