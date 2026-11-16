import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD20_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#93"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#93 yêu cầu recipients int64, title/content và kênh PUSH|EMAIL nhưng từ chối segment; response/permission/provider còn mở. HTTP 202 không chứng minh delivery; client không gửi."
};
