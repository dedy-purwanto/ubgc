import magic

from django import forms

from .models import Entry, Screenshot, Vote

class EntryForm(forms.ModelForm):

    def save(self, user, *args, **kwargs):
        self.instance.user = user
        entry = super(EntryForm, self).save(*args, **kwargs)


        return entry

    def clean_zip_file(self, *args, **kwargs):
        zip_file = self.cleaned_data['zip_file']

        file_path = zip_file.temporary_file_path()
        m = magic.Magic(mime=True)
        mimetype = m.from_file(file_path)

        if not mimetype == "application/zip":
            raise forms.ValidationError("The file must be in zip format")

        return zip_file

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
