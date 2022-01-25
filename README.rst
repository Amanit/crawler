====================
Wiki Crawler Example
====================

Setup
-----
Build an image -

    `docker build -t crawler .`

Run it with default `url` / `filename`

    `docker run --volume=/tmp:/app/data crawler`

or with passed ones

    `docker run --volume=/tmp:/app/data crawler https://ru.wikipedia.org/wiki/Веб data/wiki.json`

You will find your json files in `/tmp` folder.
