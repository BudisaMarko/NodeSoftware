from django.conf.urls.defaults import *

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # this fetches all urls, including TAP from DjNode
    (r'', include('DjNode.urls')),
)

# Replace the base by your node name and add urls
# if you have custom views.
#urlpatterns + = patterns('DjExampleNode.node.views',
#                       (r'^$', 'index'),
#                       )

