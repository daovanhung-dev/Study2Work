export type ContentPublicationStatus =
  | 'DRAFT'
  | 'PENDING_REVIEW'
  | 'APPROVED'
  | 'PUBLISHED'
  | string;

/** Khớp ContentResponse trong apps/study-server/app/modules/mentor/api_49_mentor_content_list/models.py */
export interface ContentNodeDto {
  id: number;
  course_id: number;
  content_type: string;
  title: string;
  payload: Record<string, unknown>;
  status: ContentPublicationStatus;
  /** Backend dùng exclude_none=True nên root node có thể trả undefined hoặc null */
  parent_id?: number | null;
  order: number;
}

export interface ContentTreeItemVm {
  node: ContentNodeDto;
  depth: number;
  hasActiveChildren: boolean;
  children: ContentTreeItemVm[];
}

export interface ContentKpiSummaryVm {
  rootSectionsCount: number;
  publishedCount: number;
  draftOrPendingCount: number;
  totalNodesCount: number;
}

export type ContentStatusFilter = 'ALL' | 'PUBLISHED' | 'DRAFT_OR_PENDING';

const SIGNED_INT64_PATTERN = /^[+-]?\d+$/;
const INT64_MIN = BigInt('-9223372036854775808');
const INT64_MAX = BigInt('9223372036854775807');

export function parseSignedInt64Param(raw: string | null | undefined): number | null {
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

export function buildContentTree(nodes: readonly ContentNodeDto[]): ContentTreeItemVm[] {
  const byParent = new Map<number | null, ContentNodeDto[]>();
  const activeParentIds = new Set<number>();

  for (const item of nodes) {
    const parentKey = item.parent_id ?? null;
    if (parentKey !== null) {
      activeParentIds.add(parentKey);
    }
    const group = byParent.get(parentKey) ?? [];
    group.push(item);
    byParent.set(parentKey, group);
  }

  for (const group of byParent.values()) {
    group.sort((a, b) => a.order - b.order || a.id - b.id);
  }

  const visit = (parentId: number | null, depth: number, seen: Set<number>): ContentTreeItemVm[] => {
    const list = byParent.get(parentId) ?? [];
    const result: ContentTreeItemVm[] = [];

    for (const node of list) {
      if (seen.has(node.id)) {
        continue;
      }
      const nextSeen = new Set(seen);
      nextSeen.add(node.id);
      const children = visit(node.id, depth + 1, nextSeen);
      result.push({
        node,
        depth,
        hasActiveChildren: activeParentIds.has(node.id),
        children,
      });
    }
    return result;
  };

  return visit(null, 0, new Set<number>());
}

export function computeContentKpi(nodes: readonly ContentNodeDto[]): ContentKpiSummaryVm {
  let rootSectionsCount = 0;
  let publishedCount = 0;
  let draftOrPendingCount = 0;

  for (const item of nodes) {
    if (item.parent_id === null || item.parent_id === undefined) {
      rootSectionsCount += 1;
    }
    if (item.status === 'PUBLISHED') {
      publishedCount += 1;
    } else {
      draftOrPendingCount += 1;
    }
  }

  return {
    rootSectionsCount,
    publishedCount,
    draftOrPendingCount,
    totalNodesCount: nodes.length,
  };
}

export function filterContentTree(
  tree: readonly ContentTreeItemVm[],
  statusFilter: ContentStatusFilter,
  keyword: string,
): ContentTreeItemVm[] {
  const normalizedKeyword = keyword.trim().toLowerCase();

  const matchesNode = (node: ContentNodeDto): boolean => {
    const statusOk =
      statusFilter === 'ALL' ||
      (statusFilter === 'PUBLISHED' && node.status === 'PUBLISHED') ||
      (statusFilter === 'DRAFT_OR_PENDING' && node.status !== 'PUBLISHED');
    const keywordOk =
      normalizedKeyword.length === 0 ||
      node.title.toLowerCase().includes(normalizedKeyword) ||
      node.content_type.toLowerCase().includes(normalizedKeyword);
    return statusOk && keywordOk;
  };

  const filterBranch = (items: readonly ContentTreeItemVm[]): ContentTreeItemVm[] => {
    const out: ContentTreeItemVm[] = [];
    for (const item of items) {
      const filteredChildren = filterBranch(item.children);
      if (matchesNode(item.node) || filteredChildren.length > 0) {
        out.push({
          ...item,
          children: filteredChildren,
        });
      }
    }
    return out;
  };

  return filterBranch(tree);
}

export function formatStatusLabel(status: ContentPublicationStatus): string {
  switch (status) {
    case 'PUBLISHED':
      return 'Đã xuất bản';
    case 'APPROVED':
      return 'Đã duyệt (Sẵn sàng xuất bản)';
    case 'PENDING_REVIEW':
      return 'Chờ duyệt (Bản nháp)';
    case 'DRAFT':
      return 'Bản nháp';
    default:
      return status || 'Chưa xác định';
  }
}
