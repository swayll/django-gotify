SECRET_KEY = 'fake-key-for-testing'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_gotify',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
# Тестовые настройки для Gotify
GOTIFY_URL = 'https://example.com'
GOTIFY_TOKEN = 'test-token'
