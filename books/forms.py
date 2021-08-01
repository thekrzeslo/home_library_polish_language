from django import forms
from django.forms import widgets
from .models import Books

class BooksForm(forms.ModelForm):
    title = forms.CharField(label="title", widget=widgets.TextInput(attrs={"placeholder":"title"}))
    author = forms.CharField()
    description = forms.Textarea()
    type = forms.CharField()
    class Meta:
        model = Books
        fields = [
            "title",
            "author",
            "description",
            "type",
        ]

