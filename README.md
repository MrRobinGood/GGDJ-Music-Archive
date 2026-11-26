# GG DJ Music Archive

All the Spotify playlists made by GG DJ, the name Robin Good uses when he plays music.

- The main page lives at **https://robingood.com/music/**
- This repository is its safe twin. GitHub Pages publishes the copy in `docs/`.

## How it works

1. Robin changes the archive only in his site folder, `robingood-com/music/`, and uploads it to robingood.com as usual.
2. Every Tuesday GitHub copies robingood.com/music into `docs/`, all by itself.
3. In the same run it saves a full-size copy of every cover, so the GitHub copy does not depend on Spotify.
4. It also asks the Internet Archive (web.archive.org) to keep a copy of the page.

You can start a copy by hand: Actions → "Copy the music archive from robingood.com" → Run workflow.

The GitHub copy tells search engines that the main version is on robingood.com, so the two pages are not counted twice.
