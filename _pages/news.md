---
layout: page
permalink: /news/
title: News
nav: true
nav_order: 1
---

<div class="news-archive">
  {% assign all_news = site.news | sort: 'date' | reverse %}
  {% assign news_years = all_news | group_by_exp: 'item', "item.date | date: '%Y'" %}
  {% for year in news_years %}
    <section class="news-year" aria-labelledby="news-{{ year.name }}">
      <h2 id="news-{{ year.name }}">{{ year.name }}</h2>
      {% for item in year.items %}
        {% include personal_news_row.liquid item=item %}
      {% endfor %}
    </section>
  {% endfor %}
</div>
