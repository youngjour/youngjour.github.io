// CV template — renders a bilingual academic CV from `_data/*.yml`.
//
// Package : pro-academic-cv 0.1.0 (Typst Universe)
// Author  : Wenhao Liao — https://github.com/whliao5am/pro-academic-cv-typst-template
// Import  : #import "@preview/pro-academic-cv:0.1.0": *
// Target  : the look of the package's shipped `template/main.typ`,
//           applied to the YAML under `_data/`.
//
// Build:
//   typst compile --root . --font-path cv/fonts --input lang=en cv/cv.typ assets/cv_en.pdf
//   typst compile --root . --font-path cv/fonts --input lang=ko cv/cv.typ assets/cv_ko.pdf
// The Python wrapper (`scripts/build_cv.py`) calls both.
//
// Primitive mapping — which package helper backs each CV section:
//   Education, Experience, Awards, Grants, Patents, Teaching
//     → r2c2-entry-list (2×2 header block + optional bullet list)
//   Publications → publication-entry-list
//     (auto-numbers by category; emits [J1], [C1], [W1], [Po1], [S1], [O1]).
//     YAML `type` maps to category as:
//       journal → J, conference → C, workshop → W, poster → Po,
//       other → O, `status: in-review` overrides to S.
//     `number-style: "descending"` matches academic convention (most
//     recent entry has the highest number).
//   Professional Service → multi-line-list / single-line-entry
//
// Font setup:
//   English build — no `font-settings` override; the template's
//     shipped typography (serif) applies unchanged.
//   Korean build — `font-settings.font-family` is overridden to a
//     single Hangul-capable family so both Latin and Korean runs
//     share one family (avoids the tonal mismatch of a Latin/Hangul
//     fallback array). The OTFs are committed under `cv/fonts/` and
//     supplied via `--font-path`, so CI needs no extra font install.
//     `font-settings.lang: "ko"` also engages Typst's Korean
//     line-breaking rules.

#import "@preview/pro-academic-cv:0.1.0": *
#import "strings.typ": strings

// -------- Language & data --------

#let lang = sys.inputs.at("lang", default: "en")
#let s = strings.at(lang)

#let profile = yaml("/_data/profile.yml").profile
#let education_list = yaml("/_data/education.yml").education
#let career_list = yaml("/_data/career.yml").career
#let awards_data = yaml("/_data/awards.yml")
#let awards_list = awards_data.awards
#let service_data = yaml("/_data/service.yml")
#let publications_list = yaml("/_data/publications.yml").publications
#let projects_list = yaml("/_data/projects.yml").projects
#let patents_list = yaml("/_data/patents.yml").patents
#let courses_list = yaml("/_data/teaching.yml").courses

// -------- Helpers --------

// Strip the `**…**` owner marker to Typst `strong(…)`; pass other
// authors through unchanged.
#let render-author(a) = if a.starts-with("**") and a.ends-with("**") {
  strong(a.slice(2, a.len() - 2))
} else {
  a
}

// Render a full author list as "A, B, and C" (and "A and B" for two).
#let render-authors(authors) = {
  let parts = authors.map(render-author)
  let n = parts.len()
  if n == 1 {
    parts.at(0)
  } else if n == 2 {
    [#parts.at(0) #s.conjunction #parts.at(1)]
  } else {
    let out = []
    for i in range(n - 1) {
      out = out + parts.at(i) + [, ]
    }
    out + s.conjunction + [ ] + parts.last()
  }
}

// Convert `*text*` Markdown-italic (used inside `research_meta` strings
// in projects.yml for the role label) into Typst `emph(…)` content.
#let render-md(str) = {
  let parts = str.split("*")
  let out = []
  for i in range(parts.len()) {
    if calc.rem(i, 2) == 0 {
      out = out + parts.at(i)
    } else {
      out = out + emph(parts.at(i))
    }
  }
  out
}

// Map a publication entry to a `publication-entry-list` category letter.
#let pub-category(p) = {
  let status = p.at("status", default: "published")
  if status == "in-review" {
    "S"
  } else if p.type == "journal" {
    "J"
  } else if p.type == "conference" {
    "C"
  } else if p.type == "workshop" {
    "W"
  } else if p.type == "poster" {
    "Po"
  } else {
    "O"
  }
}

#let pub-venue(p) = p.venue.at(lang, default: p.venue.en)

#let pub-suffix(p) = {
  let status = p.at("status", default: "published")
  if status == "poster" { return ", poster session" }
  if status == "in-review" { return ", in review" }
  let vol = p.at("volume", default: "")
  let iss = p.at("issue", default: "")
  let pages = p.at("pages", default: "")
  if vol != "" and iss != "" and pages != "" {
    return ", " + vol + "(" + iss + "), " + pages
  }
  if pages != "" { return ", " + pages }
  ""
}

#let pub-url(p) = {
  if p.at("doi", default: "") != "" { return "https://doi.org/" + p.doi }
  if p.at("url", default: "") != "" { return p.url }
  ""
}

// Render a single publication as the `value:` content for
// `publication-entry-list`.
#let render-pub-value(p) = {
  let venue = pub-venue(p)
  let suffix = pub-suffix(p)
  let url = pub-url(p)
  let title-part = if url != "" {
    link(url)[*#p.title*]
  } else {
    strong(p.title)
  }
  [#render-authors(p.authors) (#str(p.year)). #title-part. #emph(venue)#suffix.]
}

#let service-items(key) = {
  let entries = service_data.service.at(key)
  if lang == "en" and entries.en.len() == 0 { entries.ko } else { entries.at(lang) }
}

// -------- Document --------

#show: resume.with(
  ..(if lang == "ko" {
    (
      font-settings: (
        font-family: "Pretendard",
        font-size: 10pt,
        author-font-size: 25pt,
        lang: "ko",
      ),
    )
  } else {
    (:)
  }),
  author-info: (
    name: if lang == "ko" { profile.name_ko } else { profile.name_en },
    primary-info: [
      #profile.current_affiliations.at(0).role.at(lang), #profile.current_affiliations.at(0).institution.at(lang)
      #sym.bar.v
      #link("mailto:" + profile.identifiers.email)[#profile.identifiers.email]
    ],
    secondary-info: [
      #link("https://scholar.google.com/citations?user=" + profile.identifiers.scholar_id)[scholar]
      #sym.bar.v
      #link("https://orcid.org/" + profile.identifiers.orcid)[orcid]
      #sym.bar.v
      #link("https://github.com/" + profile.identifiers.github)[github]
      #sym.bar.v
      #link("https://linkedin.com/in/" + profile.identifiers.linkedin)[linkedin]
    ],
    tertiary-info: profile.summary_llms,
  ),
)

// -------- Education --------

== #s.education
#r2c2-entry-list(
  ..education_list.map(e => (
    entry-header-args: (
      top-left: e.institution.at(lang),
      top-right: str(e.year),
      bottom-left: e.degree.at(lang),
      bottom-right: "",
    ),
    list-items: if "detail" in e {
      ([#emph(e.detail_label.at(lang) + ":") #e.detail.at(lang)],)
    } else { () },
  ))
)

// -------- Experience --------

== #s.experience
#r2c2-entry-list(
  ..career_list.map(pos => (
    entry-header-args: (
      top-left: pos.employer.at(lang),
      top-right: pos.period.at(lang),
      bottom-left: pos.title.at(lang),
      bottom-right: "",
    ),
    list-items: {
      let bullets = pos.at("bullets", default: none)
      if bullets != none and lang in bullets and bullets.at(lang).len() > 0 {
        bullets.at(lang).map(b => [#b])
      } else { () }
    },
  ))
)

// -------- Awards (academic) --------

== #s.awards
#r2c2-entry-list(
  ..awards_list
    .filter(a => a.category == "academic")
    .map(a => (
      entry-header-args: (
        top-left: a.title.at(lang),
        top-right: str(a.year),
        bottom-left: a.context.at(lang),
        bottom-right: "",
      ),
      list-items: (),
    ))
)

// -------- Publications --------

== #s.publications
#publication-entry-list(
  publications_list.map(p => (
    category: pub-category(p),
    value: render-pub-value(p),
  )),
  number-style: "descending",
)

// -------- Research Projects & Grants --------

== #s.grants
#r2c2-entry-list(
  ..projects_list.map(p => (
    entry-header-args: (
      top-left: p.title.at(lang),
      top-right: p.period,
      bottom-left: render-md(p.research_meta.at(lang)),
      bottom-right: "",
    ),
    list-items: (),
  ))
)

// -------- Patents --------

== #s.patents
#r2c2-entry-list(
  ..patents_list.map(pat => {
    let prefix = if pat.kind == "patent" {
      if pat.status == "filed" { "Patent (Filed)" } else { "Patent (Registered)" }
    } else { "Copyright (Registered)" }
    (
      entry-header-args: (
        top-left: pat.title.at(lang),
        top-right: pat.number,
        bottom-left: prefix,
        bottom-right: pat.jurisdiction,
      ),
      list-items: (),
    )
  })
)

// -------- Professional Service --------

== #s.service
#multi-line-list(
  single-line-entry([#s.journal_reviewer], service-items("journal_reviewer").join(" · "), []),
  single-line-entry([#s.research_advisory], service-items("research_advisory").join(" · "), []),
  single-line-entry([#s.industry_collaborations], service-items("industry_collaborations").join(" · "), []),
  single-line-entry([#s.invited_lectures], service-items("invited_lectures").join(" · "), []),
)

// -------- Teaching --------

== #s.teaching
#r2c2-entry-list(
  ..courses_list.map(c => (
    entry-header-args: (
      top-left: c.title.at(lang),
      top-right: c.years,
      bottom-left: c.level.at(lang) + " · " + c.institution.at(lang),
      bottom-right: "",
    ),
    list-items: (),
  ))
)

