---
layout: page
permalink: /cv/
title: CV
nav: false
nav_order: 5
description: Education and research experience.
---

## Minghao Zhu · 朱铭皓

Physical AI, embodied foundation models, and video understanding.

[Email](mailto:zmhh_h@126.com) · [GitHub](https://github.com/ZMHH-H)

## Research and education

{% for experience in site.data.homepage.experiences %}

### {{ experience.organization }}

**{{ experience.role }}**
{% if experience.advisors %} · Advisors: {% for advisor in experience.advisors %}[{{ advisor.name }}]({{ advisor.url }}){% unless forloop.last %}, {% endunless %}{% endfor %}{% endif %}

{{ experience.period }}

{{ experience.description }}
{% endfor %}

## Publications

See the [publication list]({{ '/publications/' | relative_url }}).
