import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD17_API_BOUNDARY } from '../data-access/ad17-api-boundary';
import { AD17_UI } from '../ui/ad17-screen.ui';

export const AD17_SCREEN: AdminScreenDefinition = { ...AD17_UI, ...AD17_API_BOUNDARY };
