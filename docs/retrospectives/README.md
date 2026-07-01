# Retrospectives

Retrospective giúp giảm lặp lại, giảm token và cải thiện context. Không đọc lại toàn bộ 30 worklog nếu index/checklist đã đủ để tổng hợp.

## Cadence

| Field | Value |
|---|---|
| Frequency | Sau mỗi 30 session mới kể từ retrospective gần nhất |
| Source of session truth | `docs/worklog/INDEX.md` |
| Path format | `docs/retrospectives/RETRO_<START_SESSION>_<END_SESSION>.md` |
| Last updated | `2026-07-01` |

## Current State

| Item | Value |
|---|---|
| Latest retrospective | _none_ |
| Sessions covered | _none_ |
| Next trigger | After sessions `0001` through `0030` exist |

## Required Retrospective Template

```md
# Retrospective — <START_SESSION> to <END_SESSION>

| Field | Value |
|---|---|
| Sessions | `<START_SESSION>-<END_SESSION>` |
| Created | `YYYY-MM-DD` |
| Sources | `docs/worklog/INDEX.md`, related checklists, risk worklogs |

## Việc Lặp Lại

- <Repeated workflow>

## Lỗi Lặp Lại

- <Repeated bug/fix>

## Module Tốn Token

- <Module and reason>

## Tài Liệu Thiếu Hoặc Mâu Thuẫn

- <OPEN_QUESTION or CONFLICT>

## Skill Cần Tạo/Cập Nhật

- <Skill action>

## Quy Trình Có Thể Rút Gọn

- <Improvement>

## Context Quá Dài Hoặc Trùng Lặp

- <Context action>

## Lệnh Test/Build Cần Ghi Rõ Hơn

- <Command gap>

## Action Cải Tiến

| ID | Owner | Status | Action | Link |
|---|---|---|---|---|
| `<RETRO-ACTION-001>` | `<owner>` | `<status>` | `<action>` | `<link>` |
```

## Update Rule

Chỉ cập nhật `AGENTS.md` hoặc `docs/agent/` nếu insight ổn định, tái sử dụng và giúp agent tránh lỗi thật.
