import type { AdminScreenApiBoundary } from '../../../../shared/ui/admin-screen.model';

export const AD05_API_BOUNDARY: AdminScreenApiBoundary = {
  "apiReferences": [
    "#69",
    "#71",
    "#72"
  ],
  "sourceState": "contract-blocked",
  "sourceNote": "#69 tải UserProfile theo raw route ID. Candidate status/session effect của #71 và lifecycle/retention của #72 chưa được duyệt; local #72 chỉ đặt status DELETED. Không gọi mutation hoặc khẳng định audit, anonymization hay immediate access revocation."
};
