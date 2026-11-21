import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD04_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#69",
    "#70"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#69 tải UserProfile theo raw route ID. Body full-replacement bốn trường và role allowlist của #70 chỉ là candidate local DERIVED; PII/role/permission policy chưa được duyệt. Trang không gọi PUT hoặc lưu dữ liệu."
};
