import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import type { Cv, DoanhNghiep, JD, PrismaClient, SinhVien } from "@prisma/client";

const STUDENT_PASSWORD = "WorkStudent@123";
const BUSINESS_PASSWORD = "WorkBusiness@123";
const STUDENT_EMAIL_PREFIX = "seed.student.";
const BUSINESS_EMAIL_PREFIX = "seed.business.";
const SEED_VERSION = "work-accounts-v1";

type IndustryProfile = {
  name: string;
  companyName: string;
  address: string;
  phone: string;
  description: string;
  recruitingFocus: string;
  department: string;
  domain: string;
  skills: string;
  education: string;
  priority: string;
  salary: string;
  environment: string;
  certificate: string;
  club: string;
  jobTitles: readonly string[];
};

type StudentSeed = {
  serial: number;
  account: {
    hoten: string;
    email: string;
    matkhau: string;
    chuyennganh: string;
    avt: null;
  };
  cv: {
    avt: null;
    hoten: string;
    ngaysinh: Date;
    gioitinh: string;
    email: string;
    sdt: string;
    diachi: string;
    vitri: string;
    nganh: string;
    muctieunghiep: string;
    hocvan: string;
    kinhnghiem: string;
    kynang: string;
    ngoaingu: string;
    chungchi: string;
    duan: string;
    giaithuong: string;
    hoatdong: string;
    social: Record<string, string>;
    portfolio: string;
    luongmongmuon: string;
  };
};

type JobSeed = {
  ten_vi_tri: string;
  phong_ban: string;
  cap_bac: string;
  bao_cao_cho: string;
  nhiem_vu: string;
  trinh_do: string;
  kinh_nghiem: string;
  ky_nang: string;
  ky_nang_mem: string;
  uu_tien: string;
  muc_luong: string;
  phuc_loi: string;
  moi_truong: string;
  dia_diem: string;
  thoi_gian: string;
  han_nop: string;
  cach_ung_tuyen: string;
  mo_ta: string;
  ten_cong_ty: string;
  nganh: string;
  avt: null;
};

const INDUSTRIES: readonly IndustryProfile[] = [
  {
    name: "Công nghệ thông tin",
    companyName: "Công ty TNHH Sao Khuê Digital",
    address: "Đà Nẵng, Việt Nam",
    phone: "02363880001",
    description: "Doanh nghiệp phát triển nền tảng số và sản phẩm phần mềm cho thị trường Việt Nam.",
    recruitingFocus: "Xây dựng sản phẩm web, dữ liệu và trải nghiệm số.",
    department: "Sản phẩm & Kỹ thuật",
    domain: "nền tảng số",
    skills: "React, TypeScript, Node.js, SQL",
    education: "Đại học chuyên ngành CNTT hoặc tương đương",
    priority: "Có GitHub hoặc portfolio sản phẩm",
    salary: "15-30 triệu VNĐ/tháng",
    environment: "Agile, mentoring và làm việc hybrid",
    certificate: "AWS Cloud Practitioner hoặc chứng chỉ tương đương",
    club: "Lập trình và Công nghệ",
    jobTitles: [
      "Frontend React Developer",
      "Backend Node.js Developer",
      "QA Automation Engineer",
      "Product Designer",
    ],
  },
  {
    name: "Tài chính - Ngân hàng",
    companyName: "Việt Tín Finance",
    address: "Hà Nội, Việt Nam",
    phone: "02438800002",
    description: "Công ty công nghệ tài chính tập trung vào thanh toán số và phân tích dữ liệu tín dụng.",
    recruitingFocus: "Phát triển dịch vụ tài chính an toàn, minh bạch và dễ tiếp cận.",
    department: "Phân tích & Vận hành",
    domain: "dịch vụ tài chính số",
    skills: "Excel, SQL, Python, phân tích dữ liệu",
    education: "Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT",
    priority: "Tư duy định lượng và cẩn trọng với dữ liệu",
    salary: "12-25 triệu VNĐ/tháng",
    environment: "Quy trình rõ ràng, phối hợp liên phòng ban",
    certificate: "CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu",
    club: "Tài chính và Phân tích",
    jobTitles: [
      "Chuyên viên Phân tích Tài chính",
      "Banking Integration Developer",
      "Data Analyst",
      "Risk & Compliance Specialist",
    ],
  },
  {
    name: "Marketing - Truyền thông",
    companyName: "Mộc Miên Media",
    address: "TP. Hồ Chí Minh, Việt Nam",
    phone: "02838800003",
    description: "Agency truyền thông tích hợp cung cấp chiến lược thương hiệu, nội dung và quảng cáo số.",
    recruitingFocus: "Tạo chiến dịch có câu chuyện rõ ràng và đo lường được hiệu quả.",
    department: "Marketing & Sáng tạo",
    domain: "chiến dịch thương hiệu",
    skills: "Content, SEO, Meta Ads, Google Analytics",
    education: "Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ",
    priority: "Có portfolio nội dung hoặc chiến dịch thực tế",
    salary: "10-22 triệu VNĐ/tháng",
    environment: "Sáng tạo, phản hồi nhanh và tôn trọng ý tưởng",
    certificate: "Google Analytics hoặc Meta Blueprint",
    club: "Truyền thông và Sự kiện",
    jobTitles: [
      "Content Marketing Executive",
      "Performance Marketing Specialist",
      "Social Media Planner",
      "Account Executive",
    ],
  },
  {
    name: "Thương mại điện tử",
    companyName: "Chợ Việt Commerce",
    address: "Hải Phòng, Việt Nam",
    phone: "02253880004",
    description: "Nền tảng thương mại điện tử kết nối thương hiệu địa phương với người tiêu dùng trên toàn quốc.",
    recruitingFocus: "Tối ưu vận hành sàn, trải nghiệm mua sắm và tăng trưởng khách hàng.",
    department: "Vận hành & Tăng trưởng",
    domain: "sàn thương mại điện tử",
    skills: "E-commerce, SQL, Figma, phân tích funnel",
    education: "Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế",
    priority: "Hiểu hành vi người dùng và quy trình bán hàng online",
    salary: "11-24 triệu VNĐ/tháng",
    environment: "Nhanh, thực tế và định hướng theo dữ liệu",
    certificate: "Google Analytics hoặc chứng chỉ Product Analytics",
    club: "Kinh doanh và Khởi nghiệp",
    jobTitles: [
      "E-commerce Operations Specialist",
      "Product Owner E-commerce",
      "UI/UX Designer",
      "Customer Growth Analyst",
    ],
  },
  {
    name: "Giáo dục",
    companyName: "Học Mở Education",
    address: "Cần Thơ, Việt Nam",
    phone: "02923880005",
    description: "Đơn vị giáo dục số phát triển nội dung học tập và dịch vụ hỗ trợ người học suốt đời.",
    recruitingFocus: "Cải thiện chất lượng học tập và trải nghiệm của học viên.",
    department: "Học thuật & Sản phẩm",
    domain: "giáo dục số",
    skills: "Instructional Design, LMS, giao tiếp, Excel",
    education: "Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT",
    priority: "Yêu thích giáo dục và có tư duy lấy người học làm trung tâm",
    salary: "9-20 triệu VNĐ/tháng",
    environment: "Nhân văn, học hỏi liên tục và hợp tác đa chuyên môn",
    certificate: "Google Educator hoặc chứng chỉ đào tạo trực tuyến",
    club: "Giáo dục và Cộng đồng",
    jobTitles: [
      "Academic Advisor",
      "Instructional Designer",
      "Full-stack Developer EdTech",
      "Student Success Specialist",
    ],
  },
  {
    name: "Logistics",
    companyName: "Đông Hải Logistics",
    address: "Bình Dương, Việt Nam",
    phone: "02743880006",
    description: "Doanh nghiệp logistics cung cấp giải pháp vận chuyển, kho bãi và theo dõi chuỗi cung ứng.",
    recruitingFocus: "Tăng khả năng quan sát, tối ưu chi phí và nâng độ tin cậy giao hàng.",
    department: "Chuỗi cung ứng & Vận hành",
    domain: "chuỗi cung ứng",
    skills: "Supply Chain, Excel, SQL, quản lý vận hành",
    education: "Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật",
    priority: "Có tư duy quy trình và sẵn sàng làm việc với dữ liệu vận hành",
    salary: "10-23 triệu VNĐ/tháng",
    environment: "Kỷ luật, phối hợp thực địa và cải tiến liên tục",
    certificate: "CSCP, Excel nâng cao hoặc chứng chỉ logistics",
    club: "Logistics và Quản trị",
    jobTitles: [
      "Supply Chain Analyst",
      "Logistics Operations Coordinator",
      "Fleet Technology Product Specialist",
      "Warehouse Process Engineer",
    ],
  },
  {
    name: "Sản xuất",
    companyName: "Việt Thành Manufacturing",
    address: "Đồng Nai, Việt Nam",
    phone: "02513880007",
    description: "Nhà sản xuất công nghiệp chú trọng chất lượng, an toàn và tự động hóa dây chuyền.",
    recruitingFocus: "Chuẩn hóa quy trình và nâng hiệu suất nhà máy bằng công nghệ.",
    department: "Kỹ thuật & Chất lượng",
    domain: "sản xuất công nghiệp",
    skills: "Lean, AutoCAD, Excel, kiểm soát chất lượng",
    education: "Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp",
    priority: "Có tư duy cải tiến và tuân thủ an toàn lao động",
    salary: "12-26 triệu VNĐ/tháng",
    environment: "Thực tế, an toàn và hướng tới cải tiến đo lường được",
    certificate: "Lean Six Sigma hoặc chứng chỉ quản lý chất lượng",
    club: "Kỹ thuật và Sáng tạo",
    jobTitles: [
      "Production Planning Engineer",
      "Quality Assurance Engineer",
      "Industrial Automation Engineer",
      "Procurement Specialist",
    ],
  },
  {
    name: "Y tế - Chăm sóc sức khỏe",
    companyName: "An Tâm HealthTech",
    address: "Huế, Việt Nam",
    phone: "02343880008",
    description: "Công ty healthtech xây dựng giải pháp quản lý dịch vụ và dữ liệu chăm sóc sức khỏe.",
    recruitingFocus: "Ứng dụng công nghệ có trách nhiệm để hỗ trợ nhân viên y tế và bệnh nhân.",
    department: "Sản phẩm & Dữ liệu Y tế",
    domain: "chăm sóc sức khỏe số",
    skills: "SQL, phân tích dữ liệu, quy trình y tế, giao tiếp",
    education: "Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh",
    priority: "Tôn trọng bảo mật dữ liệu và trải nghiệm bệnh nhân",
    salary: "11-25 triệu VNĐ/tháng",
    environment: "Cẩn trọng, nhân văn và phối hợp với chuyên gia y tế",
    certificate: "Health Informatics hoặc chứng chỉ phân tích dữ liệu",
    club: "Sức khỏe và Công nghệ",
    jobTitles: [
      "Healthcare Product Specialist",
      "Clinical Data Analyst",
      "Backend Engineer",
      "Customer Care Supervisor",
    ],
  },
  {
    name: "Du lịch - Khách sạn",
    companyName: "Lữ Hành Việt Hospitality",
    address: "Nha Trang, Việt Nam",
    phone: "02583880009",
    description: "Thương hiệu du lịch và lưu trú phát triển trải nghiệm địa phương cho khách trong nước và quốc tế.",
    recruitingFocus: "Mang đến dịch vụ thân thiện, nhất quán và giàu bản sắc địa phương.",
    department: "Kinh doanh & Dịch vụ",
    domain: "du lịch và lưu trú",
    skills: "Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel",
    education: "Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ",
    priority: "Giao tiếp tốt, chủ động và yêu thích dịch vụ khách hàng",
    salary: "8-18 triệu VNĐ/tháng",
    environment: "Thân thiện, đa văn hóa và chú trọng trải nghiệm khách hàng",
    certificate: "IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch",
    club: "Du lịch và Ngoại ngữ",
    jobTitles: [
      "Travel Consultant",
      "Hotel Operations Executive",
      "Digital Marketing Executive",
      "Front Office Supervisor",
    ],
  },
  {
    name: "Năng lượng xanh",
    companyName: "Green Horizon Energy",
    address: "Quảng Ninh, Việt Nam",
    phone: "02033880010",
    description: "Doanh nghiệp năng lượng tái tạo triển khai giải pháp điện mặt trời và quản lý phát thải.",
    recruitingFocus: "Thúc đẩy chuyển dịch năng lượng bằng dự án hiệu quả và bền vững.",
    department: "Dự án & Phát triển bền vững",
    domain: "năng lượng tái tạo",
    skills: "AutoCAD, Excel, IoT, phân tích phát thải",
    education: "Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế",
    priority: "Quan tâm đến phát triển bền vững và an toàn dự án",
    salary: "12-28 triệu VNĐ/tháng",
    environment: "Định hướng tác động, an toàn và làm việc liên ngành",
    certificate: "ISO 14001 hoặc chứng chỉ quản lý dự án",
    club: "Môi trường và Đổi mới",
    jobTitles: [
      "Solar Project Engineer",
      "Sustainability Analyst",
      "IoT Field Engineer",
      "Business Development Executive",
    ],
  },
];

const SURNAMES = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng"] as const;
const MIDDLE_NAMES = ["Minh", "Ngọc", "Gia", "Thanh", "Khánh", "Thu", "Đức", "Quỳnh", "Hải", "Bảo"] as const;
const GIVEN_NAMES = ["An", "Bình", "Chi", "Dũng", "Hà", "Khang", "Linh", "Nam", "Phương", "Quân"] as const;
const CITIES = [
  "Đà Nẵng",
  "Hà Nội",
  "TP. Hồ Chí Minh",
  "Hải Phòng",
  "Cần Thơ",
  "Bình Dương",
  "Đồng Nai",
  "Huế",
  "Nha Trang",
  "Quảng Ninh",
] as const;
const DEADLINES = ["30/11/2026", "15/12/2026", "31/12/2026", "15/01/2027"] as const;
const JOB_LEVELS = ["Junior", "Middle", "Junior", "Fresher"] as const;
const BENEFITS = "BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định";
const SOFT_SKILLS = "Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề";

function padded(value: number, width: number): string {
  return String(value).padStart(width, "0");
}

function buildStudentSeed(index: number): StudentSeed {
  const serial = index + 1;
  const industryIndex = Math.floor(index / 10);
  const memberIndex = index % 10;
  const profile = INDUSTRIES[industryIndex];
  const serialText = padded(serial, 3);
  const name = `${SURNAMES[industryIndex]} ${MIDDLE_NAMES[memberIndex]} ${GIVEN_NAMES[memberIndex]}`;
  const email = `${STUDENT_EMAIL_PREFIX}${serialText}@study2work.dev`;
  const role = profile.jobTitles[memberIndex % profile.jobTitles.length];
  const experience = [
    "Fresher; hoàn thành dự án học thuật và 6 tháng thực tập.",
    `1 năm kinh nghiệm liên quan đến ${profile.domain}.`,
    `2 năm kinh nghiệm thực tế trong lĩnh vực ${profile.domain}.`,
  ][memberIndex % 3];
  const language = ["Tiếng Anh B1", "Tiếng Anh B2", "Tiếng Anh giao tiếp"][memberIndex % 3];
  const phone = `090${String(3000000 + serial).padStart(7, "0")}`;

  return {
    serial,
    account: {
      hoten: name,
      email,
      matkhau: STUDENT_PASSWORD,
      chuyennganh: profile.name,
      avt: null,
    },
    cv: {
      avt: null,
      hoten: name,
      ngaysinh: new Date(Date.UTC(1998 + (memberIndex % 5), industryIndex, 5 + memberIndex)),
      gioitinh: memberIndex % 2 === 0 ? "Nam" : "Nữ",
      email,
      sdt: phone,
      diachi: `${CITIES[industryIndex]}, Việt Nam`,
      vitri: role,
      nganh: profile.name,
      muctieunghiep: `Phát triển sự nghiệp bền vững trong lĩnh vực ${profile.name} với vai trò ${role}.`,
      hocvan: profile.education,
      kinhnghiem: experience,
      kynang: profile.skills,
      ngoaingu: language,
      chungchi: profile.certificate,
      duan: `Dự án portfolio ${serialText}: xây dựng giải pháp thử nghiệm cho ${profile.domain}.`,
      giaithuong: memberIndex % 4 === 0 ? "Giải thưởng đồ án cấp khoa" : "Thành tích học tập và hoạt động câu lạc bộ",
      hoatdong: `CLB ${profile.club}; tình nguyện cộng đồng.`,
      social: {
        linkedin: `https://www.linkedin.com/in/seed-student-${serialText}`,
        github: `https://github.com/seed-student-${serialText}`,
      },
      portfolio: `https://portfolio.study2work.dev/student-${serialText}`,
      luongmongmuon: profile.salary,
    },
  };
}

function buildJobSeed(profile: IndustryProfile, jobIndex: number): JobSeed {
  const title = profile.jobTitles[jobIndex];
  const experience = jobIndex === 3
    ? "Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương"
    : "Từ 1 đến 3 năm kinh nghiệm liên quan";

  return {
    ten_vi_tri: title,
    phong_ban: profile.department,
    cap_bac: JOB_LEVELS[jobIndex],
    bao_cao_cho: `Trưởng bộ phận ${profile.department}`,
    nhiem_vu: `Phụ trách công việc ${title}; phối hợp với đội ngũ ${profile.department.toLowerCase()} để hoàn thành mục tiêu.`,
    trinh_do: profile.education,
    kinh_nghiem: experience,
    ky_nang: profile.skills,
    ky_nang_mem: SOFT_SKILLS,
    uu_tien: profile.priority,
    muc_luong: profile.salary,
    phuc_loi: BENEFITS,
    moi_truong: profile.environment,
    dia_diem: profile.address,
    thoi_gian: "Toàn thời gian",
    han_nop: DEADLINES[jobIndex],
    cach_ung_tuyen: "Nộp CV qua hệ thống Study2Work",
    mo_ta: `Tham gia phát triển ${profile.domain} cùng ${profile.companyName}, tạo ra kết quả có thể đo lường.`,
    ten_cong_ty: profile.companyName,
    nganh: profile.name,
    avt: null,
  };
}

function buildDataset() {
  const students = Array.from({ length: 100 }, (_, index) => buildStudentSeed(index));
  const businesses = INDUSTRIES.map((profile) => ({
    profile,
    account: {
      hoten: profile.companyName,
      email: `${BUSINESS_EMAIL_PREFIX}${padded(INDUSTRIES.indexOf(profile) + 1, 2)}@study2work.dev`,
      matkhau: BUSINESS_PASSWORD,
      diachi: profile.address,
      sodienthoai: profile.phone,
      avt: null,
    },
    jobs: profile.jobTitles.map((_, index) => buildJobSeed(profile, index)),
  }));

  return {
    students,
    businesses,
    industries: INDUSTRIES.map(({ name }) => name),
  };
}

function assertMaxLength(label: string, value: unknown, maxLength: number): void {
  if (typeof value === "string" && value.length > maxLength) {
    throw new Error(`${label} vượt giới hạn ${maxLength} ký tự: ${value.length}`);
  }
}

function validateDataset(dataset: ReturnType<typeof buildDataset>): void {
  if (dataset.students.length !== 100) throw new Error("Dataset phải có đúng 100 sinh viên.");
  if (dataset.businesses.length !== 10) throw new Error("Dataset phải có đúng 10 doanh nghiệp.");
  if (dataset.businesses.reduce((total, business) => total + business.jobs.length, 0) !== 40) {
    throw new Error("Dataset phải có đúng 40 JD.");
  }
  if (dataset.industries.length !== 10) throw new Error("Dataset phải có đúng 10 ngành nghề.");

  const studentEmails = new Set<string>();
  for (const student of dataset.students) {
    if (student.account.email !== student.cv.email) throw new Error(`Email CV không khớp sinh viên ${student.serial}.`);
    if (student.cv.hoten !== student.account.hoten) throw new Error(`Họ tên CV không khớp sinh viên ${student.serial}.`);
    if (studentEmails.has(student.account.email)) throw new Error(`Trùng email sinh viên ${student.account.email}.`);
    studentEmails.add(student.account.email);

    assertMaxLength(`SinhVien[${student.serial}].hoten`, student.account.hoten, 50);
    assertMaxLength(`SinhVien[${student.serial}].email`, student.account.email, 50);
    assertMaxLength(`SinhVien[${student.serial}].matkhau`, student.account.matkhau, 20);
    assertMaxLength(`SinhVien[${student.serial}].chuyennganh`, student.account.chuyennganh, 50);
    for (const [field, value] of Object.entries(student.cv)) assertMaxLength(`Cv[${student.serial}].${field}`, value, 191);
  }

  const businessEmails = new Set<string>();
  for (const [businessIndex, business] of dataset.businesses.entries()) {
    if (businessEmails.has(business.account.email)) throw new Error(`Trùng email doanh nghiệp ${business.account.email}.`);
    businessEmails.add(business.account.email);

    assertMaxLength(`DoanhNghiep[${businessIndex + 1}].hoten`, business.account.hoten, 50);
    assertMaxLength(`DoanhNghiep[${businessIndex + 1}].email`, business.account.email, 50);
    assertMaxLength(`DoanhNghiep[${businessIndex + 1}].matkhau`, business.account.matkhau, 50);
    assertMaxLength(`DoanhNghiep[${businessIndex + 1}].diachi`, business.account.diachi, 100);
    assertMaxLength(`DoanhNghiep[${businessIndex + 1}].sodienthoai`, business.account.sodienthoai, 20);

    const titles = new Set<string>();
    for (const [jobIndex, job] of business.jobs.entries()) {
      if (titles.has(job.ten_vi_tri)) throw new Error(`Trùng JD ${job.ten_vi_tri}.`);
      titles.add(job.ten_vi_tri);
      for (const [field, value] of Object.entries(job)) assertMaxLength(`JD[${businessIndex + 1}.${jobIndex + 1}].${field}`, value, 191);
    }
  }
}

function displayValue(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "bigint") return value.toString();
  if (value instanceof Date) return value.toISOString();
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function markdownValue(value: unknown): string {
  return displayValue(value)
    .replace(/\\/g, "\\\\")
    .replace(/\|/g, "\\|")
    .replace(/\r?\n/g, "<br>");
}

function renderDetails(rows: readonly [string, unknown][]): string[] {
  return [
    "| Trường | Giá trị |",
    "| --- | --- |",
    ...rows.map(([label, value]) => `| ${markdownValue(label)} | ${markdownValue(value)} |`),
  ];
}

function renderStudentCv(cv: Cv): string[] {
  return renderDetails([
    ["ID CV", cv.id],
    ["Họ tên", cv.hoten],
    ["Ngày sinh", cv.ngaysinh],
    ["Giới tính", cv.gioitinh],
    ["Email CV", cv.email],
    ["Số điện thoại", cv.sdt],
    ["Địa chỉ", cv.diachi],
    ["Vị trí", cv.vitri],
    ["Ngành", cv.nganh],
    ["Mục tiêu nghề nghiệp", cv.muctieunghiep],
    ["Học vấn", cv.hocvan],
    ["Kinh nghiệm", cv.kinhnghiem],
    ["Kỹ năng", cv.kynang],
    ["Ngoại ngữ", cv.ngoaingu],
    ["Chứng chỉ", cv.chungchi],
    ["Dự án", cv.duan],
    ["Giải thưởng", cv.giaithuong],
    ["Hoạt động", cv.hoatdong],
    ["Mạng xã hội", cv.social],
    ["Portfolio", cv.portfolio],
    ["Mức lương mong muốn", cv.luongmongmuon],
    ["sinhvien_id", cv.sinhvien_id],
    ["created_at", cv.created_at],
  ]);
}

function renderJob(job: JD): string[] {
  return renderDetails([
    ["ID", job.id],
    ["Tên vị trí", job.ten_vi_tri],
    ["Phòng ban", job.phong_ban],
    ["Cấp bậc", job.cap_bac],
    ["Báo cáo cho", job.bao_cao_cho],
    ["Nhiệm vụ", job.nhiem_vu],
    ["Trình độ", job.trinh_do],
    ["Kinh nghiệm", job.kinh_nghiem],
    ["Kỹ năng", job.ky_nang],
    ["Kỹ năng mềm", job.ky_nang_mem],
    ["Ưu tiên", job.uu_tien],
    ["Mức lương", job.muc_luong],
    ["Phúc lợi", job.phuc_loi],
    ["Môi trường", job.moi_truong],
    ["Địa điểm", job.dia_diem],
    ["Thời gian", job.thoi_gian],
    ["Hạn nộp", job.han_nop],
    ["Cách ứng tuyển", job.cach_ung_tuyen],
    ["Ngày tạo", job.ngay_tao],
    ["Mô tả", job.mo_ta],
    ["doanhnghiep_id", job.doanhnghiep_id],
    ["Tên công ty", job.ten_cong_ty],
    ["Ngành", job.nganh],
    ["Avatar", job.avt],
  ]);
}

type SeededStudent = { definition: StudentSeed; account: SinhVien; cv: Cv };
type SeededBusiness = { definition: ReturnType<typeof buildDataset>["businesses"][number]; account: DoanhNghiep; jobs: JD[] };

function renderReport(
  dataset: ReturnType<typeof buildDataset>,
  seededStudents: readonly SeededStudent[],
  seededBusinesses: readonly SeededBusiness[],
  generatedAt: Date,
): string {
  const lines: string[] = [
    "# Work seed accounts",
    "",
    "> Dữ liệu synthetic dành cho development/QA. Mật khẩu bên dưới là plaintext vì cơ chế đăng nhập hiện tại của Work đang so sánh trực tiếp trường `matkhau`.",
    "> Không dùng các tài khoản này cho production. Tài liệu không chứa Neon connection string hoặc credential của database.",
    "",
    "## Thông tin seed",
    "",
    ...renderDetails([
      ["Seed version", SEED_VERSION],
      ["Generated at", generatedAt],
      ["Database", "neondb / public"],
      ["Student namespace", `${STUDENT_EMAIL_PREFIX}001..100@study2work.dev`],
      ["Business namespace", `${BUSINESS_EMAIL_PREFIX}01..10@study2work.dev`],
      ["Sinh viên", seededStudents.length],
      ["CV", seededStudents.length],
      ["Doanh nghiệp", seededBusinesses.length],
      ["JD", seededBusinesses.reduce((total, business) => total + business.jobs.length, 0)],
      ["Ngành nghề", dataset.industries.length],
      ["Rerun policy", "Additive idempotent; chỉ upsert namespace seed, không xóa dữ liệu khác"],
    ]),
    "",
    "## Mật khẩu dùng cho QA",
    "",
    `- Sinh viên: \`${STUDENT_PASSWORD}\``,
    `- Doanh nghiệp: \`${BUSINESS_PASSWORD}\``,
    "",
    "## Tài khoản sinh viên",
    "",
    "| STT | ID | Họ tên | Email | Mật khẩu | Chuyên ngành | CV ID |",
    "| ---: | ---: | --- | --- | --- | --- | ---: |",
  ];

  for (const seeded of seededStudents) {
    lines.push(`| ${seeded.definition.serial} | ${markdownValue(seeded.account.id)} | ${markdownValue(seeded.account.hoten)} | ${markdownValue(seeded.account.email)} | \`${markdownValue(seeded.account.matkhau)}\` | ${markdownValue(seeded.account.chuyennganh)} | ${markdownValue(seeded.cv.id)} |`);
  }

  for (const seeded of seededStudents) {
    lines.push(
      "",
      `### Sinh viên ${padded(seeded.definition.serial, 3)} — ${markdownValue(seeded.account.hoten)}`,
      "",
      ...renderDetails([
        ["ID tài khoản", seeded.account.id],
        ["Họ tên", seeded.account.hoten],
        ["Email", seeded.account.email],
        ["Mật khẩu", seeded.account.matkhau],
        ["Chuyên ngành", seeded.account.chuyennganh],
        ["Avatar", seeded.account.avt],
      ]),
      "",
      "#### CV",
      "",
      ...renderStudentCv(seeded.cv),
    );
  }

  lines.push("", "## Tài khoản doanh nghiệp", "");
  for (const [businessIndex, seeded] of seededBusinesses.entries()) {
    const { profile } = seeded.definition;
    lines.push(
      `### Doanh nghiệp ${padded(businessIndex + 1, 2)} — ${markdownValue(seeded.account.hoten)}`,
      "",
      ...renderDetails([
        ["ID tài khoản", seeded.account.id],
        ["Tên doanh nghiệp", seeded.account.hoten],
        ["Email", seeded.account.email],
        ["Mật khẩu", seeded.account.matkhau],
        ["Địa chỉ", seeded.account.diachi],
        ["Số điện thoại", seeded.account.sodienthoai],
        ["Ngành", profile.name],
        ["Mô tả doanh nghiệp", profile.description],
        ["Nhu cầu tuyển dụng", profile.recruitingFocus],
        ["Avatar", seeded.account.avt],
      ]),
      "",
      "#### JD",
      "",
    );

    for (const [jobIndex, job] of seeded.jobs.entries()) {
      lines.push(`##### JD ${businessIndex + 1}.${jobIndex + 1} — ${markdownValue(job.ten_vi_tri)}`, "", ...renderJob(job), "");
    }
  }

  return `${lines.join("\n")}\n`;
}

async function assertNeonTarget(prisma: PrismaClient, databaseUrl: string): Promise<void> {
  if (!databaseUrl.includes(".neon.tech")) {
    throw new Error("DATABASE_URL không trỏ đến Neon; seed bị từ chối để tránh ghi nhầm database.");
  }

  const target = await prisma.$queryRaw<Array<{ database_name: string; schema_name: string }>>`
    SELECT current_database() AS database_name, current_schema() AS schema_name
  `;
  const current = target[0];
  if (!current || current.database_name !== "neondb" || current.schema_name !== "public") {
    throw new Error("Neon target không đúng database/schema neondb/public; seed bị từ chối.");
  }
}

async function seedDatabase(prisma: PrismaClient, dataset: ReturnType<typeof buildDataset>): Promise<{
  students: SeededStudent[];
  businesses: SeededBusiness[];
}> {
  const seededBusinesses: SeededBusiness[] = [];

  for (const businessDefinition of dataset.businesses) {
    const account = await prisma.doanhNghiep.upsert({
      where: { email: businessDefinition.account.email },
      create: businessDefinition.account,
      update: businessDefinition.account,
    });

    const jobs: JD[] = [];
    for (const jobDefinition of businessDefinition.jobs) {
      const existing = await prisma.jD.findFirst({
        where: {
          doanhnghiep_id: account.id,
          ten_vi_tri: jobDefinition.ten_vi_tri,
        },
      });

      const data = {
        ...jobDefinition,
        doanhnghiep_id: account.id,
      };
      const job = existing
        ? await prisma.jD.update({ where: { id: existing.id }, data })
        : await prisma.jD.create({ data });
      jobs.push(job);
    }

    seededBusinesses.push({ definition: businessDefinition, account, jobs });
  }

  for (const industry of dataset.industries) {
    await prisma.banNganh.upsert({
      where: { nganh: industry },
      create: { nganh: industry },
      update: {},
    });
  }

  const seededStudents: SeededStudent[] = [];
  for (const studentDefinition of dataset.students) {
    const account = await prisma.sinhVien.upsert({
      where: { email: studentDefinition.account.email },
      create: studentDefinition.account,
      update: studentDefinition.account,
    });

    const cv = await prisma.cv.upsert({
      where: { sinhvien_id: account.id },
      create: { ...studentDefinition.cv, sinhvien_id: account.id },
      update: { ...studentDefinition.cv, sinhvien_id: account.id },
    });
    seededStudents.push({ definition: studentDefinition, account, cv });
  }

  return { students: seededStudents, businesses: seededBusinesses };
}

function printDryRun(dataset: ReturnType<typeof buildDataset>): void {
  const jobs = dataset.businesses.reduce((total, business) => total + business.jobs.length, 0);
  console.log("Dry-run thành công. Không kết nối hoặc ghi database.");
  console.log(`- Sinh viên: ${dataset.students.length}`);
  console.log(`- CV: ${dataset.students.length}`);
  console.log(`- Doanh nghiệp: ${dataset.businesses.length}`);
  console.log(`- JD: ${jobs}`);
  console.log(`- Ngành nghề: ${dataset.industries.length}`);
}

function safeErrorMessage(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message.replace(/postgres(?:ql)?:\/\/\S+/gi, "[redacted-database-url]");
}

async function main(): Promise<void> {
  const args = new Set(process.argv.slice(2));
  const isDryRun = args.has("--dry-run");
  const isConfirmed = args.has("--confirm-neon");
  const validMode = isDryRun !== isConfirmed;
  const unknownArgs = [...args].filter((arg) => arg !== "--dry-run" && arg !== "--confirm-neon");

  if (!validMode || unknownArgs.length > 0) {
    console.error("Usage: npm run seed:accounts -- --dry-run | --confirm-neon");
    process.exitCode = 1;
    return;
  }

  const dataset = buildDataset();
  validateDataset(dataset);

  if (isDryRun) {
    printDryRun(dataset);
    return;
  }

  const [{ default: prisma }, { DATABASE_URL }] = await Promise.all([
    import("../src/config/prisma.config.js"),
    import("../src/utils/constants.js"),
  ]);

  try {
    await assertNeonTarget(prisma, DATABASE_URL);
    const seeded = await seedDatabase(prisma, dataset);
    const repoRoot = resolve(fileURLToPath(new URL("../../..", import.meta.url)));
    const docsPath = resolve(repoRoot, "docs/seed_data/accounts.md");
    await writeFile(docsPath, renderReport(dataset, seeded.students, seeded.businesses, new Date()), "utf8");

    console.log("Seed Neon thành công và đã cập nhật docs/seed_data/accounts.md.");
    console.log(`- Sinh viên/CV: ${seeded.students.length}`);
    console.log(`- Doanh nghiệp: ${seeded.businesses.length}`);
    console.log(`- JD: ${seeded.businesses.reduce((total, business) => total + business.jobs.length, 0)}`);
    console.log(`- Ngành nghề: ${dataset.industries.length}`);
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((error: unknown) => {
  console.error(`Seed thất bại: ${safeErrorMessage(error)}`);
  process.exitCode = 1;
});
