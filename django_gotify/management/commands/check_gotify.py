import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from ...utils import check_connection


class Command(BaseCommand):
    help = "Check connection to Gotify server."

    def handle(self, *args, **options):
        ok, message, health = check_connection()

        if not ok:
            url = getattr(settings, "GOTIFY_URL", "")
            token = getattr(settings, "GOTIFY_TOKEN", "")

            self.stdout.write(self.style.ERROR(message))
            if not url or not token:
                self.stdout.write()
                self.stdout.write("Add the following to your Django settings.py:")
                self.stdout.write()
                self.stdout.write("    GOTIFY_URL = 'http://127.0.0.1:6543'")
                self.stdout.write("    GOTIFY_TOKEN = 'your_app_token'")
                self.stdout.write("    GOTIFY_CLIENT = 'your_client_token'  # optional")
                self.stdout.write()
                self.stdout.write("Then ensure 'django_gotify' is in INSTALLED_APPS and run this command again.")
            sys.exit(1)

        token = getattr(settings, "GOTIFY_TOKEN", "")
        token_display = f"{token[:4]}{'*' * max(0, len(token) - 8)}{token[-4:] if len(token) > 8 else ' (masked)'}"
        self.stdout.write(f"Gotify URL: {getattr(settings, 'GOTIFY_URL', '')}")
        self.stdout.write(f"Gotify Token: {token_display}")
        self.stdout.write()
        self.stdout.write(self.style.SUCCESS(message))
        self.stdout.write(str(health))
