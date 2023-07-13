from django.contrib.auth.hashers import make_password
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BierCheck24/settings.py')
settings.configure()


password = 'Passwort123!'
hashed_password = make_password(password)

print(hashed_password)