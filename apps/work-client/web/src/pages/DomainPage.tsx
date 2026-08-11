import {
  ArrowRight,
  CheckCircle2,
  DatabaseZap,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";
import { Link } from "react-router-dom";

export type WorkArea = "public" | "candidate" | "enterprise" | "university" | "ops";

export interface DomainPageProps {
  apiScope: string;
  area: WorkArea;
  description: string;
  icon: LucideIcon;
  nextStep?: {
    label: string;
    to: string;
  };
  safeguards: string[];
  title: string;
}

const areaLabel: Record<WorkArea, string> = {
  public: "Work public",
  candidate: "Không gian ứng viên",
  enterprise: "Không gian doanh nghiệp",
  university: "Không gian trường đại học",
  ops: "Vận hành Work",
};

export function DomainPage({
  apiScope,
  area,
  description,
  icon: Icon,
  nextStep,
  safeguards,
  title,
}: DomainPageProps) {
  return (
    <section aria-labelledby="screen-title" className="mx-auto max-w-6xl">
      <div className="rounded-2xl border border-work-100 bg-linear-to-br from-white via-white to-work-50 p-6 shadow-sm sm:p-8">
        <div className="flex flex-col justify-between gap-6 sm:flex-row sm:items-start">
          <div className="max-w-3xl">
            <div className="flex items-center gap-3 text-work-700">
              <span className="flex size-11 items-center justify-center rounded-xl bg-work-100">
                <Icon aria-hidden="true" size={22} />
              </span>
              <p className="text-sm font-semibold uppercase tracking-[0.16em]">{areaLabel[area]}</p>
            </div>
            <h1 className="mt-6 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl" id="screen-title">
              {title}
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">{description}</p>
          </div>
          <span className="inline-flex w-fit items-center rounded-full border border-work-200 bg-white px-3 py-1 text-xs font-semibold text-work-800">
            Nền tảng sẵn sàng tích hợp
          </span>
        </div>
        {nextStep ? (
          <Link
            className="mt-7 inline-flex min-h-11 items-center gap-2 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800"
            to={nextStep.to}
          >
            {nextStep.label}
            <ArrowRight aria-hidden="true" size={18} />
          </Link>
        ) : null}
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <DatabaseZap aria-hidden="true" className="text-work-700" size={21} />
          <h2 className="mt-4 text-base font-semibold text-slate-950">Dữ liệu từ API</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Màn hình sẽ đọc dữ liệu đã chuẩn hóa từ {apiScope}; client chỉ giữ state giao diện và
            query cache trong bộ nhớ.
          </p>
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <ShieldCheck aria-hidden="true" className="text-work-700" size={21} />
          <h2 className="mt-4 text-base font-semibold text-slate-950">Quyền do server quyết định</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Route guard cải thiện trải nghiệm; API vẫn xác thực session, membership, permission và
            phạm vi tài nguyên.
          </p>
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <CheckCircle2 aria-hidden="true" className="text-work-700" size={21} />
          <h2 className="mt-4 text-base font-semibold text-slate-950">Hành vi cần giữ khi triển khai</h2>
          <ul className="mt-2 space-y-2 text-sm leading-6 text-slate-600">
            {safeguards.map((safeguard) => (
              <li className="flex gap-2" key={safeguard}>
                <span aria-hidden="true" className="mt-2 size-1.5 shrink-0 rounded-full bg-work-600" />
                <span>{safeguard}</span>
              </li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}
