# Checklist — NOTIFICATION

| Field | Value |
|---|---|
| Module code | `NOTIFICATION` |
| Module name | Notification and Async User Messaging |
| Last updated | `2026-07-01` |
| Source BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| Status model | `docs/agent/STATUS_MODEL.md` |

## Link BD Nguồn

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `NOTIFICATION-BD-001` | `NOT_STARTED` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Domain events, notification tables, reliability rules, NOTI/SYSTEM business codes. |

## Danh Sách DD Liên Quan

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `NOTIFICATION-DD-001` | `NOT_STARTED` | `2026-07-01` | `docs/DD/NOTIFICATION/` | Planned module DD; folder not created yet. |

## Danh Sách Feature / Function / View

| ID | Type | Status | Updated | Link | Note |
|---|---|---|---|---|---|
| `NOTIFICATION-F01` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/NOTIFICATION/` | Notification templates and channels. |
| `NOTIFICATION-F02` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/NOTIFICATION/` | In-app notification feed/read state. |
| `NOTIFICATION-F03` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/NOTIFICATION/` | Async delivery and retry-safe events. |

## Trạng Thái DD

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `NOTIFICATION-DD-STATUS` | `NOT_STARTED` | `2026-07-01` | `docs/DD/NOTIFICATION/` | No NOTIFICATION DD found. |

## Trạng Thái Coding

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `NOTIFICATION-CODE-STATUS` | `NOT_STARTED` | `2026-07-01` | `backend/src/modules/notifications/` | Skeleton exists; no implementation evidence. |

## Trạng Thái Test

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `NOTIFICATION-TEST-STATUS` | `NOT_STARTED` | `2026-07-01` | `tests/` | No test command or test evidence yet. |

## Bug / Open Question

| ID | Status | Updated | Link | Description |
|---|---|---|---|---|
| `NOTIFICATION-BUG-001` | `NONE` | `2026-07-01` | `docs/worklog/INDEX.md` | No NOTIFICATION bug recorded. |
| `NOTIFICATION-OQ-001` | `OPEN` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Worker choice Celery/RQ is ADR backlog item. |

## File Code Dự Kiến Ảnh Hưởng

| ID | Status | Updated | Path | Note |
|---|---|---|---|---|
| `NOTIFICATION-FILE-001` | `NOT_STARTED` | `2026-07-01` | `backend/src/modules/notifications/` | Existing skeleton reference. |
| `NOTIFICATION-FILE-002` | `NOT_STARTED` | `2026-07-01` | `apps/web-student/src/modules/dashboard/` | Potential notification feed surface. |
| `NOTIFICATION-FILE-003` | `NOT_STARTED` | `2026-07-01` | `apps/web-admin/src/modules/system-settings/` | Potential notification template/settings surface. |

## Worklog Liên Quan

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `NOTIFICATION-WL-001` | `NOT_STARTED` | `2026-07-01` | `docs/worklog/INDEX.md` | No NOTIFICATION worklog yet. |

## Bằng Chứng Xác Nhận

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `NOTIFICATION-EV-001` | `NOT_STARTED` | `2026-07-01` | `docs/worklog/INDEX.md` | No evidence yet. |

## Việc Tiếp Theo

| ID | Status | Updated | Link | Task |
|---|---|---|---|---|
| `NOTIFICATION-NEXT-001` | `NOT_STARTED` | `2026-07-01` | `docs/DD/DD_Module_Template/` | Create NOTIFICATION DD from BD before coding. |
