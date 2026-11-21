import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD15_API_BOUNDARY } from '../data-access/ad15-api-boundary';
import { AD15_UI } from '../ui/ad15-screen.ui';

export const AD15_SCREEN: AdminScreenDefinition = { ...AD15_UI, ...AD15_API_BOUNDARY };
