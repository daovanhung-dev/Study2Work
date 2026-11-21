import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD20_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#68",
    "#93"
  ],
  "sourceState": "data-backed",
  "sourceNote": "#68 cung cấp danh sách người dùng phân trang để chọn recipients tường minh; #93 nhận recipient IDs, title/content và kênh PUSH|EMAIL, rồi trả operation_id trong meta. HTTP 202 chỉ xác nhận QUEUED, không chứng minh delivery."
};
