# Study2Work Design System

`CONTEXT_STATUS: SOURCE_BACKED_DESIGN_BASELINE`

Đây là nguồn chuẩn thị giác và UX cho Work Web, Flutter Student và Flutter
Business. Thiết kế mới phải đọc tài liệu này trước khi sửa component. Design
system chỉ thay đổi presentation và interaction state; không tự tạo route, API,
database field, persistence hoặc business flow mới.

## Design direction

- Tinh thần: professional, rõ ràng, tin cậy và tập trung vào hành động chính.
- Màu chủ đạo: cobalt blue trên nền sáng, sử dụng gradient tiết chế chỉ cho
  hero/banner khi cần tạo hierarchy.
- Surface ưu tiên phẳng, border nhẹ và shadow thấp; tránh glassmorphism, neon
  hoặc nhiều màu accent cạnh tranh với hành động chính.
- Student và Business dùng cùng hệ thống; khác nhau ở nội dung, quick action và
  icon/context, không tạo hai visual language riêng.

## Color tokens

| Token | Value | Usage |
|---|---|---|
| `primary` | `#1D4ED8` | brand, active state, primary text action |
| `primary-action` | `#2563EB` | button, link, focus accent |
| `primary-soft` | `#EFF6FF` | selected surface, badge background |
| `navy` | `#0F172A` | heading, navigation, dark footer |
| `background` | `#F8FAFC` | page/app background |
| `surface` | `#FFFFFF` | cards, forms, dialogs |
| `border` | `#E2E8F0` | divider, input/card border |
| `muted` | `#64748B` | secondary text, placeholder, metadata |
| `success` | `#16A34A` | success/active status |
| `warning` | `#D97706` | pending/attention status |
| `danger` | `#DC2626` | error/destructive action |
| `info` | `#0284C7` | informational state |

Primary buttons use `primary-action` with white text. Body text must remain
`navy` or a contrast-safe dark neutral; `muted` is not used for essential
content. Status colors are semantic and must not be used as decorative accents.

## Typography

### Web

- Body: existing `Inter` font.
- Display/heading: existing `Poppins`, weight 600–800.
- Body line-height: 1.5–1.7; headings use compact line-height around 1.15.
- Use sentence case for labels and headings; uppercase is reserved for short
  eyebrow/status labels.

### Flutter

- Use Material 3 typography and the platform-safe default font; do not add a
  font package.
- Page title: `headlineSmall`/`titleLarge`; section title: `titleMedium`; body:
  `bodyMedium`; metadata: `bodySmall`.
- Do not put important information in color alone, all-caps text or truncated
  labels.

## Layout and component tokens

- Spacing follows a 4px base: `4, 8, 12, 16, 20, 24, 32, 40, 48`.
- Small control radius: 8px; input/button radius: 10–12px; card radius:
  16px; hero/banner radius: 20–24px; pill radius: 999px.
- Primary control height: minimum 44px Web and 48px Flutter. Icon-only controls
  have a minimum 44×44px hit area.
- Use one low elevation for cards and one raised elevation for menus/dialogs;
  borders are preferred over heavy shadows.
- Content width Web: approximately 1120–1200px with fluid side padding. Avoid
  full-width text blocks on desktop.
- Web breakpoints: mobile `<768px`, tablet `768–1023px`, desktop `>=1024px`.
  Layout must reflow; do not merely hide primary navigation or actions.

## Surface patterns

- Public landing: concise hero with one primary CTA, one secondary CTA and a
  searchable job discovery area.
- Role/auth: single clear decision per view, visible role context, labeled fields,
  inline validation and a predictable secondary action.
- Workspace: role-aware header/app shell, page header, primary action, then data
  surface. Student prioritizes discover/apply/profile; Business prioritizes
  publish/manage/review.
- List/card: title, company/person, metadata, status and one clear next action;
  preserve readable hierarchy on narrow screens.
- Form: labels above fields, stable spacing, visible focus/error/success state,
  grouped fields and actions aligned at the end on desktop.
- Chat: obvious conversation header, readable message grouping, composer with
  send affordance, empty/loading/error states that do not imply real-time
  delivery when the implementation is polling.
- Loading/error/empty: use consistent iconography, short explanation and one
  recovery action where recovery is available.

## Interaction and accessibility

- Every interactive element has hover, pressed, focus-visible, disabled and
  loading behavior appropriate to its platform.
- Keyboard focus must be visible on Web; tab order follows visual/task order.
- Images have meaningful alt/semantic labels; decorative images are hidden from
  assistive technology.
- Target WCAG AA contrast for text and controls. Never communicate status only
  through red/green/blue color.
- Respect `prefers-reduced-motion` on Web and avoid non-essential animation in
  Flutter. Preserve existing loading animation only when it helps orientation.
- Inputs must remain usable with keyboard/IME, scrolling content must not be
  obscured, and error text must be associated with the relevant field.

## Role and content rules

- Keep the same route, API field, query/mutation, authentication and navigation
  semantics already present in the source.
- Presentation copy may be clarified in Vietnamese for labels, hints, loading,
  empty and error states. Do not rewrite server data or invent backend behavior.
- Screens whose API is not wired remain explicitly static/placeholder screens;
  their visual polish must not suggest that a change was persisted remotely.
- Use existing Study2Work logo, background and illustration assets. Do not add
  a new package, font, image library or external design dependency.

## Implementation mapping

- Web tokens and responsive primitives live in `src/styles/main.css` and
  `src/shared/ui/`; page components consume semantic classes/components instead
  of introducing local color systems.
- Each Flutter app gets its own `lib/theme/` and local UI primitives. The apps
  remain independent packages even though their tokens and component behavior
  are aligned.
- Existing API/auth/data helpers remain the source of truth. UI refactors must
  not modify Neon/SQLite/Gemini boundaries or chat polling behavior.
