from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):

    username = forms.CharField(max_length=30)
    name = forms.CharField(max_length=255)
    email_address = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        try:
            if self.instance.pk:
                self.fields['username'].initial = self.instance.user.username
                self.fields['name'].initial = self.instance.user.first_name
        
        except Profile.DoesNotExist:
            pass

    class Meta:
        model = Profile
    

