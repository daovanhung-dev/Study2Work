# Worklog Index

Worklog ghi lại trace từ BD/DD/checklist/skill đến code, test, bug và follow-up. Không tạo worklog giả khi chưa có phiên coding/test thực tế.

## Session Numbering

| Field | Value |
|---|---|
| Next session | `0002` |
| Path format | `docs/worklog/YYYY-MM/<SESSION_NO>_<TASK_SLUG>.md` |
| Example | `docs/worklog/2026-07/0001_auth_register_dd.md` |
| Last updated | `2026-07-01` |

## Read Rule At Session Start

1. Chọn tối đa 10 worklog gần nhất theo bảng index.
2. Chỉ mở nội dung đầy đủ tối đa 5 worklog liên quan trực tiếp đến module/bug hiện tại.
3. Ưu tiên worklog có risk, failed test, open question hoặc cùng module.

## Worklog Table

| Session | Date | Module | Task slug | Status | Risk | Worklog | Summary |
|---|---|---|---|---|---|---|---|
| `0001` | 2026-07-01 | `GLOBAL_DOCS/DIAGRAMS` | `study_diagrams_refresh` | `DONE` | Docker daemon unavailable; Java PlantUML fallback passed | `docs/worklog/2026-07/0001_study_diagrams_refresh.md` | Refreshed Study-only Use Case, Activity, Class and Sequence diagram pack from canonical BD. |

## Required Worklog Template

```md
# Worklog — <SESSION_NO> <TASK_SLUG>

| Field | Value |
|---|---|
| Session | `<SESSION_NO>` |
| Time | `YYYY-MM-DD HH:mm TZ` |
| Module | `<MODULE_CODE>` |
| Feature/function | `<FEATURE/FUNCTION>` |
| Status | `<STATUS>` |

## Mục Tiêu

<Goal of this session.>

## Context Đã Đọc

- BD: `<link>`
- DD: `<link>`
- Checklist: `<link>`
- Skill: `<link or none>`

## File Đã Tạo Hoặc Sửa

| Path | Action | Note |
|---|---|---|
| `<path>` | `<created/modified>` | `<note>` |

## Logic Đã Thay Đổi

<Short implementation summary.>

## Test Đã Chạy

| Command/check | Result | Evidence |
|---|---|---|
| `<command>` | `<result>` | `<output/link>` |

## Bug Phát Hiện

| ID | Status | Description | Link |
|---|---|---|---|
| `<BUG-ID>` | `<status>` | `<description>` | `<link>` |

## Rủi Ro Hoặc Chưa Xác Minh

- `<risk/open question>`

## Việc Tiếp Theo

- `<next task>`

## Commit Message Đề Xuất

`<type(scope): message>`
```

## Index Update Rule

Sau khi tạo worklog mới, cập nhật bảng `Worklog Table`, checklist module và link evidence liên quan.
