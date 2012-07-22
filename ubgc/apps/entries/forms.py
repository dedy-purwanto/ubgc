from django import forms

from .models import Entry

class EntryForm(forms.ModelForm):


    class Meta:
        model = Entry
        exclude = (
                'user',
                'date_added',
                'date_modified',
        )
