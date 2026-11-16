import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD24_API_BOUNDARY } from '../data-access/ad24-api-boundary';
import { AD24_UI } from '../ui/ad24-screen.ui';

export const AD24_SCREEN: AdminScreenDefinition = { ...AD24_UI, ...AD24_API_BOUNDARY };
