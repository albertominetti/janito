# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/joaompinto/janito/compare/v4.47.0...HEAD)

Changes since `v4.47.0` (2026-10-12).

### Added

- `scripts/install-janito-dev.sh`: install the current source tree as the
  `janito-dev` user command (editable install into `.venv-dev` plus a
  `~/.local/bin/janito-dev` launcher). Picks the first available tool:
  `uv` > `conda` > `pip`.
