from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from urllib.request import urlopen
from PIL import Image
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


class Reblog(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reblogs',
        null=True,
        blank=True
    )


class Block(models.Model):
    reblog = models.ForeignKey(
        Reblog,
        on_delete=models.CASCADE,
        related_name='blocks',
        null=True,
        blank=True,
    )
    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    # the following is based on code from
    # https://nikhilhaas.com/downloading-and-saving-image-to-imagefield-in-django/

    image = models.ImageField(upload_to='images', null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.url:
            image = self.download_image()

            try:
                filename = urlparse(self.url).path.split('/')[-1]
                self.image = filename
                tempfile = image
                tempfile_io = BytesIO()
                tempfile.save(tempfile_io, format=image.format)
                self.image.save(filename, ContentFile(tempfile_io.getvalue()), save=False)

            except Exception as e:
                print("Error trying to save model: saving image failed: " + str(e))
                pass

        super().save(*args, **kwargs)

    def download_image(self):
        request = urlopen(self.url, timeout=10)
        image_data = BytesIO(request.read())
        return Image.open(image_data)
