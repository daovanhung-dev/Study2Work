import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD09_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#74",
    "#76",
    "#77"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#74 tải projection Course hiện có. Body/enum/transition của #76 và dependency/lifecycle của #77 còn mở; local #77 là soft marker chứ không phải permanent-delete policy đã duyệt. Không suy diễn archive thành trạng thái backend hoặc cho phép xóa từ mockup."
};
