---
layout: single
title: "Notes"
permalink: /notes/
author_profile: true
---

Recent thoughts, updates, and reflections on my research, design work, and academic journey.

{% for post in site.posts %}
  <article class="blog-post">
    <h3>{{ post.title }}</h3>
    <div class="blog-meta">
      {{ post.date | date: "%B %d, %Y" }}
    </div>
    <div class="blog-content">
      {{ post.content }}
    </div>
    {% unless forloop.last %}
      <hr style="margin: 2em 0; border: none; border-top: 2px solid #eee;">
    {% endunless %}
  </article>
{% endfor %}