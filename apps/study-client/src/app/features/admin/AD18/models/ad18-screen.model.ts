import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD18_API_BOUNDARY } from '../data-access/ad18-api-boundary';
import { AD18_UI } from '../ui/ad18-screen.ui';

export const AD18_SCREEN: AdminScreenDefinition = { ...AD18_UI, ...AD18_API_BOUNDARY };
