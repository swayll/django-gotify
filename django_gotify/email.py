import threading

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from gotify import Gotify


class GotifyEmailBackend(BaseEmailBackend):
    def __init__(
        self,
        fail_silently=False,
        base_url=None,
        app_token=None,
        client_token=None,
        **kwargs,
    ):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self._lock = threading.RLock()

        # Get settings dynamically to avoid errors during Django initialization
        self.base_url = base_url or getattr(settings, "GOTIFY_URL", "")
        self.app_token = app_token or getattr(settings, "GOTIFY_TOKEN", "")
        self.client_token = client_token or getattr(settings, "GOTIFY_CLIENT", "")

        self.gotify = Gotify(
            base_url=self.base_url,
            app_token=self.app_token,
            client_token=self.client_token,
        )

    def open(self):
        try:
            self.gotify.get_health()
            return True
        except Exception as e:
            if not self.fail_silently:
                raise e
            return False

    def write_message(self, message, default_subject="No Subject"):
        body = str(message.body) if isinstance(message, EmailMessage) else str(message)
        title = (
            str(message.subject)
            if isinstance(message, EmailMessage)
            else str(default_subject)
        )

        priority = None
        extras = None

        if isinstance(message, EmailMessage):
            # Extract priority from headers if it exists
            priority_str = message.extra_headers.get("X-Gotify-Priority")
            if priority_str:
                try:
                    priority = int(priority_str)
                except (ValueError, TypeError):
                    pass

            # Markdown support
            if (
                message.content_subtype == "markdown"
                or message.extra_headers.get("X-Gotify-Markdown", "").lower() == "true"
            ):
                extras = {"client::display": {"contentType": "text/markdown"}}

        return self.gotify.create_message(
            message=body,
            title=title,
            priority=priority,
            extras=extras,
        )

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        msg_count = 0
        with self._lock:
            if not self.open():
                return 0

            for message in email_messages:
                try:
                    self.write_message(message)
                    msg_count += 1
                except Exception as e:
                    if not self.fail_silently:
                        raise e
        return msg_count
