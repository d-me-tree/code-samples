Dockerized version of [click's](https://click.palletsprojects.com/en/7.x/quickstart/#screencast-and-examples) `naval` example.

There's `settings` directory to support `--settings` command option, similar to django (see TODOs below).

## Build
```bash
docker build . --tag naval:latest
```

## Run
```bash
docker run --rm \
-e NAVAL_SETTINGS_MODULE=settings.local \
-it \
naval:latest
```

## TODOs
- Add `naval run --settings=settings.local` command example

