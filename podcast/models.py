from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import timedelta
from django.conf import settings

class PodcastSeries(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class PodcastEpisode(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    series = models.ForeignKey(PodcastSeries, on_delete=models.CASCADE, related_name='episodes', null=True, blank=True)
    audio_file = models.FileField(upload_to='podcasts/audio/')
    transcript = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='episodes')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=timedelta(seconds=0))



    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while PodcastEpisode.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

