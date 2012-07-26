import os, shutil, zipfile

from django.db import models
from django.utils.encoding import smart_str
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField

from django.conf import settings

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

    # We need to append the content of index html with a js
    # to overcome cross domain security issue
    def append_content(self):
        easyXDM = """
            <script>
            var socket = new easyXDM.Socket({
                onReady:  function(){
                    socket.postMessage(document.body.scrollHeight)
                }
            });
            </script>
            """
        try:
            file_path = "%s%s" % (settings.MEDIA_ROOT, self.zip_file)
            dir_path = "%s_extract" % (file_path)
            index_html = open('%s/index.html' % dir_path, 'r')

            content = index_html.read()
            content = content.replace("</body>", "%s</body>" % easyXDM)

            index_html = open('%s/index.html' % dir_path, 'w')
            index_html.write(content)

        except IOError:
            pass

    def extract_zip_file(self):
        file_path = "%s%s" % (settings.MEDIA_ROOT, self.zip_file)
        dir_path = "%s_extract" % (file_path)
        zip_file = zipfile.ZipFile(file_path)
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path)
        zip_file.extractall(path=dir_path)

        self.append_content()

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


