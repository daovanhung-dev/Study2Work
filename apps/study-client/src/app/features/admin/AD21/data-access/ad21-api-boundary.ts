import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD21_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#94",
    "#95",
    "#96"
  ],
  "sourceState": "data-backed",
  "sourceNote": "API #96 đọc Notification cùng delivery aggregate; chỉ ID/title/content/channels/status/created_at được map. #94/#95 mutations không được gọi; edit/delete, recipient và per-channel progress giữ unavailable."
};
