from datetime import datetime

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from taggit.models import Tag, TaggedItem
from utils import BasicView
from BeautifulSoup import BeautifulStoneSoup

from bookmarks.models import Bookmark
from bookmarks.forms import DeliciousImportForm, NewBookmarkForm

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
    extra_context = {'list_user': user}
    return bookmark_list(request, bookmarks, page_number=page_number,
        extra_context=extra_context, template_name=template_name)

def by_tag(request, slug, username=None, page_number=None):
    tag = get_object_or_404(Tag, slug=slug)
    extra_context = {'tag': tag}
    if username:
        user = get_object_or_404(User, username=username)
        bookmarks = user.bookmark_set.all()
        if user != request.user:
            bookmarks = bookmarks.exclude(private=True)
        extra_context.update({'list_user': user})
        template_name = "bookmarks/user_list.html"
    else:
        bookmarks = Bookmark.objects.all()
        template_name = "bookmarks/global_list.html"
    bookmarks = bookmarks.filter(pk__in=TaggedItem.objects.filter(
        tag=tag, content_type=ContentType.objects.get_for_model(Bookmark)
    ).values_list("object_id", flat=True))
    
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
def new_bookmark(request):
    if request.method == 'POST':
        bookmark = Bookmark()
        form = NewBookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark.owner = request.user
            bookmark.save()
            for tag in form.cleaned_data['tags']:
                bookmark.tags.add(tag)
            bookmark.save()
            url = reverse("user-list", args=[request.user.username])
            return HttpResponseRedirect(url)
    else:
        form = NewBookmarkForm()
    template_name = "bookmarks/new_bookmark.html"
    context = {'form': form}
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
            url = reverse("user-list", args=[request.user.username])
            return HttpResponseRedirect(url)
    else:
        form = DeliciousImportForm()
    template_name = "bookmarks/delicious_import.html"
    context = {'form': form}
    return(template_name, context)

