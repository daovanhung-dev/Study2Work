import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD25_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#103",
    "#18"
  ],
  "sourceState": "api-absent",
  "sourceNote": "Không có route export, worker, artifact storage hoặc download handler trong Study Server. Response #103 và ID/type #18 cũng chưa được thống nhất; không tạo job hoặc file giả."
};
