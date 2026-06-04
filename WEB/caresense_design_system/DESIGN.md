---
name: CareSense Design System
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
  on-surface-variant: '#3d4947'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#5c5f61'
  on-secondary: '#ffffff'
  secondary-container: '#e0e3e5'
  on-secondary-container: '#626567'
  tertiary: '#924628'
  on-tertiary: '#ffffff'
  tertiary-container: '#b05e3d'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#773215'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  container-margin: 32px
  gutter: 24px
---

## Brand & Style
The design system is centered on "Compassionate Professionalism." It targets school administrators, counselors, and educators who require immediate, actionable insights into student well-being without feeling overwhelmed by clinical data.

The style is **Modern Corporate** with a heavy emphasis on **Softness and Clarity**. By utilizing a high-degree of whitespace and gentle elevation, the interface minimizes cognitive load and reduces the "alarmist" nature often associated with monitoring tools. The aesthetic response should be one of calm, control, and reliability, ensuring that even high-risk data is presented in a way that facilitates methodical action rather than panic.

## Colors
The palette is rooted in a professional Teal (`#0D9488`) to differentiate from standard "Finance Blue" while maintaining a sense of medical and psychological trust. 

- **Primary (Teal):** Used for navigation, primary actions, and branding elements.
- **Semantic Scales:** Success (Emerald), Warning (Amber), and Danger (Rose) are reserved strictly for risk-level indicators. These are tuned to high-vibrancy to ensure they stand out against the neutral slate background.
- **Neutrals:** A Slate-based scale is used for text and borders to maintain a cool, modern temperature.
- **Surface:** The primary background is a very light off-white (`#F8FAFC`) to reduce eye strain during long-form data review.

## Typography
This design system utilizes **Inter** for its systematic, utilitarian nature and exceptional legibility at small sizes—critical for dense dashboard tables and charts.

- **Headlines:** Use tighter letter-spacing and heavier weights to create a strong visual anchor.
- **Body:** Standardized at 16px for readability, with a 14px variant for secondary metadata.
- **Labels:** Uppercase styling is permitted for `label-md` to differentiate category headers and table headers from interactive content.
- **Numeric Data:** For gauges and stats, use `Inter` with tabular numbers enabled to ensure vertical alignment in lists.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid** model. The sidebar remains at a fixed width (280px) while the main content area utilizes a fluid 12-column grid.

- **Margins:** A generous 32px outer margin ensures the content feels "airy" and focused.
- **Gaps:** Gutters are set to 24px to provide clear separation between data cards.
- **Breakpoints:**
  - **Desktop (1280px+):** 12 columns, fixed sidebar.
  - **Tablet (768px - 1279px):** 6 columns, collapsed icon-only sidebar.
  - **Mobile (<767px):** 1-2 columns, bottom navigation bar or hamburger menu.
- **Vertical Rhythm:** Components are spaced in multiples of 8px to maintain a strict visual harmony.

## Elevation & Depth
This design system uses **Tonal Layers** combined with **Ambient Shadows** to create a sense of organized hierarchy.

- **Level 0 (Background):** Slate-50 (#F8FAFC).
- **Level 1 (Cards/Sidebar):** White (#FFFFFF) with a very soft, diffused shadow (0px 4px 20px rgba(0, 0, 0, 0.05)).
- **Level 2 (Modals/Popovers):** White (#FFFFFF) with a more pronounced shadow (0px 10px 30px rgba(0, 0, 0, 0.1)).
- **Outlines:** Subtle 1px borders in Slate-200 are used on input fields and secondary buttons instead of shadows to maintain a clean profile.

## Shapes
The shape language is defined by **High-Radius Geometry**. Standard components use a 0.5rem (8px) radius, but the primary container units—specifically Dashboard Cards—utilize a `rounded-2xl` (1.5rem / 24px) aesthetic to feel approachable and modern.

- **Buttons/Inputs:** 8px (Rounded) for a precise, functional feel.
- **Dashboard Cards:** 24px (Extra Rounded) to soften the data-heavy environment.
- **Gauges/Avatars:** Full circles (pill-shaped) to represent human-centric data.

## Components
Consistent component behavior is vital for a monitoring dashboard.

- **Cards:** White background, 24px corner radius, 24px internal padding. Titles should be `title-md` in Slate-900.
- **Gauges:** Semi-circular or circular progress bars. Use `Success` for 0-20% risk, `Warning` for 21-60%, and `Danger` for 61%+.
- **Buttons:** 
  - *Primary:* Teal background, white text.
  - *Secondary:* White background, Slate-200 border, Slate-700 text.
- **Inputs:** Height set to 44px for accessibility. 8px radius. Use a 2px Teal ring on focus.
- **Status Chips:** Low-opacity background versions of the semantic colors (e.g., Danger chip has a 10% opacity Rose background) with full-opacity text.
- **Sidebar:** Fixed left, Slate-900 background or pure white depending on preference (white recommended for "Soft" style), using 16px spacing between navigation items.
- **Sliders:** Used for adjusting thresholds. Thick track (8px) with a large, tactile thumb (24px diameter) for easy interaction.