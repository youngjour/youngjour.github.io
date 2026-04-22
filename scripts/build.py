#!/usr/bin/env python3
"""Tier 2 SSOT build step.

Loads _data/*.yml, validates required fields, renders the _templates/*.j2
templates into _includes/*.qmd, and regenerates /llms.txt at the repo
root. Run before `quarto render`.
"""

from __future__ import annotations

import sys
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


# ---------- section string composition (trailing newline per section) ----------

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
    """Join entries with a blank line between (for multi-line project meta blocks)."""
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

def validate(publications, periods, projects, patents) -> None:
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


# ---------- main ----------

def build() -> None:
    pub_data = load_yaml(DATA_DIR / "publications.yml")
    proj_data = load_yaml(DATA_DIR / "projects.yml")
    pat_data = load_yaml(DATA_DIR / "patents.yml")

    publications = pub_data["publications"]
    periods = pub_data["research_work_periods"]
    projects = proj_data["projects"]
    patents = pat_data["patents"]

    validate(publications, periods, projects, patents)

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

    # Bodies (each ends with a single \n)
    bodies: dict[str, str] = {}

    for lang in ("ko", "en"):
        groups = pub_groups(lang, "Working Papers")
        bodies[f"research-publications.{lang}.qmd"] = compose_research_pub_section(groups)

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
            [
                render_project_index_entry(p, lang)
                for p in projects if p.get("highlight")
            ]
        )
        bodies[f"index-patents.{lang}.qmd"] = compose_joined_lines(
            [render_patent_entry(p, lang) for p in patents]
        )

    for out_name, body in bodies.items():
        tpl = env.get_template(out_name + ".j2")
        rendered = tpl.render(body=body)
        write_text(INCLUDES_DIR / out_name, rendered)

    # llms.txt — full file
    llms_ctx = {
        "pub_section": compose_llms_pub_section(llms_pub_groups()),
        "proj_section": compose_joined_lines([render_project_llms_entry(p) for p in projects]),
        "pat_section": compose_joined_lines([render_patent_llms_entry(p) for p in patents]),
    }
    llms_tpl = env.get_template("llms.txt.j2")
    llms_out = llms_tpl.render(**llms_ctx)
    write_text(LLMS_TXT_PATH, llms_out)

    print(
        f"{len(publications)} publications, "
        f"{len(projects)} projects, "
        f"{len(patents)} patents"
    )


if __name__ == "__main__":
    build()
