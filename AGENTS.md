# Repository Guidelines

## Project Structure & Module Organization

This repository documents a 60-day Claude/AI learning challenge. Each day lives in its own folder, for example `Day1/`, `Day2/`, `Day-3/`, `day-4/`, and `day10/`. Day folders usually contain a Markdown journal such as `day7/day7.md`, optional standalone HTML demos such as `day10/day10.html`, and local image assets such as `day6/image.png`. The `vercel-deploy/` folder contains the deployable portfolio page (`index.html`) and its assets (`profile.jpg`).

When adding a new day, keep all related files in a single day folder. Prefer a consistent pattern such as `day11/day11.md`, `day11/day11.html`, and `day11/image.png`.

## Build, Test, and Development Commands

There is no package manifest or compiled build step in the current project. Most pages are static HTML and can be opened directly in a browser.

- `git status --short`: check changed files before committing.
- `rg --files`: list tracked project files quickly.
- `npx prettier --check "**/*.{html,md}"`: optional formatting check if Prettier is available.
- `npx prettier --write "**/*.{html,md}"`: optional formatting pass for edited HTML/Markdown files.

For `vercel-deploy/index.html`, verify changes by opening the file locally and checking desktop and mobile widths.

## Coding Style & Naming Conventions

Use two-space indentation in HTML, CSS, and JavaScript blocks. Keep standalone HTML self-contained unless a shared asset is already present in the same folder. Use lowercase folder names for new day entries (`day11`, `day12`) to avoid adding more naming variants.

For Markdown, use sentence-case headings, short sections, and relative links to local assets. Keep image filenames simple and descriptive, for example `profile.jpg`, `dashboard.png`, or `prompt-flow.png`.

## Testing Guidelines

No automated test suite is configured. Validate changes manually:

- Open changed `.html` files in a browser.
- Test navigation links, buttons, forms, and theme toggles where present.
- Confirm local image paths resolve from the HTML file location.
- Scan Markdown previews for broken headings, encoding issues, and missing images.

## Commit & Pull Request Guidelines

Recent commits use short, day-focused messages such as `Day 9 - AI Nutrition Analytics App` and `day10_work done`. Prefer clear messages that identify the day and outcome, for example `Day 11 - Add prompt engineering notes`.

Pull requests should include a short summary, list changed day folders, mention any new assets, and include screenshots for visual HTML changes. Link related issues or challenge notes when applicable.

## Security & Configuration Tips

Do not commit private API keys, tokens, resumes with sensitive data, or unpublished contact details. If a demo needs external services, document required configuration in that day folder instead of hardcoding secrets.
