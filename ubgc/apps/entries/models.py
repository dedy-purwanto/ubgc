from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    embed_code = models.TextField()
    tags = models.TextField()
