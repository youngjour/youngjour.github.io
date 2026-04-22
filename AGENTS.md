# AGENTS.md — Content update rules

This repo is a bilingual (Korean root / English `/en/`) Quarto site. Most
of the site's facts are now driven by `_data/*.yml` — a single build
step (`python scripts/build.py`) renders `_includes/*.qmd` and the
`llms.txt` file from that data. A few sections (design narratives,
teaching course prose, the About-page introduction) remain hand-written
in `.qmd`.

**Read this file before modifying any content**, whether you are the site
owner or a coding agent.

## Core principles

1. **Korean and English are a coupled pair.** Whenever a fact has both
   `.ko` and `.en` forms in a data file, keep them in sync. If a change
   affects only one language (e.g. a typo fix), still read the
   counterpart field to make sure nothing diverges.
2. **Most facts live in `_data/*.yml` (the SSOT).** Publications,
   projects, patents, profile / identifiers, education, career, awards,
   professional service, and course metadata are all sourced from there.
   The site's `_includes/*.qmd` files and `llms.txt` are **generated
   outputs** — never hand-edit them.
3. **The hand-written parts are deliberately narrow.** Only the
   About-page `## Introduction` paragraph, the long teaching course
   descriptions under `## Courses` in `teaching.qmd`, the design
   narratives in `design.qmd`, `Student Collaborations` in
   `teaching.qmd`, and site configuration (`_quarto.yml`, navbar, SCSS)
   live in `.qmd` or config files.
4. **CV PDFs are derived artifacts.** `assets/cv_en.pdf` and
   `assets/cv_ko.pdf` are rendered from the same `_data/*.yml` by
   `scripts/build_cv.py` (Typst + the `pro-academic-cv` template — see
   `cv/cv.typ`). Any change to profile, education, career,
   publications, projects, patents, awards, service, or teaching
   automatically shows up in the next CV build. Do not hand-edit the
   PDFs.
5. **When in doubt, run the build.** `python scripts/build.py` is fast
   and deterministic. Run it before you commit data changes; commit the
   regenerated `_includes/*.qmd` and `llms.txt` alongside the data
   change.

## File cheat sheet — where facts live

| Fact type                                  | SSOT / file                           | Shows up on                                     |
|--------------------------------------------|---------------------------------------|--------------------------------------------------|
| Name, byline, Korean name, blockquote      | `_data/profile.yml`                   | `llms.txt`                                       |
| Identifiers (ORCID, Scholar, email, etc.)  | `_data/profile.yml`                   | `llms.txt` (site `about.links` still in `index.qmd`) |
| Current affiliations                       | `_data/profile.yml`                   | `llms.txt`                                       |
| Education                                  | `_data/education.yml`                 | About page (both langs), `llms.txt`, CV          |
| Career history                             | `_data/career.yml`                    | About page (both langs), `llms.txt`, CV          |
| Awards / honors                            | `_data/awards.yml`                    | About page (both langs), CV                      |
| Professional service                       | `_data/service.yml`                   | About page (both langs), `llms.txt`              |
| Publication (paper / talk / poster)        | `_data/publications.yml`              | Research page, About-page highlights (if `highlight:`), `llms.txt`, CV |
| Research project / grant                   | `_data/projects.yml`                  | Research page, About-page highlights (if `highlight: true`), `llms.txt`, CV |
| Patent / copyright / IP                    | `_data/patents.yml`                   | Research page, About page, `llms.txt`, CV       |
| Course (graduate-level)                    | `_data/teaching.yml` (metadata only); `teaching.qmd` (prose) | Teaching page (prose), CV            |
| Invited lecture / seminar (institution)    | `_data/service.yml` (`invited_lectures`) | About page "Professional Service"; `teaching.qmd` also lists them as prose |
| Student collaboration                      | `teaching.qmd`, `en/teaching.qmd`     | Teaching page                                    |
| Design / architecture project              | `design.qmd`, `en/design.qmd`         | Design page                                      |
| About-page Introduction paragraph          | `index.qmd`, `en/index.qmd` (prose)   | About page                                       |
| Site config (navbar, footer icons, theme)  | `_quarto.yml`, `en/_quarto.yml`       | Everywhere (layout / styling)                    |

## Change-type checklists

### Adding a publication

Publications live in `_data/publications.yml`. The Research page,
About-page highlights, and `llms.txt` are all generated from it.

- [ ] `_data/publications.yml` — add the entry at the top of the
      `publications:` list. Required fields: `id`, `year`, `type`,
      `authors`, `title`, `venue.ko`, `venue.en`, `status`. Bold the
      owner as `**Park, Youngjun**`. Use long-form author names — the
      build script derives the `Park, Y.` short form for `llms.txt`.
- [ ] If the paper is a highlight (should appear on the About page),
      set `highlight:` with `period.{ko,en}` (must exactly match a
      label in `research_work_periods`), `venue_short`, `summary.{ko,en}`,
      and — optionally — `rank` (integer; lower sorts first within the
      period) and `author_label` (override for non-default citations
      like "Park, Han et al.").
- [ ] Run `python scripts/build.py`. Review the diff under `_includes/`
      and the "Publications" section of `llms.txt`.
- [ ] Verify DOI / URL resolves (HEAD request returns 200).
- [ ] Commit `_data/publications.yml`, the regenerated `_includes/*.qmd`,
      and `llms.txt` together.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Adding a research project / grant

- [ ] `_data/projects.yml` — add the entry. Required fields: `id`,
      `title.{ko,en}`, `period`, `research_meta.{ko,en}`, `llms_line`.
- [ ] If top-5 impactful, set `highlight: true` and add `index_meta.{ko,en}`
      plus `index_summary.{ko,en}`. At most 5 projects may be highlighted
      at once (the build will fail otherwise).
- [ ] Run `python scripts/build.py`. Review diffs under `_includes/` and
      in `llms.txt`.
- [ ] Commit `_data/projects.yml`, `_includes/*`, and `llms.txt` together.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Adding a patent / copyright

- [ ] `_data/patents.yml` — add the entry. Required fields: `id`, `kind`
      (`patent` or `copyright`), `status` (`filed` or `registered`),
      `jurisdiction` (e.g. `KR`), `number`, `title.{ko,en}`.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] Commit `_data/patents.yml`, `_includes/*`, and `llms.txt` together.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Changing a career position (new role, end date, affiliation)

- [ ] `_data/career.yml` — edit the existing entry or add a new one.
      Required fields per entry: `id`, `title.{ko,en}`, `employer.{ko,en}`,
      `period.{ko,en}`. `bullets.{ko,en}` are optional — use `bullets: null`
      for positions that only show role + period.
- [ ] If the llms.txt form of the role or employer differs from the
      English site (e.g. "Co-founder and CTO" vs "Co-founder · CTO"),
      add `title.llms` / `employer.llms` overrides. Period is
      auto-normalised to llms form ("Present" → "present"; spaces
      around en-dash stripped) — override `period.llms` only if the
      auto-form is wrong.
- [ ] If this change also affects the "Current affiliations" list in
      `llms.txt` or the blockquote summary, update
      `_data/profile.yml` (`current_affiliations` and `summary_llms`).
- [ ] If the title changed enough to warrant a new site subtitle, also
      update `_quarto.yml` and `en/_quarto.yml` `navbar.title` /
      `subtitle`, and `README.md` top-line description.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Updating education

- [ ] `_data/education.yml` — edit the entry or add a new one. Required
      fields: `id`, `degree.{ko,en}`, `institution.{ko,en}`, `year`. If
      the entry has a sub-detail (dissertation / thesis), add
      `detail_label.{ko,en}` and `detail.{ko,en}`, plus an optional
      `detail.llms` override if the llms form is more concise than the
      English site form.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Adding an award

- [ ] `_data/awards.yml` — add the entry. Required fields: `id`, `year`,
      `category` (must match one of the declared `award_categories`),
      `title.{ko,en}`, `context.{ko,en}`. Category `academic` renders
      as a bold bullet; `sports` renders as a plain bullet.
- [ ] If the award warrants a new category, add one to
      `award_categories` at the top of the file — the build errors if
      an award references an unknown category.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Updating professional service

- [ ] `_data/service.yml` — edit the relevant section under `service:`
      (`journal_reviewer`, `research_advisory`,
      `industry_collaborations`, `invited_lectures`). Each section has
      `.ko` and `.en` lists; leave `.en: []` to reuse `.ko` when the
      lists are identical.
- [ ] If a new display label is needed (e.g. renaming "Journal Reviewer"
      to something else), edit the `labels:` block at the top of the
      file. Each label has `.ko` / `.en` / `.llms` forms;
      `invited_lectures.llms: null` keeps that section out of
      `llms.txt`.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] CV re-export if the change affects a CV-visible section.

### Updating identifiers (ORCID, Google Scholar, email, ar-ge URL)

- [ ] `_data/profile.yml` — edit `identifiers`. The build regenerates
      the `## Identifiers` block in `llms.txt` from these values.
- [ ] `index.qmd` / `en/index.qmd` `about.links` — update (site
      sidebar still hand-written).
- [ ] `_quarto.yml` / `en/_quarto.yml` footer icons — update if the
      icon URL changed.
- [ ] `README.md` "Contact" — update.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] CV re-export if the identifier appears on the CV.

### Adding a course (graduate level)

Course **prose** (syllabus, weekly tables, readings) stays hand-written
in `teaching.qmd`. Course **metadata** (title, institution, level,
years) goes into `_data/teaching.yml` so the CV can pick it up.

- [ ] `_data/teaching.yml` — add the entry with `id`, `title.{ko,en}`,
      `institution.{ko,en}`, `level.{ko,en}`, `years`.
- [ ] `teaching.qmd` + `en/teaching.qmd` — add the prose section under
      `## Courses`. Keep the `### <Korean title>: <English title>`
      header convention.
- [ ] Run `python scripts/build.py` (so the CV picks up the new
      course).
- [ ] `python scripts/build_cv.py` picks up the change automatically on
      the next full build (no manual CV step needed).

### Adding an invited lecture / seminar

- [ ] If it's at a new institution, add it to `_data/service.yml`
      under `service.invited_lectures.{ko,en}`.
- [ ] `teaching.qmd` + `en/teaching.qmd` — add a line to the
      `## Invited Lectures · Seminars` list with the topic.
- [ ] Run `python scripts/build.py`.
- [ ] CV re-export if this is a new institution.

### Adding or updating a design project

Design-project prose stays entirely hand-written.

- [ ] `design.qmd` — add a new section using the existing
      `::: {.project-meta}` div pattern.
- [ ] `en/design.qmd` — matching.
- [ ] Image goes in `assets/images/design/`.
- [ ] No `_data/` update; no `llms.txt` update unless it is a headline
      project that changes the overall summary (in which case also
      update `_data/profile.yml` `summary_llms`).

## CV generation

`assets/cv_en.pdf` and `assets/cv_ko.pdf` are generated by
`scripts/build_cv.py` from the same `_data/*.yml` that drives the site.
Any change to profile, education, career, publications, projects,
patents, awards, service, or teaching metadata is reflected in the
next CV build — no manual re-export.

- Template: The template pinned in `cv/cv.typ` is
  `@preview/pro-academic-cv:0.1.0` by Wenhao Liao (upstream:
  <https://github.com/whliao5am/pro-academic-cv-typst-template>).
  A different package by the same author, `@preview/acadennial-cv`,
  exists on Typst Universe but is not used here.
- Fonts: `cv/fonts/Pretendard-Regular.otf` + `Pretendard-Bold.otf`
  (SIL OFL — license at `cv/fonts/OFL.txt`). Committed to the repo
  so CI needs no extra font install.
- Section strings: `cv/strings.typ` — KO / EN labels keyed by language.
- Build: `python scripts/build_cv.py` (uses the `typst` PyPI package;
  no separate Typst CLI needed).
- When the CV template itself needs editing, work in `cv/cv.typ` and
  rebuild; do not hand-edit the PDFs.

## Parity check (before committing)

Before you commit, run this mental pass:

1. For every `_data/*.yml` change, did you run `python scripts/build.py`
   and commit the resulting `_includes/*.qmd` and `llms.txt` alongside?
2. Are the `.ko` and `.en` forms aligned (no stale translation)?
3. If the fact appears in `llms.txt` sections controlled by data, has
   the rendered section been regenerated and reviewed?
4. Did this change affect CV content? If yes,
   `python scripts/build_cv.py` has been run and the two new PDFs are
   staged. (CI will re-run the build anyway, but staging them keeps
   the commit self-contained.)
5. Run `quarto render .` locally (KO root) and `cd en && quarto render .`
   (EN) to confirm both build clean.

## Build workflow

Any edit to `_data/*.yml` must be followed by:

```bash
python scripts/build.py
```

The build script validates required fields on load and exits with a
clear error if anything is missing (e.g. a publication's `highlight.period`
that doesn't match one of the declared `research_work_periods`, an
award pointing at an unknown category, or more than five highlighted
projects). Keep `_data/`, `_includes/`, and `llms.txt` in a single
commit so the YAML and its rendered outputs never drift.

The build is also run automatically in CI
(`.github/workflows/publish.yml`), so production site renders stay
correct even if a local build was skipped — but CI only runs on push,
so **local previews** reflect whatever is on disk. Always run the build
before `quarto preview` if you just changed data.

## Build & preview

```bash
# Regenerate data-driven includes + llms.txt, then preview
python scripts/build.py
quarto preview .

# Preview the English site
cd en && quarto preview .

# Rebuild the CV PDFs after a data change
python scripts/build_cv.py

# Full build of data + CV + both sites
./build.sh
```

Deployment is automatic on push to `main` via
`.github/workflows/publish.yml`, which runs `scripts/build.py` and
`scripts/build_cv.py` before `quarto render`.

## Future work

The `_data/` SSOT covers every user-visible fact the site currently
carries. Future work is cosmetic polish on the CV template (margins,
publication sort order, Korean line-breaking tweaks) — those live in
`cv/cv.typ` and do not require data-layer changes.
