#!/usr/bin/env python3
"""Generate source-traceable Markdown API DDs for the V1-PILOT catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BD = ROOT / "docs" / "BD"
TEMPLATE = ROOT / ".agent" / "docs" / "dd" / "DD_API_Template_MD"
OUT = ROOT / "docs" / "DD" / "V1_PILOT"
ZIP = ROOT / "docs" / "DD" / "V1_PILOT.zip"
T = chr(96)
FENCE = T * 3

DOMAINS = {
    "IAM": ("01_IAM", "Platform Identity"),
    "STU": ("02_STUDY", "Study"),
    "WRK": ("03_WORK", "Work"),
    "UNI": ("04_UNIVERSITY", "University"),
    "PAY": ("05_PAYMENT", "Payment"),
    "AIX": ("06_AI", "AI"),
    "OPS": ("07_OPERATIONS", "Operations"),
    "INT": ("08_INTEGRATION", "Integration and Realtime"),
}
DOMAIN_ORDER = tuple(DOMAINS)
EXPECTED = {
    "IAM": 25,
    "STU": 62,
    "WRK": 62,
    "UNI": 16,
    "PAY": 16,
    "AIX": 10,
    "OPS": 10,
    "INT": 11,
}
GAPS = [
    ("OQ-IAM-AUTHVERSION", "Nguồn lưu authVersion", "IAM", "users và identity projection chưa mô tả cột hoặc nguồn dữ liệu cho authVersion dùng trong JWT/sự kiện.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.1"),
    ("OQ-IAM-MFA-ENROLLMENT", "Mô hình MFA chờ xác nhận", "IAM", "mfa_methods chưa mô tả trạng thái ghi danh MFA đang chờ xác nhận và thời hạn.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.1"),
    ("OQ-STU-ONBOARDING", "Bản nháp và cấu hình onboarding", "STU", "Hợp đồng lưu nháp, trạng thái và câu hỏi onboarding chưa khớp mô hình onboarding_submissions bất biến.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2"),
    ("OQ-STU-SKILLS-HISTORY", "Nguồn kỹ năng và lịch sử học", "STU", "Một số API kỹ năng và lịch sử học chưa có bảng liên kết, lịch sử hoặc chính sách lưu giữ rõ ràng.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2"),
    ("OQ-STU-EVIDENCE-FILES", "Quan hệ minh chứng và tệp", "STU", "evidence_records chưa thể hiện rõ quan hệ với file_objects cho hợp đồng minh chứng có tệp.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.2"),
    ("OQ-WRK-SEARCH-CONSENT", "Đồng ý tìm kiếm ứng viên", "WRK", "Lịch sử chính sách, thời hạn và trường hiển thị của search consent chưa có mô hình riêng phù hợp.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3"),
    ("OQ-WRK-PUBLIC-JOB-SLUG", "Định danh jobSlug công khai", "WRK", "Tuyến công khai dùng job slug nhưng schema chỉ bảo đảm duy nhất trong không gian dữ liệu.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3"),
    ("OQ-UNI-INCOMPLETE-FLOWS", "Luồng University chưa đủ mô hình/API", "UNI", "Affiliation invitation, phản hồi đề nghị và dữ liệu báo cáo chưa có mô hình hoặc API đầy đủ.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3"),
    ("OQ-PAY-ENTITLEMENT-HOLD", "Giữ chỗ và hoàn quyền lợi", "PAY", "Thời điểm trừ, hoàn và chống chi tiêu trùng cho quyền lợi chưa được mô hình hóa đầy đủ.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4"),
    ("OQ-PAY-PROMOTION-METRICS", "Mô hình đo lường quảng bá", "PAY", "Thiết kế chưa chốt giữa lưu sự kiện hiển thị/nhấp gốc và chỉ giữ bộ đếm tổng hợp.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4"),
    ("OQ-AIX-EVALUATION-KILL-SWITCH", "Đánh giá AI và kill switch", "AIX", "Dataset, evaluation run/result và phạm vi kill switch chi tiết hơn mô hình hiện hành.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.4"),
    ("OQ-OPS-MISSING-READ-CONTRACTS", "Các hợp đồng vận hành còn thiếu", "OPS", "Một số màn vận hành cần queue, detail hoặc approval counterpart nhưng catalog chỉ có mutation hoặc thiếu API đối ứng.", "06_BAO_CAO_RAO_SOAT_LOGIC.md §4.3–§4.4"),
]
HTTP_BY_CODE = {
    "INVALID_CREDENTIALS": "401",
    "ACCOUNT_SUSPENDED": "403",
    "REFRESH_TOKEN_REUSE_DETECTED": "401",
    "MFA_REQUIRED": "403",
    "ONBOARDING_REQUIRED": "409",
    "PRIMARY_PATH_SWITCH_COOLDOWN": "409",
    "FILE_NOT_CLEAN": "409",
    "ATTEMPT_LIMIT_REACHED": "409",
    "REVIEW_CONFLICT": "412",
    "APPLICATION_ALREADY_EXISTS": "409",
    "JOB_REVISION_STALE": "409",
    "INVALID_APPLICATION_TRANSITION": "409",
    "CONVERSATION_READ_ONLY": "409",
    "CONSENT_REQUIRED": "403",
    "PAYMENT_AMOUNT_MISMATCH": "202",
    "ORDER_ALREADY_SETTLED": "409",
    "ENTITLEMENT_INSUFFICIENT": "409",
    "AI_DISABLED": "503",
    "AI_OUTPUT_BLOCKED": "422",
    "VERSION_CONFLICT": "412",
    "IDEMPOTENCY_KEY_REUSED": "409",
    "DEPENDENCY_UNAVAILABLE": "503",
    "PERMISSION_DENIED": "403",
}


@dataclass(frozen=True)
class Api:
    api_id: str
    domain: str
    source_line: int
    section: str
    subsection: str
    method: str
    raw_target: str
    endpoint: str
    transport: str
    service: str | None
    actor: str
    input_contract: str
    processing: str
    operations: str
    errors: str
    screens: str
    operation_class: str
    folder: str


@dataclass(frozen=True)
class Table:
    table_id: str
    name: str
    source_line: int
    columns: tuple[str, ...]


def q(value: object) -> str:
    return T + str(value) + T


def link(label: str, target: str) -> str:
    return "[" + label + "](" + target + ")"


def cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[tuple[object, ...]]) -> str:
    lines = [
        "| " + " | ".join(cell(item) for item in headers) + " |",
        "| " + " | ".join("---:" if i == 0 else "---" for i in range(len(headers))) + " |",
    ]
    lines.extend("| " + " | ".join(cell(item) for item in row) + " |" for row in rows)
    return "\n".join(lines)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def strip_md(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("**", "").replace("\\|", "|")).strip()


def spans(value: str) -> list[str]:
    pattern = re.escape(T) + r"([^" + re.escape(T) + r"]+)" + re.escape(T)
    return re.findall(pattern, value)


def row_cells(value: str) -> list[str]:
    value = value.strip()
    if not value.startswith("|") or not value.endswith("|"):
        raise ValueError("invalid Markdown table row")
    result: list[str] = []
    current: list[str] = []
    escaped = False
    for char in value[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    result.append("".join(current).strip())
    return result


def slug(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = value.replace("{", "").replace("}", "").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def parse_target(value: str) -> tuple[str, str, str, str | None]:
    raw = spans(value)[0] if spans(value) else strip_md(value)
    parts = raw.split()
    if len(parts) < 2 or parts[0].upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        raise ValueError("invalid endpoint target: " + raw)
    method = parts[0].upper()
    if parts[1].startswith("wss://"):
        return method, raw, parts[1], None
    if len(parts) >= 3 and parts[1] in {"identity", "study", "work"} and parts[2].startswith("/"):
        return method, raw, parts[2], parts[1]
    return method, raw, parts[1], None


def catalog() -> list[Api]:
    path = BD / "04_DAC_TA_API.md"
    pattern = re.compile(r"^\|\s*\*\*(API-(IAM|STU|WRK|UNI|PAY|AIX|OPS|INT)-\d{3})\*\*\s*\|")
    section = ""
    subsection = ""
    result: list[Api] = []
    for source_line, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith("## "):
            section = strip_md(line[3:])
        elif line.startswith("### "):
            subsection = strip_md(line[4:])
        match = pattern.match(line)
        if not match:
            continue
        cells = row_cells(line)
        api_id, domain = match.group(1), match.group(2)
        method, raw_target, endpoint, service = parse_target(cells[1])
        if endpoint.startswith("wss://"):
            transport, op_class = "websocket", "realtime"
        elif service:
            transport, op_class = "internal_http", ("read_candidate" if method == "GET" else "mutation_candidate")
        else:
            transport, op_class = "public_http", ("read_candidate" if method == "GET" else "mutation_candidate")
        if len(cells) == 8:
            actor, input_contract, processing, operations, errors, screens = cells[2:]
        elif len(cells) == 6:
            actor, input_contract, processing, errors = cells[2:]
            operations = "N/A — internal endpoint table has no separate operations column."
            screens = "SYSTEM"
        elif len(cells) == 4:
            actor, processing = cells[2:]
            input_contract = "N/A — WebSocket protocol is specified as one contract."
            operations = "N/A — WebSocket lifecycle is part of the protocol contract."
            errors = "SOURCE_REQUIRED — no independent endpoint error catalog."
            screens = "SYSTEM"
        else:
            raise ValueError("unexpected API row shape at line " + str(source_line))
        result.append(
            Api(
                api_id=api_id,
                domain=domain,
                source_line=source_line,
                section=section,
                subsection=subsection,
                method=method,
                raw_target=raw_target,
                endpoint=endpoint,
                transport=transport,
                service=service,
                actor=strip_md(actor),
                input_contract=strip_md(input_contract),
                processing=strip_md(processing),
                operations=strip_md(operations),
                errors=strip_md(errors),
                screens=strip_md(screens),
                operation_class=op_class,
                folder=api_id + "_" + slug(raw_target.replace(" ", "-")),
            )
        )
    counts = Counter(item.domain for item in result)
    if len(result) != 212 or len({item.api_id for item in result}) != 212 or dict(counts) != EXPECTED:
        raise ValueError("catalog must contain the current 212 API IDs")
    if len({item.folder for item in result}) != 212:
        raise ValueError("DD folder slug collision")
    return result


def table_catalog() -> dict[str, Table]:
    path = BD / "03_THIET_KE_CO_SO_DU_LIEU.md"
    source = path.read_text(encoding="utf-8").splitlines()
    heading = re.compile(r"^####\s+(TBL-[A-Z]+-\d+)\s+—\s+(.+)$")
    result: dict[str, Table] = {}
    for index, line in enumerate(source):
        match = heading.match(line)
        if not match:
            continue
        names = spans(match.group(2))
        if not names:
            continue
        details = []
        for next_line in source[index + 1 : index + 8]:
            if next_line.startswith("#### ") or next_line.startswith("### "):
                break
            if "Cột riêng:" in next_line:
                details.append(next_line)
        columns: list[str] = []
        for item in spans(" ".join(details)):
            if re.fullmatch(r"[a-z][a-z0-9_]*", item) and item not in columns:
                columns.append(item)
        result[names[0]] = Table(match.group(1), names[0], index + 1, tuple(columns))
    return result


def refs(api: Api, tables: dict[str, Table]) -> list[Table]:
    text = " ".join((api.input_contract, api.processing, api.operations))
    result = []
    for name, item in tables.items():
        if re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", text):
            result.append(item)
    return result


def has_write(api: Api) -> bool:
    if api.transport == "websocket":
        return False
    text = (" " + api.processing + " " + api.operations + " ").lower()
    return any(
        token in text
        for token in (" tx:", " thêm ", " tạo ", " ghi ", " cập nhật ", " đánh dấu ", " thu hồi ", " chèn ", " xóa ", " insert ", " update ", " delete ", " revoke ")
    )


def is_webhook(api: Api) -> bool:
    return "/webhooks/" in api.endpoint or "webhook" in api.raw_target.lower()


def operation(api: Api) -> str:
    text = (" " + api.processing + " " + api.operations + " ").lower()
    if " xóa " in text or " delete " in text:
        return "DELETE"
    if " cập nhật " in text or " update " in text or " đánh dấu " in text:
        return "UPDATE"
    if " thêm " in text or " tạo " in text or " chèn " in text or " insert " in text:
        return "INSERT"
    return "SOURCE_REQUIRED"


def path_params(api: Api) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\{([A-Za-z][A-Za-z0-9_]*)\}", api.endpoint)))


def inputs(api: Api) -> tuple[list[str], list[str]]:
    before = api.input_contract.split("→", 1)[0].strip()
    ignored = {
        "HTTP", "HTTPS", "JSON", "UUID", "VND", "TX", "MFA", "TOTP", "SYSTEM", "ACTIVE", "PENDING", "READY", "FAILED", "CANCELLED", "PUBLISHED", "DRAFT", "CLEAN", "ISSUED", "REVOKED", "HIDDEN", "UNAVAILABLE", "SOURCE_REQUIRED", "Authorization", "Idempotency-Key", "If-Match",
    }
    physical: list[str] = []
    for span in spans(before):
        for item in re.findall(r"[A-Za-z][A-Za-z0-9_-]*", span):
            if item in ignored or item in path_params(api) or item.isupper() or item in physical:
                continue
            physical.append(item)
    unquoted = re.sub(re.escape(T) + r"[^" + re.escape(T) + r"]+" + re.escape(T), "", before).strip(" ,;:")
    gaps = [] if not unquoted or "không có đầu vào" in before.lower() else [unquoted]
    return physical, gaps


def error_codes(api: Api) -> list[str]:
    ignored = {"HTTP", "API", "SCR", "SYSTEM", "SOURCE_REQUIRED", "TBD"}
    result = []
    for item in re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", api.errors):
        if item not in ignored and item not in result:
            result.append(item)
    return result


def output_phrase(api: Api) -> str:
    return api.input_contract.split("→", 1)[1].strip() if "→" in api.input_contract else "SOURCE_REQUIRED — endpoint row does not split input and output fields."


def gap_ids(api: Api) -> list[str]:
    text = " ".join((api.api_id, api.endpoint, api.input_contract, api.processing, api.operations)).lower()
    result = []
    if "authversion" in text:
        result.append("OQ-IAM-AUTHVERSION")
    if api.api_id in {"API-IAM-017", "API-IAM-018"}:
        result.append("OQ-IAM-MFA-ENROLLMENT")
    if api.domain == "STU" and "onboarding" in text:
        result.append("OQ-STU-ONBOARDING")
    if api.domain == "STU" and ("skill" in text or "lịch sử học" in text):
        result.append("OQ-STU-SKILLS-HISTORY")
    if api.domain in {"STU", "INT"} and "evidence" in text and ("file" in text or "tệp" in text):
        result.append("OQ-STU-EVIDENCE-FILES")
    if api.domain == "WRK" and ("search" in text or "tìm kiếm" in text or "consent" in text):
        result.append("OQ-WRK-SEARCH-CONSENT")
    if api.api_id == "API-WRK-002" or "/jobs/{slug}" in api.endpoint:
        result.append("OQ-WRK-PUBLIC-JOB-SLUG")
    if api.domain == "UNI":
        result.append("OQ-UNI-INCOMPLETE-FLOWS")
    if api.domain == "PAY" and ("entitlement" in text or "refund" in text):
        result.append("OQ-PAY-ENTITLEMENT-HOLD")
    if api.domain == "PAY" and ("impression" in text or "click" in text or "promotion" in text):
        result.append("OQ-PAY-PROMOTION-METRICS")
    if api.domain == "AIX":
        result.append("OQ-AIX-EVALUATION-KILL-SWITCH")
    if api.domain == "OPS":
        result.append("OQ-OPS-MISSING-READ-CONTRACTS")
    return list(dict.fromkeys(result))


def fm(api: Api, title: str, order: int, sheet: str) -> str:
    return "\n".join(
        [
            "---",
            'title: "' + title + '"',
            "order: " + str(order),
            'source_workbook: "DD_API_Template(1).xlsx"',
            'source_sheet: "' + sheet + '"',
            'format: "markdown"',
            'dd_id: "' + api.api_id + '"',
            'api_name: "' + api.raw_target.replace('"', "'") + '"',
            'status: "Draft — Needs Confirmation"',
            "---",
        ]
    )


def appendix(filename: str, sheet: str) -> str:
    return "\n".join(
        [
            "---",
            "## Phụ lục đối chiếu template Markdown",
            "",
            "- Template Markdown: " + q(".agent/docs/dd/DD_API_Template_MD/" + filename) + ".",
            "- Workbook/sheet prototype: " + q("DD_API_Template(1).xlsx") + " / " + q(sheet) + ".",
            "- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.",
        ]
    )


def api_path(api: Api, output: Path) -> Path:
    return output / DOMAINS[api.domain][0] / api.folder


def local_source(filename: str) -> str:
    return "../../../../BD/" + filename


def headers(api: Api) -> list[tuple[object, ...]]:
    rows: list[tuple[object, ...]] = []
    full = " ".join((api.actor, api.input_contract, api.processing, api.operations))
    if api.transport == "internal_http":
        rows.append((1, "Service authentication", "SOURCE_REQUIRED", "Yes", "mTLS + service JWT/signature", "Internal convention confirms the mechanisms, not a named carrier.", "[S02](./05_Data_Mapping.md#s02)"))
    elif is_webhook(api):
        rows.append((1, "Provider signature/authentication", "SOURCE_REQUIRED", "Yes", "SOURCE_REQUIRED — provider-specific signature and optional IP allowlist", "Inbound webhook; exact header/query/form carrier and canonical signing input are not locked by the endpoint row.", "[S02](./05_Data_Mapping.md#s02)"))
    elif api.transport == "public_http" and "Không xác thực" not in api.actor and "Cookie/mã làm mới" not in api.actor and "nhà cung cấp" not in api.actor.lower():
        rows.append((1, "Bearer access token", "Authorization", "Yes", "Bearer access-token", "BD §2.2 public authentication.", "[S02](./05_Data_Mapping.md#s02)"))
    elif "Cookie/mã làm mới" in api.actor:
        rows.append((1, "Refresh-token carrier", "SOURCE_REQUIRED", "Yes", "Cookie/mã làm mới", "Physical cookie/header name is not locked.", "[S01](./05_Data_Mapping.md#s01)"))
    if "khóa lặp" in full.lower() or "idempotency-key" in full.lower():
        rows.append((len(rows) + 1, "Idempotency key", "Idempotency-Key", "Yes", "16–128 random characters", "BD §2.4.", "[S05](./05_Data_Mapping.md#s05)"))
    if "if-match" in full.lower():
        rows.append((len(rows) + 1, "Optimistic-concurrency version", "If-Match", "Yes", "Quoted version", "DIRECT endpoint/global convention.", "[S03](./05_Data_Mapping.md#s03)"))
    return rows


def cover(api: Api, today: str) -> str:
    return "\n".join(
        [
            fm(api, "Cover", 0, "Cover"),
            "",
            "# Study2Work — API Detail Design",
            "",
            "## Thông tin tài liệu",
            "",
            table(
                ["Thuộc tính", "Giá trị"],
                [
                    ("Project/System", q("Study2Work V1-PILOT")),
                    ("Module", q(DOMAINS[api.domain][1])),
                    ("Loại tài liệu", q("API Detail Design")),
                    ("API ID", q(api.api_id)),
                    ("API name", q(api.raw_target)),
                    ("HTTP method", q(api.method)),
                    ("Endpoint", q(api.endpoint)),
                    ("Version", q("0.1")),
                    ("Status", q("Draft — Needs Confirmation")),
                    ("Created by", "Generated from current docs/BD"),
                    ("Reviewed by", q("TBD")),
                    ("Approved by", q("TBD")),
                    ("Created date", q(today)),
                    ("Updated date", q(today)),
                ],
            ),
            "",
            "## Tên hiển thị",
            "",
            FENCE + "text",
            "Study2Work API Detail Design",
            api.api_id + " — " + api.raw_target,
            FENCE,
            "",
            "## Căn cứ",
            "",
            "- Primary endpoint contract: " + q("docs/BD/04_DAC_TA_API.md:L" + str(api.source_line)) + ".",
            "- This DD remains Draft because BD does not lock every wire field, DB column mapping or source gap.",
            "",
            appendix("00_Cover.md", "Cover"),
        ]
    )


def history(api: Api, today: str) -> str:
    return "\n".join(
        [
            fm(api, "Lịch sử update", 1, "Lịch sử"),
            "",
            "# Lịch sử update",
            "",
            "## Metadata",
            "",
            table(["Thuộc tính", "Giá trị"], [("Ngày tạo", q(today)), ("Ngày update cuối cùng", q(today))]),
            "",
            "## Lịch sử thay đổi",
            "",
            table(["Version", "Ngày update", "Người update", "Nội dung update", "Remarks"], [(q("0.1"), q(today), "Generated from docs/BD", "Create source-traceable Draft DD", "No unsupported fields, tables, columns, roles or codes added.")]),
            "",
            appendix("01_Lich_su.md", "Lịch sử"),
        ]
    )


def overview(api: Api, tables: dict[str, Table]) -> str:
    mentioned = refs(api, tables)
    writing = has_write(api)
    gaps = gap_ids(api)
    source_rows = [
        "- " + link("04_DAC_TA_API.md", local_source("04_DAC_TA_API.md")) + ": " + q("L" + str(api.source_line)) + " — endpoint contract.",
        "- " + link("01_TONG_QUAN_DU_AN.md", local_source("01_TONG_QUAN_DU_AN.md")) + " — business rules, authorization and service boundaries.",
        "- " + link("03_THIET_KE_CO_SO_DU_LIEU.md", local_source("03_THIET_KE_CO_SO_DU_LIEU.md")) + " — physical terminology when a table is explicitly named.",
        "- " + link("02_BIEU_DO_HE_THONG.md", local_source("02_BIEU_DO_HE_THONG.md")) + " — flow/concurrency context only.",
        "- " + link("05_DAC_TA_MAN_HINH.md", local_source("05_DAC_TA_MAN_HINH.md")) + " — screen coverage only.",
    ]
    transaction = "DIRECT — endpoint prose states a transaction." if "tx:" in api.processing.lower() else ("TBD — mutation candidate has no complete transaction boundary at endpoint detail." if api.operation_class == "mutation_candidate" else "N/A — no source-confirmed business mutation.")
    parts = [
        fm(api, "Overview", 2, "Overview"),
        "",
        "# Overview",
        "",
        "## Khái quát",
        "",
        table(
            ["Thuộc tính", "Giá trị"],
            [
                ("API ID", q(api.api_id)),
                ("Module", q(DOMAINS[api.domain][1])),
                ("Method", q(api.method)),
                ("Endpoint", q(api.endpoint)),
                ("Purpose", output_phrase(api)),
                ("Consumer/Actor", api.actor),
                ("Authentication", "mTLS/service identity" if api.transport == "internal_http" else ("WebSocket protocol authentication" if api.transport == "websocket" else api.actor)),
                ("Authorization", api.actor),
                ("Basis", q("DIRECT") + " for catalog facts; " + q("SOURCE_REQUIRED") + " for missing field detail."),
                ("Status", q("Draft — Needs Confirmation")),
                ("Transaction", transaction),
                ("Side effects", api.operations),
            ],
        ),
        "",
        "## Sources",
        "",
        *source_rows,
        "",
        "## Tables read",
        "",
    ]
    if mentioned and not writing:
        parts.extend("- " + q(item.name) + " (" + q(item.table_id) + ")." for item in mentioned)
    else:
        parts.append("N/A — no read table is independently materialized from this endpoint row.")
    parts.extend(["", "## Tables write", ""])
    if mentioned and writing:
        parts.extend("- " + q(item.name) + " (" + q(item.table_id) + ")." for item in mentioned)
    elif api.operation_class == "mutation_candidate":
        parts.append("SOURCE_REQUIRED — catalog describes a mutation candidate without a certain physical target table.")
    else:
        parts.append("N/A — READ-ONLY API.")
    parts.extend(["", "## Mục chú ý", ""])
    parts.append("- Transport: " + q(api.transport) + ".")
    if api.service:
        parts.append("- Target service: " + q(api.service) + ".")
    if api.transport == "websocket":
        parts.append("- WebSocket delivery is not modeled as a REST response envelope.")
    parts.extend(["", "## Assumptions", "", "- None. Missing physical keys, types, locations, columns and value sources remain " + q("SOURCE_REQUIRED") + "."])
    parts.extend(["", "## Conflicts", ""])
    if gaps:
        parts.extend("- [" + item + "](../../OPEN_QUESTIONS.md#" + item.lower() + ")." for item in gaps)
    else:
        parts.append("N/A — no official review gap matched automatically; endpoint field detail may still be SOURCE_REQUIRED.")
    parts.extend(
        [
            "",
            "## Security note",
            "",
            "- Apply the global BD prohibition on logging or returning secrets, tokens, raw sensitive content, SQL and stack traces.",
            "- Authorization, tenant and ownership checks are server-authoritative.",
            "",
            "## Performance note",
            "",
            "- Apply pagination, cache, rate-limit and retry behavior only where the API catalog or BD §2.3–§2.4 states it.",
            "",
            appendix("02_Overview.md", "Overview"),
        ]
    )
    return "\n".join(parts)


def request(api: Api) -> str:
    if api.transport == "websocket":
        return websocket_request(api)
    header_rows = headers(api)
    params = path_params(api)
    physical, gaps = inputs(api)
    body_source = "phần thân" in api.input_contract.lower() or "body" in api.input_contract.lower()
    query_rows = []
    body_rows = []
    destination = body_rows if body_source else query_rows
    for number, item in enumerate(physical, start=1):
        record = (
            number,
            q(item),
            q(item),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            q("SOURCE_REQUIRED"),
            "DIRECT physical key; source does not lock complete type/location validation.",
            "[S01](./05_Data_Mapping.md#s01)",
        )
        destination.append(record)
    parts = [
        fm(api, "Request", 3, "1.Request"),
        "",
        "# Request",
        "",
        "## API endpoint",
        "",
        table(
            ["Thuộc tính", "Giá trị"],
            [
                ("HTTP method", q(api.method)),
                ("URI", q(api.endpoint)),
                ("Character encoding", q("UTF-8")),
                ("Content-Type", "SOURCE_REQUIRED — provider-specific inbound webhook carrier." if is_webhook(api) else (q("application/json; charset=utf-8") if api.transport == "public_http" else "SOURCE_REQUIRED — protocol-specific carrier.")),
            ],
        ),
        "",
        "## Request header",
        "",
    ]
    if header_rows:
        parts.append(table(["No", "Logical name", "Field name", "Required", "Value/Format", "Description", "Data Mapping reference"], header_rows))
    else:
        parts.append("N/A — no physical request header is independently confirmed by the endpoint row.")
    parts.extend(["", "## Path parameters", ""])
    if params:
        path_rows = [
            (number, q(item), q(item), q("string"), "Yes", "N/A", "N/A", "Path segment", "SOURCE_REQUIRED", "N/A", "DIRECT from URI.", "[S01](./05_Data_Mapping.md#s01)")
            for number, item in enumerate(params, start=1)
        ]
        parts.append(table(["No", "Logical name", "Physical name", "Type", "Required", "Min", "Max", "Format", "Valid values", "Default", "Description", "Data Mapping reference"], path_rows))
    else:
        parts.append("N/A — endpoint has no path placeholder.")
    parts.extend(["", "## Query parameters", ""])
    if query_rows:
        parts.append(table(["No", "Logical name", "Physical name", "Type", "Required", "Min", "Max", "Format", "Valid values", "Default", "Description", "Data Mapping reference"], query_rows))
    else:
        parts.append("N/A — no query location is source-confirmed.")
    parts.extend(["", "## Request body", ""])
    if body_rows:
        expanded = []
        for row in body_rows:
            expanded.append(row[:7] + (q("SOURCE_REQUIRED"),) + row[7:])
        parts.append(table(["No", "Logical name", "Physical name", "Type", "Required", "Min", "Max", "Character type", "Format", "Valid values", "Default", "Description", "Data Mapping reference"], expanded))
    else:
        parts.append("N/A — no complete physical request-body schema is source-confirmed.")
    parts.extend(["", "## Contract items chưa materialize thành field", ""])
    gap_rows = [(number, phrase, "Physical key, location, type or rule", q("SOURCE_REQUIRED") + "; not included in JSON example.") for number, phrase in enumerate(gaps, start=1)]
    if not gap_rows:
        gap_rows = [(1, "N/A", "N/A", "No additional unmaterialized input phrase detected.")]
    parts.append(table(["No", "Source phrase", "Missing contract detail", "Handling"], gap_rows))
    parts.extend(
        [
            "",
            "## Contract source",
            "",
            "> " + api.input_contract,
            "",
            "## Ví dụ Request data",
            "",
            "N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.",
            "",
            appendix("03_Request.md", "1.Request"),
        ]
    )
    return "\n".join(parts)


def websocket_request(api: Api) -> str:
    handshake_rows = [
        ("URI", q(api.endpoint), "DIRECT protocol endpoint."),
        ("Client authentication", "Access token via secure subprotocol or first authentication frame", "DIRECT lifecycle contract; exact physical carrier remains SOURCE_REQUIRED."),
        ("Connection authorization", "Server checks recipient object, session and projection", "DIRECT lifecycle contract."),
    ]
    message_rows = [
        (1, "subscribe", q("type"), q("subscribe"), "DIRECT named field/value.", "[S03](./05_Data_Mapping.md#s03)"),
        (2, "subscribe", q("applicationId"), q("SOURCE_REQUIRED"), "DIRECT named field; type/requiredness is not split by source.", "[S03](./05_Data_Mapping.md#s03)"),
        (3, "subscribe", q("lastSequence"), q("SOURCE_REQUIRED"), "DIRECT named field; type/requiredness is not split by source.", "[S03](./05_Data_Mapping.md#s03)"),
    ]
    return "\n".join(
        [
            fm(api, "Request", 3, "1.Request"),
            "",
            "# Request",
            "",
            "## WebSocket handshake",
            "",
            table(["Thuộc tính", "Giá trị", "Handling"], handshake_rows),
            "",
            "## Client message contract",
            "",
            table(["No", "Message", "Field", "Value", "Status", "Data Mapping reference"], message_rows),
            "",
            "## Connection lifecycle",
            "",
            "- Liveness check every 25 seconds; timeout after 60 seconds.",
            "- Client reconnects with exponential backoff.",
            "- Subscription authorization is evaluated per application and recruiter assignment.",
            "",
            "## Server event linkage",
            "",
            "- Server event frame and at-least-once delivery semantics are defined in [04_Response.md](./04_Response.md).",
            "",
            "## Contract source",
            "",
            "> " + api.processing,
            "",
            "## Ví dụ client message",
            "",
            "N/A — a complete physical WebSocket frame schema is not sufficiently source-confirmed for this Draft DD.",
            "",
            appendix("03_Request.md", "1.Request"),
        ]
    )


def response(api: Api) -> str:
    if api.transport == "websocket":
        return websocket_response(api)
    response_rows = [
        (1, q("success"), "Success", q("success"), q("boolean"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "Fixed by branch", "N/A", "BD §2.1 envelope."),
        (2, q("businessCode"), "Business code", q("businessCode"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "Source-confirmed or SOURCE_REQUIRED", "N/A", "BD §2.1 envelope."),
        (3, q("message"), "Safe message", q("message"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "Safe localized message", "N/A", "BD §2.1 envelope."),
        (4, q("data"), "Response data", q("data"), q("object | array | null"), "Yes", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", output_phrase(api), "SOURCE_REQUIRED for nested shape", "Catalog output phrase retained below."),
        (5, q("meta"), "Metadata", q("meta"), q("object"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "Pagination/field errors when applicable", "{}", "BD §2.1 envelope."),
        (6, q("traceId"), "Trace ID", q("traceId"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "Trace propagation/generation", "N/A", "BD §2.1 envelope."),
    ]
    codes = error_codes(api)
    success_json = {
        "success": True,
        "businessCode": "<SOURCE_REQUIRED>",
        "message": "<SOURCE_REQUIRED>",
        "data": {},
        "meta": {},
        "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10",
    }
    error_json = {
        "success": False,
        "businessCode": codes[0] if codes else "<SOURCE_REQUIRED>",
        "message": "<SOURCE_REQUIRED>",
        "data": None,
        "meta": {"fieldErrors": []},
        "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10",
    }
    return "\n".join(
        [
            fm(api, "Response", 4, "2.Response"),
            "",
            "# Response",
            "",
            "## Format",
            "",
            table(["Thuộc tính", "Giá trị"], [("Format", q("JSON")), ("Character encoding", q("UTF-8")), ("Content-Type", q("application/json; charset=utf-8")), ("HTTP status", "Source-confirmed by branch; it is not a JSON response field.")]),
            "",
            "## Response fields",
            "",
            table(["No", "Path", "Logical name", "Physical name", "Type", "Nullable", "Source table", "Source column", "Source step", "Transform", "Null/empty/omit rule", "Remarks"], response_rows),
            "",
            "## Output contract from API catalog",
            "",
            "> " + output_phrase(api),
            "",
            "## Ví dụ thành công",
            "",
            FENCE + "json",
            json.dumps(success_json, ensure_ascii=False, indent=2),
            FENCE,
            "",
            "## Ví dụ lỗi",
            "",
            FENCE + "json",
            json.dumps(error_json, ensure_ascii=False, indent=2),
            FENCE,
            "",
            appendix("04_Response.md", "2.Response"),
        ]
    )


def websocket_response(api: Api) -> str:
    rows = [
        (1, q("type"), "Event type", q("type"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "DIRECT protocol field", "N/A", "Server event category."),
        (2, q("eventId"), "Event ID", q("eventId"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "DIRECT protocol field", "N/A", "At-least-once delivery deduplication key."),
        (3, q("sequence"), "Sequence", q("sequence"), q("integer"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "DIRECT protocol field", "N/A", "Gap detection / REST history reload."),
        (4, q("occurredAt"), "Occurred at", q("occurredAt"), q("string"), "No", "N/A", "N/A", "[S06](./05_Data_Mapping.md#s06)", "DIRECT protocol field", "N/A", "Event timestamp."),
    ]
    event_json = {
        "type": "message.created",
        "eventId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10",
        "sequence": 1,
        "occurredAt": "2026-08-14T00:00:00Z",
    }
    return "\n".join(
        [
            fm(api, "Response", 4, "2.Response"),
            "",
            "# Response",
            "",
            "## Format",
            "",
            table(["Thuộc tính", "Giá trị"], [("Transport", q("WebSocket")), ("Endpoint", q(api.endpoint)), ("REST envelope", "N/A — WebSocket frames are not a REST envelope.")]),
            "",
            "## Server event fields",
            "",
            table(["No", "Path", "Logical name", "Physical name", "Type", "Nullable", "Source table", "Source column", "Source step", "Transform", "Null/empty/omit rule", "Remarks"], rows),
            "",
            "## Server event types",
            "",
            "- " + q("message.created") + ".",
            "- " + q("message.tombstoned") + ".",
            "- " + q("receipt.updated") + ".",
            "- " + q("conversation.read_only") + ".",
            "- " + q("interview.changed") + ".",
            "- " + q("notification.created") + ".",
            "",
            "## Ví dụ server event",
            "",
            FENCE + "json",
            json.dumps(event_json, ensure_ascii=False, indent=2),
            FENCE,
            "",
            appendix("04_Response.md", "2.Response"),
        ]
    )


def request_matrix(api: Api) -> list[tuple[object, ...]]:
    if api.transport == "websocket":
        return [
            ("Handshake token transport", "API catalog", "S01/S02", "Secure subprotocol or first authentication frame", "Authenticate connection", "Connection establishment", "N/A", "Physical carrier remains SOURCE_REQUIRED."),
            (q("type"), "API catalog", "S01/S03", "DIRECT value subscribe", "Subscription dispatch", "Per client message", "N/A", "DIRECT named field/value."),
            (q("applicationId"), "API catalog", "S01/S03", "Authorization per application", "Subscription lookup", "Per client message", "N/A", "Type/requiredness remains SOURCE_REQUIRED."),
            (q("lastSequence"), "API catalog", "S01/S03", "Gap-detection input", "Resume/reload decision", "Per client message", "N/A", "Type/requiredness remains SOURCE_REQUIRED."),
        ]
    rows: list[tuple[object, ...]] = []
    for header in headers(api):
        rows.append((header[2], "BD global/endpoint convention", "S01/S02", "As stated", "Authentication/idempotency/concurrency", "N/A", "N/A", "N/A"))
    for item in path_params(api):
        rows.append((q(item), "Endpoint URI", "S01", "Path parsing", "Resource lookup", "N/A", "N/A", "N/A"))
    physical, gaps = inputs(api)
    for item in physical:
        rows.append((q(item), "API catalog", "S01/S03", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "N/A", "N/A", "Physical key direct; location/type not locked."))
    for item in gaps:
        rows.append((item, "API catalog", "S01/S03", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "N/A", "N/A", "Not materialized as a physical key."))
    return rows or [("N/A", "API catalog", "S01", "N/A", "N/A", "N/A", "N/A", "No independently materialized request item.")]


def data_mapping(api: Api, tables: dict[str, Table]) -> str:
    mentioned = refs(api, tables)
    writing = has_write(api)
    query_rows = [(q("Q" + str(i).zfill(2)), "SOURCE_REQUIRED — complete query contract not specified.", "SOURCE_REQUIRED", q(item.name), "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "S04") for i, item in enumerate(mentioned, start=1)]
    if not query_rows:
        query_rows = [(q("Q01"), "N/A — no source-confirmed physical query.", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "S04")]
    if api.operation_class in {"read_candidate", "realtime"}:
        mutation_rows = [("N/A", "N/A — READ-ONLY API", "N/A", "N/A", "N/A", "N/A", "N/A", "[07_table.md](./07_table.md)", "N/A", "N/A")]
    elif mentioned and writing:
        op = operation(api)
        mutation_rows = [
            (q("M" + str(i).zfill(2)), op, q(item.name), "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "[" + str(7 + i - 1).zfill(2) + "_" + item.name + "_" + op.lower() + ".md](./" + str(7 + i - 1).zfill(2) + "_" + item.name + "_" + op.lower() + ".md)", "TBD unless source says TX", "SOURCE_REQUIRED")
            for i, item in enumerate(mentioned, start=1)
        ]
    else:
        mutation_rows = [(q("M01"), "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "[07_source_required_mutation.md](./07_source_required_mutation.md)", "TBD", "Mutation candidate lacks confirmed physical target.")]
    response_rows = [
        (q("success"), q("boolean"), "Fixed branch", "N/A", "S06", "Success/error branch", "N/A", "BD §2.1"),
        (q("businessCode"), q("string"), "Endpoint/global contract", "N/A", "S06", "DIRECT or SOURCE_REQUIRED", "N/A", "No new code."),
        (q("message"), q("string"), "Safe response text", "N/A", "S06", "Localized safe text", "N/A", "BD §2.1"),
        (q("data"), q("object | array | null"), "Endpoint output phrase", "N/A", "S06", output_phrase(api), "SOURCE_REQUIRED for nested shape", "API catalog"),
        (q("meta"), q("object"), "Envelope metadata", "N/A", "S06", "Pagination/field errors only when applicable", "{}", "BD §2.1"),
        (q("traceId"), q("string"), "Trace propagation/generation", "N/A", "S06", "DIRECT global convention", "N/A", "BD §2.1"),
    ]
    if api.transport == "websocket":
        response_rows = [(q(item), q(kind), "Protocol", "N/A", "S06", "DIRECT", "N/A", "API-INT-011") for item, kind in [("type", "string"), ("eventId", "string"), ("sequence", "integer"), ("occurredAt", "string")]]
    transaction = "BEGIN/COMMIT/ROLLBACK are bounded by the source-confirmed transaction; external delivery occurs after commit where outbox/saga is stated." if "tx:" in api.processing.lower() else ("TBD — this mutation candidate lacks a complete transaction boundary at endpoint detail." if api.operation_class == "mutation_candidate" else "N/A — no source-confirmed business mutation.")
    auth = "Apply mTLS, service JWT audience/signature and replay protection." if api.transport == "internal_http" else ("Apply WebSocket authentication and subscription authorization." if api.transport == "websocket" else "Apply public API authentication, account-state, permission, tenant and ownership rules from BD §2.2.")
    response_text = "Map only protocol fields and at-least-once delivery semantics; clients deduplicate and reload REST history after a sequence gap." if api.transport == "websocket" else "Map the standard BD envelope in [04_Response.md](./04_Response.md); unnamed nested data remains SOURCE_REQUIRED."
    return "\n".join(
        [
            fm(api, "Data Mapping", 5, "3. Data mapping"),
            "",
            "# Data Mapping",
            "",
            "## Traceability matrices",
            "",
            "### Request Usage Matrix",
            "",
            table(["Request field/item", "Nguồn", "Data Mapping step", "Validate", "SQL/Mutation usage", "Branch/Loop", "Response usage", "Gap"], request_matrix(api)),
            "",
            "### Query Matrix",
            "",
            table(["Query ID", "Mục đích", "Type", "Base table/view", "Alias", "Columns", "JOIN", "WHERE", "GROUP/HAVING", "ORDER", "Pagination", "Result variable", "Branch"], query_rows),
            "",
            "### Mutation Matrix",
            "",
            table(["Mutation ID", "Operation", "Target table", "Record condition", "Fields", "Value sources", "Audit", "Mapping file", "Transaction", "Failure behavior"], mutation_rows),
            "",
            "### Response Source Matrix",
            "",
            table(["Response field", "Type", "Source type", "Table/column or generator", "Data Mapping step", "Transform", "Null/empty rule", "Gap"], response_rows),
            "",
            "## Flow xử lý data",
            "",
            '<a id="s01"></a>',
            "### S01. Get request/protocol data",
            "",
            "- Receive only items documented in [03_Request.md](./03_Request.md).",
            "- Do not convert unnamed source phrases into JSON keys.",
            "",
            '<a id="s02"></a>',
            "### S02. Authentication and authorization",
            "",
            "- Actor/authorization source: " + api.actor + ".",
            "- " + auth,
            "",
            '<a id="s03"></a>',
            "### S03. Validate source-confirmed input",
            "",
            "- Validate only constraints named by endpoint/global contract; absent physical schema remains " + q("SOURCE_REQUIRED") + ".",
            "- Endpoint input contract: " + api.input_contract + ".",
            "",
            '<a id="s04"></a>',
            "### S04. Execute source-defined processing",
            "",
            "> " + api.processing,
            "",
            "- Operations/observability contract: " + api.operations,
            "",
            '<a id="s05"></a>',
            "### S05. Idempotency, transaction and failure handling",
            "",
            "- " + transaction,
            "- Refer to [06_Error.md](./06_Error.md); never return stack traces, SQL, secrets or tokens.",
            "",
            '<a id="s06"></a>',
            "### S06. Map response/protocol output",
            "",
            "- " + response_text,
            "",
            appendix("05_Data_Mapping.md", "3. Data mapping"),
        ]
    )


def errors(api: Api) -> str:
    rows = []
    for number, item in enumerate(error_codes(api), start=1):
        rows.append((number, "Endpoint business/error code", "DIRECT", q(item), "As specified by API catalog.", q(HTTP_BY_CODE.get(item, "SOURCE_REQUIRED")), q(item), "N/A — no legacy error-message ID in BD.", "[S05](./05_Data_Mapping.md#s05)", "TBD" if api.operation_class == "mutation_candidate" else "No", q("docs/BD/04_DAC_TA_API.md:L" + str(api.source_line))))
    if not rows:
        rows = [(1, "SOURCE_REQUIRED", "N/A", "N/A", "Endpoint row does not name a dedicated business code.", "SOURCE_REQUIRED", "SOURCE_REQUIRED", "N/A", "[S05](./05_Data_Mapping.md#s05)", "TBD" if api.operation_class == "mutation_candidate" else "No", "Global failure/safety rules still apply.")]
    return "\n".join(
        [
            fm(api, "Error", 6, "4.Error"),
            "",
            "# Error",
            "",
            "## Giải thích",
            "",
            "Codes are copied only from endpoint/error catalog. HTTP status is source-confirmed only when a source maps it; otherwise it is SOURCE_REQUIRED.",
            "",
            "## Error cases",
            "",
            table(["No", "Category", "Verify check", "Item", "Condition", "HTTP status", "Error code", "Error message ID", "Data Mapping reference", "Rollback", "Remarks"], rows),
            "",
            "## Global safety rules",
            "",
            "- Do not disclose tenant/resource existence across unauthorized scope.",
            "- Do not return stack trace, raw SQL, passwords, tokens, secrets or unsafe PII.",
            "",
            appendix("06_Error.md", "4.Error"),
        ]
    )


def mapping(api: Api, item: Table | None, order: int, op: str) -> str:
    filename = str(order).zfill(2) + "_" + item.name + "_" + op.lower() + ".md" if item else ("07_table.md" if api.operation_class in {"read_candidate", "realtime"} else "07_source_required_mutation.md")
    if item is None:
        read_only = api.operation_class in {"read_candidate", "realtime"}
        return "\n".join(
            [
                fm(api, "Định nghĩa table", order, "table"),
                "",
                "# Định nghĩa table",
                "",
                "## Table metadata",
                "",
                table(["Thuộc tính", "Giá trị"], [("Physical table", "N/A" if read_only else q("SOURCE_REQUIRED")), ("Logical table", "N/A — READ-ONLY API" if read_only else "SOURCE_REQUIRED"), ("Operation", "N/A — READ-ONLY API" if read_only else q("SOURCE_REQUIRED")), ("Data Mapping step", "[S05](./05_Data_Mapping.md#s05)")]),
                "",
                "## Mapping status",
                "",
                "N/A — READ-ONLY API." if read_only else "SOURCE_REQUIRED — mutation candidate does not identify a physical target table or column mapping.",
                "",
                appendix(filename, "table"),
            ]
        )
    rows = [(number, q(column), "Schema field explicitly named in BD", q("SOURCE_REQUIRED"), "No value source or operation mapping is named by this endpoint row.") for number, column in enumerate(item.columns, start=1)]
    if not rows:
        rows = [(1, q("SOURCE_REQUIRED"), "No individual column named in source", q("SOURCE_REQUIRED"), "Do not invent a column mapping.")]
    return "\n".join(
        [
            fm(api, "Định nghĩa table", order, "table"),
            "",
            "# Định nghĩa table",
            "",
            "## Table metadata",
            "",
            table(["Thuộc tính", "Giá trị"], [("Physical table", q(item.name)), ("Logical table", q(item.table_id)), ("Operation", q(op)), ("Data Mapping step", "[S05](./05_Data_Mapping.md#s05)")]),
            "",
            "## Mutation mapping",
            "",
            "> SOURCE_REQUIRED — catalog names this table in a mutation flow but does not provide per-column setting/value mapping. This file deliberately does not invent one.",
            "",
            table(["No", "Physical column", "Logical name", "Type", "Remarks"], rows),
            "",
            "## Schema source",
            "",
            "- " + link("03_THIET_KE_CO_SO_DU_LIEU.md", local_source("03_THIET_KE_CO_SO_DU_LIEU.md")) + ": " + q("L" + str(item.source_line)) + ".",
            "- Endpoint source: " + q("docs/BD/04_DAC_TA_API.md:L" + str(api.source_line)) + ".",
            "",
            appendix(filename, "table"),
        ]
    )


def write_api(api: Api, output: Path, tables: dict[str, Table], today: str) -> None:
    destination = api_path(api, output)
    core = {
        "00_Cover.md": cover(api, today),
        "01_Lich_su.md": history(api, today),
        "02_Overview.md": overview(api, tables),
        "03_Request.md": request(api),
        "04_Response.md": response(api),
        "05_Data_Mapping.md": data_mapping(api, tables),
        "06_Error.md": errors(api),
    }
    for name, content in core.items():
        write(destination / name, content)
    mentioned = refs(api, tables)
    if api.operation_class in {"read_candidate", "realtime"}:
        write(destination / "07_table.md", mapping(api, None, 7, "N/A"))
    elif mentioned and has_write(api):
        op = operation(api)
        for number, item in enumerate(mentioned, start=7):
            write(destination / (str(number).zfill(2) + "_" + item.name + "_" + op.lower() + ".md"), mapping(api, item, number, op))
    else:
        write(destination / "07_source_required_mutation.md", mapping(api, None, 7, "SOURCE_REQUIRED"))


def api_link(api: Api, filename: str = "00_Cover.md") -> str:
    return link(api.api_id, DOMAINS[api.domain][0] + "/" + api.folder + "/" + filename)


def source_report() -> str:
    bd_rows = [(q(str(path.relative_to(ROOT))), lines(path), checksum(path), "In scope — current working-tree source.") for path in sorted(BD.glob("*.md"))]
    template_rows = [(q(str(path.relative_to(ROOT))), lines(path), checksum(path), "Validated DD template baseline.") for path in sorted(TEMPLATE.glob("*.md"))]
    return "\n".join(
        [
            "# Source Read Report",
            "",
            "## Source precedence",
            "",
            "1. docs/BD/01_TONG_QUAN_DU_AN.md — business decisions.",
            "2. docs/BD/04_DAC_TA_API.md — API/realtime/internal contract and business codes.",
            "3. docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md — physical data terminology.",
            "4. docs/BD/02_BIEU_DO_HE_THONG.md — flow and concurrency explanation.",
            "5. docs/BD/05_DAC_TA_MAN_HINH.md — screen coverage only.",
            "6. docs/BD/06_BAO_CAO_RAO_SOAT_LOGIC.md — official gaps, not permission to fill them.",
            "",
            "## Basic Design sources",
            "",
            table(["Source", "Lines", "SHA-256", "Read status"], bd_rows),
            "",
            "## Markdown template fingerprint",
            "",
            table(["Template file", "Lines", "SHA-256", "Status"], template_rows),
            "",
            "## Working-tree note",
            "",
            "- Hashes describe the current local BD files, including user-owned worktree changes.",
            "- Historical DD directories are neither restored nor used as source of truth.",
        ]
    )


def open_questions() -> str:
    result = ["# Open Questions", "", "Only source-backed unresolved issues are recorded. This document does not propose new API IDs, routes, tables, columns, enums, roles or business codes.", ""]
    for gap_id, title, domain, detail, evidence in GAPS:
        result.extend(
            [
                '<a id="' + gap_id.lower() + '"></a>',
                "## " + gap_id + " — " + title,
                "",
                "- Domain: " + q(domain) + ".",
                "- Evidence: " + q(evidence) + ".",
                "- Gap: " + detail,
                "- Handling: affected DDs remain " + q("Draft — Needs Confirmation") + " and use " + q("SOURCE_REQUIRED") + " or " + q("TBD") + ".",
                "",
            ]
        )
    result.extend(
        [
            "## Unapproved screen-derived candidates",
            "",
            "- No DD is created for a screen surface without an approved API ID and route.",
            "",
            "### Operations read/approval counterparts",
            "",
            "- SCR-OPS-014 requires a support queue, internal-note and resolution-event surface while the catalog names only an existing support detail API (docs/BD/05_DAC_TA_MAN_HINH.md:L188).",
            "- SCR-OPS-018 requires verification detail/read context while the catalog names a list and a decision action (docs/BD/05_DAC_TA_MAN_HINH.md:L191-L192).",
            "- SCR-OPS-020 requires refund queue/detail and reject/decision context beyond the currently named request and approve actions (docs/BD/05_DAC_TA_MAN_HINH.md:L194).",
            "- SCR-OPS-022 and SCR-OPS-023 require runtime/policy/evaluation read and activation context beyond mutation-oriented AI catalog entries (docs/BD/05_DAC_TA_MAN_HINH.md:L196-L197).",
            "- SCR-OPS-025 requires break-glass status and second-approval context beyond session creation (docs/BD/05_DAC_TA_MAN_HINH.md:L199).",
            "",
            "### Other screen read surfaces requiring reconciliation",
            "",
            "- University affiliation invitation/list, cohort/program/distribution/partnership/referral reads and outcome reporting have screen coverage but must use only approved catalog contracts (docs/BD/05_DAC_TA_MAN_HINH.md:L159-L162).",
            "- Candidate and enterprise views describe CV revision, job revision/history, interview detail and payment/refund-list reads that must not be converted into DDs without an approved API contract (docs/BD/05_DAC_TA_MAN_HINH.md:L127-L148).",
            "- Study support/content screens may require draft/version reads; those remain screen requirements until the API catalog approves a contract (docs/BD/05_DAC_TA_MAN_HINH.md:L187-L190).",
        ]
    )
    return "\n".join(result)


def business_codes() -> str:
    return "\n".join(
        [
            "# Business Code Delta",
            "",
            "## Result",
            "",
            "- No business code was added, renamed or made canonical by DD generation.",
            "- DD error rows reproduce endpoint/catalog codes only; absent mappings remain SOURCE_REQUIRED.",
            "- Template legacy error-message IDs are not used because the current BD contract does not define them.",
        ]
    )


def catalog_report(apis: list[Api]) -> str:
    rows = [(api_link(api), q(api.domain), q(api.transport), q(api.method), q(api.endpoint), q("Draft — Needs Confirmation"), q("docs/BD/04_DAC_TA_API.md:L" + str(api.source_line))) for api in apis]
    return "\n".join(["# API Catalog — Study2Work V1-PILOT", "", "This catalog is generated from current endpoint rows. Event contracts are linked from DD mapping but have no standalone DD folder.", "", table(["API", "Domain", "Transport", "Method", "Endpoint", "Status", "Primary source"], rows)])


def coverage(apis: list[Api], tables: dict[str, Table]) -> str:
    rows = []
    for api in apis:
        mapping_name = "07_table.md" if api.operation_class in {"read_candidate", "realtime"} else ("07+ mutation mapping" if refs(api, tables) and has_write(api) else "07_source_required_mutation.md")
        rows.append((q(api.api_id), q(api.domain), q(api.transport), q(api.method), q(api.endpoint), link(api.folder, DOMAINS[api.domain][0] + "/" + api.folder + "/00_Cover.md"), mapping_name, ", ".join(gap_ids(api)) if gap_ids(api) else "SOURCE_REQUIRED field-level detail", q("docs/BD/04_DAC_TA_API.md:L" + str(api.source_line))))
    return "\n".join(["# Coverage Matrix", "", "Checkpoint order: IAM → Study → Work → University → Payment → AI → Operations → Integration/WebSocket.", "", table(["API ID", "Domain", "Transport", "Method", "Endpoint", "DD folder", "DB mapping", "Main gap", "Source"], rows)])


def checkpoints(apis: list[Api], output: Path) -> None:
    for domain in DOMAIN_ORDER:
        selected = [api for api in apis if api.domain == domain]
        rows = [(link(api.api_id, api.folder + "/00_Cover.md"), q(api.method), q(api.endpoint), q(api.transport), q("Draft — Needs Confirmation"), ", ".join(gap_ids(api)) if gap_ids(api) else "SOURCE_REQUIRED field-level detail") for api in selected]
        content = "\n".join(
            [
                "# " + DOMAINS[domain][1] + " checkpoint",
                "",
                "- APIs in checkpoint: " + str(len(selected)) + ".",
                "- Status: all DDs remain Draft until missing contract/schema decisions are supplied.",
                "- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.",
                "- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).",
                "",
                table(["API", "Method", "Endpoint", "Transport", "Status", "Main gap"], rows),
            ]
        )
        write(output / DOMAINS[domain][0] / "00_CHECKPOINT.md", content)


def plan_result(apis: list[Api]) -> str:
    rows = [(q(domain), len([api for api in apis if api.domain == domain]), "Draft — Needs Confirmation", link(DOMAINS[domain][0] + "/00_CHECKPOINT.md", DOMAINS[domain][0] + "/00_CHECKPOINT.md")) for domain in DOMAIN_ORDER]
    return "\n".join(
        [
            "# Plan Result",
            "",
            "## Overall status",
            "",
            q("PARTIALLY COMPLETED — SOURCE GAPS PRESERVED"),
            "",
            "All 212 approved API IDs have a DD folder. The batch is not Final because canonical BD explicitly contains unresolved contract/data-model decisions.",
            "",
            "## Domain results",
            "",
            table(["Domain", "API count", "Status", "Checkpoint"], rows),
            "",
            "## Deliverables",
            "",
            "- 212 API DD folders.",
            "- Root catalog, coverage matrix, source report, open questions, business-code delta and verification report.",
            "- ZIP package after technical validation.",
        ]
    )


def readme() -> str:
    return "\n".join(
        [
            "# Study2Work V1-PILOT API Detail Design",
            "",
            "- [API catalog](./API_CATALOG.md)",
            "- [Coverage matrix](./COVERAGE_MATRIX.md)",
            "- [Source read report](./SOURCE_READ_REPORT.md)",
            "- [Open questions](./OPEN_QUESTIONS.md)",
            "- [Business code delta](./BUSINESS_CODE_DELTA.md)",
            "- [Verification report](./VERIFICATION_REPORT.md)",
            "- [Plan result](./PLAN_RESULT.md)",
            "",
            "Each approved API has one folder under its domain checkpoint. Content derives from the current Basic Design, not historical DD files.",
        ]
    )


def parse_fm(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def json_blocks(text: str) -> list[str]:
    return re.findall(re.escape(FENCE) + r"json\s*\n(.*?)" + re.escape(FENCE), text, flags=re.DOTALL)


def md_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def table_width(line: str) -> int:
    return len(re.split(r"(?<!\\)\|", line.strip())[1:-1])


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and table_width(stripped) > 0


def is_table_separator(line: str) -> bool:
    if not is_table_row(line):
        return False
    cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return bool(cells) and all(re.fullmatch(r"\s*:?-{3,}:?\s*", item) for item in cells)


def validate_markup(document: Path, errors: list[str]) -> None:
    text = document.read_text(encoding="utf-8")
    if text.count(FENCE) % 2:
        errors.append(str(document) + " has unclosed code fence")
    for block in json_blocks(text):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(str(document) + " invalid JSON: " + str(exc))
    document_lines = text.splitlines()
    for line_number, line in enumerate(document_lines):
        if not is_table_separator(line):
            continue
        if line_number == 0 or not is_table_row(document_lines[line_number - 1]):
            errors.append(str(document) + " has a table separator without header")
            continue
        expected_width = table_width(document_lines[line_number - 1])
        if table_width(line) != expected_width:
            errors.append(str(document) + " has a table separator with mismatched width")
        row_number = line_number + 1
        while row_number < len(document_lines) and is_table_row(document_lines[row_number]):
            if table_width(document_lines[row_number]) != expected_width:
                errors.append(str(document) + " has a table row with mismatched width")
            row_number += 1
    for target in md_links(text):
        if "://" in target:
            continue
        file_target, marker, fragment = target.partition("#")
        destination = document.resolve() if not file_target else (document.parent / file_target).resolve()
        if not destination.exists():
            errors.append(str(document) + " has broken link " + target)
        elif not str(destination).startswith(str(ROOT.resolve())):
            errors.append(str(document) + " link escapes repo " + target)
        elif marker:
            linked_text = destination.read_text(encoding="utf-8")
            anchor = r'<a\s+id=["\']' + re.escape(fragment) + r'["\']></a>'
            if not re.search(anchor, linked_text):
                errors.append(str(document) + " has broken anchor " + target)


def api_directories(output: Path) -> list[Path]:
    return sorted({item.parent for item in output.rglob("00_Cover.md")})


def validate(output: Path, apis: list[Api], zip_path: Path | None = None) -> dict[str, object]:
    errors: list[str] = []
    expected = {api.api_id: api for api in apis}
    seen: dict[str, Path] = {}
    core = ["00_Cover.md", "01_Lich_su.md", "02_Overview.md", "03_Request.md", "04_Response.md", "05_Data_Mapping.md", "06_Error.md"]
    for directory in api_directories(output):
        cover = directory / "00_Cover.md"
        info = parse_fm(cover.read_text(encoding="utf-8"))
        api_id = info.get("dd_id")
        if not api_id:
            errors.append(str(cover) + " missing dd_id")
            continue
        if api_id in seen:
            errors.append("duplicate DD ID " + api_id)
        seen[api_id] = directory
        api = expected.get(api_id)
        if api is None:
            errors.append("unexpected API ID " + api_id)
            continue
        if directory.name != api.folder or directory.parent.name != DOMAINS[api.domain][0]:
            errors.append(str(directory) + " has noncanonical location")
        for name in core:
            if not (directory / name).is_file():
                errors.append(str(directory) + " missing " + name)
        if not any(item.name.startswith("07_") for item in directory.glob("*.md")):
            errors.append(str(directory) + " has no 07+ mapping")
        for document in directory.glob("*.md"):
            text = document.read_text(encoding="utf-8")
            info = parse_fm(text)
            prefix = re.match(r"(\d{2})_", document.name)
            if prefix and info.get("order") != str(int(prefix.group(1))):
                errors.append(str(document) + " has mismatched front matter order")
            if info.get("dd_id") != api_id:
                errors.append(str(document) + " has mismatched dd_id")
            validate_markup(document, errors)
        response_text = (directory / "04_Response.md").read_text(encoding="utf-8")
        mapping_text = (directory / "05_Data_Mapping.md").read_text(encoding="utf-8")
        fields = ("type", "eventId", "sequence", "occurredAt") if api.transport == "websocket" else ("success", "businessCode", "message", "data", "meta", "traceId")
        for field in fields:
            if q(field) not in response_text:
                errors.append(str(directory / "04_Response.md") + " missing " + field)
        for name in ("Request Usage Matrix", "Query Matrix", "Mutation Matrix", "Response Source Matrix"):
            if name not in mapping_text:
                errors.append(str(directory / "05_Data_Mapping.md") + " missing " + name)
        if api.operation_class in {"read_candidate", "realtime"}:
            target = directory / "07_table.md"
            if not target.is_file() or "N/A — READ-ONLY API" not in target.read_text(encoding="utf-8"):
                errors.append(str(directory) + " missing read-only mapping")
        elif api.operation_class == "mutation_candidate" and "TBD — this mutation candidate" not in mapping_text and "BEGIN/COMMIT/ROLLBACK" not in mapping_text:
            errors.append(str(directory / "05_Data_Mapping.md") + " lacks transaction/TBD statement")
    missing = sorted(set(expected) - set(seen))
    if missing:
        errors.append("missing DDs: " + ", ".join(missing))
    for document in list(output.glob("*.md")) + list(output.glob("*/00_CHECKPOINT.md")):
        validate_markup(document, errors)
    root_reports = ["README.md", "API_CATALOG.md", "COVERAGE_MATRIX.md", "SOURCE_READ_REPORT.md", "OPEN_QUESTIONS.md", "BUSINESS_CODE_DELTA.md", "PLAN_RESULT.md"]
    if zip_path:
        root_reports.append("VERIFICATION_REPORT.md")
    for name in root_reports:
        if not (output / name).is_file():
            errors.append("missing root report " + name)
    coverage_path = output / "COVERAGE_MATRIX.md"
    if coverage_path.is_file():
        count = sum(1 for line in coverage_path.read_text(encoding="utf-8").splitlines() if line.startswith("| " + T + "API-"))
        if count != 212:
            errors.append("coverage matrix has " + str(count) + " API rows")
    if zip_path:
        if not zip_path.is_file():
            errors.append("missing ZIP " + str(zip_path))
        else:
            with zipfile.ZipFile(zip_path) as archive:
                bad = archive.testzip()
                if bad:
                    errors.append("ZIP corrupt at " + bad)
                expected_members = {
                    output.name + "/" + str(path.relative_to(output))
                    for path in output.rglob("*")
                    if path.is_file()
                }
                archive_members = set(archive.namelist())
                if expected_members != archive_members:
                    errors.append("ZIP file set does not match generated output")
    return {"status": "PASS" if not errors else "FAIL", "api_count_expected": len(apis), "api_count_found": len(seen), "errors": errors}


def verification(result: dict[str, object], zip_path: Path) -> str:
    errors = result["errors"]
    try:
        zip_display = str(zip_path.relative_to(ROOT))
    except ValueError:
        zip_display = str(zip_path)
    rows = [
        ("Expected API IDs", result["api_count_expected"]),
        ("Generated API folders", result["api_count_found"]),
        ("Required file structure", "PASS" if not errors else "See findings"),
        ("JSON examples", "PASS" if not errors else "See findings"),
        ("Relative links", "PASS" if not errors else "See findings"),
        ("ZIP package", zip_display),
    ]
    content = [
        "# Verification Report",
        "",
        "## Overall result",
        "",
        q(result["status"]),
        "",
        table(["Check", "Result"], rows),
        "",
        "## Source defects preserved",
        "",
        "- Field-level request/response schemas, DB column values and official model gaps remain SOURCE_REQUIRED or TBD; none were silently invented.",
        "- Legacy template response fields are replaced by the current BD envelope.",
        "",
        "## Findings",
        "",
    ]
    if errors:
        content.extend("- " + str(item) for item in errors)
    else:
        content.append("- No coverage, file-structure, JSON, link or ZIP failure found.")
    return "\n".join(content)


def reports(output: Path, apis: list[Api], tables: dict[str, Table]) -> None:
    write(output / "README.md", readme())
    write(output / "API_CATALOG.md", catalog_report(apis))
    write(output / "COVERAGE_MATRIX.md", coverage(apis, tables))
    write(output / "SOURCE_READ_REPORT.md", source_report())
    write(output / "OPEN_QUESTIONS.md", open_questions())
    write(output / "BUSINESS_CODE_DELTA.md", business_codes())
    write(output / "PLAN_RESULT.md", plan_result(apis))
    checkpoints(apis, output)


def package(output: Path, zip_path: Path) -> None:
    if zip_path.exists():
        raise FileExistsError("refusing to overwrite ZIP " + str(zip_path))
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                archive.write(path, output.name + "/" + str(path.relative_to(output)))


def generate(output: Path, zip_path: Path, today: str) -> dict[str, object]:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("refusing to overwrite nonempty output " + str(output))
    for path in list(BD.glob("*.md")) + list(TEMPLATE.glob("*.md")):
        if not path.is_file():
            raise FileNotFoundError(path)
    apis = catalog()
    tables = table_catalog()
    for api in apis:
        write_api(api, output, tables, today)
    reports(output, apis, tables)
    preliminary = {"status": "PENDING", "api_count_expected": len(apis), "api_count_found": len(apis), "errors": []}
    write(output / "VERIFICATION_REPORT.md", verification(preliminary, zip_path))
    interim = validate(output, apis)
    if interim["errors"]:
        write(output / "VERIFICATION_REPORT.md", verification(interim, zip_path))
        raise RuntimeError("generation validation failed:\n" + "\n".join(interim["errors"]))
    write(output / "VERIFICATION_REPORT.md", verification(interim, zip_path))
    package(output, zip_path)
    final = validate(output, apis, zip_path)
    if final["errors"]:
        write(output / "VERIFICATION_REPORT.md", verification(final, zip_path))
        raise RuntimeError("final validation failed:\n" + "\n".join(final["errors"]))
    return final


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--zip", dest="zip_path", type=Path, default=ZIP)
    parser.add_argument("--created-date", default=dt.date.today().isoformat())
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        apis = catalog()
        if args.validate_only:
            result = validate(args.output, apis, args.zip_path)
        else:
            result = generate(args.output, args.zip_path, args.created_date)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
