import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD08_API_BOUNDARY } from '../data-access/ad08-api-boundary';
import { AD08_UI } from '../ui/ad08-screen.ui';

export const AD08_SCREEN: AdminScreenDefinition = { ...AD08_UI, ...AD08_API_BOUNDARY };
