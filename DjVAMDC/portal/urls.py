from django.conf.urls.defaults import *

urlpatterns = patterns('DjVAMDC.portal.views',
                       (r'^$', 'index'),
                       (r'^vald/',include('DjVAMDC.vald.urls')),
)
