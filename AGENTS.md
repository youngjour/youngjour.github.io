# AGENTS.md — Content update rules

This repo is a bilingual (Korean root / English `/en/`) Quarto site. The
same fact often lives in 3–5 files. This document lists the exact files
that must be touched for each type of change so nothing drifts.

**Read this file before modifying any content**, whether you are the site
owner or a coding agent.

## Core principles

1. **Korean and English are a coupled pair.** Any edit to a `.qmd` file
   in the repo root must be reviewed against its counterpart under `en/`
   in the same commit. If the KO version gains a publication, the EN
   version gains it too — in the same PR.
2. **Publications, projects, and patents have a single source of truth.**
   `_data/publications.yml`, `_data/projects.yml`, and `_data/patents.yml`
   drive every place those facts appear on the site and in `llms.txt`.
   For everything else (career, education, awards, professional service,
   teaching, design, identifiers) facts still live in multiple places —
   follow the checklists below literally for those.
3. **`llms.txt` is a mirror, not a draft.** If a fact changes on the site,
   `llms.txt` must be updated in the same commit. The reverse is not
   true — do not put anything in `llms.txt` that is not also on a page.
4. **CV PDFs are derived artifacts.** When a CV-relevant fact changes
   (see "CV re-export triggers" below), re-export both `cv_en.pdf` and
   `cv_ko.pdf` from the master CV source and replace the files in
   `assets/`. Do not hand-edit the PDFs.
5. **When in doubt, update more places, not fewer.** A missing update
   causes silent drift; a redundant one is trivially fixed.

## File cheat sheet — where facts currently live

| Fact type                 | KO file(s)                | EN file(s)                   | Also update                              |
|---------------------------|---------------------------|------------------------------|------------------------------------------|
| Publication (paper/talk)  | `_data/publications.yml` (SSOT) — run `python scripts/build.py` | same SSOT | `llms.txt` (auto); CV (see triggers) |
| Research project / grant  | `_data/projects.yml` (SSOT) — run `python scripts/build.py` | same SSOT | `llms.txt` (auto); CV |
| Patent / copyright / IP   | `_data/patents.yml` (SSOT) — run `python scripts/build.py` | same SSOT | `llms.txt` (auto); CV |
| Career position           | `index.qmd`               | `en/index.qmd`               | `llms.txt` ("Current affiliations" / "Career history"); CV |
| Education                 | `index.qmd`               | `en/index.qmd`               | `llms.txt` ("Education"); CV             |
| Award                     | `index.qmd`               | `en/index.qmd`               | CV (usually); `llms.txt` only if listed there |
| Course (graduate)         | `teaching.qmd`            | `en/teaching.qmd`            | CV                                       |
| Invited lecture / seminar | `teaching.qmd`, `index.qmd` ("Professional Service → 특강 · 세미나") | `en/teaching.qmd`, `en/index.qmd`           | CV                                       |
| Student collaboration     | `teaching.qmd`            | `en/teaching.qmd`            | —                                        |
| Design / architecture project | `design.qmd`          | `en/design.qmd`              | CV (if major)                            |
| Identifier (ORCID, Scholar, ar-ge URL, email) | `index.qmd` (`about.links`), `_quarto.yml`, `README.md` | `en/index.qmd` (`about.links`), `en/_quarto.yml` | `llms.txt` ("Identifiers"); CV           |
| Professional service (reviewer, advisory) | `index.qmd` | `en/index.qmd`               | `llms.txt` ("Professional service"); CV  |

## Change-type checklists

### Adding a publication

Publications live in `_data/publications.yml` (Tier 2 SSOT). The Research
page, About-page highlights, and `llms.txt` are all generated from it by
`scripts/build.py`. **Do not hand-edit `research.qmd`, `en/research.qmd`,
`index.qmd`, `en/index.qmd`, or `llms.txt` for publication changes** —
those changes will be overwritten on next build.

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
- [ ] CV re-export (see triggers).

### Adding a research project / grant

Projects live in `_data/projects.yml`. The Research page full list, the
About-page top-5 highlight, and the `llms.txt` "Research projects"
section are all generated from it.

- [ ] `_data/projects.yml` — add the entry. Required fields: `id`,
      `title.{ko,en}`, `period`, `research_meta.{ko,en}`, `llms_line`.
- [ ] If top-5 impactful, set `highlight: true` and add `index_meta.{ko,en}`
      plus `index_summary.{ko,en}`. At most 5 projects may be highlighted
      at once (the build will fail otherwise).
- [ ] Run `python scripts/build.py`. Review diffs under `_includes/` and
      in `llms.txt`.
- [ ] Commit `_data/projects.yml`, `_includes/*`, and `llms.txt` together.
- [ ] CV re-export.

### Adding a patent / copyright

Patents live in `_data/patents.yml`. The Research-page section, the
About-page section, and the `llms.txt` "Patents and intellectual property"
section are all generated from it.

- [ ] `_data/patents.yml` — add the entry. Required fields: `id`, `kind`
      (`patent` or `copyright`), `status` (`filed` or `registered`),
      `jurisdiction` (e.g. `KR`), `number`, `title.{ko,en}`.
- [ ] Run `python scripts/build.py`. Review diffs.
- [ ] Commit `_data/patents.yml`, `_includes/*`, and `llms.txt` together.
- [ ] CV re-export.

### Changing a career position (new role, end date, affiliation)

- [ ] `index.qmd` "Career" — update.
- [ ] `en/index.qmd` "Career" — update.
- [ ] `llms.txt` "Current affiliations" and/or "Career history" — update.
      If the change affects the summary, also revise the blockquote.
- [ ] `_quarto.yml` subtitle / description — update only if the job
      title changed (e.g., "Co-founder · CTO, ar-ge inc.").
- [ ] `en/_quarto.yml` — matching.
- [ ] `README.md` top-line description — update only if major.
- [ ] CV re-export.

### Adding a course or invited lecture

- [ ] `teaching.qmd` — add under the correct subsection (Courses /
      Invited Lectures · Seminars).
- [ ] `en/teaching.qmd` — matching.
- [ ] If it's a named lecture series (e.g., at a new institution),
      `index.qmd` "Professional Service → 특강·세미나" also gets the
      new institution; same for `en/index.qmd`.
- [ ] CV re-export.

### Adding or updating a design project

- [ ] `design.qmd` — add a new section using the existing project-meta
      `::: {.project-meta}` div pattern.
- [ ] `en/design.qmd` — matching.
- [ ] Image goes in `assets/images/design/`.
- [ ] No `llms.txt` update required unless it is a headline project that
      changes the overall summary.

### Adding an award

- [ ] `index.qmd` "Awards · Honors" — add.
- [ ] `en/index.qmd` — matching.
- [ ] `llms.txt` — only update if awards are listed there (currently they
      are NOT; keep parity with what's already in llms.txt).
- [ ] CV re-export.

### Updating identifiers (ORCID, Google Scholar, email, ar-ge URL)

- [ ] `index.qmd` `about.links` — update.
- [ ] `en/index.qmd` `about.links` — update.
- [ ] `_quarto.yml` footer — update.
- [ ] `en/_quarto.yml` footer — update.
- [ ] `llms.txt` "Identifiers" — update.
- [ ] `README.md` "Contact" — update.
- [ ] CV re-export if the ID appears on the CV.

## CV re-export triggers

Re-export both `cv_en.pdf` and `cv_ko.pdf` whenever any of the following
change:

- Any publication (add / accept / withdraw / revise metadata).
- Any career position (start / end / title / affiliation).
- Any funded project, patent, or major award.
- Any education entry.
- Any identifier that appears on the CV.

Minor site-only changes (a blog-like paragraph rewrite, an image, a
design project's narrative) do not trigger re-export.

## Parity check (before committing)

Before you commit, run this mental pass:

1. Did the KO file you just edited have a matching file under `en/`?
   If yes, did you open it? Diff it against the KO file to confirm
   parity.
2. Does `llms.txt` mention the fact you added? If the fact belongs in
   any of these sections — Publications, Research projects, Patents,
   Career history, Current affiliations, Identifiers, Education,
   Professional service — it must appear there.
3. Did this change trigger a CV re-export? If yes, is the new PDF in
   `assets/`?
4. Run `quarto render .` locally (KO root) and `cd en && quarto render .`
   (EN) to confirm both build clean. If running in CI only, wait for the
   GitHub Actions run to go green before considering the change done.

## Build workflow

For any content that lives in `_data/*.yml`, edit the YAML file and run
`python scripts/build.py` before `quarto preview` or `quarto render`.
The build step is also run automatically in CI, but local previews
reflect the current `_includes/` directory — stale includes will show
stale content.

```bash
# Regenerate _includes/*.qmd and llms.txt from _data/
python scripts/build.py
```

The build script validates required fields on load and exits with a
clear error if anything is missing (e.g. a publication's `highlight.period`
that doesn't match one of the declared `research_work_periods`, or more
than five highlighted projects). Keep `_data/`, `_includes/`, and
`llms.txt` in a single commit so the YAML and its rendered outputs never
drift.

## Build & preview

```bash
# Regenerate data-driven includes, then preview
python scripts/build.py
quarto preview .

# Preview the English site
cd en && quarto preview .

# Full build of both (before committing content changes)
./build.sh
```

Deployment is automatic on push to `main` via
`.github/workflows/publish.yml`, which runs `scripts/build.py` before
`quarto render`.

## Future work

Tier 3 would render the CV PDFs from the same `_data/*.yml` sources so
that a CV re-export is automatic on any data change. Until that lands,
re-exports are manual — see the triggers above.
