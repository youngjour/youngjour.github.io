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

Requires [Quarto CLI](https://quarto.org/docs/get-started/) (v1.4+).

```bash
# Preview the Korean site with live reload
quarto preview .

# Preview the English site
cd en && quarto preview .

# Build both sites (outputs to _site/ and _site/en/)
./build.sh
```

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
