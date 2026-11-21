import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD21_API_BOUNDARY } from '../data-access/ad21-api-boundary';
import { AD21_UI } from '../ui/ad21-screen.ui';

export const AD21_SCREEN: AdminScreenDefinition = { ...AD21_UI, ...AD21_API_BOUNDARY };
