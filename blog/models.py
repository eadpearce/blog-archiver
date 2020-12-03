from django.db import models


class Blog(models.Model):
    avatar = models.JSONField()
    description = models.TextField()
    name = models.CharField(max_length=100)
    title = models.TextField()
    total_posts = models.IntegerField()
    url = models.CharField(max_length=100)
    uuid = models.CharField(primary_key=True, editable=False, max_length=100)
