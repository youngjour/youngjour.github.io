---
layout: archive
title: "Youngjun Park"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

<a href="javascript:generatePDF()" class="pdf-download-btn" title="Print or save as PDF">
  <i class="fas fa-download"></i>Download as PDF
</a>

{% include pdf-script.html %}

<div class="cv-contact-info">
<strong>PostDoc Researcher</strong>, Urban AI Institute, Korea Advanced Institute of Science and Technology<br>
<strong>Partner Architect</strong>, Ar-ge Architects, Inc.<br>
Email: youngjourpark@gmail.com | Phone: (+82) 10-2399-4900<br>
Seoul, South Korea
</div>

## Education

* **Ph.D in Architecture**, Seoul National University, 2022
  * Focus: Walking activities in urban parks, evidence-based urban design

* **M.S. in Urban Design**, Seoul National University, 2017
  * Thesis: Car-sharing and urban mobility in residential neighborhoods

* **B.A. in Architecture**, Seoul National University, 2013

## Professional Positions

* **PostDoc Researcher**, Urban AI Institute, KAIST (2025-present)
  * Research in urban analytics and science with Agentic AI framework
  * Manage the interdisciplinary and international research projects for Center for Advanced Urban Systems at KAIST

* **Partner Architect**, Ar-ge Architects, Inc. (2024-present)
  * Leading architectural design projects integrating computational techniques

* **PostDoc Researcher**, School of Computing, KAIST (2022-2025)
  * Research in AI-centered urban solution with smart city technologies, based on IoT and distributed computing systems
  * Cross-disciplinary collaborations in urban computing


* **Partner Architect**, Ar-ge Architects, Inc. (2024-present)
  * Leading architectural design projects integrating computational methods

* **PostDoc Researcher**, School of Computing, KAIST (2022-present)
  * Research in urban analytics, AI applications, and smart city technologies
  * Cross-disciplinary collaborations in urban computing

* **Lecturer**, Department of Architecture, Seoul National University (2021-2023)
  * "Urban Design Analysis: The Pedestrian and the City" (Graduate level in Architecture Major)
  * "Theory of Urban Design: From Classic to Today" (Graduate level in Urban Design Major)

* **Military Officer (1st Lieutenant)**, Combat Engineer, Republic of Korea Army (2013-2015)
  * Leadership and project management experience

## Technical Skills

### Programming & Data Science
* Programming Languages: Python, R, SQL
* Machine Learning: scikit-learn, TensorFlow, PyTorch
* GIS & Spatial Analysis: QGIS, ArcGIS, PostGIS, GeoPandas
* Data Visualization: Matplotlib, Plotly, CSS, Deck.gl
* AI techniques: Language Model, Graph Network, Time-Series Prediction
<!-- * Mobile Development: Android, iOS app development -->

### Urban Design & Architecture
* Design Software: ArchiCAD with BIM, AutoCAD, SketchUp, Adobe Creative Suite
* BIM & Parametric Design: ArchiCAD, Grasshopper
* Analysis Tools: OSMnx, Space Syntax, GIS Software
* Visualization: 3D rendering, architectural presentation

### Research Methods
* Statistical Analysis: Advanced statistical modeling and hypothesis testing, spatiotemporal analysis, graph network analysis
* Big Data Processing: Handling large-scale urban datasets
* Survey Design: Questionnaire development and analysis
* Field Research: Participatory community design, travel survey with GPS sensor, urban observation and video analysis

### Languages
* Korean: Native
* English: Fluent

## Publications

{% for post in site.publications reversed %}
  * **{{ post.title }}** - {{ post.venue }}, {{ post.date | date: "%Y" }}
{% endfor %}

## Research Projects

{% for post in site.research reversed %}
  * **{{ post.title }}** - {{ post.excerpt }}
{% endfor %}

## Design Projects

{% for post in site.design reversed %}
  * **{{ post.title }}** - {{ post.excerpt }}
{% endfor %}

## Talks

{% for post in site.talks reversed %}
  * **{{ post.title }}** - {{ post.venue }}, {{ post.date | date: "%Y" }}
{% endfor %}

## Teaching

{% for post in site.teaching reversed %}
  * **{{ post.title }}** - {{ post.venue }}, {{ post.date | date: "%Y" }}
{% endfor %}

## Current Research Projects

* **Center for Advanced Urban System** (2024-current)
  * KAIST, GS Engineering & Construction Corporation
  * AI-based urban system development and smart city technologies

* **AI-based Contactless Drug Detection Technology** (2024-current)
  * KAIST research project focusing on public safety applications

* **Multimodal Spatiotemporal Urban Prediction Model** (2024-current)
  * Large Language Model applications for urban analytics

## Patents & Intellectual Property

* **Korean Patent (Applied)** No.10-2024-0108083: Method and Device for Estimating House Value Using Neural Network Model
* **Korean Patent (Registered)** No.10-23679770000: Method and Server for Providing Commercial Real Estate Information
* **Korean Copyright (Registered)** C-2023-062275: Geographic Data Visualization Program

## Awards and Honors

* **G-School Best Innovation Awards** (2023) - "Spatial Awareness in Deep Learning", KAIST-NYU Young Researcher Day, Urban X
* **1st Prize, AI-based Population Prediction** (2023) - Data Analysis Competition, Korea Land & Housing Corporation
* **Thesis Award** (2018) - Master thesis, Architectural Institute of Korea
* **Young Architectural Fellowship** (2016) - Korean Institute of Architects
* **Excellent Officer Award** (2015) - Republic of Korea Army

## Professional Service

* **Reviewer**: International conferences and journals in urban planning and computer science
* **Research Consultant**: Architecture and Urban Research Institute of Korea (AURI), 2022-2023
* **Industry Collaboration**: Technology transfer and commercial applications of research