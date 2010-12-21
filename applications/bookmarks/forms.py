from django import forms
from django.forms import ModelForm
from bookmarks.models import Bookmark

class DeliciousImportForm(forms.Form):
    delicious_html = forms.FileField()

class NewBookmarkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        initial_url = kwargs.pop("initial_url", None)
        initial_title = kwargs.pop("initial_title", None)
        super(NewBookmarkForm, self).__init__(*args, **kwargs)
        self.fields["url"].initial = initial_url
        self.fields["title"].initial = initial_title

    class Meta:
        model=Bookmark
        exclude = ('owner', 'pub_date',)
