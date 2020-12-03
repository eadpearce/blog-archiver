from django.db import models
from blog.models import Blog


class Post(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    id = models.IntegerField(primary_key=True, editable=False)
    type = models.CharField(max_length=100)
    post_url = models.URLField()
    tags = models.JSONField(null=True, blank=True)
    summary = models.TextField()
    source_url = models.URLField(null=True, blank=True)
    content = models.JSONField(null=True, blank=True)
    layout = models.JSONField(null=True, blank=True)
    trail = models.JSONField(null=True, blank=True)
