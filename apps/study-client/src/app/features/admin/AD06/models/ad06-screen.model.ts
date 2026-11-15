import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD06_API_BOUNDARY } from '../data-access/ad06-api-boundary';
import { AD06_UI } from '../ui/ad06-screen.ui';

export const AD06_SCREEN: AdminScreenDefinition = { ...AD06_UI, ...AD06_API_BOUNDARY };
