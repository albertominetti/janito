# Janito Web UI with Docker

The Janito repository ships a `Dockerfile` that runs the browser chat
(`janito --web`) on port **9090**, and every release publishes the image to
the GitHub Container Registry (GHCR) as `ghcr.io/joaompinto/janito`.

## Run a released image

```bash
docker run --rm -p 9090:9090 ghcr.io/joaompinto/janito:latest
# then open http://localhost:9090
```

Available tags per release: full version (`4.49.1`), `major.minor`
(`4.49`), and `latest`.

## Configuration

Config, auth and web sessions live in `~/.janito` inside the container
(`/home/appuser/.janito`). Persist them with a named volume:

```bash
docker run --rm -p 9090:9090 \
  -v janito-config:/home/appuser/.janito \
  ghcr.io/joaompinto/janito:latest
```

Protect the UI with a bearer token (see [Web UI](web-ui.md)):

```bash
docker run --rm -p 9090:9090 \
  -e JANITO_WEB_TOKEN=secret \
  -v janito-config:/home/appuser/.janito \
  ghcr.io/joaompinto/janito:latest
```

All normal `janito --web` flags still apply by overriding the command:

```bash
docker run --rm -p 9090:9090 ghcr.io/joaompinto/janito:latest \
  janito --web --web-host 0.0.0.0 --web-port 9090 --no-web-open -r -w
```

## Build locally

```bash
docker build -t janito:local .
docker run --rm -p 9090:9090 janito:local
```

The build accepts an optional version stamp (used by the release workflow
to tag the Python package version via `setuptools_scm`):

```bash
docker build --build-arg VERSION=4.49.1 -t janito:local .
```

## Publishing

`.github/workflows/docker-publish.yml` builds and pushes the image to GHCR
on every `v*` tag push and on published GitHub releases, using the release
tag (without the leading `v`) as the `VERSION` build-arg.

To verify the pipeline without cutting a release, push a `docker-test-*`
tag (or run the workflow manually): it publishes a throwaway
`test-<sha>` (or `manual-<sha>`) tag and never touches `latest` or the
version tags.
