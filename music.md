---
layout: music
title: Music
date: 2025-10-23 09:37:00 -0700
---

<div id="static-music-list" class="music-list">
{% for track in site.data.music-index.tracks %}
 <div class="music-track dropdown-container">
    <p class="music-header dropdown-header">
    <!--<button class="dropdown">V</button>-->
    {% if track.tracknumber != null %}
    <span class="tracknumber">{{ track.tracknumber }}</span>
    {% endif %}
    <span class="music-name">{{ track.title }}</span>
    <span class="spacer"></span>
    <span class="music-type">{{ track.type }}</span>
    <a class="music-download" href="{{ track.path }}" download>Download</a>
    </p>
    <div class="dropdown-content">
        <ul class="music-games">
            {% for game in track.games %}
                <li>{{ game }}</li>
            {% endfor %}
        </ul>
        <span class="music-file"><audio controls src="{{ track.path }}"><i>Audio playback not supported. Click <a href="{{ track.path }}">here</a> to attempt to play it in your browser.</i></audio></span>
    </div>
 </div>
{% endfor %}
</div>
