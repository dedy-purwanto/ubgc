from django import forms

from .models import Entry, Screenshot, Vote

class EntryForm(forms.ModelForm):

    def save(self, user, *args, **kwargs):
        self.instance.user = user
        return super(EntryForm, self).save(*args, **kwargs)


    class Meta:

        model = Entry
        exclude = (
                'user',
                'num_votes',
                'date_added',
                'date_modified',
        )


class ScreenshotForm(forms.ModelForm):

    class Meta:

        model = Screenshot
        exclude = ('entry', 'date_added')


class VoteForm(forms.ModelForm):

    def save(self, user, entry, *args, **kwargs):
        self.instance.user = user
        self.instance.entry = entry
        return super(VoteForm, self).save(*args, **kwargs)

    class Meta:

        model = Vote
        exclude = ('entry', 'user', 'date_added',)
