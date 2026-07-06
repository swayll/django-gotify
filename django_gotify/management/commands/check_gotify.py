import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from gotify import Gotify


class Command(BaseCommand):
    help = "Check connection to Gotify server."

    def handle(self, *args, **options):
        url = getattr(settings, "GOTIFY_URL", "")
        token = getattr(settings, "GOTIFY_TOKEN", "")

        missing = []
        if not url:
            missing.append("GOTIFY_URL")
        if not token:
            missing.append("GOTIFY_TOKEN")

        if missing:
            self.stdout.write(self.style.ERROR(
                f"Missing Gotify settings: {', '.join(missing)}."
            ))
            self.stdout.write()
            self.stdout.write("Add the following to your Django settings.py:")
            self.stdout.write()
            self.stdout.write("    GOTIFY_URL = 'http://127.0.0.1:6543'")
            self.stdout.write("    GOTIFY_TOKEN = 'your_app_token'")
            self.stdout.write("    GOTIFY_CLIENT = 'your_client_token'  # optional")
            self.stdout.write()
            self.stdout.write("Then ensure 'django_gotify' is in INSTALLED_APPS and run this command again.")
            sys.exit(1)

        client_token = getattr(settings, "GOTIFY_CLIENT", "")

        self.stdout.write(f"Gotify URL: {url}")
        self.stdout.write(f"Gotify Token: {token[:4]}{'*' * max(0, len(token) - 8)}{token[-4:] if len(token) > 8 else ' (masked)'}")
        self.stdout.write()

        try:
            gotify = Gotify(
                base_url=url,
                app_token=token,
                client_token=client_token,
            )
            health = gotify.get_health()
            self.stdout.write(self.style.SUCCESS("Gotify connection successful!"))
            self.stdout.write(str(health))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to connect to Gotify: {e}"))
            sys.exit(1)
