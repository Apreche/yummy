from django.conf.urls.defaults import *
from bookmarks.models import Bookmark

urlpatterns = patterns('',
    url(r"^tagged/(?P<slug>[\w\d]+)", "taggit.views.tagged_object_list",
        kwargs={"queryset":Bookmark.objects.all}, name="by-tag"),
)
urlpatterns += patterns('bookmarks.views',
    url(r'^$', 'global_list', name="global-list"),
    url(r'^(?P<page_number>\d+)/$', 'global_list', name="global-list-page"),
    url(r'^post/$', 'new_bookmark', name="new-bookmark"),
    url(r'^import/$', 'delicious_import', name="delicious-import"),
    url(r'^user/(?P<username>\w+)/$', 'user_list', name="user-list"),
    url(r'^user/(?P<username>\w+)/(?P<page_number>\d+)/$', 'user_list', name="user-list-page"),
)

