from datetime import datetime

from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from taggit.models import Tag
from utils import BasicView
from BeautifulSoup import BeautifulStoneSoup

from bookmarks.models import Bookmark
from bookmarks.forms import DeliciousImportForm, NewBookmarkForm

def global_list(request):
    bookmarks = Bookmark.objects.exclude(private=True)
    template_name = "bookmarks/global_list.html"
    return bookmark_list(request, bookmarks, template_name=template_name)

def user_list(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = Bookmark.objects.filter(owner=user)
    if user != request.user:
        bookmarks = bookmarks.exclude(private=True)
    template_name = "bookmarks/user_list.html"
    extra_context = {'list_user': user}
    return bookmark_list(request, bookmarks, extra_context=extra_context,
        template_name=template_name)

def tag_list(request, tags, username=None):
    template_name = "bookmarks/tag_list.html"
    extra_context = {}
    bookmarks = Bookmark.objects.all()

    tag_list = tags.split('+')
    tag_objects = Tag.objects.filter(slug__in=tag_list)
    if len(tag_objects) == 0:
        raise Http404
    for tag in tag_objects:
        bookmarks = bookmarks.filter(tags__in=[tag])
    extra_context.update({'tags': tag_objects})

    if username:
        user = get_object_or_404(User, username=username)
        bookmarks = bookmarks.filter(owner=user)
        if user != request.user:
            bookmarks = bookmarks.exclude(private=True)
        extra_context.update({'list_user': user})
        template_name = "bookmarks/tag_user_list.html"
    else:
        bookmarks = bookmarks.exclude(private=True)

    return bookmark_list(request, bookmarks, extra_context=extra_context,
        template_name=template_name)

@BasicView
def bookmark_list(request, bookmarks, extra_context={},
    template_name="bookmarks/list.html"):
    context = {'bookmarks': bookmarks}
    context.update(extra_context)
    return(template_name, context)

@login_required
@BasicView
def delete_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)

    if bookmark.owner == request.user:
        if request.method == "POST" and request.POST.get("confirm", "") == "true":
            bookmark.delete()
            url = reverse("user-list", args=[request.user.username])
            return HttpResponseRedirect(url)
    return ("bookmarks/delete_bookmark.html", {"bookmark": bookmark})

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
                            if len(tag) > 0:
                                bookmark.tags.add(tag)
                        bookmark.save()
            url = reverse("user-list", args=[request.user.username])
            return HttpResponseRedirect(url)
    else:
        form = DeliciousImportForm()
    template_name = "bookmarks/delicious_import.html"
    context = {'form': form}
    return(template_name, context)
