from django import forms

class DeliciousImportForm(forms.Form):
    delicious_html = forms.FileField()
