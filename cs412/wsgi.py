"""
WSGI config for cs412 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application


def _load_env_file(env_path: Path) -> None:
	if not env_path.exists():
		return
	for raw_line in env_path.read_text(encoding='utf-8').splitlines():
		line = raw_line.strip()
		if not line or line.startswith('#') or '=' not in line:
			continue
		key, value = line.split('=', 1)
		parsed_value = value.strip().strip('"').strip("'")
		os.environ.setdefault(key.strip(), parsed_value)


# Optional secret locations for deployment and local testing.
for _path in (
	Path('/home/ugrad/ksolter/.secrets/newsapi.env'),
	Path(__file__).resolve().parent.parent / '.env',
):
	_load_env_file(_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')

application = get_wsgi_application()
