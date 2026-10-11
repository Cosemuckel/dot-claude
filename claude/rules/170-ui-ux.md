---
paths:
  - "**/*.{tsx,jsx,vue,svelte}"
  - "**/*.{css,scss,less}"
  - "**/components/**"
  - "**/pages/**"
  - "**/app/**"
---

# UI/UX and frontend design

Use these rules when changing user interfaces.

## Existing design system

Reuse the project's established components, tokens, spacing, typography, icons, and interaction patterns.

Do not invent a parallel design system.

Prefer consistency over novelty.

## States

Consider the relevant:
- loading;
- success;
- empty;
- error;
- disabled;
- permission-denied;
- partial-data;
- offline or degraded states.

## Accessibility

Prefer semantic HTML.

Ensure keyboard accessibility and visible focus.

Provide meaningful labels and names.

Use ARIA only when semantics cannot express the requirement naturally.

Maintain appropriate contrast and readable interaction states.

Do not rely on color alone to communicate important information.

## Responsive behavior

Consider the supported viewport sizes, long text, overflow, touch interaction, and layout degradation.

Do not optimize solely for the screenshot or viewport currently visible.

## Interaction quality

Prefer predictable, reversible interactions.

Avoid unnecessary modals, nested menus, hidden state, or surprising side effects.

Match the surrounding product's interaction patterns.
