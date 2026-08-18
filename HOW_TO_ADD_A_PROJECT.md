# How to add a new project

You never need to touch `index.html`, the CSS, or the JS to add a project.
Everything is driven by one file: **`projects.json`**.

## Adding a project that lives in another GitHub repo

Open `projects.json` in VS Code and add a new block inside the `[ ]` array
(don't forget the comma after the previous entry's closing `}`):

```json
{
  "title": "Your project's name",
  "description": "One or two sentences on what it does and what you used.",
  "tags": ["Tag One", "Tag Two"],
  "status": "Complete",
  "date": "2026",
  "link": "https://github.com/NickMobus/your-other-repo",
  "external": true
}
```

- `link` — the GitHub repo URL, or that repo's own GitHub Pages URL if it has one.
- `external: true` — makes the card open in a new tab (since it's leaving this site).
- `status` — whatever's true: `"Complete"`, `"In progress"`, `"Archived"`, etc.
- `date` — used to sort the grid (most recent first). Just the year is fine.

## Adding a project that lives inside this repo

1. Create a new folder under `projects/`, e.g. `projects/my-new-project/`.
2. Put that project's `index.html` (and any images/data it needs) inside that folder.
3. Add a block to `projects.json` like the one above, but with:
   - `"link": "projects/my-new-project/index.html"`
   - `"external": false` (or just omit it)

## Checking it worked

Commit and push your change to GitHub, wait ~a minute for GitHub Pages to
rebuild, then check `https://nickmobus.github.io`. The new card should
appear in the grid automatically.

If you want to preview locally before pushing: opening `index.html` by
double-clicking it won't load the project cards (browsers block that for
local files). Install the **Live Server** extension in VS Code, right-click
`index.html`, and choose "Open with Live Server" instead.
