from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('alexdaphne.views',
    (r'^$', 'home'),
    (r'^maps', 'maps'),
    (r'^contact', 'contact'),
    (r'^rsvp/add', 'rsvp_add'),
    (r'^rsvp/', 'rsvp_dump'),
    (r'^thankyou', 'thankyou'),
    (r'^photos', 'photos'),
    (r'^events/(?P<event_id>\w+)/$', 'events'),
)

urlpatterns += patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(.*)$', 'django.views.static.serve',
         {'document_root' : settings.MEDIA_ROOT, 'show_indexes' : True}),
    )
