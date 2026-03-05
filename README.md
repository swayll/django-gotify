# Django Gotify
[![Django CI](https://github.com/swayll/django-gotify/actions/workflows/django.yml/badge.svg)](https://github.com/swayll/django-gotify/actions/workflows/django.yml)
[![PyPI version](https://img.shields.io/pypi/v/django-gotify.svg)](https://pypi.org/project/django-gotify/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-gotify.svg)](https://pypi.org/project/django-gotify/)
[![License](https://img.shields.io/pypi/l/django-gotify.svg)](https://github.com/swayll/django-gotify/blob/main/LICENSE)

**Self-hosted push notifications and alerting for your Django projects.**

`django-gotify` is a lightweight package that integrates your Django application with a [Gotify](https://gotify.net/) server. It provides a custom Email Backend to send standard Django emails as push notifications, and a built-in Logging Handler to instantly alert your devices about server errors and warnings.

## 🚀 Features

* **Email Backend Integration**: Acts as a drop-in replacement for Django's default email backend. Send notifications using standard `send_mail()` calls.
* **Smart Logging Handler**: Automatically routes Django logs to Gotify. It intelligently maps Python log levels (DEBUG, ERROR, CRITICAL) to Gotify message priorities.
* **Thread-Safe**: Safely processes and sends multiple messages concurrently.
* **Fail Silently Support**: Respects Django's `fail_silently` flag to prevent notification errors from crashing your application.

## 📦 Installation

Install via pip:

```bash
pip install django-gotify

```

*(Note: You do not need to add this to `INSTALLED_APPS` since it only provides backend classes and handlers).*

## 🛠 Configuration & Usage

Add your Gotify server credentials to your `settings.py`:

```python
GOTIFY_URL = 'http://127.0.0.1:6543'
GOTIFY_TOKEN = 'your_app_token'       # For logging
GOTIFY_CLIENT = 'your_client_token'   # Optional

```

### 1. Using as an Email Backend

To route all outgoing Django emails to Gotify, update your email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django_gotify.email.GotifyEmailBackend'

```

Now, anytime you use Django's `send_mail()`, it will appear as a push notification:

```python
from django.core.mail import send_mail

send_mail(
    subject="New User Registration",
    message="A new user just signed up on the platform.",
    from_email=None,
    recipient_list=[], # Not required for Gotify
)

```

### 2. Using as a Logging Handler

To get real-time alerts for server errors, add the Gotify handler to your `LOGGING` configuration in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'gotify': {
            'level': 'ERROR',
            'class': 'django_gotify.log.GotifyLogHandler',
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

## 💡 How it helps

Instead of paying for third-party SMS services or cluttering your inbox with automated server emails, you can:

* **Monitor Errors Instantly**: Get a push notification on your phone the second an `HTTP 500` error occurs in production.
* **Simplify Alerts**: Trigger internal admin alerts (like "New Order Received") using Django's familiar `send_mail` functions without actually setting up an SMTP server.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://github.com/swayll/django-gotify/blob/main/LICENSE)
