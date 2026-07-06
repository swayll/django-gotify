# Django Gotify
[![Django CI](https://github.com/swayll/django-gotify/actions/workflows/django.yml/badge.svg)](https://github.com/swayll/django-gotify/actions/workflows/django.yml)
[![PyPI version](https://img.shields.io/pypi/v/django-gotify.svg)](https://pypi.org/project/django-gotify/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-gotify.svg)](https://pypi.org/project/django-gotify/)
[![License](https://img.shields.io/pypi/l/django-gotify.svg)](https://github.com/swayll/django-gotify/blob/main/LICENSE)

**Self-hosted push notifications and alerting for your Django projects.**

`django-gotify` is a lightweight package that integrates your Django application with a [Gotify](https://gotify.net/) server. It provides a custom Email Backend to send standard Django emails as push notifications, a built-in Logging Handler to instantly alert your devices about server errors and warnings, and a management command to verify your Gotify connection.

## Features

* **Email Backend Integration**: Acts as a drop-in replacement for Django's default email backend. Send notifications using standard `send_mail()` calls.
* **Smart Logging Handler**: Automatically routes Django logs to Gotify. It intelligently maps Python log levels (DEBUG, ERROR, CRITICAL) to Gotify message priorities.
* **Connection Check**: `check_gotify` management command verifies connectivity to your Gotify server.
* **Programmatic API**: `check_connection()` and `get_gotify_client()` — reusable functions to verify connectivity and construct clients from any Python code.
* **Thread-Safe**: Safely processes and sends multiple messages concurrently.
* **Fail Silently Support**: Respects Django's `fail_silently` flag to prevent notification errors from crashing your application.
* **Markdown Support**: Send formatted messages via `X-Gotify-Markdown` header or `markdown` content subtype.

## Installation

Install via pip:

```bash
pip install django-gotify
```

*(Note: You only need to add `'django_gotify'` to `INSTALLED_APPS` temporarily to use the `check_gotify` management command. For normal backend/handler usage it is not required.)*

## Configuration

Add your Gotify server credentials to your `settings.py`:

```python
GOTIFY_URL = 'http://127.0.0.1:6543'
GOTIFY_TOKEN = 'your_app_token'       # For logging and create_message
GOTIFY_CLIENT = 'your_client_token'   # Optional, for client-authenticated endpoints
```

## Usage

### 1. Email Backend

To route all outgoing Django emails to Gotify, update your email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django_gotify.GotifyEmailBackend'
```

Now, anytime you use Django's `send_mail()`, it will appear as a push notification:

```python
from django.core.mail import send_mail

send_mail(
    subject="New User Registration",
    message="A new user just signed up on the platform.",
    from_email=None,
    recipient_list=[],  # Not required for Gotify
)
```

### 2. Logging Handler

To get real-time alerts for server errors, add the Gotify handler to your `LOGGING` configuration in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'gotify': {
            'level': 'ERROR',
            'class': 'django_gotify.GotifyLogHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['gotify', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

Log levels are automatically mapped to Gotify priorities:

| Python level | Gotify priority |
|---|---|
| DEBUG | 2 |
| INFO, WARNING | 5 |
| ERROR | 8 |
| CRITICAL | 9 |

### 3. Connection Check

#### Management command

Temporarily add `'django_gotify'` to `INSTALLED_APPS`, then run:

```bash
python manage.py check_gotify
```

The command validates that `GOTIFY_URL` and `GOTIFY_TOKEN` are configured and verifies connectivity to your Gotify server. If settings are missing, it prints guidance on how to configure them.

#### Programmatic API

Use from any Python code without adding to `INSTALLED_APPS`:

```python
from django_gotify import check_connection, get_gotify_client

# Verify connectivity
ok, message, health = check_connection()
if not ok:
    print(f"Gotify is not reachable: {message}")

# Get a configured client
client = get_gotify_client()
client.create_message(
    message="Hello from code!",
    title="Programmatic Message",
    priority=5,
)
```

### 4. Message Priority & Markdown

Control priority and formatting via `EmailMessage` headers:

```python
from django.core.mail import EmailMessage

msg = EmailMessage(
    subject="**Important** alert",
    body="Server disk usage exceeded **90%**",
    to=["ops@example.com"],
    headers={
        "X-Gotify-Priority": "8",
        "X-Gotify-Markdown": "true",
    },
)
msg.send()
```

Alternatively, use `content_subtype="markdown"` on the message.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Development setup

```bash
git clone https://github.com/swayll/django-gotify.git
cd django-gotify
python -m venv venv && source venv/bin/activate
pip install -e .
pip install -r requirements.txt
pre-commit install
```

### Running checks

```bash
python runtests.py                 # Run test suite
ruff check .                       # Lint
ruff format --check .              # Format check
ruff format .                      # Auto-format
```

## License

[MIT](https://github.com/swayll/django-gotify/blob/main/LICENSE)
