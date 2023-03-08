"""
WSGI config for graphs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os,sys
sys.path.append('/var/www/almgraphs/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphs.settings")
os.environ['HTTPS'] = "on"
os.environ['wsgi.url_scheme'] = 'https'
""" activate_this = '../../env/bin/activate'
exec(activate_this, dict(__file__=activate_this)) """
# exec(open("/var/www/almgraphs/env/bin/activate").read())
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphs.settings')

application = get_wsgi_application()
