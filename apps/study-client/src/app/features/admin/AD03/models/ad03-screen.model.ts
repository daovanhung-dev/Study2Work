import type { AdminScreenDefinition } from '../../../../shared/ui/admin-screen.model';
import { AD03_API_BOUNDARY } from '../data-access/ad03-api-boundary';
import { AD03_UI } from '../ui/ad03-screen.ui';

export const AD03_SCREEN: AdminScreenDefinition = { ...AD03_UI, ...AD03_API_BOUNDARY };
