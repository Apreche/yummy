from django.contrib import admin
from bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)

admin.site.register(Bookmark, BookmarkAdmin)
