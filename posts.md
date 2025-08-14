---
layout: default
title: "Posts"
permalink: /posts.html
---
{% if site.posts.size == 0 %}
<small>No posts yet!</small>
{% else %}
{% for post in site.posts %}
[{{post.title}}]({{post.url}})
{% endfor %}
{% endif %}

