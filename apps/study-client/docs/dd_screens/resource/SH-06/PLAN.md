# SH-06 — Trang không tồn tại / tài nguyên không còn

## 1. Phạm vi và bằng chứng

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [SH-06 -> API #08 GET /api/v1/courses/{course_id}; GS-01 /courses; SH-01 /]
screen: SH-06, /not-found, State view, AC-05, API #08
artifact_status: DESIGN_TARGET / NOT_IMPLEMENTED
variants: ROUTE_NOT_FOUND, RESOURCE_NOT_FOUND
```

- Thiết kế một state view trong một folder. `ROUTE_NOT_FOUND` và `RESOURCE_NOT_FOUND` là biến thể của SH-06, không phải route con.
- Canonical visual target: `.agents/web-study/design.md`; screen logic: `apps/study-client/docs/dd_screens/list_screen.md` SH-06, GS-01/GS-03, F02, state/security rules.
- API #08 current source khác inventory: server đã có route/import/view/query/validator/test source. Inventory §5 vẫn đánh dấu `D`, GS-03 nói #08–#10 chưa wired, và DD #08 vẫn `Draft — Needs Confirmation`. Giữ `DISCREPANCY`, ưu tiên source cho current HTTP behavior, không tuyên bố live schema/deploy.
- API #08 chỉ query `PUBLISHED`; invalid ID, không có row và non-published cùng trả HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`. Query/mapping failure trả safe 500. Vì vậy lỗi 500/network không được render thành SH-06.
- Study Web hiện chưa có router/client source. Route `/not-found`, state mapping và links là design target.
- CUA đã thử lại trong turn này: không có browser surface; `createBrowserTab("chrome", "https://chatgpt.com", ...)` trả `Browser is not available: chrome`. Sau khi chốt plan, dùng built-in imagegen chỉ để tạo artwork minh họa; sẽ không ghi rằng ChatGPT website tạo/tải gói này.

## 2. State matrix, logic và CTA

| State | Khi nào hiển thị | Eyebrow + H1 | Body | Hành động chính | Hành động phụ |
|---|---|---|---|---|---|
| `ROUTE_NOT_FOUND` | Client router không khớp path với route đã đăng ký; không gọi API #08. | `TRANG KHÔNG KHẢ DỤNG` · **Trang này không / tồn tại** | Desktop: “Địa chỉ có thể không chính xác hoặc đã thay đổi. Hãy tìm khóa học từ danh sách bên dưới.” Mobile rút gọn theo viewport nhưng giữ cùng ý. | **Tìm khóa học** → GS-01 `/courses`. | **Về trang chủ** → SH-01 `/`. |
| `RESOURCE_NOT_FOUND` | GS-03/API #08 trả 404: ID sai, không có course row hoặc course không `PUBLISHED`. | `KHÓA HỌC KHÔNG KHẢ DỤNG` · **Không tìm thấy / khóa học này** | Desktop: “Khóa học này không thể hiển thị tại địa chỉ hiện tại. Bạn có thể chọn một khóa học khác.” Mobile rút gọn theo viewport nhưng giữ cùng ý. | **Tìm khóa học** → GS-01 `/courses`. | **Về trang chủ** → SH-01 `/`. |

Ở cả hai biến thể không in `404`, `course_id`, URL đầy đủ, tên khóa học hoặc trạng thái draft/private. Cùng một copy `RESOURCE_NOT_FOUND` áp dụng cho missing và unpublished; người dùng không biết course có từng tồn tại hay không. Nút “Tìm khóa học” điều hướng tĩnh; không dựng search field hoặc tự gọi #06 từ state view.

### Flow tách biệt

```text
Unmatched client path
  -> ROUTE_NOT_FOUND
  -> GS-01 /courses | SH-01 /

GS-03 route /courses/:courseId
  -> public GET API #08 /api/v1/courses/{course_id}
  -> 200: render GS-03 (outside SH-06)
  -> 404: RESOURCE_NOT_FOUND
  -> 500/network: SERVICE_ERROR (outside SH-06; do not convert to 404)
```

API #08 current source selects only `courses.status = 'PUBLISHED'`, returns the same safe 404 for malformed ID / no row / unpublished, rolls back query failures and maps them to 500 `DESIGN_INTERNAL_ERROR`. Success is a read-only singleton `CoursePage`. SH-06 does not render any success DTO or retry the request.

## 3. Art direction, bố cục, màu

- **Visual thesis:** “Một trang giấy bị thiếu trong hành trình học.” Minh họa giấy xếp lớp với một góc gập, đường chấm ngừng trước khoảng trống, nét mềm và có chủ ý. Không tái dùng cổng ngưỡng của SH-05, không cảnh báo đỏ, kính lúp, dấu hỏi lớn, người/khóa học giả, text hoặc mã 404 trong art.
- **Canvas desktop:** 1440×960; header trắng cao 96px, divider `#D4E2E9`; content max 1120px (`x=160..1280`). Copy trái (`x=160..700`) và art phải (`x≈850..1280`), khoảng trắng rõ giữa hai vùng.
- **Header:** shared Study mark x=160,y=30, 38×38; wordmark Study x=210. Không thêm nav/action mới vào global state shell; logo/wordmark về SH-01.
- **Copy:** eyebrow box `160,264,340×20`; H1 `160,312,540×104`, 44/52/700, tối đa hai dòng; body `160,436,520×60`, 17/28/400, hai dòng; primary CTA `160,560,224×56`; secondary link hit-area `160,640,180×44`. Hai state giữ cùng bounds, không layout jump.
- **Illustration stage:** vùng phải `x≈810..1280`, `y≈250..725`. #8 halo x=870,y=265,380×380; #9 transparent paper illustration x=858,y=250,w=420,h=420; #10 route line x=817..930, baseline y=696; #11 node tâm (948,696), 29×29; #12 ba chấm nhấn nhẹ quanh halo. Artwork không có nội dung có thể nhận dạng như tên/id/data. PNG giấy 1254×1254 RGBA, được co trong SVG để giữ nét và alpha.
- **Responsive 390×844:** header 72px, gutter24; eyebrow baseline116; H1 baselines166/204; body257/282; CTA x=24,y=328,w=342,h=54; secondary hit-area y=398,h=44; art co theo scale 0.58 và nằm dưới action.
- **320×844:** gutter16; H1 28/38; body 15/25 với copy ngắn; button full-width `288×54`; art co scale0.51. Giữ copy/action, không horizontal scroll. Badge ở ảnh annotated compact co còn16px để nằm trong gutter.
- **Palette:** page `#F6FAFC`, surface `#FFFFFF`, heading `#073B57`, body `#536A7A`, primary `#0B5F8A`, hover `#084968`, soft `#E8F4FA`, decorative accent `#43A5C5`, border `#D4E2E9`. Noto Sans là system sans khả dụng trong môi trường render; không tải font ngoài.

## 4. Element map (12 targets)

Bounds là pixel trong canvas. SVG minh họa raster là một `<image>` group; các halo/route/node/dots rời vẫn có target riêng. Badge annotated là 24px desktop, 20px ở 390px và 16px ở 320px để vừa lề hẹp mà không che chữ.

| # | Element/nội dung | Bounds desktop 1440×960 | Style | Ý nghĩa/sự kiện | Hover/focus/mobile |
|---:|---|---|---|---|---|
| 1 | Study brand mark | `160,30,38×38`; hit `157,27,44×44` | `#0B5F8A`, radius11; glyph trắng nét mảnh | Link → SH-01 `/` | Hover/pressed `#084968` 140ms; focus-visible 2px primary + offset2; mobile `24,18,36×36`, hit44×44. |
| 2 | Wordmark `Study` | Anchor x=210 baseline58 | Noto Sans 23/30/700 `#073B57` | Cùng brand anchor về `/`, không tạo tab-stop thứ hai | Hover/pressed `#084968`; mobile x=72 baseline43, 22/28/700. |
| 3 | State eyebrow | `160,264,340×20` | 13/18/700 `#0B5F8A`, tracking0.5 | Static text; thay copy theo state | No hover/focus; mobile x=24 baseline116, 12/18; x=16 ở 320px. |
| 4 | H1 | `160,312,540×104`; baselines350/402 | 44/52/700 `#073B57`; state-specific two lines | Một H1, không click; screen-reader text liền mạch | Mobile x=24 baselines166/204, 32/38; 320px 28/38. Không truncate. |
| 5 | Supporting copy | `160,436,520×60`; baselines455/483 | 17/28/400 `#536A7A`; state-specific | Static, không lộ API response/id/status | Mobile x=24 baselines257/282, 16/25; 320px 15/25, copy rút gọn. |
| 6 | Primary button `Tìm khóa học` | `160,560,224×56`, radius10 | Ocean-primary fill, white 16/24/600 | Click/Enter → GS-01 `/courses`; no API call from SH-06 | Hover/pressed `#084968` 140ms; focus ring 2px + offset2; mobile full width342×54, 320px288×54. |
| 7 | Secondary link `Về trang chủ` + arrow | hit `160,640,180×44`; glyph baseline668 | 15/22/600 `#0B5F8A`, underline only hover; 1.6px arrow | Click → SH-01 `/`; no query/token | Hover underline + `#084968`; visible focus; mobile hit x24,y398,w342,h44; 320px x16. |
| 8 | Soft halo behind artwork | `870,265,380×380` | `#E8F4FA`, circle, one diffuse shadow; no gradient | Decorative, `aria-hidden=true` | No hover/focus; scale with illustration. |
| 9 | Blank folded-page illustration PNG | `858,250,420×420` transparent asset | Editorial paper-cut layers; pale paper/sky planes, restrained shadows; no embedded text | One decorative image group, `aria-hidden=true`; file stored inside SH-06 folder | No hover/focus; scale0.58 at390px and0.51 at320px; no clipping. |
| 10 | Dotted route with deliberate gap | `817,694.5,113×3` | Accent `#43A5C5`, 3px round dots `2 9` | Decorative path metaphor; not a progress bar | No hover/focus/animation. Mobile transform with art stage. |
| 11 | Open endpoint ring | visual `933.5,681.5,29×29`; center `(948,696)` | White fill, 3px ocean stroke, 4px accent core; no X/question mark | Decorative route endpoint, `aria-hidden=true` | No hover/focus; scale proportionally. |
| 12 | Three quiet accent dots | centers `(900,300)`, `(1240,420)`, `(1204,645)` | 3–4px `#43A5C5`, varied low opacity | Static decoration in same illustration composition | No hover/focus; no repeated motion; scales with art. |

### Marker positions

Mỗi ảnh `_annotated` có đúng 12 badge nối leader line ra element tương ứng. Badge không nằm trong accessibility tree; clean screenshots không có badge.

| # | Desktop center (24px badge) | Mobile 390px center (20px) | Compact 320px center (16px) |
|---:|---:|---:|---:|
| 1 | `(138,32)` | `(12,12)` | `(8,12)` |
| 2 | `(304,26)` | `(144,12)` | `(136,12)` |
| 3 | `(138,261)` | `(12,98)` | `(8,88)` |
| 4 | `(138,327)` | `(12,151)` | `(8,130)` |
| 5 | `(138,444)` | `(12,247)` | `(8,230)` |
| 6 | `(138,566)` | `(12,309)` | `(8,315)` |
| 7 | `(138,646)` | `(12,438)` | `(8,438)` |
| 8 | `(841,264)` | `(42,548)` | `(31,560)` |
| 9 | `(1298,271)` | `(337,548)` | `(289,560)` |
| 10 | `(798,678)` | `(32,776)` | `(10,766)` |
| 11 | `(927,736)` | `(151,822)` | `(126,828)` |
| 12 | `(1261,655)` | `(337,735)` | `(286,735)` |

Leader lines stop at the nearest element boundary or its whitespace envelope. They do not cross the glyphs or CTA label.

## 5. Hành vi, accessibility và open decisions

| Event | Expected behavior | Status/evidence |
|---|---|---|
| Unmatched route | Render `ROUTE_NOT_FOUND`; không call API #08; cho GS-01/SH-01 actions | Inventory target; client router absent. |
| API #08 404 | Render `RESOURCE_NOT_FOUND`; use same generic copy for invalid/missing/unpublished | Current server source; no client mapping source. |
| API #08 500 / network | Use `SERVICE_ERROR`, not SH-06 | Current server source returns 500 on query/mapping failure; global inventory separates service error. |
| Bấm primary | Navigate `/courses` (GS-01) | Design target; no extra API request. |
| Bấm secondary/brand | Navigate `/` (SH-01) | Design target. |

- Text order: brand → eyebrow → H1 → paragraph → primary → secondary. Art group `aria-hidden=true`.
- Controls hit area ≥44×44; body copy wraps at 320px; focus ring stays visible. Text/state conveys meaning without accent color.
- Hover 140ms color/underline only; `prefers-reduced-motion` removes nonessential motion. Art is static.
- No course name, course id, raw response, draft/private label or 404 status code in page/UI. No card, search field, recommendation, random course sample or new API is added.
- Open decisions: Study Web router and `SERVICE_ERROR` component are absent; API #08 contract is draft and `CoursePage` singleton shape conflicts with a detail resource. This screen consumes no success payload, so those uncertainties do not change the 404 art/copy.
- No child screens exist in SH-06 inventory. GS-01 and SH-01 remain linked screens, not nested subfolders.

