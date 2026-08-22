# Task — Extract `<Button>` from a single-page component

Goal: replace the inline button JSX in `src/Page.tsx` with a reusable,
typed `<Button>` component so future pages can call `<Button label="..."
onClick={...} />` without re-typing the styling.

This task does **not** refactor `Page.tsx`'s logic; it only swaps the inline
`<button>` element for the new component.

## Acceptance criteria

1. **Given** the new `Button` component is rendered with `label="Save"`
   **When** the component is mounted in a test
   **Then** it renders a `<button>` element whose accessible name is "Save".

2. **Given** the `Button` is rendered with `variant="secondary"`
   **When** the test queries the rendered element
   **Then** it has the CSS class `btn btn--secondary`.

3. **Given** the `Button` is rendered with an `onClick` handler
   **When** a user clicks the button
   **Then** the handler is called exactly once.

## Out of scope

- Changing `Page.tsx`'s state, effects, or non-button markup.
- Adding a new styling system, theme provider, or CSS-in-JS library.
- Adding icon support, loading spinners, or disabled-state logic.
- Refactoring any other component in the project.
- Updating build, lint, or Vitest configuration.