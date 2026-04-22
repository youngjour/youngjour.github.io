// Bilingual labels for section headings and small strings used in cv.typ.
// Keyed by language ("en" | "ko"). When a third language is added, extend
// the "strings" dictionary here.
//
// Keys use snake_case so Typst's dotted-access works for every entry
// (hyphen in a Typst identifier is parsed as subtraction).

#let strings = (
  en: (
    education: "Education",
    experience: "Experience",
    awards: "Awards and Honors",
    publications: "Research and Publications",
    preprints: "Preprints (In Review)",
    journal: "Journal",
    conference: "Conference",
    workshop: "Workshop",
    poster: "Poster",
    other: "Other",
    grants: "Research Projects and Grants",
    patents: "Patents and Intellectual Property",
    service: "Professional Service",
    teaching: "Teaching",
    journal_reviewer: "Journal Reviewer",
    research_advisory: "Research Advisory",
    industry_collaborations: "Industry–Academic Collaborations",
    invited_lectures: "Invited Lectures · Seminars",
    dissertation: "Dissertation",
    thesis: "Thesis",
    conjunction: "and",
  ),
  ko: (
    education: "학력",
    experience: "경력",
    awards: "수상 및 영예",
    publications: "연구 및 논문",
    preprints: "프리프린트 (심사 중)",
    journal: "저널",
    conference: "학회",
    workshop: "워크숍",
    poster: "포스터",
    other: "기타",
    grants: "연구 프로젝트 및 연구비",
    patents: "특허 및 지적재산권",
    service: "학회 및 전문 활동",
    teaching: "강의",
    journal_reviewer: "저널 리뷰어",
    research_advisory: "연구 자문",
    industry_collaborations: "산학 협력",
    invited_lectures: "특강 · 세미나",
    dissertation: "학위논문",
    thesis: "학위논문",
    conjunction: "및",
  ),
)
