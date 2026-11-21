---
name: Study2Work LMS
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#784b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#996100'
  on-tertiary-container: '#ffeedd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system targets learners transitioning into professional careers, alongside industry mentors and academic administrators. The visual tone balances scholastic rigor with the polish of a modern productivity tool: serious enough to validate real career advancement, yet warm and encouraging enough to sustain long-term engagement.

The design language sits within **Corporate / Modern EdTech** with refined tactile touches. Visual clutter is stripped away in favor of high-legibility typographic scale, structured modular cards, and confident functional color coding. Interfaces should evoke clarity, steady momentum, and professional competence without feeling cold, intimidating, or clinical.

## Colors

The palette is engineered for WCAG AA compliance across all critical interaction paths:

- **Primary (`#2563EB`)**: Anchor blue representing trust and momentum. Utilized for primary calls-to-action, active navigation nodes, and high-priority interactive elements.
- **Secondary (`#10B981`)**: Vivid emerald green reserved for learning progress bars, completion checkmarks, quiz masteries, and positive grade indicators.
- **Tertiary (`#F59E0B`)**: Warm amber for upcoming assignment deadlines, review requests, streak trackers, and warning notices.
- **Neutrals**: Grounded in cool slate (`#0F172A` deep text, `#1E293B` heavy headings, `#64748B` supporting body/labels, `#E2E8F0` structural borders, `#F8FAFC` foundation canvas). High contrast ensures reading stamina across intensive study sessions.

Interactive states must always use luminosity shifts rather than opacity shifts to preserve text contrast ratios against backgrounds.

## Typography

The design system relies on **Plus Jakarta Sans** across all roles. Its geometric foundation provides clean readability for course catalogs, data grids, and code snippets, while its subtle humanist curves maintain warmth during long reading sessions.

- **Headlines & Titles**: Tight negative tracking (`-0.01em` to `-0.02em`) creates crisp, magazine-grade headers on desktop dashboards.
- **Body Content**: Set to generous line heights (`1.5x` minimum) to promote relaxed scannability in lesson texts, assignment prompts, and peer feedback feeds.
- **Labels & Microcopy**: Slightly elevated weights (`600` and `700`) paired with subtle positive letter spacing maintain instant legibility at sizes down to 11px on module status tags and progress markers.

## Layout & Spacing

A strict 8px/4px spatial grid governs the rhythm of the design system:

- **Desktop (>= 1280px)**: 12-column responsive fluid grid with `2rem` page margins and `1.5rem` gutters. Maximum application canvas caps at 1440px for learning content readability.
- **Tablet (768px - 1279px)**: 8-column layout with `1.5rem` margins and `1rem` gutters. Sidebars fold into collapsible utility rails.
- **Mobile (< 768px)**: 4-column layout with `1rem` outer canvas padding. Complex metrics, assignment grids, and video layout panels collapse into single-column vertical stacks.

All interior component distances rely strictly on the `space-*` tokens. Grouped form labels and inputs utilize `space-xs` (4px) to `space-sm` (8px), card interior sections utilize `space-md` (16px) or `space-lg` (24px), and major content cards separate with `space-xl` (32px).

## Elevation & Depth

Visual hierarchy uses **tonal surfaces combined with subtle, cool-slate ambient shadows** rather than heavy drop shadows:

- **Level 0 (Canvas Base)**: `#F8FAFC`. Default page foundation.
- **Level 1 (Card & Content Surface)**: Solid `#FFFFFF` bordered by a crisp `1px solid #E2E8F0` stroke with an ambient resting shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.05)`.
- **Level 2 (Hover / Elevated Cards)**: `0 4px 12px -2px rgba(15, 23, 42, 0.08)`. Applied on mouseover for interactive course cards, actionable tasks, and dropdown containers.
- **Level 3 (Modals / Slide-over Drawers)**: `0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.08)` accompanied by an accessible backdrop scrim (`rgba(15, 23, 42, 0.4)`).

Border outlines provide structural clarity, ensuring high visibility under varied lighting or low-contrast display environments.

## Shapes

The system standardizes on a **Rounded (Level 2)** shape cadence to deliver a modern, inviting software experience:

- **Controls & Small Components (8px / `0.5rem`)**: Form text inputs, standard buttons, dropdown menus, and alert banners.
- **Cards & Modules (12px to 16px / `0.75rem` to `1rem`)**: Course cards, gradebook summaries, video player containers, and modal dialogs.
- **Pill Elements (9999px / Fully Rounded)**: Status chips, user achievement badges, filter pills, and circular avatar wrappers.

## Components

### Buttons
- **Primary**: Solid `#2563EB` fill with `#FFFFFF` text. Height of 40px (desktop), 8px border radius, font `label-lg`. Hover darkens to `#1D4ED8`; focus ring presents a 2px offset with `#93C5FD`.
- **Secondary / Outline**: `#FFFFFF` background with `1px solid #CBD5E1` border and `#1E293B` text. Hover shifts background to `#F1F5F9`.
- **Destructive**: Solid `#EF4444` fill with `#FFFFFF` text for permanent grade/submission deletions.

### Inputs & Form Controls
- **Idle State**: Height 42px, background `#FFFFFF`, border `1px solid #CBD5E1`, text `#0F172A`, placeholder `#94A3B8`.
- **Focused State**: Border `1px solid #2563EB`, outer glow shadow `0 0 0 3px rgba(37, 99, 235, 0.15)`.
- **Error State**: Border `1px solid #EF4444`, outer shadow `0 0 0 3px rgba(239, 68, 68, 0.15)`, accompanied by explicit error text in `#DC2626` below.
- **Success State**: Border `1px solid #10B981`, checkmark iconography within trailing slot.

### Cards
- Base surface `#FFFFFF`, border `1px solid #E2E8F0`, rounded 12px.
- Distinct header, body, and footer dividers utilizing `#F1F5F9` sub-panels for metadata like instructor avatars, duration tags, and progress percentages.

### Chips & Badges
- **Status Pills**: 24px height, full pill radius. 
  - *Completed*: `#ECFDF5` background, `#047857` text, 12px semi-bold.
  - *In Progress*: `#EFF6FF` background, `#1D4ED8` text.
  - *Pending / Due Soon*: `#FFFBEB` background, `#B45309` text.

### Checkboxes & Radio Buttons
- 18px square (checkbox) or circle (radio), 1.5px border `#94A3B8`. 
- Active state fills with `#2563EB` containing a high-contrast white check or dot.

### Specialized EdTech Components
- **Progress Trackers**: 8px height track with `#E2E8F0` fill; indicator bar fills with `#10B981` (learning completion) or `#2563EB` (module progression).
- **Grade Indicators**: Modular badge display featuring bold font scale (`headline-md`) alongside mentor rubric taglines.