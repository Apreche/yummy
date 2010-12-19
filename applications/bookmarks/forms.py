from django import forms
from django.forms import ModelForm
from bookmarks.models import Bookmark

class DeliciousImportForm(forms.Form):
    delicious_html = forms.FileField()

class NewBookmarkForm(ModelForm):
    class Meta:
        model=Bookmark
        exclude = ('owner', 'pub_date',)
