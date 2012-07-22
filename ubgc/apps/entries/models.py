from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    embed_code = models.TextField()
    tags = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)
