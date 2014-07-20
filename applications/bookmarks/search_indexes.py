import datetime
from haystack.indexes import *
from haystack import site
from bookmarks.models import Bookmark


class BookmarkIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='owner')
    pub_date = DateTimeField(model_attr='pub_date')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Bookmark.objects.exclude(private=True)


site.register(Bookmark, BookmarkIndex)