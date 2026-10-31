# SH-01 — Design Plan

| Field | Target |
|---|---|
| Screen ID | SH-01 |
| Status | DESIGN_TARGET / NOT_IMPLEMENTED |
| Inventory | apps/study-client/docs/dd_screens/list_screen.md, STT 01 |
| Route | / |
| Actor / surface | Guest / Page |
| Acceptance criterion / wave | AC-03 / W0 |
| Reference viewport | 1440 × 1320 px, full page |

## 1. Evidence and scope

SH-01 is the first screen in the inventory: a public Study introduction page that presents the learning proposition, helps visitors find courses, and links to course discovery, sign-in and registration. The inventory identifies SH-01 as R for its referenced APIs, but that does not mean this Vue page is implemented: the current checkout contains the inventory document and no Study Web source/router.

This plan is for one screen only. GS-01, GS-02, GS-03, SH-02 and SH-03 remain separate screen IDs. SH-01 includes navigation to them but does not duplicate their page designs. It has no child page, dialog or suggestion panel in this design; therefore no child-screen subfolder is needed.

### Source and contract findings

| Evidence | Current finding | Design consequence |
|---|---|---|
| .agents/web-study/design.md | Canonical Study Web visual target: light-first ocean palette, Inter/system sans-serif, 4px spacing rhythm, restrained surfaces, 44px minimum controls, WCAG AA and reduced-motion support. | Use these tokens and constraints. Do not use the generic clay/playful direction returned by the UI skill because it conflicts with this project guide. |
| Inventory §2, row 01; §3 F02 | SH-01 is /, Guest, AC-03, APIs #05/#06; links to GS-01, SH-02 and SH-03. F02 maps search to GS-02 and later course selection to GS-03. | Header/footer link to GS-01/SH-02/SH-03. The hero search submits to GS-02. A course preview does not deep-link to GS-03 from SH-01. |
| Current API #05 source | Public GET /api/v1/categories; optional exact-match locale, default vi-VN; reads ACTIVE categories and maps id, name, slug, nullable description. Empty results are HTTP 200. | Category labels may be shown as read-only metadata. Do not imply that a category selects or filters courses. |
| Current API #06 source | Public GET /api/v1/courses; only PUBLISHED courses; default page 1, size 20, size range 1–100; default order created_at DESC, id ASC. Response fields: id, title, nullable description, nullable thumbnail_url, decimal-string price, status and mentor{id, full_name, nullable avatar_url}. | Home preview requests page=1&size=3; use only returned fields. Omit price because no currency unit is defined; omit status, ratings and category because they are not useful public card fields or not present in this response. |
| API #06 validator/test source | Sending category returns 422 DESIGN_VALIDATION_ERROR; current response has no category. Test fixture rows use fake DB data. | Do not send a category query or bind #05 categories to course cards. Sample copy in the image is illustrative only, not live catalog content. |
| Study Web subcontext and source inventory | .agents/web-work/study/AGENTS.md and INDEX.md are missing in this checkout; apps/study-client has no source/router/package files. Study OpenAPI is a placeholder. | Label the output DESIGN_TARGET; no implementation, live data or working route is claimed. |

The API #05/#06 DD packages remain Draft — Needs Confirmation; their examples and fake-row tests do not establish live schema, migration deployment or production data. Current source determines displayable fields, while the screen inventory supplies the expected user journey.

## 2. Goals and exclusions

### Goals

- Make the next useful actions obvious: search for a course, browse the course list, sign in or register.
- Give a calm, polished first impression with readable Vietnamese copy and a compact public header.
- Show a small preview of published courses and active category metadata without implying unsupported filters or course-category relations.
- Keep the layout usable at desktop, tablet and 320px mobile widths.
- Include stable #1–#41 markers in the annotated image. Markers identify every visible leaf element represented in the specification table; they are overlays for review, not product UI.

### Explicit exclusions

- No rating, star average, review count, popularity count, student count or testimonial.
- No price display until the currency/unit is confirmed.
- No clickable category chips or category filtering.
- No invented category field on a course, API, route, backend behavior, live database state or external-storage URL.
- No course-card deep link from SH-01; course selection-to-detail belongs to GS-01 → GS-03 in F02.
- No rotating hero, autoplay, large gradient, glass effect, heavy shadow, emoji icon or decorative copy that claims a platform metric.
- No mobile drawer, modal or search-suggestion child surface.

## 3. Layout plan

| Area | Desktop layout at 1440px | Responsive behavior |
|---|---|---|
| Page frame | #F6FAFC; centered content max-width 1120px; 32px outer gutters. Full-page reference image is 1440×1320px. | Gutters 24px at tablet and 16px at mobile. Main content remains in one scroll column. |
| Public header | 72px-high white header with a quiet bottom border. Brand left, two navigation links centered/left, sign-in and register actions right. | Header stays one row. At <768px, logo acts as Home so the explicit Home nav link is hidden; Courses, Sign in and compact Register remain visible. No drawer. |
| Hero | Two columns: text/search about 560px; decorative flat illustration about 460px. Generous whitespace; no proof metrics. | Stack text before illustration at tablet/mobile. Hide the decorative illustration below 768px; keep headline, search and routes visible. Search button becomes full width below the input. |
| Categories | Small title/support line and two sample taxonomy labels with a slim accent on a single wrap-capable row. Labels are static text, not controls. | Wrap to multiple rows. No horizontal carousel or swipe-only interaction. |
| Course preview | Section title and Xem tất cả link; 3 equal cards in a 3-column grid, 24px gap. Each card has thumbnail, title, optional description, mentor avatar and mentor name. | Two columns at tablet and one column at mobile. Long descriptions clamp to 2 lines; full title and mentor identity remain available. |
| Footer | Minimal white/soft-surface footer with Study brand/copy and links only to /courses, /login, /register. | Stack brand and links; no new policy routes are introduced. |

### Vertical composition

1. Header: y≈24–96.
2. Hero: y≈136–468; H1 is the strongest element and search is the primary action.
3. Category metadata: y≈528–630.
4. Course preview: y≈684–1118.
5. Footer: y≈1192–1290.

All dimensions are design targets at the reference viewport; use a 4px spacing scale and 12–16px card radius. Keep borders at 1px and shadows low/diffuse. Primary buttons and form controls are at least 48px high; links have a generous 44px line/target area.

## 4. Visual direction

| Token | Value | Use in SH-01 |
|---|---|---|
| ocean-primary | #0B5F8A | Primary CTA, active Home link and visible keyboard focus. |
| ocean-hover | #084968 | Hover/pressed primary controls. |
| ocean-deep | #073B57 | Main headline and strong accents. |
| sky-accent | #43A5C5 | Small decorative illustration details only. |
| ocean-soft | #E8F4FA | Eyebrow and quiet information backgrounds. |
| page-background | #F6FAFC | Main page surface. |
| surface | #FFFFFF | Header, inputs and course cards. |
| text-primary | #17324D | Headings and primary content. |
| text-muted | #536A7A | Supporting copy and mentor metadata. |
| border | #D4E2E9 | Card/input/header boundaries. |

Use Inter if locally available; otherwise use the system sans-serif stack. No remote font import or new package. Target type sizes: eyebrow 13/18px 600; H1 48/58px 700; section headings 30/38px 650; card titles 18/26px 600; body 16/26px 400; nav/button 15/22px 600; metadata 14/20px 500. Keep text contrast at least 4.5:1 and meaningful icon/border contrast at least 3:1.

The illustration is a single decorative, flat vector-like composition (open book + three abstract course tiles + small arcs). It contains no labels, pseudo-statistics, external brand marks or course content; it is hidden from assistive technology and may be removed on mobile.

## 5. Numbered element plan for the annotated image

Every number below must appear as a small #n callout in the annotated image and map to one row in SCREEN.md. Place callouts beside their targets, never on top of text or a control label. Use a consistent 24×24px circular ocean-primary badge with white 12px/700 Inter text and a thin white keyline. Use SH-01_annotated.png with callouts and SH-01_clean.png without callouts.

| Marker | Element | Target / event |
|---:|---|---|
| #1 | Brand symbol | Decorative mark inside Home link. |
| #2 | Study wordmark | Home link /. |
| #3 | Trang chủ nav link | /. Hidden on mobile because the brand link is Home. |
| #4 | Khóa học nav link | GS-01 /courses. |
| #5 | Đăng nhập header action | SH-02 /login. |
| #6 | Đăng ký header primary action | SH-03 /register. |
| #7 | Hero eyebrow | Static text. |
| #8 | Hero H1 | Static headline. |
| #9 | Hero supporting paragraph | Static text; no outcome/metric claim. |
| #10 | Search field label | Visible accessible label. |
| #11 | Search textbox | User text; URL-safe search query on submit. |
| #12 | Search glyph | Decorative SVG inside textbox; no click behavior. |
| #13 | Tìm khóa học submit button | Non-empty trimmed query → GS-02 /courses/search?q=...; empty query → GS-01. |
| #14 | Hero illustration group | Decorative only; aria-hidden; no event. |
| #15 | Category section heading | Static text. |
| #16 | Category support line | Static text; clarify these are browse topics, not filters. |
| #17 | Static taxonomy label Lập trình with 2×16px #43A5C5 accent | Illustrative #05 category display; no click/tap/hover/focus/filter action. |
| #18 | Static taxonomy label Thiết kế with 2×16px #43A5C5 accent | Illustrative #05 category display; no click/tap/hover/focus/filter action. |
| #19 | Course preview heading | Static text. |
| #20 | Xem tất cả link | GS-01 /courses. |
| #21–#25 | Course card 1: thumbnail, title, description, mentor avatar, mentor name | Display-only sample record from the #06 field shape; no click or hover. |
| #26–#30 | Course card 2: thumbnail, title, description, mentor avatar, mentor name | Display-only sample record from the #06 field shape; no click or hover. |
| #31–#35 | Course card 3: thumbnail, title, description, mentor avatar, mentor name | Display-only sample record from the #06 field shape; no click or hover. |
| #36 | Footer brand symbol | Decorative mark. |
| #37 | Footer Study wordmark | Home link /. |
| #38 | Footer supporting copy | Static text. |
| #39 | Footer Khóa học link | GS-01 /courses. |
| #40 | Footer Đăng nhập link | SH-02 /login. |
| #41 | Footer Đăng ký link | SH-03 /register. |

The two category names and three example course/mentor records in the picture are VISUAL_SAMPLE content used only to compose the mockup. They are not statements about live catalog rows. Do not display card price, currency, rating, review count, course status or a course category.

## 6. Interaction and state plan

| Trigger | Expected design behavior | Boundary |
|---|---|---|
| Click/tap brand or Home | Navigate to /. | Proposed UI route; not implemented in current checkout. |
| Click/tap Courses or Xem tất cả | Navigate to GS-01 /courses. | Screen inventory target. |
| Click/tap Sign in/Register | Navigate to SH-02 /login or SH-03 /register. | Screen inventory target. |
| Enter query and submit by button or Enter | Trim leading/trailing whitespace, encode query once, reset search page to 1, navigate to GS-02 with q. | API #07 belongs to GS-02; SH-01 does not call it directly. |
| Submit blank/whitespace-only query | Navigate to GS-01 /courses; do not send an empty q. | UI fallback decision; no backend rule added. |
| Hover links/buttons | Change color to ocean-hover or underline link; 140ms, no layout movement. | Only interactive controls receive pointer/hover treatment. |
| Focus visible | 2px ocean-primary outline with 2px offset; tab order follows visual/task order. | Must remain visible around all breakpoints. |
| Reduced motion | Remove nonessential translation/entrance motion; retain immediate color/focus feedback. | Honor prefers-reduced-motion: reduce. |
| Initialize page | Resolve the route, then load category metadata (#05) cache-first by vi-VN where a client cache is actually available and request course preview (#06) independently. | Cache TTL is unspecified; do not invent one. #05 failure does not block #06 and vice versa. |
| #05 returns empty | Keep hero and courses. Show a short category empty message in the category region; do not manufacture topics. | API #05 empty list is a successful 200. |
| #06 returns empty | Keep hero/search/categories. Replace cards with an honest empty message and a Retry action for the same read request. | No fake course card; no new API. |
| #05 or #06 read fails | Show section-level error with Retry; do not collapse the other successful section. Include trace ID only when actually supplied by the server. | API source has safe 500 envelope; no live DB claim. |
| Loading | Use skeleton placeholders matching the section/card geometry; never flash sample data as if it came from the API. | Screenshot is a design preview only; samples are labelled in this plan/spec. |

Category labels and course preview cards are deliberately noninteractive. Their visuals must not use capsule/button silhouettes, pointer cursors, hover lift, pressed styling, button semantics or misleading link affordance. The only course-discovery actions on SH-01 are the search form and explicit links to GS-01/GS-02.

## 7. State and responsive review checklist

- INITIAL/LOADING: retain header and hero copy; category/course areas use stable skeletons with no layout shift.
- READY: render only validated category/course data; null descriptions and null thumbnail/avatar fields use documented fallback/hide behavior.
- EMPTY: category and course empty states are independent; do not show fabricated cards or categories.
- ERROR: independent section error and safe retry; do not transform API errors into “not found”.
- Search IDLE, FOCUS, TYPING, SUBMITTING: visible label, clear focus ring, button loading/disabled without shifting layout, submit by Enter or click.
- At 320px, no horizontal page overflow; stacked search; category wraps; one course card per row; no essential content depends on the illustration.
- At 768–1023px, maintain two-card grid where it fits; readable line lengths and no clipped navigation.
- At ≥1024px, 1120px maximum content width; three-card row; H1 does not compete with the illustration.
- Verify all colors on composed surfaces, 44px control/target minimum, semantic links/buttons, visible focus and reduced motion.
- Final annotated image includes every marker #1–#41 exactly once and does not obscure the corresponding content. Clean image has identical geometry/copy without marker overlays.

## 8. Planned artifact structure

resource/SH-01/
├── PLAN.md
├── SH-01_annotated.png
├── SH-01_clean.png
└── SCREEN.md

This screen has no child screen surface. Related IDs are linked in SCREEN.md and are authored in their own folder during their own one-screen session.

## 9. Review before creation

1. Compare the generated image to the layout, ocean tokens, responsive notes and exact marker map above.
2. Inspect that #1–#41 are unique, legible and attached to the right leaf element; ensure no uncatalogued interface control appears.
3. Compare every generated label to the SCREEN.md element table, including routes, click/hover behavior, dimensions and typography.
4. Confirm that course cards omit price/currency, ratings, category and status; taxonomy labels and course cards do not look clickable.
5. Check that the clean image is pixel-equivalent in layout/content apart from marker overlays.
6. Record concrete visual defects and a targeted fix plan, regenerate/revise, and repeat review until the screen matches this plan.
