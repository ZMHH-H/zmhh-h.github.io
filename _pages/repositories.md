---
layout: page
permalink: /repositories/
description: Research code and open-source contributions.
title: Repositories
nav: true
nav_order: 4
---

<div class="repository-page">
  {% if site.data.repositories.github_users %}
    <section class="repository-summary" aria-labelledby="github-activity-heading">
      <div class="repository-summary-copy">
        <p class="repository-eyebrow">OPEN SOURCE</p>
        <h2 id="github-activity-heading">GitHub activity</h2>
        <p>Open-source work on <span class="repository-topic">embodied intelligence</span>, <span class="repository-topic">multimodal learning</span>, <span class="repository-topic">and video understanding</span>.</p>
        {% for user in site.data.repositories.github_users %}
          <a class="repository-profile-link" href="https://github.com/{{ user }}">{{ user }} on GitHub <span aria-hidden="true">↗</span></a>
        {% endfor %}
      </div>
      <div class="repository-stats">
        {% for user in site.data.repositories.github_users %}
          {% include repository/repo_user.liquid username=user %}
        {% endfor %}
      </div>
    </section>
    {% if site.repo_trophies.enabled %}
      <div class="repositories repository-trophies">
        {% for user in site.data.repositories.github_users %}
          {% include repository/repo_trophies.liquid username=user %}
        {% endfor %}
      </div>
    {% endif %}
  {% endif %}

{% if site.data.repositories.github_repos %}

<section class="repository-projects" aria-labelledby="selected-repositories-heading">
<div class="repository-section-heading">
<h2 id="selected-repositories-heading">Selected repositories</h2>
<span>{{ site.data.repositories.github_repos.size }} repositories</span>
</div>
<div class="repository-grid">
{% for repo in site.data.repositories.github_repos %}
{% include repository/repo.liquid repository=repo %}
{% endfor %}
</div>
</section>
{% endif %}

</div>
