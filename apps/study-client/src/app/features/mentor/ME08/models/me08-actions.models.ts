export type Me08ActionIntent = 'publish' | 'unpublish' | 'delete';

/** Khớp ContentResponse của API #49 và #52 */
export interface Me08ContentNodeDto {
  id: number;
  course_id: number;
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
  status: string;
  parent_id?: number | null;
  order: number;
}

/** Khớp PublishContentRequest trong apps/study-server/app/modules/mentor/api_52_mentor_content_publish/models.py */
export interface PublishContentRequestDto {
  published: boolean;
}

/** Khớp DeleteResult trong apps/study-server/app/modules/mentor/api_53_mentor_content_delete/models.py */
export interface DeleteResultDto {
  id: number;
  status: 'deleted';
  deleted_at: string;
}

export interface Me08TargetInspectionVm {
  node: Me08ContentNodeDto;
  activeChildCount: number;
  canPublish: boolean;
  canUnpublish: boolean;
  canDelete: boolean;
  publishGuardNote: string;
  deleteGuardNote: string;
}

const SIGNED_INT64_PATTERN = /^[+-]?\d+$/;
const INT64_MIN = BigInt('-9223372036854775808');
const INT64_MAX = BigInt('9223372036854775807');

export function parseMe08Int64Param(raw: string | null | undefined): number | null {
  if (!raw || raw.length > 20 || !SIGNED_INT64_PATTERN.test(raw)) {
    return null;
  }
  try {
    const big = BigInt(raw);
    if (big < INT64_MIN || big > INT64_MAX) {
      return null;
    }
    const num = Number(big);
    return Number.isSafeInteger(num) ? num : null;
  } catch {
    return null;
  }
}

export function inspectTargetContent(
  node: Me08ContentNodeDto,
  allCourseNodes: readonly Me08ContentNodeDto[],
): Me08TargetInspectionVm {
  const activeChildCount = allCourseNodes.filter(
    (item) => (item.parent_id ?? null) === node.id,
  ).length;

  const isPublished = node.status === 'PUBLISHED';
  const isApproved = node.status === 'APPROVED';

  /**
   * Theo api_52/view.py:
   * - published=true chỉ cho phép khi status == 'APPROVED' (hoặc idempotent khi đã 'PUBLISHED')
   * - published=false chỉ cho phép khi status == 'PUBLISHED' (hoặc idempotent khi đã 'APPROVED')
   */
  const canPublish = isApproved;
  const canUnpublish = isPublished;

  let publishGuardNote = '';
  if (isPublished) {
    publishGuardNote =
      'Nội dung đang ở trạng thái PUBLISHED. Có thể gửi PATCH #52 { published: false } để đưa về APPROVED.';
  } else if (isApproved) {
    publishGuardNote =
      'Nội dung đang ở trạng thái APPROVED, đủ điều kiện gửi PATCH #52 { published: true } để xuất bản.';
  } else {
    publishGuardNote = `Nội dung đang ở trạng thái ${node.status}. Backend API #52 yêu cầu trạng thái APPROVED trước khi xuất bản (nếu gọi sẽ trả 422 DESIGN_VALIDATION_ERROR).`;
  }

  /**
   * Theo api_53/view.py:
   * - Không cho xóa nếu status == 'PUBLISHED' ("Unpublish Content before deleting it.")
   * - Không cho xóa nếu có con trực tiếp đang active ("Delete active child Content before deleting its parent.")
   */
  const canDelete = !isPublished && activeChildCount === 0;
  let deleteGuardNote = 'Nội dung đủ điều kiện xóa mềm (DELETE #53).';
  if (isPublished) {
    deleteGuardNote =
      'Không thể xóa trực tiếp khi nội dung đang PUBLISHED. Cần gỡ xuất bản (PATCH #52 { published: false }) trước khi xóa (#53).';
  } else if (activeChildCount > 0) {
    deleteGuardNote = `Nội dung đang có ${activeChildCount} mục con trực tiếp hoạt động. Cần xóa các mục con trước khi xóa mục cha (#53).`;
  }

  return {
    node,
    activeChildCount,
    canPublish,
    canUnpublish,
    canDelete,
    publishGuardNote,
    deleteGuardNote,
  };
}
