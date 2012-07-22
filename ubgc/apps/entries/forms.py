from django import forms

from .models import Entry

class EntryForm(forms.ModelForm):

    def save(self, user, *args, **kwargs):
        self.instance.user = user
        super(EntryForm, self).save(*args, **kwargs)


    class Meta:
        model = Entry
        exclude = (
                'user',
                'date_added',
                'date_modified',
        )
