# SPEC: ST-11 Static Lesson Player Fallback

## Status

- Revision: `1`
- Approval: `PENDING`
- Source screen: `apps/study-client/docs/dd_screens/ST-11-TrinhHocBaiLessonPlayer/`

## Expected behavior

Render the static fallback composition shown by the ST-11 clean screenshot at the documented route `/student/lessons/:lessonId`. The page communicates that lesson content is not ready and offers the documented return links. It does not claim that lesson playback is available.

## Current behavior

- `apps/study-client/src/app/app.routes.ts` has Admin and root readiness routes only.
- There is no Student feature or ST-11 page in current source.
- The DD is marked blocked for a real loaded Lesson Player. Its supplied image and HTML describe a fallback state; player controls, lesson data, resources, progress, and next-lesson behavior are not specified for implementation.
- API catalog entries #24–#27 are draft/needs-confirmation and are outside this static UI scope.

## Scope

1. Add the ST-11 static fallback page using the existing Study Web Angular standalone conventions.
2. Add the documented preview route `/student/lessons/:lessonId` without interpreting the parameter or adding guards.
3. Match the supplied `images/screen-clean.png` composition and copy. Use existing Ocean design tokens and an inline/local SVG play decoration; do not add remote fonts, CDN assets, dependencies, or new icon packages.
4. Preserve the seven anchor destinations and labels documented in ST-11 HTML/DD. Destinations remain static links; no additional route behavior is promised.
5. Make the composition responsive and retain semantic headings, navigation landmarks, and keyboard-visible focus.

## Out of scope

- Lesson/player controls, playback, lesson-specific dynamic content, API calls (#24–#27), progress persistence, resource listing, next-lesson behavior, loading/error behavior, authentication/authorization, and Student destination screens.
- Replacing or changing the ST-11 DD, its images, or the existing shared icon registry.
- Adding/running tests in this task. Verification will be a production Angular build and visual route inspection if the local server can be started; test status remains `NOT_RUN`.

## Traceability

| Requirement | Evidence | Acceptance |
|---|---|---|
| R1: reproduce the static fallback composition | `images/screen-clean.png`, `images/README.md`, `code.html`, DD `01`–`06` | Header, breadcrumb, centered fallback card, CTA, and footer appear in the documented order and hierarchy. |
| R2: show the exact fallback message and CTA | DD `04_UI_Spec.md`, `code.html` | Static Vietnamese heading/body/CTA match source copy; no lesson controls or dynamic lesson fields appear. |
| R3: make the screen reachable for preview | DD `00-overview.md`, `apps/study-client/docs/list_screen.md` | `/student/lessons/:lessonId` renders the static page without consuming or validating the parameter. |
| R4: retain documented links and responsive layout | DD `04_UI_Spec.md`, `code.html`, frontend rules | Seven anchors keep source destinations; layout adapts to narrow viewports and keyboard focus remains visible. |

## Discrepancies and limits

- The DD status is `BLOCKED` for a functional lesson player. This implementation is only the provided fallback presentation; it does not resolve that blocker.
- Student routes and link destinations are absent from current source. Adding the single documented ST-11 preview route does not implement those destinations or access control.
- The screenshot uses remote Plus Jakarta Sans and Material Symbols. Project rules favor existing local styling; the implementation will use the configured system/Inter stack and local SVG, so glyph/font rendering may differ slightly while preserving layout.

## Open decisions

- None for the approved static fallback scope. Functional player behavior remains undecided and deferred.
