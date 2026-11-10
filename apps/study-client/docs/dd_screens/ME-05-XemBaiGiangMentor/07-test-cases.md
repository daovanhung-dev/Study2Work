# ME-05 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-05-TC-001` | Planning ref / not run | `AC-21` | See source acceptance section | P1 |

## 2. Test planning references

### ME-05-TC-001 — Acceptance planning reference (AC-21)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-05](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-21`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 7. Blockers and acceptance

| ID | Blocker / required decision | Evidence / owner action |
|---|---|---|
| ME05-B01 | Study Web router, API client and auth integration absent. | Provide editable app source and approved session/route behavior. |
| ME05-B02 | Assigned-course authorization and Mentor identity do not match current direct-owner numeric JWT-sub source. | Resolve AC-21 assignment relation/identity and align #46/#47/#48. |
| ME05-B03 | Course name/code and return route unavailable from #48; route only has lecture ID. | Define course context/ME-03 lookup or approved navigation state. |
| ME05-B04 | #47 `content:int64` decimal string cannot be assumed to be academic Markdown/code; null is allowed by #48. | Confirm content serialization, sanitize/render rules and null presentation. |
| ME05-B05 | Status enum and mutation lifecycle are open; #48 is read-only, #47 creates PUBLISHED. | Define allowed states and approved Mentor status API before exposing #14. |
| ME05-B06 | Edit button has no Mentor lecture update API/route. | Approve endpoint/body/validation or remove #15 from production UI. |
| ME05-B07 | Video player, transcript, chapter timing, duration and preview access have no #48 fields or media source. | Define media resource/playback/caption/preview contract; do not use mock player data. |
| ME05-B08 | Asset URL access/download/PDF preview not verified. | Confirm storage URL authorization, MIME/preview, expiry, file naming and error policy. |
| ME05-B09 | Analytics metrics/chart/realtime values have no source in ME-05 contract. | Assign API/data source, metric definitions and freshness or remove #25. |
| ME05-B10 | Discussion cards/reply and ST-25 target lack Mentor route/API; ST-25 is Student-facing. | Define Mentor discussion ownership, route, read/write API and count policy. |
| ME05-B11 | Course tree and previous/current/next lesson rows are not returned by #48. | Define #49/ME-06 relationship or approved lesson-curriculum navigation source. |
| ME05-B12 | API #48 DD remains Draft; legacy schema/migration 005 deployment/live DB unverified; status/content/path/error rules need confirmation. | API/DB owner confirms target schema and outstanding Q-48-01…07. Reconcile API DD error `data` wording with current helper source (`null`). |
| ME05-B13 | Static sample personal/course/file data and `href="#"` destinations are not deployable sources. | Replace with server data and approved route/URL fields. |

### DD acceptance for ME-05

- All 33 markers resolve one-to-one to element rows; all visible interactive controls map to event entries or an explicit blocked/unwired status.
- API #48 field/error/auth/ordering/side-effect claims match source; current API DD and live schema status remain separately stated.
- Approved decisions resolve blockers before calling the UI DD implementable. Until then ME-05 is **not DD READY**.
- `IMPLEMENTATION BLOCKED` reflects missing contract/runtime prerequisites. `RUNTIME VERIFIED` remains false because no browser route/API deployment was exercised.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 4. Kiểm tra và tiêu chí kết thúc phiên

- Giữ nguyên hash `screen.png` và `code.html`.
- JSON có đúng 33 số liên tiếp và 33 ID duy nhất; SVG có 33 marker khớp JSON/DD; marker nằm trong tọa độ ảnh gốc; annotated PNG có kích thước đúng scale 2 và được xem trực quan.
- 100% element có mô tả; mọi nút/link/nhóm player/timeline có event entry hoặc ghi rõ `unwired/blocked`; API #48 fields/errors/access/effects đúng source; mọi route/field giả lập được đánh dấu gap.
- Tất cả relative links trong DD và worklog/tracker trỏ đúng file; checkpoint tăng 32/83 → 33/83 chỉ khi đủ 4 file cốt lõi; không sửa các Screen ID khác.
- Không chạy test/runtime; `DD READY` không được dùng nếu blockers còn chặn implementability, `IMPLEMENTATION BLOCKED` ghi phụ thuộc, `RUNTIME VERIFIED` giữ riêng và chưa đạt.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
