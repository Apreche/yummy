from django.conf.urls.defaults import *
from bookmarks.models import Bookmark

urlpatterns = patterns('bookmarks.views',
    url(r'^$', 'global_list', name="global-list"),
    url(r'^tagged/(?P<slug>[\w\d]+)', "by_tag", name="by-tag"),
    url(r'^(?P<page_number>\d+)/$', 'global_list', name="global-list-page"),
    url(r'^post/$', 'new_bookmark', name="new-bookmark"),
    url(r'^delete/(?P<pk>\d+)$', 'delete_bookmark', name="delete-bookmark"),
    url(r'^import/$', 'delicious_import', name="delicious-import"),
    url(r'^user/(?P<username>\w+)/$', 'user_list', name="user-list"),
    url(r'^user/(?P<username>\w+)/(?P<page_number>\d+)/$', 'user_list', name="user-list-page"),
    url(r'^user/(?P<username>\w+)/tagged/(?P<slug>[\w\d]+)', "by_tag", name="user-by-tag"),
)
