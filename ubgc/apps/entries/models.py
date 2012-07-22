from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

class Entry(models.Model):

    user = models.ForeignKey(User, related_name='entries')
    title = models.CharField(max_length=255)
    description = models.TextField()
    embed_code = models.TextField()
    tags = models.TextField()
    disabled = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Vote(models.Model):

    entry = models.ForeignKey(Entry, related_name='votes')
    user = models.ForeignKey(User, related_name='votes')
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.entry.title, self.user)


class Screenshot(models.Model):

    entry = models.ForeignKey(Entry)
    photo = ThumbnailerImageField(upload_to='entries/photo/%Y/%m/%d')
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Screenshot %s - %s" % (self.pk, self.entry.title)
