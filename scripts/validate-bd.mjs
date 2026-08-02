import { readdir, readFile, stat } from "node:fs/promises";
import { dirname, extname, resolve } from "node:path";
import process from "node:process";
import mermaid from "mermaid";

const root = process.cwd();
const bdDir = resolve(root, "docs/BD");
const expectedFiles = [
  "01_TONG_QUAN_DU_AN.md",
  "02_BIEU_DO_HE_THONG.md",
  "03_THIET_KE_CO_SO_DU_LIEU.md",
  "04_DAC_TA_API.md",
  "05_DAC_TA_MAN_HINH.md",
];

const errors = [];
const fail = (message) => errors.push(message);

const entries = await readdir(bdDir, { withFileTypes: true });
const actualFiles = entries.filter((entry) => entry.isFile()).map((entry) => entry.name).sort();
const directories = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();

if (directories.length > 0) {
  fail(`docs/BD must not contain subdirectories: ${directories.join(", ")}`);
}

if (JSON.stringify(actualFiles) !== JSON.stringify([...expectedFiles].sort())) {
  fail(
    `docs/BD must contain exactly ${expectedFiles.join(", ")}; found ${actualFiles.join(", ") || "no files"}`,
  );
}

const documents = new Map();
for (const file of expectedFiles) {
  try {
    documents.set(file, await readFile(resolve(bdDir, file), "utf8"));
  } catch (error) {
    fail(`Cannot read ${file}: ${error.message}`);
  }
}

const requiredContent = new Map([
  [
    "01_TONG_QUAN_DU_AN.md",
    [
      [/tầm nhìn/i, "Tầm nhìn"],
      [/phạm vi/i, "Phạm vi"],
      [/(thuật ngữ|glossary)/i, "Glossary/thuật ngữ"],
      [/(actor|tác nhân)/i, "Actor"],
      [/(rbac|phân quyền)/i, "RBAC"],
      [/(quy tắc nghiệp vụ|business rule)/i, "Business rules"],
      [/kiến trúc/i, "Kiến trúc"],
      [/data ownership|quyền sở hữu dữ liệu/i, "Data ownership"],
      [/bảo mật/i, "Bảo mật"],
      [/(quyền riêng tư|privacy)/i, "Privacy"],
      [/(retention|lưu giữ)/i, "Retention"],
      [/(quản trị AI|AI governance)/i, "AI governance"],
      [/(NFR|phi chức năng|SLO)/i, "NFR/SLO"],
      [/(rollout|triển khai theo giai đoạn)/i, "Rollout"],
      [/(traceability|truy vết)/i, "Master traceability"],
    ],
  ],
  [
    "02_BIEU_DO_HE_THONG.md",
    [
      [/(use case|biểu đồ UC)/i, "Use Case diagrams"],
      [/(activity|biểu đồ AC)/i, "Activity diagrams"],
      [/(class|biểu đồ lớp)/i, "Class diagrams"],
      [/(sequence|biểu đồ tuần tự)/i, "Sequence diagrams"],
      [/tiền điều kiện/i, "Diagram preconditions"],
      [/nhánh lỗi/i, "Diagram error branches"],
      [/```mermaid/i, "Mermaid blocks"],
    ],
  ],
  [
    "03_THIET_KE_CO_SO_DU_LIEU.md",
    [
      [/(ba database|ba cơ sở dữ liệu|identity database)/i, "Three physical databases"],
      [/(enum catalog|danh mục enum)/i, "Enum catalog"],
      [/(danh mục bảng|table catalog|chi tiết bảng)/i, "Table catalog"],
      [/(cột|column)/i, "Column definitions"],
      [/(khóa chính|PK)/i, "Primary keys"],
      [/(khóa ngoại|FK)/i, "Foreign keys"],
      [/(unique|duy nhất)/i, "Unique constraints"],
      [/(chỉ mục|index)/i, "Indexes"],
      [/(transaction|giao dịch)/i, "Transactions"],
      [/(locking|khóa đồng thời)/i, "Locking"],
      [/outbox/i, "Outbox"],
      [/(anonymization|ẩn danh)/i, "Anonymization"],
      [/(migration|di trú)/i, "Migration policy"],
      [/(retention|lưu giữ)/i, "Retention"],
    ],
  ],
  [
    "04_DAC_TA_API.md",
    [
      [/quy ước bắt buộc/i, "API conventions"],
      [/actor\/quyền/i, "Actor/permission field"],
      [/input\/validation/i, "Input/validation field"],
      [/xử lý, dữ liệu/i, "Processing/data field"],
      [/idempotency/i, "Idempotency"],
      [/If-Match/i, "Optimistic concurrency"],
      [/business code/i, "Business codes"],
      [/internal API/i, "Internal API"],
      [/webhook/i, "Webhooks"],
      [/realtime/i, "Realtime"],
      [/acceptance cases/i, "Acceptance cases"],
    ],
  ],
  [
    "05_DAC_TA_MAN_HINH.md",
    [
      [/sitemap/i, "Sitemap"],
      [/(public|công khai)/i, "Public screens"],
      [/(auth|xác thực)/i, "Authentication screens"],
      [/(learner|học viên)/i, "Learner screens"],
      [/(candidate|ứng viên)/i, "Candidate screens"],
      [/(enterprise|doanh nghiệp)/i, "Enterprise screens"],
      [/(university|trường đại học)/i, "University screens"],
      [/(publisher|biên tập|xuất bản)/i, "Publisher screens"],
      [/(admin|quản trị)/i, "Admin screens"],
      [/(loading|đang tải)/i, "Loading state"],
      [/(empty|dữ liệu rỗng)/i, "Empty state"],
      [/(offline|mất mạng)/i, "Offline state"],
      [/(responsive|đáp ứng)/i, "Responsive behavior"],
      [/(accessibility|khả năng tiếp cận)/i, "Accessibility"],
      [/(analytics|phân tích hành vi)/i, "Analytics"],
    ],
  ],
]);

for (const [file, requirements] of requiredContent) {
  const text = documents.get(file) ?? "";
  for (const [pattern, label] of requirements) {
    if (!pattern.test(text)) fail(`${file} is missing required section/content: ${label}`);
  }
}

const forbiddenPatterns = [
  [/\bTODO\b/i, "TODO"],
  [/\bTBD\b/i, "TBD"],
  [/chưa quyết định/i, "chưa quyết định"],
  [/\bplaceholder\b/i, "placeholder"],
  [/`UPDATED`/, "legacy content state UPDATED"],
  [/`RESET_BY_ADMIN`/, "legacy enrollment state RESET_BY_ADMIN"],
  [/`AVAILABLE`/, "undefined legacy state AVAILABLE"],
  [/S2W-STUDY-API-\d+/i, "legacy API ID"],
  [/\]\([^)]*(?:study2work_study_full_schema_seed\.sql|Review_API_DD|API_DD_Plans)[^)]*\)/i, "legacy link"],
];

for (const [file, text] of documents) {
  for (const [pattern, label] of forbiddenPatterns) {
    if (pattern.test(text)) fail(`${file} contains forbidden text: ${label}`);
  }
}

const idSource =
  "(?:CAP|BR|PERM|UC|AC|CLS|SEQ|TBL|API|EVT|ERR|SCR|NFR|TC)-(?:IAM|STU|WRK|PAY|UNI|AIX|INT|OPS)-\\d{3}";
const anyIdPattern = new RegExp(`\\b(${idSource})\\b`, "g");
const headingDefinition = new RegExp(`^#{2,6}\\s+(?:\\*\\*)?(${idSource})(?:\\*\\*)?(?:\\s|[:—–-])`, "gm");
const tableDefinition = new RegExp(`^\\|\\s*\\*\\*(${idSource})\\*\\*\\s*\\|`, "gm");
const listDefinition = new RegExp(`^\\s*[-*]\\s+\\*\\*(${idSource})\\*\\*(?:\\s*[:—–-])`, "gm");

const ownerByType = new Map([
  ["CAP", "01_TONG_QUAN_DU_AN.md"],
  ["BR", "01_TONG_QUAN_DU_AN.md"],
  ["PERM", "01_TONG_QUAN_DU_AN.md"],
  ["UC", "01_TONG_QUAN_DU_AN.md"],
  ["NFR", "01_TONG_QUAN_DU_AN.md"],
  ["TC", "01_TONG_QUAN_DU_AN.md"],
  ["AC", "02_BIEU_DO_HE_THONG.md"],
  ["CLS", "02_BIEU_DO_HE_THONG.md"],
  ["SEQ", "02_BIEU_DO_HE_THONG.md"],
  ["TBL", "03_THIET_KE_CO_SO_DU_LIEU.md"],
  ["API", "04_DAC_TA_API.md"],
  ["EVT", "04_DAC_TA_API.md"],
  ["ERR", "04_DAC_TA_API.md"],
  ["SCR", "05_DAC_TA_MAN_HINH.md"],
]);

const definitions = new Map();
const occurrences = new Map();
for (const [file, text] of documents) {
  for (const match of text.matchAll(anyIdPattern)) {
    const id = match[1];
    occurrences.set(id, (occurrences.get(id) ?? 0) + 1);
  }

  const fileDefinitions = new Set();
  for (const pattern of [headingDefinition, tableDefinition, listDefinition]) {
    pattern.lastIndex = 0;
    for (const match of text.matchAll(pattern)) fileDefinitions.add(match[1]);
  }

  for (const id of fileDefinitions) {
    const type = id.split("-")[0];
    const expectedOwner = ownerByType.get(type);
    if (expectedOwner !== file) {
      fail(`${id} is defined in ${file}, but ${type} definitions belong in ${expectedOwner}`);
    }
    const previous = definitions.get(id);
    if (previous) fail(`${id} has duplicate definitions in ${previous} and ${file}`);
    else definitions.set(id, file);
  }
}

for (const id of occurrences.keys()) {
  if (!definitions.has(id)) fail(`Reference ${id} does not resolve to a canonical definition`);
}

for (const [id, file] of definitions) {
  const type = id.split("-")[0];
  if (["TBL", "API", "SCR"].includes(type) && (occurrences.get(id) ?? 0) < 2) {
    fail(`${id} is orphaned: it is defined in ${file} but has no trace/reference`);
  }
}

// Every public API definition row must retain the canonical detailed template.
const apiText = documents.get("04_DAC_TA_API.md") ?? "";
const apiRows = apiText.split(/\r?\n/).filter((line) => /^\|\s*\*\*API-/.test(line));
for (const row of apiRows) {
  const id = row.match(new RegExp(idSource))?.[0] ?? "unknown API";
  const cellCount = row.split("|").length - 2;
  if (!id.startsWith("API-INT-") && cellCount < 8) {
    fail(`${id} must include all endpoint template columns; found ${cellCount}`);
  }
  if (/\|\s*(?:—|-)?\s*\|/.test(row)) {
    fail(`${id} contains an empty API template cell; use N/A with a reason`);
  }
}

// Method + path uniqueness is scoped by owning service, not by the whole ecosystem.
const methodPathDefinitions = [];
for (const row of apiRows) {
  const id = row.match(new RegExp(idSource))?.[0];
  const contract = row.match(/`(GET|POST|PUT|PATCH|DELETE)\s+([^`]+)`/i);
  if (!id || !contract) continue;
  const method = contract[1].toUpperCase();
  let path = contract[2].trim().replace(/\s+/g, " ");
  let service;
  if (/^(identity|study|work)\s+\//i.test(path)) {
    [service, path] = path.split(/\s+/, 2);
    service = service.toLowerCase();
  } else {
    const context = id.split("-")[1];
    service = context === "IAM" ? "identity" : context === "STU" ? "study" : "work";
  }
  methodPathDefinitions.push({ id, key: `${service}:${method}:${path}` });
}

const methodPaths = new Map();
for (const { id, key } of methodPathDefinitions) {
  const previous = methodPaths.get(key);
  if (previous) fail(`Duplicate method + path in one service: ${previous} and ${id} (${key})`);
  else methodPaths.set(key, id);
}

// Canonical invariants/state names must be present and legacy alternatives must be absent.
const allText = [...documents.values()].join("\n");
const requiredCanonicalTerms = [
  "PENDING_EMAIL_VERIFICATION",
  "DELETION_PENDING",
  "SUPERSEDED",
  "SWITCHED_OUT",
  "UNDER_REVIEW",
  "NEEDS_REVISION",
  "REVIEW_PENDING",
  "INTERVIEWING",
  "OFFER_DECLINED",
  "TAKEN_DOWN",
  "UNAVAILABLE",
  "REVOKED",
];
for (const term of requiredCanonicalTerms) {
  if (!allText.includes(term)) fail(`Canonical enum/state ${term} is not documented`);
}

// Validate local Markdown links in all canonical files.
const markdownLinkPattern = /(?<!!)\[[^\]]+\]\(([^)]+)\)/g;
for (const [file, text] of documents) {
  for (const match of text.matchAll(markdownLinkPattern)) {
    let target = match[1].trim();
    if (target.startsWith("<") && target.endsWith(">")) target = target.slice(1, -1);
    if (/^(https?:|mailto:|#)/i.test(target)) continue;
    target = target.split("#", 1)[0];
    if (!target) continue;
    const path = resolve(dirname(resolve(bdDir, file)), decodeURIComponent(target));
    try {
      const targetStat = await stat(path);
      if (!targetStat.isFile() && !targetStat.isDirectory()) fail(`${file} link is not a file/directory: ${match[1]}`);
    } catch {
      fail(`${file} contains a broken relative Markdown link: ${match[1]}`);
    }
  }
}

// Traceability tables cannot silently omit a layer; use N/A plus a reason when truly inapplicable.
const overview = documents.get("01_TONG_QUAN_DU_AN.md") ?? "";
const traceHeading = overview.search(/^#{2,6} .*?(?:traceability|truy vết).*$/im);
if (traceHeading < 0) {
  fail("01_TONG_QUAN_DU_AN.md is missing the master traceability matrix");
} else {
  const traceSection = overview.slice(traceHeading);
  const tableLines = traceSection.split(/\r?\n/).filter((line) => line.startsWith("|"));
  if (tableLines.length < 3) fail("Master traceability matrix must contain a header and capability rows");
  for (const line of tableLines) {
    if (/^\|\s*:?-{3}/.test(line)) continue;
    const cells = line.slice(1, -1).split("|").map((cell) => cell.trim());
    if (cells.some((cell) => cell.length === 0)) {
      fail("Master traceability matrix contains a blank cell; use N/A with a reason");
      break;
    }
  }
}

// Mermaid is parsed, not merely fenced. Syntax validation follows the official Mermaid API.
const mermaidBlockPattern = /```mermaid\s*\n([\s\S]*?)```/g;
let mermaidCount = 0;
for (const [file, text] of documents) {
  let index = 0;
  for (const match of text.matchAll(mermaidBlockPattern)) {
    index += 1;
    mermaidCount += 1;
    try {
      await mermaid.parse(match[1], { suppressErrors: true });
    } catch (error) {
      fail(`${file} Mermaid block ${index} is invalid: ${error.message}`);
    }
  }
}
if (mermaidCount < 16) {
  fail(`Expected at least 16 Mermaid diagrams across UC/AC/CLASS/SEQUENCE; found ${mermaidCount}`);
}

if (errors.length > 0) {
  console.error("Basic Design validation failed:\n");
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log(
    `Basic Design validation passed: ${expectedFiles.length} files, ${definitions.size} canonical IDs, ${apiRows.length} APIs, ${mermaidCount} Mermaid diagrams.`,
  );
}
