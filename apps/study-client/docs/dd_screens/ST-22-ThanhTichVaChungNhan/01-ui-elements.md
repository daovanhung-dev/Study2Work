# ST-22 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-22_markers.json](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-22-EL-001` | `ST22-EL-01` | Study2Work brand and logo |
| #2 | `ST-22-EL-002` | `ST22-EL-02` | Primary navigation group |
| #3 | `ST-22-EL-003` | `ST22-EL-03` | Header search field |
| #4 | `ST-22-EL-004` | `ST22-EL-04` | Notification and account controls |
| #5 | `ST-22-EL-005` | `ST22-EL-05` | Learner/institution context label |
| #6 | `ST-22-EL-006` | `ST22-EL-06` | Current term and enrollment status |
| #7 | `ST-22-EL-007` | `ST22-EL-07` | Breadcrumb trail |
| #8 | `ST-22-EL-008` | `ST22-EL-08` | Ledger node status badge |
| #9 | `ST-22-EL-009` | `ST22-EL-09` | Cryptographic trust-layer hero label |
| #10 | `ST-22-EL-010` | `ST22-EL-10` | Hero title and descriptive copy |
| #11 | `ST-22-EL-011` | `ST22-EL-11` | Certificate verification sample card |
| #12 | `ST-22-EL-012` | `ST22-EL-12` | Copy verification identifier button |
| #13 | `ST-22-EL-013` | `ST22-EL-13` | Official certificate count metric |
| #14 | `ST-22-EL-014` | `ST22-EL-14` | Skill badge count metric |
| #15 | `ST-22-EL-015` | `ST22-EL-15` | Reputation points metric |
| #16 | `ST-22-EL-016` | `ST22-EL-16` | Percentile/rank metric |
| #17 | `ST-22-EL-017` | `ST22-EL-17` | Credentials section heading |
| #18 | `ST-22-EL-018` | `ST22-EL-18` | Credentials section explanatory copy |
| #19 | `ST-22-EL-019` | `ST22-EL-19` | Certificate 1 verified badge and identifier |
| #20 | `ST-22-EL-020` | `ST22-EL-20` | Certificate 1 issuer, issue date and GPA |
| #21 | `ST-22-EL-021` | `ST22-EL-21` | Certificate 1 program title and description |
| #22 | `ST-22-EL-022` | `ST22-EL-22` | Certificate 1 proof hash and QR image |
| #23 | `ST-22-EL-023` | `ST22-EL-23` | Certificate 1 view, PDF, LinkedIn and QR actions |
| #24 | `ST-22-EL-024` | `ST22-EL-24` | Certificate 2 verified badge and identifier |
| #25 | `ST-22-EL-025` | `ST22-EL-25` | Certificate 2 issuer, issue date and GPA |
| #26 | `ST-22-EL-026` | `ST22-EL-26` | Certificate 2 program title and description |
| #27 | `ST-22-EL-027` | `ST22-EL-27` | Certificate 2 proof hash and QR image |
| #28 | `ST-22-EL-028` | `ST22-EL-28` | Certificate 2 view, PDF, LinkedIn and QR actions |
| #29 | `ST-22-EL-029` | `ST22-EL-29` | Competencies section heading |
| #30 | `ST-22-EL-030` | `ST22-EL-30` | Competency filter chips |
| #31 | `ST-22-EL-031` | `ST22-EL-31` | TypeScript Master competency card |
| #32 | `ST-22-EL-032` | `ST22-EL-32` | Performance Hero competency card |
| #33 | `ST-22-EL-033` | `ST22-EL-33` | 7-Day Streak competency card |
| #34 | `ST-22-EL-034` | `ST22-EL-34` | Bug Hunter competency card |
| #35 | `ST-22-EL-035` | `ST22-EL-35` | Helpful Peer competency card |
| #36 | `ST-22-EL-036` | `ST22-EL-36` | Next-certificate title and description |
| #37 | `ST-22-EL-037` | `ST22-EL-37` | Readiness percentage ring and estimated date |
| #38 | `ST-22-EL-038` | `ST22-EL-38` | Next-certificate prerequisite status group |
| #39 | `ST-22-EL-039` | `ST22-EL-39` | Continue-course call to action |
| #40 | `ST-22-EL-040` | `ST22-EL-40` | Academic integrity and On-Chain Proof callout |
| #41 | `ST-22-EL-041` | `ST22-EL-41` | Footer brand and description |
| #42 | `ST-22-EL-042` | `ST22-EL-42` | Footer program links |
| #43 | `ST-22-EL-043` | `ST22-EL-43` | Footer community and support links |
| #44 | `ST-22-EL-044` | `ST22-EL-44` | Footer contact information |
| #45 | `ST-22-EL-045` | `ST22-EL-45` | Footer ISO certification badges |
| #46 | `ST-22-EL-046` | `ST22-EL-46` | Copyright strip and legal links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker đặt trên `screen_annotated.png`; JSON lưu target `x/y` theo ảnh gốc và vị trí badge trên annotated canvas. Các chi tiết trong PNG là mockup sample, không phải response proof. “Static” dưới đây có nghĩa asset HTML/PNG không có data binding/handler hiện tại.

**State chung của marker:** PNG chỉ cung cấp một trạng thái nhìn thấy tĩnh. Hover, focus, pressed, disabled, loading, success và error styling không được mô tả trong asset; ghi `UNSPECIFIED` cho đến khi có design/system source. Không suy ra keyboard/focus behavior hoặc accessibility label từ ảnh. Các event affordance chưa có route/API contract vẫn bị chặn.

| ID / marker | Element, loại, vị trí | Thuộc tính, nguồn dữ liệu, visibility/state | Event |
|---|---|---|---|
| ST22-EL-01 | Logo/brand Study2Work; header trái | Text/logo trong mockup. Route home, link target và state runtime chưa có; không lấy từ #38. | EV-14 |
| ST22-EL-02 | Nhóm primary navigation; header | Label nav tĩnh. Active item/route guard/destinations chưa wire. | EV-14 |
| ST22-EL-03 | Search field appearance; header trong PNG | PNG có ô search, nhưng `code.html` không có `<input>`; value/query/filter/API và validation chưa thuộc contract ST-22. Không dùng để lọc achievements. | — |
| ST22-EL-04 | Notification và account controls; header phải | Icon/profile menu tĩnh trong mockup; notification/account routes và session actions chưa xác nhận. | EV-14 |
| ST22-EL-05 | Institution/learner context label | Tên institution/learner là sample; không có source field từ #38. Visible trong PNG only. | — |
| ST22-EL-06 | Current term/enrollment status; top phải | Term/status sample; #38 không trả term/enrollment. Không suy status từ `course_id`. | — |
| ST22-EL-07 | Breadcrumb trail | Text breadcrumb, route destination chưa wired; chỉ current HTML empty prototype có link “back to progress”. | EV-14 |
| ST22-EL-08 | Ledger node status badge | On-chain node/status label là mockup claim; không được coi là ledger lookup/verification. | — |
| ST22-EL-09 | Cryptographic trust-layer hero label | Decorative trust-layer label; source/proof status absent. Không tuyên bố encryption/signature validity từ UI. | — |
| ST22-EL-10 | Hero title và explanatory copy | Static marketing copy; không có API field hoặc business rule hỗ trợ mọi claim trong copy. | — |
| ST22-EL-11 | Certificate verification sample card | Identifier/hash sample; #38 không trả certificate verification record. Render blocked until source contract. | EV-07, EV-11 |
| ST22-EL-12 | Copy verification identifier button | Button-like mockup control; clipboard value, success/error feedback và permission behavior chưa có contract/handler. | EV-07 |
| ST22-EL-13 | Official certificate count metric | Giá trị “02” là sample; không đếm `items` khi không có định nghĩa certificate-vs-achievement. | EV-04 |
| ST22-EL-14 | Skill badge count metric | Giá trị “14” là sample; #38 không có category/taxonomy/skill field. | EV-04 |
| ST22-EL-15 | Reputation points metric | “850” sample; không có reputation point source hoặc formula. | EV-04 |
| ST22-EL-16 | Percentile/rank metric | “Top 3%” sample; cohort, time window, calculation/authorization và source chưa có. | EV-04 |
| ST22-EL-17 | Credentials section heading | Heading tĩnh; credential collection relationship to achievement unresolved. | — |
| ST22-EL-18 | Credentials explanatory copy | Text claim về tiêu chuẩn/đối tác là sample; không có API #38 field hoặc compliance source. | — |
| ST22-EL-19 | Certificate 1 verified badge và identifier | On-Chain/verified badge, certificate code là sample; không map từ `id`/`code` mặc định. | EV-05 |
| ST22-EL-20 | Certificate 1 issuer, issue date, GPA | Issuer/GPA là unsupported; `awarded_at` chưa được xác nhận là certificate issue date. | EV-05 |
| ST22-EL-21 | Certificate 1 program title/description | Course/program title/description sample; Achievement `title` không được tự hiểu là program metadata. | EV-05 |
| ST22-EL-22 | Certificate 1 proof hash và QR image | Hash/QR sample; signature/issuer/target verification contract không có. | EV-05, EV-11 |
| ST22-EL-23 | Certificate 1 view/PDF/LinkedIn/QR actions | Bốn affordances nhìn thấy trong PNG; destinations, file URL, share payload, verification source, consent và handler chưa xác nhận. | EV-08, EV-09, EV-10, EV-11 |
| ST22-EL-24 | Certificate 2 verified badge và identifier | Nhóm giống certificate 1; sample content, không có certificate entity/schema trong #38. | EV-05 |
| ST22-EL-25 | Certificate 2 issuer, issue date, GPA | Issuer/date/GPA sample; không map từ #38 nếu chưa có projection được duyệt. | EV-05 |
| ST22-EL-26 | Certificate 2 program title/description | Program text sample, không có provenance từ #38. | EV-05 |
| ST22-EL-27 | Certificate 2 proof hash và QR image | Proof/QR sample; validity/provider/verifier chưa có contract. | EV-05, EV-11 |
| ST22-EL-28 | Certificate 2 view/PDF/LinkedIn/QR actions | Actions như EL-23; không tạo endpoint hoặc route từ mockup. | EV-08, EV-09, EV-10, EV-11 |
| ST22-EL-29 | Competencies section heading | Heading “Bộ sưu tập Huy hiệu kỹ năng đạt được”; taxonomy/award rules chưa được định nghĩa bởi #38. | — |
| ST22-EL-30 | Competency filter chips | All/Specialization/Community là sample facets; `course_id` không tương đương category filter. No default/selection/query semantics defined. | EV-06 |
| ST22-EL-31 | TypeScript Master competency card | Label/description/date sample; không có type/category/skill award mapping trong Achievement. | EV-05, EV-06 |
| ST22-EL-32 | Performance Hero competency card | Sample competency and date; source, award rule, status/expiry absent. | EV-05, EV-06 |
| ST22-EL-33 | 7-Day Streak competency card | Sample streak; no activity window/timezone/continuity rule. | EV-05, EV-06 |
| ST22-EL-34 | Bug Hunter competency card | Sample badge/level/date; no assessment/test evidence mapping. | EV-05, EV-06 |
| ST22-EL-35 | Helpful Peer competency card | Sample community badge/date; no interaction threshold/moderation/award rule. | EV-05, EV-06 |
| ST22-EL-36 | Next-certificate title and description | Target program/readiness narrative is sample; no qualification/progress contract. | EV-12 |
| ST22-EL-37 | Readiness ring and estimated date | 72% and date are unsupported sample values; no formula, denominator, date source or precision. | EV-12 |
| ST22-EL-38 | Next-certificate prerequisite status group | Three prerequisite cards/statuses are sample; no enrollment/lesson/assignment state mapping. | EV-12 |
| ST22-EL-39 | Continue-course CTA | Button-like mockup; course/lesson route, required ID, authorization gate and return path absent. | EV-12 |
| ST22-EL-40 | Academic integrity / On-Chain Proof callout | Copy/link is a mockup claim; integrity standard/proof verifier destination not established. | EV-13 |
| ST22-EL-41 | Footer brand and description | Static brand/description in screenshot; not data from #38. | EV-14 |
| ST22-EL-42 | Footer program links | Link labels in mockup; actual href/destinations/route guard not confirmed. | EV-14 |
| ST22-EL-43 | Footer community/support links | Labels are static; no destination or support behavior contract. | EV-14 |
| ST22-EL-44 | Footer contact information | Address, phone, email sample; authoritative contact data source absent. | EV-14 |
| ST22-EL-45 | Footer ISO badges | Certification marks are screenshot content; no current certificate/claim verification evidence. | — |
| ST22-EL-46 | Copyright strip and legal links | Footer text/link labels; legal destinations not confirmed by this screen's source. | EV-14 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/earned/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
