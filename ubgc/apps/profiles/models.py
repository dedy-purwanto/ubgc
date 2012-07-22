from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField

class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    photo = ThumbnailerImageField(upload_to='profiles/photo/%Y/%m/%d', 
            blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user

    @property
    def name(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created and not instance.pk == 1:
        Profile.objects.create(user=instance)

