# Migrating your existing repo to this structure

These steps use VS Code's file explorer (drag-and-drop), not the terminal.

## 1. Create the new folder

In VS Code's Explorer panel (left sidebar), right-click your repo's root
folder → **New Folder** → name it `projects`. Inside `projects`, make
another folder named `ocean-acidification`.

## 2. Move the old project's files in

Your current `index.html` and all its supporting files (the notebooks,
the PNG charts, the CSV/JSON data files) all belong to the ocean
acidification project. Select them in the Explorer:

- `index.html`
- every `.ipynb` file
- every `.png` file
- `BCO_DMO_data.csv`, `global_monthly_co2_1980_2024.csv`,
  `monthly_average_BATS_cleaned.csv`
- `co2_raw_data_1980_2024.json`
- `bats_dataset_head.html`

Drag them all into `projects/ocean-acidification/`. (Click the first file,
then Ctrl/Cmd-click the rest to multi-select before dragging.)

## 3. Add the new hub files

Unzip the files I've given you and copy them into your repo's **root**
folder (the top level, next to `projects/`):

- `index.html` (this replaces your old one — the old one already moved
  to `projects/ocean-acidification/` in step 2)
- `assets/` (the whole folder — CSS and JS)
- `projects.json`
- `HOW_TO_ADD_A_PROJECT.md`

## 4. Update the README (optional but recommended)

Your current README still says "Machine Learning for DTSC Website." You
may want to update it to describe the site as your general project hub,
and mention that the DTSC project now lives in `projects/ocean-acidification/`.

## 5. Commit and push

In VS Code's Source Control panel: stage all the changes, write a commit
message like `Restructure site into project hub`, commit, then push.
Give GitHub Pages a minute to rebuild, then check
`https://nickmobus.github.io`.

## 6. Sanity check

- Homepage loads and shows one project card (ocean acidification).
- Clicking that card opens the tabbed report exactly as it looked before.
- Nothing under `projects/ocean-acidification/` needs to change — its
  image paths are relative to itself, so moving the whole folder together
  keeps everything working.
