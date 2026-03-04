# Changelog

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
