# GG-DJ Music Archive

All the Spotify playlists made by GG DJ, the name Robin Good uses when he plays music.

- The main page lives at **https://robingood.com/music/**
- This repository is its safe twin. GitHub Pages publishes the copy in `docs/`.

## How it works

1. Robin changes the archive only in his site folder, `robingood-com/music/`, and uploads it to robingood.com as usual.
2. Once a month GitHub checks robingood.com/music. Only if the page has changed does it copy it into `docs/`. Otherwise it stops after a few seconds.
3. When it copies, it also it saves a full-size copy of every cover, so the GitHub copy does not depend on Spotify.
4. Then it asks the Internet Archive (web.archive.org) to keep a copy of the page.

You can start a copy by hand: Actions → "Copy the music archive from robingood.com" → Run workflow.

The GitHub copy tells search engines that the main version is on robingood.com, so the two pages are not counted twice.
