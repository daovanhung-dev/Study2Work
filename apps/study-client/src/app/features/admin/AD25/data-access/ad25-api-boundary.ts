import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD25_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#103",
    "#18"
  ],
  "sourceState": "api-absent",
  "sourceNote": "#103 không có Study Server route/worker; #18 có route nhưng chỉ đọc notification operations. T041 duyệt UUID owner-only và status policy cho export, nhưng producer/result/artifact mapping chưa có; không gửi request hoặc tạo file giả."
};
