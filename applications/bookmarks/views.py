from datetime import datetime

from django import forms
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from utils import BasicView
from BeautifulSoup import BeautifulStoneSoup

from bookmarks.models import Bookmark
from bookmarks.forms import DeliciousImportForm

def global_list(request, page_number=None):
    bookmarks = Bookmark.objects.filter(private=False)
    template_name = "bookmarks/global_list.html"
    return bookmark_list(request, bookmarks, page_number=page_number,
        template_name=template_name)

def user_list(request, username, page_number=None):
    user = get_object_or_404(User, username=username)
    bookmarks = Bookmark.objects.filter(owner=user)
    if user != request.user:
        bookmarks = bookmarks.exclude(private=True)
    template_name = "bookmarks/user_list.html"
    extra_context = {'user': user}
    return bookmark_list(request, bookmarks, page_number=page_number,
        extra_context=extra_context, template_name=template_name)

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

@login_required
@BasicView
def delicious_import(request):
    if request.method == 'POST':
        form = DeliciousImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                soup = BeautifulStoneSoup(request.FILES['delicious_html'],
                    convertEntities="html", smartQuotesTo="html")
            except TypeError:
                raise forms.ValidationError("Not a delicious HTML file")
            rows = soup.findAll(['dt','dd'])
            for row in rows:
                if row.name == 'dd':
                    continue
                else:
                    bookmark = Bookmark()
                    link = row.first()
                    bookmark.title = link.text
                    bookmark.url = link['href']
                    bookmark.owner = request.user
                    pub_date = datetime.utcfromtimestamp(int(link['add_date']))
                    bookmark.pub_date = pub_date
                    bookmark.private = link['private'] == u"1"
                    if row.find('dd'):
                        bookmark.description = row.find('dd').text
                    bookmark.save()
                    if link.has_key('tags'):
                        tags = link['tags'].split(',')
                        for tag in tags:
                            bookmark.tags.add(tag)
                        bookmark.save()
    else:
        form = DeliciousImportForm()
    template_name = "bookmarks/delicious_import.html"
    context = {'form': form}
    return(template_name, context)

