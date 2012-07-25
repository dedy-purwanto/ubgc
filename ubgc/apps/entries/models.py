from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField

class Entry(models.Model):

    user = models.ForeignKey(User, related_name='entries')
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.TextField()
    disabled = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    num_votes = models.IntegerField(default=0)
    zip_file = models.FileField(upload_to='entries/zip_file/%Y/%m/%d')
    

    def calculate_votes(self, is_delete=False):
        self.num_votes = self.votes.all().count()
        if is_delete:
            self.num_votes -= 1
        self.save()

    def extract_zip_file(self):
        pass

    @property
    def slug(self):
        return slugify(self.title)
    
    @property
    def tag_list(self):
        return self.tags.split(",")

    def __unicode__(self):
        return self.title
    
    class Meta:

        ordering = ('title',)


class Vote(models.Model):

    entry = models.ForeignKey(Entry, related_name='votes')
    user = models.ForeignKey(User, related_name='votes')
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                vote = Vote.objects.get(entry=self.entry, user=self.user)
                if vote:
                    raise Exception("Another vote object with this data already exists")
            except Vote.DoesNotExist:
                pass

        return super(Vote, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s" % (self.entry.title, self.user)


@receiver(post_save, sender=Vote)
def vote_post_save(sender, instance, created, **kwargs):
    if created:
        instance.entry.calculate_votes()

@receiver(pre_delete, sender=Vote)
def vote_pre_delete(sender, instance, **kwargs):
    instance.entry.calculate_votes(is_delete=True)


class Screenshot(models.Model):

    entry = models.ForeignKey(Entry, related_name='photos')
    photo = ThumbnailerImageField(upload_to='entries/photo/%Y/%m/%d')
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Screenshot %s - %s" % (self.pk, self.entry.title)


