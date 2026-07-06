# Changelog

## [0.3.0] - 2026-07-06

### Added
- `check_connection()` and `get_gotify_client()` in `django_gotify.utils` — reusable programmatic API.
- `ruff` configuration for linting and formatting (`pyproject.toml`).
- `mypy` configuration (`pyproject.toml`).
- `.pre-commit-config.yaml` with `ruff` hooks.
- GitHub issue templates (bug report, feature request) and PR template.
- CI step: `ruff check` in `django.yml`.

### Changed
- `GotifyEmailBackend` and `GotifyLogHandler` now construct clients via `get_gotify_client()`.
- `check_gotify` management command delegates to `check_connection()`.
- Gotify dependency pinned to `>=0.5.0,<0.7.0` in `setup.cfg`, `==0.6.0` in `requirements.txt`.

## [0.2.0] - 2026-07-06

### Added
- `AppConfig` (`django_gotify.apps.DjangoGotifyConfig`) for proper Django integration.
- Management command `check_gotify` to verify Gotify server connectivity.
- Public exports from `django_gotify`: `GotifyEmailBackend`, `GotifyLogHandler`.
- Comprehensive test coverage: fail_silently, log priority levels (DEBUG→CRITICAL), management command.

### Changed
- `GotifyEmailBackend.write_message` renamed to `_write_message` (private API).

## [0.1.0] - 2024-05-22

### Added
- Initial release of `django-gotify`.
- `GotifyEmailBackend` for sending emails via Gotify.
- `GotifyLogHandler` for sending Django logs to Gotify.
- Support for message priority via `X-Gotify-Priority` header in emails.
- Support for Markdown content via `X-Gotify-Markdown` header or `markdown` content subtype.
- CI/CD workflow for testing with multiple Python and Django versions.

### Fixed
- Fixed CI workflow to correctly handle Django 5.0 compatibility with Python versions.
