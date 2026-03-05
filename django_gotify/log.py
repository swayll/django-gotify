import logging

from django.conf import settings
from gotify import Gotify


class GotifyLogHandler(logging.Handler):
    def __init__(self, base_url=None, app_token=None, client_token=None):
        super().__init__()
        self.base_url = base_url or getattr(settings, "GOTIFY_URL", "")
        self.app_token = app_token or getattr(settings, "GOTIFY_TOKEN", "")
        self.client_token = client_token or getattr(settings, "GOTIFY_CLIENT", "")

        self.gotify = Gotify(
            base_url=self.base_url,
            app_token=self.app_token,
            client_token=self.client_token,
        )

    def emit(self, record):
        try:
            msg = self.format(record)
            title = f"Django Log: {record.levelname} - {record.name}"

            priority = 5
            if record.levelno >= logging.CRITICAL:
                priority = 9
            elif record.levelno >= logging.ERROR:
                priority = 8
            elif record.levelno <= logging.DEBUG:
                priority = 2

            self.gotify.create_message(message=msg, title=title, priority=priority)
        except Exception:
            self.handleError(record)
