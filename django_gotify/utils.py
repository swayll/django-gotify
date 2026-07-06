from django.conf import settings
from gotify import Gotify
from gotify.errors import GotifyConfigurationError, GotifyError


def get_gotify_client(base_url=None, app_token=None, client_token=None):
    return Gotify(
        base_url=getattr(settings, "GOTIFY_URL", "") if base_url is None else base_url,
        app_token=getattr(settings, "GOTIFY_TOKEN", "") if app_token is None else app_token,
        client_token=getattr(settings, "GOTIFY_CLIENT", "") if client_token is None else client_token,
    )


def check_connection(base_url=None, app_token=None, client_token=None):
    base_url = getattr(settings, "GOTIFY_URL", "") if base_url is None else base_url
    app_token = getattr(settings, "GOTIFY_TOKEN", "") if app_token is None else app_token
    client_token = getattr(settings, "GOTIFY_CLIENT", "") if client_token is None else client_token

    if not base_url:
        return False, "GOTIFY_URL is not configured.", None
    if not app_token:
        return False, "GOTIFY_TOKEN is not configured.", None

    try:
        gotify = get_gotify_client(
            base_url=base_url,
            app_token=app_token,
            client_token=client_token,
        )
        health = gotify.get_health()
        return True, "Gotify connection successful.", health
    except GotifyConfigurationError as e:
        return False, f"Gotify configuration error: {e}", None
    except GotifyError as e:
        return False, f"Gotify server error: {e}", None
    except Exception as e:
        return False, f"Failed to connect: {e}", None
