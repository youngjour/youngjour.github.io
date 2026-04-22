# Youngjun Park — Personal Website

Bilingual (Korean / English) academic website for Youngjun Park — architect, urban data scientist, and co-founder / CTO of ar-ge inc.

Live site: [https://youngjour.github.io](https://youngjour.github.io)

> Before changing any content on the site, read [AGENTS.md](AGENTS.md)
> — it lists every file that must be touched for each type of update.

## Stack

- **[Quarto](https://quarto.org/)** — static site generator
- **GitHub Pages** — hosting (deployed to the `gh-pages` branch)
- **GitHub Actions** — automated render and publish on push to `main`
- **SCSS** — custom theme extending Quarto's `cosmo` bootswatch

## Repository layout

```
.
├── _quarto.yml              # Korean (root) site config — navbar, theme, metadata
├── index.qmd                # Korean About / landing page (trestles template)
├── research.qmd             # Korean Research page
├── teaching.qmd             # Korean Teaching page
├── design.qmd               # Korean Design page
├── _paper-template.qmd      # Template for individual paper pages
├── en/
│   ├── _quarto.yml          # English site config
│   ├── index.qmd            # English About / landing page
│   ├── research.qmd
│   ├── teaching.qmd
│   └── design.qmd
├── assets/
│   ├── css/
│   │   ├── custom.scss      # Theme overrides
│   │   └── main.scss
│   └── images/              # Profile photos and figures
├── resources/               # CVs and other downloadable files
├── .github/workflows/
│   └── publish.yml          # Renders both sites and publishes to gh-pages
├── build.sh                 # Local build helper (KO + EN)
└── robots.txt
```

The Korean site is the root (`/`); the English site is published under `/en/`. The language switcher in each navbar links across.

## Local development

Requires [Quarto CLI](https://quarto.org/docs/get-started/) (v1.4+) and
Python 3.10+.

```bash
# Install the Python build dependencies (yaml + jinja2)
pip install -r scripts/requirements.txt

# Regenerate data-driven includes and llms.txt from _data/*.yml
python scripts/build.py

# Preview the Korean site with live reload
quarto preview .

# Preview the English site
cd en && quarto preview .

# Build both sites (runs the data build + outputs to _site/ and _site/en/)
./build.sh
```

## Content data

Most site facts are stored as structured YAML under `_data/` and are the
**single source of truth** for the pages, `llms.txt`, and (once the CV
pipeline lands) the CV PDFs. The files in `_includes/*.qmd` and the
data-driven sections of `llms.txt` are generated outputs — do not
hand-edit them.

- `_data/publications.yml` — publications (papers, talks, posters).
- `_data/projects.yml` — funded research projects.
- `_data/patents.yml` — patents and copyrights.
- `_data/profile.yml` — name, byline, identifiers, current affiliations,
  and the `llms.txt` blockquote summary.
- `_data/education.yml` — degree entries.
- `_data/career.yml` — chronological positions shown on the About page
  and in `llms.txt` "Career history".
- `_data/awards.yml` — awards and honors (categorised).
- `_data/service.yml` — professional service (reviewer, advisory,
  industry collaborations, invited lectures).
- `_data/teaching.yml` — course metadata used by the CV generator.

Run `python scripts/build.py` after editing any `_data/*.yml` file.
The build step is also wired into `build.sh` and the GitHub Actions
workflow, so CI renders stay correct; local previews, however, reflect
the files on disk — run the build manually before `quarto preview` if
you just changed data. See [AGENTS.md](AGENTS.md) for the full
per-change checklist.

## Deployment

Pushes to `main` trigger `.github/workflows/publish.yml`, which:

1. Renders the Korean site (`quarto render .`)
2. Renders the English site (`cd en && quarto render .`)
3. Publishes `_site/` to the `gh-pages` branch via `peaceiris/actions-gh-pages`

GitHub Pages serves `gh-pages`.

## Adding a paper page

1. Copy `_paper-template.qmd` into a papers directory (e.g. `papers/2025-food-deserts.qmd`).
2. Fill in the YAML front matter — keep `google-scholar: true` so citation metadata is emitted.
3. Add a link to the paper from `research.qmd` (and `en/research.qmd` if bilingual).

## Contact

- Email: youngjourpark@gmail.com
- Google Scholar: [sGRKN6UAAAAJ](https://scholar.google.com/citations?user=sGRKN6UAAAAJ)
- ORCID: [0000-0002-4254-2268](https://orcid.org/0000-0002-4254-2268)
- GitHub: [@youngjour](https://github.com/youngjour)
- LinkedIn: [youngjourpark](https://linkedin.com/in/youngjourpark)

## License

Content © Youngjun Park. Site scaffolding available under MIT License.
