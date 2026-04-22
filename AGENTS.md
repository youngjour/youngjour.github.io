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
2. **Facts live in multiple places by design.** There is no single source
   of truth yet (that is a future Tier 2 refactor). Until then, follow
   the checklists below literally.
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
| Publication (paper/talk)  | `research.qmd`, `index.qmd` (if it belongs in "Research Works" highlights) | `en/research.qmd`, `en/index.qmd` (same rule) | `llms.txt` (always); CV (see triggers) |
| Research project / grant  | `research.qmd`, `index.qmd` (if it belongs in the 5-project Projects highlight) | `en/research.qmd`, `en/index.qmd` (same rule) | `llms.txt`; CV                           |
| Patent / copyright / IP   | `index.qmd`, `research.qmd` | `en/index.qmd`, `en/research.qmd`           | `llms.txt`; CV                           |
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

- [ ] Decide: is this a "research works" highlight (appears on the About
      page) or only a full-list entry (Research page only)?
- [ ] `research.qmd` — add under the correct year section. Use the same
      citation format as existing entries. Bold the owner as
      `**Park, Youngjun**`.
- [ ] `en/research.qmd` — add the matching entry. Translate venue/title
      conservatively; keep author list identical.
- [ ] If it's a highlight: `index.qmd` "Research Works" — add a one-line
      bullet. Counterpart in `en/index.qmd`.
- [ ] `llms.txt` "Publications" — add under the matching year subsection.
      Match the existing citation format exactly (author abbreviation,
      bold owner, bare DOI URL).
- [ ] Verify DOI / URL resolves (HEAD request returns 200).
- [ ] CV re-export (see triggers).

### Adding a research project / grant

- [ ] `research.qmd` "Research Projects" — add entry with period, role,
      institution, funder, project number.
- [ ] `en/research.qmd` — matching entry.
- [ ] If top-5 impactful: `index.qmd` "Projects" — add; counterpart in
      `en/index.qmd`.
- [ ] `llms.txt` "Research projects" — add. Include project number.
- [ ] CV re-export.

### Adding a patent / copyright

- [ ] `research.qmd` "Patents · Intellectual Property" — add.
- [ ] `en/research.qmd` — matching.
- [ ] `index.qmd` same section — add.
- [ ] `en/index.qmd` — matching.
- [ ] `llms.txt` "Patents and intellectual property" — add.
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

## Build & preview

```bash
# Preview the Korean site
quarto preview .

# Preview the English site
cd en && quarto preview .

# Full build of both (before committing content changes)
./build.sh
```

Deployment is automatic on push to `main` via
`.github/workflows/publish.yml`.

## Future work

This file will be slimmer once the Tier 2 refactor lands: `_data/*.yml`
as single source of truth, `_includes/*.qmd` and `llms.txt` auto-
generated from the data, and (Tier 3) the CV rendered from the same
data. Until then, the checklists above are authoritative.
