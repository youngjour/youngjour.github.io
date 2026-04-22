#!/usr/bin/env python3
"""SSOT build step.

Loads `_data/*.yml`, validates required fields, renders `_templates/*.j2`
into `_includes/*.qmd`, and regenerates `llms.txt` at the repo root. Run
before `quarto render`.

Data files:
  publications.yml   papers, talks, posters
  projects.yml       funded research projects
  patents.yml        patents and copyrights
  profile.yml        name, byline, identifiers, current affiliations
  education.yml      degree entries
  career.yml         chronological positions
  awards.yml         awards and honors (categorised)
  service.yml        professional service (reviewer, advisory, etc.)
  teaching.yml       course metadata (Phase 3b CV only)
"""

from __future__ import annotations

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "_data"
TEMPLATES_DIR = ROOT / "_templates"
INCLUDES_DIR = ROOT / "_includes"
LLMS_TXT_PATH = ROOT / "llms.txt"


# ---------- helpers ----------

def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_text(path: Path, content: str) -> None:
    path.write_bytes(content.encode("utf-8"))


def short_author(name: str) -> str:
    bolded = name.startswith("**") and name.endswith("**")
    inner = name[2:-2] if bolded else name
    if "," in inner:
        last, given = inner.split(",", 1)
        given = given.strip()
        initials = " ".join(f"{g[0]}." for g in given.split())
        result = f"{last}, {initials}"
    else:
        result = inner
    return f"**{result}**" if bolded else result


def author_last_name(name: str) -> str:
    inner = name[2:-2] if name.startswith("**") and name.endswith("**") else name
    if "," in inner:
        return inner.split(",", 1)[0].strip()
    return inner.strip()


def owner_index(authors: list[str]) -> int:
    for i, a in enumerate(authors):
        if a.startswith("**") and a.endswith("**"):
            return i
    raise ValueError(f"No owner (**-wrapped) author in {authors!r}")


def default_author_label(authors: list[str]) -> str:
    owner_i = owner_index(authors)
    if len(authors) == 1:
        return author_last_name(authors[0])
    if owner_i == 0:
        return f"{author_last_name(authors[0])} et al."
    return f"{author_last_name(authors[0])}, {author_last_name(authors[owner_i])} et al."


# ---------- publications ----------

def research_suffix(p: dict) -> str:
    status = p.get("status", "published")
    if status == "in-review":
        return " (in-review)"
    if status == "poster":
        return ", poster session"
    vol = p.get("volume") or ""
    iss = p.get("issue") or ""
    pages = p.get("pages") or ""
    if vol and iss and pages:
        return f", {vol}({iss}), {pages}"
    if pages:
        return f", {pages}"
    return ""


def research_url(p: dict) -> str:
    if p.get("doi"):
        return f"https://doi.org/{p['doi']}"
    if p.get("url"):
        return p["url"]
    if p.get("research_only_url"):
        return p["research_only_url"]
    return ""


def llms_url(p: dict) -> str:
    if p.get("doi"):
        return f"https://doi.org/{p['doi']}"
    if p.get("url"):
        return p["url"]
    return ""


def render_research_entry(p: dict, lang: str) -> str:
    venue = p["venue"][lang]
    authors_str = "; ".join(p["authors"])
    title = p["title"]
    year = p["year"]
    if p.get("status") == "in-review":
        italic = f"*Submitted to {venue}*"
    else:
        italic = f"*{venue}*"
    body = f'- {authors_str}. ({year}) "{title}." {italic}{research_suffix(p)}.'
    url = research_url(p)
    if url:
        label = p.get("url_label") or "Published"
        if p.get("url_italic") is False:
            body += f"\n  [[{label}]({url})]"
        else:
            body += f"\n  *[[{label}]({url})]*"
    return body


def render_llms_entry(p: dict) -> str:
    short_authors = "; ".join(short_author(a) for a in p["authors"])
    title = p.get("title_llms") or p["title"]
    venue = p["venue"].get("llms") or p["venue"]["en"]
    year = p["year"]
    if p.get("status") == "in-review":
        venue_part = f"Submitted to *{venue}* (in review)"
    elif p.get("status") == "poster":
        venue_part = f"*{venue}*, poster session"
    else:
        vol = p.get("volume") or ""
        iss = p.get("issue") or ""
        pages = p.get("pages") or ""
        if vol and iss and pages:
            venue_part = f"*{venue}*, {vol}({iss}), {pages}"
        elif pages:
            venue_part = f"*{venue}*, {pages}"
        else:
            venue_part = f"*{venue}*"
    line = f"- {short_authors} ({year}). {title}. {venue_part}."
    url = llms_url(p)
    if url:
        line += f" {url}"
    return line


def render_highlight_entry(p: dict, lang: str) -> str:
    hl = p["highlight"]
    label = hl.get("author_label") or default_author_label(p["authors"])
    venue_short = hl["venue_short"]
    year = p["year"]
    year_str = f"{year}, in-review" if p.get("status") == "in-review" else str(year)
    summary = hl["summary"][lang]
    return f"- {label} ({year_str}) *{venue_short}* — {summary}"


# ---------- projects ----------

def render_project_research_entry(proj: dict, lang: str) -> str:
    title = proj["title"][lang]
    period = proj["period"]
    meta = proj["research_meta"][lang]
    return f"**{title}** ({period})\n{meta}"


def render_project_index_entry(proj: dict, lang: str) -> str:
    title = proj["title"][lang]
    period = proj["period"]
    meta = proj["index_meta"][lang]
    summary = proj["index_summary"][lang]
    return f"**{title}** ({period})\n{meta}\n{summary}"


def render_project_llms_entry(proj: dict) -> str:
    title = proj["title"]["en"]
    period = proj["period"]
    return f"- {title} ({period}). {proj['llms_line']}"


# ---------- patents ----------

_PATENT_KIND_KO = {"patent": "특허", "copyright": "저작권"}
_PATENT_KIND_EN = {"patent": "Patent", "copyright": "Copyright"}
_PATENT_STATUS_KO = {"filed": "출원", "registered": "등록"}
_PATENT_STATUS_EN = {"filed": "Filed", "registered": "Registered"}
_JURIS_KO = {"KR": "한국"}
_JURIS_EN = {"KR": "Korean"}


def render_patent_entry(pat: dict, lang: str) -> str:
    kind = pat["kind"]
    status = pat["status"]
    juris = pat["jurisdiction"]
    title = pat["title"][lang]
    num = pat["number"]
    if lang == "ko":
        juris_label = _JURIS_KO.get(juris, juris)
        kind_label = _PATENT_KIND_KO[kind]
        status_label = _PATENT_STATUS_KO[status]
    else:
        juris_label = _JURIS_EN.get(juris, juris)
        kind_label = _PATENT_KIND_EN[kind]
        status_label = _PATENT_STATUS_EN[status]
    return f"- **{juris_label} {kind_label} ({status_label})** {num} — {title}"


def render_patent_llms_entry(pat: dict) -> str:
    kind = pat["kind"]
    status = pat["status"]
    juris = pat["jurisdiction"]
    title = pat["title"]["en"]
    num = pat["number"]
    juris_label = _JURIS_EN.get(juris, juris)
    kind_label = _PATENT_KIND_EN[kind]
    status_label = _PATENT_STATUS_EN[status]
    return f"- {juris_label} {kind_label} ({status_label}) {num} — {title}."


# ---------- profile (llms.txt only; site identifiers live in index.qmd about.links) ----------

def render_llms_identifiers(profile: dict) -> str:
    ids = profile["identifiers"]
    lines = [
        f"- ORCID: https://orcid.org/{ids['orcid']}",
        f"- Google Scholar: https://scholar.google.com/citations?user={ids['scholar_id']}",
        f"- GitHub: https://github.com/{ids['github']}",
        f"- LinkedIn: https://linkedin.com/in/{ids['linkedin']}",
        f"- Email: {ids['email']}",
    ]
    return "\n".join(lines) + "\n"


def render_llms_affiliation(aff: dict) -> str:
    inst_en = aff["institution"]["en"]
    role_llms = aff["role"].get("llms") or aff["role"]["en"]
    status = aff["status"]["en"]
    url = aff.get("url")
    name = f"[{inst_en}]({url})" if url else inst_en
    return f"- {name} — {role_llms} ({status})."


def render_llms_affiliations(profile: dict) -> str:
    lines = [render_llms_affiliation(a) for a in profile["current_affiliations"]]
    return "\n".join(lines) + "\n"


# ---------- education ----------

def render_education_entry(edu: dict, lang: str) -> str:
    degree = edu["degree"][lang]
    inst = edu["institution"][lang]
    year = edu["year"]
    lines = [f"- **{degree}** · {inst} · {year}"]
    if edu.get("detail"):
        label = edu["detail_label"][lang]
        detail = edu["detail"][lang]
        lines.append(f"  - {label}: {detail}")
    return "\n".join(lines)


def render_llms_education_entry(edu: dict) -> str:
    degree = edu["degree"]["en"]
    inst = edu["institution"]["en"]
    year = edu["year"]
    base = f"- {degree}, {inst}, {year}."
    if edu.get("detail"):
        label = edu["detail_label"]["en"]
        detail = edu["detail"].get("llms") or edu["detail"]["en"]
        base += f" {label}: {detail}."
    return base


# ---------- career ----------

def normalize_llms_period(period_en: str) -> str:
    """Strip spaces around en-dash and lowercase 'Present'."""
    if period_en == "Present":
        return "present"
    return period_en.replace(" – ", "–").replace(" — ", "—")


def render_career_entry(pos: dict, lang: str) -> str:
    title = pos["title"][lang]
    employer = pos["employer"][lang]
    period = pos["period"][lang]
    header = f"**{title}** — {employer}\n*{period}*"
    bullets = pos.get("bullets")
    if bullets and bullets.get(lang):
        bullet_lines = "\n".join(f"- {b}" for b in bullets[lang])
        return f"{header}\n\n{bullet_lines}"
    return header


def render_llms_career_entry(pos: dict) -> str:
    title = pos["title"].get("llms") or pos["title"]["en"]
    employer = pos["employer"].get("llms") or pos["employer"]["en"]
    period_llms = pos["period"].get("llms") or normalize_llms_period(pos["period"]["en"])
    return f"- {title}, {employer} — {period_llms}."


# ---------- awards ----------

def render_award_entry(aw: dict, lang: str) -> str:
    title = aw["title"][lang]
    context = aw["context"][lang]
    year = aw["year"]
    if aw["category"] == "academic":
        return f"- **{title}** — {context} ({year})"
    return f"- {title} — {context} ({year})"


# ---------- professional service ----------

_SERVICE_SECTION_KEYS = (
    "journal_reviewer",
    "research_advisory",
    "industry_collaborations",
    "invited_lectures",
)


def _service_items(service_data: dict, key: str, lang: str) -> list[str]:
    """Return items for a section in the given lang, falling back to KO if EN is empty."""
    entries = service_data["service"][key]
    if lang == "en" and not entries["en"]:
        return entries["ko"]
    return entries[lang]


def render_service_site(service_data: dict, lang: str) -> str:
    labels = service_data["labels"]
    parts = []
    for key in _SERVICE_SECTION_KEYS:
        items = _service_items(service_data, key, lang)
        label = labels[key][lang]
        parts.append(f"**{label}**\n" + " · ".join(items))
    return "\n\n".join(parts) + "\n"


def render_service_llms(service_data: dict) -> str:
    labels = service_data["labels"]
    lines = []
    # Journal reviewer — italicise each entry, comma-join.
    items = _service_items(service_data, "journal_reviewer", "en")
    lines.append(
        f"- {labels['journal_reviewer']['llms']}: "
        + ", ".join(f"*{i}*" for i in items)
        + "."
    )
    # Research advisory — plain, semicolon.
    items = _service_items(service_data, "research_advisory", "en")
    lines.append(
        f"- {labels['research_advisory']['llms']}: " + "; ".join(items) + "."
    )
    # Industry collaborations — plain, semicolon.
    items = _service_items(service_data, "industry_collaborations", "en")
    lines.append(
        f"- {labels['industry_collaborations']['llms']}: " + "; ".join(items) + "."
    )
    # Invited lectures are intentionally omitted from llms.txt.
    return "\n".join(lines) + "\n"


# ---------- section string composition ----------

def compose_research_pub_section(groups: list[dict]) -> str:
    parts = []
    for g in groups:
        parts.append(f"### {g['title']}\n\n" + "\n".join(g["entries"]) + "\n")
    return "\n".join(parts)


def compose_llms_pub_section(groups: list[dict]) -> str:
    parts = []
    for g in groups:
        parts.append(f"### {g['title']}\n\n" + "\n".join(g["entries"]) + "\n")
    return "\n".join(parts)


def compose_joined_blocks(entries: list[str]) -> str:
    """Join entries with a blank line between (for multi-line blocks)."""
    return "\n\n".join(entries) + "\n"


def compose_joined_lines(entries: list[str]) -> str:
    """Single newline between each entry (for bullet lists)."""
    return "\n".join(entries) + "\n"


def compose_index_highlight_section(groups: list[dict]) -> str:
    parts = []
    for g in groups:
        header = f"**{g['label']}** — {g['affiliation']}"
        if g["entries"]:
            parts.append(header + "\n\n" + "\n".join(g["entries"]) + "\n")
        else:
            parts.append(header + "\n")
    return "\n".join(parts)


# ---------- validation ----------

def validate_all(
    publications,
    periods,
    projects,
    patents,
    profile,
    education,
    career,
    awards,
    award_categories,
    service_data,
    courses,
) -> None:
    # publications
    ids = set()
    plabels_ko = {p["label"]["ko"] for p in periods}
    plabels_en = {p["label"]["en"] for p in periods}
    for p in publications:
        pid = p.get("id") or ""
        if not pid:
            raise SystemExit(f"Publication missing id: {p!r}")
        if pid in ids:
            raise SystemExit(f"Duplicate publication id: {pid}")
        ids.add(pid)
        for key in ("year", "type", "authors", "title", "venue", "status"):
            if key not in p or p[key] in (None, ""):
                raise SystemExit(f"Publication {pid}: missing required field '{key}'")
        if "ko" not in p["venue"] or "en" not in p["venue"]:
            raise SystemExit(f"Publication {pid}: venue needs ko and en")
        try:
            owner_index(p["authors"])
        except ValueError:
            raise SystemExit(f"Publication {pid}: no owner (**-wrapped) author")
        hl = p.get("highlight")
        if hl:
            if hl["period"]["ko"] not in plabels_ko:
                raise SystemExit(
                    f"Publication {pid}: highlight.period.ko is not one of "
                    f"the declared research_work_periods"
                )
            if hl["period"]["en"] not in plabels_en:
                raise SystemExit(
                    f"Publication {pid}: highlight.period.en is not one of "
                    f"the declared research_work_periods"
                )
            for key in ("venue_short", "summary"):
                if key not in hl:
                    raise SystemExit(f"Publication {pid}: highlight.{key} required")

    # projects
    proj_ids = set()
    for p in projects:
        pid = p.get("id") or ""
        if not pid:
            raise SystemExit(f"Project missing id: {p!r}")
        if pid in proj_ids:
            raise SystemExit(f"Duplicate project id: {pid}")
        proj_ids.add(pid)
        for key in ("title", "period", "research_meta", "llms_line"):
            if key not in p:
                raise SystemExit(f"Project {pid}: missing '{key}'")
        if p.get("highlight"):
            for key in ("index_meta", "index_summary"):
                if key not in p:
                    raise SystemExit(f"Project {pid}: highlight requires '{key}'")
    highlighted = [p for p in projects if p.get("highlight")]
    if len(highlighted) > 5:
        raise SystemExit(f"Too many highlighted projects: {len(highlighted)} (max 5)")

    # patents
    pat_ids = set()
    for p in patents:
        pid = p.get("id") or ""
        if not pid:
            raise SystemExit(f"Patent missing id: {p!r}")
        if pid in pat_ids:
            raise SystemExit(f"Duplicate patent id: {pid}")
        pat_ids.add(pid)
        for key in ("kind", "status", "jurisdiction", "number", "title"):
            if key not in p:
                raise SystemExit(f"Patent {pid}: missing '{key}'")

    # profile
    for key in ("name_en", "name_ko", "byline", "summary_llms", "identifiers", "current_affiliations"):
        if key not in profile:
            raise SystemExit(f"profile.yml: missing '{key}'")
    for key in ("email", "orcid", "scholar_id", "github", "linkedin", "arge_url"):
        if key not in profile["identifiers"]:
            raise SystemExit(f"profile.yml: identifiers missing '{key}'")
    for aff in profile["current_affiliations"]:
        for key in ("institution", "role", "status"):
            if key not in aff:
                raise SystemExit(f"profile.yml: affiliation missing '{key}'")

    # education
    edu_ids = set()
    for e in education:
        eid = e.get("id") or ""
        if not eid:
            raise SystemExit(f"Education missing id: {e!r}")
        if eid in edu_ids:
            raise SystemExit(f"Duplicate education id: {eid}")
        edu_ids.add(eid)
        for key in ("degree", "institution", "year"):
            if key not in e:
                raise SystemExit(f"Education {eid}: missing '{key}'")
        if e.get("detail") and "detail_label" not in e:
            raise SystemExit(f"Education {eid}: detail requires detail_label")

    # career
    car_ids = set()
    for p in career:
        pid = p.get("id") or ""
        if not pid:
            raise SystemExit(f"Career missing id: {p!r}")
        if pid in car_ids:
            raise SystemExit(f"Duplicate career id: {pid}")
        car_ids.add(pid)
        for key in ("title", "employer", "period"):
            if key not in p:
                raise SystemExit(f"Career {pid}: missing '{key}'")

    # awards
    cat_ids = {c["id"] for c in award_categories}
    aw_ids = set()
    for a in awards:
        aid = a.get("id") or ""
        if not aid:
            raise SystemExit(f"Award missing id: {a!r}")
        if aid in aw_ids:
            raise SystemExit(f"Duplicate award id: {aid}")
        aw_ids.add(aid)
        for key in ("year", "category", "title", "context"):
            if key not in a:
                raise SystemExit(f"Award {aid}: missing '{key}'")
        if a["category"] not in cat_ids:
            raise SystemExit(
                f"Award {aid}: category '{a['category']}' is not one of "
                f"the declared award_categories"
            )

    # service
    for key in _SERVICE_SECTION_KEYS:
        if key not in service_data["service"]:
            raise SystemExit(f"service.yml: missing section '{key}'")
        if key not in service_data["labels"]:
            raise SystemExit(f"service.yml: missing label '{key}'")

    # courses
    co_ids = set()
    for c in courses:
        cid = c.get("id") or ""
        if not cid:
            raise SystemExit(f"Course missing id: {c!r}")
        if cid in co_ids:
            raise SystemExit(f"Duplicate course id: {cid}")
        co_ids.add(cid)
        for key in ("title", "institution", "level", "years"):
            if key not in c:
                raise SystemExit(f"Course {cid}: missing '{key}'")


# ---------- main ----------

def build() -> None:
    pub_data = load_yaml(DATA_DIR / "publications.yml")
    proj_data = load_yaml(DATA_DIR / "projects.yml")
    pat_data = load_yaml(DATA_DIR / "patents.yml")
    profile_data = load_yaml(DATA_DIR / "profile.yml")
    edu_data = load_yaml(DATA_DIR / "education.yml")
    career_data = load_yaml(DATA_DIR / "career.yml")
    awards_data = load_yaml(DATA_DIR / "awards.yml")
    service_data = load_yaml(DATA_DIR / "service.yml")
    teaching_data = load_yaml(DATA_DIR / "teaching.yml")

    publications = pub_data["publications"]
    periods = pub_data["research_work_periods"]
    projects = proj_data["projects"]
    patents = pat_data["patents"]
    profile = profile_data["profile"]
    education = edu_data["education"]
    career = career_data["career"]
    awards = awards_data["awards"]
    award_categories = awards_data["award_categories"]
    courses = teaching_data["courses"]

    validate_all(
        publications, periods, projects, patents,
        profile, education, career, awards, award_categories,
        service_data, courses,
    )

    working = [p for p in publications if p.get("status") == "in-review"]
    published = [p for p in publications if p.get("status") != "in-review"]
    years = sorted({p["year"] for p in published}, reverse=True)

    def pub_groups(lang: str, working_title: str) -> list[dict]:
        out = []
        if working:
            out.append({
                "title": working_title,
                "entries": [render_research_entry(p, lang) for p in working],
            })
        for y in years:
            out.append({
                "title": str(y),
                "entries": [
                    render_research_entry(p, lang)
                    for p in published if p["year"] == y
                ],
            })
        return out

    def llms_pub_groups() -> list[dict]:
        out = []
        if working:
            out.append({
                "title": "Working papers",
                "entries": [render_llms_entry(p) for p in working],
            })
        for y in years:
            out.append({
                "title": str(y),
                "entries": [render_llms_entry(p) for p in published if p["year"] == y],
            })
        return out

    def highlight_groups(lang: str) -> list[dict]:
        out = []
        for period in periods:
            lk = period["label"]["ko"]
            le = period["label"]["en"]
            members = [
                p for p in publications
                if p.get("highlight")
                and p["highlight"]["period"]["ko"] == lk
                and p["highlight"]["period"]["en"] == le
            ]
            members.sort(key=lambda p: p["highlight"].get("rank", 999))
            entries = [render_highlight_entry(p, lang) for p in members]
            out.append({
                "label": period["label"][lang],
                "affiliation": period["affiliation"][lang],
                "entries": entries,
            })
        return out

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    INCLUDES_DIR.mkdir(exist_ok=True)

    bodies: dict[str, str] = {}

    for lang in ("ko", "en"):
        # Existing (Tier 2)
        bodies[f"research-publications.{lang}.qmd"] = compose_research_pub_section(
            pub_groups(lang, "Working Papers")
        )
        bodies[f"research-projects.{lang}.qmd"] = compose_joined_blocks(
            [render_project_research_entry(p, lang) for p in projects]
        )
        bodies[f"research-patents.{lang}.qmd"] = compose_joined_lines(
            [render_patent_entry(p, lang) for p in patents]
        )
        bodies[f"index-research-works-highlights.{lang}.qmd"] = (
            compose_index_highlight_section(highlight_groups(lang))
        )
        bodies[f"index-projects-highlights.{lang}.qmd"] = compose_joined_blocks(
            [render_project_index_entry(p, lang) for p in projects if p.get("highlight")]
        )
        bodies[f"index-patents.{lang}.qmd"] = compose_joined_lines(
            [render_patent_entry(p, lang) for p in patents]
        )

        # New (Phase 3a)
        bodies[f"index-education.{lang}.qmd"] = compose_joined_lines(
            [render_education_entry(e, lang) for e in education]
        )
        bodies[f"index-career.{lang}.qmd"] = compose_joined_blocks(
            [render_career_entry(p, lang) for p in career]
        )
        bodies[f"index-awards.{lang}.qmd"] = compose_joined_lines(
            [render_award_entry(a, lang) for a in awards]
        )
        bodies[f"index-professional-service.{lang}.qmd"] = render_service_site(
            service_data, lang
        )

    for out_name, body in bodies.items():
        tpl = env.get_template(out_name + ".j2")
        rendered = tpl.render(body=body)
        write_text(INCLUDES_DIR / out_name, rendered)

    # llms.txt — full file, now fully data-driven
    llms_ctx = {
        "name_en": profile["name_en"],
        "name_ko": profile["name_ko"],
        "byline": profile["byline"],
        "summary": profile["summary_llms"],
        "identifiers_section": render_llms_identifiers(profile),
        "affiliations_section": render_llms_affiliations(profile),
        "education_section": compose_joined_lines(
            [render_llms_education_entry(e) for e in education]
        ),
        "career_section": compose_joined_lines(
            [render_llms_career_entry(c) for c in career]
        ),
        "pub_section": compose_llms_pub_section(llms_pub_groups()),
        "proj_section": compose_joined_lines(
            [render_project_llms_entry(p) for p in projects]
        ),
        "pat_section": compose_joined_lines(
            [render_patent_llms_entry(p) for p in patents]
        ),
        "service_section": render_service_llms(service_data),
    }
    llms_tpl = env.get_template("llms.txt.j2")
    llms_out = llms_tpl.render(**llms_ctx)
    write_text(LLMS_TXT_PATH, llms_out)

    print(
        f"{len(publications)} publications, "
        f"{len(projects)} projects, "
        f"{len(patents)} patents, "
        f"{len(education)} education, "
        f"{len(career)} career, "
        f"{len(awards)} awards, "
        f"{len(courses)} courses"
    )


if __name__ == "__main__":
    build()
