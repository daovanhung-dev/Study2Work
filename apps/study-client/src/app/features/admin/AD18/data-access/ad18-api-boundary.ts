import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD18_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#90"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#90 là DELETE-only; source có hard-delete khi không có attempt/answer history và tombstone khi có history. Policy, quyền, audit và schema production còn mở; client không gửi DELETE."
};
