from django import forms

from .models import Entry, Screenshot

class EntryForm(forms.ModelForm):

    def save(self, user, *args, **kwargs):
        self.instance.user = user
        return super(EntryForm, self).save(*args, **kwargs)


    class Meta:

        model = Entry
        exclude = (
                'user',
                'date_added',
                'date_modified',
        )


class ScreenshotForm(forms.ModelForm):

    class Meta:

        model  = Screenshot
        exclude = ('entry', 'date_added')
