---
layout: page
permalink: /publications/
description: Research papers on embodied intelligence and video understanding.
title: Publications
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications home-publications">

{% include publication_contribution_note.liquid %}

{% bibliography --file home-papers --group_by none --template home_publication %}

</div>
