import type { ApiEnvelope } from '../../../../core/http/api-envelope';

export type AD01PeriodKey = 'today' | 'last7' | 'last30';

export interface AD01DateRange {
  from: string;
  to: string;
}

export type AD01MetricKey =
  | 'user_records_created'
  | 'course_records_created'
  | 'enrollment_records_created'
  | 'discussion_records_created';

export interface AD01ReportMetric {
  key: AD01MetricKey;
  value: string;
  label: string;
}

export interface AD01ReportSummary {
  period: AD01DateRange;
  metrics: readonly AD01ReportMetric[];
  generatedAt: string;
}

export interface AD01MetricCardModel {
  key: AD01MetricKey;
  title: string;
  value: string;
  description: string;
  icon: 'users' | 'book' | 'checklist' | 'activity';
}

const METRIC_ORDER: readonly AD01MetricKey[] = [
  'user_records_created',
  'course_records_created',
  'enrollment_records_created',
  'discussion_records_created',
];

const METRIC_ICONS: Record<AD01MetricKey, AD01MetricCardModel['icon']> = {
  user_records_created: 'users',
  course_records_created: 'book',
  enrollment_records_created: 'checklist',
  discussion_records_created: 'activity',
};

const PLACEHOLDER_LABELS: Record<AD01MetricKey, string> = {
  user_records_created: 'Tài khoản được tạo',
  course_records_created: 'Khóa học được tạo',
  enrollment_records_created: 'Lượt ghi danh được tạo',
  discussion_records_created: 'Bản ghi thảo luận được tạo',
};

/** Tạo kỳ date inclusive theo các ngày lịch Việt Nam, không phụ thuộc timezone trình duyệt. */
export function createAD01DateRange(period: AD01PeriodKey, now = new Date()): AD01DateRange {
  const parts = new Intl.DateTimeFormat('en-CA', {
    day: '2-digit',
    month: '2-digit',
    timeZone: 'Asia/Ho_Chi_Minh',
    year: 'numeric',
  }).formatToParts(now);
  const year = Number(parts.find((part) => part.type === 'year')?.value);
  const month = Number(parts.find((part) => part.type === 'month')?.value);
  const day = Number(parts.find((part) => part.type === 'day')?.value);
  const length = period === 'today' ? 1 : period === 'last7' ? 7 : 30;
  const end = new Date(Date.UTC(year, month - 1, day));
  const start = new Date(Date.UTC(year, month - 1, day - length + 1));

  return { from: start.toISOString().slice(0, 10), to: end.toISOString().slice(0, 10) };
}

/** Kiểm tra response #101 trước khi page đưa dữ liệu vào các card. */
export function parseAD01ReportSummary(
  envelope: ApiEnvelope<unknown>,
  expectedPeriod?: AD01DateRange,
): AD01ReportSummary | null {
  if (envelope.success !== true || envelope.businessCode !== 'DESIGN_RESOURCE_RETRIEVED') {
    return null;
  }
  if (!isRecord(envelope.data)) return null;

  const period = envelope.data['period'];
  const metrics = envelope.data['metrics'];
  const generatedAt = envelope.data['generated_at'];
  if (
    !isRecord(period) ||
    !isISODate(period['from']) ||
    !isISODate(period['to']) ||
    period['from'] > period['to'] ||
    (expectedPeriod !== undefined &&
      (period['from'] !== expectedPeriod.from || period['to'] !== expectedPeriod.to)) ||
    !Array.isArray(metrics) ||
    metrics.length !== METRIC_ORDER.length ||
    typeof generatedAt !== 'string' ||
    Number.isNaN(Date.parse(generatedAt))
  ) {
    return null;
  }

  const parsedMetrics: AD01ReportMetric[] = [];
  for (const key of METRIC_ORDER) {
    const metric = metrics.find((candidate: unknown) => isRecord(candidate) && candidate['key'] === key);
    if (
      !isRecord(metric) ||
      typeof metric['value'] !== 'string' ||
      !/^\d+$/.test(metric['value']) ||
      typeof metric['label'] !== 'string' ||
      !metric['label'].trim()
    ) {
      return null;
    }
    parsedMetrics.push({ key, value: metric['value'], label: metric['label'] });
  }

  return {
    period: { from: period['from'], to: period['to'] },
    metrics: parsedMetrics,
    generatedAt,
  };
}

/** Tạo bốn card cùng thứ tự API, giữ nguyên giá trị count dạng chuỗi. */
export function createAD01MetricCards(
  metrics?: readonly AD01ReportMetric[],
): AD01MetricCardModel[] {
  return METRIC_ORDER.map((key, index) => {
    const metric = metrics?.[index];
    return {
      key,
      title: metric?.label ?? PLACEHOLDER_LABELS[key],
      value: metric ? formatCount(metric.value) : '— —',
      description: 'Số bản ghi trong kỳ báo cáo',
      icon: METRIC_ICONS[key],
    };
  });
}

function formatCount(value: string): string {
  return value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isISODate(value: unknown): value is string {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00.000Z`);
  return !Number.isNaN(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
}
