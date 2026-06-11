---
title: UI
---

# UI

Remove this section if {{cookiecutter.project_name}} has no user interface.

## Overview

Describe the UI layer — component structure, rendering approach, and how it connects to the core library.

## Component Structure

```
src/
└── {{cookiecutter.project_slug}}/
    └── ui/
        ├── components/     # reusable primitives
        ├── views/          # page-level compositions
        └── __init__.py     # public UI exports
```

## State Management

Describe how UI state is managed and how it stays in sync with library state.

## Theming & Styling

Describe the styling approach and how consumers can customize the appearance.

## Accessibility

Describe your accessibility baseline (WCAG level, ARIA patterns, keyboard navigation support).

## Design Decisions

Document any non-obvious UI architecture choices.
