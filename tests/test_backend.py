import logging
from unittest.mock import patch

from django.core.mail import send_mail
from django.test import TestCase

from django_gotify.email import GotifyEmailBackend


class GotifyBackendTest(TestCase):
    @patch("django_gotify.email.Gotify")
    def test_send_email_calls_gotify(self, MockGotify):
        """Проверка, что send_mail вызывает метод create_message в Gotify"""
        mock_instance = MockGotify.return_value

        # Отправляем письмо через наш бэкенд
        send_mail(
            "Test Subject",
            "Test Body",
            "from@example.com",
            ["to@example.com"],
            connection=GotifyEmailBackend(),
        )

        # Проверяем, что Gotify.create_message был вызван с правильными аргументами
        mock_instance.create_message.assert_called_once_with(
            message="Test Body", title="Test Subject"
        )

    @patch("django_gotify.log.Gotify")
    def test_logging_handler_calls_gotify(self, MockGotify):
        """Проверка, что логгер отправляет сообщения в Gotify"""
        mock_instance = MockGotify.return_value
        from django_gotify.log import GotifyLogHandler

        # Настраиваем логгер вручную для теста
        logger = logging.getLogger("test_logger")
        handler = GotifyLogHandler(base_url="http://test.com", app_token="abc")
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        # Генерируем ошибку
        logger.error("Test Error Log")

        # Проверяем вызов
        self.assertTrue(mock_instance.create_message.called)
        args, kwargs = mock_instance.create_message.call_args
        self.assertEqual(kwargs["message"], "Test Error Log")
        self.assertIn("ERROR", kwargs["title"])
