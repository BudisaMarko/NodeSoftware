import os
import sys
sys.path.append('/vamdc/NodeSoftware')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.chianti.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
