import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD16_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#88",
    "#89"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#88 có nested shape DERIVED; #89 catalog chưa khai báo body; không có GET chi tiết để nạp form sửa. Lưu và thêm câu hỏi đang khóa."
};
