# Study Web Design System

```text
STATUS: INTENDED_DESIGN_TARGET
THEME: LIGHT_FIRST
SCOPE: STUDY_WEB_ONLY
```

## Scope and authority

- Apply this guide to the Study Web front end only. It is the canonical visual
  target for Study Web UI, UX, graphic design, layout, styling and frontend
  implementation tasks.
- Read this page before planning or changing any Study Web visual or frontend
  work. Follow its tokens and interaction rules unless the user approves a
  specific exception.
- This page defines intended design, not current runtime behavior. The current
  checkout does not contain `apps/study-client/`; do not use this page as
  evidence that a screen, route, interaction or API integration exists.
- `.agents/project/design.md` remains the design source for Work Web and Work
  Mobile. This Study Web guide defines a separate ocean-blue visual identity
  and must not be applied to those apps by default.
- Design decisions do not authorize new routes, features, API fields, data
  flows, persistence or backend behavior.

## Design direction

Study Web should feel calm, polished and welcoming. Keep the learning content
easy to scan, use generous whitespace and make the next useful action obvious.
Use simple surfaces and restrained accents; avoid a childish look, dense
decoration, glass effects, neon, heavy shadows and large gradients. Use the
light theme as the baseline. Dark theme design is outside this guide's scope.

## Color tokens

Use semantic tokens consistently instead of adding page-specific hex values.
Primary and text colors below have been checked against white for WCAG AA
normal-text contrast. The bright sky accent is decorative and must not carry
essential text or status information.

| Token | Value | Use |
|---|---|---|
| `ocean-primary` | `#0B5F8A` | Primary actions, active navigation, links and focus ring |
| `ocean-hover` | `#084968` | Hover and pressed emphasis for primary actions |
| `ocean-deep` | `#073B57` | Strong headings and selected dark accents |
| `sky-accent` | `#43A5C5` | Small decorative highlights only |
| `ocean-soft` | `#E8F4FA` | Selected and informational backgrounds |
| `page-background` | `#F6FAFC` | Main page background |
| `surface` | `#FFFFFF` | Cards, inputs, menus and dialogs |
| `text-primary` | `#17324D` | Headings and primary body text |
| `text-muted` | `#536A7A` | Secondary text and metadata |
| `border` | `#D4E2E9` | Dividers and quiet surface boundaries |
| `success` | `#18794E` | Success state, paired with text or an icon |
| `warning` | `#8A4B08` | Warning state, paired with text or an icon |
| `danger` | `#B42318` | Error/destructive state, paired with text or an icon |

Use white text on `ocean-primary` and `ocean-hover`; use `text-primary` or
`text-muted` on light surfaces. Do not use `sky-accent` or `border` alone for
small text, important control boundaries or focus indication. Do not encode
success, warning or error through color alone.

## Typography

- Use `Inter` when it is already available; otherwise use the system sans-serif
  stack. Do not add a remote font import or package for this guide.
- Use sentence case. Keep body text at 16px or larger where practical, with
  line-height around 1.55–1.7. Use compact heading line-height around 1.15–1.3.
- Use 600–700 weight for headings and key actions. Reserve bold weight for
  emphasis; avoid long all-caps labels and overly light text on pale surfaces.
- Keep long reading text near 65–75 characters per line on wide screens.

## Layout and surfaces

- Use a 4px spacing rhythm: `4, 8, 12, 16, 24, 32, 40, 48, 64`.
- Use a content width up to about 1120px, centered with responsive gutters:
  16px on narrow screens, 24px on tablet and 32px on desktop.
- Reflow at mobile `<768px`, tablet `768–1023px` and desktop `>=1024px`;
  retain access to primary content and actions at every width.
- Prefer flat white surfaces, subtle borders and low, diffuse shadows. Use
  8–12px radius for controls and 12–16px for cards. Avoid multiple competing
  elevations or decorative gradients behind reading content.
- Keep controls at least 44px high and icon-only controls at least 44×44px.
  Use a consistent 20–24px line-icon size and stroke style; do not use emoji as
  interface icons.
- Keep the visual hierarchy consistent: page title, short supporting context,
  main content, then secondary actions. Do not invent page-specific workflows
  from this design guide.

## Interaction and motion

| Motion token | Duration | Use |
|---|---:|---|
| `motion-quick` | 140ms | Hover, focus and pressed feedback |
| `motion-standard` | 200ms | Menus, controls and surface-state changes |
| `motion-enter` | 280ms | Short page or content transitions when they aid orientation |

Use `cubic-bezier(0.22, 1, 0.36, 1)` for these transitions. Prefer opacity,
color and subtle shadow changes; any entrance translation should stay within
4px. Keep state feedback immediate, do not shift surrounding layout, and avoid
parallax, autoplay and looping decorative motion. Under
`prefers-reduced-motion: reduce`, remove nonessential entrances and transforms
while keeping clear immediate state feedback.

Every interactive control must have appropriate hover, focus-visible, pressed,
disabled and loading states. Use semantic buttons and links, preserve normal
keyboard operation, and never make color or animation the only explanation of
a state.

## Accessibility and content

- Meet WCAG AA contrast: at least 4.5:1 for normal text and 3:1 for large text,
  meaningful icons and control boundaries. Recheck composed states rather than
  assuming a token remains accessible on every background.
- Show a clear keyboard focus indicator with sufficient contrast; keep tab
  order aligned with task order and ensure sticky elements do not cover focus.
- Associate visible labels and help/error text with form controls. Give
  icon-only actions accessible names and expose expanded/selected/disabled
  state where applicable.
- Use headings in order, meaningful alt text for informative images and
  hidden semantics for decorative graphics. Support reflow at 320 CSS pixels
  and browser zoom without loss of content or actions.
- Write concise, warm and direct copy. Prefer clear next steps over vague
  encouragement; keep empty, loading and error states honest about whether an
  action is available or has completed.

## Review checklist

- The page feels calm, minimal and welcoming; the primary action is easy to
  find without competing accents.
- Semantic tokens are used consistently and text/control contrast is checked
  on its actual surface.
- Layout reflows without hiding primary content; controls meet the stated hit
  area and keyboard-focus requirements.
- Motion is short, stable and optional; reduced-motion preferences are
  respected.
- No new route, API behavior, data flow, dependency or backend claim was
  introduced by visual design alone.
