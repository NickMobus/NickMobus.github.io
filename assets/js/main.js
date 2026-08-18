/*
  Reads projects.json and renders one card per project into #project-grid.

  To add a new project: open projects.json and add a new object to the
  array. Nothing here needs to change. See HOW_TO_ADD_A_PROJECT.md for
  the field-by-field walkthrough.

  Note: fetch() for a local file only works when the page is served over
  http(s) — either on GitHub Pages, or locally via a tool like VS Code's
  "Live Server" extension. Double-clicking index.html to open it directly
  (file://) will show "Couldn't load projects" because browsers block
  fetch() on local files for security reasons.
*/

async function loadProjects() {
  const grid = document.getElementById("project-grid");
  const countEl = document.getElementById("project-count");

  try {
    const response = await fetch("projects.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const projects = await response.json();

    if (!Array.isArray(projects) || projects.length === 0) {
      grid.innerHTML = '<p class="loading">No projects yet — add one to projects.json.</p>';
      countEl.textContent = "";
      return;
    }

    // Most recent first, if a "date" field is present.
    projects.sort((a, b) => (b.date || "").localeCompare(a.date || ""));

    grid.innerHTML = projects.map(renderCard).join("");
    countEl.textContent = `${projects.length} project${projects.length === 1 ? "" : "s"}`;
  } catch (err) {
    console.error("Failed to load projects.json:", err);
    grid.innerHTML =
      '<p class="error">Couldn\'t load projects. If you\'re viewing this file directly ' +
      "from your computer, that's expected — see the note in assets/js/main.js. " +
      "This works normally once the site is live on GitHub Pages.</p>";
  }
}

function renderCard(project) {
  const {
    title = "Untitled project",
    description = "",
    tags = [],
    status = "",
    date = "",
    link = "#",
    external = false,
  } = project;

  const tagsHtml = tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join("");
  const linkLabel = external ? "View repo \u2197" : "Open project \u2192";
  const rel = external ? ' target="_blank" rel="noopener"' : "";

  return `
    <a class="project-card" href="${escapeAttr(link)}"${rel}>
      <div class="card-top">
        <span>${escapeHtml(date)}</span>
        ${status ? `<span class="card-status">${escapeHtml(status)}</span>` : ""}
      </div>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(description)}</p>
      <div class="card-tags">${tagsHtml}</div>
      <span class="card-link-label">${linkLabel}</span>
    </a>
  `;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function escapeAttr(str) {
  return escapeHtml(str).replace(/"/g, "&quot;");
}

document.getElementById("year").textContent = new Date().getFullYear();
loadProjects();
