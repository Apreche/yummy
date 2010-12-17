from django.conf.urls.defaults import *

urlpatterns = patterns('bookmarks.views',
    url(r'^$', 'global_list', name="global-list"),
    url(r'^(?P<page_number>\d+)$', 'global_list', name="global-list-page"),
)
