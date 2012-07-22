from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from profiles.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                self.stdout.write("Profile %s created" % user.username)
            else:
                self.stdout.write("Profile %s already exists" % user.username)

        self.stdout.write("Done")
