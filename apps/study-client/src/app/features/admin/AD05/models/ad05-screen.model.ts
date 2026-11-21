import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD05_API_BOUNDARY } from '../data-access/ad05-api-boundary';
import { AD05_UI } from '../ui/ad05-screen.ui';

export const AD05_SCREEN: AdminScreenDefinition = { ...AD05_UI, ...AD05_API_BOUNDARY };
