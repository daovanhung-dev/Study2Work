import {
  BarChart3,
  BriefcaseBusiness,
  Building2,
  CircleUserRound,
  ClipboardList,
  CreditCard,
  FileText,
  GraduationCap,
  LayoutDashboard,
  Mail,
  Search,
  Settings,
  ShieldCheck,
  UsersRound,
} from "lucide-react";
import { createBrowserRouter, Navigate } from "react-router-dom";

import { DomainPage, type DomainPageProps } from "@/pages/DomainPage";
import { NotFoundPage, RouteErrorPage } from "@/pages/StatePages";

import { RequireAccess, type AccessRequirement } from "./guards";
import { PublicLayout, WorkspaceLayout } from "./layouts";

function screen(props: DomainPageProps) {
  return <DomainPage {...props} />;
}

const candidateAccess: AccessRequirement = {
  authenticated: true,
  requireVerifiedEmail: true,
  roles: ["CANDIDATE"],
};

const enterpriseAccess: AccessRequirement = {
  authenticated: true,
  requireVerifiedEmail: true,
  roles: ["ENTERPRISE_MEMBER"],
  tenantType: "ENTERPRISE",
};

const universityAccess: AccessRequirement = {
  authenticated: true,
  requireVerifiedEmail: true,
  roles: ["UNIVERSITY_MEMBER"],
  tenantType: "UNIVERSITY",
};

const authenticatedAccess: AccessRequirement = {
  authenticated: true,
  requireVerifiedEmail: true,
};

export const router = createBrowserRouter([
  {
    errorElement: <RouteErrorPage />,
    children: [
      {
        element: <PublicLayout />,
        children: [
          { index: true, element: <Navigate replace to="/jobs" /> },
          {
            path: "jobs",
            element: screen({
              apiScope: "API-WRK-001",
              area: "public",
              description:
                "Danh mục việc làm công khai sẽ hỗ trợ tìm kiếm, bộ lọc URL, phân trang và vị trí được tài trợ có nhãn rõ ràng.",
              icon: BriefcaseBusiness,
              nextStep: { label: "Mở chi tiết việc làm", to: "/jobs/example-role" },
              safeguards: [
                "Nguồn lọc và sắp xếp là URL, không ghi nhận truy vấn nhạy cảm vào analytics.",
                "Vị trí tài trợ tách khỏi xếp hạng organic và luôn có nhãn bằng chữ.",
              ],
              title: "Khám phá việc làm phù hợp",
            }),
          },
          {
            path: "jobs/:jobSlug",
            element: screen({
              apiScope: "API-WRK-002",
              area: "public",
              description:
                "Chi tiết việc làm sẽ hiển thị revision đã xuất bản, doanh nghiệp, mức lương và hạn tuyển do server xác nhận.",
              icon: FileText,
              nextStep: { label: "Bắt đầu ứng tuyển", to: "/jobs/example-role/apply" },
              safeguards: [
                "Trạng thái nhận hồ sơ và revision được kiểm tra lại ngay trước khi nộp.",
                "Lưu việc làm yêu cầu phiên ứng viên; không dùng client để quyết định eligibility.",
              ],
              title: "Chi tiết việc làm",
            }),
          },
          {
            path: "companies/:companySlug",
            element: screen({
              apiScope: "API-WRK-003",
              area: "public",
              description:
                "Trang doanh nghiệp chỉ dùng public projection đã được phép công bố cùng các tin đang hoạt động.",
              icon: Building2,
              safeguards: [
                "Không hiển thị thành viên nội bộ, tài liệu pháp lý hoặc dữ liệu xác minh riêng tư.",
                "Huy hiệu xác minh chỉ xuất hiện khi server cấp public projection phù hợp.",
              ],
              title: "Hồ sơ doanh nghiệp",
            }),
          },
          {
            element: <RequireAccess requirement={candidateAccess} />,
            children: [
              {
                path: "jobs/:jobId/apply",
                element: screen({
                  apiScope: "API-WRK-022 và API-WRK-023",
                  area: "candidate",
                  description:
                    "Luồng ứng tuyển sẽ tập hợp snapshot công việc, CV đã xuất bản, câu trả lời và lựa chọn Study evidence do ứng viên xác nhận rõ ràng.",
                  icon: ClipboardList,
                  nextStep: { label: "Xem đơn ứng tuyển", to: "/candidate/applications" },
                  safeguards: [
                    "Một idempotency key được giữ xuyên suốt lần gửi và retry.",
                    "Study evidence không sẵn sàng không đồng nghĩa bị từ chối ứng tuyển.",
                  ],
                  title: "Ứng tuyển việc làm",
                }),
              },
            ],
          },
          {
            element: <RequireAccess requirement={authenticatedAccess} />,
            children: [
              {
                path: "enterprise/create",
                element: screen({
                  apiScope: "API-WRK-035",
                  area: "enterprise",
                  description:
                    "Quy trình tạo doanh nghiệp sẽ thu thập legal identity, thông tin liên hệ và điều khoản trước khi tạo workspace ở trạng thái xác minh.",
                  icon: Building2,
                  safeguards: [
                    "Server xử lý claim trùng lặp và không cho người tạo tự xác minh.",
                    "Dữ liệu pháp lý chỉ gửi khi người dùng chủ động xác nhận ở bước review.",
                  ],
                  title: "Tạo không gian doanh nghiệp",
                }),
              },
              {
                path: "university/create",
                element: screen({
                  apiScope: "API-UNI-001",
                  area: "university",
                  description:
                    "Quy trình tạo trường đại học sẽ thu thập identity, mã cơ sở và liên hệ trước khi mở workspace đang chờ xác minh.",
                  icon: GraduationCap,
                  safeguards: [
                    "Xử lý trùng lặp theo claim/support thay vì tiết lộ tenant hiện có.",
                    "Tài liệu và dữ liệu nhạy cảm được kiểm soát bởi API upload riêng.",
                  ],
                  title: "Tạo không gian trường đại học",
                }),
              },
            ],
          },
        ],
      },
      {
        element: <RequireAccess requirement={candidateAccess} />,
        children: [
          {
            path: "candidate",
            element: <WorkspaceLayout area="candidate" />,
            children: [
              {
                index: true,
                element: screen({
                  apiScope: "API-WRK-018, API-WRK-020, API-WRK-024 và API-WRK-028",
                  area: "candidate",
                  description:
                    "Tổng quan tập hợp mức độ hoàn thiện hồ sơ, việc làm gợi ý, đơn ứng tuyển, phỏng vấn và lời mời bằng các widget độc lập.",
                  icon: LayoutDashboard,
                  nextStep: { label: "Hoàn thiện hồ sơ", to: "/candidate/profile" },
                  safeguards: [
                    "Mỗi widget có loading, empty và lỗi riêng; không dùng empty thay cho lỗi quyền.",
                    "Chỉ dữ liệu được API cho phép mới xuất hiện trong cache bộ nhớ.",
                  ],
                  title: "Tổng quan ứng viên",
                }),
              },
              {
                path: "profile",
                element: screen({
                  apiScope: "API-WRK-005, API-WRK-006 và API-WRK-004",
                  area: "candidate",
                  description:
                    "Hồ sơ nghề nghiệp sẽ hỗ trợ thông tin cơ bản, kỹ năng, học vấn và kinh nghiệm theo các ID ổn định.",
                  icon: CircleUserRound,
                  safeguards: [
                    "Các cập nhật nhạy cảm dùng If-Match và hiển thị state conflict thay vì tự ghi đè.",
                    "Lỗi field-level từ meta.fieldErrors là nguồn kết quả cuối cùng.",
                  ],
                  title: "Hồ sơ nghề nghiệp",
                }),
              },
              {
                path: "privacy",
                element: screen({
                  apiScope: "API-WRK-007",
                  area: "candidate",
                  description:
                    "Quyền riêng tư và searchable consent được quản lý riêng với trạng thái private mặc định.",
                  icon: ShieldCheck,
                  safeguards: [
                    "Contact, CV và Study evidence không được đưa vào public search fields.",
                    "Rút consent có hiệu lực ngay tại API; giao diện không tự suy diễn trạng thái index.",
                  ],
                  title: "Quyền riêng tư & hiển thị hồ sơ",
                }),
              },
              {
                path: "cvs",
                element: screen({
                  apiScope: "API-WRK-008 đến API-WRK-013",
                  area: "candidate",
                  description:
                    "Khu vực CV sẽ quản lý danh sách CV, draft revision, publish, export và lựa chọn CV mặc định.",
                  icon: FileText,
                  nextStep: { label: "Mở CV", to: "/candidate/cvs/new" },
                  safeguards: [
                    "Nội dung CV và AI draft không được ghi vào localStorage hoặc analytics.",
                    "Publish tạo revision bất biến; export kiểm entitlement do server quyết định.",
                  ],
                  title: "CV của bạn",
                }),
              },
              {
                path: "cvs/:cvId",
                element: screen({
                  apiScope: "API-WRK-010 đến API-WRK-013",
                  area: "candidate",
                  description:
                    "Trình soạn CV sẽ làm việc với typed sections, revision hiện hành và cơ chế autosave có optimistic concurrency.",
                  icon: FileText,
                  safeguards: [
                    "AI output luôn là nội dung chưa tin cậy cần người dùng xem, sửa và lưu riêng.",
                    "Conflict 412 mở trạng thái reload/so sánh thay vì ghi đè âm thầm.",
                  ],
                  title: "Soạn CV",
                }),
              },
              {
                path: "portfolio",
                element: screen({
                  apiScope: "API-WRK-014 đến API-WRK-017",
                  area: "candidate",
                  description:
                    "Portfolio quản lý link/file, mô tả, visibility và thứ tự hiển thị mà không làm thay đổi snapshot đã nộp.",
                  icon: FileText,
                  safeguards: [
                    "Link chỉ được kiểm tra HTTPS; server không fetch preview tùy ý.",
                    "File chỉ hiển thị sau khi có trạng thái CLEAN.",
                  ],
                  title: "Portfolio",
                }),
              },
              {
                path: "discover",
                element: screen({
                  apiScope: "API-WRK-018, API-WRK-019 và API-PAY-012/013",
                  area: "candidate",
                  description:
                    "Việc làm gợi ý, việc đã lưu và sponsored slots sẽ được tách rõ để ứng viên hiểu vì sao một công việc xuất hiện.",
                  icon: Search,
                  safeguards: [
                    "Lý do gợi ý chỉ dùng các tiêu chí được phép, không dùng đặc tính nhạy cảm.",
                    "Tin đã đóng vẫn giữ trong saved history với trạng thái do API trả về.",
                  ],
                  title: "Khám phá việc làm",
                }),
              },
              {
                path: "invitations",
                element: screen({
                  apiScope: "API-WRK-020 và API-WRK-021",
                  area: "candidate",
                  description:
                    "Lời mời hiển thị công việc, tenant, hạn phản hồi và lựa chọn chấp nhận hoặc từ chối rõ ràng.",
                  icon: Mail,
                  safeguards: [
                    "Chấp nhận chỉ mở luồng ứng tuyển; không tự tạo application hoặc chat.",
                    "Trạng thái hết hạn, trùng lặp hay transition lỗi sẽ reload từ API.",
                  ],
                  title: "Lời mời từ doanh nghiệp",
                }),
              },
              {
                path: "applications",
                element: screen({
                  apiScope: "API-WRK-024",
                  area: "candidate",
                  description:
                    "Danh sách đơn ứng tuyển dùng trạng thái canonical, bộ lọc theo URL và lưu cả lịch sử terminal.",
                  icon: ClipboardList,
                  safeguards: [
                    "Không có thao tác xóa để tránh thay đổi lịch sử ứng tuyển.",
                    "Phân biệt empty result do filter với empty result của tài khoản mới.",
                  ],
                  title: "Đơn ứng tuyển",
                }),
              },
              {
                path: "applications/:applicationId",
                element: screen({
                  apiScope: "API-WRK-025 đến API-WRK-027",
                  area: "candidate",
                  description:
                    "Chi tiết đơn sẽ hiển thị snapshot đã nộp, lịch sử ATS an toàn, trạng thái evidence và các action hợp lệ.",
                  icon: ClipboardList,
                  safeguards: [
                    "Evidence PENDING/UNAVAILABLE/REVOKED không phải tín hiệu đánh giá tiêu cực.",
                    "Rút đơn và rút consent luôn hiển thị hậu quả trước khi xác nhận.",
                  ],
                  title: "Chi tiết đơn ứng tuyển",
                }),
              },
              {
                path: "applications/:applicationId/chat",
                element: screen({
                  apiScope: "API-WRK-031 đến API-WRK-034",
                  area: "candidate",
                  description:
                    "Chat dùng lịch sử REST làm nguồn chính, sau đó mới subscribe realtime với event sequence và recovery khi có gap.",
                  icon: UsersRound,
                  safeguards: [
                    "Tin nhắn plain text; nội dung chat không vào analytics.",
                    "Trạng thái terminal là read-only và optimistic send dùng client message ID.",
                  ],
                  title: "Trao đổi về đơn ứng tuyển",
                }),
              },
              {
                path: "interviews",
                element: screen({
                  apiScope: "API-WRK-028 đến API-WRK-030",
                  area: "candidate",
                  description:
                    "Lịch phỏng vấn sẽ hiển thị timezone người dùng, phiên bản lịch hiện tại và các response hợp lệ.",
                  icon: ClipboardList,
                  safeguards: [
                    "Conflict lịch cũ yêu cầu tải lại trước khi phản hồi.",
                    "Link ICS dùng một lần và không lộ dữ liệu nội bộ.",
                  ],
                  title: "Lịch phỏng vấn",
                }),
              },
              {
                path: "interviews/:interviewId",
                element: screen({
                  apiScope: "API-WRK-028 đến API-WRK-030",
                  area: "candidate",
                  description:
                    "Chi tiết phỏng vấn sử dụng schedule version hiện tại, thời gian local/UTC và trạng thái response do server trả về.",
                  icon: ClipboardList,
                  safeguards: [
                    "Reschedule hoặc decline luôn kiểm tra version hiện hành trước khi gửi.",
                    "ICS và thông tin lịch chỉ được cấp trong scope ứng viên tham gia.",
                  ],
                  title: "Chi tiết phỏng vấn",
                }),
              },
              {
                path: "topcv-billing",
                element: screen({
                  apiScope: "API-PAY-001 đến API-PAY-006",
                  area: "candidate",
                  description:
                    "Thanh toán CV premium, export và AI usage hiển thị giá VND, entitlement và trạng thái order do server xác nhận.",
                  icon: CreditCard,
                  safeguards: [
                    "Không auto-renew hoặc lưu thẻ trong Work.",
                    "Provider redirect không được xem là giao dịch đã settle.",
                  ],
                  title: "Thanh toán & TopCV",
                }),
              },
              {
                path: "university-affiliations",
                element: screen({
                  apiScope: "API-UNI-006 và API-UNI-007",
                  area: "candidate",
                  description:
                    "Ứng viên xem và phản hồi lời mời liên kết trường đại học với mục đích, scope và hạn consent rõ ràng.",
                  icon: GraduationCap,
                  safeguards: [
                    "Consent mặc định từ chối và withdrawal có hiệu lực ngay.",
                    "Không có hành vi tạo application chỉ vì liên kết trường.",
                  ],
                  title: "Liên kết trường đại học",
                }),
              },
            ],
          },
        ],
      },
      {
        element: <RequireAccess requirement={enterpriseAccess} />,
        children: [
          {
            path: "enterprise/:enterpriseId",
            element: <WorkspaceLayout area="enterprise" />,
            children: [
              {
                index: true,
                element: screen({
                  apiScope: "API-WRK-036, API-WRK-042, API-WRK-054 và API-PAY-005",
                  area: "enterprise",
                  description:
                    "Tổng quan doanh nghiệp tập hợp verification, usage, jobs, ATS và interviews theo permission của thành viên.",
                  icon: LayoutDashboard,
                  nextStep: { label: "Quản lý tin tuyển dụng", to: "jobs" },
                  safeguards: [
                    "Widget tôn trọng permission từng phần và nêu thời điểm freshness.",
                    "Tenant switch phải xóa query cache, socket subscription và draft nhạy cảm.",
                  ],
                  title: "Tổng quan doanh nghiệp",
                }),
              },
              {
                path: "settings",
                element: screen({
                  apiScope: "API-WRK-037 đến API-WRK-041",
                  area: "enterprise",
                  description:
                    "Cài đặt doanh nghiệp quản lý public/legal profile, xác minh, thành viên và role theo membership version.",
                  icon: Settings,
                  safeguards: [
                    "Không thể xóa owner cuối cùng hoặc tự nâng quyền bằng giao diện.",
                    "Legal change sau verified bắt đầu quy trình re-verification.",
                  ],
                  title: "Cài đặt doanh nghiệp",
                }),
              },
              {
                path: "jobs",
                element: screen({
                  apiScope: "API-WRK-042 và API-WRK-048 đến API-WRK-050",
                  area: "enterprise",
                  description:
                    "Danh sách job quản lý lifecycle, filter và các CTA phù hợp với trạng thái công việc.",
                  icon: BriefcaseBusiness,
                  nextStep: { label: "Soạn job mới", to: "../jobs/new/edit" },
                  safeguards: [
                    "Pause/close đồng bộ trạng thái public theo server, không xóa ứng tuyển hiện có.",
                    "Không mở lại job terminal bằng thao tác client.",
                  ],
                  title: "Tin tuyển dụng",
                }),
              },
              {
                path: "jobs/:jobId/edit",
                element: screen({
                  apiScope: "API-WRK-043 đến API-WRK-045",
                  area: "enterprise",
                  description:
                    "Trình soạn JD làm việc theo revision, field validation, skill/salary/location và autosave có If-Match.",
                  icon: FileText,
                  safeguards: [
                    "Job đã publish luôn mở DRAFT revision mới.",
                    "AI JD draft phải được người dùng accept/edit rồi lưu một lần riêng.",
                  ],
                  title: "Soạn tin tuyển dụng",
                }),
              },
              {
                path: "jobs/:jobId/publish",
                element: screen({
                  apiScope: "API-WRK-046 và API-WRK-047",
                  area: "enterprise",
                  description:
                    "Bước publish kiểm tra completeness, policy, rights, entitlement và trusted grant trước khi gửi review/publish.",
                  icon: ShieldCheck,
                  safeguards: [
                    "Server là nguồn cuối cho permission/MFA/revision và trạng thái xuất bản.",
                    "Checklist lỗi luôn liên kết về đúng field của bản nháp.",
                  ],
                  title: "Review & publish tin tuyển dụng",
                }),
              },
              {
                path: "talent/search",
                element: screen({
                  apiScope: "API-WRK-051 và API-PAY-012/013",
                  area: "enterprise",
                  description:
                    "Candidate search chỉ dùng redacted public projection của ứng viên đã opt-in và entitlement hợp lệ.",
                  icon: Search,
                  safeguards: [
                    "Không hiển thị contact, CV hoặc Study evidence trong search result.",
                    "Mọi truy vấn/search result cần được audit ở backend.",
                  ],
                  title: "Tìm ứng viên",
                }),
              },
              {
                path: "talent/:candidatePublicId",
                element: screen({
                  apiScope: "API-WRK-052 và API-WRK-053",
                  area: "enterprise",
                  description:
                    "Hồ sơ public của ứng viên hiển thị projection đã redaction và matching reason có thể giải thích.",
                  icon: CircleUserRound,
                  safeguards: [
                    "Consent được kiểm lại ở cả màn hình mở và action invite.",
                    "Invite không tạo conversation hoặc application.",
                  ],
                  title: "Hồ sơ ứng viên công khai",
                }),
              },
              {
                path: "talent/invitations",
                element: screen({
                  apiScope: "API-WRK-053",
                  area: "enterprise",
                  description:
                    "Danh sách lời mời theo job, status và expiry cho phép theo dõi nguồn talent outreach một cách có kiểm soát.",
                  icon: UsersRound,
                  safeguards: [
                    "Không có CTA nhắn tin trực tiếp từ lời mời.",
                    "Trạng thái entitlement và invitation do API trả về, không tự suy diễn.",
                  ],
                  title: "Lời mời ứng viên",
                }),
              },
              {
                path: "ats",
                element: screen({
                  apiScope: "API-WRK-054 và API-WRK-058",
                  area: "enterprise",
                  description:
                    "ATS hỗ trợ cả list và board có alternative keyboard; thay đổi stage luôn có confirmation và version hiện tại.",
                  icon: ClipboardList,
                  safeguards: [
                    "AI shortlist chỉ gợi ý hoặc highlight, không tự chuyển trạng thái ứng viên.",
                    "Transition decision cần actor/reason/artifact theo policy server.",
                  ],
                  title: "ATS & tuyển dụng",
                }),
              },
              {
                path: "applications/:applicationId",
                element: screen({
                  apiScope: "API-WRK-055 đến API-WRK-059",
                  area: "enterprise",
                  description:
                    "Chi tiết hồ sơ ứng tuyển sử dụng immutable snapshots, permission theo assignment và các trạng thái evidence rõ ràng.",
                  icon: ClipboardList,
                  safeguards: [
                    "Evidence PENDING/UNAVAILABLE không được dùng làm tín hiệu từ chối.",
                    "Truy cập PII, evidence và quyết định đều được backend audit.",
                  ],
                  title: "Hồ sơ ứng tuyển",
                }),
              },
              {
                path: "applications/:applicationId/chat",
                element: screen({
                  apiScope: "API-WRK-031 đến API-WRK-034",
                  area: "enterprise",
                  description:
                    "Chat tuyển dụng dùng lịch sử REST, realtime recovery và kiểm tra assignment của recruiter ở mọi request/send/subscribe.",
                  icon: UsersRound,
                  safeguards: [
                    "Removed recruiter mất quyền truy cập ngay khi server xác nhận membership/assignment mới.",
                    "Conversation terminal là read-only; nội dung tin nhắn không được gửi vào analytics.",
                  ],
                  title: "Trao đổi với ứng viên",
                }),
              },
              {
                path: "interviews/:interviewId",
                element: screen({
                  apiScope: "API-WRK-060 đến API-WRK-062",
                  area: "enterprise",
                  description:
                    "Màn hình phỏng vấn dùng schedule version hiện tại, timezone rõ ràng và action reschedule/cancel/no-show theo permission.",
                  icon: ClipboardList,
                  safeguards: [
                    "Không lộ participant hoặc calendar data nội bộ ra ngoài scope.",
                    "Reschedule tạo version mới và reset candidate confirmation.",
                  ],
                  title: "Điều phối phỏng vấn",
                }),
              },
              {
                path: "billing-topjd",
                element: screen({
                  apiScope: "API-PAY-001 đến API-PAY-013",
                  area: "enterprise",
                  description:
                    "Billing doanh nghiệp quản lý sản phẩm, order, credits, invoice và partnership request theo billing permission.",
                  icon: CreditCard,
                  safeguards: [
                    "Giá và settlement luôn do server/provider xác nhận.",
                    "Promotion chỉ hợp lệ cho published job và cần nhãn tài trợ rõ ràng.",
                  ],
                  title: "Thanh toán & TopJD",
                }),
              },
              {
                path: "billing/return/:provider",
                element: screen({
                  apiScope: "API-PAY-003 và API-PAY-016",
                  area: "enterprise",
                  description:
                    "Trang return chỉ hiển thị trạng thái order được API xác thực sau callback của provider.",
                  icon: CreditCard,
                  safeguards: [
                    "URL return không thể tự settle giao dịch.",
                    "Membership được kiểm lại trước khi hiển thị bất kỳ dữ liệu order nào.",
                  ],
                  title: "Kết quả thanh toán",
                }),
              },
            ],
          },
        ],
      },
      {
        element: <RequireAccess requirement={universityAccess} />,
        children: [
          {
            path: "university/:universityId",
            element: <WorkspaceLayout area="university" />,
            children: [
              {
                index: true,
                element: screen({
                  apiScope: "API-UNI-008 đến API-UNI-016",
                  area: "university",
                  description:
                    "Tổng quan trường đại học tổ chức verification, thành viên, affiliations, partnership, campus jobs và báo cáo aggregate.",
                  icon: LayoutDashboard,
                  nextStep: { label: "Xem xác minh", to: "verification" },
                  safeguards: [
                    "Dữ liệu mức cá nhân chỉ có khi consent còn hiệu lực và đúng mục đích.",
                    "Report aggregate không hiển thị cohort nhỏ hơn ngưỡng bảo vệ.",
                  ],
                  title: "Tổng quan trường đại học",
                }),
              },
              {
                path: "verification",
                element: screen({
                  apiScope: "API-UNI-002",
                  area: "university",
                  description:
                    "Xác minh trường hiển thị legal snapshot, CLEAN documents, consent và checklist theo verification state.",
                  icon: ShieldCheck,
                  safeguards: [
                    "Tài liệu nhạy cảm dùng signed access và không cache preview lâu dài.",
                    "Pending state khóa hành vi gửi mới cho đến khi API cho phép.",
                  ],
                  title: "Xác minh trường đại học",
                }),
              },
              {
                path: "members",
                element: screen({
                  apiScope: "API-UNI-003 và API-UNI-004",
                  area: "university",
                  description:
                    "Quản lý thành viên và invite trường đại học theo role, seat và tenant membership hiện hành.",
                  icon: UsersRound,
                  safeguards: [
                    "Không bỏ owner cuối cùng hoặc hành động vượt quyền ở client.",
                    "Lỗi cross-tenant hiển thị generic để bảo vệ thông tin scope.",
                  ],
                  title: "Thành viên trường đại học",
                }),
              },
              {
                path: "affiliations",
                element: screen({
                  apiScope: "API-UNI-005 và API-UNI-016",
                  area: "university",
                  description:
                    "Affiliations hỗ trợ lời mời theo batch, trạng thái liên kết và export redacted khi được cấp quyền.",
                  icon: GraduationCap,
                  safeguards: [
                    "Không có affiliation active trước khi learner chấp nhận consent.",
                    "Không đọc CV, chat hoặc Study evidence qua màn hình này.",
                  ],
                  title: "Liên kết học viên",
                }),
              },
              {
                path: "partnerships",
                element: screen({
                  apiScope: "API-UNI-013",
                  area: "university",
                  description:
                    "Partnership với doanh nghiệp dùng request state rõ ràng, scope đồng ý và mốc thời gian có kiểm soát.",
                  icon: Building2,
                  safeguards: [
                    "Không có chia sẻ dữ liệu ngầm khi partnership được đề xuất.",
                    "Mọi response cần permission riêng và được audit ở backend.",
                  ],
                  title: "Đối tác doanh nghiệp",
                }),
              },
              {
                path: "reports",
                element: screen({
                  apiScope: "API-UNI-014 đến API-UNI-016",
                  area: "university",
                  description:
                    "Reporting hiển thị aggregate outcomes, freshness và async export theo policy cohort threshold.",
                  icon: BarChart3,
                  safeguards: [
                    "Biểu đồ luôn có bảng dữ liệu tương đương cho accessibility.",
                    "Export được tạo bất đồng bộ và chỉ dùng signed URL thời hạn ngắn.",
                  ],
                  title: "Báo cáo kết quả",
                }),
              },
            ],
          },
        ],
      },
      {
        element: <RequireAccess requirement={{ authenticated: true, requireFreshMfa: true, roles: ["OPS"] }} />,
        children: [
          {
            path: "ops",
            element: <WorkspaceLayout area="ops" />,
            children: [
              {
                index: true,
                element: screen({
                  apiScope: "API-OPS-001 đến API-OPS-009",
                  area: "ops",
                  description:
                    "Không gian vận hành Work tập hợp health, queue, moderation, tenant risk và audit workflows cho nhân sự được cấp quyền.",
                  icon: LayoutDashboard,
                  safeguards: [
                    "MFA freshness được kiểm trước khi mở route đặc quyền.",
                    "Tất cả thao tác vận hành có audit trail do backend ghi nhận.",
                  ],
                  title: "Tổng quan vận hành",
                }),
              },
              {
                path: "users",
                element: screen({
                  apiScope: "API-OPS-001 và API-OPS-002",
                  area: "ops",
                  description:
                    "Quản lý người dùng vận hành theo quyền giới hạn, account state và quy trình review cần lý do rõ ràng.",
                  icon: UsersRound,
                  safeguards: [
                    "Không lộ dữ liệu ngoài resource scope của operator.",
                    "Action nhạy cảm cần step-up và audit backend.",
                  ],
                  title: "Vận hành người dùng",
                }),
              },
              {
                path: "jobs",
                element: screen({
                  apiScope: "API-OPS-003 và API-OPS-004",
                  area: "ops",
                  description:
                    "Moderation job và workflow review làm việc với trạng thái server-authoritative và lý do quyết định.",
                  icon: BriefcaseBusiness,
                  safeguards: [
                    "Không thay đổi published revision bằng dữ liệu client cũ.",
                    "Decision và evidence review tạo audit record bất biến.",
                  ],
                  title: "Kiểm duyệt việc làm",
                }),
              },
              {
                path: "tenants",
                element: screen({
                  apiScope: "API-OPS-005 và API-OPS-006",
                  area: "ops",
                  description:
                    "Tenant operations hỗ trợ trạng thái xác minh, risk và intervention theo permission và break-glass policy.",
                  icon: Building2,
                  safeguards: [
                    "Không lộ tenant details ngoài quyền vận hành hiện tại.",
                    "State transition yêu cầu lý do và actor có thể audit.",
                  ],
                  title: "Vận hành tenant",
                }),
              },
              {
                path: "audit",
                element: screen({
                  apiScope: "API-OPS-007 và API-OPS-008",
                  area: "ops",
                  description:
                    "Audit log và export dùng bộ lọc có policy, phạm vi rõ ràng và background job được server kiểm tra.",
                  icon: ClipboardList,
                  safeguards: [
                    "Export không được tạo chỉ từ URL hoặc state client.",
                    "Dữ liệu nhạy cảm có retention và watermark theo policy.",
                  ],
                  title: "Audit & xuất dữ liệu",
                }),
              },
              {
                path: "settings",
                element: screen({
                  apiScope: "API-OPS-009",
                  area: "ops",
                  description:
                    "Cài đặt vận hành và break-glass luôn hiển thị scope, thời hạn và yêu cầu phê duyệt tương ứng.",
                  icon: ShieldCheck,
                  safeguards: [
                    "Break-glass chỉ là elevated session có thời hạn, không biến thành role mutation.",
                    "SEV-1 exception vẫn tạo security alert và full audit trail.",
                  ],
                  title: "Cài đặt vận hành",
                }),
              },
            ],
          },
        ],
      },
      {
        path: "*",
        element: <NotFoundPage />,
      },
    ],
  },
]);
