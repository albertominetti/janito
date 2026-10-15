# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/joaompinto/janito/compare/v4.49.0...HEAD)

Changes since `v4.49.0` (2026-10-15).

## [v4.49.0](https://github.com/joaompinto/janito/compare/v4.48.0...v4.49.0) - 2026-10-15

Changes since `v4.48.0` (2026-10-13).

### Added

- Meta provider: add `muse-wonder-1.0` with a 1M-token context window,
  configurable reasoning, stateless Responses support, search grounding,
  and built-in pricing.
- Google provider: add `gemini-4-argon` with a unified 1M-token context
  window, configurable reasoning, Completions and native Gemini API support,
  and built-in pricing.

### Changed

- Google provider now defaults to `gemini-3.8-flash` instead of
  `gemini-3.7-flash`.

## [v4.48.0](https://github.com/joaompinto/janito/compare/v4.47.0...v4.48.0) - 2026-10-13

Changes since `v4.47.0` (2026-10-12).

### Added

- CLI startup banner displays `Janito role is <role>` below the version,
  with the resolved session role rendered in bold green using Rich.

- `scripts/install-janito-dev.sh`: install the current source tree as the
  `janito-dev` user command (editable install into `.venv-dev` plus a
  `~/.local/bin/janito-dev` launcher). Picks the first available tool:
  `uv` > `conda` > `pip`.
- Docs: OpenAI provider section now lists the built-in models (`gpt-6.1-sol`
  default, `gpt-6-sol`, `gpt-6-luna`, `gpt-6-astra`) and documents both
  authentication modes (pay-as-you-go API key and Sign in with ChatGPT OAuth).

### Changed

- Describe Janito as an **AI Coding Agent with tools, MCP, and skills** across
  the README, documentation, package metadata, and CLI help.
