import logging
from io import StringIO
from unittest.mock import patch

from django.core.mail import EmailMessage, send_mail
from django.core.management import call_command
from django.test import TestCase

from django_gotify import GotifyEmailBackend, GotifyLogHandler, check_connection, get_gotify_client
from django_gotify.email import GotifyEmailBackend as _GotifyEmailBackend


class GotifyBackendTest(TestCase):
    @patch("django_gotify.utils.Gotify")
    def test_send_email_calls_gotify(self, MockGotify):
        mock_instance = MockGotify.return_value

        send_mail(
            "Test Subject",
            "Test Body",
            "from@example.com",
            ["to@example.com"],
            connection=GotifyEmailBackend(),
        )

        mock_instance.create_message.assert_called_once_with(
            message="Test Body", title="Test Subject", priority=None, extras=None
        )

    @patch("django_gotify.utils.Gotify")
    def test_send_email_with_priority_and_markdown(self, MockGotify):
        mock_instance = MockGotify.return_value

        msg = EmailMessage(
            "Markdown Subject",
            "**Bold** message",
            "from@example.com",
            ["to@example.com"],
            headers={"X-Gotify-Priority": "7", "X-Gotify-Markdown": "true"},
        )
        msg.connection = GotifyEmailBackend()
        msg.send()

        mock_instance.create_message.assert_called_once_with(
            message="**Bold** message",
            title="Markdown Subject",
            priority=7,
            extras={"client::display": {"contentType": "text/markdown"}},
        )

    @patch("django_gotify.utils.Gotify")
    def test_fail_silently_true(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.side_effect = Exception("Gotify down")

        backend = _GotifyEmailBackend(fail_silently=True)
        result = backend.send_messages([EmailMessage("Subject", "Body", to=["test@example.com"])])
        self.assertEqual(result, 0)

    @patch("django_gotify.utils.Gotify")
    def test_fail_silently_false(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.side_effect = Exception("Gotify down")

        backend = _GotifyEmailBackend(fail_silently=False)
        with self.assertRaises(Exception):
            backend.send_messages([EmailMessage("Subject", "Body", to=["test@example.com"])])

    @patch("django_gotify.utils.Gotify")
    def test_empty_messages(self, MockGotify):
        mock_instance = MockGotify.return_value

        backend = _GotifyEmailBackend()
        result = backend.send_messages([])
        self.assertEqual(result, 0)
        mock_instance.create_message.assert_not_called()

    @patch("django_gotify.utils.Gotify")
    def test_send_message_write_error_fail_silently(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.create_message.side_effect = Exception("Send failed")

        backend = _GotifyEmailBackend(fail_silently=True)
        result = backend.send_messages([EmailMessage("Subject", "Body", to=["test@example.com"])])
        self.assertEqual(result, 0)

    @patch("django_gotify.utils.Gotify")
    def test_invalid_priority_header(self, MockGotify):
        mock_instance = MockGotify.return_value

        msg = EmailMessage(
            "Subject",
            "Body",
            to=["test@example.com"],
            headers={"X-Gotify-Priority": "not_a_number"},
        )
        msg.connection = GotifyEmailBackend()
        msg.send()

        mock_instance.create_message.assert_called_once_with(
            message="Body", title="Subject", priority=None, extras=None
        )


class GotifyLogHandlerTest(TestCase):
    def _log_and_get_priority(self, level, message="Test message"):
        from django_gotify.log import GotifyLogHandler as Handler

        with patch("django_gotify.utils.Gotify") as MockGotify:
            mock_instance = MockGotify.return_value

            logger = logging.getLogger("test_priority_logger")
            logger.handlers.clear()
            handler = Handler(base_url="http://test.com", app_token="abc")
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            logger.log(level, message)
            return mock_instance.create_message.call_args[1]["priority"]

    def test_debug_priority(self):
        self.assertEqual(self._log_and_get_priority(logging.DEBUG), 2)

    def test_info_priority(self):
        self.assertEqual(self._log_and_get_priority(logging.INFO), 5)

    def test_warning_priority(self):
        self.assertEqual(self._log_and_get_priority(logging.WARNING), 5)

    def test_error_priority(self):
        self.assertEqual(self._log_and_get_priority(logging.ERROR), 8)

    def test_critical_priority(self):
        self.assertEqual(self._log_and_get_priority(logging.CRITICAL), 9)

    @patch("django_gotify.utils.Gotify")
    def test_logging_handler_calls_gotify(self, MockGotify):
        mock_instance = MockGotify.return_value

        logger = logging.getLogger("test_logger")
        logger.handlers.clear()
        handler = GotifyLogHandler(base_url="http://test.com", app_token="abc")
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        logger.error("Test Error Log")

        self.assertTrue(mock_instance.create_message.called)
        args, kwargs = mock_instance.create_message.call_args
        self.assertEqual(kwargs["message"], "Test Error Log")
        self.assertIn("ERROR", kwargs["title"])


class UtilsTest(TestCase):
    @patch("django_gotify.utils.Gotify")
    def test_get_gotify_client(self, MockGotify):
        get_gotify_client(
            base_url="http://g.example.com",
            app_token="tok",
            client_token="ctok",
        )
        MockGotify.assert_called_once_with(
            base_url="http://g.example.com",
            app_token="tok",
            client_token="ctok",
        )

    @patch("django_gotify.utils.Gotify")
    def test_check_connection_missing_url(self, MockGotify):
        ok, msg, health = check_connection(base_url="", app_token="tok")
        self.assertFalse(ok)
        self.assertIn("GOTIFY_URL", msg)
        self.assertIsNone(health)

    @patch("django_gotify.utils.Gotify")
    def test_check_connection_missing_token(self, MockGotify):
        ok, msg, health = check_connection(base_url="http://g.example.com", app_token="")
        self.assertFalse(ok)
        self.assertIn("GOTIFY_TOKEN", msg)
        self.assertIsNone(health)

    @patch("django_gotify.utils.Gotify")
    def test_check_connection_success(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.return_value = {"health": "green"}

        ok, msg, health = check_connection(base_url="http://g.example.com", app_token="tok")
        self.assertTrue(ok)
        self.assertEqual(health, {"health": "green"})

    @patch("django_gotify.utils.Gotify")
    def test_check_connection_server_error(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.side_effect = Exception("Connection refused")

        ok, msg, health = check_connection(base_url="http://g.example.com", app_token="tok")
        self.assertFalse(ok)
        self.assertIn("Failed to connect", msg)
        self.assertIsNone(health)


class CheckGotifyCommandTest(TestCase):
    def test_missing_url_and_token(self):
        with self.settings(GOTIFY_URL="", GOTIFY_TOKEN=""):
            out = StringIO()
            with self.assertRaises(SystemExit) as cm:
                call_command("check_gotify", stdout=out, stderr=StringIO())
            self.assertEqual(cm.exception.code, 1)
            out.seek(0)
            output = out.getvalue()
            self.assertIn("GOTIFY_URL", output)
            self.assertIn("GOTIFY_TOKEN", output)
            self.assertIn("settings.py", output)

    def test_missing_token_only(self):
        with self.settings(GOTIFY_URL="http://gotify.example.com", GOTIFY_TOKEN=""):
            out = StringIO()
            with self.assertRaises(SystemExit):
                call_command("check_gotify", stdout=out, stderr=StringIO())
            out.seek(0)
            self.assertIn("GOTIFY_TOKEN", out.getvalue())

    @patch("django_gotify.utils.Gotify")
    def test_connection_success(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.return_value = {"health": "green"}

        out = StringIO()
        call_command("check_gotify", stdout=out, stderr=StringIO())
        out.seek(0)
        output = out.getvalue()
        self.assertIn("successful", output)

    @patch("django_gotify.utils.Gotify")
    def test_connection_failed(self, MockGotify):
        mock_instance = MockGotify.return_value
        mock_instance.get_health.side_effect = Exception("Connection refused")

        out = StringIO()
        with self.assertRaises(SystemExit) as cm:
            call_command("check_gotify", stdout=out, stderr=StringIO())
        self.assertEqual(cm.exception.code, 1)
        out.seek(0)
        self.assertIn("Failed to connect", out.getvalue())
