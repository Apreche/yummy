from django.conf.urls.defaults import *

urlpatterns = patterns('bookmarks.views',
    url(r'^$', 'global_list', name="global-list"),
    url(r'^post/$', 'new_bookmark', name="new-bookmark"),
    url(r'^delete/(?P<id>\d+)/$', 'delete_bookmark', name="delete-bookmark"),
    url(r'^import/$', 'delicious_import', name="delicious-import"),
    url(r'^user/(?P<username>\w+)/$', 'user_list', name="user-list"),
    url(r'^user/(?P<username>\w+)/tags/(?P<tags>[\w\+\-]+)/$', "tag_list", name="user-tag-list"),
    url(r'^tags/(?P<tags>[\w\+\-]+)/$', "tag_list", name="tag-list"),
    url(r'^extensions/$', "extensions", name="extensions"),
)
