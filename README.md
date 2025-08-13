## Pages
[Notes](/notes.html)
## Posts
{% if site.posts %}
{% for post in site.posts %}
[{{post.title}}]({{post.url}})
{% endfor %}
{% else %}
*No posts yet!*
{% endif %}
