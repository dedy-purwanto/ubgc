from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

class Entry(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    embed_code = models.TextField()
    tags = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Vote(models.Model):

    entry = models.ForeignKey(Entry)
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.entry.title, self.user)

class Screenshot(models.Model):

    entry = models.ForeignKey(Entry)
    photo = ThumbnailerImageField(upload_to='institution/photo/%Y/%m/%d')
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Screenshot %s - %s" % (self.pk, self.entry.title)
