---
layout: archive
title: "Notes"
permalink: /notes/
author_profile: true
---

Recent thoughts, updates, and reflections on my research, design work, and academic journey.

{% for post in site.posts %}
  <article class="blog-post">
    <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
    <div class="blog-meta">
      {{ post.date | date: "%B %d, %Y" }}
    </div>
    <div class="blog-excerpt">
      {{ post.excerpt }}
      {% if post.content != post.excerpt %}
        <a href="{{ post.url }}">Read more →</a>
      {% endif %}
    </div>
  </article>
{% endfor %}