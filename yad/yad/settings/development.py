from .base import *

from dotenv import load_dotenv

load_dotenv()


DEBUG = True

ALLOWED_HOSTS = json.loads(os.getenv(
    'ALLOWED_HOST',
    '["*"]'
    # '["localhost", "127.0.0.1", "[::1]", "testserver",]'
))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
