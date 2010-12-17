from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404
from utils import BasicView

from bookmarks.models import Bookmark

def global_list(request, page_number=None):
    bookmarks = Bookmark.objects.filter(private=False)
    template_name = "bookmarks/global_list.html"
    return bookmark_list(request, bookmarks, page_number=page_number,
        template_name=template_name)

@BasicView
def bookmark_list(request, bookmarks, page_number=None,
        extra_context={}, template_name="bookmarks/list.html"):
    if page_number is None:
        page_number = 1
    paginator = Paginator(bookmarks, 10, allow_empty_first_page=False)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        raise Http404
    context = extra_context
    context.update({'page': page})
    return(template_name, context)
