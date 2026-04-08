#!/bin/bash

python manage.py collectstatic --noinput || echo "Warning: collectstatic failed, continuing..."

python manage.py migrate --noinput

echo "Checking superuser..."

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
u = os.getenv('DJANGO_SUPERUSER_USERNAME')
e = os.getenv('DJANGO_SUPERUSER_EMAIL')
p = os.getenv('DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
    print(f'Superuser {u} created')
else:
    print(f'Superuser {u} already exists')
"

exec "$@"